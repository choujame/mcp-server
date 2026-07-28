# MCP Server — 使用指南

## 自動爬蟲規則

**每當需要讀取、抓取、分析任何網頁內容時，優先使用以下工具，不要使用 httpx / requests 自行抓取：**

| 情境 | 使用工具 |
|------|---------|
| 讀取單一網頁內容 | `firecrawl_scrape(url)` |
| 爬整個網站（多頁） | `firecrawl_crawl(url, limit)` |
| 需要更強健的爬蟲（JavaScript、動態頁面） | `apify_scrape(url, max_pages)` |
| Firecrawl / Apify 都失敗，或頁面需要真實瀏覽器渲染 | `browser_scrape(url)`（需安裝 `browser` 選用依賴，見下方） |

### 選擇邏輯
1. 預設用 `firecrawl_scrape`（最快，適合單頁靜態內容）
2. 需要整個網站時用 `firecrawl_crawl`
3. Firecrawl 失敗或頁面需要 JavaScript 渲染時改用 `apify_scrape`
4. 若以上都失敗（例如頁面有反爬蟲機制、需要等待動態內容載入），最後才用 `browser_scrape`（Playwright headless Chromium 實際渲染頁面）

## 選用依賴（Optional Dependencies）

```bash
pip install "mcp-server[browser]"   # 安裝 browser_scrape 所需的 Playwright
python -m playwright install chromium
```

## 環境變數

```
FINANCIAL_DATASETS_API_KEY   # financialdatasets.ai API key
FIRECRAWL_API_KEY            # firecrawl.dev API key
APIFY_API_TOKEN              # apify.com API token
MCP_TRANSPORT                # stdio（本地）或 sse（雲端），預設 stdio
PORT                         # SSE 模式的監聽 port，預設 8000
```

## 本地啟動

```bash
python server.py
```

## 雲端部署（Railway / Render）

1. 在平台設定以下環境變數：
   - `MCP_TRANSPORT=sse`
   - `FIRECRAWL_API_KEY=...`
   - `APIFY_API_TOKEN=...`
2. 部署後取得 URL，例如 `https://your-app.railway.app`
3. 在 Claude Code 新增 MCP server：
   ```bash
   claude mcp add --transport sse https://your-app.railway.app/sse
   ```
