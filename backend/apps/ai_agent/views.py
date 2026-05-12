from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.clinics.models import Clinic

from .agent import run_agent
from .models import ChatMessage, ChatSession
from .serializers import ChatRequestSerializer, ChatResponseSerializer


class ChatAPIView(APIView):
    """REST endpoint for sending a message to the AI chatbot."""

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        clinic = get_object_or_404(Clinic, slug=data["clinic_slug"])
        if not clinic.ai_enabled:
            return Response(
                {"detail": "AI is disabled for this clinic."},
                status=status.HTTP_403_FORBIDDEN,
            )

        session, _ = ChatSession.objects.get_or_create(
            session_key=data["session_key"], defaults={"clinic": clinic}
        )

        # Persist user message
        ChatMessage.objects.create(
            session=session, role=ChatMessage.Role.USER, content=data["message"]
        )

        # Build conversation history for the agent
        history = [
            {"role": m.role, "content": m.content}
            for m in session.messages.filter(
                role__in=[ChatMessage.Role.USER, ChatMessage.Role.ASSISTANT]
            ).order_by("created_at")
        ]

        reply = run_agent(clinic=clinic, messages=history)

        ChatMessage.objects.create(
            session=session, role=ChatMessage.Role.ASSISTANT, content=reply
        )

        return Response(ChatResponseSerializer({"reply": reply}).data)
