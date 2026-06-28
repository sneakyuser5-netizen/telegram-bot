from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes

from config import ADMIN_ID


async def admin_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        "🔧 ADMIN PANEL",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📂 Files", callback_data="admin_files")],
            [InlineKeyboardButton("📊 Statistics", callback_data="admin_stats")],
            [InlineKeyboardButton("💾 Database", callback_data="admin_db")],
            [InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")]
        ])
    )


adminpanel_handler = CommandHandler(
    "admin",
    admin_cmd
)
