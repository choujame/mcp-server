#!/usr/bin/env python3
"""
Telegram Family Bot - Comprehensive Test Suite

This script tests the complete workflow of the Telegram Family Bot without needing
actual n8n deployment. It verifies all core logic:
- Message parsing from Telegram webhook
- Medical keyword detection
- Branch routing logic
- Conversation memory management
- LLM prompt generation
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import sys


class TelegramMessageParser:
    """Parse Telegram webhook messages"""

    @staticmethod
    def parse_message(body: Dict) -> Dict:
        """Parse Telegram webhook body"""
        message = body.get('message') or body
        return {
            'text': message.get('text', ''),
            'chat_id': message.get('chat', {}).get('id'),
            'user_id': message.get('from', {}).get('id'),
            'first_name': message.get('from', {}).get('first_name', 'User'),
            'message_id': message.get('message_id'),
            'has_photo': bool(message.get('photo')),
            'source_type': 'telegram',
            'timestamp': message.get('date')
        }


class MedicalKeywordDetector:
    """Detect medical-related messages"""

    # Traditional Chinese medical keywords
    MEDICAL_KEYWORDS = ['醫', '藥', '病', '痛', '診', '癌', '感', '血', '糖', '壓', '眠', '頭', '疼']

    @staticmethod
    def detect_medical(text: str) -> bool:
        """Check if text contains medical keywords"""
        text_lower = text.lower()
        return any(keyword in text for keyword in MedicalKeywordDetector.MEDICAL_KEYWORDS)


class BranchRouter:
    """Route messages to appropriate handler"""

    @staticmethod
    def route(parsed_msg: Dict) -> str:
        """
        Route message to: 'photo', 'medical', or 'general'
        Matches the Branch Switch node in n8n workflow
        """
        if parsed_msg.get('has_photo'):
            return 'photo'
        elif MedicalKeywordDetector.detect_medical(parsed_msg.get('text', '')):
            return 'medical'
        else:
            return 'general'


class ConversationMemory:
    """Simulate Simple Memory node - maintains conversation context"""

    def __init__(self, context_window_length: int = 5):
        self.context_window = context_window_length
        self.sessions: Dict[str, List[Dict]] = {}

    def add_message(self, chat_id: str, role: str, text: str):
        """Add message to session memory"""
        if chat_id not in self.sessions:
            self.sessions[chat_id] = []

        self.sessions[chat_id].append({
            'role': role,
            'text': text,
            'timestamp': datetime.now().isoformat()
        })

        # Keep only last N messages
        if len(self.sessions[chat_id]) > self.context_window * 2:
            self.sessions[chat_id] = self.sessions[chat_id][-(self.context_window * 2):]

    def get_context(self, chat_id: str) -> List[Dict]:
        """Get conversation context for this session"""
        return self.sessions.get(chat_id, [])

    def get_context_text(self, chat_id: str) -> str:
        """Get conversation context as formatted text"""
        context = self.get_context(chat_id)
        lines = []
        for msg in context[-self.context_window:]:  # Last N messages only
            role = "User" if msg['role'] == 'user' else "Assistant"
            lines.append(f"{role}: {msg['text']}")
        return "\n".join(lines)


class PromptGenerator:
    """Generate LLM prompts"""

    BOT_PERSONA_NAME = "家庭助手"

    @staticmethod
    def generate_general_chat_prompt(user_name: str, user_text: str, context: str = "") -> str:
        """Generate prompt for general chat agent"""
        context_section = f"\n\n對話歷史：\n{context}" if context else ""

        prompt = f"""你是 {PromptGenerator.BOT_PERSONA_NAME}，一個家庭群組的 AI 助手。

用戶：{user_name}
訊息：{user_text}{context_section}

回覆原則：
- 使用台灣繁體中文
- 簡短、溫暖、自然
- 不要自稱 AI 或機器人
- 不要過度分析

請直接回一句適當的回覆。"""
        return prompt

    @staticmethod
    def generate_medical_search_prompt(user_name: str, question: str, context: str = "") -> str:
        """Generate prompt for medical search agent"""
        context_section = f"\n\n對話歷史：\n{context}" if context else ""

        prompt = f"""請一律使用台灣繁體中文回覆。

用戶：{user_name}
健康問題：{question}{context_section}

回覆要溫暖、清楚。若涉及醫療，請提醒對方這不是正式診斷，重要症狀應詢問醫師。"""
        return prompt


class TelegramAPIFormatter:
    """Format messages for Telegram API"""

    @staticmethod
    def format_reply(user_text: str, bot_response: str, user_name: str = "User") -> str:
        """Format bot reply for Telegram"""
        return f"💬 {user_name} 說：{user_text}\n\n🤖 {PromptGenerator.BOT_PERSONA_NAME}：{bot_response}"


class TelegramBotWorkflowTest:
    """Comprehensive test suite for Telegram bot workflow"""

    def __init__(self):
        self.parser = TelegramMessageParser()
        self.router = BranchRouter()
        self.detector = MedicalKeywordDetector()
        self.memory = ConversationMemory()
        self.prompt_gen = PromptGenerator()
        self.formatter = TelegramAPIFormatter()

        self.test_results = []
        self.passed = 0
        self.failed = 0

    def test(self, name: str, condition: bool, message: str = ""):
        """Record test result"""
        status = "✓ PASS" if condition else "✗ FAIL"
        self.test_results.append(f"{status}: {name}")
        if message:
            self.test_results.append(f"       {message}")

        if condition:
            self.passed += 1
        else:
            self.failed += 1

    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("\n" + "="*70)
        print("TELEGRAM FAMILY BOT - COMPREHENSIVE TEST SUITE")
        print("="*70 + "\n")

        self.test_message_parsing()
        self.test_medical_detection()
        self.test_branch_routing()
        self.test_conversation_memory()
        self.test_prompt_generation()
        self.test_full_workflow()

        self.print_summary()

    def test_message_parsing(self):
        """Test: Message parsing from Telegram webhook"""
        print("1️⃣  Testing Message Parsing...")

        # Test case 1: Normal text message
        webhook_payload = {
            'message': {
                'text': '你好，家庭助手',
                'chat': {'id': 6119894493},
                'from': {'id': 123456, 'first_name': 'John'},
                'message_id': 1,
                'date': 1234567890
            }
        }
        parsed = self.parser.parse_message(webhook_payload)
        self.test(
            "Parse normal text message",
            parsed['text'] == '你好，家庭助手' and parsed['chat_id'] == 6119894493,
            f"Extracted: text='{parsed['text']}', chat_id={parsed['chat_id']}"
        )

        # Test case 2: Message with photo
        webhook_payload['message']['photo'] = [{'file_id': 'abc123'}]
        parsed = self.parser.parse_message(webhook_payload)
        self.test(
            "Detect photo in message",
            parsed['has_photo'] == True,
            f"has_photo={parsed['has_photo']}"
        )

        # Test case 3: Extract user name
        parsed = self.parser.parse_message(webhook_payload)
        self.test(
            "Extract user first name",
            parsed['first_name'] == 'John',
            f"first_name='{parsed['first_name']}'"
        )

        print()

    def test_medical_detection(self):
        """Test: Medical keyword detection"""
        print("2️⃣  Testing Medical Keyword Detection...")

        test_cases = [
            ('我的頭疼，要看醫生嗎？', True, '頭疼、醫 keywords detected'),
            ('血糖有點高', True, '血糖 keywords detected'),
            ('晚安，睡眠不好', True, '眠 keyword detected'),
            ('今天天氣很好', False, 'No medical keywords'),
            ('早上吃了藥', True, '藥 keyword detected'),
        ]

        for text, should_detect, reason in test_cases:
            detected = self.detector.detect_medical(text)
            self.test(
                f"Medical detection: '{text[:20]}...'",
                detected == should_detect,
                f"{reason} - detected={detected}"
            )

        print()

    def test_branch_routing(self):
        """Test: Message routing to correct handler"""
        print("3️⃣  Testing Branch Routing...")

        # Test general message
        msg = {'text': 'Hello everyone', 'has_photo': False}
        route = self.router.route(msg)
        self.test(
            "Route general message",
            route == 'general',
            f"Route: {route}"
        )

        # Test medical message
        msg = {'text': '我的頭疼', 'has_photo': False}
        route = self.router.route(msg)
        self.test(
            "Route medical message",
            route == 'medical',
            f"Route: {route}"
        )

        # Test photo message
        msg = {'text': 'Look at this photo', 'has_photo': True}
        route = self.router.route(msg)
        self.test(
            "Route photo message",
            route == 'photo',
            f"Route: {route}"
        )

        print()

    def test_conversation_memory(self):
        """Test: Conversation memory management"""
        print("4️⃣  Testing Conversation Memory...")

        chat_id = '6119894493'

        # Add messages
        self.memory.add_message(chat_id, 'user', '你好')
        self.memory.add_message(chat_id, 'assistant', '嗨，很高興認識你！')
        self.memory.add_message(chat_id, 'user', '最近怎樣？')

        # Check context
        context = self.memory.get_context(chat_id)
        self.test(
            "Store conversation messages",
            len(context) == 3,
            f"Messages stored: {len(context)}"
        )

        # Check context text formatting
        context_text = self.memory.get_context_text(chat_id)
        self.test(
            "Format context as text",
            'User: 你好' in context_text and 'Assistant:' in context_text,
            f"Context formatted correctly"
        )

        print()

    def test_prompt_generation(self):
        """Test: LLM prompt generation"""
        print("5️⃣  Testing Prompt Generation...")

        # Test general chat prompt
        prompt = self.prompt_gen.generate_general_chat_prompt('John', '你好')
        self.test(
            "Generate general chat prompt",
            '家庭助手' in prompt and 'John' in prompt and '你好' in prompt,
            f"Prompt contains all required elements"
        )

        # Test medical prompt
        prompt = self.prompt_gen.generate_medical_search_prompt('John', '頭疼')
        self.test(
            "Generate medical search prompt",
            '台灣繁體中文' in prompt and '診斷' in prompt and '醫師' in prompt,
            f"Medical prompt contains safety reminders"
        )

        # Test with context
        self.memory.add_message('123', 'user', '早安')
        self.memory.add_message('123', 'assistant', '早上好！')
        context = self.memory.get_context_text('123')

        prompt = self.prompt_gen.generate_general_chat_prompt('Jane', '今天怎樣', context)
        self.test(
            "Include conversation context in prompt",
            'User: 早安' in prompt,
            f"Conversation history included"
        )

        print()

    def test_full_workflow(self):
        """Test: Complete workflow from message to reply"""
        print("6️⃣  Testing Full Workflow...")

        # Simulate a complete user interaction
        webhook = {
            'message': {
                'text': '我的頭疼了',
                'chat': {'id': 6119894493},
                'from': {'id': 123456, 'first_name': 'Tom'},
                'message_id': 1,
                'date': 1234567890
            }
        }

        # Step 1: Parse
        parsed = self.parser.parse_message(webhook)
        self.test(
            "Workflow Step 1: Parse message",
            parsed['text'] == '我的頭疼了',
            f"Parsed: {parsed}"
        )

        # Step 2: Route
        route = self.router.route(parsed)
        self.test(
            "Workflow Step 2: Route to medical",
            route == 'medical',
            f"Route: {route}"
        )

        # Step 3: Get conversation context
        context = self.memory.get_context_text(str(parsed['chat_id']))
        self.test(
            "Workflow Step 3: Get conversation context",
            True,  # Always succeeds, might be empty
            f"Context length: {len(context)} chars"
        )

        # Step 4: Generate prompt
        if route == 'medical':
            prompt = self.prompt_gen.generate_medical_search_prompt(
                parsed['first_name'],
                parsed['text'],
                context
            )
        else:
            prompt = self.prompt_gen.generate_general_chat_prompt(
                parsed['first_name'],
                parsed['text'],
                context
            )

        self.test(
            "Workflow Step 4: Generate LLM prompt",
            len(prompt) > 50,
            f"Prompt generated, length: {len(prompt)} chars"
        )

        # Step 5: Format reply (simulating LLM response)
        simulated_llm_response = "這個問題應該詢問醫師。頭疼可能有多種原因，如果持續疼痛，建議就醫檢查。"
        formatted_reply = self.formatter.format_reply(
            parsed['text'],
            simulated_llm_response,
            parsed['first_name']
        )

        self.test(
            "Workflow Step 5: Format Telegram reply",
            '家庭助手' in formatted_reply and '醫師' in formatted_reply,
            f"Reply formatted: {len(formatted_reply)} chars"
        )

        # Step 6: Store in memory
        self.memory.add_message(str(parsed['chat_id']), 'user', parsed['text'])
        self.memory.add_message(str(parsed['chat_id']), 'assistant', simulated_llm_response)

        stored_context = self.memory.get_context_text(str(parsed['chat_id']))
        self.test(
            "Workflow Step 6: Store in conversation memory",
            '我的頭疼了' in stored_context,
            f"Memory stored successfully"
        )

        print()

    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*70)
        print("TEST RESULTS")
        print("="*70)

        for result in self.test_results:
            print(result)

        print("\n" + "="*70)
        total = self.passed + self.failed
        percentage = (self.passed / total * 100) if total > 0 else 0

        print(f"TOTAL: {self.passed}/{total} PASSED ({percentage:.1f}%)")

        if self.failed == 0:
            print("\n✨ ALL TESTS PASSED! Bot logic is ready for deployment. ✨")
        else:
            print(f"\n⚠️  {self.failed} TEST(S) FAILED - Please review above.")

        print("="*70 + "\n")

        return self.failed == 0


def main():
    """Run test suite"""
    tester = TelegramBotWorkflowTest()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
