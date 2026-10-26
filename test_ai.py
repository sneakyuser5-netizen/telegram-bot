import logging
from requests.exceptions import HTTPError

from services.cloudflare_service import ask as cloudflare_ask
from services.gemini_service import ask as gemini_ask
from services.openrouter_service import ask as openrouter_ask

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

providers = [
    ("Cloudflare", cloudflare_ask),
    ("Gemini", gemini_ask),
    ("OpenRouter", openrouter_ask),
]

for name, provider in providers:
    print(f"\n========== {name} ==========")

    try:
        answer = provider(1, "Say hello in one short sentence.")

        if isinstance(answer, str) and answer.strip():
            print("SUCCESS")
            print(answer.strip())
        else:
            print("FAILED: Empty response")

    except HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "unknown"
        print(f"FAILED: HTTP {status}")

    except Exception as exc:
        print(f"FAILED: {type(exc).__name__}")
