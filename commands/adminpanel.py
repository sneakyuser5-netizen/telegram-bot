from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes

from config import ADMIN_ID


async def admin_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    user = update.effective_user
    message = update.effective_message

    if ADMIN_ID == 0 or user is None or user.id != ADMIN_ID:
        if message:
            await message.reply_text("⛔ Unauthorized.")
        return

    await message.reply_text(
        "🔧 ADMIN PANEL",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📂 Files", callback_data="admin_files")],
            [InlineKeyboardButton("📊 Statistics", callback_data="admin_stats")],
            [InlineKeyboardButton("💾 Database", callback_data="admin_db")],
            [InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")],
        ]),
    )


adminpanel_handler = CommandHandler("admin", admin_cmd)
