#!/usr/bin/env python3
"""
Telegram Family Bot - API Integration Test

This script tests actual integration with:
1. Telegram Bot API - sending messages
2. Groq LLM API - generating responses

To run this test, set environment variables:
  export TELEGRAM_BOT_TOKEN="your_token_here"
  export GROQ_API_KEY="your_groq_api_key_here"
  export TEST_CHAT_ID="your_chat_id_here"

Or pass them as arguments:
  python3 test_telegram_api_integration.py --telegram-token xxx --groq-key yyy --chat-id zzz
"""

import os
import sys
import json
import argparse
import requests
from typing import Optional, Dict, Tuple
from datetime import datetime


class TelegramAPIClient:
    """Test Telegram Bot API"""

    def __init__(self, token: str):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"

    def test_connection(self) -> Tuple[bool, str]:
        """Test if token is valid"""
        try:
            response = requests.get(f"{self.base_url}/getMe", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    bot_info = data.get('result', {})
                    return True, f"✓ Bot found: @{bot_info.get('username')} (ID: {bot_info.get('id')})"
            return False, f"✗ Invalid response: {response.text}"
        except Exception as e:
            return False, f"✗ Connection error: {str(e)}"

    def send_test_message(self, chat_id: str, text: str) -> Tuple[bool, str]:
        """Send a test message"""
        try:
            payload = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML"
            }
            response = requests.post(
                f"{self.base_url}/sendMessage",
                json=payload,
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    msg = data.get('result', {})
                    return True, f"✓ Message sent (ID: {msg.get('message_id')})"
            return False, f"✗ Send failed: {response.text}"
        except Exception as e:
            return False, f"✗ Error: {str(e)}"


class GroqAPIClient:
    """Test Groq LLM API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = "llama-3.3-70b-versatile"

    def test_connection(self) -> Tuple[bool, str]:
        """Test if API key is valid"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": "Hello"}],
                    "max_tokens": 10
                },
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                if data.get('choices'):
                    return True, f"✓ Groq API working (Model: {self.model})"
            return False, f"✗ Invalid response: {response.text[:100]}"
        except requests.exceptions.Timeout:
            return False, "✗ Timeout - Groq API not responding"
        except Exception as e:
            return False, f"✗ Error: {str(e)}"

    def generate_response(self, prompt: str) -> Tuple[bool, str]:
        """Generate a response from the LLM"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a helpful family assistant. Always respond in Traditional Chinese."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 150,
                "temperature": 0.7
            }

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                message = data.get('choices', [{}])[0].get('message', {}).get('content', '')
                if message:
                    tokens_used = data.get('usage', {}).get('total_tokens', 0)
                    return True, f"✓ Response generated\n     {message[:100]}...\n     (Tokens: {tokens_used})"
            return False, f"✗ Generation failed: {response.text[:100]}"
        except requests.exceptions.Timeout:
            return False, "✗ Timeout - Generation took too long"
        except Exception as e:
            return False, f"✗ Error: {str(e)}"


class WorkflowIntegrationTest:
    """Test complete workflow with real APIs"""

    def __init__(self, telegram_token: Optional[str], groq_key: Optional[str], chat_id: Optional[str]):
        self.telegram_token = telegram_token
        self.groq_key = groq_key
        self.chat_id = chat_id

        self.telegram = TelegramAPIClient(telegram_token) if telegram_token else None
        self.groq = GroqAPIClient(groq_key) if groq_key else None

        self.results = []

    def test_telegram_api(self) -> bool:
        """Test Telegram API integration"""
        print("\n1️⃣  Testing Telegram Bot API...")

        if not self.telegram_token:
            print("   ⚠️  TELEGRAM_BOT_TOKEN not provided, skipping Telegram tests")
            return False

        # Test connection
        success, message = self.telegram.test_connection()
        self.results.append(("Telegram API Connection", success, message))
        print(f"   {message}")

        if not success:
            return False

        # Test sending message
        if self.chat_id:
            test_msg = f"🤖 Test from n8n bot at {datetime.now().strftime('%H:%M:%S')}"
            success, message = self.telegram.send_test_message(self.chat_id, test_msg)
            self.results.append(("Send Test Message", success, message))
            print(f"   {message}")

        return True

    def test_groq_api(self) -> bool:
        """Test Groq LLM API"""
        print("\n2️⃣  Testing Groq LLM API...")

        if not self.groq_key:
            print("   ⚠️  GROQ_API_KEY not provided, skipping Groq tests")
            return False

        # Test connection
        success, message = self.groq.test_connection()
        self.results.append(("Groq API Connection", success, message))
        print(f"   {message}")

        if not success:
            return False

        # Test generation - general chat
        print("   Testing general chat response...")
        prompt = "家人們，我今天很開心。"
        success, message = self.groq.generate_response(prompt)
        self.results.append(("General Chat Response", success, message))
        print(f"   {message}")

        # Test generation - medical
        print("   Testing medical response...")
        prompt = "我的頭疼了怎麼辦？"
        success, message = self.groq.generate_response(prompt)
        self.results.append(("Medical Query Response", success, message))
        print(f"   {message}")

        return True

    def test_end_to_end(self) -> bool:
        """Test complete workflow"""
        print("\n3️⃣  Testing End-to-End Workflow...")

        if not (self.telegram and self.groq and self.chat_id):
            print("   ⚠️  Missing credentials for end-to-end test")
            return False

        print("   Simulating: User message → Parse → Route → Generate → Send")

        # Simulate workflow
        user_message = "我今天感到很疲憊"

        # Step 1: Detect medical
        print(f"   Step 1: User message: '{user_message}'")

        medical_keywords = ['醫', '藥', '病', '痛', '診', '癌', '感', '血', '糖', '壓', '眠', '頭', '疼']
        is_medical = any(kw in user_message for kw in medical_keywords)
        print(f"   Step 2: Is medical? {is_medical}")

        # Step 2: Generate response
        if is_medical:
            prompt = f"用戶問：{user_message}\n\n請用台灣繁體中文簡短溫暖地回應。"
        else:
            prompt = f"家庭群組中有人說：{user_message}\n\n請用台灣繁體中文簡短溫暖地回應。"

        success, message = self.groq.generate_response(prompt)
        print(f"   Step 3: Generate response - {message.split('(')[0]}")

        if success:
            # Step 3: Send to Telegram
            response_text = message.split('\n')[1] if '\n' in message else "回應已生成"
            full_reply = f"📱 User said: {user_message}\n\n🤖 Assistant: {response_text}"

            success2, message2 = self.telegram.send_test_message(self.chat_id, full_reply)
            print(f"   Step 4: Send to Telegram - {message2}")
            self.results.append(("End-to-End Workflow", success2, message2))
            return success2

        return False

    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*70)
        print("API INTEGRATION TEST RESULTS")
        print("="*70)

        for test_name, success, message in self.results:
            status = "✓" if success else "✗"
            print(f"{status} {test_name}")
            if message:
                lines = message.split('\n')
                for line in lines:
                    if line.strip():
                        print(f"  {line}")

        print("\n" + "="*70)

        passed = sum(1 for _, s, _ in self.results if s)
        total = len(self.results)

        if total == 0:
            print("⚠️  No tests could be run (missing credentials)")
        elif passed == total:
            print(f"✨ ALL {total} TESTS PASSED - APIs are ready! ✨")
        else:
            print(f"⚠️  {passed}/{total} tests passed - check configuration")

        print("="*70 + "\n")


def main():
    """Run API integration tests"""
    parser = argparse.ArgumentParser(
        description="Test Telegram Bot and Groq LLM API integration"
    )
    parser.add_argument('--telegram-token', help='Telegram Bot Token')
    parser.add_argument('--groq-key', help='Groq API Key')
    parser.add_argument('--chat-id', help='Telegram Chat ID for testing')

    args = parser.parse_args()

    # Get credentials from arguments or environment
    telegram_token = args.telegram_token or os.getenv('TELEGRAM_BOT_TOKEN')
    groq_key = args.groq_key or os.getenv('GROQ_API_KEY')
    chat_id = args.chat_id or os.getenv('TEST_CHAT_ID')

    print("\n" + "="*70)
    print("TELEGRAM FAMILY BOT - API INTEGRATION TEST")
    print("="*70)

    print("\n📋 Configuration:")
    print(f"  Telegram Bot: {'✓ Configured' if telegram_token else '✗ Not provided'}")
    print(f"  Groq API: {'✓ Configured' if groq_key else '✗ Not provided'}")
    print(f"  Test Chat ID: {'✓ Configured' if chat_id else '✗ Not provided'}")

    tester = WorkflowIntegrationTest(telegram_token, groq_key, chat_id)

    # Run tests
    tester.test_telegram_api()
    tester.test_groq_api()
    tester.test_end_to_end()

    # Print results
    tester.print_summary()


if __name__ == '__main__':
    main()
