from django.db import models

from apps.clinics.models import Clinic
from apps.patients.models import Patient
from apps.services.models import Service
from core.models import TimeStampedModel


class Appointment(TimeStampedModel):
    """A booked appointment for a patient at a clinic."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"
        NO_SHOW = "no_show", "No-Show"

    class Source(models.TextChoices):
        MANUAL = "manual", "Manual"
        AI = "ai", "AI Agent"
        PUBLIC = "public", "Public Form"

    clinic = models.ForeignKey(
        Clinic, on_delete=models.CASCADE, related_name="appointments"
    )
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="appointments"
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="appointments",
    )

    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()

    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.PENDING
    )
    source = models.CharField(
        max_length=16, choices=Source.choices, default=Source.MANUAL
    )

    note = models.TextField(blank=True)

    class Meta:
        ordering = ("-starts_at",)
        indexes = [
            models.Index(fields=["clinic", "starts_at"]),
            models.Index(fields=["status"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(ends_at__gt=models.F("starts_at")),
                name="appointment_ends_after_starts",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.patient.full_name} - {self.starts_at:%Y-%m-%d %H:%M}"
