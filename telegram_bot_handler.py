import logging
import os
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError
from stock_analyzer import get_stock_analyzer
from dotenv import load_dotenv

logger = logging.getLogger("telegram-bot-handler")
load_dotenv()


class TelegramBotHandler:
    """Handles Telegram bot commands and messages."""

    def __init__(self):
        self.bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        self.app = None
        self.analyzer = get_stock_analyzer()

        if not self.bot_token:
            logger.error("❌ TELEGRAM_BOT_TOKEN not configured!")
        if not self.chat_id:
            logger.error("❌ TELEGRAM_CHAT_ID not configured!")

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
        try:
            await update.message.reply_text(message)
            logger.info("✅ /start response sent")
        except Exception as e:
            logger.error(f"❌ Error in /start: {e}")

    async def scan_tw_ma(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /tw_ma command - scan Taiwan stocks."""
        logger.info("📍 /tw_ma command received")
        try:
            await update.message.reply_text("📊 正在掃描台股 MA 回撤機會，請稍候...")

            results = self.analyzer.get_ma_crossover_stocks(market="tw", days=5)
            message = self.analyzer.format_results(results)

            await update.message.reply_text(message)
            logger.info("✅ /tw_ma response sent successfully")
        except Exception as e:
            logger.error(f"❌ Error in /tw_ma: {e}", exc_info=True)
            await update.message.reply_text(f"❌ 掃描失敗: {str(e)}")

    async def scan_us_ma(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /us_ma command - scan US stocks."""
        logger.info("📍 /us_ma command received")
        try:
            await update.message.reply_text("📊 正在掃描美股 MA 回撤機會，請稍候...")

            results = self.analyzer.get_ma_crossover_stocks(market="us", days=5)
            message = self.analyzer.format_results(results)

            await update.message.reply_text(message)
            logger.info("✅ /us_ma response sent successfully")
        except Exception as e:
            logger.error(f"❌ Error in /us_ma: {e}", exc_info=True)
            await update.message.reply_text(f"❌ 掃描失敗: {str(e)}")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command."""
        logger.info("📍 /help command received")
        message = """
📚 使用幫助

📊 股票掃描命令:
• /tw_ma - 掃描台股 MA 回撤
• /us_ma - 掃描美股 MA 回撤

💡 MA 回撤是什麼?
移動平均線短期回撤,但仍保持中期上升趨勢的股票。
這通常被視為買點。

📈 趨勢標記:
• BULLISH (看漲) - 股價在 MA20 上方
• BEARISH (看跌) - 股價在 MA20 下方

⚠️ 免責聲明:
本分析僅供參考,不構成投資建議。
投資有風險,請自行研究和評估。
"""
        try:
            await update.message.reply_text(message)
            logger.info("✅ /help response sent")
        except Exception as e:
            logger.error(f"❌ Error in /help: {e}")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle regular messages."""
        text = update.message.text.lower()
        logger.info(f"📍 Message received: {text[:50]}")

        if "台股" in text and ("ma" in text or "移動平均" in text or "回撤" in text):
            await self.scan_tw_ma(update, context)
        elif "美股" in text and ("ma" in text or "移動平均" in text or "回撤" in text):
            await self.scan_us_ma(update, context)
        else:
            response = """
❓ 未理解的命令。

試試以下命令:
• /tw_ma - 掃描台股
• /us_ma - 掃描美股
• /help - 幫助
"""
            await update.message.reply_text(response)
            logger.info(f"ℹ️ Unknown message, sent help")

    async def initialize(self) -> None:
        """Initialize the Telegram bot."""
        if not self.bot_token:
            logger.error("❌ Cannot initialize: TELEGRAM_BOT_TOKEN not set")
            return

        try:
            logger.info("🔧 Creating Telegram Application with token...")
            self.app = Application.builder().token(self.bot_token).build()

            # Register command handlers
            logger.info("📋 Registering command handlers...")
            self.app.add_handler(CommandHandler("start", self.start))
            self.app.add_handler(CommandHandler("tw_ma", self.scan_tw_ma))
            self.app.add_handler(CommandHandler("us_ma", self.scan_us_ma))
            self.app.add_handler(CommandHandler("help", self.help_command))

            # Register text message handler (for natural language)
            self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

            logger.info("✅ Telegram bot handler initialized successfully!")
            logger.info(f"   ✓ Bot Token: {self.bot_token[:20]}...")
            logger.info(f"   ✓ Chat ID: {self.chat_id}")
            logger.info(f"   ✓ Commands: /start, /tw_ma, /us_ma, /help")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Telegram bot: {e}", exc_info=True)
            raise

    async def run(self) -> None:
        """Run the bot with polling."""
        if not self.app:
            logger.error("❌ App not initialized. Call initialize() first.")
            await self.initialize()

        if self.app:
            logger.info("🚀 Starting Telegram bot polling...")
            logger.info("   Listening for messages... Press Ctrl+C to stop")
            try:
                await self.app.run_polling(allowed_updates=Update.ALL_TYPES)
            except Exception as e:
                logger.error(f"❌ Error during polling: {e}", exc_info=True)
            finally:
                logger.info("Bot polling stopped")


# Global instance
_bot_handler = None


def get_telegram_bot_handler() -> TelegramBotHandler:
    """Get or create the global telegram bot handler."""
    global _bot_handler
    if _bot_handler is None:
        _bot_handler = TelegramBotHandler()
    return _bot_handler


async def run_telegram_bot():
    """Run the Telegram bot."""
    handler = get_telegram_bot_handler()
    await handler.initialize()
    await handler.run()
