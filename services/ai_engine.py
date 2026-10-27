"""Conversational AI engine for Whisper AI."""

from services.interpreter import interpret
from services.context_manager import (
    add_message,
    get_context,
    get_history,
    set_context,
)
from services.ai_router import ask_ai_provider
from services.business_knowledge import BUSINESS
from services.service_engine import get_service_response


INTENT_TOPICS = {
    "bca": "bca",
    "vpn_premium": "vpn_premium",
    "vpn_training": "vpn_training",
    "free_files": "free_files",
    "niu_service": "niu",
    "niu_explain": "niu",
    "support": "support",
    "services": "services",
    "services_explain_all": "services",
}


def _remember(chat_id: int, message: str, response: str) -> str:
    """Store the exchange and return the response."""
    add_message(chat_id, "user", message)
    add_message(chat_id, "assistant", response)
    return response


def _fallback_response() -> str:
    """Provide a useful fallback if every AI provider fails."""
    return (
        "I'm sorry, I'm having trouble responding right now. "
        "Please try again shortly or contact The-Whisperer on "
        f"Telegram {BUSINESS['contact']['telegram']} or "
        f"WhatsApp {BUSINESS['contact']['whatsapp']}."
    )


def ask(chat_id: int, message: str) -> str:
    """Answer naturally using official facts and conversation history."""
    if not message or not message.strip():
        return "Please send a message."

    message = message.strip()
    result = interpret(chat_id, message)
    intent = result.get("intent", "general")

    # Capture earlier turns before adding the current message.
    history = get_history(chat_id)
    context = get_context(chat_id)

    # Answer expiry questions without inventing an expiry period.
    if intent == "free_files":
        expiry_terms = (
            "expir", "expiry", "expire", "validity", "valid until",
            "date limite", "expiration", "expire le", "durée de validité",
        )
        if any(term in message.lower() for term in expiry_terms):
            if any(term in message.lower() for term in (
                "date limite", "expiration", "durée de validité",
            )):
                response = (
                    "Je n'ai pas d'information confirmée sur la date "
                    "d'expiration des fichiers VPN gratuits. "
                    "Vérifiez les détails du fichier ou contactez le support "
                    "pour confirmation."
                )
            else:
                response = (
                    "I don't have verified information about when the free "
                    "VPN files expire. Please check the file details or "
                    "contact support to confirm."
                )
            return _remember(chat_id, message, response)

    # Use the predefined response for Free VPN Files.
    # This prevents the AI from inventing external download links.
    if intent == "free_files":
        response = get_service_response(chat_id, intent)
        if response:
            return _remember(chat_id, message, response)

    # Update the topic when a service is clearly identified.
    topic = INTENT_TOPICS.get(intent)
    if topic:
        set_context(chat_id, topic)

    # Preserve the current topic for follow-up questions.
    elif context and context.get("topic"):
        set_context(
            chat_id,
            context["topic"],
            context.get("state", "general"),
        )

    try:
        response = ask_ai_provider(
            chat_id,
            message,
            history=history,
        )
    except Exception:
        response = ""

    if not response or not response.strip():
        response = _fallback_response()

    return _remember(chat_id, message, response.strip())
