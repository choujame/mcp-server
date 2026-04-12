import os
import logging
from telegram import Bot
from telegram.error import TelegramError
from dotenv import load_dotenv

logger = logging.getLogger("telegram-manager")


class TelegramManager:
    """Manages Telegram bot communications and notifications."""

    def __init__(self):
        """Initialize Telegram manager with bot token and chat ID."""
        load_dotenv()
        self.bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        self.bot = None

        if self.bot_token and self.chat_id:
            try:
                self.bot = Bot(token=self.bot_token)
                logger.info("Telegram Bot initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Telegram Bot: {e}")

    async def send_message(self, message: str, chat_id: str | None = None) -> dict:
        """Send a message via Telegram.

        Args:
            message: The message text to send
            chat_id: Optional specific chat ID (uses default if not provided)

        Returns:
            Dictionary with status and message ID or error
        """
        if not self.bot:
            return {"error": "Telegram Bot not configured. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env"}

        target_chat_id = chat_id or self.chat_id
        if not target_chat_id:
            return {"error": "No chat ID provided or configured"}

        try:
            msg = await self.bot.send_message(chat_id=target_chat_id, text=message)
            logger.info(f"Message sent successfully to {target_chat_id}")
            return {
                "status": "success",
                "message_id": msg.message_id,
                "chat_id": msg.chat_id
            }
        except TelegramError as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return {"error": str(e)}

    async def send_alert(self, alert_type: str, ticker: str, message: str) -> dict:
        """Send a financial alert via Telegram.

        Args:
            alert_type: Type of alert (price_change, news, earnings, etc.)
            ticker: Stock ticker symbol
            message: Alert message

        Returns:
            Dictionary with status or error
        """
        formatted_message = f"🚨 **{alert_type.upper()} ALERT** 🚨\n"
        formatted_message += f"📊 Ticker: {ticker}\n"
        formatted_message += f"📝 {message}"

        return await self.send_message(formatted_message)

    async def get_bot_info(self) -> dict:
        """Get information about the Telegram bot.

        Returns:
            Dictionary with bot information or error
        """
        if not self.bot:
            return {"error": "Telegram Bot not configured"}

        try:
            me = await self.bot.get_me()
            return {
                "bot_username": me.username,
                "bot_name": me.first_name,
                "is_bot": me.is_bot,
                "can_join_groups": me.can_join_groups
            }
        except TelegramError as e:
            logger.error(f"Failed to get bot info: {e}")
            return {"error": str(e)}


# Global instance
_telegram_manager = None


def get_telegram_manager() -> TelegramManager:
    """Get or create the global Telegram manager instance."""
    global _telegram_manager
    if _telegram_manager is None:
        _telegram_manager = TelegramManager()
    return _telegram_manager
