"""
Tests for the appointments REST API and public booking endpoint.
"""
from datetime import timedelta

import pytest

from apps.appointments.models import Appointment
from apps.notifications.models import Notification


pytestmark = pytest.mark.django_db


def test_create_appointment_via_api(api, clinic, service, patient, tomorrow_10am):
    resp = api.post(
        "/api/v1/appointments/",
        {
            "patient": patient.id,
            "service": service.id,
            "starts_at": tomorrow_10am.isoformat(),
            "note": "first visit",
        },
        format="json",
    )
    assert resp.status_code == 201, resp.content
    appt = Appointment.objects.get(pk=resp.data["id"])
    assert appt.clinic == clinic
    assert appt.source == Appointment.Source.MANUAL


def test_appointment_signal_creates_notification(
    api, user, clinic, service, patient, tomorrow_10am
):
    api.post(
        "/api/v1/appointments/",
        {
            "patient": patient.id,
            "service": service.id,
            "starts_at": tomorrow_10am.isoformat(),
        },
        format="json",
    )
    assert Notification.objects.filter(
        user=user, kind=Notification.Kind.APPOINTMENT
    ).exists()


def test_public_booking_endpoint_creates_patient_and_appointment(
    client, clinic, service, tomorrow_10am
):
    resp = client.post(
        f"/api/v1/public/clinic/{clinic.slug}/book/",
        {
            "full_name": "Walk-in Patient",
            "phone": "+998905555555",
            "service_id": service.id,
            "starts_at": tomorrow_10am.isoformat(),
        },
        content_type="application/json",
    )
    assert resp.status_code == 201, resp.content
    appt = Appointment.objects.get(pk=resp.json()["id"])
    assert appt.source == Appointment.Source.PUBLIC
    assert appt.patient.phone == "+998905555555"


def test_stats_endpoint(api, clinic, service, patient, tomorrow_10am):
    from apps.appointments.services import BookingInput, book_appointment

    book_appointment(
        BookingInput(
            clinic=clinic, patient=patient, service=service, starts_at=tomorrow_10am
        )
    )

    resp = api.get("/api/v1/appointments/stats/")
    assert resp.status_code == 200
    assert resp.data["total"] >= 1
    assert resp.data["upcoming"] >= 1


def test_user_cannot_see_other_clinic_appointments(
    api, clinic, service, patient, tomorrow_10am
):
    from django.contrib.auth import get_user_model

    from apps.appointments.services import BookingInput, book_appointment
    from apps.clinics.models import Clinic

    # Create another user + clinic + appointment
    User = get_user_model()
    other = User.objects.create_user(email="other@test.com", password="x")
    other_clinic = Clinic.objects.create(owner=other, name="Other")
    from apps.patients.models import Patient
    from apps.services.models import Service

    other_svc = Service.objects.create(
        clinic=other_clinic, name="X", duration_minutes=30, price=0
    )
    other_patient = Patient.objects.create(
        clinic=other_clinic, full_name="X", phone="+111"
    )
    book_appointment(
        BookingInput(
            clinic=other_clinic,
            patient=other_patient,
            service=other_svc,
            starts_at=tomorrow_10am + timedelta(hours=3),
        )
    )

    # First user's list should not contain other clinic's data
    resp = api.get("/api/v1/appointments/")
    assert resp.status_code == 200
    for a in resp.data["results"]:
        assert a["service"] != other_svc.id
