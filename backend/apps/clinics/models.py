from django.conf import settings
from django.db import models
from django.utils.text import slugify

from core.models import TimeStampedModel


class Clinic(TimeStampedModel):
    """A clinic owned by a user (OWNER role)."""

    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clinic",
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True, blank=True)

    phone = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to="clinics/logo/", blank=True, null=True)

    description = models.TextField(blank=True)
    timezone = models.CharField(max_length=64, default="Asia/Tashkent")

    # Booking settings
    work_start = models.TimeField(default="09:00")
    work_end = models.TimeField(default="18:00")
    slot_duration_minutes = models.PositiveSmallIntegerField(default=30)

    # AI settings
    ai_enabled = models.BooleanField(default=True)
    ai_system_prompt = models.TextField(
        blank=True,
        help_text="Custom system prompt for the clinic's AI agent.",
    )
    ai_welcome_message = models.CharField(
        max_length=500,
        default="Assalomu alaykum! Men sizga uchrashuvni bron qilishda yordam beraman.",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or "clinic"
            slug = base
            i = 1
            while Clinic.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
