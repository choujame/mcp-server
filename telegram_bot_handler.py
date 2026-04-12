import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram_manager import get_telegram_manager
from stock_analyzer import get_stock_analyzer
from dotenv import load_dotenv
import os

logger = logging.getLogger("telegram-bot-handler")

load_dotenv()


class TelegramBotHandler:
    """Handles Telegram bot commands and messages."""

    def __init__(self):
        self.bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        self.app = None
        self.analyzer = get_stock_analyzer()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command."""
        message = """
👋 歡迎使用 MCP 股票分析 Bot!

可用命令:
🇹🇼 /tw_ma - 掃描台股 MA 回撤機會
🇺🇸 /us_ma - 掃描美股 MA 回撤機會
📊 /help - 幫助信息
💰 /stock <ticker> - 查詢股票信息

例如: /tw_ma 或 /us_ma
"""
        await update.message.reply_text(message)

    async def scan_tw_ma(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /tw_ma command - scan Taiwan stocks."""
        await update.message.reply_text("📊 正在掃描台股 MA 回撤機會，請稍候...")

        try:
            results = self.analyzer.get_ma_crossover_stocks(market="tw", days=5)
            message = self.analyzer.format_results(results)
            await update.message.reply_text(message)
        except Exception as e:
            logger.error(f"Error scanning TW stocks: {e}")
            await update.message.reply_text(f"❌ 掃描失敗: {str(e)}")

    async def scan_us_ma(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /us_ma command - scan US stocks."""
        await update.message.reply_text("📊 正在掃描美股 MA 回撤機會，請稍候...")

        try:
            results = self.analyzer.get_ma_crossover_stocks(market="us", days=5)
            message = self.analyzer.format_results(results)
            await update.message.reply_text(message)
        except Exception as e:
            logger.error(f"Error scanning US stocks: {e}")
            await update.message.reply_text(f"❌ 掃描失敗: {str(e)}")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command."""
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
        await update.message.reply_text(message)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle regular messages."""
        text = update.message.text.lower()

        if "台股" in text and ("ma" in text or "移動平均" in text):
            await self.scan_tw_ma(update, context)
        elif "美股" in text and ("ma" in text or "移動平均" in text):
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

    async def initialize(self) -> None:
        """Initialize the Telegram bot."""
        if not self.bot_token:
            logger.error("TELEGRAM_BOT_TOKEN not configured")
            return

        logger.info("Creating Telegram Application...")
        self.app = Application.builder().token(self.bot_token).build()

        # Add handlers in order of specificity
        logger.info("Registering command handlers...")
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("tw_ma", self.scan_tw_ma))
        self.app.add_handler(CommandHandler("us_ma", self.scan_us_ma))
        self.app.add_handler(CommandHandler("help", self.help_command))

        # Message handler for any text that's not a command
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

        logger.info("✅ Telegram bot handler initialized successfully")
        logger.info(f"✅ Bot Token configured: {self.bot_token[:20]}...")
        logger.info(f"✅ Chat ID configured: {self.chat_id}")

    async def run(self) -> None:
        """Run the bot with polling."""
        if not self.app:
            await self.initialize()

        if self.app:
            await self.app.run_polling()


# Global instance
_bot_handler = None


def get_telegram_bot_handler() -> TelegramBotHandler:
    """Get or create the global telegram bot handler."""
    global _bot_handler
    if _bot_handler is None:
        _bot_handler = TelegramBotHandler()
    return _bot_handler


async def run_telegram_bot():
    """Run the Telegram bot in the background."""
    handler = get_telegram_bot_handler()
    await handler.initialize()
    await handler.run()
