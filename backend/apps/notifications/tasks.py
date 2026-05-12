from celery import shared_task


@shared_task
def send_appointment_reminder(appointment_id: int) -> None:
    """Stub: send an SMS/email reminder for an appointment."""
    from apps.appointments.models import Appointment

    try:
        appt = Appointment.objects.select_related("patient", "clinic").get(
            pk=appointment_id
        )
    except Appointment.DoesNotExist:
        return

    # In a real implementation integrate SMS/email providers here.
    print(
        f"[reminder] {appt.clinic.name} -> {appt.patient.phone} "
        f"at {appt.starts_at:%Y-%m-%d %H:%M}"
    )
