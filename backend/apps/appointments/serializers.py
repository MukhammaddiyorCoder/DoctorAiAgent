from rest_framework import serializers

from apps.patients.models import Patient
from apps.services.models import Service

from .models import Appointment
from .services import BookingInput, book_appointment, reschedule_appointment


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.full_name", read_only=True)
    service_name = serializers.CharField(source="service.name", read_only=True)

    class Meta:
        model = Appointment
        fields = (
            "id",
            "patient",
            "patient_name",
            "service",
            "service_name",
            "starts_at",
            "ends_at",
            "status",
            "source",
            "note",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "ends_at", "source", "created_at", "updated_at")

    def validate_patient(self, value: Patient) -> Patient:
        user = self.context["request"].user
        if value.clinic.owner_id != user.id:
            raise serializers.ValidationError("Patient does not belong to your clinic.")
        return value

    def validate_service(self, value: Service) -> Service:
        user = self.context["request"].user
        if value.clinic.owner_id != user.id:
            raise serializers.ValidationError("Service does not belong to your clinic.")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        return book_appointment(
            BookingInput(
                clinic=user.clinic,
                patient=validated_data["patient"],
                service=validated_data["service"],
                starts_at=validated_data["starts_at"],
                note=validated_data.get("note", ""),
                source=Appointment.Source.MANUAL,
            )
        )

    def update(self, instance: Appointment, validated_data):
        new_start = validated_data.get("starts_at")
        if new_start and new_start != instance.starts_at:
            reschedule_appointment(instance, new_start)
        for field in ("status", "note"):
            if field in validated_data:
                setattr(instance, field, validated_data[field])
        instance.save()
        return instance


class PublicAppointmentCreateSerializer(serializers.Serializer):
    """Public/AI booking payload. Creates patient on the fly if needed."""

    full_name = serializers.CharField(max_length=150)
    phone = serializers.CharField(max_length=32)
    email = serializers.EmailField(required=False, allow_blank=True)
    service_id = serializers.IntegerField()
    starts_at = serializers.DateTimeField()
    note = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        clinic = self.context["clinic"]
        try:
            attrs["service"] = Service.objects.get(
                id=attrs["service_id"], clinic=clinic, is_active=True
            )
        except Service.DoesNotExist as exc:  # noqa: PERF203
            raise serializers.ValidationError(
                {"service_id": "Invalid service for this clinic."}
            ) from exc
        return attrs

    def create(self, validated_data):
        clinic = self.context["clinic"]
        patient, _ = Patient.objects.get_or_create(
            clinic=clinic,
            phone=validated_data["phone"],
            defaults={
                "full_name": validated_data["full_name"],
                "email": validated_data.get("email", ""),
            },
        )
        return book_appointment(
            BookingInput(
                clinic=clinic,
                patient=patient,
                service=validated_data["service"],
                starts_at=validated_data["starts_at"],
                note=validated_data.get("note", ""),
                source=Appointment.Source.PUBLIC,
            )
        )
