"""
Celery application for Doctor AI Agent.
"""
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

app = Celery("doctor_ai")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Periodic tasks (also manageable at runtime via django-celery-beat admin)
app.conf.beat_schedule = {
    "schedule-tomorrow-reminders-hourly": {
        "task": "apps.notifications.tasks.schedule_tomorrow_reminders",
        "schedule": crontab(minute=0),  # top of every hour
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self) -> None:
    print(f"Request: {self.request!r}")
