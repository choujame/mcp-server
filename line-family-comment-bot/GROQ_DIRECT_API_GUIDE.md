# 📘 Telegram 家庭助手 - Groq 直接 API 使用指南

**建立日期**：2026-05-21  
**狀態**：✅ 已準備  
**工作流程檔案**：`TELEGRAM_BOT_GROQ_DIRECT.json`

---

## 🎯 使用本指南的時機

如果您遇到以下問題，請使用本工作流程：

- ❌ LLM Model 節點顯示 "OpenAI account 5" credential
- ❌ LLM 配置無法正確保存
- ❌ Groq API credential 設置失敗
- ❌ 工作流程無法連接到 LLM 模型

✅ **本工作流程直接呼叫 Groq API，避免所有 credential 問題！**

---

## 🚀 完整部署步驟（5 分鐘）

### **步驟 1：進入正確目錄**
```bash
cd /home/user/mcp-server
pwd
```

**預期結果**：
```
/home/user/mcp-server
```

---

### **步驟 2：更新本地檔案**
```bash
git pull origin claude/line-family-comment-bot-Jzs7e
```

**預期結果**：
```
Already up to date.
```

或者看到新增的檔案：
```
create mode 100644 line-family-comment-bot/TELEGRAM_BOT_GROQ_DIRECT.json
```

---

### **步驟 3：確認 ngrok 正在運行**

**第一個 PowerShell 視窗：**

查看 ngrok 是否還在運行。如果停止了，重新啟動：
```powershell
ngrok http 5678
```

**預期看到**：
```
Forwarding    https://outlet-oxford-clothing.ngrok-free.dev -> http://localhost:5678
```

✅ **記下這個 ngrok URL，稍後會用到**

---

### **步驟 4：確認 n8n 正在運行**

**第二個 PowerShell 視窗：**

查看 n8n 是否還在運行。如果停止了，重新啟動：
```powershell
n8n start
```

**預期看到**：
```
n8n ready on http://localhost:5678
Server started on port 5678
```

---

### **步驟 5：打開 n8n 儀表板**

在瀏覽器中訪問：
```
http://localhost:5678
```

**預期結果**：看到 n8n 儀表板首頁

---

### **步驟 6：刪除舊工作流程（如果存在）**

1. 在 n8n 中找到舊的工作流程（如 "Telegram Family Bot - Complete Version"）
2. 點擊右上角三個點 **⋮**
3. 選擇 **Delete**
4. 確認刪除

**原因**：避免 webhook 路徑衝突

---

### **步驟 7：導入新工作流程**

1. 點擊 **+ Create workflow** 或 **New**
2. 選擇 **Import from file**
3. 選擇檔案：
   ```
   /home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_GROQ_DIRECT.json
   ```
4. 點擊 **Import**

**預期結果**：看到工作流程被導入，節點顯示如下：
```
Webhook
  ↓
Parse Message
  ↓
Branch Switch
  ├─ Output 0: Medical Prompt
  └─ Output 1: Normal Prompt
  ↓
Call Groq API
  ↓
Parse Groq Response
  ↓
Send Telegram Message
```

---

### **步驟 8：配置 Groq API Key**

找到 **Call Groq API** 節點：

1. 雙擊打開節點
2. 在 **Header Parameters** 中找到 `Authorization` 欄位
3. 將值從 `Bearer YOUR_GROQ_API_KEY` 改為 `Bearer <您的真實 API Key>`
4. 點擊 **Save**

**您的 Groq API Key**：
```
YOUR_GROQ_API_KEY
```

**正確格式範例**：
```
Bearer YOUR_GROQ_API_KEY
```

---

### **步驟 9：啟用工作流程**

1. 點擊右上角 **Toggle** 按鈕（變綠色 🟢）
2. 確認看到訊息："Workflow is active"

---

### **步驟 10：在 Telegram 測試**

1. 打開 Telegram
2. 搜尋 **@cozuesg_bot**
3. 發送訊息測試：

**一般訊息**：
```
你好！
```

**醫療相關**（測試路由）：
```
我最近頭很疼，怎麼辦？
```

**預期結果**：
- 機器人立即回應（3-5 秒內）
- 回應使用繁體中文
- 一般訊息和醫療訊息有不同的回覆方式

✅ **完成！機器人已成功部署**

---

## 🔄 工作流程架構

```
Webhook (接收 Telegram 訊息)
  ↓
Parse Message (解析訊息內容)
  - 提取：text, chat_id, user_id, first_name
  - 偵測：是否包含醫療關鍵字
  ↓
Branch Switch (路由決策)
  - 醫療訊息 → Medical Prompt
  - 一般訊息 → Normal Prompt
  ↓
[對應的 Prompt 設置系統指令]
  ↓
Call Groq API (直接 HTTP 呼叫)
  - URL: https://api.groq.com/openai/v1/chat/completions
  - 模型: llama-3.3-70b-versatile
  - 溫度: 0.7
  - 最大令牌: 256
  ↓
Parse Groq Response (解析 API 回應)
  ↓
Send Telegram Message (發送回覆)
```

---

## 🔑 配置詳細信息

### **Telegram Bot 配置**

| 項目 | 值 |
|------|-----|
| Bot Token | `YOUR_TELEGRAM_BOT_TOKEN` |
| Chat ID | `YOUR_CHAT_ID` |
| Bot 帳號 | `@cozuesg_bot` |
| Bot 名稱 | 家庭助手 |

### **Groq API 配置**

| 項目 | 值 |
|------|-----|
| API 端點 | `https://api.groq.com/openai/v1/chat/completions` |
| 模型 | `llama-3.3-70b-versatile` |
| API Key | `YOUR_GROQ_API_KEY` |
| 溫度設置 | `0.7` |
| 最大令牌數 | `256` |

### **醫療關鍵字偵測**

本工作流程自動偵測以下中文字符，判斷訊息是否與醫療相關：

```
醫 藥 病 痛 診 癌 感 血 糖 壓 眠 頭 疼
```

如果訊息包含任何這些字符，自動路由到 Medical Prompt。

---

## ✅ 部署檢查清單

在開始前，確保完成以下所有項目：

- [ ] 進入 `/home/user/mcp-server` 目錄
- [ ] 運行 `git pull origin claude/line-family-comment-bot-Jzs7e`
- [ ] ngrok 正在運行（看到 Forwarding URL）
- [ ] n8n 正在運行（看到 Server started on port 5678）
- [ ] 瀏覽器能訪問 `http://localhost:5678`
- [ ] 刪除舊工作流程（避免 webhook 衝突）
- [ ] 導入 TELEGRAM_BOT_GROQ_DIRECT.json
- [ ] 配置 Call Groq API 節點中的 Groq API Key
- [ ] 啟用工作流程（Toggle 為綠色 🟢）
- [ ] 在 Telegram 中成功接收機器人回應

---

## 🔄 重新啟動服務

如需重新啟動 ngrok 或 n8n，請參考：
```
/home/user/mcp-server/line-family-comment-bot/RESTART_SERVICES.md
```

---

## 🆘 常見問題

### **問題 1：Call Groq API 節點顯示紅色錯誤**

**原因**：API Key 未正確設置或過期

**解決方案**：
1. 打開 Call Groq API 節點
2. 檢查 `Authorization` 欄位
3. 確保格式為：`Bearer YOUR_API_KEY`（注意 `Bearer ` 和空格）
4. 保存並重新啟動工作流程

---

### **問題 2：收不到機器人回應**

**檢查清單**：
1. ngrok 是否還在運行？（查看第一個 PowerShell 視窗）
2. n8n 是否還在運行？（查看第二個 PowerShell 視窗）
3. Toggle 是否為綠色（已啟用）？
4. Groq API Key 是否正確配置？

**除錯步驟**：
1. 點擊工作流程中的 **Execute Workflow** 按鈕手動測試
2. 查看 **Execution** 標籤查看錯誤信息
3. 檢查 ngrok 日誌是否收到 Telegram webhook

---

### **問題 3：Groq API 返回錯誤**

**常見錯誤信息**：
- `401 Unauthorized` → API Key 錯誤或過期
- `429 Too Many Requests` → API 速率限制
- `500 Internal Server Error` → Groq 服務暫時故障

**解決方案**：
1. 驗證 API Key 正確性
2. 等待 1 分鐘後重試（速率限制）
3. 檢查 Groq 服務狀態（https://status.groq.com）

---

### **問題 4：Webhook 路徑衝突錯誤**

**錯誤信息**：`Webhook already exists`

**解決方案**：
1. 刪除舊工作流程（見步驟 6）
2. 重新啟動 n8n（按 Ctrl+C 然後 `n8n start`）
3. 重新導入工作流程

---

## 📁 相關檔案位置

```
/home/user/mcp-server/line-family-comment-bot/
├── TELEGRAM_BOT_GROQ_DIRECT.json  ← 使用本檔案！
├── TELEGRAM_BOT_COMPLETE.json      (舊版本 - 有 credential 問題)
├── TELEGRAM_BOT_SIMPLE_FIXED.json  (簡化版本)
├── START_HERE.md                   (初始部署指南)
├── RESTART_SERVICES.md             (重啟服務指南)
├── FIX_WORKFLOW_ERROR.md           (修復錯誤指南)
├── WINDOWS_DEPLOYMENT.md           (Windows 部署指南)
├── DEPLOYMENT_RECORD.md            (部署紀錄參考)
└── GROQ_DIRECT_API_GUIDE.md        (本檔案)
```

---

## 🎓 為什麼要用 Groq 直接 API？

### **舊方法的問題**
- ❌ 需要在 n8n 配置 OpenAI 兼容 credential
- ❌ n8n 的 credential 設置複雜且容易出錯
- ❌ LLM 節點無法正確保存配置
- ❌ 手動配置多個 LLM 節點繁瑣

### **新方法的優勢**
- ✅ 直接 HTTP 呼叫，無需額外 credential 配置
- ✅ 工作流程內包含所有必要設置
- ✅ 更簡潔的節點結構
- ✅ 更容易除錯和修改

---

## 📞 快速參考

| 項目 | 值 |
|------|-----|
| 工作流程檔案 | TELEGRAM_BOT_GROQ_DIRECT.json |
| n8n 位址 | http://localhost:5678 |
| Groq API 端點 | https://api.groq.com/openai/v1/chat/completions |
| 模型 | llama-3.3-70b-versatile |
| Telegram Bot | @cozuesg_bot |
| Chat ID | 6119894493 |

---

**最後更新**：2026-05-21  
**建議使用**：本檔案為最新且推薦的部署方式

