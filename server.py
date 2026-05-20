import json
import os
import httpx
import logging
import sys
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Configure logging to write to stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("financial-datasets-mcp")

# Initialize FastMCP server
mcp = FastMCP("financial-datasets")

# Constants
FINANCIAL_DATASETS_API_BASE = "https://api.financialdatasets.ai"


# Helper function to make API requests
async def make_request(url: str) -> dict[str, any] | None:
    """Make a request to the Financial Datasets API with proper error handling."""
    # Load environment variables from .env file
    load_dotenv()
    
    headers = {}
    if api_key := os.environ.get("FINANCIAL_DATASETS_API_KEY"):
        headers["X-API-KEY"] = api_key

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"Error": str(e)}


@mcp.tool()
async def get_income_statements(
    ticker: str,
    period: str = "annual",
    limit: int = 4,
) -> str:
    """Get income statements for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        period: Period of the income statement (e.g. annual, quarterly, ttm)
        limit: Number of income statements to return (default: 4)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/financials/income-statements/?ticker={ticker}&period={period}&limit={limit}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch income statements or no income statements found."

    # Extract the income statements
    income_statements = data.get("income_statements", [])

    # Check if income statements are found
    if not income_statements:
        return "Unable to fetch income statements or no income statements found."

    # Stringify the income statements
    return json.dumps(income_statements, indent=2)


@mcp.tool()
async def get_balance_sheets(
    ticker: str,
    period: str = "annual",
    limit: int = 4,
) -> str:
    """Get balance sheets for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        period: Period of the balance sheet (e.g. annual, quarterly, ttm)
        limit: Number of balance sheets to return (default: 4)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/financials/balance-sheets/?ticker={ticker}&period={period}&limit={limit}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch balance sheets or no balance sheets found."

    # Extract the balance sheets
    balance_sheets = data.get("balance_sheets", [])

    # Check if balance sheets are found
    if not balance_sheets:
        return "Unable to fetch balance sheets or no balance sheets found."

    # Stringify the balance sheets
    return json.dumps(balance_sheets, indent=2)


@mcp.tool()
async def get_cash_flow_statements(
    ticker: str,
    period: str = "annual",
    limit: int = 4,
) -> str:
    """Get cash flow statements for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        period: Period of the cash flow statement (e.g. annual, quarterly, ttm)
        limit: Number of cash flow statements to return (default: 4)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/financials/cash-flow-statements/?ticker={ticker}&period={period}&limit={limit}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch cash flow statements or no cash flow statements found."

    # Extract the cash flow statements
    cash_flow_statements = data.get("cash_flow_statements", [])

    # Check if cash flow statements are found
    if not cash_flow_statements:
        return "Unable to fetch cash flow statements or no cash flow statements found."

    # Stringify the cash flow statements
    return json.dumps(cash_flow_statements, indent=2)


@mcp.tool()
async def get_current_stock_price(ticker: str) -> str:
    """Get the current / latest price of a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/prices/snapshot/?ticker={ticker}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch current price or no current price found."

    # Extract the current price
    snapshot = data.get("snapshot", {})

    # Check if current price is found
    if not snapshot:
        return "Unable to fetch current price or no current price found."

    # Stringify the current price
    return json.dumps(snapshot, indent=2)


@mcp.tool()
async def get_historical_stock_prices(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "day",
    interval_multiplier: int = 1,
) -> str:
    """Gets historical stock prices for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        start_date: Start date of the price data (e.g. 2020-01-01)
        end_date: End date of the price data (e.g. 2020-12-31)
        interval: Interval of the price data (e.g. minute, hour, day, week, month)
        interval_multiplier: Multiplier of the interval (e.g. 1, 2, 3)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/prices/?ticker={ticker}&interval={interval}&interval_multiplier={interval_multiplier}&start_date={start_date}&end_date={end_date}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch prices or no prices found."

    # Extract the prices
    prices = data.get("prices", [])

    # Check if prices are found
    if not prices:
        return "Unable to fetch prices or no prices found."

    # Stringify the prices
    return json.dumps(prices, indent=2)


@mcp.tool()
async def get_company_news(ticker: str) -> str:
    """Get news for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/news/?ticker={ticker}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch news or no news found."

    # Extract the news
    news = data.get("news", [])

    # Check if news are found
    if not news:
        return "Unable to fetch news or no news found."
    return json.dumps(news, indent=2)


@mcp.tool()
async def get_available_crypto_tickers() -> str:
    """
    Gets all available crypto tickers.
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/tickers"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch available crypto tickers or no available crypto tickers found."

    # Extract the available crypto tickers
    tickers = data.get("tickers", [])

    # Stringify the available crypto tickers
    return json.dumps(tickers, indent=2)


@mcp.tool()
async def get_crypto_prices(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "day",
    interval_multiplier: int = 1,
) -> str:
    """
    Gets historical prices for a crypto currency.
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/?ticker={ticker}&interval={interval}&interval_multiplier={interval_multiplier}&start_date={start_date}&end_date={end_date}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch prices or no prices found."

    # Extract the prices
    prices = data.get("prices", [])

    # Check if prices are found
    if not prices:
        return "Unable to fetch prices or no prices found."

    # Stringify the prices
    return json.dumps(prices, indent=2)


@mcp.tool()
async def get_historical_crypto_prices(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "day",
    interval_multiplier: int = 1,
) -> str:
    """Gets historical prices for a crypto currency.

    Args:
        ticker: Ticker symbol of the crypto currency (e.g. BTC-USD). The list of available crypto tickers can be retrieved via the get_available_crypto_tickers tool.
        start_date: Start date of the price data (e.g. 2020-01-01)
        end_date: End date of the price data (e.g. 2020-12-31)
        interval: Interval of the price data (e.g. minute, hour, day, week, month)
        interval_multiplier: Multiplier of the interval (e.g. 1, 2, 3)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/?ticker={ticker}&interval={interval}&interval_multiplier={interval_multiplier}&start_date={start_date}&end_date={end_date}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch prices or no prices found."

    # Extract the prices
    prices = data.get("prices", [])

    # Check if prices are found
    if not prices:
        return "Unable to fetch prices or no prices found."

    # Stringify the prices
    return json.dumps(prices, indent=2)


@mcp.tool()
async def get_current_crypto_price(ticker: str) -> str:
    """Get the current / latest price of a crypto currency.

    Args:
        ticker: Ticker symbol of the crypto currency (e.g. BTC-USD). The list of available crypto tickers can be retrieved via the get_available_crypto_tickers tool.
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/snapshot/?ticker={ticker}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch current price or no current price found."

    # Extract the current price
    snapshot = data.get("snapshot", {})

    # Check if current price is found
    if not snapshot:
        return "Unable to fetch current price or no current price found."

    # Stringify the current price
    return json.dumps(snapshot, indent=2)


@mcp.tool()
async def get_sec_filings(
    ticker: str,
    limit: int = 10,
    filing_type: str | None = None,
) -> str:
    """Get all SEC filings for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        limit: Number of SEC filings to return (default: 10)
        filing_type: Type of SEC filing (e.g. 10-K, 10-Q, 8-K)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/filings/?ticker={ticker}&limit={limit}"
    if filing_type:
        url += f"&filing_type={filing_type}"
 
    # Call the API
    data = await make_request(url)

    # Extract the SEC filings
    filings = data.get("filings", [])

    # Check if SEC filings are found
    if not filings:
        return f"Unable to fetch SEC filings or no SEC filings found."

    # Stringify the SEC filings
    return json.dumps(filings, indent=2)

# LINE Family Comment Bot Tools

@mcp.tool()
async def verify_line_config(
    channel_access_token: str,
    channel_secret: str,
    channel_id: str,
) -> str:
    """Verify LINE Messaging API configuration.

    Args:
        channel_access_token: LINE channel access token
        channel_secret: LINE channel secret
        channel_id: LINE channel ID

    Returns:
        Verification result message
    """
    errors = []

    if not channel_access_token or len(channel_access_token) < 10:
        errors.append("Invalid channel_access_token format")

    if not channel_secret or len(channel_secret) < 10:
        errors.append("Invalid channel_secret format")

    if not channel_id or len(channel_id) < 5:
        errors.append("Invalid channel_id format")

    if errors:
        return json.dumps({
            "status": "invalid",
            "errors": errors
        }, indent=2)

    return json.dumps({
        "status": "valid",
        "message": "LINE configuration looks valid. Credentials are properly formatted.",
        "note": "This is basic validation. Test the webhook connection in LINE Developers console."
    }, indent=2)


@mcp.tool()
async def validate_n8n_connection(n8n_base_url: str, n8n_api_key: str = "") -> str:
    """Validate connection to n8n instance.

    Args:
        n8n_base_url: Base URL of n8n instance (e.g. http://localhost:5678)
        n8n_api_key: Optional n8n API key for authenticated access

    Returns:
        Connection validation result
    """
    try:
        if not n8n_base_url:
            return json.dumps({
                "status": "error",
                "message": "n8n_base_url is required"
            }, indent=2)

        # Ensure URL has correct format
        if not n8n_base_url.startswith(("http://", "https://")):
            n8n_base_url = "http://" + n8n_base_url

        if n8n_base_url.endswith("/"):
            n8n_base_url = n8n_base_url[:-1]

        headers = {}
        if n8n_api_key:
            headers["X-N8N-API-KEY"] = n8n_api_key

        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{n8n_base_url}/api/health", headers=headers)

            if response.status_code == 200:
                return json.dumps({
                    "status": "connected",
                    "message": f"Successfully connected to n8n at {n8n_base_url}",
                    "base_url": n8n_base_url
                }, indent=2)
            else:
                return json.dumps({
                    "status": "error",
                    "message": f"n8n returned status code {response.status_code}",
                    "suggestion": "Check if n8n is running and the URL is correct"
                }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e),
            "suggestion": "Check n8n URL and network connectivity"
        }, indent=2)


@mcp.tool()
async def generate_line_bot_config_template() -> str:
    """Generate a template for LINE bot configuration.

    Returns:
        LINE bot configuration template
    """
    template = {
        "line_config": {
            "CHANNEL_ACCESS_TOKEN": "Your LINE channel access token here",
            "CHANNEL_SECRET": "Your LINE channel secret here",
            "CHANNEL_ID": "Your LINE channel ID here",
            "BOT_MENTION_NAME": "Family Bot",
            "BOT_PERSONA_NAME": "SmallChen",
            "ELDER_A_DISPLAY_NAME": "Mom",
            "ELDER_A_ADDRESS": "媽媽",
            "ELDER_B_DISPLAY_NAME": "Dad",
            "ELDER_B_ADDRESS": "爸爸"
        },
        "llm_config": {
            "type": "lm_studio or google_gemini or openai_compatible",
            "lm_studio": {
                "base_url": "http://localhost:1234/v1",
                "api_key": "lm-studio",
                "model": "model-name-from-lm-studio"
            },
            "google_gemini": {
                "api_key": "Your Google Gemini API key",
                "model": "gemini-2.0-flash"
            },
            "openai_compatible": {
                "base_url": "https://api.openrouter.ai/v1",
                "api_key": "Your API key",
                "model": "model-name"
            }
        },
        "n8n_config": {
            "webhook_url": "Will be provided by n8n after workflow setup",
            "context_window_length": 5
        }
    }

    return json.dumps(template, indent=2)


@mcp.tool()
async def get_line_bot_setup_checklist() -> str:
    """Get the LINE bot setup checklist.

    Returns:
        Setup checklist for LINE Family Comment Bot
    """
    checklist = {
        "setup_steps": [
            {
                "step": 1,
                "title": "Prepare n8n",
                "tasks": [
                    "Install n8n locally or use n8n Cloud",
                    "Open n8n in browser"
                ]
            },
            {
                "step": 2,
                "title": "Import Workflow",
                "tasks": [
                    "Create new workflow in n8n",
                    "Import LINE_FAMILY_COMMENT_BOT.public.json",
                    "Do not enable yet, continue setup first"
                ]
            },
            {
                "step": 3,
                "title": "Setup LINE Developers",
                "tasks": [
                    "Go to LINE Developers Console",
                    "Create Messaging API channel",
                    "Copy Channel Access Token",
                    "Copy Channel Secret",
                    "Copy Channel ID"
                ]
            },
            {
                "step": 4,
                "title": "Configure n8n Nodes",
                "tasks": [
                    "Open LINE Config node in n8n",
                    "Fill CHANNEL_ACCESS_TOKEN",
                    "Fill CHANNEL_SECRET",
                    "Fill CHANNEL_ID",
                    "Set BOT_MENTION_NAME (e.g. Family Bot)",
                    "Set BOT_PERSONA_NAME and elder names"
                ]
            },
            {
                "step": 5,
                "title": "Setup LLM",
                "tasks": [
                    "Choose LLM route: LM Studio, Google Gemini, or OpenAI-compatible",
                    "Configure OpenAI-compatible model nodes with credentials",
                    "Test LLM connection"
                ]
            },
            {
                "step": 6,
                "title": "Setup Webhook (Local n8n only)",
                "tasks": [
                    "Install and setup ngrok",
                    "Run ngrok http 5678",
                    "Copy production webhook URL from n8n",
                    "Update LINE Webhook URL in LINE Developers"
                ]
            },
            {
                "step": 7,
                "title": "Test Connection",
                "tasks": [
                    "Enable workflow in n8n",
                    "Click Verify in LINE Developers",
                    "Add bot as LINE friend",
                    "Send test message"
                ]
            },
            {
                "step": 8,
                "title": "Join Family Group",
                "tasks": [
                    "Confirm bot responds correctly",
                    "Add bot to family LINE group",
                    "Monitor responses"
                ]
            }
        ],
        "important_notes": [
            "Never share CHANNEL_ACCESS_TOKEN or CHANNEL_SECRET publicly",
            "Keep family member names private",
            "Test as individual friend first before group",
            "Free Ngrok URLs change on restart - use static domain for stability",
            "Recommended context window: 5-10 messages",
            "Bot should not be too chatty in family groups"
        ]
    }

    return json.dumps(checklist, indent=2)


if __name__ == "__main__":
    # Log server startup
    logger.info("Starting Financial Datasets MCP Server...")

    # Initialize and run the server
    mcp.run(transport="stdio")

    # This line won't be reached during normal operation
    logger.info("Server stopped")
