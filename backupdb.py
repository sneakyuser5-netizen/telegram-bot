from telegram import Update

from telegram.ext import (
    CommandHandler,
    ContextTypes
)

from config import ADMIN_ID


async def backupdb_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.effective_user.id != ADMIN_ID:
        return

    with open("database.db", "rb") as f:
        await update.message.reply_document(
            document=f,
            filename="database.db",
            caption="📦 Database Backup"
        )


backupdb_handler = CommandHandler(
    "backupdb",
    backupdb_cmd
)