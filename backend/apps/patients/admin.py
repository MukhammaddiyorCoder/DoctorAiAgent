from django.contrib import admin

from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "clinic", "created_at")
    list_filter = ("clinic", "gender")
    search_fields = ("full_name", "phone", "email")
