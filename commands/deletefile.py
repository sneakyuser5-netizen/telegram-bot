from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from config import ADMIN_ID
from services.files import delete_file


async def deletefile_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user = update.effective_user
    message = update.effective_message

    if ADMIN_ID == 0 or user is None or user.id != ADMIN_ID:
        if message:
            await message.reply_text("⛔ Unauthorized.")
        return

    if not context.args:
        await message.reply_text("Usage: /deletefile category")
        return

    category = context.args[0].lower()

    try:
        deleted = delete_file(category)
    except Exception:
        await message.reply_text("❌ Could not delete the file. Check the database.")
        return

    if deleted:
        await message.reply_text(f"✅ {category} deleted.")
    else:
        await message.reply_text(f"❌ {category} not found.")


deletefile_handler = CommandHandler("deletefile", deletefile_cmd)
