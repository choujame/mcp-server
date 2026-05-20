"""
Taiwan Legal Database MCP Server

Provides tools for querying three public Taiwan government databases:
  - 全國法規資料庫 (Ministry of Justice)
  - 司法院裁判書查詢 (Judicial Yuan)
  - 立法院議案系統 (Legislative Yuan)
"""

import json
import logging
import os
import sys
from typing import Optional

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("taiwan-legal-mcp")

load_dotenv()

mcp = FastMCP("taiwan-legal")

MOJ_API_BASE = os.getenv("MOJ_API_BASE", "https://law.moj.gov.tw/api/v1/Law")
JUDICIAL_API_BASE = os.getenv("JUDICIAL_API_BASE", "https://judgment.judicial.gov.tw/FJUD/api")
LY_API_BASE = os.getenv("LY_API_BASE", "https://lis.ly.gov.tw")

DEFAULT_TIMEOUT = 30.0
DEFAULT_PAGE_SIZE = 20


async def _get(url: str, params: dict | None = None) -> dict | list | None:
    headers = {
        "Accept": "application/json",
        "User-Agent": "taiwan-legal-mcp/1.0",
    }
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT, follow_redirects=True) as client:
        try:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            logger.error("HTTP %s for %s", exc.response.status_code, url)
            return {"error": f"HTTP {exc.response.status_code}: {exc.response.text[:200]}"}
        except Exception as exc:
            logger.error("Request failed for %s: %s", url, exc)
            return {"error": str(exc)}


def _fmt(data: dict | list | None) -> str:
    if data is None:
        return "No data returned."
    if isinstance(data, dict) and "error" in data:
        return f"Error: {data['error']}"
    return json.dumps(data, ensure_ascii=False, indent=2)


@mcp.tool()
async def search_laws(keyword: str) -> str:
    """搜尋法條：依關鍵字搜尋法規條文。

    Uses 全國法規資料庫 (MOJ) SearchLaw endpoint to find laws matching
    the keyword. Returns law names, categories, and pcodes that can be
    passed to get_law_content.

    Args:
        keyword: Keyword to search for (Chinese or English).
    """
    data = await _get(f"{MOJ_API_BASE}/SearchLaw", {"keyword": keyword})

    if isinstance(data, dict) and "error" in data:
        return _fmt(data)

    results = (data or {}).get("SearchResult", [])
    if not results:
        return f"未找到包含「{keyword}」的法規。"

    laws = [
        {
            "law_name": r.get("LawName", ""),
            "pcode": r.get("LawPCode", ""),
            "category": r.get("LawCategory", ""),
            "last_amended": r.get("LawModifiedDate", ""),
        }
        for r in results
    ]
    return json.dumps(laws, ensure_ascii=False, indent=2)


@mcp.tool()
async def get_law_content(law_name: str) -> str:
    """取得法規全文。

    Resolves the law name to a pcode via SearchLaw, then fetches the full
    article text from 全國法規資料庫 (MOJ).

    Args:
        law_name: Exact or partial name of the law, e.g. 「民法」or「勞動基準法」.
    """
    search_data = await _get(f"{MOJ_API_BASE}/SearchLaw", {"keyword": law_name})
    if isinstance(search_data, dict) and "error" in search_data:
        return _fmt(search_data)

    results = (search_data or {}).get("SearchResult", [])
    if not results:
        return f"找不到法規「{law_name}」，請確認名稱是否正確。"

    pcode = results[0].get("LawPCode", "")
    if not pcode:
        return f"無法取得「{law_name}」的法規代碼。"

    law_data = await _get(f"{MOJ_API_BASE}/Law", {"pcode": pcode})
    return _fmt(law_data)


@mcp.tool()
async def search_judgments(keyword: str, court: Optional[str] = None) -> str:
    """查詢判決書。

    Searches 司法院裁判書系統 (Judicial Yuan) for court decisions matching
    the keyword.

    Args:
        keyword: Keyword to search in judgment titles or content.
        court:   Optional court code, e.g. "TPS" (最高法院),
                 "TPH" (臺灣高等法院), "TPC" (臺灣臺北地方法院).
    """
    params: dict = {
        "jud_title": keyword,
        "page": 1,
        "pageSize": DEFAULT_PAGE_SIZE,
    }
    if court:
        params["court"] = court

    data = await _get(f"{JUDICIAL_API_BASE}/Search", params)
    if isinstance(data, dict) and "error" in data:
        return _fmt(data)

    judgments = (data or {}).get("jud", [])
    if not judgments:
        return f"未找到關於「{keyword}」的判決書。"

    summary = [
        {
            "case_no": j.get("jud_no", ""),
            "date": j.get("jud_date", ""),
            "court": j.get("court_name", ""),
            "title": j.get("jud_title", ""),
        }
        for j in judgments
    ]
    return json.dumps(summary, ensure_ascii=False, indent=2)


@mcp.tool()
async def get_legislation_progress(
    bill_no: Optional[str] = None,
    keyword: Optional[str] = None,
) -> str:
    """查詢立法院議案進度。

    Queries the Legislative Yuan (立法院) for the status and progress of bills.
    At least one of bill_no or keyword must be provided.

    Args:
        bill_no: Bill number, e.g. "1100803070".
        keyword: Keyword to search in bill names.
    """
    if not bill_no and not keyword:
        return "請提供議案編號 (bill_no) 或關鍵字 (keyword)。"

    params: dict = {
        "action": "getBillList",
        "pageSize": DEFAULT_PAGE_SIZE,
        "page": 1,
    }
    if bill_no:
        params["billNo"] = bill_no
    if keyword:
        params["keyword"] = keyword

    data = await _get(f"{LY_API_BASE}/lisdoc/docIndex.action", params)
    if isinstance(data, dict) and "error" in data:
        return _fmt(data)

    bills = (data or {}).get("bills", [])
    if not bills:
        hint = bill_no or keyword
        return f"未找到關於「{hint}」的議案。"

    return json.dumps(bills, ensure_ascii=False, indent=2)


@mcp.tool()
async def track_law_changes(law_name: str) -> str:
    """查詢法規異動紀錄。

    Returns the amendment history for a specific law from
    全國法規資料庫 (MOJ), including each amendment date and reason.

    Args:
        law_name: Name of the law, e.g. 「勞動基準法」.
    """
    search_data = await _get(f"{MOJ_API_BASE}/SearchLaw", {"keyword": law_name})
    if isinstance(search_data, dict) and "error" in search_data:
        return _fmt(search_data)

    results = (search_data or {}).get("SearchResult", [])
    if not results:
        return f"找不到法規「{law_name}」。"

    pcode = results[0].get("LawPCode", "")
    if not pcode:
        return f"無法取得「{law_name}」的法規代碼。"

    history_data = await _get(f"{MOJ_API_BASE}/History", {"pcode": pcode})
    return _fmt(history_data)


@mcp.tool()
async def explain_legal_term(term: str) -> str:
    """法律名詞解釋（用法規資料庫的相關條文解釋）。

    Searches 全國法規資料庫 (MOJ) for laws containing the term and returns
    the top relevant results. Use get_law_content with the returned pcode to
    read the full article text for an authoritative definition.

    Args:
        term: Legal term to look up, e.g. 「善意第三人」or「連帶責任」.
    """
    data = await _get(f"{MOJ_API_BASE}/SearchLaw", {"keyword": term})

    if isinstance(data, dict) and "error" in data:
        return _fmt(data)

    results = (data or {}).get("SearchResult", [])
    if not results:
        return f"法規資料庫中未找到與「{term}」相關的條文。"

    related_laws = [
        {
            "law_name": r.get("LawName", ""),
            "pcode": r.get("LawPCode", ""),
            "category": r.get("LawCategory", ""),
            "last_amended": r.get("LawModifiedDate", ""),
        }
        for r in results[:10]
    ]

    explanation = {
        "term": term,
        "note": (
            "以下為法規資料庫中包含此名詞的相關法規。"
            "如需查閱特定條文，請使用 get_law_content 取得法規全文。"
        ),
        "related_laws": related_laws,
    }
    return json.dumps(explanation, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    logger.info("Starting Taiwan Legal Database MCP Server...")
    mcp.run(transport="stdio")
