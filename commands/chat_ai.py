from telegram import Update
from telegram.ext import ContextTypes

from services.ai_engine import ask


async def chat_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message:
        return

    message = update.message.text

    if not message:
        return

    chat_id = update.effective_chat.id

    response = ask(chat_id, message)

    if response:
        await update.message.reply_text(response)
