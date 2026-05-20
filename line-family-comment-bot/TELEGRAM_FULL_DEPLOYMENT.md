# Telegram Family Bot - 完整功能部署指南

這是一個**功能完整的家庭 Telegram 機器人**，包含所有高級功能！

---

## ✨ **包含的功能**

✅ **對話記憶** - 記住最近的對話上下文  
✅ **LLM 整合** - 使用 Groq AI 智能回覆  
✅ **圖片理解** - 可以識別和分析圖片  
✅ **智能判斷** - 判斷是否需要回覆（避免過度回覆）  
✅ **醫療搜尋** - 健康相關諮詢  
✅ **溫暖語氣** - 像真人一樣溫和地回應  

---

## 🚀 **快速部署（10 分鐘）**

### **Step 1: 設定 Webhook**

在 PowerShell 運行：

```powershell
$token="8982238347:AAEvvIrMe_o8XifY6LGxQPRLBGCNNHlQBRI";$url="https://outlet-oxford-clothing.ngrok-free.dev/webhook/telegram";$api="https://api.telegram.org/bot$token/setWebhook?url=$url";curl $api
```

結果應該是：`{"ok":true,"result":true}` ✓

---

### **Step 2: 匯入完整 Workflow**

在 n8n 中：

1. **點擊 "Create"** → **"New Workflow"**
2. **點擊菜單** → **"Import"**
3. **選擇檔案**：`TELEGRAM_BOT_FULL.json`
4. **等待匯入完成**

---

### **Step 3: 配置關鍵參數**

匯入後，需要配置這些節點：

#### **LLM Chat 節點**

檢查這些參數是否正確：

```json
{
  "model": "mixtral-8x7b-32768",
  "baseUrl": "https://api.groq.com/openai/v1",
  "apiKey": "YOUR_GROQ_API_KEY"
}
```

**如果需要修改**：
- 雙擊 "LLM Chat" 節點
- 檢查 Model、Base URL、API Key

#### **Send Telegram Message 節點**

```json
{
  "token": "8982238347:AAEvvIrMe_o8XifY6LGxQPRLBGCNNHlQBRI",
  "chatId": "6119894493"
}
```

---

### **Step 4: 啟用並測試**

1. **點擊 "Save"** 保存 workflow
2. **點擊啟用**（綠色開關）
3. **打開 Telegram**
4. **給 bot 發送訊息**
5. **應該收到智能回覆！** ✅

---

## 🔧 **完整功能說明**

### **1. 對話記憶（Simple Memory）**

```
Bot 會記住最近的對話，理解上下文。

例：
您: 我今天不舒服
Bot: 請告訴我您哪裡不舒服

您: 頭疼
Bot: 我很遺憾聽說您頭疼。建議...
```

**配置**：已內置，記憶長度為 5 條訊息

### **2. LLM 整合（Groq）**

```
使用 Groq 的 Mixtral 模型進行智能回覆

特點：
- 快速回應
- 支援長文本
- 理解中文和英文
- 免費額度充足
```

**如果要換 LLM**：
- Google Gemini：改 baseUrl 和 model
- OpenRouter：改 apiKey 和 baseUrl
- LM Studio（本地）：baseUrl: `http://localhost:1234/v1`

### **3. 智能判斷（Intent Judge）**

```
根據關鍵詞判斷是否需要回覆

觸發回覆的情況：
- 包含問候詞（你好、早、晚等）
- 包含求助詞（幫助、醫生、症狀等）
- 訊息長度超過 3 個字

避免過度回覆，只在有意義的時候才回應
```

### **4. 訊息解析（Parse Message）**

```
提取訊息資訊：
- 聊天 ID
- 用戶名
- 訊息內容
- 是否有圖片
- 時間戳
```

### **5. 對話記錄**

```
訊息格式：
您: [用戶輸入的訊息]

家庭助手: [AI 的回覆]

這樣可以清楚地看到對話流程
```

---

## ⚙️ **高級配置**

### **修改回覆風格**

在 LLM Chat 節點的 System Prompt 中修改：

```
預設：
"你是一個溫和、尊重的家庭聊天機器人。用簡潔、自然的語言回應。"

可以改為：
"你是一個年輕的家庭成員，用活潑的語氣回應。"
或
"你是一個專業的醫療諮詢顧問。"
```

### **修改回覆條件**

在 Intent Judge 節點中修改關鍵詞：

```javascript
const keywords = ['你好', '早', '晚', '醫生', '症狀', '疼', '不舒服'];
// 添加或刪除關鍵詞來改變觸發條件
```

### **修改記憶長度**

在 Simple Memory 節點中設置 `contextWindowLength`：

```
推薦值：
- 5：標準（平衡效能和記憶）
- 3：省資源
- 10：更長的對話歷史
```

---

## 🆘 **故障排除**

### **問題 1: 502 Bad Gateway**

**原因**：n8n 崩潰或沒有回應  
**解決**：
```
1. 檢查 n8n 是否在運行
2. 查看 Executions 日誌中的錯誤
3. 重啟 n8n 服務
4. 查看 console 中的錯誤訊息
```

### **問題 2: 沒有收到回覆**

**原因**：Workflow 沒有啟用或有錯誤  
**解決**：
```
1. 確保 Workflow 啟用（綠色開關）
2. 在 Telegram 中發送更明確的訊息（包含關鍵詞）
3. 檢查 Intent Judge 的條件
4. 查看 Executions 中的執行記錄
```

### **問題 3: Groq 返回錯誤**

**原因**：API Key 無效或額度用完  
**解決**：
```
1. 確認 API Key 正確
2. 訪問 https://console.groq.com/ 檢查額度
3. 換用其他 LLM（Google Gemini 或本地 LM Studio）
4. 減少對話歷史長度以節省 tokens
```

### **問題 4: Telegram 訊息沒有發出**

**原因**：Token 或 Chat ID 錯誤  
**解決**：
```
1. 確認 Token: 8982238347:AAEvvIrMe...（前面）
2. 確認 Chat ID: 6119894493
3. 確保沒有多餘空格
4. 重新運行 webhook 設定命令
```

---

## 💡 **使用提示**

### **最佳實踐**

✅ 先在個人 Telegram 測試  
✅ 定期檢查 API 額度  
✅ 調整回覆關鍵詞以避免過度回覆  
✅ 保持 ngrok 一直運行  
✅ 定期查看 Executions 日誌  

### **自訂建議**

想要個性化？可以：
- 改變 bot 的性格（在 System Prompt）
- 添加新的關鍵詞觸發
- 整合其他服務（天氣、新聞等）
- 添加命令支援（/start, /help）
- 記錄對話到資料庫

---

## 📊 **工作流程圖**

```
用戶發送訊息
    ↓
Webhook 接收
    ↓
解析訊息（用戶名、內容、時間）
    ↓
Simple Memory 獲取對話歷史
    ↓
Intent Judge 判斷是否需要回覆
    ↓（是）
LLM Chat 生成智能回覆
    ↓
Send Telegram Message 發送回覆
    ↓
用戶收到回覆 ✅
```

---

## ✨ **完成！**

您現在有一個**完全功能的智能 Telegram 家庭機器人**！

支援：
- 🧠 記憶對話上下文
- 🤖 AI 智能回覆
- 💭 理解自然語言
- 🎯 智能判斷回覆時機
- 📱 隨時隨地聊天

---

**有任何問題或想要調整，隨時告訴我！** 🚀
