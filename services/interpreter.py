from services.intent_classifier import classify_intent


def interpret(chat_id: int, message: str) -> dict:
    """
    Determines what the user wants.
    It does NOT generate replies.
    """

    return {
        "chat_id": chat_id,
        "message": message,
        "intent": classify_intent(message),
    }
