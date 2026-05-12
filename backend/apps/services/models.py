from django.db import models

from apps.clinics.models import Clinic
from core.models import TimeStampedModel


class Service(TimeStampedModel):
    """A medical service offered by a clinic."""

    clinic = models.ForeignKey(
        Clinic, on_delete=models.CASCADE, related_name="services"
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    duration_minutes = models.PositiveSmallIntegerField(default=30)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=8, default="UZS")

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)
        indexes = [models.Index(fields=["clinic", "is_active"])]

    def __str__(self) -> str:
        return f"{self.clinic.name} - {self.name}"
