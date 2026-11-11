import asyncio
import logging
import sqlite3
from datetime import datetime, timezone

import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters,
)

from config import TOKEN
from currency_crawler import refresh_prices
from db_functions import create_table, retrieve_latest

REFRESH_INTERVAL_SECONDS = 5 * 60
STALE_AFTER_SECONDS = 15 * 60
logger = logging.getLogger(__name__)


async def refresh_job(context: ContextTypes.DEFAULT_TYPE):
    try:
        await asyncio.to_thread(refresh_prices)
    except (requests.RequestException, ValueError, sqlite3.Error):
        logger.exception("Currency refresh failed; keeping previous prices")


async def post_init(application):
    try:
        await asyncio.to_thread(create_table)
    except sqlite3.Error:
        logger.exception("Could not initialize currency database")
    job = application.job_queue.run_repeating(
        refresh_job, interval=REFRESH_INTERVAL_SECONDS,
        first=REFRESH_INTERVAL_SECONDS, name="refresh-prices",
        job_kwargs={"max_instances": 1, "coalesce": True},
    )
    await job.run(application)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=("Welcome! Prices are in tomans (1 toman = 10 rials).\n"
              "Prices refresh every 5 minutes while the bot is running.\n\n"
              "/dollar\n/euro\n/pound"),
    )


def format_price(currency, snapshot, now=None):
    if snapshot is None:
        return "Prices are not available yet. Please try again shortly."
    now = now or datetime.now(timezone.utc)
    updated = snapshot["updated_at"]
    labels = {"dollar": "US Dollar", "pound": "British Pound", "euro": "Euro"}
    message = (
        f"{labels[currency]}: {snapshot[currency]:,} tomans\n"
        f"Last successful update: {updated:%Y-%m-%d %H:%M:%S} UTC\n"
        "Source: TGJU"
    )
    if (now - updated).total_seconds() >= STALE_AFTER_SECONDS:
        message += "\nWarning: this price is stale (15 minutes or older)."
    return message


async def send_price(update, context, currency):
    try:
        snapshot = await asyncio.to_thread(retrieve_latest)
        text = format_price(currency, snapshot)
    except sqlite3.Error:
        logger.exception("Could not read currency database")
        text = "Prices are temporarily unavailable. Please try again shortly."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


async def dollar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_price(update, context, "dollar")


async def pound(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_price(update, context, "pound")


async def euro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_price(update, context, "euro")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sorry, that command is not defined. Use /start for available commands.",
    )


def build_application():
    application = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    for command, callback in (
        ("start", start), ("dollar", dollar), ("pound", pound), ("euro", euro),
    ):
        application.add_handler(CommandHandler(command, callback))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    return application


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    build_application().run_polling()
