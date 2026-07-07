from services.cloudflare_service import ask as cloudflare_ask
from services.cerebras_service import ask as cerebras_ask
from services.openrouter_service import ask as openrouter_ask


PROVIDERS = [
    ("Cloudflare", cloudflare_ask),
    ("Cerebras", cerebras_ask),
    ("OpenRouter", openrouter_ask),
]


def ask_ai_provider(chat_id: int, message: str) -> str:
    """
    Try AI providers in order until one succeeds.
    """

    last_error = None

    for name, provider in PROVIDERS:
        try:
            print(f"[AI Router] Trying {name}...")
            return provider(chat_id, message)

        except Exception as e:
            print(f"[AI Router] {name} failed: {e}")
            last_error = e

    return (
        "⚠️ Whisper AI is temporarily unavailable.\n\n"
        "Please try again in a few moments."
    )
