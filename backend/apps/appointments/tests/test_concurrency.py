"""
Concurrency test for the booking flow. Verifies that when two threads try to
book the same slot simultaneously, exactly one succeeds and the other is
rejected with SlotConflictError (thanks to select_for_update locking).
"""
from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import connections
from django.test import TransactionTestCase
from django.utils import timezone

from apps.appointments.models import Appointment
from apps.appointments.services import (
    BookingInput,
    SlotConflictError,
    book_appointment,
)
from apps.clinics.models import Clinic
from apps.patients.models import Patient
from apps.services.models import Service


class ConcurrentBookingTest(TransactionTestCase):
    """Run against a real transaction-capable backend (postgres in CI, sqlite local)."""

    def setUp(self) -> None:
        User = get_user_model()
        self.user = User.objects.create_user(
            email="conc@test.com", password="x", full_name="Conc"
        )
        self.clinic = Clinic.objects.create(
            owner=self.user, name="Conc Clinic", timezone="Asia/Tashkent"
        )
        self.service = Service.objects.create(
            clinic=self.clinic, name="Svc", duration_minutes=30, price=0
        )
        self.p1 = Patient.objects.create(
            clinic=self.clinic, full_name="P1", phone="+11111"
        )
        self.p2 = Patient.objects.create(
            clinic=self.clinic, full_name="P2", phone="+22222"
        )
        self.slot = (timezone.now() + timedelta(days=1)).replace(
            hour=10, minute=0, second=0, microsecond=0
        )

    def _book(self, patient: Patient, barrier: threading.Barrier):
        """Worker: wait on the barrier then attempt to book the slot."""
        barrier.wait(timeout=5)
        try:
            return book_appointment(
                BookingInput(
                    clinic=self.clinic,
                    patient=patient,
                    service=self.service,
                    starts_at=self.slot,
                )
            )
        except SlotConflictError:
            return "conflict"
        finally:
            # Close the thread-local DB connection
            connections.close_all()

    def test_concurrent_booking_serializes(self) -> None:
        barrier = threading.Barrier(2)
        with ThreadPoolExecutor(max_workers=2) as pool:
            f1 = pool.submit(self._book, self.p1, barrier)
            f2 = pool.submit(self._book, self.p2, barrier)
            r1, r2 = f1.result(), f2.result()

        outcomes = [r1, r2]
        successes = [o for o in outcomes if isinstance(o, Appointment)]
        conflicts = [o for o in outcomes if o == "conflict"]

        assert len(successes) == 1, f"expected 1 success, got {outcomes}"
        assert len(conflicts) == 1, f"expected 1 conflict, got {outcomes}"
        assert Appointment.objects.filter(clinic=self.clinic).count() == 1
