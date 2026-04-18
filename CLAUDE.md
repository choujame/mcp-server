# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A single-file MCP (Model Context Protocol) server that wraps the [Financial Datasets API](https://www.financialdatasets.ai/). It exposes stock and crypto financial data as tools that Claude and other MCP-compatible AI assistants can call.

## Commands

```bash
# Install dependencies
uv venv && source .venv/bin/activate
uv add "mcp[cli]" httpx python-dotenv

# Run the server (stdio transport, for use with MCP clients)
uv run server.py

# Run with the MCP dev inspector (for interactive testing)
mcp dev server.py
```

The server requires a `FINANCIAL_DATASETS_API_KEY` environment variable (set in a `.env` file). Without it, requests still go through but unauthenticated (may be rate-limited or rejected by the API).

## Architecture

The entire server lives in `server.py`. There are no modules, no routing layers, no database — just a `FastMCP` instance with tool functions registered via `@mcp.tool()`.

**Request flow:** MCP client calls a tool → tool builds a URL → `make_request()` makes a GET to `https://api.financialdatasets.ai` → response JSON is extracted and returned as a JSON string.

**`make_request(url)`** is the single HTTP helper. It loads `.env` on every call (intentional, so env changes are picked up at runtime), attaches the API key header if present, and returns the parsed JSON dict or `{"Error": "..."}` on failure.

**All tools follow the same pattern:**
1. Build a query URL from parameters
2. Call `await make_request(url)`
3. Extract the relevant key from the response dict (e.g. `data.get("income_statements", [])`)
4. Return `json.dumps(result, indent=2)` or a "unable to fetch" string

**Transport:** The server runs on `stdio` transport (`mcp.run(transport="stdio")`), which is the standard for Claude Desktop and similar MCP clients. Logging goes to `stderr` to avoid polluting the stdio MCP channel.

## Tool Inventory

| Tool | API endpoint |
|---|---|
| `get_income_statements` | `/financials/income-statements/` |
| `get_balance_sheets` | `/financials/balance-sheets/` |
| `get_cash_flow_statements` | `/financials/cash-flow-statements/` |
| `get_current_stock_price` | `/prices/snapshot/` |
| `get_historical_stock_prices` | `/prices/` |
| `get_company_news` | `/news/` |
| `get_available_crypto_tickers` | `/crypto/prices/tickers` |
| `get_crypto_prices` | `/crypto/prices/` |
| `get_historical_crypto_prices` | `/crypto/prices/` (same endpoint as above) |
| `get_current_crypto_price` | `/crypto/prices/snapshot/` |
| `get_sec_filings` | `/filings/` |

Note: `get_crypto_prices` and `get_historical_crypto_prices` are duplicates — they call the same endpoint with identical logic.

## Adding a New Tool

1. Add an `async def` function decorated with `@mcp.tool()` in `server.py`
2. Write a docstring with an `Args:` section — FastMCP uses these for the MCP tool description and parameter schema
3. Follow the existing pattern: build URL → `make_request` → extract key → return `json.dumps`
4. Return a descriptive string (not raise) on missing data, consistent with the existing tools
