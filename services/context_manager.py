"""
Conversation Context Manager

Stores the current conversation context for each chat.
"""

_contexts = {}


def set_context(chat_id: int, topic: str, state: str = "general"):
    """
    Save the current topic for a user.
    """

    _contexts[chat_id] = {
        "topic": topic,
        "state": state,
    }


def get_context(chat_id: int):
    """
    Return the user's current context.
    """

    return _contexts.get(chat_id)


def clear_context(chat_id: int):
    """
    Remove the user's conversation context.
    """

    _contexts.pop(chat_id, None)
