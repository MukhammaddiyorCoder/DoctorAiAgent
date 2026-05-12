"""
Tool definitions passed to Claude (tool-use pattern) and their server-side
handlers. Each tool returns a JSON-serializable dict.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from django.utils import timezone as djtz
from django.utils.dateparse import parse_datetime

from apps.appointments.models import Appointment
from apps.appointments.services import BookingInput, SlotConflictError, book_appointment
from apps.clinics.models import Clinic
from apps.patients.models import Patient
from apps.services.models import Service

TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "name": "list_services",
        "description": "List all active medical services offered by the clinic.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "list_available_slots",
        "description": (
            "List available time slots for a given service on a given date. "
            "Date should be in YYYY-MM-DD format."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "service_id": {"type": "integer"},
                "date": {"type": "string", "description": "YYYY-MM-DD"},
            },
            "required": ["service_id", "date"],
        },
    },
    {
        "name": "book_appointment",
        "description": (
            "Book an appointment for a patient. If the patient does not exist, "
            "one will be created using full_name and phone."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "full_name": {"type": "string"},
                "phone": {"type": "string"},
                "service_id": {"type": "integer"},
                "starts_at": {
                    "type": "string",
                    "description": "ISO 8601 datetime, e.g. 2025-06-01T10:00:00",
                },
                "note": {"type": "string"},
            },
            "required": ["full_name", "phone", "service_id", "starts_at"],
        },
    },
]


# --------------------------------------------------------------------------- #
# Tool handlers
# --------------------------------------------------------------------------- #
def tool_list_services(clinic: Clinic, **_: Any) -> dict:
    services = Service.objects.filter(clinic=clinic, is_active=True)
    return {
        "services": [
            {
                "id": s.id,
                "name": s.name,
                "duration_minutes": s.duration_minutes,
                "price": str(s.price),
                "currency": s.currency,
            }
            for s in services
        ]
    }


def tool_list_available_slots(clinic: Clinic, service_id: int, date: str, **_: Any) -> dict:
    try:
        service = Service.objects.get(id=service_id, clinic=clinic, is_active=True)
    except Service.DoesNotExist:
        return {"error": "Service not found."}

    try:
        tz = ZoneInfo(clinic.timezone)
    except Exception:
        tz = djtz.get_current_timezone()

    day = datetime.strptime(date, "%Y-%m-%d").date()
    start_of_day = datetime.combine(day, clinic.work_start, tzinfo=tz)
    end_of_day = datetime.combine(day, clinic.work_end, tzinfo=tz)
    step = timedelta(minutes=clinic.slot_duration_minutes)
    duration = timedelta(minutes=service.duration_minutes)

    booked = list(
        Appointment.objects.filter(
            clinic=clinic,
            starts_at__gte=start_of_day,
            starts_at__lt=end_of_day,
            status__in=[Appointment.Status.PENDING, Appointment.Status.CONFIRMED],
        ).values_list("starts_at", "ends_at")
    )

    now = djtz.now()
    slots: list[str] = []
    cursor = start_of_day
    while cursor + duration <= end_of_day:
        slot_end = cursor + duration
        if cursor >= now:
            conflict = any(s < slot_end and e > cursor for s, e in booked)
            if not conflict:
                slots.append(cursor.isoformat())
        cursor += step

    return {"slots": slots[:20], "service_name": service.name}


def tool_book_appointment(
    clinic: Clinic,
    full_name: str,
    phone: str,
    service_id: int,
    starts_at: str,
    note: str = "",
    **_: Any,
) -> dict:
    try:
        service = Service.objects.get(id=service_id, clinic=clinic, is_active=True)
    except Service.DoesNotExist:
        return {"error": "Service not found."}

    starts = parse_datetime(starts_at)
    if starts is None:
        return {"error": "Invalid datetime format. Use ISO 8601."}
    if djtz.is_naive(starts):
        try:
            tz = ZoneInfo(clinic.timezone)
        except Exception:
            tz = djtz.get_current_timezone()
        starts = starts.replace(tzinfo=tz)

    patient, _ = Patient.objects.get_or_create(
        clinic=clinic,
        phone=phone,
        defaults={"full_name": full_name},
    )

    try:
        appt = book_appointment(
            BookingInput(
                clinic=clinic,
                patient=patient,
                service=service,
                starts_at=starts,
                note=note,
                source=Appointment.Source.AI,
            )
        )
    except SlotConflictError:
        return {"error": "The requested time slot is no longer available."}
    except Exception as exc:  # pragma: no cover
        return {"error": str(exc)}

    return {
        "appointment_id": appt.id,
        "status": appt.status,
        "starts_at": appt.starts_at.isoformat(),
        "ends_at": appt.ends_at.isoformat(),
    }


TOOL_HANDLERS = {
    "list_services": tool_list_services,
    "list_available_slots": tool_list_available_slots,
    "book_appointment": tool_book_appointment,
}


def run_tool(name: str, clinic: Clinic, arguments: dict) -> dict:
    handler = TOOL_HANDLERS.get(name)
    if handler is None:
        return {"error": f"Unknown tool: {name}"}
    return handler(clinic=clinic, **arguments)
