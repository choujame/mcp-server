# MCP Server Configuration for Claude

## Server Information

**Status:** ✅ Running on Replit

### URLs

- **Main URL:** `https://718a7d59-a331-4e88-8db0-04a6d1ade9be-00-235lr451755zr.sisko.replit.dev`
- **SSE Endpoint (for Claude):** `https://718a7d59-a331-4e88-8db0-04a6d1ade9be-00-235lr451755zr.sisko.replit.dev/sse`

## Available Tools

### Financial Data Tools
- `get_income_statements` - Get income statements for a company
- `get_balance_sheets` - Get balance sheets for a company
- `get_cash_flow_statements` - Get cash flow statements for a company
- `get_current_stock_price` - Get current stock price
- `get_historical_stock_prices` - Get historical stock prices
- `get_company_news` - Get news for a company
- `get_sec_filings` - Get SEC filings for a company
- `get_available_crypto_tickers` - Get available crypto tickers
- `get_crypto_prices` - Get historical crypto prices
- `get_historical_crypto_prices` - Get historical crypto prices
- `get_current_crypto_price` - Get current crypto price

### Telegram Tools (NEW!)
- `send_telegram_message` - Send a custom message via Telegram
  - Parameters: `message` (required), `chat_id` (optional)
  - Example: Send financial alerts or notifications

- `send_financial_alert` - Send a formatted financial alert via Telegram
  - Parameters: `alert_type`, `ticker`, `message`
  - Example: Price changes, earnings announcements, news alerts

- `get_telegram_bot_info` - Get information about the connected Telegram bot
  - Useful for verifying bot connection status

## Telegram Configuration

### Bot Details
- **Bot Username:** @choujamebot
- **Bot Token:** (Configured in Replit Secrets)
- **Chat ID:** 6119894493

### How to Use Telegram Tools

1. **Send a simple message:**
   ```
   "Send a message to my Telegram: Hello from MCP Server!"
   ```
   Tool: `send_telegram_message`
   Message: "Hello from MCP Server!"

2. **Send a financial alert:**
   ```
   "Alert me about Apple stock changes"
   ```
   Tool: `send_financial_alert`
   Alert Type: "price_change"
   Ticker: "AAPL"
   Message: "Stock price has changed"

3. **Check bot status:**
   ```
   "Is my Telegram bot connected?"
   ```
   Tool: `get_telegram_bot_info`

## Connect to Claude Desktop

### Claude Desktop Configuration

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "mcp-server": {
      "url": "https://718a7d59-a331-4e88-8db0-04a6d1ade9be-00-235lr451755zr.sisko.replit.dev/sse"
    }
  }
}
```

### Claude Web Version

1. Go to [claude.ai](https://claude.ai)
2. Open Settings → Connected Applications
3. Add MCP Server:
   - URL: `https://718a7d59-a331-4e88-8db0-04a6d1ade9be-00-235lr451755zr.sisko.replit.dev/sse`
4. Click Connect

## Features

### 1️⃣ Markitdown Support
- Installed: ✅
- Purpose: Convert various file formats to Markdown

### 2️⃣ Telegram Bot Integration
- Status: ✅ Configured
- Chat ID: 6119894493
- Capabilities:
  - Send custom messages
  - Send financial alerts
  - Verify bot connection

### 3️⃣ Telegram Notifications
- Status: ✅ Enabled
- Use cases:
  - Stock price alerts
  - News notifications
  - Financial updates

## Example Usage

### Get Stock Price and Send Alert

```
1. Get Apple's current stock price using: get_current_stock_price(ticker="AAPL")
2. If price meets criteria, send alert: send_financial_alert(
     alert_type="price_threshold",
     ticker="AAPL",
     message="Stock price reached $150"
   )
```

### Get News and Notify via Telegram

```
1. Get company news: get_company_news(ticker="TSLA")
2. Send important news via Telegram: send_telegram_message(
     message="Important Tesla news: [news details]"
   )
```

## Environment Variables

All configured in Replit Secrets:

- `TELEGRAM_BOT_TOKEN` - Bot authentication token
- `TELEGRAM_CHAT_ID` - Recipient Chat ID
- `FINANCIAL_DATASETS_API_KEY` - (Optional) Financial data API key

## Support

- **MCP Server Repository:** https://github.com/choujame/mcp-server
- **Telegram Bot:** @choujamebot
- **Branch:** claude/install-markitdown-CPNdV

---

**Last Updated:** 2026-04-12
**Deployment:** Replit (Free Tier)
**Status:** 🟢 Active and Running
