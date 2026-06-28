from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from config import ADMIN_ID
from services.files import get_download_stats


async def filestats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    stats = get_download_stats()

    if not stats:
        await update.message.reply_text(
            "📊 No downloads recorded yet."
        )
        return

    text = "📊 Download Statistics\n\n"

    for category, count in stats:
        text += f"✅ {category} → {count}\n"

    await update.message.reply_text(text)


filestats_handler = CommandHandler(
    "filestats",
    filestats_cmd
)