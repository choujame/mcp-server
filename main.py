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
from concurrent.futures import ThreadPoolExecutor
import server
from telegram_bot_handler import run_telegram_bot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("main")


def run_mcp_server():
    """Run the MCP server in stdio mode."""
    logger.info("Starting MCP server...")
    server.mcp.run(transport="stdio")


async def run_services():
    """Run both MCP server and Telegram bot concurrently."""
    # Run Telegram bot in a thread pool
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(max_workers=1)

    # Start Telegram bot in background
    try:
        await run_telegram_bot()
    except Exception as e:
        logger.error(f"Telegram bot error: {e}")


if __name__ == "__main__":
    import threading

    logger.info("Initializing services...")

    # Start Telegram bot in a separate thread
    telegram_thread = threading.Thread(target=lambda: asyncio.run(run_services()), daemon=True)
    telegram_thread.start()
    logger.info("Telegram bot handler started in background")

    # Run MCP server in main thread
    logger.info("Starting MCP server on stdio...")
    run_mcp_server()
