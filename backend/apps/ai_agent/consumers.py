import json
import uuid

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from apps.clinics.models import Clinic

from .agent import run_agent
from .models import ChatMessage, ChatSession


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket endpoint at ws://.../ws/chat/{clinic_slug}/

    Client messages:
        {"type": "message", "text": "...", "session_key": "..."}

    Server messages:
        {"type": "assistant", "text": "..."}
        {"type": "error",     "text": "..."}
    """

    async def connect(self) -> None:
        self.slug = self.scope["url_route"]["kwargs"]["slug"]
        self.clinic = await self._get_clinic(self.slug)
        if self.clinic is None:
            await self.close(code=4404)
            return
        await self.accept()
        await self.send_json(
            {"type": "system", "text": self.clinic.ai_welcome_message}
        )

    async def disconnect(self, code: int) -> None:  # noqa: D401
        pass

    async def receive_json(self, content: dict, **kwargs) -> None:
        msg_type = content.get("type", "message")
        if msg_type != "message":
            return

        text = (content.get("text") or "").strip()
        if not text:
            return

        session_key = content.get("session_key") or uuid.uuid4().hex
        session = await self._get_or_create_session(session_key)

        await self._save_message(session, "user", text)

        history = await self._history(session)
        reply = await sync_to_async(run_agent, thread_sensitive=False)(
            self.clinic, history
        )

        await self._save_message(session, "assistant", reply)
        await self.send_json({"type": "assistant", "text": reply, "session_key": session_key})

    # -- DB helpers ----------------------------------------------------------
    @sync_to_async
    def _get_clinic(self, slug: str):
        return Clinic.objects.filter(slug=slug, ai_enabled=True).first()

    @sync_to_async
    def _get_or_create_session(self, session_key: str) -> ChatSession:
        obj, _ = ChatSession.objects.get_or_create(
            session_key=session_key, defaults={"clinic": self.clinic}
        )
        return obj

    @sync_to_async
    def _save_message(self, session: ChatSession, role: str, content: str) -> None:
        ChatMessage.objects.create(session=session, role=role, content=content)

    @sync_to_async
    def _history(self, session: ChatSession) -> list[dict]:
        return [
            {"role": m.role, "content": m.content}
            for m in session.messages.filter(
                role__in=[ChatMessage.Role.USER, ChatMessage.Role.ASSISTANT]
            ).order_by("created_at")
        ]


def _json(data: dict) -> str:  # pragma: no cover
    return json.dumps(data, ensure_ascii=False)
