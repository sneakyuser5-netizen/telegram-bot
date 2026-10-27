"""Manage short-lived conversation context for each chat."""

from collections import deque

_MAX_MESSAGES = 12
_contexts = {}


def set_context(chat_id: int, topic: str, state: str = "general") -> None:
    """Save the current topic without discarding conversation history."""
    context = _contexts.setdefault(
        chat_id,
        {"topic": topic, "state": state, "history": deque(maxlen=_MAX_MESSAGES)},
    )
    context["topic"] = topic
    context["state"] = state


def get_context(chat_id: int):
    """Return the current context for a chat."""
    return _contexts.get(chat_id)


def add_message(chat_id: int, role: str, content: str) -> None:
    """Append a user or assistant message to the short conversation history."""
    if role not in ("user", "assistant") or not content or not content.strip():
        return

    context = _contexts.setdefault(
        chat_id,
        {"topic": None, "state": "general", "history": deque(maxlen=_MAX_MESSAGES)},
    )
    context["history"].append({"role": role, "content": content.strip()})


def get_history(chat_id: int) -> list:
    """Return a copy of the recent conversation history."""
    context = _contexts.get(chat_id)
    if not context:
        return []
    return list(context.get("history", []))


def clear_context(chat_id: int) -> None:
    """Clear the context and history for a chat."""
    _contexts.pop(chat_id, None)
