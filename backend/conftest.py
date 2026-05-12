"""
Project-wide pytest fixtures.
"""
from __future__ import annotations

from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient

from apps.clinics.models import Clinic
from apps.patients.models import Patient
from apps.services.models import Service


User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="owner@test.com",
        password="testpass123",
        full_name="Test Owner",
    )


@pytest.fixture
def clinic(db, user):
    return Clinic.objects.create(
        owner=user,
        name="Test Clinic",
        timezone="Asia/Tashkent",
    )


@pytest.fixture
def service(db, clinic):
    return Service.objects.create(
        clinic=clinic,
        name="Konsultatsiya",
        duration_minutes=30,
        price=100000,
    )


@pytest.fixture
def patient(db, clinic):
    return Patient.objects.create(
        clinic=clinic,
        full_name="Test Patient",
        phone="+998900000001",
    )


@pytest.fixture
def api(db, user):
    """Authenticated APIClient for the default owner."""
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def tomorrow_10am(clinic):
    """A timezone-aware datetime at 10:00 tomorrow in the clinic's timezone."""
    now = timezone.now()
    target = (now + timedelta(days=1)).replace(
        hour=10, minute=0, second=0, microsecond=0
    )
    return target
