import os
import sqlite3

from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

from config import ADMIN_ID

WAIT_DB = 1
RESTORE_PATH = "database_restored.db"
PART_PATH = RESTORE_PATH + ".part"
MAX_DB_BYTES = 50 * 1024 * 1024  # 50 MB


def is_admin(update: Update) -> bool:
    user = update.effective_user
    return ADMIN_ID != 0 and user is not None and user.id == ADMIN_ID


def validate_database(path: str) -> tuple[bool, str]:
    """Check SQLite integrity and the tables/columns this bot requires."""
    if not os.path.isfile(path) or os.path.getsize(path) == 0:
        return False, "The uploaded file is empty or missing."

    try:
        conn = sqlite3.connect(f"file:{os.path.abspath(path)}?mode=ro", uri=True)
        try:
            result = conn.execute("PRAGMA integrity_check").fetchone()
            if not result or result[0] != "ok":
                return False, "SQLite integrity check failed."

            required = {
                "users": {"user_id", "referrals", "referred_by", "reward_unlocked", "joined_at"},
                "downloads": {"category", "count"},
                "files": {"id", "category", "size", "file_id", "created_at"},
            }

            tables = {
                row[0]
                for row in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ).fetchall()
            }

            for table, required_columns in required.items():
                if table not in tables:
                    return False, f"Required table missing: {table}"

                columns = {
                    row[1] for row in conn.execute(f"PRAGMA table_info({table})")
                }
                if not required_columns.issubset(columns):
                    return False, f"Required columns missing in table: {table}"

            return True, "Database passed validation."
        finally:
            conn.close()
    except (sqlite3.Error, OSError, ValueError):
        return False, "The file is not a valid, readable SQLite database."


async def restoredb_start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not is_admin(update):
        await update.effective_message.reply_text("⛔ Unauthorized.")
        return ConversationHandler.END

    await update.effective_message.reply_text(
        "📤 Send a valid database.db backup (maximum 50 MB). "
        "After validation, use /applyrestore for confirmation, then stop the bot ""and follow the offline restore instructions."
    )
    return WAIT_DB


async def receive_db(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not is_admin(update):
        await update.effective_message.reply_text("⛔ Unauthorized.")
        return ConversationHandler.END

    message = update.effective_message
    document = message.document if message else None

    if not document:
        if message:
            await message.reply_text("Please send a database file.")
        return WAIT_DB

    if document.file_name != "database.db":
        await message.reply_text("❌ Please send a file named database.db.")
        return WAIT_DB

    if not document.file_size or document.file_size > MAX_DB_BYTES:
        await message.reply_text("❌ File is empty or exceeds the 50 MB limit.")
        return WAIT_DB

    try:
        telegram_file = await document.get_file()
        await telegram_file.download_to_drive(custom_path=PART_PATH)

        if os.path.getsize(PART_PATH) > MAX_DB_BYTES:
            os.remove(PART_PATH)
            await message.reply_text("❌ Uploaded file exceeds the 50 MB limit.")
            return WAIT_DB

        valid, reason = validate_database(PART_PATH)
        if not valid:
            os.remove(PART_PATH)
            await message.reply_text(f"❌ Database rejected: {reason}")
            return WAIT_DB

        os.replace(PART_PATH, RESTORE_PATH)
        await message.reply_text(
            "✅ Database backup received and validated. "
            "The live database has not been changed. "
            "Next, use /applyrestore to confirm validation. Then stop the bot and ""run: python apply_restore_offline.py"
        )
        return ConversationHandler.END

    except Exception:
        if os.path.exists(PART_PATH):
            os.remove(PART_PATH)
        await message.reply_text(
            "❌ Could not receive or validate the backup. "
            "The live database was not changed."
        )
        return WAIT_DB


async def cancel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not is_admin(update):
        await update.effective_message.reply_text("⛔ Unauthorized.")
        return ConversationHandler.END

    if os.path.exists(PART_PATH):
        os.remove(PART_PATH)

    await update.effective_message.reply_text("Restore cancelled.")
    return ConversationHandler.END


restoredb_handler = ConversationHandler(
    entry_points=[CommandHandler("restoredb", restoredb_start)],
    states={
        WAIT_DB: [
            MessageHandler(filters.Document.ALL, receive_db),
        ]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
