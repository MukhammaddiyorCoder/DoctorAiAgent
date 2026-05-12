"""
Signals for appointments. Creates notifications for clinic owners on key
lifecycle events.
"""
from __future__ import annotations

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notifications.models import Notification

from .models import Appointment


@receiver(post_save, sender=Appointment)
def notify_owner_on_appointment_change(
    sender, instance: Appointment, created: bool, **kwargs
) -> None:
    """Notify the clinic owner when a new appointment is created or status changes."""
    owner = instance.clinic.owner

    if created:
        title = "Yangi uchrashuv"
        source_label = {
            Appointment.Source.AI: "AI chatbot",
            Appointment.Source.PUBLIC: "Ommaviy forma",
            Appointment.Source.MANUAL: "Admin",
        }.get(instance.source, instance.source)
        body = (
            f"{instance.patient.full_name} — {instance.service.name} "
            f"({source_label}) {instance.starts_at:%Y-%m-%d %H:%M}"
        )
    elif instance.status == Appointment.Status.CANCELLED:
        title = "Uchrashuv bekor qilindi"
        body = (
            f"{instance.patient.full_name} — "
            f"{instance.starts_at:%Y-%m-%d %H:%M}"
        )
    else:
        return

    Notification.objects.create(
        user=owner,
        kind=Notification.Kind.APPOINTMENT,
        title=title,
        body=body,
        data={
            "appointment_id": instance.id,
            "status": instance.status,
            "source": instance.source,
        },
    )
