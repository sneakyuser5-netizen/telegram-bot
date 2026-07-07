from telegram import Update
from telegram.ext import ContextTypes

from services.ai_engine import ask_ai


async def chat_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles every normal text message using the AI system.
    """

    user_id = update.effective_user.id
    message = update.message.text

    if not message:
        return

    response = ask_ai(user_id, message)

    if response:
        await update.message.reply_text(response)
