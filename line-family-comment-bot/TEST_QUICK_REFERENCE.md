# Telegram Bot Testing - Quick Reference

## 🚀 TL;DR - How to Test Everything

### 1. Core Logic Test (5 seconds)
```bash
cd line-family-comment-bot
python3 test_telegram_bot.py
```
**Expected**: 22/22 tests pass ✅

---

### 2. API Integration Test (Without credentials - verify setup)
```bash
python3 test_telegram_api_integration.py
```
**Expected**: Shows "No tests could be run (missing credentials)" ⚠️

---

### 3. API Integration Test (With Real Credentials)

**Get your credentials first:**
1. Telegram Bot Token from @BotFather
2. Groq API Key from https://console.groq.com/keys
3. Your Telegram Chat ID

**Then run:**
```bash
export TELEGRAM_BOT_TOKEN="123456789:ABCDef..."
export GROQ_API_KEY="gsk_..."
export TEST_CHAT_ID="6119894493"

python3 test_telegram_api_integration.py
```

Or one-liner:
```bash
python3 test_telegram_api_integration.py \
  --telegram-token "123456789:ABCDef..." \
  --groq-key "gsk_..." \
  --chat-id "6119894493"
```

**Expected**: All tests pass ✅

---

## 📊 Test Coverage

| Test | Command | Status | Time |
|------|---------|--------|------|
| **Logic** | `python3 test_telegram_bot.py` | ✅ Ready | 2s |
| **API Setup** | `python3 test_telegram_api_integration.py` | ✅ Ready | 2s |
| **API Real** | With credentials above | ⏳ Pending | 10s |
| **n8n Deploy** | Manual in n8n UI | ⏳ Pending | 5m |

---

## ✅ All Test Files

| File | Purpose |
|------|---------|
| `test_telegram_bot.py` | 22 core logic tests |
| `test_telegram_api_integration.py` | API connectivity tests |
| `TESTING_GUIDE.md` | Detailed testing instructions |
| `TEST_QUICK_REFERENCE.md` | This file |

---

## 📝 Test Output Examples

### ✅ Core Test Success Output
```
======================================================================
TOTAL: 22/22 PASSED (100.0%)

✨ ALL TESTS PASSED! Bot logic is ready for deployment. ✨
======================================================================
```

### ✅ API Test With Credentials Success Output
```
📋 Configuration:
  Telegram Bot: ✓ Configured
  Groq API: ✓ Configured
  Test Chat ID: ✓ Configured

1️⃣  Testing Telegram Bot API...
   ✓ Bot found: @your_bot_name (ID: 123456789)
   ✓ Message sent (ID: 12345)

2️⃣  Testing Groq LLM API...
   ✓ Groq API working (Model: llama-3.3-70b-versatile)
   Testing general chat response...
   ✓ Response generated...
   Testing medical response...
   ✓ Response generated...

3️⃣  Testing End-to-End Workflow...
   ✓ Message sent (ID: 12347)

======================================================================
✨ ALL API TESTS PASSED - APIs are ready! ✨
======================================================================
```

---

## 🎯 What Gets Tested

### Core Logic Tests (Completed ✅)
- Message parsing from Telegram webhook
- Medical keyword detection
- Message routing (general/medical/photo)
- Conversation memory management
- LLM prompt generation
- Complete workflow integration

### API Integration Tests (Needs credentials ⏳)
- Telegram Bot API connectivity
- Send message to Telegram
- Groq LLM API connectivity
- Generate responses with LLM
- End-to-end workflow with real APIs

### n8n Deployment Tests (Manual ⏳)
- Workflow import
- Credential configuration
- Webhook setup
- Message sending and receiving
- Feature verification

---

## 🔍 Checking Test Results

### If tests PASS ✅
→ Your bot is ready for n8n deployment

### If tests FAIL ❌
→ Check error messages and troubleshoot

Common issues:
- **API key invalid**: Check credentials format
- **API timeout**: Check internet connection
- **Webhook issues**: Ensure ngrok is running
- **Encoding errors**: Check UTF-8 settings

---

## 📦 Files Included

```
line-family-comment-bot/
├── test_telegram_bot.py              ← Core logic tests
├── test_telegram_api_integration.py  ← API integration tests
├── TESTING_GUIDE.md                  ← Full testing guide
├── TEST_QUICK_REFERENCE.md           ← This file
├── TELEGRAM_BOT_COMPLETE.json        ← Production workflow
└── DEPLOYMENT_GUIDE.md               ← n8n setup guide
```

---

## ⚡ Quick Commands Summary

```bash
# Run core tests
python3 test_telegram_bot.py

# Test API integration (no credentials)
python3 test_telegram_api_integration.py

# Test with real API credentials
export TELEGRAM_BOT_TOKEN="your_token"
export GROQ_API_KEY="your_key"
export TEST_CHAT_ID="your_chat_id"
python3 test_telegram_api_integration.py

# All in one line
python3 test_telegram_api_integration.py \
  --telegram-token "your_token" \
  --groq-key "your_key" \
  --chat-id "your_chat_id"
```

---

## 🎊 Success Criteria

| Milestone | Status |
|-----------|--------|
| Core logic tests pass | ✅ DONE |
| API tests can run | ✅ READY |
| All features verified | ⏳ PENDING |
| Deployed to n8n | ⏳ PENDING |
| Production ready | ⏳ PENDING |

**Current Status**: Core logic fully tested and verified. Ready for API and n8n testing.

---

## 🚀 Ready to Deploy?

1. ✅ Core tests passed
2. ⏳ Run API tests with credentials
3. ⏳ Deploy to n8n
4. ⏳ Send test messages in Telegram
5. ✅ Live!

**Start with**: `python3 test_telegram_bot.py`
