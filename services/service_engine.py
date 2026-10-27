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
    if intent == "services":
        set_context(chat_id, "services")
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

    # EXPLAIN ALL OFFICIAL SERVICES
    if intent == "services_explain_all":
        set_context(chat_id, "services")
        return (
            "🚀 Here is what The-Whisperer offers:\n\n"
            "1️⃣ Biz Connect Academy (BCA)\n"
            f"{details['bca']['description']}\n"
            f"💰 Registration: {services['bca']['price']}\n"
            f"🔗 Register: {services['bca']['registration_link']}\n\n"
            "2️⃣ Premium VPN\n"
            f"{details['vpn_premium']['description']}\n"
            f"💰 Price: {services['vpn_premium']['price']}\n"
            f"📅 Duration: {services['vpn_premium']['duration']}\n"
            f"📶 Data: {services['vpn_premium']['daily_data']}\n\n"
            "3️⃣ VPN Training\n"
            f"{details['vpn_training']['description']}\n"
            f"💰 Price: {services['vpn_training']['price']}\n\n"
            "4️⃣ Free VPN Files\n"
            f"{details['free_files']['description']}\n\n"
            "5️⃣ NIU Assistance\n"
            f"{details['niu']['description']}\n"
            f"💰 Service fee: {services['niu']['price']}\n\n"
            "6️⃣ Support\n"
            f"{details['support']['description']}\n\n"
            "💬 Which service interests you most? Tell me, and I'll "
            "guide you through the next step."
        )

    # Redirect requests for services not currently offered.
    if intent == "unsupported_service":
        set_context(chat_id, "services")
        return (
            "😊 Thanks for your interest! That service isn't among "
            "The-Whisperer's current offers.\n\n"
            "However, I'd be happy to help you with one of our six services:\n\n"
            "1️⃣ Biz Connect Academy (BCA) — registration for 2,900 FCFA.\n"
            "2️⃣ Premium VPN — 500 FCFA for 30 days, with 250 MB/day.\n"
            "3️⃣ VPN Training — learn to create, configure and manage VPN files.\n"
            "4️⃣ Free VPN Files — access available VPN files through the bot menu.\n"
            "5️⃣ NIU Assistance — service fee of 1,000 FCFA.\n"
            "6️⃣ Support — contact The-Whisperer for assistance.\n\n"
            "🚀 One of these services might be exactly what you need! "
            "Which one would you like to explore? I'll guide you through "
            "the next steps."
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
            f"💰 Registration: {bca['price']}\n"
            f"🔗 Register here: {bca['registration_link']}\n\n"
            "Open the link to register. If you need help, contact "
            "support on Telegram @The_whisperer237 or WhatsApp "
            "237675310628."
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
