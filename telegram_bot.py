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
    try:
        logger.info(f"📍 /start command from {update.effective_user.id}")
        message = """
👋 歡迎使用 MCP 股票分析 Bot！

━━━━━━━━━━━━━━━━━━━━━━

📊 快速命令：
  🇹🇼 /tw_ma - 台股 MA 回撤掃描
  🇺🇸 /us_ma - 美股 MA 回撤掃描

📈 進階功能：
  📊 /week_ma - 週線分析
  📋 /history - 歷史股價
  📈 /chart - 走勢圖表

❓ /help - 完整使用指南

━━━━━━━━━━━━━━━━━━━━━━

💡 快速開始：
輸入 /tw_ma 即可查看台股機會
輸入 /us_ma 即可查看美股機會
輸入 /help 查看詳細說明

⚠️ 免責聲明：
本分析僅供參考，投資有風險。
"""
        await update.message.reply_text(message)
        logger.info("✅ /start response sent successfully")
    except Exception as e:
        logger.error(f"❌ Error in /start: {e}", exc_info=True)
        try:
            await update.message.reply_text("⚠️ 命令處理出錯")
        except:
            pass


async def scan_tw_ma(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /tw_ma command."""
    logger.info(f"📍 /tw_ma command from user {update.effective_user.id}")

    try:
        # Send "waiting" message
        await update.message.reply_text("📊 正在掃描台股 MA 回撤機會，請稍候...")
        logger.info("   Waiting message sent")

        # Get analysis
        logger.info("   Analyzing stocks...")
        results = analyzer.get_ma_crossover_stocks(market="tw", days=5)

        # Format results
        logger.info("   Formatting results...")
        message = analyzer.format_results(results)

        # Send results
        logger.info("   Sending results...")
        await update.message.reply_text(message)
        logger.info("✅ /tw_ma completed successfully")

    except Exception as e:
        logger.error(f"❌ Error in /tw_ma: {e}", exc_info=True)
        try:
            await update.message.reply_text(f"❌ 掃描失敗: {str(e)[:100]}")
        except:
            pass


async def scan_us_ma(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /us_ma command."""
    logger.info(f"📍 /us_ma command from user {update.effective_user.id}")

    try:
        # Send "waiting" message
        await update.message.reply_text("📊 正在掃描美股 MA 回撤機會，請稍候...")
        logger.info("   Waiting message sent")

        # Get analysis
        logger.info("   Analyzing stocks...")
        results = analyzer.get_ma_crossover_stocks(market="us", days=5)

        # Format results
        logger.info("   Formatting results...")
        message = analyzer.format_results(results)

        # Send results
        logger.info("   Sending results...")
        await update.message.reply_text(message)
        logger.info("✅ /us_ma completed successfully")

    except Exception as e:
        logger.error(f"❌ Error in /us_ma: {e}", exc_info=True)
        try:
            await update.message.reply_text(f"❌ 掃描失敗: {str(e)[:100]}")
        except:
            pass


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    logger.info("📍 /help command received")
    message = """
📚 完整使用指南

━━━━━━━━━━━━━━━━━━━━━━

📊 基礎掃描命令：
  🇹🇼 /tw_ma - 台股 MA 回撤五日掃描
  🇺🇸 /us_ma - 美股 MA 回撤五日掃描

📈 進階分析命令：
  📊 /week_ma - 週線 MA 分析
  📋 /history - 過去七天股價記錄
  📈 /chart - 股價走勢圖表

❓ /help - 查看本幫助信息

━━━━━━━━━━━━━━━━━━━━━━

💡 什麼是 MA 回撤？
移動平均線短期回撤，但仍保持中期上升趨勢。
這通常被視為良好買點。

📊 如何解讀結果？
• 現價：目前股票價格
• MA5、MA10、MA20：5日、10日、20日移動平均線
• 支撐：近期低點（買入區域）
• 壓力：近期高點（賣出區域）
• 趨勢：看漲(BULLISH) 或 看跌(BEARISH)

⚠️ 免責聲明：
本分析僅供參考，不構成投資建議。
投資有風險，請自行評估與決定。
"""
    await update.message.reply_text(message)
    logger.info("✅ /help response sent")


async def week_ma(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /week_ma command - weekly MA analysis."""
    logger.info(f"📍 /week_ma command from {update.effective_user.id}")

    try:
        await update.message.reply_text("📊 正在分析週線數據，請稍候...")

        # Analyze top Taiwan stocks
        stocks = ["2330.TW", "2454.TW", "3008.TW"]
        message = "📊 台股週線 MA 分析\n" + "━" * 40 + "\n\n"

        for ticker in stocks:
            result = analyzer.get_weekly_ma_analysis(ticker)
            message += analyzer.format_weekly_analysis(result) + "\n"

        await update.message.reply_text(message)
        logger.info("✅ /week_ma completed successfully")
    except Exception as e:
        logger.error(f"❌ Error in /week_ma: {e}", exc_info=True)
        try:
            await update.message.reply_text(f"❌ 週線分析失敗：{str(e)[:100]}")
        except:
            pass


async def history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /history command - show historical data."""
    logger.info(f"📍 /history command from {update.effective_user.id}")

    try:
        await update.message.reply_text("📋 正在獲取歷史股價數據，請稍候...")

        # Show history for top stocks
        stocks = ["2330.TW", "AAPL"]
        message = "📋 最近七天股價記錄\n" + "━" * 40 + "\n\n"

        for ticker in stocks:
            result = analyzer.get_historical_data(ticker, days=7)
            message += analyzer.format_historical_data(result) + "\n"

        await update.message.reply_text(message)
        logger.info("✅ /history completed successfully")
    except Exception as e:
        logger.error(f"❌ Error in /history: {e}", exc_info=True)
        try:
            await update.message.reply_text(f"❌ 歷史數據獲取失敗：{str(e)[:100]}")
        except:
            pass


async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /chart command - show price charts."""
    logger.info(f"📍 /chart command from {update.effective_user.id}")

    try:
        message = """
📈 股價走勢圖表（30天）

━━━━━━━━━━━━━━━━━━━━━━

🇹🇼 台股圖表：
  🔹 2330.TW - 台積電（TSM）
  🔹 2454.TW - 聯發科（MediaTek）
  🔹 3008.TW - 瑞昱（Realtek）

🇺🇸 美股圖表：
  🔹 AAPL - 蘋果
  🔹 MSFT - 微軟
  🔹 GOOGL - 谷歌

━━━━━━━━━━━━━━━━━━━━━━

💡 提示：
市場開盤後將顯示實時圖表。
週一到週五美股開盤時段可查看。

📊 圖表包含：
  • 30天股價走勢
  • 開盤、收盤、高低價
  • 移動平均線（MA5、MA20）
"""
        await update.message.reply_text(message)
        logger.info("✅ /chart completed successfully")
    except Exception as e:
        logger.error(f"❌ Error in /chart: {e}", exc_info=True)
        try:
            await update.message.reply_text(f"❌ 圖表生成失敗：{str(e)[:100]}")
        except:
            pass


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

    # Add handlers - order matters!
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tw_ma", scan_tw_ma))
    app.add_handler(CommandHandler("us_ma", scan_us_ma))
    app.add_handler(CommandHandler("week_ma", week_ma))
    app.add_handler(CommandHandler("history", history))
    app.add_handler(CommandHandler("chart", chart))
    app.add_handler(CommandHandler("help", help_command))

    # Add text handler AFTER command handlers
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
