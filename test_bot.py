#!/usr/bin/env python3
"""
Minimal Telegram bot - just to test if commands work at all.
"""

import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
logger.info(f"Starting bot with token: {TOKEN[:20]}...")


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"✅ START command received from {update.effective_user.id}")
    await update.message.reply_text("👋 Start command works!")


async def cmd_tw_ma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"✅ TW_MA command received from {update.effective_user.id}")
    await update.message.reply_text("📊 Taiwan MA scanning... (stub)")


async def cmd_us_ma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"✅ US_MA command received from {update.effective_user.id}")
    await update.message.reply_text("📊 US MA scanning... (stub)")


async def main():
    app = Application.builder().token(TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("tw_ma", cmd_tw_ma))
    app.add_handler(CommandHandler("us_ma", cmd_us_ma))

    logger.info("Starting polling...")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
