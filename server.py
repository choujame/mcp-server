import json
import os
import re
import shutil
import httpx
import logging
import sys
from datetime import datetime, timezone
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

# ---------------------------------------------------------------------------
# Obsidian Knowledge Base Tools (Karpathy-style)
# ---------------------------------------------------------------------------

def _resolve_vault(vault_path: str) -> Path:
    """Return a validated absolute Path for the vault, loading from env if needed."""
    load_dotenv()
    vp = vault_path.strip() or os.environ.get("OBSIDIAN_VAULT_PATH", "").strip()
    if not vp:
        raise ValueError(
            "vault_path is required. Pass it directly or set OBSIDIAN_VAULT_PATH in .env"
        )
    p = Path(vp).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(f"Vault directory not found: {p}")
    if not p.is_dir():
        raise NotADirectoryError(f"Vault path is not a directory: {p}")
    return p


def _safe_child(parent: Path, name: str) -> Path:
    """Resolve a child path and ensure it stays inside parent (no path traversal)."""
    child = (parent / name).resolve()
    if not str(child).startswith(str(parent)):
        raise ValueError(f"Path traversal detected: {name!r}")
    return child


def _slugify(title: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    slug = re.sub(r"[\s_]+", "-", slug).strip("-")
    return slug or "untitled"


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


@mcp.tool()
async def setup_vault_structure(vault_path: str = "") -> str:
    """Set up the Karpathy-style knowledge base structure inside an Obsidian vault.

    Creates:
      - raw/        — drop zone for clipped articles / raw notes
      - wiki/       — AI-processed, structured knowledge entries
      - index.md    — auto-maintained table of contents
      - log.md      — append-only activity log

    Args:
        vault_path: Absolute path to the Obsidian vault folder.
                    Falls back to the OBSIDIAN_VAULT_PATH environment variable.
    """
    vault = _resolve_vault(vault_path)
    created = []

    for folder in ("raw", "wiki", "raw/processed"):
        d = vault / folder
        if not d.exists():
            d.mkdir(parents=True)
            created.append(f"  created  {folder}/")
        else:
            created.append(f"  exists   {folder}/")

    index_path = vault / "index.md"
    if not index_path.exists():
        index_path.write_text(
            "# Knowledge Base Index\n\n"
            "> Auto-maintained by Claude Code\n\n"
            "## Wiki Entries\n\n"
            "_No entries yet. Run `update_index` after adding wiki pages._\n",
            encoding="utf-8",
        )
        created.append("  created  index.md")
    else:
        created.append("  exists   index.md")

    log_path = vault / "log.md"
    if not log_path.exists():
        log_path.write_text(
            "# Knowledge Base Log\n\n"
            "> Append-only activity log — do not edit manually.\n\n",
            encoding="utf-8",
        )
        created.append("  created  log.md")
    else:
        created.append("  exists   log.md")

    report = "\n".join(created)
    return f"Vault structure ready at {vault}\n\n{report}"


@mcp.tool()
async def list_raw_files(vault_path: str = "") -> str:
    """List unprocessed files waiting in raw/.

    Args:
        vault_path: Absolute path to the Obsidian vault.
    """
    vault = _resolve_vault(vault_path)
    raw_dir = vault / "raw"
    if not raw_dir.exists():
        return "raw/ directory does not exist. Run setup_vault_structure first."

    files = sorted(
        f.name for f in raw_dir.iterdir()
        if f.is_file() and not f.name.startswith(".")
    )
    if not files:
        return "raw/ is empty — nothing to process."
    return json.dumps({"count": len(files), "files": files}, indent=2)


@mcp.tool()
async def read_raw_file(filename: str, vault_path: str = "") -> str:
    """Read the contents of a file from raw/.

    Args:
        filename: File name relative to raw/ (e.g. "article.md").
        vault_path: Absolute path to the Obsidian vault.
    """
    vault = _resolve_vault(vault_path)
    path = _safe_child(vault / "raw", filename)
    if not path.exists():
        return f"File not found: raw/{filename}"
    return path.read_text(encoding="utf-8")


@mcp.tool()
async def create_wiki_entry(
    title: str,
    content: str,
    tags: list[str] | None = None,
    vault_path: str = "",
) -> str:
    """Create (or overwrite) a processed wiki entry in wiki/.

    The file is written as Markdown with YAML front-matter containing title,
    date, and tags so Obsidian can index it.

    Args:
        title:      Human-readable title of the entry.
        content:    Markdown body of the entry (without front-matter).
        tags:       Optional list of tag strings.
        vault_path: Absolute path to the Obsidian vault.
    """
    vault = _resolve_vault(vault_path)
    wiki_dir = vault / "wiki"
    wiki_dir.mkdir(exist_ok=True)

    slug = _slugify(title)
    filename = f"{slug}.md"
    path = _safe_child(wiki_dir, filename)

    tag_list = tags or []
    tag_yaml = json.dumps(tag_list)  # compact JSON array is valid YAML

    frontmatter = (
        f"---\n"
        f'title: "{title}"\n'
        f"date: {_today()}\n"
        f"tags: {tag_yaml}\n"
        f"---\n\n"
    )
    path.write_text(frontmatter + content.strip() + "\n", encoding="utf-8")
    return f"Wiki entry written: wiki/{filename}"


@mcp.tool()
async def list_wiki_entries(vault_path: str = "") -> str:
    """List all entries in wiki/.

    Args:
        vault_path: Absolute path to the Obsidian vault.
    """
    vault = _resolve_vault(vault_path)
    wiki_dir = vault / "wiki"
    if not wiki_dir.exists():
        return "wiki/ directory does not exist. Run setup_vault_structure first."

    entries = []
    for f in sorted(wiki_dir.iterdir()):
        if f.is_file() and f.suffix == ".md" and not f.name.startswith("."):
            entries.append({"filename": f.name, "size_bytes": f.stat().st_size})

    if not entries:
        return "wiki/ is empty — no entries yet."
    return json.dumps({"count": len(entries), "entries": entries}, indent=2)


@mcp.tool()
async def read_wiki_entry(filename: str, vault_path: str = "") -> str:
    """Read a wiki entry from wiki/.

    Args:
        filename:   File name relative to wiki/ (e.g. "machine-learning.md").
        vault_path: Absolute path to the Obsidian vault.
    """
    vault = _resolve_vault(vault_path)
    path = _safe_child(vault / "wiki", filename)
    if not path.exists():
        return f"File not found: wiki/{filename}"
    return path.read_text(encoding="utf-8")


@mcp.tool()
async def update_index(vault_path: str = "") -> str:
    """Regenerate index.md from the current contents of wiki/.

    Scans wiki/ for Markdown files, reads their front-matter title and tags,
    then rewrites index.md with a sorted alphabetical table of contents.

    Args:
        vault_path: Absolute path to the Obsidian vault.
    """
    vault = _resolve_vault(vault_path)
    wiki_dir = vault / "wiki"
    if not wiki_dir.exists():
        return "wiki/ directory does not exist. Run setup_vault_structure first."

    entries = []
    frontmatter_re = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
    title_re = re.compile(r'^title:\s*"?([^"\n]+)"?', re.MULTILINE)
    tags_re = re.compile(r'^tags:\s*(\[.*?\])', re.MULTILINE)

    for f in sorted(wiki_dir.iterdir()):
        if not (f.is_file() and f.suffix == ".md" and not f.name.startswith(".")):
            continue
        text = f.read_text(encoding="utf-8")
        fm_match = frontmatter_re.match(text)
        fm = fm_match.group(1) if fm_match else ""

        title_match = title_re.search(fm)
        title = title_match.group(1).strip() if title_match else f.stem

        tags_match = tags_re.search(fm)
        try:
            tags = json.loads(tags_match.group(1)) if tags_match else []
        except Exception:
            tags = []

        tag_str = " ".join(f"`{t}`" for t in tags) if tags else ""
        entries.append((title, f.name, tag_str))

    lines = [
        "# Knowledge Base Index\n",
        "> Auto-maintained by Claude Code\n",
        f"\n_Last updated: {_today()} — {len(entries)} entries_\n",
        "\n## Wiki Entries\n",
    ]
    if entries:
        lines.append("| Title | Tags |\n|-------|------|\n")
        for title, fname, tag_str in entries:
            lines.append(f"| [[wiki/{fname}\\|{title}]] | {tag_str} |\n")
    else:
        lines.append("_No entries yet._\n")

    (vault / "index.md").write_text("".join(lines), encoding="utf-8")
    return f"index.md updated with {len(entries)} entries."


@mcp.tool()
async def append_log(entry: str, vault_path: str = "") -> str:
    """Append a timestamped entry to log.md.

    Args:
        entry:      The text to record (one or more lines).
        vault_path: Absolute path to the Obsidian vault.
    """
    vault = _resolve_vault(vault_path)
    log_path = vault / "log.md"
    if not log_path.exists():
        log_path.write_text(
            "# Knowledge Base Log\n\n"
            "> Append-only activity log — do not edit manually.\n\n",
            encoding="utf-8",
        )

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    block = f"\n### {now}\n\n{entry.strip()}\n"
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(block)
    return f"Log entry appended at {now}."


@mcp.tool()
async def archive_raw_file(filename: str, vault_path: str = "") -> str:
    """Move a processed file from raw/ to raw/processed/.

    Call this after you have created a wiki entry from a raw file so the
    source is preserved but no longer appears in the unprocessed queue.

    Args:
        filename:   File name relative to raw/ (e.g. "article.md").
        vault_path: Absolute path to the Obsidian vault.
    """
    vault = _resolve_vault(vault_path)
    src = _safe_child(vault / "raw", filename)
    if not src.exists():
        return f"File not found: raw/{filename}"

    dest_dir = vault / "raw" / "processed"
    dest_dir.mkdir(exist_ok=True)
    dest = _safe_child(dest_dir, filename)

    # Avoid silent overwrites by appending a timestamp suffix
    if dest.exists():
        stem, suffix = dest.stem, dest.suffix
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        dest = dest_dir / f"{stem}-{ts}{suffix}"

    shutil.move(str(src), str(dest))
    return f"Archived: raw/{filename} → raw/processed/{dest.name}"


@mcp.tool()
async def search_knowledge_base(query: str, vault_path: str = "") -> str:
    """Case-insensitive text search across all notes in raw/ and wiki/.

    Returns file paths and the matching lines with surrounding context.

    Args:
        query:      Search string (plain text, case-insensitive).
        vault_path: Absolute path to the Obsidian vault.
    """
    vault = _resolve_vault(vault_path)
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    results = []

    for subdir in ("raw", "wiki"):
        d = vault / subdir
        if not d.exists():
            continue
        for f in sorted(d.rglob("*.md")):
            if f.name.startswith("."):
                continue
            lines = f.read_text(encoding="utf-8").splitlines()
            hits = []
            for i, line in enumerate(lines):
                if pattern.search(line):
                    start = max(0, i - 1)
                    end = min(len(lines), i + 2)
                    ctx = lines[start:end]
                    hits.append({"line": i + 1, "context": "\n".join(ctx)})
            if hits:
                rel = str(f.relative_to(vault))
                results.append({"file": rel, "matches": hits})

    if not results:
        return f"No results found for: {query!r}"
    return json.dumps({"query": query, "total_files": len(results), "results": results}, indent=2)


if __name__ == "__main__":
    # Log server startup
    logger.info("Starting Financial Datasets MCP Server...")

    # Initialize and run the server
    mcp.run(transport="stdio")

    # This line won't be reached during normal operation
    logger.info("Server stopped")
