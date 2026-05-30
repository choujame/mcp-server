import json
import os
import httpx
import logging
import sys
import subprocess
import shutil
import asyncio
from pathlib import Path
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

# ── AgEnD: Multi-agent fleet tools ──────────────────────────────────────────
# Mirrors the peer-to-peer MCP tools from github.com/suzuke/AgEnD.
# Agents discover, message, and manage each other through tmux sessions.

AGEND_PREFIX = "agend-"  # tmux session name prefix


def _tmux_available() -> bool:
    return shutil.which("tmux") is not None


def _run(cmd: list[str]) -> tuple[int, str, str]:
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


@mcp.tool()
async def agend_list_agents() -> str:
    """List all running AgEnD agent tmux sessions.

    Returns a JSON array of agent info objects with name, pid, and created fields.
    """
    if not _tmux_available():
        return json.dumps({"error": "tmux is not installed"})

    rc, out, err = _run(["tmux", "list-sessions", "-F",
                         "#{session_name}\t#{session_id}\t#{session_created}"])
    if rc != 0:
        if "no server running" in err:
            return json.dumps([])
        return json.dumps({"error": err})

    agents = []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) == 3 and parts[0].startswith(AGEND_PREFIX):
            agents.append({
                "name": parts[0][len(AGEND_PREFIX):],
                "session": parts[0],
                "id": parts[1],
                "created": parts[2],
            })
    return json.dumps(agents, indent=2)


@mcp.tool()
async def agend_start_agent(
    name: str,
    project_path: str,
    cli: str = "claude",
) -> str:
    """Start a new agent in an isolated tmux session.

    Args:
        name: Unique agent name (e.g. "backend", "frontend")
        project_path: Absolute path to the project directory
        cli: CLI backend to use — claude | gemini | codex | opencode (default: claude)
    """
    if not _tmux_available():
        return json.dumps({"error": "tmux is not installed"})

    session = f"{AGEND_PREFIX}{name}"
    rc, _, _ = _run(["tmux", "has-session", "-t", session])
    if rc == 0:
        return json.dumps({"error": f"Agent '{name}' is already running"})

    path = Path(project_path).expanduser().resolve()
    if not path.is_dir():
        return json.dumps({"error": f"Directory not found: {project_path}"})

    cli_map = {
        "claude": "claude",
        "gemini": "gemini",
        "codex": "codex",
        "opencode": "opencode",
    }
    cmd = cli_map.get(cli, cli)

    rc, _, err = _run([
        "tmux", "new-session", "-d",
        "-s", session,
        "-c", str(path),
        cmd,
    ])
    if rc != 0:
        return json.dumps({"error": err})
    return json.dumps({"status": "started", "agent": name, "session": session, "cli": cmd})


@mcp.tool()
async def agend_send_message(name: str, message: str) -> str:
    """Send a message / prompt to a running agent's tmux session.

    Args:
        name: Agent name (as given to agend_start_agent)
        message: Text to send (simulates keyboard input)
    """
    if not _tmux_available():
        return json.dumps({"error": "tmux is not installed"})

    session = f"{AGEND_PREFIX}{name}"
    rc, _, _ = _run(["tmux", "has-session", "-t", session])
    if rc != 0:
        return json.dumps({"error": f"Agent '{name}' is not running"})

    escaped = message.replace("'", "'\\''")
    rc, _, err = _run(["tmux", "send-keys", "-t", session, message, "Enter"])
    if rc != 0:
        return json.dumps({"error": err})
    return json.dumps({"status": "sent", "agent": name})


@mcp.tool()
async def agend_get_output(name: str, lines: int = 50) -> str:
    """Capture recent terminal output from an agent's tmux session.

    Args:
        name: Agent name
        lines: Number of lines to capture (default: 50)
    """
    if not _tmux_available():
        return json.dumps({"error": "tmux is not installed"})

    session = f"{AGEND_PREFIX}{name}"
    rc, _, _ = _run(["tmux", "has-session", "-t", session])
    if rc != 0:
        return json.dumps({"error": f"Agent '{name}' is not running"})

    rc, out, err = _run(["tmux", "capture-pane", "-p", "-t", session,
                          "-S", f"-{lines}"])
    if rc != 0:
        return json.dumps({"error": err})
    return json.dumps({"agent": name, "output": out})


@mcp.tool()
async def agend_stop_agent(name: str) -> str:
    """Stop a running agent's tmux session.

    Args:
        name: Agent name to stop
    """
    if not _tmux_available():
        return json.dumps({"error": "tmux is not installed"})

    session = f"{AGEND_PREFIX}{name}"
    rc, _, _ = _run(["tmux", "has-session", "-t", session])
    if rc != 0:
        return json.dumps({"error": f"Agent '{name}' is not running"})

    rc, _, err = _run(["tmux", "kill-session", "-t", session])
    if rc != 0:
        return json.dumps({"error": err})
    return json.dumps({"status": "stopped", "agent": name})


@mcp.tool()
async def agend_broadcast(message: str) -> str:
    """Broadcast a message to all running AgEnD agent sessions.

    Args:
        message: Text to send to every agent
    """
    if not _tmux_available():
        return json.dumps({"error": "tmux is not installed"})

    agents_json = await agend_list_agents()
    agents = json.loads(agents_json)
    if isinstance(agents, dict) and "error" in agents:
        return agents_json
    if not agents:
        return json.dumps({"status": "no agents running"})

    results = []
    for agent in agents:
        rc, _, err = _run(["tmux", "send-keys", "-t", agent["session"], message, "Enter"])
        results.append({"agent": agent["name"], "ok": rc == 0, "error": err if rc != 0 else None})
    return json.dumps(results, indent=2)


if __name__ == "__main__":
    # Log server startup
    logger.info("Starting Financial Datasets MCP Server...")

    # Initialize and run the server
    mcp.run(transport="stdio")

    # This line won't be reached during normal operation
    logger.info("Server stopped")
