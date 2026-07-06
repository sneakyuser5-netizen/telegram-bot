from typing import Optional

from services.business_knowledge import BUSINESS
from services.service_details import SERVICE_DETAILS
from services.conversation_memory import set_context
from services.intent_classifier import classify_intent


def get_service_response(chat_id: int, message: str) -> Optional[str]:
    text = message.lower().strip()

    services = BUSINESS["services"]
    details = SERVICE_DETAILS

    # =====================================================
    # BCA
    # =====================================================

    if any(word in text for word in [
        "bca",
        "biz connect",
        "academy",
        "affiliate",
        "earn money",
        "make money",
        "online income",
        "money online",
        "register bca",
    ]):

        bca = services["bca"]
        set_context(chat_id, "bca", "general")

        return (
            "🚀 Biz Connect Academy (BCA)\n\n"

            "Biz Connect Academy is The-Whisperer's online learning platform designed to help people acquire practical digital skills and build sustainable income online.\n\n"

            "Whether you're a student, entrepreneur or employee, BCA teaches skills that can immediately be applied in real life.\n\n"

            "📚 Courses include:\n"
            "• Artificial Intelligence (AI)\n"
            "• Facebook & TikTok Ads\n"
            "• WhatsApp Bot Creation\n"
            "• Affiliate Marketing\n"
            "• Digital Product Sales\n"
            "• TikTok Monetization\n"
            "• Canva Pro & CapCut Pro\n"
            "• Audience Growth\n"
            "• Visa Card Creation\n"
            "• And many more...\n\n"

            f"🌍 Available in {len(bca['countries'])} countries:\n"
            + ", ".join(bca["countries"])
            + "\n\n"

            f"💰 Registration Fee: {bca['price']}\n\n"

            "💸 Referral Rewards:\n"
            f"🥇 Level 1: {bca['referral']['level1']}"
            f"🥈 Level 2: {bca['referral']['level2']}"
            f"🥉 Level 3: {bca['referral']['level3']}\n\n"

            "⚠️ BCA is NOT an investment platform.\n"
            "Members earn through referrals and by applying the digital skills they learn.\n\n"

            f"🔗 Register:\n{bca['registration_link']}\n\n"

            "Would you like me to explain how registration works or how the referral system works? 😊"
        )

    # =====================================================
    # PREMIUM VPN
    # =====================================================

    if any(word in text for word in [
        "premium vpn",
        "vpn premium",
        "buy vpn",
        "activate vpn",
    ]):

        vpn = services["vpn_premium"]
        set_context(chat_id, "vpn_premium", "general")

        return (
            "🔐 Premium VPN\n\n"

            "Our Premium VPN offers a fast, secure and stable internet connection suitable for everyday browsing.\n\n"

            f"📅 Duration: {vpn['duration']}\n"
            f"📶 Daily Data: {vpn['daily_data']}\n"
            f"💰 Price: {vpn['price']}\n\n"

            "📲 To activate your VPN, simply contact The-Whisperer using the bot menu.\n\n"

            "Would you like to know how activation works? 😊"
        )
   # =====================================================
    # VPN TRAINING
    # =====================================================

    if any(word in text for word in [
        "vpn training",
        "learn vpn",
        "vpn course",
        "create vpn",
        "vpn files creation",
    ]):

        vpn = services["vpn_training"]
        set_context(chat_id, "vpn_training", "general")

        return (
            "📡 VPN Training\n\n"

            "This training teaches you how to create, configure and manage VPN files from beginner to advanced level.\n\n"

            "📚 During the training you'll learn:\n"
            "• VPN file creation\n"
            "• Configuration techniques\n"
            "• Troubleshooting\n"
            "• Practical deployment\n"
            "• Ways to earn income using your VPN skills\n\n"

            f"💰 Training Fee: {vpn['price']}\n\n"

            "📲 To register, contact The-Whisperer through the bot menu.\n\n"

            "Would you like to know how the training is organized? 😊"
        )

    # =====================================================
    # FREE VPN FILES
    # =====================================================

    if any(word in text for word in [
        "free vpn",
        "free vpn files",
        "free files",
        "vpn files",
    ]):

        ff = services["free_files"]
        set_context(chat_id, "free_files", "general")

        return (
            "🎁 Free VPN Files\n\n"

            "The-Whisperer regularly shares free VPN files that users can access directly from the bot menu.\n\n"

            f"📅 Validity: {ff['duration']}\n\n"

            "Simply open the bot menu and choose **Free VPN Files** to access the latest available files.\n\n"

            "Would you also like to know the advantages of Premium VPN compared to the free files? 😊"
        )

    # =====================================================
    # NIU
    # =====================================================

    if "niu" in text:

        set_context(chat_id, "niu", "general")

        # User wants an explanation
        if classify_intent(message) == "explain":

            return (
                "🆔 NIU stands for **Numéro d'Identifiant Unique**.\n\n"

                "It is a taxpayer identification number issued by the tax administration. It uniquely identifies an individual or business for tax and administrative purposes.\n\n"

                "A NIU is commonly used to:\n"
                "• Register a business\n"
                "• Open certain bank accounts\n"
                "• Complete tax procedures\n"
                "• Access some financial services\n"
                "• Avoid tax-related penalties\n\n"

                "If later you decide to obtain your NIU, The-Whisperer can assist you through the entire process. 😊"
            )

        # User wants the service

        niu = services["niu"]

        return (
            f"🆔 {niu['name']}\n\n"

            f"{niu['description']}\n\n"

            f"💰 Price: {niu['price']}\n\n"

            "✔ Benefits:\n• "
            + "\n• ".join(niu["benefits"]) 
            + "\n\n"

            "📲 Contact The-Whisperer through the bot menu to begin the process.\n\n"

            "Do you have any questions before getting your NIU? 😊"
        )
    # =====================================================
    # SUPPORT
    # =====================================================

    if any(word in text for word in [
        "support",
        "help",
        "contact",
        "administrator",
        "admin",
    ]):

        support = services["support"]
        set_context(chat_id, "support", "general")

        return (
            f"🆘 {support['name']}\n\n"

            "If you need assistance, The-Whisperer is available to help you.\n\n"

            "📲 Contact options:\n"
            f"• Telegram: {BUSINESS['contact']['telegram']}\n"
            f"• WhatsApp: {BUSINESS['contact']['whatsapp']}\n\n"

            "You can also use the bot menu whenever you need support with any service.\n\n"

            "How can I assist you today? 😊"
        )

    # =====================================================
    # NOTHING MATCHED
    # =====================================================

    return None
