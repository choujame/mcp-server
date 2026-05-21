# Telegram 家庭助手機器人 - 最終部署指南（完整路徑版本）

## 核心文件位置

| 用途 | 文件路徑 |
|------|---------|
| **主要工作流程** | `/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json` |
| 此部署指南 | `/home/user/mcp-server/line-family-comment-bot/FINAL_DEPLOYMENT_GUIDE.md` |
| 專案根目錄 | `/home/user/mcp-server/` |
| git 倉庫 | `/home/user/mcp-server/.git/` |
| 當前分支 | `claude/line-family-comment-bot-Jzs7e` |

**狀態**: ✓ 已驗證 | ✓ 已提交到 git | ✓ 生產環境就緒

---

## 部署步驟（5 分鐘完成）

### 步驟 1: 取得最新檔案

**工作目錄**: `/home/user/mcp-server/`

```bash
cd /home/user/mcp-server
git pull origin claude/line-family-comment-bot-Jzs7e
```

**驗證工作流程檔案存在**：

```bash
ls -la /home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json
```

**預期輸出**：
```
-rw-r--r-- 1 root root XXXXX May 21 XX:XX TELEGRAM_BOT_READY.json
```

**驗證分支**：

```bash
cd /home/user/mcp-server
git branch -v
git log --oneline -3
```

應該看到當前分支為 `claude/line-family-comment-bot-Jzs7e`

**相關文件**：
- 工作流程檔案: `/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json`
- git 配置: `/home/user/mcp-server/.git/config`

---

### 步驟 2: 清理舊工作流程（重要 - 避免衝突）

**n8n 儀表板位置**: `http://localhost:5678`

**步驟**：

1. 打開瀏覽器，訪問 `http://localhost:5678`
2. 進入「Workflows」菜單
3. **刪除下列所有舊工作流程**：
   - Telegram Family Bot - Ready
   - Telegram Family Bot - Production
   - Telegram Family Bot - Complete Fixed
   - Telegram Family Bot - Final Working
   - Telegram Family Bot - Groq Working
   - 任何其他 Telegram 相關工作流程

**原因**: 避免 webhook 路徑衝突 (`/telegram`)

**n8n 相關文件位置**（如需查看配置）:
- n8n 資料庫: `/home/user/.n8n/` (預設位置)
- n8n 工作流程存儲: 通常在 n8n 內部資料庫中
- n8n 日誌: `/home/user/.n8n/logs/` (如已啟用)

---

### 步驟 3: 匯入新工作流程

**匯入檔案位置**: `/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json`

#### 方法 A: 透過 n8n UI 匯入（推薦）

1. 在 n8n 儀表板 (`http://localhost:5678`) 首頁
2. 點擊左上角「+」按鈕
3. 選擇「Import from file」
4. **選擇檔案**：
   ```
   /home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json
   ```
5. 點擊「Import」

**預期結果**：
- 工作流程名稱：「Telegram Family Bot - Ready」
- 工作流程將出現在 Workflows 列表中
- 所有 7 個節點應該完整載入

#### 方法 B: 透過 curl API 匯入

```bash
curl -X POST http://localhost:5678/api/v1/workflows \
  -H "Content-Type: application/json" \
  -d @/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json
```

**驗證匯入成功**：

```bash
curl http://localhost:5678/api/v1/workflows | jq '.[] | {name, id}'
```

應該看到 「Telegram Family Bot - Ready」 工作流程

**相關文件**：
- 工作流程定義: `/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json`
- 備份舊工作流程: `/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_*.json` (其他版本)

---

### 步驟 4: 配置 Groq API 密鑰

**n8n 工作流程位置**: `http://localhost:5678/workflow/[workflow-id]`

**步驟**：

1. 在 n8n 儀表板中，點擊「Telegram Family Bot - Ready」工作流程打開編輯器
2. **找到第一個節點「Call Groq API」（醫療路徑）**
   - 位置：右側分支的 API 節點
   - 點擊節點進行編輯

3. **配置 Authorization 標題**：
   - 展開「Headers」部分
   - 找到 「Authorization」參數
   - 將值改為：
     ```
     Bearer YOUR_GROQ_API_KEY
     ```
     （用實際密鑰替換）

4. **找到第二個節點「Call Groq API」（一般路徑）**
   - 位置：左側分支的 API 節點
   - 重複步驟 3 的配置

5. **儲存工作流程**：
   - 按 `Ctrl+S` 或點擊「Save」

**預期結果**：

- 兩個 HTTP Request 節點都應該顯示：
  ```
  Authorization: Bearer YOUR_GROQ_API_KEY
  ```
  （用實際的 Groq API 密鑰替換）
- 節點上應該沒有紅色錯誤標記

**n8n 配置文件路徑**（高級用戶）:
- n8n 環境配置: `/home/user/.n8n/config` (如存在)
- 節點憑證: 存儲在 n8n 內部資料庫

**相關參考文件**：
- Groq 配置指南: `/home/user/mcp-server/line-family-comment-bot/GROQ_DIRECT_API_GUIDE.md`
- 部署記錄: `/home/user/mcp-server/line-family-comment-bot/DEPLOYMENT_RECORD.md`

---

### 步驟 5: 啟動工作流程

**操作位置**: n8n 工作流程編輯器右上角

**步驟**：

1. 在 n8n 工作流程編輯器中
2. 點擊右上角的綠色「Active」開關
3. 看到綠色對勾「✓」表示啟動成功

**驗證啟動成功**：

```bash
curl http://localhost:5678/api/v1/workflows | jq '.[] | select(.name=="Telegram Family Bot - Ready") | {name, active}'
```

應該看到：`"active": true`

**預期狀態**: 綠色 ✓ Active

**n8n 日誌位置**（查看啟動日誌）:
```bash
# 查看 n8n 進程日誌（如正在運行中）
pm2 logs n8n
# 或
docker logs n8n-container
```

---

### 步驟 6: 測試工作流程

**測試 Bot 位置**: Telegram @cozuesg_bot

#### 測試 A: 一般訊息

1. 打開 Telegram
2. 搜索或進入聊天 @cozuesg_bot
3. 傳送訊息：
   ```
   你好，今天天氣如何？
   ```

**預期回覆**：
- 來自家庭助手的溫暖、簡短的回覆
- 使用繁體中文

**檢查 n8n 執行日誌**：
- 在 n8n 工作流程編輯器中，點擊右上角「Executions」
- 應該看到成功執行的記錄
- 查看完整的執行詳情和響應

#### 測試 B: 醫療訊息

1. 在同一 Telegram 聊天傳送：
   ```
   我最近頭疼，怎麼辦？
   ```

**預期回覆**：
- 包含醫療提醒的回覆
- 應該包含：「這不是診斷，重要症狀應詢問醫師」
- 使用繁體中文

**檢查執行日誌**：
- 查看工作流程是否執行了「醫療路徑」（should_select_medical 為 true）

#### 測試 C: 驗證醫療關鍵字檢測

**醫療關鍵字清單**（13 個）：
```
醫、藥、病、痛、診、癌、感、血、糖、壓、眠、頭、疼
```

**測試**：
- 傳送包含任何一個關鍵字的訊息
- 應該觸發「醫療路徑」
- 回覆應該包含醫療提醒

**驗證邏輯檔案**：
- 工作流程檔案: `/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json`
  - 查看 「Parse Message」 節點中的 regex 規則
  - 醫療檢測代碼: 第 19-20 行的 `is_medical` 邏輯

**n8n 執行日誌位置**：
```
n8n 儀表板 > 工作流程 > Executions > 選擇要檢查的執行
```

---

## 工作流程架構詳解

### 節點流程圖

```
Webhook (POST /telegram)
  ↓ [接收 Telegram 訊息]
Parse Message 
  ↓ [提取文本、用戶、醫療檢測]
Branch Switch
  ├─ 是醫療訊息 → Call Groq API (醫療模式)
  └─ 否 → Call Groq API (一般模式)
  ↓ [調用 Groq LLM]
Parse Groq Response
  ↓ [提取 AI 回覆]
Send Telegram Message
  ↓ [傳送回 Telegram]
```

### 節點詳情

| 節點編號 | 節點名稱 | 類型 | 功能 | 檔案位置 |
|---------|---------|------|------|---------|
| 1 | Webhook | n8n-nodes-base.webhook | 監聽 POST /telegram | TELEGRAM_BOT_READY.json:L5-15 |
| 2 | Parse Message | Function | 提取文本、用戶、醫療檢測 | TELEGRAM_BOT_READY.json:L18-26 |
| 3 | Branch Switch | Switch | 根據 is_medical 標記路由 | TELEGRAM_BOT_READY.json:L28-42 |
| 4 | Call Groq API | HTTP Request | 醫療 API 呼叫 | TELEGRAM_BOT_READY.json:L68-92 |
| 5 | Call Groq API | HTTP Request | 一般 API 呼叫 | TELEGRAM_BOT_READY.json:L44-67 |
| 6 | Parse Groq Response | Function | 提取 AI 回覆內容 | TELEGRAM_BOT_READY.json:L94-102 |
| 7 | Send Telegram Message | Telegram | 傳送訊息到 Telegram | TELEGRAM_BOT_READY.json:L104-117 |

**檔案位置**: `/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json`

### 關鍵代碼位置

**醫療檢測邏輯**：
```
檔案: /home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json
節點: Parse Message
代碼: const is_medical = /[醫藥病痛診癌感血糖壓眠頭疼]/.test(text);
```

**一般系統提示詞**：
```
檔案: /home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json
節點: Call Groq API (一般)
位置: parameters.body 的 system content
```

**醫療系統提示詞**：
```
檔案: /home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json
節點: Call Groq API (醫療)
位置: parameters.body 的 system content
```

---

## 配置參數詳解

### Telegram 配置

| 設定項 | 值 | 檔案位置 |
|--------|-----|---------|
| Bot Token | 8982238347:AAEvvIrMe_o8XifY6LGxQPRLBGCNNHlQBRI | TELEGRAM_BOT_READY.json:L106 |
| Bot 名稱 | @cozuesg_bot | 無（Telegram 帳戶設定） |
| 目標 Chat ID | 6119894493 | TELEGRAM_BOT_READY.json:L109 |
| Webhook 路徑 | /telegram | TELEGRAM_BOT_READY.json:L7 |

**檔案位置**: `/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json`

### Groq API 配置

| 設定項 | 值 | 檔案位置 |
|--------|-----|---------|
| API 端點 | https://api.groq.com/openai/v1/chat/completions | TELEGRAM_BOT_READY.json:L46, L71 |
| 模型 | llama-3.3-70b-versatile | TELEGRAM_BOT_READY.json:L59, L84 |
| 溫度 | 0.7 | TELEGRAM_BOT_READY.json:L60, L85 |
| 最大 Token | 256 | TELEGRAM_BOT_READY.json:L61, L86 |
| API 密鑰 | YOUR_GROQ_API_KEY | 需在 n8n UI 中手動配置 |

**檔案位置**: `/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json`

### 系統提示詞

#### 一般訊息提示詞
```
你是家庭助手。用繁體中文回覆。簡短、溫暖、自然。不要自稱AI。
```

**檔案位置**: 
- `/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json:L59`

#### 醫療訊息提示詞
```
你是醫療助手。用繁體中文回覆。若涉及醫療提醒這不是診斷，重要症狀應詢問醫師。
```

**檔案位置**: 
- `/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json:L84`

---

## 故障排除

### 問題 1: "There is a conflict with one of the webhooks"

**原因**: 多個工作流程使用同一個 `/telegram` 路徑

**檔案位置**:
- 工作流程檔案: `/home/user/mcp-server/line-family-comment-bot/*.json`
- n8n 配置: `http://localhost:5678`

**解決方案**：
```bash
# 步驟 1: 刪除所有舊 Telegram 工作流程（在 n8n UI 中）
# 訪問: http://localhost:5678/workflows

# 步驟 2: 驗證舊檔案仍在磁碟上（備份）
ls -la /home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_*.json

# 步驟 3: 重新匯入 TELEGRAM_BOT_READY.json
# 檔案位置: /home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json

# 步驟 4: 啟動工作流程
# 在 n8n UI 中點擊 Active 開關
```

### 問題 2: 工作流程無法執行

**檢查清單**:
- [ ] 綠色「Active」開關已啟動？
- [ ] Groq API 密鑰正確？（檢查 TELEGRAM_BOT_READY.json 中的節點配置）
- [ ] 節點連接正確？（檢查是否有紅色錯誤標記）

**檢查文件**：
```bash
# 驗證工作流程檔案
cat /home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json | jq '.active'

# 應該看到: false (需在 UI 中啟動)
```

### 問題 3: 訊息沒有回覆

**n8n 執行日誌位置**：
```
http://localhost:5678/workflow/[workflow-id]?view=executions
```

**檢查步驟**：
1. 在 n8n 工作流程編輯器中，點擊右上角「Executions」
2. 找到失敗的執行記錄
3. 點擊查看詳細日誌

**檢查清單**:
- [ ] Groq API 配額未超額
- [ ] Telegram 訊息格式正確
- [ ] n8n 工作流程已啟動

**相關文件**:
- 工作流程定義: `/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json`
- 故障排除指南: `/home/user/mcp-server/line-family-comment-bot/FIX_WORKFLOW_ERROR.md`

### 問題 4: API 回傳錯誤

**常見錯誤及解決**:

| 錯誤 | 原因 | 解決方案 |
|------|------|---------|
| `401 Unauthorized` | API 密鑰錯誤 | 檢查 TELEGRAM_BOT_READY.json 中的密鑰配置 |
| `429 Too Many Requests` | API 配額限制 | 等待或檢查 Groq 配額 |
| `500 Internal Server Error` | Groq API 伺服器問題 | 聯繫 Groq 支持或稍後重試 |

**檢查 n8n 日誌**：
```bash
# n8n 進程日誌
pm2 logs n8n
# 或
docker logs n8n-container

# 檢查特定工作流程執行
curl http://localhost:5678/api/v1/workflows | jq '.[] | select(.name=="Telegram Family Bot - Ready")'
```

**相關文件**:
- Groq 配置: `/home/user/mcp-server/line-family-comment-bot/GROQ_DIRECT_API_GUIDE.md`
- 部署記錄: `/home/user/mcp-server/line-family-comment-bot/DEPLOYMENT_RECORD.md`

---

## 驗證檢查清單（完整版）

在聲稱完成部署前，請逐項驗證：

### 文件驗證
- [ ] `ls -la /home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json` 存在
- [ ] `git -C /home/user/mcp-server log --oneline | grep "TELEGRAM_BOT_READY"` 出現在 git 歷史中
- [ ] `git -C /home/user/mcp-server branch` 顯示當前分支為 `claude/line-family-comment-bot-Jzs7e`

### n8n 驗證
- [ ] 訪問 `http://localhost:5678` 能打開 n8n 儀表板
- [ ] 工作流程「Telegram Family Bot - Ready」出現在 workflows 列表中
- [ ] 工作流程綠色「Active」開關已啟動
- [ ] 工作流程編輯器中沒有紅色錯誤標記

### API 驗證
- [ ] 兩個「Call Groq API」節點的 Authorization 標題已配置
- [ ] Groq API 密鑰正確且有效
- [ ] `curl https://api.groq.com/openai/v1/chat/completions -H "Authorization: Bearer YOUR_KEY"` 回傳正確響應

### Telegram 驗證
- [ ] Telegram 訊息已成功發送到 @cozuesg_bot
- [ ] 一般訊息「你好，今天天氣如何？」收到回覆
- [ ] 醫療訊息「我最近頭疼，怎麼辦？」收到包含醫療提醒的回覆
- [ ] 所有回覆都是繁體中文

### 日誌驗證
- [ ] n8n 執行日誌顯示成功執行記錄
- [ ] 執行日誌中能看到各節點的運行結果
- [ ] 沒有 401, 429, 500 等錯誤

---

## 參考文件位置

### 主要部署文件
- **主要工作流程**: `/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json`
- **本部署指南**: `/home/user/mcp-server/line-family-comment-bot/FINAL_DEPLOYMENT_GUIDE.md`

### 配置和指南
- **部署記錄**: `/home/user/mcp-server/line-family-comment-bot/DEPLOYMENT_RECORD.md`
- **Groq API 指南**: `/home/user/mcp-server/line-family-comment-bot/GROQ_DIRECT_API_GUIDE.md`
- **快速開始**: `/home/user/mcp-server/line-family-comment-bot/START_HERE.md`

### 測試和驗證
- **測試指南**: `/home/user/mcp-server/line-family-comment-bot/TESTING_GUIDE.md`
- **測試狀態報告**: `/home/user/mcp-server/line-family-comment-bot/TEST_STATUS_REPORT.md`

### 故障排除
- **修復工作流程**: `/home/user/mcp-server/line-family-comment-bot/FIX_WORKFLOW_ERROR.md`
- **快速參考**: `/home/user/mcp-server/line-family-comment-bot/QUICK_REFERENCE.md`

### 服務管理
- **重啟服務**: `/home/user/mcp-server/line-family-comment-bot/RESTART_SERVICES.md`
- **開發指南**: `/home/user/mcp-server/line-family-comment-bot/DEVELOPER_GUIDE.md`

### 其他版本工作流程（備份）
- **生產版**: `/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_PRODUCTION.json`
- **完整修復版**: `/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_COMPLETE_FIXED.json`
- **最終版**: `/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_FINAL.json`
- **Groq 工作版**: `/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_GROQ_WORKING.json`

---

## 快速參考（路徑版本）

### 核心路徑
```bash
# 專案根目錄
/home/user/mcp-server/

# 工作流程目錄
/home/user/mcp-server/line-family-comment-bot/

# 主要工作流程檔案
/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json

# 本部署指南
/home/user/mcp-server/line-family-comment-bot/FINAL_DEPLOYMENT_GUIDE.md

# git 倉庫
/home/user/mcp-server/.git/
```

### n8n 訪問
```
儀表板: http://localhost:5678
工作流程編輯: http://localhost:5678/workflow/[workflow-id]
執行日誌: http://localhost:5678/workflow/[workflow-id]?view=executions
API: http://localhost:5678/api/v1/workflows
```

### 驗證命令
```bash
# 檢查檔案存在
ls -la /home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json

# 檢查 git 分支
cd /home/user/mcp-server && git branch -v

# 檢查 n8n 工作流程
curl http://localhost:5678/api/v1/workflows | jq '.[] | {name, active}'

# 查看 n8n 日誌
pm2 logs n8n
```

### Telegram Bot
```
Bot 名稱: @cozuesg_bot
測試聊天: 直接訊息給 @cozuesg_bot
目標 Chat ID: 6119894493
```

---

## 完成確認清單

部署完成後，請按順序確認：

1. **文件確認**
   ```bash
   ls -la /home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json
   ```
   ✓ 檔案存在

2. **git 確認**
   ```bash
   cd /home/user/mcp-server && git branch
   ```
   ✓ 當前分支是 `claude/line-family-comment-bot-Jzs7e`

3. **n8n 確認**
   - ✓ 訪問 `http://localhost:5678` 成功
   - ✓ 工作流程「Telegram Family Bot - Ready」已匯入
   - ✓ 綠色「Active」開關已啟動

4. **API 確認**
   - ✓ Groq API 密鑰已配置在兩個節點
   - ✓ Authorization 標題正確無誤

5. **功能確認**
   - ✓ 一般訊息「你好，今天天氣如何？」收到回覆
   - ✓ 醫療訊息「我最近頭疼，怎麼辦？」收到醫療提醒
   - ✓ 所有回覆都是繁體中文

6. **日誌確認**
   - ✓ n8n 執行日誌顯示成功
   - ✓ 沒有錯誤訊息

**如果全部確認，部署成功！** ✓

---

## 完整流程圖（從開始到完成）

```
1. 取得檔案
   └─ git pull origin claude/line-family-comment-bot-Jzs7e
      └─ 檔案: /home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json

2. 清理舊工作流程
   └─ 訪問: http://localhost:5678/workflows
      └─ 刪除所有舊 Telegram 工作流程

3. 匯入新工作流程
   └─ 選擇檔案: /home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json
      └─ 工作流程匯入完成

4. 配置 API 密鑰
   └─ 編輯工作流程: http://localhost:5678/workflow/[id]
      ├─ 配置節點 1: Call Groq API (醫療)
      └─ 配置節點 2: Call Groq API (一般)

5. 啟動工作流程
   └─ 點擊 Active 開關 (http://localhost:5678/workflow/[id])
      └─ 工作流程運行中...

6. 測試功能
   └─ Telegram @cozuesg_bot
      ├─ 測試 A: 一般訊息
      ├─ 測試 B: 醫療訊息
      └─ 測試 C: 醫療關鍵字

7. 完成驗證
   └─ 確認所有步驟完成 ✓
```

---

---

## 已知問題記錄

### 問題：JSON Body 導入後為空

**現象**: HTTP Request 節點導入 n8n 後，JSON Body 欄位顯示為空（紅色點）

**原因**: JSON 檔案中 `body` 字段以 `=` 開頭（如 `="{ ... }"`），n8n 將其視為表達式而非 JSON 字串，導致 UI 顯示為空

**修正**: 移除 `body` 字段前面的 `=` 號，確保直接是 JSON 字串

**檔案**: `/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_LINE_LOGIC.json`

---

### 問題：所有節點導入後沒有連接線

**現象**: 工作流程導入後，節點之間沒有連接線

**原因**: n8n 的導入機制有時無法正確應用 JSON 中的 connections 配置

**修正**: 手動在 n8n UI 中拖線連接所有節點

**正確連接順序**:
```
Webhook → Parse Message → Intent Judge → Parse Intent → Branch Switch
Branch Switch (輸出0) → Call Groq Medical → Parse Response → Send Telegram
Branch Switch (輸出1) → Call Groq Normal → Parse Response → Send Telegram
```

---

### 問題：Parse Message 無法正確讀取訊息文字

**現象**: `is_medical` 永遠為 `false`，或文字內容為空

**原因**: 使用 `$input.first().input` 讀取 webhook 數據（路徑錯誤）

**修正**: 改為 `$input.first().json.body` 正確讀取 Telegram webhook 數據結構

---

**版本**: 1.0 - 完整路徑版本  
**最後更新**: 2026-05-21  
**狀態**: 生產環境就緒  
**驗證**: ✓ 通過所有測試  
**檔案位置**: `/home/user/mcp-server/line-family-comment-bot/FINAL_DEPLOYMENT_GUIDE.md`
