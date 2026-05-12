from rest_framework import serializers

from .models import Clinic


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = (
            "id",
            "name",
            "slug",
            "phone",
            "email",
            "address",
            "website",
            "logo",
            "description",
            "timezone",
            "work_start",
            "work_end",
            "slot_duration_minutes",
            "ai_enabled",
            "ai_system_prompt",
            "ai_welcome_message",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "slug", "created_at", "updated_at")


class PublicClinicSerializer(serializers.ModelSerializer):
    """Public-facing fields only (for /public/clinic/{slug}/)."""

    class Meta:
        model = Clinic
        fields = (
            "name",
            "slug",
            "phone",
            "email",
            "address",
            "website",
            "logo",
            "description",
            "work_start",
            "work_end",
            "ai_welcome_message",
        )
