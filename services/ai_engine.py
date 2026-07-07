from services.interpreter import interpret
from services.service_engine import get_service_response
from services.context_manager import get_context
from services.ai_router import ask_ai_provider


def ask(chat_id: int, message: str) -> str:
    """
    Main Whisper AI engine.

    Flow:
        1. Understand user intent
        2. Try official business response
        3. Handle follow-up conversations
        4. Use AI only if needed
    """

    result = interpret(chat_id, message)

    intent = result["intent"]

    # ----------------------------------
    # Official business responses
    # ----------------------------------

    response = get_service_response(chat_id, intent)

    if response:
        return response

    # ----------------------------------
    # Conversation follow-up
    # ----------------------------------

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
                    "4️⃣ Your lifetime access will be activated.\n\n"
                    "Would you like me to explain the referral system?"
                )

            if topic == "vpn_premium":
                return (
                    "To activate your Premium VPN, simply contact "
                    "The-Whisperer through the bot menu."
                )

            if topic == "vpn_training":
                return (
                    "The training starts from beginner level and "
                    "covers everything needed to create VPN files."
                )

            if topic == "niu":
                return (
                    "The-Whisperer can help you obtain your NIU quickly "
                    "and legally. Simply contact him through the bot menu."
                )

    # ----------------------------------
    # AI fallback
    # ----------------------------------

    return ask_ai_provider(chat_id, message)
