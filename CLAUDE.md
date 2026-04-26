# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Model Context Protocol (MCP) server** that exposes stock market and crypto data from the [Financial Datasets API](https://www.financialdatasets.ai/) to AI assistants like Claude. The entire server lives in a single file: `server.py`.

## Setup

Requires Python 3.11+ and [uv](https://github.com/astral-sh/uv).

```bash
uv venv
source .venv/bin/activate
uv sync
cp .env.example .env
# Set FINANCIAL_DATASETS_API_KEY in .env
```

## Running the Server

```bash
uv run server.py
```

The server communicates over **stdio** (MCP transport), so it produces no visible output when run directly — it's meant to be launched by an MCP client (e.g. Claude Desktop).

## Architecture

All logic is in `server.py`. The pattern is uniform across every tool:

1. **`FastMCP`** from `mcp.server.fastmcp` is the framework. Tools are registered with `@mcp.tool()`.
2. **`make_request(url)`** is the single shared async helper — it loads the API key from `.env` on every call (via `load_dotenv()`), sets the `X-API-KEY` header, makes a GET request with `httpx`, and returns the parsed JSON or an `{"Error": ...}` dict on failure.
3. Each tool constructs a URL against `FINANCIAL_DATASETS_API_BASE = "https://api.financialdatasets.ai"`, calls `make_request`, extracts the relevant key from the response dict, and returns `json.dumps(result, indent=2)` as a string.
4. `mcp.run(transport="stdio")` is invoked in `__main__`.

## API Endpoint Patterns

| Category | Base path |
|---|---|
| Financials | `/financials/income-statements/`, `/financials/balance-sheets/`, `/financials/cash-flow-statements/` |
| Stock prices | `/prices/` (historical), `/prices/snapshot/` (current) |
| Crypto | `/crypto/prices/`, `/crypto/prices/snapshot/`, `/crypto/prices/tickers` |
| SEC filings | `/filings/` |

All financial and price endpoints accept `ticker` as a query parameter. Period-based endpoints (`annual`, `quarterly`, `ttm`) and date-range endpoints (`start_date`, `end_date`) follow from the tool signatures.

## Adding a New Tool

1. Add an `async def` function decorated with `@mcp.tool()`.
2. Write a docstring — the MCP framework exposes this as the tool description to clients.
3. Build the URL from `FINANCIAL_DATASETS_API_BASE`, call `make_request(url)`, extract the relevant response key, and return `json.dumps(..., indent=2)`.
4. Return a descriptive string (not an exception) when data is missing.

Note: `get_crypto_prices` and `get_historical_crypto_prices` are currently identical in implementation — they hit the same endpoint with the same parameters.

## Environment

- `FINANCIAL_DATASETS_API_KEY` — required for authenticated API endpoints. Some endpoints (like available crypto tickers) may work without a key.
- Logging goes to **stderr** so it doesn't interfere with the stdio MCP transport.
