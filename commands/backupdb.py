import os

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from config import ADMIN_ID


async def backupdb_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user = update.effective_user
    message = update.effective_message

    if ADMIN_ID == 0 or user is None or user.id != ADMIN_ID:
        await message.reply_text("⛔ Unauthorized.")
        return

    if not os.path.isfile("database.db"):
        await message.reply_text("❌ No database.db file exists.")
        return

    try:
        with open("database.db", "rb") as database_file:
            await message.reply_document(
                document=database_file,
                filename="database.db",
                caption="📦 Database Backup",
            )
    except OSError:
        await message.reply_text("❌ Could not read the database for backup.")


backupdb_handler = CommandHandler("backupdb", backupdb_cmd)
