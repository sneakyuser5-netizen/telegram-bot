"""Business-focused AI engine with short-lived conversation history."""

from services.interpreter import interpret
from services.service_engine import get_service_response
from services.context_manager import (
    add_message,
    get_context,
    get_history,
    set_context,
)
from services.ai_router import ask_ai_provider
from services.business_knowledge import BUSINESS


BUSINESS_KEYWORDS = (
    "bca", "biz connect", "academy", "referral", "register",
    "registration", "premium vpn", "vpn", "vpn file", "vpn files",
    "training", "niu", "identification number", "free files",
    "service", "services", "offer", "offers", "price", "cost",
    "fee", "pay", "payment", "whisperer", "contact", "support",
    "whatsapp", "telegram", "account", "how do i join",
    "how can i join", "how to join", "subscribe",
)


def _remember(chat_id: int, message: str, response: str) -> str:
    """Store a completed exchange and return its response."""
    add_message(chat_id, "user", message)
    add_message(chat_id, "assistant", response)
    return response


def _is_business_related(message: str) -> bool:
    """Allow free-form AI questions that relate to our official services."""
    lowered = message.casefold()
    return any(keyword in lowered for keyword in BUSINESS_KEYWORDS)


def _redirect_response() -> str:
    """Build a service menu using authoritative business data."""
    services = BUSINESS["services"]
    bca = services["bca"]
    premium_vpn = services["vpn_premium"]
    vpn_training = services["vpn_training"]
    niu = services["niu"]

    return (
        "I'm here to help you with The-Whisperer's official services 😊\\n\\n"
        "You can explore:\\n"
        f"• {bca['name']} — registration: {bca['price']}\\n"
        f"• {premium_vpn['name']} — {premium_vpn['price']} for "
        f"{premium_vpn['duration']}, with {premium_vpn['daily_data']}\\n"
        f"• {vpn_training['name']} — price {vpn_training['price']}\\n"
        f"• {services['free_files']['name']}\\n"
        f"• {niu['name']} — service fee: {niu['price']}\\n"
        f"• {services['support']['name']}\\n\\n"
        "Which service would you like to know more about?"
    )


def ask(chat_id: int, message: str) -> str:
    """Answer service intents or use AI with recent conversation history."""
    if not message or not message.strip():
        return "Please send a message."

    message = message.strip()
    result = interpret(chat_id, message)
    intent = result.get("intent", "general")

    # Capture earlier history before recording the current user message.
    history = get_history(chat_id)
    context = get_context(chat_id)

    # Known intents use authoritative business responses.
    response = get_service_response(chat_id, intent)
    if response:
        return _remember(chat_id, message, response)

    # Follow-ups need context to be meaningful.
    if intent == "follow_up":
        if context and context.get("topic"):
            topic = context["topic"]
            set_context(chat_id, topic, context.get("state", "general"))
            try:
                response = ask_ai_provider(chat_id, message, history=history)
            except Exception:
                response = ""
            if response and response.strip():
                return _remember(chat_id, message, response.strip())

        response = (
            "Of course 😊 Which of The-Whisperer's services are you asking about: "
            "BCA, Premium VPN, VPN Training, Free VPN Files, or NIU Assistance?"
        )
        return _remember(chat_id, message, response)

    # A new message may continue the current business conversation even
    # when the intent classifier doesn't recognize a specific service.
    if not _is_business_related(message):
        return _remember(chat_id, message, _redirect_response())

    # Use AI for natural business-related questions, with previous turns.
    response = ask_ai_provider(chat_id, message, history=history)

    if not response or not response.strip():
        response = (
            "I can help you explore The-Whisperer's official services. "
            "Which service are you interested in?"
        )

    return _remember(chat_id, message, response.strip())
