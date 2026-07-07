from services.business_knowledge import BUSINESS
from services.service_details import SERVICE_DETAILS
from services.context_manager import set_context


def get_service_response(chat_id: int, intent: str) -> str | None:
    """
    Returns the official Whisper AI response for a known intent.
    """

    services = BUSINESS["services"]
    details = SERVICE_DETAILS

    # ===========================
    # SERVICES LIST
    # ===========================

    if intent == "services":
        return (
            "🚀 Here are the services offered by The-Whisperer:\n\n"

            "1️⃣ Biz Connect Academy (BCA)\n"
            "2️⃣ Premium VPN\n"
            "3️⃣ VPN Training\n"
            "4️⃣ NIU Assistance\n"
            "5️⃣ Free VPN Files\n"
            "6️⃣ Support\n\n"

            "Which one would you like to know more about?"
        )

    # ===========================
    # GREETING
    # ===========================

    if intent == "greeting":
        return (
            "👋 Hello!\n\n"
            "I'm Whisper AI, the official assistant of The-Whisperer.\n\n"
            "I can help you learn about our services, answer questions and guide you.\n\n"
            "What would you like to know today?"
        )

    # ===========================
    # BCA
    # ===========================

    if intent == "bca":
        set_context(chat_id, "bca")

        bca = services["bca"]
        info = details["bca"]

        return (
            f"🚀 {bca['name']}\n\n"
            f"{info['description']}\n\n"
            f"💰 Registration: {bca['price']}\n\n"
            "Would you like me to explain how registration works?"
        )

    # ===========================
    # PREMIUM VPN
    # ===========================

    if intent == "vpn_premium":
        set_context(chat_id, "vpn_premium")

        vpn = services["vpn_premium"]
        info = details["vpn_premium"]

        return (
            f"🔐 {vpn['name']}\n\n"
            f"{info['description']}\n\n"
            f"💰 Price: {vpn['price']}\n"
            f"📅 Duration: {vpn['duration']}\n"
            f"📶 Data: {vpn['daily_data']}"
        )

    # ===========================
    # VPN TRAINING
    # ===========================

    if intent == "vpn_training":
        set_context(chat_id, "vpn_training")

        vpn = services["vpn_training"]
        info = details["vpn_training"]

        return (
            f"📡 {vpn['name']}\n\n"
            f"{info['description']}\n\n"
            f"💰 Price: {vpn['price']}"
        )

    # ===========================
    # FREE FILES
    # ===========================

    if intent == "free_files":
        set_context(chat_id, "free_files")

        info = details["free_files"]

        return (
            "🎁 Free VPN Files\n\n"
            f"{info['description']}"
        )

    # ===========================
    # NIU SERVICE
    # ===========================

    if intent == "niu_service":
        set_context(chat_id, "niu")

        niu = services["niu"]

        return (
            f"🆔 {niu['name']}\n\n"
            "Need help obtaining your NIU?\n\n"
            f"💰 Service fee: {niu['price']}"
        )

    # ===========================
    # NIU EXPLANATION
    # ===========================

    if intent == "niu_explain":
        set_context(chat_id, "niu")

        return (
            "🆔 NIU stands for **Numéro d'Identifiant Unique**.\n\n"
            "It is an official taxpayer identification number used for administrative and tax procedures.\n\n"
            "It can be required to:\n"
            "• Open certain bank accounts\n"
            "• Register a business\n"
            "• Complete tax procedures\n"
            "• Access some financial services"
        )

    # ===========================
    # SUPPORT
    # ===========================

    if intent == "support":
        contact = BUSINESS["contact"]

        return (
            "🆘 Support\n\n"
            f"Telegram: {contact['telegram']}\n"
            f"WhatsApp: {contact['whatsapp']}"
        )

    return None
