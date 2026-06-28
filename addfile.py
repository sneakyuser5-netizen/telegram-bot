from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from services.files import add_file
from config import ADMIN_ID

WAIT_FILE = 1

async def addfile_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return ConversationHandler.END

    await update.message.reply_text(
        "📤 Send the file you want to save."
    )

    return WAIT_FILE

async def receive_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.document:
        await update.message.reply_text(
            "❌ Please send a document."
        )
        return WAIT_FILE

    document = update.message.document

    file_id = document.file_id
    filename = document.file_name

    category = filename.split(".")[-1].lower()

    print("SAVED CATEGORY:", category)

    add_file(
        category,
        str(document.file_size),
        file_id
    )

    await update.message.reply_text(
        "✅ File saved successfully."
    )

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return ConversationHandler.END

addfile_handler = ConversationHandler(
    entry_points=[
        CommandHandler("addfile", addfile_start)
    ],
    states={
        WAIT_FILE: [
            MessageHandler(filters.Document.ALL, receive_file)
        ]
    },
    fallbacks=[
        CommandHandler("cancel", cancel)
    ]
)