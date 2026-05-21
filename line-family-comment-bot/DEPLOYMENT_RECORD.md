# 📋 Telegram Family Bot 部署記錄

**更新日期**：2026-05-21  
**狀態**：✅ 準備就緒  

---

## 📂 重要檔案路徑

### 核心工作流程檔案
- **主工作流程**：`C:\Users\user\mcp-server\line-family-comment-bot\TELEGRAM_BOT_COMPLETE.json`
- **簡化版本**：`C:\Users\user\mcp-server\line-family-comment-bot\TELEGRAM_BOT_SIMPLE_FIXED.json`

### 部署指南
- **快速開始**：`C:\Users\user\mcp-server\line-family-comment-bot\START_HERE.md`
- **重新啟動服務**：`C:\Users\user\mcp-server\line-family-comment-bot\RESTART_SERVICES.md`
- **修復錯誤**：`C:\Users\user\mcp-server\line-family-comment-bot\FIX_WORKFLOW_ERROR.md`
- **Windows 部署**：`C:\Users\user\mcp-server\line-family-comment-bot\WINDOWS_DEPLOYMENT.md`
- **本記錄文件**：`C:\Users\user\mcp-server\line-family-comment-bot\DEPLOYMENT_RECORD.md`

---

## 🔧 Telegram Bot 配置

### Bot Token
```
8982238347:AAEvvIrMe_o8XifY6LGxQPRLBGCNNHlQBRI
```

### Chat ID
```
6119894493
```

### Bot 帳號
```
@cozuesg_bot
```

### Bot 名稱
```
家庭助手
```

---

## 🔑 Groq API 配置

### Base URL
```
https://api.groq.com/openai/v1
```

### 模型
```
llama-3.3-70b-versatile
```

### API Key
```
YOUR_GROQ_API_KEY (從用戶提供)
```

---

## 🚀 完整部署步驟

### 步驟 1：進入正確目錄
```powershell
cd C:\Users\user\mcp-server
pwd
```

### 步驟 2：更新本地檔案
```powershell
git pull origin claude/line-family-comment-bot-Jzs7e
```

### 步驟 3：啟動 ngrok (第一個 PowerShell 視窗)
```powershell
ngrok http 5678
```

**等待看到**：
```
Forwarding: https://outlet-oxford-clothing.ngrok-free.dev -> http://localhost:5678
```

### 步驟 4：啟動 n8n (第二個 PowerShell 視窗)
```powershell
n8n start
```

**等待看到**：
```
n8n ready on http://localhost:5678
Server started on port 5678
```

### 步驟 5：打開 n8n 儀表板
在瀏覽器中訪問：
```
http://localhost:5678
```

### 步驟 6：導入工作流程
1. 點擊 **+ Create workflow**
2. 選擇 **Import from file**
3. 選擇檔案：
   ```
   C:\Users\user\mcp-server\line-family-comment-bot\TELEGRAM_BOT_COMPLETE.json
   ```
4. 點擊 **Import**

### 步驟 7：配置 Groq API Key
**配置 LLM Model - Chat**：
1. 點擊節點
2. 輸入 Base URL：`https://api.groq.com/openai/v1`
3. 輸入 API Key：`YOUR_GROQ_API_KEY` (從用戶提供)
4. 點擊 Save

**配置 LLM Model - Medical**：
- 重複上述步驟

### 步驟 8：啟用工作流程
1. 點擊右上角 **Toggle** (變綠色 🟢)
2. 確認看到 "Workflow is active"

### 步驟 9：在 Telegram 中測試
1. 打開 Telegram
2. 搜尋 **@cozuesg_bot**
3. 發送訊息：`你好`
4. 機器人應該立即回應

---

## 🔄 重新啟動服務

### 停止服務
```powershell
# 在 ngrok 視窗：Ctrl+C
# 在 n8n 視窗：Ctrl+C
```

### 重新啟動服務
```powershell
# 第一個視窗：ngrok http 5678
# 第二個視窗：n8n start
```

詳見：`C:\Users\user\mcp-server\line-family-comment-bot\RESTART_SERVICES.md`

---

## 🧪 工作流程結構

### 完整流程
```
Webhook (接收 Telegram 消息)
  ↓
Telegram Config (設定配置)
  ↓
Parse Message (解析消息)
  ↓
Branch Switch (路由決策)
  ├─ Output 0: 有照片 → Simple Memory
  ├─ Output 1: 醫療相關 → Medical Search Agent
  └─ Output 2: 一般訊息 → Simple Memory
  ↓
[路徑分岔]

一般聊天路徑：
  Simple Memory (保存上下文)
  ↓
  Normal Chat Agent (生成回覆)
  ↓
  LLM Model - Chat (Groq 模型)
  ↓
  Send Telegram Message (發送回覆)

醫療查詢路徑：
  Medical Search Agent (處理醫療問題)
  ↓
  LLM Model - Medical (Groq 模型)
  ↓
  Wiki Tool (查詢資訊)
  ↓
  Send Telegram Message (發送回覆)
```

---

## 🔍 節點清單

| 節點名稱 | 類型 | 功能 |
|---------|------|------|
| Webhook | Webhook | 接收 Telegram 消息 |
| Telegram Config | Set | 配置 Bot Token 和 Chat ID |
| Parse Message | Function | 解析 Telegram 消息數據 |
| Branch Switch | Switch | 根據條件路由消息 |
| Simple Memory | LangChain Memory | 保存對話上下文 |
| Normal Chat Agent | LangChain Agent | 一般聊天代理 |
| Medical Search Agent | LangChain Agent | 醫療查詢代理 |
| Wiki Tool | Wikipedia Tool | 維基百科信息查詢 |
| LLM Model - Chat | Groq LLM | 一般聊天模型 |
| LLM Model - Medical | Groq LLM | 醫療查詢模型 |
| Send Telegram Message | Telegram | 發送回覆消息 |

---

## 🚨 常見問題

### 沒有收到機器人回應
1. 檢查 ngrok 是否還在運行
2. 檢查 n8n 是否還在運行
3. 檢查 Toggle 是否為綠色（已啟用）
4. 查看 Executions 標籤中的錯誤信息

### Webhook 路徑衝突
1. 刪除舊工作流程
2. 重新導入 TELEGRAM_BOT_COMPLETE.json
3. 重新啟動 n8n

### Groq API 錯誤
1. 驗證 API Key 是否正確
2. 驗證 Base URL 是否正確：`https://api.groq.com/openai/v1`
3. 檢查模型名稱是否正確：`llama-3.3-70b-versatile`

### 無法訪問 http://localhost:5678
1. 確認 n8n 是否仍在運行
2. 運行 `n8n --version` 確認 n8n 已安裝
3. 刷新瀏覽器 (Ctrl+R 或 F5)

---

## ✅ 部署檢查清單

- [ ] 進入 `C:\Users\user\mcp-server` 目錄
- [ ] 運行 `git pull origin claude/line-family-comment-bot-Jzs7e`
- [ ] ngrok 已啟動（看到 Forwarding URL）
- [ ] n8n 已啟動（看到 Server started on port 5678）
- [ ] 瀏覽器能訪問 `http://localhost:5678`
- [ ] 工作流程已導入（TELEGRAM_BOT_COMPLETE.json）
- [ ] LLM Model - Chat 已配置 Groq API Key
- [ ] LLM Model - Medical 已配置 Groq API Key
- [ ] Toggle 已啟用（變綠色 🟢）
- [ ] 在 Telegram 中收到機器人回應

---

## 📞 快速參考

| 項目 | 值 |
|------|-----|
| 本地 n8n 地址 | http://localhost:5678 |
| ngrok Forwarding | https://outlet-oxford-clothing.ngrok-free.dev |
| Telegram Bot | @cozuesg_bot |
| Chat ID | 6119894493 |
| ngrok Port | 5678 |
| n8n Port | 5678 |

---

## 📚 相關文檔

- **詳細部署**：`START_HERE.md`
- **服務重啟**：`RESTART_SERVICES.md`
- **錯誤修復**：`FIX_WORKFLOW_ERROR.md`
- **Windows 指南**：`WINDOWS_DEPLOYMENT.md`
- **本文件**：`DEPLOYMENT_RECORD.md`

---

**最後更新**：2026-05-21  
**狀態**：✅ 部署準備就緒
