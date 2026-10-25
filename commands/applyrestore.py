import os

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from config import ADMIN_ID
from commands.restoredb import validate_database

RESTORE_DB = "database_restored.db"


async def applyrestore_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user = update.effective_user
    message = update.effective_message

    if message is None:
        return

    if ADMIN_ID <= 0 or user is None or user.id != ADMIN_ID:
        await message.reply_text("⛔ Unauthorized.")
        return

    if not os.path.isfile(RESTORE_DB):
        await message.reply_text(
            "❌ No staged restore found. Use /restoredb first."
        )
        return

    valid, reason = validate_database(RESTORE_DB)
    if not valid:
        await message.reply_text(
            f"❌ Restore file rejected: {reason}"
        )
        return

    await message.reply_text(
        "✅ The staged database passed validation.\n\n"
        "⚠️ The live database has NOT been changed.\n"
        "After stopping the bot completely, run: ""python apply_restore_offline.py. "
        "Keep the current database and its backups until the "
        "restored bot has been tested."
    )


applyrestore_handler = CommandHandler(
    "applyrestore",
    applyrestore_cmd,
)
