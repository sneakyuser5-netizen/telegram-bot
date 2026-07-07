import requests

from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
)


def ask(chat_id: int, message: str) -> str:
    """
    Send a prompt to OpenRouter AI.
    """

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Whisper AI, the official assistant of "
                    "The-Whisperer. Be concise, helpful and friendly."
                ),
            },
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
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"].strip()
