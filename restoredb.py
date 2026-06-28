from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from config import ADMIN_ID

WAIT_DB = 1


async def restoredb_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_user.id != ADMIN_ID:
        return ConversationHandler.END

    await update.message.reply_text(
        "📤 Send database.db"
    )

    return WAIT_DB


async def receive_db(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    document = update.message.document

    if not document:
        return WAIT_DB

    if document.file_name != "database.db":
        await update.message.reply_text(
            "❌ Please send database.db"
        )
        return WAIT_DB

    file = await document.get_file()

    await file.download_to_drive(
        "database_restored.db"
    )

    await update.message.reply_text(
        "✅ Backup received."
    )

    return ConversationHandler.END


async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    return ConversationHandler.END


restoredb_handler = ConversationHandler(
    entry_points=[
        CommandHandler(
            "restoredb",
            restoredb_start
        )
    ],
    states={
        WAIT_DB: [
            MessageHandler(
                filters.Document.ALL,
                receive_db
            )
        ]
    },
    fallbacks=[
        CommandHandler(
            "cancel",
            cancel
        )
    ]
)