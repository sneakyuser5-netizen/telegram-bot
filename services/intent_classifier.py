def classify_intent(message: str) -> str:
    """
    Classifies the user's intent.
    Returns only an intent string.
    """

    text = message.lower().strip()

    # Greetings
    if any(word in text for word in [
        "hi", "hello", "hey", "bonjour", "salut"
    ]):
        return "greeting"

    # Menu / services
    if any(word in text for word in [
        "services", "what do you offer", "what can you do",
        "menu", "offer"
    ]):
        return "services"

    # BCA
    if any(word in text for word in [
        "bca", "biz connect", "academy",
        "affiliate", "earn money", "make money"
    ]):
        return "bca"

    # Premium VPN
    if any(word in text for word in [
        "premium vpn", "vpn premium"
    ]):
        return "vpn_premium"

    # VPN Training
    if any(word in text for word in [
        "vpn training", "learn vpn", "vpn course"
    ]):
        return "vpn_training"

    # Free VPN Files
    if any(word in text for word in [
        "free vpn", "free files", "vpn files"
    ]):
        return "free_files"

    # NIU
    if "niu" in text:
        explain_words = [
            "what", "what is", "de quoi",
            "c'est quoi", "meaning", "used for",
            "purpose", "pourquoi", "why"
        ]

        if any(word in text for word in explain_words):
            return "niu_explain"

        return "niu_service"

    # Support
    if any(word in text for word in [
        "support", "administrator", "admin"
    ]):
        return "support"

    # Conversation follow-up
    if text in [
        "yes", "yeah", "sure", "ok", "okay",
        "oui", "d'accord", "continue", "tell me more"
    ]:
        return "follow_up"

    return "general"
