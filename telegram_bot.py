#!/usr/bin/env python3
"""
Simple Telegram bot runner using polling mode.
"""

import logging
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging FIRST
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("telegram-bot")

logger.info("=" * 60)
logger.info("🤖 Telegram Bot Startup")
logger.info("=" * 60)

# Check configuration
bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

if not bot_token:
    logger.error("❌ TELEGRAM_BOT_TOKEN not configured!")
    sys.exit(1)

if not chat_id:
    logger.error("❌ TELEGRAM_CHAT_ID not configured!")
    sys.exit(1)

logger.info(f"✅ Bot Token: {bot_token[:20]}...")
logger.info(f"✅ Chat ID: {chat_id}")

# Import after configuration is verified
import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
from stock_analyzer import get_stock_analyzer

logger.info("✅ Dependencies imported successfully")

# Get analyzer
analyzer = get_stock_analyzer()
logger.info("✅ Stock analyzer initialized")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    logger.info("📍 /start command received")
    message = """
👋 歡迎使用 MCP 股票分析 Bot!

可用命令:
🇹🇼 /tw_ma - 掃描台股 MA 回撤機會
🇺🇸 /us_ma - 掃描美股 MA 回撤機會
📊 /help - 幫助信息

例如: /tw_ma 或 /us_ma
"""
    await update.message.reply_text(message)
    logger.info("✅ /start response sent")


async def scan_tw_ma(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /tw_ma command."""
    logger.info("📍 /tw_ma command received")
    await update.message.reply_text("📊 正在掃描台股 MA 回撤機會，請稍候...")

    try:
        results = analyzer.get_ma_crossover_stocks(market="tw", days=5)
        message = analyzer.format_results(results)
        await update.message.reply_text(message)
        logger.info("✅ /tw_ma response sent")
    except Exception as e:
        logger.error(f"❌ Error in /tw_ma: {e}", exc_info=True)
        await update.message.reply_text(f"❌ 掃描失敗: {str(e)}")


async def scan_us_ma(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /us_ma command."""
    logger.info("📍 /us_ma command received")
    await update.message.reply_text("📊 正在掃描美股 MA 回撤機會，請稍候...")

    try:
        results = analyzer.get_ma_crossover_stocks(market="us", days=5)
        message = analyzer.format_results(results)
        await update.message.reply_text(message)
        logger.info("✅ /us_ma response sent")
    except Exception as e:
        logger.error(f"❌ Error in /us_ma: {e}", exc_info=True)
        await update.message.reply_text(f"❌ 掃描失敗: {str(e)}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    logger.info("📍 /help command received")
    message = """
📚 使用幫助

📊 股票掃描命令:
• /tw_ma - 掃描台股 MA 回撤
• /us_ma - 掃描美股 MA 回撤

💡 MA 回撤是什麼?
移動平均線短期回撤，但仍保持中期上升趨勢的股票。
這通常被視為買點。

⚠️ 免責聲明:
本分析僅供參考，不構成投資建議。
"""
    await update.message.reply_text(message)
    logger.info("✅ /help response sent")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages."""
    text = update.message.text.lower()
    logger.info(f"📍 Text message: {text[:50]}")

    if "台股" in text and ("ma" in text or "移動平均" in text):
        await scan_tw_ma(update, context)
    elif "美股" in text and ("ma" in text or "移動平均" in text):
        await scan_us_ma(update, context)
    else:
        await update.message.reply_text(
            "❓ 未理解的命令。試試: /tw_ma 或 /us_ma"
        )


async def main():
    """Start the bot."""
    logger.info("🔧 Creating Telegram application...")

    app = Application.builder().token(bot_token).build()

    logger.info("📋 Adding command handlers...")
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tw_ma", scan_tw_ma))
    app.add_handler(CommandHandler("us_ma", scan_us_ma))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("✅ All handlers registered")
    logger.info("🚀 Starting bot polling...")
    logger.info("   Waiting for messages on @choujamebot...")

    await app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    logger.info("Starting event loop...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
