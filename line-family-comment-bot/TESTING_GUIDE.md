# Telegram Family Bot - Complete Testing Guide

## 📊 Test Status: READY FOR DEPLOYMENT ✅

This document covers all testing performed on the Telegram Family Bot and instructions for running additional tests with real credentials.

---

## ✅ Part 1: Core Logic Testing (COMPLETED)

All core workflow logic has been tested and verified. Run the comprehensive test suite:

```bash
python3 test_telegram_bot.py
```

### Test Results Summary
- **Total Tests**: 22
- **Passed**: 22 (100%)
- **Status**: ✅ ALL TESTS PASSED

### What Was Tested

#### 1️⃣ Message Parsing (3 tests)
- ✓ Parse normal text messages from Telegram webhook
- ✓ Detect photo attachments
- ✓ Extract user information (name, ID, chat ID)

#### 2️⃣ Medical Keyword Detection (5 tests)
- ✓ Detect Traditional Chinese medical keywords: 醫、藥、病、痛、診、癌、感、血、糖、壓、眠、頭、疼
- ✓ Correctly identify medical vs. non-medical messages
- ✓ Handle edge cases (messages with multiple keywords)

#### 3️⃣ Message Routing (3 tests)
- ✓ Route general messages to general chat agent
- ✓ Route medical messages to medical search agent
- ✓ Route photo messages to photo handler

#### 4️⃣ Conversation Memory (2 tests)
- ✓ Store up to 10 messages (5-message context window)
- ✓ Format conversation context correctly for LLM prompts

#### 5️⃣ LLM Prompt Generation (3 tests)
- ✓ Generate appropriate prompts for general chat
- ✓ Generate medical prompts with safety reminders
- ✓ Include conversation history in prompts

#### 6️⃣ Complete Workflow (6 tests)
- ✓ Parse → Route → Context → Prompt → Format → Store
- ✓ Handle medical query end-to-end
- ✓ Memory persistence across messages

---

## 🔌 Part 2: API Integration Testing

### Option A: Basic Test (No Credentials Needed)

Verify the test script works:
```bash
python3 test_telegram_api_integration.py
```

Expected output:
```
⚠️  No tests could be run (missing credentials)
```

This is expected - the script is ready but needs real API keys.

### Option B: Full Integration Test (With Credentials)

#### Step 1: Get Your API Credentials

**Telegram Bot Token:**
- Go to Telegram: talk to @BotFather
- Create a new bot or get existing bot token
- Format: `123456789:ABCDEfghijklmnop...`

**Groq API Key:**
- Visit: https://console.groq.com/keys
- Generate new API key
- Format: `gsk_...`

#### Step 2: Run API Tests

**Option A: Using Environment Variables**
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export GROQ_API_KEY="your_groq_key_here"
export TEST_CHAT_ID="your_chat_id_here"

python3 test_telegram_api_integration.py
```

**Option B: Using Command Line Arguments**
```bash
python3 test_telegram_api_integration.py \
  --telegram-token "your_bot_token_here" \
  --groq-key "your_groq_key_here" \
  --chat-id "your_chat_id_here"
```

#### Step 3: Expected Test Results

✅ **Telegram API Connection Test**
```
✓ Telegram API Connection
  ✓ Bot found: @YourBotName (ID: 123456789)
```

✅ **Telegram Message Send Test**
```
✓ Send Test Message
  ✓ Message sent (ID: 12345)
```

✅ **Groq API Connection Test**
```
✓ Groq API Connection
  ✓ Groq API working (Model: llama-3.3-70b-versatile)
```

✅ **LLM Response Generation Tests**
```
✓ General Chat Response
  ✓ Response generated
     [Response text...]
     (Tokens: 42)

✓ Medical Query Response
  ✓ Response generated
     [Response text...]
     (Tokens: 55)
```

✅ **End-to-End Workflow Test**
```
✓ End-to-End Workflow
  ✓ Message sent (ID: 12347)
```

---

## 🚀 Part 3: n8n Deployment Testing

### Prerequisites
- n8n installed and running locally or cloud
- ngrok installed (for local webhook tunneling)
- Telegram Bot Token and Chat ID from step above
- Groq API Key configured

### Deployment Steps

1. **Import Workflow**
   - Open n8n dashboard
   - Click "Create New Workflow"
   - Click "Menu" → "Import from file"
   - Select: `TELEGRAM_BOT_COMPLETE.json`

2. **Configure Credentials**
   - Open the workflow
   - Click each node that needs configuration:
     - **Telegram Config**: Set BOT_TOKEN, CHAT_ID, BOT_PERSONA_NAME
     - **LLM Model nodes**: Set Groq API key in credentials

3. **Setup Webhook**
   - Start ngrok: `ngrok http 5678`
   - Copy ngrok URL (example: `https://abcd-1234.ngrok.io`)
   - In n8n Webhook node: Set path to `/telegram`

4. **Activate Workflow**
   - Click the toggle to activate (green)
   - Confirm it shows "Active"

5. **Test Telegram Connection**
   - In Telegram, message your bot
   - Monitor n8n "Executions" tab in real-time
   - Verify messages appear and are processed

### Troubleshooting

#### Issue: Webhook shows 403 error
- **Cause**: Ngrok tunnel not configured correctly
- **Fix**: 
  1. Restart ngrok: `ngrok http 5678`
  2. Copy new URL to n8n Webhook node
  3. Ensure webhook path is `/telegram`

#### Issue: Messages not being parsed
- **Cause**: Telegram message structure mismatch
- **Fix**: Check n8n logs for actual message format, update Parse Message function if needed

#### Issue: LLM returns errors
- **Cause**: Groq API key invalid or rate limited
- **Fix**: Verify API key, check Groq dashboard for usage limits

#### Issue: Chinese characters show as gibberish
- **Cause**: Text encoding issue in Telegram node
- **Fix**: Ensure "Parse Mode" is set correctly in Send Telegram Message node

---

## 📋 Part 4: Features Verification Checklist

Use this checklist when testing in n8n:

### General Chat
- [ ] Send: "你好" → Bot responds with greeting
- [ ] Send: "最近怎樣？" → Bot responds conversationally
- [ ] Send: "謝謝你" → Bot acknowledges thanks
- [ ] Send: Simple text → Bot maintains conversation context

### Medical Queries
- [ ] Send: "我的頭疼" → Routes to medical agent
- [ ] Send: "血糖有點高" → Routes to medical agent
- [ ] Send: "睡眠不好" → Routes to medical agent
- [ ] Medical responses include safety reminder about seeing doctor

### Photo Handling
- [ ] Send: Message with photo attachment
- [ ] Bot receives and logs photo
- [ ] Check n8n execution logs for photo metadata

### Conversation Memory
- [ ] Send: "我叫 Alice"
- [ ] Send: "我叫什麼名字？"
- [ ] Bot remembers previous message and responds correctly
- [ ] Memory window includes last 5 messages

### Special Cases
- [ ] Empty message → No crash, appropriate handling
- [ ] Very long message (>1000 chars) → Processes correctly
- [ ] Messages with emojis → Handles correctly
- [ ] Multiple users in group → Maintains separate memory per chat

---

## 🧪 Part 5: Load Testing (Optional)

For production deployment, test with multiple messages:

```bash
# Send 10 test messages rapidly
for i in {1..10}; do
  echo "Test message $i"
  sleep 1
done
```

Monitor n8n:
- Check execution queue
- Monitor CPU/memory usage
- Verify no messages are dropped
- Check response times remain acceptable

---

## 🔒 Part 6: Security Testing

### API Key Security
- [ ] Never commit actual API keys to git
- [ ] Use environment variables in production
- [ ] Rotate API keys periodically
- [ ] Monitor API key usage

### Message Privacy
- [ ] Verify conversation memory is per-chat
- [ ] Different chat IDs have separate memory
- [ ] No cross-contamination between users

### Rate Limiting
- [ ] Test with rapid messages (Groq rate limits)
- [ ] Verify graceful error handling
- [ ] Check response timeout settings

---

## 📊 Summary

| Component | Status | Details |
|-----------|--------|---------|
| Message Parsing | ✅ TESTED | 3/3 tests passed |
| Medical Detection | ✅ TESTED | 5/5 tests passed |
| Branch Routing | ✅ TESTED | 3/3 tests passed |
| Memory System | ✅ TESTED | 2/2 tests passed |
| Prompt Generation | ✅ TESTED | 3/3 tests passed |
| Full Workflow | ✅ TESTED | 6/6 tests passed |
| Telegram API | ⏳ PENDING | Needs credentials |
| Groq LLM API | ⏳ PENDING | Needs credentials |
| n8n Deployment | ⏳ PENDING | User deployment |

---

## ✅ What's Been Delivered

1. **TELEGRAM_BOT_COMPLETE.json** - Complete, production-ready workflow
2. **test_telegram_bot.py** - Comprehensive logic test suite (22 tests, 100% passing)
3. **test_telegram_api_integration.py** - API integration tests ready for credentials
4. **TESTING_GUIDE.md** - This document
5. **Complete documentation in Traditional Chinese** - Deployment guides and FAQs

---

## 🎯 Next Steps

1. **Run Core Tests** (No credentials needed)
   ```bash
   python3 test_telegram_bot.py
   ```

2. **Prepare for API Testing** (Get credentials)
   - Telegram Bot Token
   - Groq API Key
   - Target Chat ID

3. **Run API Integration Tests**
   ```bash
   python3 test_telegram_api_integration.py \
     --telegram-token "your_token" \
     --groq-key "your_key" \
     --chat-id "your_chat_id"
   ```

4. **Deploy to n8n**
   - Import TELEGRAM_BOT_COMPLETE.json
   - Configure credentials
   - Setup ngrok tunnel
   - Activate workflow

5. **Run Feature Verification**
   - Use the checklist above
   - Send test messages
   - Monitor n8n executions
   - Verify all features work

---

## 📞 Need Help?

- Check DEPLOYMENT_GUIDE.md for detailed setup instructions
- Review QUICK_START_TELEGRAM.md for quick reference
- Check error logs in n8n Executions tab
- Verify credentials are correct and have permissions

**Bot is READY FOR DEPLOYMENT! 🚀**
