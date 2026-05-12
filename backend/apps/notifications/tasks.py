from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone

logger = get_task_logger(__name__)


@shared_task
def send_appointment_reminder(appointment_id: int) -> str:
    """Send an SMS/email reminder for a single appointment."""
    from apps.appointments.models import Appointment

    try:
        appt = Appointment.objects.select_related("patient", "clinic").get(
            pk=appointment_id
        )
    except Appointment.DoesNotExist:
        return "not_found"

    # In a real implementation, integrate SMS / email providers here.
    logger.info(
        "[reminder] %s -> %s at %s",
        appt.clinic.name,
        appt.patient.phone,
        appt.starts_at.isoformat(),
    )

    Notification = _notification_model()
    Notification.objects.create(
        user=appt.clinic.owner,
        kind=Notification.Kind.APPOINTMENT,
        title="Eslatma",
        body=(
            f"Ertaga: {appt.patient.full_name} — {appt.service.name} "
            f"({appt.starts_at:%H:%M})"
        ),
        data={"appointment_id": appt.id},
    )
    return "sent"


@shared_task
def schedule_tomorrow_reminders() -> int:
    """
    Periodic task: enqueue a reminder for every confirmed/pending appointment
    that starts within the next 24 hours. Runs hourly via Celery Beat.
    """
    from apps.appointments.models import Appointment

    now = timezone.now()
    window_end = now + timezone.timedelta(hours=24)

    qs = Appointment.objects.filter(
        starts_at__gte=now,
        starts_at__lte=window_end,
        status__in=[Appointment.Status.PENDING, Appointment.Status.CONFIRMED],
    ).values_list("id", flat=True)

    count = 0
    for appt_id in qs:
        send_appointment_reminder.delay(appt_id)
        count += 1
    logger.info("Scheduled %s reminder(s)", count)
    return count


def _notification_model():
    from apps.notifications.models import Notification

    return Notification
