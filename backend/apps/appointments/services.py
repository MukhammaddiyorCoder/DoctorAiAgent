"""
Business logic for appointments. Contains the concurrent-booking-safe
create/reschedule helpers.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from django.db import transaction
from django.db.models import Q
from django.utils import timezone as djtz
from rest_framework.exceptions import ValidationError

from apps.clinics.models import Clinic
from apps.patients.models import Patient
from apps.services.models import Service

from .models import Appointment


class SlotConflictError(ValidationError):
    default_detail = "Selected time slot is no longer available."
    default_code = "slot_conflict"


@dataclass
class BookingInput:
    clinic: Clinic
    patient: Patient
    service: Service
    starts_at: datetime
    note: str = ""
    source: str = Appointment.Source.MANUAL


def _conflicts_qs(
    clinic: Clinic, starts_at: datetime, ends_at: datetime, exclude_id: int | None = None
):
    qs = Appointment.objects.filter(
        clinic=clinic,
        status__in=[Appointment.Status.PENDING, Appointment.Status.CONFIRMED],
    ).filter(
        # overlap: existing.starts < new.ends AND existing.ends > new.starts
        Q(starts_at__lt=ends_at) & Q(ends_at__gt=starts_at)
    )
    if exclude_id:
        qs = qs.exclude(pk=exclude_id)
    return qs


def validate_within_working_hours(clinic: Clinic, starts_at: datetime, ends_at: datetime) -> None:
    """Ensure slot is inside clinic working hours (in the clinic's local timezone)."""
    try:
        tz = ZoneInfo(clinic.timezone)
    except Exception:
        tz = djtz.get_current_timezone()
    local_start = starts_at.astimezone(tz) if djtz.is_aware(starts_at) else starts_at
    local_end = ends_at.astimezone(tz) if djtz.is_aware(ends_at) else ends_at

    if local_start.date() != local_end.date():
        raise ValidationError(
            {"starts_at": "Appointment cannot span multiple days."}
        )
    if local_start.time() < clinic.work_start or local_end.time() > clinic.work_end:
        raise ValidationError(
            {"starts_at": "Time is outside of clinic working hours."}
        )


@transaction.atomic
def book_appointment(data: BookingInput) -> Appointment:
    """
    Book an appointment while protecting against concurrent races.

    Uses ``select_for_update`` on any overlapping appointments for the same
    clinic to serialize conflicting bookings.
    """
    if data.service.clinic_id != data.clinic.id:
        raise ValidationError({"service": "Service does not belong to this clinic."})

    starts_at = data.starts_at
    ends_at = starts_at + timedelta(minutes=data.service.duration_minutes)

    validate_within_working_hours(data.clinic, starts_at, ends_at)

    # Lock any overlapping rows to avoid race conditions
    conflicts = list(
        _conflicts_qs(data.clinic, starts_at, ends_at).select_for_update()
    )
    if conflicts:
        raise SlotConflictError()

    appointment = Appointment.objects.create(
        clinic=data.clinic,
        patient=data.patient,
        service=data.service,
        starts_at=starts_at,
        ends_at=ends_at,
        note=data.note,
        source=data.source,
        status=Appointment.Status.PENDING,
    )
    return appointment


@transaction.atomic
def reschedule_appointment(appointment: Appointment, starts_at: datetime) -> Appointment:
    ends_at = starts_at + timedelta(minutes=appointment.service.duration_minutes)
    validate_within_working_hours(appointment.clinic, starts_at, ends_at)

    conflicts = list(
        _conflicts_qs(
            appointment.clinic, starts_at, ends_at, exclude_id=appointment.id
        ).select_for_update()
    )
    if conflicts:
        raise SlotConflictError()

    appointment.starts_at = starts_at
    appointment.ends_at = ends_at
    appointment.save(update_fields=["starts_at", "ends_at", "updated_at"])
    return appointment
