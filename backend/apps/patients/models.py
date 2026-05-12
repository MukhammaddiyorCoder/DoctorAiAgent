from django.db import models

from apps.clinics.models import Clinic
from core.models import TimeStampedModel


class Patient(TimeStampedModel):
    """A patient registered at a clinic."""

    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "other", "Other"

    clinic = models.ForeignKey(
        Clinic, on_delete=models.CASCADE, related_name="patients"
    )
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=32)
    email = models.EmailField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=8, choices=Gender.choices, blank=True
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ("full_name",)
        constraints = [
            models.UniqueConstraint(
                fields=("clinic", "phone"),
                name="unique_patient_phone_per_clinic",
            )
        ]
        indexes = [models.Index(fields=["clinic", "phone"])]

    def __str__(self) -> str:
        return self.full_name
