import requests

from config import (
    CLOUDFLARE_ACCOUNT_ID,
    CLOUDFLARE_API_TOKEN,
    CLOUDFLARE_MODEL,
)


#def ask(chat_id: int, message: str) -> str:
def ask(chat_id: int, message: str) -> str:
    """
    Send a prompt to Cloudflare AI.
    """
    if not CLOUDFLARE_ACCOUNT_ID or not CLOUDFLARE_API_TOKEN:
        raise RuntimeError(
            "Cloudflare AI is not configured. Check the local environment."
        )

    if not message or not message.strip():
        return "Please send a message."

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{CLOUDFLARE_ACCOUNT_ID}/ai/run/{CLOUDFLARE_MODEL}"
    )

    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
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
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=(5, 15),
    )

    response.raise_for_status()

    data = response.json()

    if not data.get("success"):
        raise Exception("Cloudflare request failed.")

    result = data.get("result", {})

    if "response" in result:
        return result["response"]

    if "messages" in result:
        return result["messages"][-1]["content"]

    raise Exception("Unexpected Cloudflare response.")
