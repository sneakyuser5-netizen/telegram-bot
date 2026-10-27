import logging
from time import monotonic

from requests.exceptions import HTTPError

from services.cloudflare_service import ask as cloudflare_ask
from services.gemini_service import ask as gemini_ask
from services.openrouter_service import ask as openrouter_ask

logger = logging.getLogger(__name__)

PROVIDERS = [
    ("Cloudflare", cloudflare_ask),
    ("Gemini", gemini_ask),
    ("OpenRouter", openrouter_ask),
]


def ask_ai_provider(chat_id: int, message: str, history=None) -> str:
    """Try configured AI providers in order until one succeeds."""
    for name, provider in PROVIDERS:
        started = monotonic()

        try:
            answer = provider(chat_id, message, history=history)
            elapsed = monotonic() - started

            if isinstance(answer, str) and answer.strip():
                logger.info(
                    "%s provider succeeded in %.2f seconds.",
                    name,
                    elapsed,
                )
                return answer.strip()

            logger.warning(
                "%s provider returned an empty response after %.2f seconds.",
                name,
                elapsed,
            )

        except HTTPError as exc:
            elapsed = monotonic() - started
            status = (
                exc.response.status_code
                if exc.response is not None
                else "unknown"
            )
            logger.warning(
                "%s provider failed after %.2f seconds (HTTP %s).",
                name,
                elapsed,
                status,
            )

        except Exception as exc:
            elapsed = monotonic() - started
            # Do not log raw exception messages, request details, or secrets.
            logger.warning(
                "%s provider failed after %.2f seconds (%s).",
                name,
                elapsed,
                type(exc).__name__,
            )

    logger.error("All configured AI providers failed.")
    return ""
