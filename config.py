import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TOKEN = os.getenv("BOT_TOKEN")
BOT_TOKEN = TOKEN  # Optional alias

ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

CHANNEL_LINK = os.getenv("CHANNEL_LINK", "")
WHATSAPP_URL = os.getenv("WHATSAPP_URL", "")
PLATFORM_URL = os.getenv("PLATFORM_URL", "")

# AI Providers
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
CLOUDFLARE_API_KEY = os.getenv("CLOUDFLARE_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Models
OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "google/gemma-4-31b-it:free"
)
