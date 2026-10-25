import asyncio
import logging

from telegram import Update
from telegram.ext import ContextTypes

from services.ai_engine import ask

logger = logging.getLogger(__name__)


async def chat_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_obj = update.effective_message
    chat = update.effective_chat

    if message_obj is None or chat is None:
        return

    message = message_obj.text
    if not message or not message.strip():
        return

    try:
        # Run synchronous provider requests outside the bot's event loop.
        response = await asyncio.to_thread(ask, chat.id, message)

    except Exception as exc:
        # Log the exception type only; avoid logging messages that may
        # contain request details or sensitive information.
        logger.error("AI handler failed (%s).", type(exc).__name__)
        response = (
            "Sorry, I couldn't process your message right now. "
            "Please try again shortly."
        )

    if response:
        await message_obj.reply_text(response)
