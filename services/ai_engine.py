from services.interpreter import interpret
from services.service_engine import get_service_response
from services.context_manager import get_context
from services.ai_router import ask_ai_provider
from services.cloudflare_service import ask as cf

def ask(chat_id: int, message: str) -> str:
    return cf(chat_id, "Say hello.")

#def ask(chat_id: int, message: str) -> str:
    """
    Whisper AI Main Engine

    Flow:
    1. Understand message
    2. Try business knowledge
    3. Handle follow-up
    4. AI fallback
    """

    result = interpret(chat_id, message)

    intent = result.get("intent")

    # ----------------------------
    # BUSINESS KNOWLEDGE
    # ----------------------------

    response = get_service_response(chat_id, message)

    if response:
        return response

    # ----------------------------
    # FOLLOW UP
    # ----------------------------

    if intent == "follow_up":

        context = get_context(chat_id)

        if context:

            topic = context["topic"]

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

            elif topic == "vpn_premium":
                return (
                    "🚀 To activate Premium VPN, simply contact "
                    "The-Whisperer using the bot menu."
                )

            elif topic == "vpn_training":
                return (
                    "📡 The VPN training starts from beginner level "
                    "and teaches you everything needed to create your own VPN files."
                )

            elif topic == "niu":
                return (
                    "🆔 The-Whisperer can help you obtain your NIU "
                    "quickly and legally.\n\n"
                    "Would you like me to explain the application process?"
                )

    # ----------------------------
    # AI
    # ----------------------------

    return ask_ai_provider(chat_id, message)
