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

ARTICLE_TOOLS_BASE = "https://eternityspring.github.io/article-tools"


@mcp.tool()
def get_article_tool_url(tool: str) -> str:
    """Get the URL for an article formatting tool.

    Args:
        tool: The tool name. One of: 'cover', 'md-to-wechat', 'md-to-x', 'qrcode', 'index'.
    """
    valid_tools = {"cover", "md-to-wechat", "md-to-x", "qrcode", "index"}
    if tool not in valid_tools:
        return f"Unknown tool '{tool}'. Valid options: {', '.join(sorted(valid_tools))}"
    if tool == "index":
        return ARTICLE_TOOLS_BASE + "/"
    return f"{ARTICLE_TOOLS_BASE}/{tool}.html"


@mcp.tool()
def format_markdown_for_wechat(content: str) -> str:
    """Convert markdown to WeChat public account compatible HTML.

    Supports headers, bold/italic, inline code, links, unordered/ordered lists,
    blockquotes, fenced code blocks, horizontal rules, and tables.

    Args:
        content: Markdown text to convert.
    """
    import re

    lines = content.split("\n")
    output = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # Fenced code block
        if re.match(r"^```", line):
            lang = line[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not re.match(r"^```", lines[i]):
                code_lines.append(lines[i])
                i += 1
            code = "\n".join(code_lines)
            output.append(
                f'<pre style="background:#f4f4f4;padding:12px;border-radius:4px;'
                f'overflow-x:auto;font-size:14px;line-height:1.6;">'
                f'<code>{code}</code></pre>'
            )
            i += 1
            continue

        # Table (detect by | separator)
        if "|" in line and re.match(r"^\|", line.strip()):
            table_lines = []
            while i < len(lines) and "|" in lines[i]:
                table_lines.append(lines[i])
                i += 1
            # Remove separator row (---|---)
            rows = [r for r in table_lines if not re.match(r"^[\s|:-]+$", r)]
            html = '<table style="border-collapse:collapse;width:100%;margin:12px 0;">'
            for row_idx, row in enumerate(rows):
                cells = [c.strip() for c in row.strip().strip("|").split("|")]
                tag = "th" if row_idx == 0 else "td"
                style = (
                    'style="border:1px solid #ddd;padding:6px 10px;'
                    + ("background:#f0f0f0;font-weight:bold;" if row_idx == 0 else "")
                    + '"'
                )
                html += "<tr>" + "".join(f"<{tag} {style}>{_inline_md(c)}</{tag}>" for c in cells) + "</tr>"
            html += "</table>"
            output.append(html)
            continue

        # Horizontal rule
        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", line.strip()):
            output.append('<hr style="border:none;border-top:1px solid #ddd;margin:16px 0;">')
            i += 1
            continue

        # Blockquote
        if line.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].startswith(">"):
                quote_lines.append(lines[i].lstrip("> "))
                i += 1
            inner = " ".join(quote_lines)
            output.append(
                f'<blockquote style="border-left:4px solid #07c160;margin:8px 0;'
                f'padding:8px 16px;background:#f9f9f9;color:#555;">'
                f'{_inline_md(inner)}</blockquote>'
            )
            continue

        # Headers
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            size = {1: "24px", 2: "20px", 3: "18px", 4: "16px", 5: "15px", 6: "14px"}[level]
            color = "#07c160" if level <= 2 else "#333"
            output.append(
                f'<p style="font-size:{size};font-weight:bold;color:{color};'
                f'margin:16px 0 8px;border-bottom:{"2px solid #07c160" if level == 1 else "none"};'
                f'padding-bottom:{"6px" if level == 1 else "0"};">{text}</p>'
            )
            i += 1
            continue

        # Blank line
        if line.strip() == "":
            i += 1
            continue

        # Unordered list
        m = re.match(r"^[-*+]\s+(.*)", line)
        if m:
            output.append(f'<p style="margin:4px 0;padding-left:16px;">• {_inline_md(m.group(1))}</p>')
            i += 1
            continue

        # Ordered list
        m = re.match(r"^(\d+)\.\s+(.*)", line)
        if m:
            output.append(
                f'<p style="margin:4px 0;padding-left:16px;">'
                f'{m.group(1)}. {_inline_md(m.group(2))}</p>'
            )
            i += 1
            continue

        # Regular paragraph
        output.append(f'<p style="margin:8px 0;line-height:1.75;font-size:16px;">{_inline_md(line)}</p>')
        i += 1

    return "\n".join(output)


def _inline_md(text: str) -> str:
    """Convert inline markdown to HTML."""
    import re
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"_(.+?)_", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r'<code style="background:#f4f4f4;padding:2px 6px;border-radius:3px;font-size:14px;">\1</code>', text)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2" style="color:#07c160;">\1</a>', text)
    return text


@mcp.tool()
def format_markdown_for_x(
    content: str,
    max_chars: int = 270,
    suggest_hashtags: bool = True,
) -> str:
    """Split and format content into an X (Twitter) thread, with hashtag suggestions.

    Each post is kept under max_chars. The last post includes suggested hashtags
    extracted from the content's keywords.

    Args:
        content: The text or markdown content to format.
        max_chars: Maximum characters per post (default 270, leaving room for numbering).
        suggest_hashtags: Append suggested hashtags to the last post (default True).
    """
    import re

    # Strip markdown to plain text
    text = re.sub(r"#{1,6}\s+", "", content)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"__(.+?)__", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"_(.+?)_", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    # Extract hashtag candidates from existing #tags and capitalised words
    raw_tags = re.findall(r"#(\w+)", content)
    cap_words = re.findall(r"\b([A-Z][a-zA-Z]{3,})\b", content)
    candidates = list(dict.fromkeys(raw_tags + cap_words))[:5]
    hashtags = " ".join(f"#{t}" for t in candidates)

    # Split into sentences
    sentences = re.split(r"(?<=[。！？.!?])\s*", text)
    sentences = [s.strip() for s in sentences if s.strip()]

    posts, current = [], ""
    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= max_chars:
            current = (current + " " + sentence).strip()
        else:
            if current:
                posts.append(current)
            if len(sentence) > max_chars:
                for j in range(0, len(sentence), max_chars):
                    posts.append(sentence[j:j + max_chars])
                current = ""
            else:
                current = sentence
    if current:
        posts.append(current)

    # Append hashtags to last post if they fit
    if suggest_hashtags and hashtags and posts:
        last = posts[-1]
        candidate_last = last + "\n" + hashtags
        if len(candidate_last) <= max_chars + 30:
            posts[-1] = candidate_last

    total = len(posts)
    numbered = [f"[{idx + 1}/{total}] {post}" for idx, post in enumerate(posts)]
    return "\n---\n".join(numbered)


@mcp.tool()
def format_markdown_for_threads(content: str, max_chars: int = 500) -> str:
    """Split and format content into a Threads thread.

    Each post is kept under max_chars (Threads limit is 500). Posts are
    separated by a blank line. Non-final posts end with 👇 to signal continuation.

    Args:
        content: The text or markdown content to format.
        max_chars: Maximum characters per post (default 500).
    """
    import re

    # Strip markdown to plain text
    text = re.sub(r"#{1,6}\s+", "", content)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"__(.+?)__", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"_(.+?)_", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    # Split into sentences
    sentences = re.split(r"(?<=[。！？.!?])\s*", text)
    sentences = [s.strip() for s in sentences if s.strip()]

    # Pack sentences into posts within max_chars (reserve 2 chars for 👇)
    limit = max_chars - 2
    posts, current = [], ""
    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= limit:
            current = (current + "\n" + sentence).strip()
        else:
            if current:
                posts.append(current)
            if len(sentence) > limit:
                for j in range(0, len(sentence), limit):
                    posts.append(sentence[j:j + limit])
                current = ""
            else:
                current = sentence
    if current:
        posts.append(current)

    result = []
    for i, post in enumerate(posts):
        if i < len(posts) - 1:
            result.append(post + "\n👇")
        else:
            result.append(post)

    return "\n\n".join(result)


@mcp.tool()
def generate_article_cover_html(
    title: str,
    subtitle: str = "",
    author: str = "",
    bg_color: str = "#07c160",
    text_color: str = "#ffffff",
    width: int = 900,
    height: int = 383,
) -> str:
    """Generate a standalone HTML file for an article cover image.

    The returned HTML can be saved as a .html file and opened in a browser
    to screenshot/export as the article cover. Default dimensions match
    WeChat public account cover size (900×383 px).

    Args:
        title: Main article title.
        subtitle: Optional subtitle or tagline.
        author: Author name shown at bottom-right.
        bg_color: Background color (default WeChat green #07c160).
        text_color: Text color (default #ffffff).
        width: Cover width in pixels (default 900).
        height: Cover height in pixels (default 383).
    """
    subtitle_html = (
        f'<div class="subtitle">{subtitle}</div>' if subtitle else ""
    )
    author_html = (
        f'<div class="author">— {author}</div>' if author else ""
    )
    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ width: {width}px; height: {height}px; overflow: hidden; }}
  .cover {{
    width: {width}px;
    height: {height}px;
    background: {bg_color};
    color: {text_color};
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 48px 64px;
    text-align: center;
    font-family: "PingFang TC", "Microsoft JhengHei", "Noto Sans TC", sans-serif;
    position: relative;
  }}
  .cover::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.08);
    clip-path: circle(60% at 90% 10%);
  }}
  .title {{
    font-size: 42px;
    font-weight: bold;
    line-height: 1.3;
    letter-spacing: 2px;
    position: relative;
  }}
  .subtitle {{
    font-size: 20px;
    margin-top: 16px;
    opacity: 0.85;
    position: relative;
  }}
  .author {{
    position: absolute;
    bottom: 24px;
    right: 40px;
    font-size: 16px;
    opacity: 0.7;
  }}
</style>
</head>
<body>
  <div class="cover">
    <div class="title">{title}</div>
    {subtitle_html}
    {author_html}
  </div>
</body>
</html>"""
    return html


@mcp.tool()
async def generate_qrcode(
    content: str,
    size: int = 300,
    format: str = "png",
    fg_color: str = "000000",
    bg_color: str = "ffffff",
) -> str:
    """Generate a QR code for the given text or URL with custom colors.

    Returns a direct image URL using the free api.qrserver.com service.
    The URL can be opened in a browser or embedded directly in articles.

    Args:
        content: Text or URL to encode in the QR code.
        size: Image size in pixels (default 300, range 100–1000).
        format: Image format, 'png' or 'svg' (default 'png').
        fg_color: Foreground (module) color as hex without # (default 000000 = black).
        bg_color: Background color as hex without # (default ffffff = white).
    """
    import urllib.parse

    if format not in ("png", "svg"):
        format = "png"
    size = max(100, min(1000, size))
    fg_color = fg_color.lstrip("#")
    bg_color = bg_color.lstrip("#")
    encoded = urllib.parse.quote(content)
    url = (
        f"https://api.qrserver.com/v1/create-qr-code/"
        f"?data={encoded}&size={size}x{size}&format={format}"
        f"&color={fg_color}&bgcolor={bg_color}"
    )
    result = {
        "qrcode_url": url,
        "content": content,
        "size": size,
        "format": format,
        "fg_color": f"#{fg_color}",
        "bg_color": f"#{bg_color}",
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    logger.info("Starting Financial Datasets MCP Server...")
    mcp.run(transport="stdio")
    logger.info("Server stopped")
