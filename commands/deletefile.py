from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from config import ADMIN_ID
from services.files import delete_file


async def deletefile_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: /deletefile category"
        )
        return

    category = context.args[0].lower()

    deleted = delete_file(category)

    if deleted:
        await update.message.reply_text(
            f"✅ {category} deleted."
        )
    else:
        await update.message.reply_text(
            f"❌ {category} not found."
        )


deletefile_handler = CommandHandler(
    "deletefile",
    deletefile_cmd
)
