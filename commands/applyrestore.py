import os
import shutil

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes
)

from config import ADMIN_ID


async def applyrestore_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.effective_user.id != ADMIN_ID:
        return

    if not os.path.exists(
        "database_restored.db"
    ):
        await update.message.reply_text(
            "❌ No restore file found."
        )
        return

    shutil.copyfile(
        "database_restored.db",
        "database.db"
    )

    await update.message.reply_text(
        "✅ Restore applied.\n"
        "🔄 Restart the bot."
    )


applyrestore_handler = CommandHandler(
    "applyrestore",
    applyrestore_cmd
)
