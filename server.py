import json
import os
import httpx
import logging
import sys
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from scrapling.fetchers import AsyncFetcher

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

@mcp.tool()
async def scrape_url(
    url: str,
    css_selector: str | None = None,
) -> str:
    """Scrape content from a webpage using Scrapling.

    Args:
        url: The URL to scrape
        css_selector: Optional CSS selector to extract specific elements (e.g. 'h1', '.price', '#content')
    """
    try:
        fetcher = AsyncFetcher(auto_match=False)
        page = await fetcher.get(url, stealthy_headers=True)
        if css_selector:
            elements = page.css(css_selector)
            if not elements:
                return f"No elements found for selector '{css_selector}'"
            return json.dumps([el.text for el in elements], indent=2)
        return page.get_all_text(separator="\n", strip=True)
    except Exception as e:
        return f"Error scraping {url}: {e}"


@mcp.tool()
async def scrape_table(
    url: str,
    table_selector: str = "table",
) -> str:
    """Scrape a table from a webpage and return it as JSON.

    Args:
        url: The URL containing the table
        table_selector: CSS selector for the table (default: 'table')
    """
    try:
        fetcher = AsyncFetcher(auto_match=False)
        page = await fetcher.get(url, stealthy_headers=True)
        tables = page.css(table_selector)
        if not tables:
            return "No tables found on the page."
        results = []
        for table in tables:
            headers = [th.text.strip() for th in table.css("th")]
            rows = []
            for tr in table.css("tr"):
                cells = [td.text.strip() for td in tr.css("td")]
                if cells:
                    if headers:
                        rows.append(dict(zip(headers, cells)))
                    else:
                        rows.append(cells)
            if rows:
                results.append(rows)
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error scraping table from {url}: {e}"


@mcp.tool()
async def scrape_stock_summary(ticker: str) -> str:
    """Scrape key fundamental metrics for a stock (P/E, EPS, market cap, etc.) from Finviz.

    Args:
        ticker: Stock ticker symbol (e.g. AAPL, GOOGL)
    """
    url = f"https://finviz.com/quote.ashx?t={ticker.upper()}"
    try:
        fetcher = AsyncFetcher(auto_match=False)
        page = await fetcher.get(url, stealthy_headers=True)
        cells = page.css("table.snapshot-table2 td")
        if not cells:
            return f"No fundamental data found for {ticker}."
        keys = [c.text.strip() for i, c in enumerate(cells) if i % 2 == 0]
        values = [c.text.strip() for i, c in enumerate(cells) if i % 2 == 1]
        return json.dumps(dict(zip(keys, values)), indent=2)
    except Exception as e:
        return f"Error scraping stock summary for {ticker}: {e}"


@mcp.tool()
async def scrape_earnings_calendar(date: str | None = None) -> str:
    """Scrape upcoming earnings announcements.

    Args:
        date: Date in YYYY-MM-DD format (default: today)
    """
    from datetime import date as dt
    target = date or dt.today().strftime("%Y-%m-%d")
    url = f"https://stockanalysis.com/calendar/earnings/?date={target}"
    try:
        fetcher = AsyncFetcher(auto_match=False)
        page = await fetcher.get(url, stealthy_headers=True)
        headers = [th.text.strip() for th in page.css("table thead th")]
        rows = page.css("table tbody tr")
        if not rows:
            return f"No earnings data found for {target}."
        results = []
        for row in rows:
            cells = [td.text.strip() for td in row.css("td")]
            if cells:
                results.append(dict(zip(headers, cells)) if headers else cells)
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error scraping earnings calendar: {e}"


@mcp.tool()
async def scrape_insider_trades(ticker: str) -> str:
    """Scrape recent insider trading transactions for a stock from OpenInsider.

    Args:
        ticker: Stock ticker symbol (e.g. AAPL, GOOGL)
    """
    url = f"http://openinsider.com/search?q={ticker.upper()}"
    try:
        fetcher = AsyncFetcher(auto_match=False)
        page = await fetcher.get(url, stealthy_headers=True)
        headers = [th.text.strip() for th in page.css("table.tinytable thead th")]
        rows = page.css("table.tinytable tbody tr")
        if not rows:
            return f"No insider trading data found for {ticker}."
        results = []
        for row in rows:
            cells = [td.text.strip() for td in row.css("td")]
            if cells:
                results.append(dict(zip(headers, cells)) if headers else cells)
        return json.dumps(results[:20], indent=2)
    except Exception as e:
        return f"Error scraping insider trades for {ticker}: {e}"


@mcp.tool()
async def scrape_analyst_ratings(ticker: str) -> str:
    """Scrape analyst price targets and buy/sell ratings for a stock.

    Args:
        ticker: Stock ticker symbol (e.g. AAPL, GOOGL)
    """
    url = f"https://stockanalysis.com/stocks/{ticker.lower()}/forecast/"
    try:
        fetcher = AsyncFetcher(auto_match=False)
        page = await fetcher.get(url, stealthy_headers=True)
        headers = [th.text.strip() for th in page.css("table thead th")]
        rows = page.css("table tbody tr")
        if not rows:
            return f"No analyst ratings found for {ticker}."
        results = []
        for row in rows:
            cells = [td.text.strip() for td in row.css("td")]
            if cells:
                results.append(dict(zip(headers, cells)) if headers else cells)
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"Error scraping analyst ratings for {ticker}: {e}"


if __name__ == "__main__":
    # Log server startup
    logger.info("Starting Financial Datasets MCP Server...")

    # Initialize and run the server
    mcp.run(transport="stdio")

    # This line won't be reached during normal operation
    logger.info("Server stopped")
