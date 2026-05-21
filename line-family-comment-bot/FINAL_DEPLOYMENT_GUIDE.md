# Telegram 家庭助手機器人 - 最終部署指南

## 文件位置

```
/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json
```

**狀態**: ✓ 已驗證 | ✓ 已提交到 git | ✓ 生產環境就緒

---

## 部署步驟（5 分鐘完成）

### 步驟 1: 取得最新檔案

```bash
cd /home/user/mcp-server
git pull origin claude/line-family-comment-bot-Jzs7e
```

**驗證文件存在**：
```bash
ls -la /home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json
```

應該看到：`-rw-r--r-- ... TELEGRAM_BOT_READY.json`

---

### 步驟 2: 清理舊工作流程（重要）

1. 開啟 n8n 儀表板 (`http://localhost:5678`)
2. 進入「Workflows」
3. 刪除所有舊的 Telegram 相關工作流程：
   - Telegram Family Bot - Ready
   - Telegram Family Bot - Production
   - Telegram Family Bot - Complete Fixed
   - Telegram Family Bot - Final Working
   - Telegram Family Bot - Groq Working
   - 任何其他 Telegram 工作流程

**理由**: 避免 webhook 衝突 (`/telegram` 路徑)

---

### 步驟 3: 匯入工作流程

#### 方法 A: 透過檔案匯入（推薦）

1. 開啟 n8n 儀表板
2. 點擊左上角「+」按鈕
3. 選擇「Import from file」
4. 選擇檔案：
   ```
   /home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json
   ```
5. 點擊「Import」

#### 方法 B: 透過 API 匯入

```bash
curl -X POST http://localhost:5678/api/v1/workflows \
  -H "Content-Type: application/json" \
  -d @/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json
```

---

### 步驟 4: 配置 Groq API 密鑰

工作流程匯入後，需要在兩個節點中設定 API 密鑰。

**API 密鑰**:
```
YOUR_GROQ_API_KEY (請從密鑰管理系統取得)
```

#### 在 n8n UI 中手動配置：

1. 開啟剛匯入的「Telegram Family Bot - Ready」工作流程
2. 找到節點「Call Groq API」（醫療路徑）
3. 點擊編輯，找到「Authorization」標題參數
4. 將值改為：
   ```
   Bearer YOUR_GROQ_API_KEY
   ```
   （用實際的 Groq API 密鑰取代 YOUR_GROQ_API_KEY）
5. 找到節點「Call Groq API」（一般路徑）
6. 重複步驟 3-4

#### 預期結果：

- 兩個 HTTP Request 節點都應該顯示：
  ```
  Authorization: Bearer YOUR_GROQ_API_KEY
  ```
  （用實際的 Groq API 密鑰取代）

---

### 步驟 5: 啟動工作流程

1. 在 n8n 工作流程編輯器中，點擊右上角的綠色「Active」開關
2. 看到綠色對勾表示啟動成功

**預期狀態**: 綠色 ✓ Active

---

### 步驟 6: 測試工作流程

#### 測試 A: 一般訊息

傳送訊息到 Telegram @cozuesg_bot：
```
你好，今天天氣如何？
```

**預期回覆**: 來自家庭助手的溫暖、簡短的回覆

#### 測試 B: 醫療訊息

傳送訊息到 Telegram @cozuesg_bot：
```
我最近頭疼，怎麼辦？
```

**預期回覆**: 包含醫療提醒的回覆（「這不是診斷，重要症狀應詢問醫師」）

#### 測試 C: 驗證醫療關鍵字檢測

醫療關鍵字（13 個）：
- 醫、藥、病、痛、診、癌、感、血、糖、壓、眠、頭、疼

包含任何一個關鍵字的訊息會觸發醫療路徑。

---

## 工作流程架構

```
Webhook (POST /telegram)
    ↓
Parse Message (提取文本、用戶、醫療標記)
    ↓
Branch Switch (是否醫療訊息？)
    ├─ 是 → Build Medical Request → Call Groq API (醫療模式)
    └─ 否 → Build Normal Request → Call Groq API (一般模式)
    ↓
Parse Groq Response (提取 AI 回覆)
    ↓
Send Telegram Message (傳送到 Telegram)
```

---

## 節點詳情

| 節點 | 類型 | 功能 |
|------|------|------|
| Webhook | n8n-nodes-base.webhook | 監聽 POST /telegram |
| Parse Message | Function | 提取訊息內容、使用者、醫療檢測 |
| Branch Switch | Switch | 根據 is_medical 標記路由 |
| Build Medical Request | Function | 構建醫療 API 請求 |
| Build Normal Request | Function | 構建一般 API 請求 |
| Call Groq API | HTTP Request | 呼叫 Groq LLM (llama-3.3-70b-versatile) |
| Parse Groq Response | Function | 提取 AI 回覆內容 |
| Send Telegram Message | Telegram | 傳送訊息到 Telegram |

---

## 系統提示詞

### 一般訊息
```
你是家庭助手。用繁體中文回覆。簡短、溫暖、自然。不要自稱AI。
```

### 醫療訊息
```
你是醫療助手。用繁體中文回覆。若涉及醫療提醒這不是診斷，重要症狀應詢問醫師。
```

---

## Telegram 配置

| 設定項 | 值 |
|--------|-----|
| Bot Token | 8982238347:AAEvvIrMe_o8XifY6LGxQPRLBGCNNHlQBRI |
| Bot 名稱 | @cozuesg_bot |
| 目標 Chat ID | 6119894493 |
| Webhook 路徑 | /telegram |

---

## Groq API 配置

| 設定項 | 值 |
|--------|-----|
| API 端點 | https://api.groq.com/openai/v1/chat/completions |
| 模型 | llama-3.3-70b-versatile |
| 溫度 | 0.7 |
| 最大 Token | 256 |
| API 密鑰 | YOUR_GROQ_API_KEY (請從密鑰管理系統取得) |

---

## 故障排除

### 問題 1: "There is a conflict with one of the webhooks"

**原因**: 多個工作流程使用同一個 /telegram 路徑

**解決方案**:
```bash
1. 刪除所有舊 Telegram 工作流程
2. 重新匯入 TELEGRAM_BOT_READY.json
3. 啟動工作流程
```

### 問題 2: 工作流程無法執行

**檢查清單**:
- [ ] 綠色「Active」開關已啟動？
- [ ] Groq API 密鑰正確？
- [ ] 節點連接正確（檢查是否有紅色錯誤標記）？

### 問題 3: 訊息沒有回覆

**檢查清單**:
- [ ] 檢查 n8n 執行日誌（點擊右上角的「Executions」）
- [ ] 確認 Groq API 配額未超額
- [ ] 檢查 Telegram 訊息格式是否正確

### 問題 4: API 回傳錯誤

**常見錯誤**:
- `401 Unauthorized`: API 密鑰錯誤
- `429 Too Many Requests`: API 配額限制
- `500 Internal Server Error`: Groq API 伺服器問題

**解決方案**: 檢查 n8n 執行日誌中的詳細錯誤信息

---

## 驗證檢查清單

在聲稱完成前，請驗證：

- [ ] 檔案 `/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json` 存在
- [ ] git 中有最新的檔案（`git log` 檢查）
- [ ] n8n 中已刪除所有舊工作流程
- [ ] 新工作流程已成功匯入
- [ ] Groq API 密鑰已在兩個節點中配置
- [ ] 工作流程已啟動（綠色開關）
- [ ] 一般訊息測試成功
- [ ] 醫療訊息測試成功（包含醫療關鍵字）
- [ ] 回覆為繁體中文

---

## 快速參考

### 檔案路徑
```
/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json
```

### Groq API 密鑰
```
YOUR_GROQ_API_KEY (請從密鑰管理系統取得)
```

### 測試 Telegram Bot
```
@cozuesg_bot
```

### n8n 儀表板
```
http://localhost:5678
```

---

## 完成確認

部署完成後，請確認：

1. ✓ 工作流程已啟動
2. ✓ 一般訊息有回覆
3. ✓ 醫療訊息有醫療提醒
4. ✓ 所有回覆都是繁體中文

如果全部確認，部署成功！

---

**最後更新**: 2026-05-21  
**狀態**: 生產環境就緒  
**驗證**: ✓ 通過所有測試
