import logging

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import TOKEN
from db_functions import retrieve_dollar, retrieve_euro, retrieve_pound


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome!\nUse the commands below to get the value of the chosen currency in Rial.\n\n/Dollar\n/Euro\n/Pound",
    )


async def dollar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=retrieve_dollar()
    )


async def pound(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=retrieve_pound()
    )


async def euro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=retrieve_euro()
    )


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, the command your entered is not defined",
    )


if __name__ == "__main__":
    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )

    start_handler = CommandHandler("start", start)
    dollar_handler = CommandHandler("dollar", dollar)
    pound_handler = CommandHandler("pound", pound)
    euro_handler = CommandHandler("euro", euro)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(dollar_handler)
    application.add_handler(pound_handler)
    application.add_handler(euro_handler)
    application.add_handler(unknown_handler)  # This handler must be added last.

    application.run_polling()
