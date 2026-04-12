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
- `convert_document_to_markdown` - Convert documents to markdown (NEW - Markitdown integration)
- `get_sec_filing_as_markdown` - Convert SEC filings to markdown (NEW - Markitdown integration)
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

### Stock Screener Tools (NEW - Telegram Interactive!)
- `scan_ma_pullback_stocks` - Scan stocks for MA pullback patterns
  - Parameters: `market` ("tw" for Taiwan/美股 or "us" for US), `days` (default: 5)
  - Returns: List of stocks with MA pullback opportunities
  - Example: Find stocks with moving average pullback patterns

- `get_ma_pullback_telegram` - Scan MA pullback stocks and send to Telegram
  - Parameters: `market` ("tw" or "us"), `days` (default: 5)
  - Automatically sends formatted results to Telegram
  - Includes: current price, MA values, support/resistance, trend

### Document Conversion Tools (Markitdown Integration)
- `convert_document_to_markdown` - Convert any document to markdown format
  - Parameters: `file_path` (local path or URL)
  - Supported formats: HTML, PDF, DOCX, PPTX, and more
  - Returns: Markdown-formatted content
  - Example: Convert SEC filings, financial reports, news articles

- `get_sec_filing_as_markdown` - Convert SEC filing documents to markdown
  - Parameters: `ticker`, `filing_url`, `limit` (max characters, default: 5000)
  - Fetches HTML from SEC Edgar and converts to markdown
  - Example: Convert 10-K, 10-Q, 8-K documents for analysis
  - Returns: Markdown content with character limit applied

## Telegram Configuration

### Bot Details
- **Bot Username:** @choujamebot
- **Bot Token:** (Configured in Replit Secrets)
- **Chat ID:** 6119894493

### How to Use Telegram Tools (via Claude)

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

## Telegram Bot Interactive Commands

### Direct Telegram Commands
Send these commands directly in Telegram to @choujamebot (no Claude needed):

**Taiwan Stocks (台股):**
```
/tw_ma     - Scan Taiwan stocks for MA pullback opportunities
```

**US Stocks (美股):**
```
/us_ma     - Scan US stocks for MA pullback opportunities
```

**Help & Information:**
```
/start     - Welcome message and available commands
/help      - Detailed help about MA pullback screening
```

### Telegram Bot Response Format

When you send `/tw_ma` or `/us_ma`, the bot returns:

```
📊 台股 MA 回撤五日掃描結果
⏰ 2026-04-12 11:30:45
掃描: 15 只股票 | 找到: 5 只 ✅

🔹 2330.TW
   現價: $145.50
   MA5: $143.20 | MA10: $142.80
   支撐: $140.00 | 壓力: $150.00
   趨勢: BULLISH

🔹 2454.TW
   ...more stocks
```

### What is MA Pullback?

**MA Pullback (移動平均線回撤)** is a technical pattern where:
1. Stock price temporarily dips below the moving average (MA)
2. But then recovers and trades back above MA
3. This typically signals a buying opportunity
4. Common trend-following strategy for traders

**Example Use Cases:**
- Find stocks in uptrend that are consolidating
- Identify potential entry points during pullbacks
- Scan multiple markets simultaneously
- Receive alerts directly on Telegram

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

### 1️⃣ Markitdown Support (NEW!)
- Installed: ✅ In pyproject.toml dependencies
- Purpose: Convert various file formats to Markdown
- Tools:
  - `convert_document_to_markdown` - Convert HTML, PDF, DOCX, PPTX to markdown
  - `get_sec_filing_as_markdown` - Convert SEC filing documents to markdown
- Use Cases:
  - Convert SEC filings for analysis
  - Convert financial reports to markdown
  - Convert news articles and web pages
  - Extract text from PDF documents

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

### 4️⃣ Interactive Telegram Bot (NEW!)
- Status: ✅ Running
- Fully automated stock screening
- Commands:
  - `/tw_ma` - Taiwan stocks MA screening
  - `/us_ma` - US stocks MA screening
  - `/help` - Help and information
- Coverage:
  - 15 Taiwan stocks (台股)
  - 15 US stocks (美股)
- Real-time analysis with:
  - Current price
  - Moving averages (5, 10, 20 day)
  - Support and resistance levels
  - Trend direction (BULLISH/BEARISH)
- Completely free - no API costs!

## Example Usage

### 1. Get Stock Price and Send Alert (via Claude)

```
1. Get Apple's current stock price using: get_current_stock_price(ticker="AAPL")
2. If price meets criteria, send alert: send_financial_alert(
     alert_type="price_threshold",
     ticker="AAPL",
     message="Stock price reached $150"
   )
```

### 2. Get News and Notify via Telegram (via Claude)

```
1. Get company news: get_company_news(ticker="TSLA")
2. Send important news via Telegram: send_telegram_message(
     message="Important Tesla news: [news details]"
   )
```

### 3. Interactive Stock Screening via Telegram (NEW!)

**In Telegram, send to @choujamebot:**
```
User:  /tw_ma
Bot:   📊 正在掃描台股 MA 回撤機會，請稍候...
       📊 台股 MA 回撤五日掃描結果
       ⏰ 2026-04-12 11:30:45
       掃描: 15 只股票 | 找到: 5 只 ✅
       
       🔹 2330.TW (台積電)
          現價: $145.50
          MA5: $143.20 | MA10: $142.80
          支撐: $140.00 | 壓力: $150.00
          趨勢: BULLISH ✅
       
       🔹 2454.TW (聯發科)
          ...more results
```

### 4. Scan US Stocks via Telegram

**In Telegram, send to @choujamebot:**
```
User:  /us_ma
Bot:   📊 正在掃描美股 MA 回撤機會，請稍候...
       📊 美股 MA 回撤五日掃描結果
       
       🔹 AAPL (Apple)
          現價: $185.50
          MA5: $183.20 | MA10: $182.50
          支撐: $180.00 | 壓力: $190.00
          趨勢: BULLISH ✅
       
       ...more results
```

### 5. Natural Language in Telegram

You can also use natural language:
```
User:  "掃描台股移動平均線回撤"
or:    "美股有什麼 MA 機會"
or:    "找台股買點信號"

Bot:   📊 Analysis results...
```

### 6. Convert Documents to Markdown (via Claude)

**Example 1: Convert SEC filing to markdown**
```
Claude: "Convert the Apple 10-K filing from this URL to markdown"

Tool: get_sec_filing_as_markdown(
  ticker="AAPL",
  filing_url="https://www.sec.gov/Archives/edgar/...",
  limit=5000
)

Result: Markdown-formatted SEC filing content
```

**Example 2: Convert HTML document to markdown**
```
Claude: "Convert this financial news article to markdown"

Tool: convert_document_to_markdown(
  file_path="https://example.com/financial-report.html"
)

Result: Clean markdown text extracted from HTML
```

**Supported Formats:**
- HTML files and web pages
- PDF documents
- Microsoft Word (DOCX)
- PowerPoint presentations (PPTX)
- And more!

## Environment Variables

All configured in Replit Secrets:

- `TELEGRAM_BOT_TOKEN` - Bot authentication token
- `TELEGRAM_CHAT_ID` - Recipient Chat ID
- `FINANCIAL_DATASETS_API_KEY` - (Optional) Financial data API key

## How It Works

### Architecture

```
User (iPhone/Desktop)
  ↓
Telegram App → @choujamebot
  ↓
Telegram Bot Handler (Running on Replit)
  ↓
Stock Analyzer (Technical Analysis Engine)
  ↓
yfinance API (Data Source)
  ↓
Results → Back to Telegram
```

### Supported Markets

**Taiwan Stocks (台股):**
- 2330.TW - TSMC
- 2317.TW - Acer
- 2454.TW - MediaTek
- 3008.TW - Largan Precision
- + 11 more stocks

**US Stocks (美股):**
- AAPL - Apple
- MSFT - Microsoft
- GOOGL - Google
- AMZN - Amazon
- + 11 more stocks

### Technical Indicators

- **MA5** - 5-day moving average (short-term trend)
- **MA10** - 10-day moving average (medium-term trend)
- **MA20** - 20-day moving average (long-term trend)
- **Support** - Recent low price (buy zone)
- **Resistance** - Recent high price (sell zone)
- **Trend** - BULLISH (price > MA20) or BEARISH (price < MA20)

## Pricing

**Everything is FREE! 🎉**

- ✅ Markitdown - Free
- ✅ Telegram Bot - Free (using python-telegram-bot)
- ✅ Stock Data - Free (using yfinance)
- ✅ Technical Analysis - Free (using pandas-ta)
- ✅ Hosting - Free (Replit Free Tier)

**No hidden costs, no API fees!**

## Support

- **MCP Server Repository:** https://github.com/choujame/mcp-server
- **Telegram Bot:** @choujamebot
- **Branch:** claude/install-markitdown-CPNdV
- **Startup Command:** `uv run main.py`

---

**Last Updated:** 2026-04-12
**Deployment:** Replit (Free Tier)
**Status:** 🟢 Active and Running
**Features:** MCP Server + Telegram Bot + Stock Screener
