import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TOKEN = os.getenv("BOT_TOKEN")
BOT_TOKEN = TOKEN

ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

CHANNEL_LINK = os.getenv("CHANNEL_LINK", "")
WHATSAPP_URL = os.getenv("WHATSAPP_URL", "")
PLATFORM_URL = os.getenv("PLATFORM_URL", "")


# =========================
# AI PROVIDERS
# =========================

# Cloudflare
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_KEY", "")
CLOUDFLARE_MODEL = os.getenv(
    "CLOUDFLARE_MODEL",
    "@cf/meta/llama-3.1-8b-instruct"
)


# Cerebras
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY", "")
CEREBRAS_MODEL = os.getenv(
    "CEREBRAS_MODEL",
    "llama-3.1-8b"
)


# OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "meta-llama/llama-3.1-8b-instruct:free"
)
