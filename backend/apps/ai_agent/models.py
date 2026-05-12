from django.db import models

from apps.clinics.models import Clinic
from core.models import TimeStampedModel


class ChatSession(TimeStampedModel):
    """Represents a single chat conversation with the AI agent."""

    clinic = models.ForeignKey(
        Clinic, on_delete=models.CASCADE, related_name="chat_sessions"
    )
    session_key = models.CharField(max_length=64, unique=True, db_index=True)
    visitor_name = models.CharField(max_length=150, blank=True)
    visitor_phone = models.CharField(max_length=32, blank=True)

    def __str__(self) -> str:
        return f"Chat {self.session_key} ({self.clinic.name})"


class ChatMessage(TimeStampedModel):
    class Role(models.TextChoices):
        USER = "user", "User"
        ASSISTANT = "assistant", "Assistant"
        TOOL = "tool", "Tool"
        SYSTEM = "system", "System"

    session = models.ForeignKey(
        ChatSession, on_delete=models.CASCADE, related_name="messages"
    )
    role = models.CharField(max_length=16, choices=Role.choices)
    content = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ("created_at",)
        indexes = [models.Index(fields=["session", "created_at"])]

    def __str__(self) -> str:
        return f"{self.role}: {self.content[:40]}"
