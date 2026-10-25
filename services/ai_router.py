import logging

from services.cloudflare_service import ask as cloudflare_ask
from services.cerebras_service import ask as cerebras_ask
from services.openrouter_service import ask as openrouter_ask


logger = logging.getLogger(__name__)

PROVIDERS = [
    ("Cloudflare", cloudflare_ask),
    ("Cerebras", cerebras_ask),
    ("OpenRouter", openrouter_ask),
]


def ask_ai_provider(chat_id: int, message: str) -> str:
    """Try configured AI providers in order until one succeeds."""
    for name, provider in PROVIDERS:
        try:
            answer = provider(chat_id, message)

            if isinstance(answer, str) and answer.strip():
                return answer.strip()

            logger.warning("%s returned an empty response.", name)

        except Exception as exc:
            # Avoid logging raw exception messages that may contain
            # request details or other sensitive information.
            logger.warning(
                "%s provider failed (%s).",
                name,
                type(exc).__name__,
            )

    return (
        "Sorry, the AI service is temporarily unavailable. "
        "Please try again in a little while."
    )
