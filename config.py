import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))

CHANNEL_LINK = os.getenv("CHANNEL_LINK", "")
WHATSAPP_URL = os.getenv("WHATSAPP_URL", "")
PLATFORM_URL = os.getenv("PLATFORM_URL", "")