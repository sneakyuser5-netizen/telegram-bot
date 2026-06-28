from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from services.files import get_file


async def testfile(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text(
            "Usage: /testfile ehi\nExample: /testfile nm"
        )
        return

    category = context.args[0].lower()

    file_id = get_file(category)

    if not file_id:
        await update.message.reply_text(
            f"No {category} file found."
        )
        return

    await update.message.reply_document(file_id)


testfile_handler = CommandHandler("testfile", testfile)