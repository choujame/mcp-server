#!/usr/bin/env python3
"""
Main entry point for the MCP server with Telegram bot support.

This script runs both:
1. MCP server (for Claude integration)
2. Telegram bot handler (for Telegram message processing)
"""

import asyncio
import logging
import sys
import signal
from server import mcp
from telegram_bot_handler import get_telegram_bot_handler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("main")

# Global reference for cleanup
bot_handler = None


async def start_telegram_bot():
    """Start the Telegram bot in polling mode."""
    global bot_handler
    try:
        logger.info("Initializing Telegram bot handler...")
        bot_handler = get_telegram_bot_handler()
        await bot_handler.initialize()
        logger.info("Telegram bot handler initialized, starting polling...")
        await bot_handler.run()
    except Exception as e:
        logger.error(f"Telegram bot error: {e}", exc_info=True)


def run_mcp_server():
    """Run the MCP server in stdio mode."""
    logger.info("Starting MCP server on stdio transport...")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    import threading

    logger.info("=" * 60)
    logger.info("Starting MCP Server with Telegram Bot Support")
    logger.info("=" * 60)

    # Create and start Telegram bot thread
    def run_telegram():
        try:
            asyncio.run(start_telegram_bot())
        except KeyboardInterrupt:
            logger.info("Telegram bot interrupted")
        except Exception as e:
            logger.error(f"Telegram bot fatal error: {e}", exc_info=True)

    telegram_thread = threading.Thread(target=run_telegram, daemon=True, name="TelegramBot")
    telegram_thread.start()
    logger.info("✅ Telegram bot thread started")

    # Small delay to let Telegram bot initialize
    import time
    time.sleep(2)

    # Run MCP server in main thread (blocks until interrupted)
    logger.info("✅ MCP server starting on stdio...")
    try:
        run_mcp_server()
    except KeyboardInterrupt:
        logger.info("MCP server interrupted")
    except Exception as e:
        logger.error(f"MCP server error: {e}", exc_info=True)
    finally:
        logger.info("Shutdown complete")

