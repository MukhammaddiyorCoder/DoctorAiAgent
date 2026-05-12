from django.db import models

from apps.clinics.models import Clinic
from core.models import TimeStampedModel


class Plan(TimeStampedModel):
    class Tier(models.TextChoices):
        FREE = "free", "Free"
        PRO = "pro", "Pro"
        BUSINESS = "business", "Business"

    name = models.CharField(max_length=50)
    tier = models.CharField(max_length=16, choices=Tier.choices, unique=True)
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=8, default="USD")
    max_appointments_per_month = models.PositiveIntegerField(default=100)
    max_ai_messages_per_month = models.PositiveIntegerField(default=500)
    features = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ("price_monthly",)

    def __str__(self) -> str:
        return self.name


class Subscription(TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        PAST_DUE = "past_due", "Past Due"
        CANCELLED = "cancelled", "Cancelled"

    clinic = models.OneToOneField(
        Clinic, on_delete=models.CASCADE, related_name="subscription"
    )
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name="subscriptions")
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.ACTIVE
    )
    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.clinic.name} - {self.plan.name}"
