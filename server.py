import asyncio
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
FIRECRAWL_API_BASE = "https://api.firecrawl.dev/v1"
APIFY_API_BASE = "https://api.apify.com/v2"


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
async def firecrawl_scrape(url: str, formats: list[str] | None = None) -> str:
    """Scrape a single webpage using Firecrawl and return clean content (markdown by default).

    Args:
        url: The URL to scrape
        formats: Output formats to request, e.g. ["markdown"], ["html"], ["links"] (default: ["markdown"])
    """
    load_dotenv()
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        return "Error: FIRECRAWL_API_KEY not set in environment"

    if formats is None:
        formats = ["markdown"]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {"url": url, "formats": formats}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{FIRECRAWL_API_BASE}/scrape",
                json=payload,
                headers=headers,
                timeout=60.0,
            )
            response.raise_for_status()
            data = response.json()
            if not data.get("success"):
                return f"Firecrawl error: {json.dumps(data)}"
            page = data.get("data", {})
            meta = page.get("metadata", {})
            result = {
                "url": url,
                "title": meta.get("title", ""),
                "description": meta.get("description", ""),
            }
            for fmt in formats:
                if fmt in page:
                    result[fmt] = page[fmt]
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error scraping {url}: {str(e)}"


@mcp.tool()
async def firecrawl_crawl(url: str, limit: int = 10) -> str:
    """Crawl an entire website using Firecrawl and return clean markdown from multiple pages.

    Args:
        url: The root URL to start crawling from
        limit: Maximum number of pages to crawl (default: 10)
    """
    load_dotenv()
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        return "Error: FIRECRAWL_API_KEY not set in environment"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {"url": url, "limit": limit, "scrapeOptions": {"formats": ["markdown"]}}

    async with httpx.AsyncClient() as client:
        try:
            start_resp = await client.post(
                f"{FIRECRAWL_API_BASE}/crawl",
                json=payload,
                headers=headers,
                timeout=30.0,
            )
            start_resp.raise_for_status()
            start_data = start_resp.json()
            if not start_data.get("success"):
                return f"Firecrawl crawl error: {json.dumps(start_data)}"

            job_id = start_data.get("id")
            for _ in range(60):
                await asyncio.sleep(2)
                poll_resp = await client.get(
                    f"{FIRECRAWL_API_BASE}/crawl/{job_id}",
                    headers=headers,
                    timeout=30.0,
                )
                poll_resp.raise_for_status()
                poll_data = poll_resp.json()
                status = poll_data.get("status")
                if status == "completed":
                    pages = poll_data.get("data", [])
                    results = [
                        {
                            "url": p.get("metadata", {}).get("sourceURL", ""),
                            "title": p.get("metadata", {}).get("title", ""),
                            "markdown": p.get("markdown", ""),
                        }
                        for p in pages
                    ]
                    return json.dumps(results, indent=2)
                elif status == "failed":
                    return f"Crawl job failed: {json.dumps(poll_data)}"

            return f"Crawl job timed out after 120s (job_id={job_id})"
        except Exception as e:
            return f"Error crawling {url}: {str(e)}"


@mcp.tool()
async def apify_scrape(url: str, max_pages: int = 3) -> str:
    """Scrape a webpage (or small site) using Apify's Website Content Crawler actor.
    Returns clean text and markdown extracted by a professional crawler.

    Args:
        url: The URL to scrape
        max_pages: Maximum number of pages to crawl from that URL (default: 3)
    """
    load_dotenv()
    api_token = os.environ.get("APIFY_API_TOKEN")
    if not api_token:
        return "Error: APIFY_API_TOKEN not set in environment"

    auth_param = f"token={api_token}"
    payload = {
        "startUrls": [{"url": url}],
        "maxCrawlPages": max_pages,
        "crawlerType": "cheerio",
    }

    async with httpx.AsyncClient() as client:
        try:
            run_resp = await client.post(
                f"{APIFY_API_BASE}/acts/apify~website-content-crawler/runs?{auth_param}",
                json=payload,
                timeout=30.0,
            )
            run_resp.raise_for_status()
            run_data = run_resp.json().get("data", {})
            run_id = run_data.get("id")
            dataset_id = run_data.get("defaultDatasetId")

            for _ in range(60):
                await asyncio.sleep(3)
                status_resp = await client.get(
                    f"{APIFY_API_BASE}/actor-runs/{run_id}?{auth_param}",
                    timeout=30.0,
                )
                status_resp.raise_for_status()
                run_status = status_resp.json().get("data", {}).get("status")
                if run_status == "SUCCEEDED":
                    items_resp = await client.get(
                        f"{APIFY_API_BASE}/datasets/{dataset_id}/items?{auth_param}&fields=url,title,text,markdown",
                        timeout=30.0,
                    )
                    items_resp.raise_for_status()
                    return json.dumps(items_resp.json(), indent=2)
                elif run_status in ("FAILED", "ABORTED", "TIMED-OUT"):
                    return f"Apify run {run_status} (run_id={run_id})"

            return f"Apify run timed out after 180s (run_id={run_id})"
        except Exception as e:
            return f"Error scraping {url} with Apify: {str(e)}"


@mcp.tool()
async def browser_scrape(url: str) -> str:
    """Scrape a webpage with a real headless browser (Playwright/Chromium).
    Use this as a last-resort fallback when firecrawl_scrape and apify_scrape fail
    or the page requires JavaScript rendering that they can't handle.
    Requires the optional 'browser' extra: pip install "mcp-server[browser]" && python -m playwright install chromium

    Args:
        url: The URL to scrape
    """
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        return (
            "Error: Playwright is not installed. Install the optional browser extra with:\n"
            '  pip install "mcp-server[browser]"\n'
            "  python -m playwright install chromium"
        )

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            try:
                page = await browser.new_page()
                await page.goto(url, wait_until="networkidle", timeout=60000)
                title = await page.title()
                text = await page.inner_text("body")
                result = {"url": url, "title": title, "text": text}
                return json.dumps(result, indent=2)
            finally:
                await browser.close()
    except Exception as e:
        return f"Error scraping {url} with browser: {str(e)}"


if __name__ == "__main__":
    load_dotenv()
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    port = int(os.environ.get("PORT", 8000))

    logger.info("Starting MCP Server (transport=%s)...", transport)

    if transport == "sse":
        mcp.run(transport="sse", host="0.0.0.0", port=port)
    else:
        mcp.run(transport="stdio")
