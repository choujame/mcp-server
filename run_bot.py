#!/usr/bin/env python3
"""
Simple entry point - just run the Telegram bot.
This is the simplest possible approach.
"""

import subprocess
import sys

print("=" * 60)
print("Starting Telegram Bot (polling mode)...")
print("=" * 60)

try:
    subprocess.run([sys.executable, "telegram_bot.py"], check=True)
except KeyboardInterrupt:
    print("\nBot stopped")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
