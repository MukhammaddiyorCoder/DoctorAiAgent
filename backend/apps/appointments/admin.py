from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "clinic",
        "patient",
        "service",
        "starts_at",
        "ends_at",
        "status",
        "source",
    )
    list_filter = ("status", "source", "clinic")
    search_fields = ("patient__full_name", "patient__phone")
    date_hierarchy = "starts_at"
