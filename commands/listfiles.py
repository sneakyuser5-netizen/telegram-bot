from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from config import ADMIN_ID
from services.files import list_files_info


async def listfiles_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    files = list_files_info()

    if not files:
        await update.message.reply_text(
            "❌ No files stored."
        )
        return

    text = "📂 Stored Files\n\n"

    for category, size, created_at in files:

        try:
            size_mb = round(int(size) / 1024 / 1024, 2)
            size_text = f"{size_mb} MB"
        except:
            size_text = size

        text += (
            f"✅ {category}\n"
            f"📦 Size: {size_text}\n"
            f"📅 Uploaded: {created_at}\n\n"
        )

    await update.message.reply_text(text)


listfiles_handler = CommandHandler(
    "listfiles",
    listfiles_cmd
)
