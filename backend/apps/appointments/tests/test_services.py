"""
Tests for the appointment booking service layer.
"""
from datetime import timedelta

import pytest

from apps.appointments.models import Appointment
from apps.appointments.services import (
    BookingInput,
    SlotConflictError,
    book_appointment,
    reschedule_appointment,
)


pytestmark = pytest.mark.django_db


def test_book_appointment_happy_path(clinic, service, patient, tomorrow_10am):
    appt = book_appointment(
        BookingInput(
            clinic=clinic,
            patient=patient,
            service=service,
            starts_at=tomorrow_10am,
        )
    )
    assert appt.pk is not None
    assert appt.ends_at == tomorrow_10am + timedelta(minutes=service.duration_minutes)
    assert appt.status == Appointment.Status.PENDING


def test_book_appointment_rejects_overlap(
    clinic, service, patient, tomorrow_10am
):
    book_appointment(
        BookingInput(
            clinic=clinic,
            patient=patient,
            service=service,
            starts_at=tomorrow_10am,
        )
    )
    # Same slot -> conflict
    with pytest.raises(SlotConflictError):
        book_appointment(
            BookingInput(
                clinic=clinic,
                patient=patient,
                service=service,
                starts_at=tomorrow_10am,
            )
        )


def test_book_appointment_rejects_partial_overlap(
    clinic, service, patient, tomorrow_10am
):
    book_appointment(
        BookingInput(
            clinic=clinic,
            patient=patient,
            service=service,
            starts_at=tomorrow_10am,
        )
    )
    # 15 min later overlaps with 30-minute service
    with pytest.raises(SlotConflictError):
        book_appointment(
            BookingInput(
                clinic=clinic,
                patient=patient,
                service=service,
                starts_at=tomorrow_10am + timedelta(minutes=15),
            )
        )


def test_book_appointment_allows_adjacent_slot(
    clinic, service, patient, tomorrow_10am
):
    book_appointment(
        BookingInput(
            clinic=clinic,
            patient=patient,
            service=service,
            starts_at=tomorrow_10am,
        )
    )
    # Exactly back-to-back should be fine
    appt = book_appointment(
        BookingInput(
            clinic=clinic,
            patient=patient,
            service=service,
            starts_at=tomorrow_10am + timedelta(minutes=30),
        )
    )
    assert appt.pk is not None


def test_book_appointment_outside_working_hours(clinic, service, patient, tomorrow_10am):
    # Before 09:00 -> invalid
    before_hours = tomorrow_10am.replace(hour=7, minute=0)
    from rest_framework.exceptions import ValidationError

    with pytest.raises(ValidationError):
        book_appointment(
            BookingInput(
                clinic=clinic,
                patient=patient,
                service=service,
                starts_at=before_hours,
            )
        )


def test_cancelled_appointment_does_not_block_slot(
    clinic, service, patient, tomorrow_10am
):
    appt = book_appointment(
        BookingInput(
            clinic=clinic,
            patient=patient,
            service=service,
            starts_at=tomorrow_10am,
        )
    )
    appt.status = Appointment.Status.CANCELLED
    appt.save()

    # Same slot should now be bookable
    new_appt = book_appointment(
        BookingInput(
            clinic=clinic,
            patient=patient,
            service=service,
            starts_at=tomorrow_10am,
        )
    )
    assert new_appt.pk != appt.pk


def test_reschedule_appointment(clinic, service, patient, tomorrow_10am):
    appt = book_appointment(
        BookingInput(
            clinic=clinic,
            patient=patient,
            service=service,
            starts_at=tomorrow_10am,
        )
    )
    new_start = tomorrow_10am + timedelta(hours=2)
    reschedule_appointment(appt, new_start)
    appt.refresh_from_db()
    assert appt.starts_at == new_start
