import re


def classify_intent(message: str) -> str:
    """Classify the user's intent without generating a response."""
    text = message.lower().strip()
    text = re.sub(r"\s+", " ", text)

    # Greetings: match whole words, not arbitrary letter sequences.
    if re.fullmatch(
        r"(hi|hello|hey|bonjour|salut|good morning|good afternoon|good evening)[!. ]*",
        text,
    ):
        return "greeting"

    # Requests to explain or list all business services.
    all_services_patterns = (
        "explain all",
        "explain everything",
        "tell me about all your services",
        "explain all your services",
        "explain all the services",
        "all your services",
        "everything you offer",
        "describe all services",
        "tell me everything",
    )
    if any(phrase in text for phrase in all_services_patterns):
        return "services_explain_all"

    # Services not currently listed among the official offers.
    unsupported_patterns = (
        "virtual card",
        "virtual visa",
        "virtual mastercard",
        "mastercard card",
        "visa card",
        "crypto wallet",
        "bank account opening",
    )
    if any(phrase in text for phrase in unsupported_patterns):
        return "unsupported_service"

    # Menu / services.
    if any(phrase in text for phrase in (
        "services",
        "what do you offer",
        "what can you do",
        "menu",
        "offer",
    )):
        return "services"

    # Registration questions belong to BCA.
    if any(phrase in text for phrase in (
        "how do i register",
        "how can i register",
        "how to register",
        "how do i sign up",
        "how can i sign up",
        "how to sign up",
        "registration process",
        "registration link",
    )):
        return "bca"

    # BCA.
    if any(phrase in text for phrase in (
        "bca",
        "biz connect",
        "academy",
        "affiliate",
        "earn money",
        "make money",
    )):
        return "bca"

    # Premium VPN.
    if any(phrase in text for phrase in ("premium vpn", "vpn premium")):
        return "vpn_premium"

    # VPN training.
    if any(phrase in text for phrase in (
        "vpn training",
        "learn vpn",
        "vpn course",
    )):
        return "vpn_training"

    # Free VPN files.
    if any(phrase in text for phrase in (
        "free vpn",
        "free files",
        "vpn files",
    )):
        return "free_files"

    # NIU.
    if re.search(r"\bniu\b", text):
        explain_words = (
            "what",
            "what is",
            "de quoi",
            "c'est quoi",
            "meaning",
            "used for",
            "purpose",
            "pourquoi",
            "why",
        )
        if any(phrase in text for phrase in explain_words):
            return "niu_explain"
        return "niu_service"

    # Support.
    if any(word in text for word in (
        "support",
        "administrator",
        "admin",
        "help",
        "contact",
        "whatsapp",
        "telegram",
    )):
        return "support"

    # Short conversation follow-ups.
    if text in (
        "yes",
        "yeah",
        "sure",
        "ok",
        "okay",
        "oui",
        "d'accord",
        "continue",
        "tell me more",
        "more details",
        "explain more",
    ):
        return "follow_up"

    return "general"
