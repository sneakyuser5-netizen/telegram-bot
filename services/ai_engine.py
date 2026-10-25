from services.interpreter import interpret
from services.service_engine import get_service_response
from services.context_manager import get_context
from services.ai_router import ask_ai_provider


def ask(chat_id: int, message: str) -> str:
    """
    Return a business response when an intent is recognized.
    Otherwise, use the configured AI provider fallback chain.
    """
    if not message or not message.strip():
        return "Please send a message."

    result = interpret(chat_id, message)
    intent = result.get("intent", "general")

    # Answer known business intents before using an AI provider.
    response = get_service_response(chat_id, intent)
    if response:
        return response

    # Handle short follow-up replies using saved conversation context.
    if intent == "follow_up":
        context = get_context(chat_id)

        if context:
            topic = context.get("topic")

            if topic == "bca":
                return (
                    "🎉 Great!\n\n"
                    "To register for BCA:\n\n"
                    "1️⃣ Open the registration link.\n"
                    "2️⃣ Complete the form.\n"
                    "3️⃣ Pay the registration fee.\n"
                    "4️⃣ Your account will be activated.\n\n"
                    "Would you also like me to explain how the referral system works?"
                )

            if topic == "vpn_premium":
                return (
                    "🚀 To activate Premium VPN, simply contact "
                    "The-Whisperer using the bot menu."
                )

            if topic == "vpn_training":
                return (
                    "📡 The VPN training starts from beginner level "
                    "and teaches you everything needed to create your own VPN files."
                )

            if topic == "niu":
                return (
                    "🆔 The-Whisperer can help you obtain your NIU "
                    "quickly and legally.\n\n"
                    "Would you like me to explain the application process?"
                )

    # Unknown questions go through the provider fallback chain.
    return ask_ai_provider(chat_id, message)
