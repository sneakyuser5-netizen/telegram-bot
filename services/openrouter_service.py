import requests

from services.identity import SYSTEM_PROMPT

from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
)


def ask(chat_id: int, message: str, history=None) -> str:
    """
    Send a prompt to OpenRouter AI.
    """

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://telegram.org",
    "X-Title": "Whisper AI",
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            *[
                {
                    "role": item["role"],
                    "content": item["content"].strip(),
                }
                for item in (history or [])[-12:]
                if isinstance(item, dict)
                and item.get("role") in ("user", "assistant")
                and isinstance(item.get("content"), str)
                and item["content"].strip()
            ],
            {
                "role": "user",
                "content": message,
            },
        ],
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=(5, 15),
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"].strip()
