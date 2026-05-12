from django.apps import AppConfig


class AppointmentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.appointments"
    label = "appointments"

    def ready(self) -> None:  # pragma: no cover
        from . import signals  # noqa: F401
