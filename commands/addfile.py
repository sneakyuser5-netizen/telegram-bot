from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

from services.files import add_file
from config import ADMIN_ID

WAIT_FILE = 1

# Categories currently offered by the bot's download menu.
ALLOWED_CATEGORIES = {
    "hat", "sip", "nm", "ehi", "hc", "ssc",
    "npvt", "v2ray", "ink", "dark", "ziv",
}


def is_admin(update: Update) -> bool:
    user = update.effective_user
    return ADMIN_ID != 0 and user is not None and user.id == ADMIN_ID


async def addfile_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not is_admin(update):
        await update.effective_message.reply_text("⛔ Unauthorized.")
        return ConversationHandler.END

    await update.effective_message.reply_text(
        "📤 Send the file you want to save.\n"
        "The filename extension must match a supported category, "
        "for example: file.nm"
    )
    return WAIT_FILE


async def receive_file(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    # Recheck authorization before making any database changes.
    if not is_admin(update):
        if update.effective_message:
            await update.effective_message.reply_text("⛔ Unauthorized.")
        return ConversationHandler.END

    message = update.effective_message
    document = message.document if message else None

    if not document:
        await message.reply_text("❌ Please send a document.")
        return WAIT_FILE

    filename = document.file_name or ""
    if "." not in filename or filename.endswith("."):
        await message.reply_text(
            "❌ The filename must include a supported extension, "
            "for example: file.nm"
        )
        return WAIT_FILE

    category = filename.rsplit(".", 1)[-1].lower()

    if category not in ALLOWED_CATEGORIES:
        await message.reply_text(
            "❌ Unsupported category. Allowed categories: "
            + ", ".join(sorted(ALLOWED_CATEGORIES))
        )
        return WAIT_FILE

    if not document.file_size or document.file_size <= 0:
        await message.reply_text("❌ The uploaded file appears to be empty.")
        return WAIT_FILE

    try:
        add_file(
            category,
            str(document.file_size),
            document.file_id,
        )
    except Exception:
        await message.reply_text(
            "❌ Could not save the file. The database may be unavailable."
        )
        return ConversationHandler.END

    await message.reply_text(
        f"✅ File saved successfully under category: {category}"
    )
    return ConversationHandler.END


async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not is_admin(update):
        if update.effective_message:
            await update.effective_message.reply_text("⛔ Unauthorized.")
        return ConversationHandler.END

    await update.effective_message.reply_text("Upload cancelled.")
    return ConversationHandler.END


addfile_handler = ConversationHandler(
    entry_points=[CommandHandler("addfile", addfile_start)],
    states={
        WAIT_FILE: [
            MessageHandler(filters.Document.ALL, receive_file),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
