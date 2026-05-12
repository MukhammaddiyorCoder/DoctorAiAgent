from django.contrib import admin

from .models import ChatMessage, ChatSession


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ("session_key", "clinic", "visitor_name", "created_at")
    search_fields = ("session_key", "visitor_name", "visitor_phone")
    list_filter = ("clinic",)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("session", "role", "content", "created_at")
    list_filter = ("role",)
