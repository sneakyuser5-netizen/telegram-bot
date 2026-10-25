from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from config import ADMIN_ID
from services.files import get_download_stats


async def filestats_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user = update.effective_user
    message = update.effective_message

    if ADMIN_ID == 0 or user is None or user.id != ADMIN_ID:
        if message:
            await message.reply_text("⛔ Unauthorized.")
        return

    try:
        stats = get_download_stats()
    except Exception:
        await message.reply_text("❌ Could not read download statistics.")
        return

    if not stats:
        await message.reply_text("📊 No downloads recorded yet.")
        return

    text = "📊 Download Statistics\n\n"
    for category, count in stats:
        text += f"✅ {category} → {count}\n"

    await message.reply_text(text)


filestats_handler = CommandHandler("filestats", filestats_cmd)
