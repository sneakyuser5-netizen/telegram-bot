import requests

from services.identity import SYSTEM_PROMPT
from config import GEMINI_API_KEY, GEMINI_MODEL


def ask(chat_id: int, message: str, history=None) -> str:
    """Send a prompt to Google Gemini."""
    if not GEMINI_API_KEY:
        raise RuntimeError("Gemini API key is not configured.")

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{GEMINI_MODEL}:generateContent"
    )

    headers = {
        "x-goog-api-key": GEMINI_API_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "system_instruction": {
            "parts": [
                {
                    "text": SYSTEM_PROMPT
                }
            ]
        },
        "contents": [
            *[
                {
                    "role": "model" if item.get("role") == "assistant" else "user",
                    "parts": [{"text": item["content"].strip()}],
                }
                for item in (history or [])[-12:]
                if isinstance(item, dict)
                and item.get("role") in ("user", "assistant")
                and isinstance(item.get("content"), str)
                and item["content"].strip()
            ],
            {
                "role": "user",
                "parts": [{"text": message}],
            },
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1024,
        },
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=(5, 15),
    )
    response.raise_for_status()

    data = response.json()
    candidates = data.get("candidates", [])
    if not candidates:
        raise RuntimeError("Gemini returned no response candidates.")

    parts = candidates[0].get("content", {}).get("parts", [])
    answer = "".join(part.get("text", "") for part in parts).strip()

    if not answer:
        raise RuntimeError("Gemini returned an empty response.")

    return answer
