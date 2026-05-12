"""
Claude AI agent wrapper. Runs a tool-use loop against the Anthropic SDK and
returns the assistant's final text response.
"""
from __future__ import annotations

import logging
from typing import Any

from django.conf import settings

from apps.clinics.models import Clinic

from .tools import TOOL_DEFINITIONS, run_tool

logger = logging.getLogger(__name__)

DEFAULT_SYSTEM_PROMPT = (
    "You are a friendly medical clinic assistant for {clinic_name}. "
    "Help patients book appointments by asking for their name, phone, "
    "desired service, and preferred time. Use the provided tools to list "
    "services, check availability and create bookings. Confirm details "
    "before finalizing. Respond in the same language the user writes in "
    "(prefer Uzbek if unclear). Keep responses concise."
)


def _build_system_prompt(clinic: Clinic) -> str:
    if clinic.ai_system_prompt:
        return clinic.ai_system_prompt
    return DEFAULT_SYSTEM_PROMPT.format(clinic_name=clinic.name)


def run_agent(clinic: Clinic, messages: list[dict[str, Any]]) -> str:
    """
    Run one turn of the agent against the given conversation history.
    ``messages`` should follow Anthropic's message format.
    Returns the final text response.
    """
    if not settings.ANTHROPIC_API_KEY:
        return (
            "AI is not configured. Please set ANTHROPIC_API_KEY in the environment."
        )

    try:
        import anthropic
    except ImportError:  # pragma: no cover
        return "Anthropic SDK not installed."

    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    system_prompt = _build_system_prompt(clinic)

    working_messages = list(messages)

    # Tool-use loop. At most 5 iterations to avoid runaways.
    for _ in range(5):
        response = client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=1024,
            system=system_prompt,
            tools=TOOL_DEFINITIONS,
            messages=working_messages,
        )

        if response.stop_reason == "tool_use":
            tool_results_content: list[dict[str, Any]] = []
            assistant_content: list[dict[str, Any]] = []
            for block in response.content:
                block_dict = block.model_dump() if hasattr(block, "model_dump") else block
                assistant_content.append(block_dict)
                if block_dict.get("type") == "tool_use":
                    result = run_tool(
                        name=block_dict["name"],
                        clinic=clinic,
                        arguments=block_dict.get("input", {}) or {},
                    )
                    tool_results_content.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block_dict["id"],
                            "content": str(result),
                        }
                    )

            working_messages.append({"role": "assistant", "content": assistant_content})
            working_messages.append({"role": "user", "content": tool_results_content})
            continue

        # Final text response
        text_parts: list[str] = []
        for block in response.content:
            block_dict = block.model_dump() if hasattr(block, "model_dump") else block
            if block_dict.get("type") == "text":
                text_parts.append(block_dict.get("text", ""))
        return "\n".join(text_parts).strip() or "..."

    return "I couldn't complete the request. Please try again."
