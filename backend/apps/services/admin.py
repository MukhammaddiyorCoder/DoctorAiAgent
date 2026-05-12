from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "clinic", "duration_minutes", "price", "is_active")
    list_filter = ("is_active", "clinic")
    search_fields = ("name", "clinic__name")
