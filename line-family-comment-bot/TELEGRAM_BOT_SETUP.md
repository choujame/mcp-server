# Telegram Bot 簡單部署指南

這是最簡單的部署方式，只需 3 個步驟！

## 📋 **您的配置資訊**

```
Telegram Token: 8982238347:AAEvvIrMe_o8XifY6LGxQPRLBGCNNHlQBRI
Chat ID: 6119894493
Ngrok URL: https://outlet-oxford-clothing.ngrok-free.dev
```

---

## 🚀 **3 步快速部署**

### **Step 1: 設定 Telegram Webhook（複製貼上）**

在 PowerShell 運行：

```powershell
$token = "8982238347:AAEvvIrMe_o8XifY6LGxQPRLBGCNNHlQBRI"
$url = "https://outlet-oxford-clothing.ngrok-free.dev/webhook/telegram"
$api = "https://api.telegram.org/bot$token/setWebhook?url=$url"
curl $api
```

應該顯示：`{"ok":true,"result":true}`

---

### **Step 2: 在 n8n 中建立簡單 Workflow**

**在 n8n 中：**

1. **點擊 "Create"** → **"New Workflow"**

2. **添加節點**：
   - **Webhook**（觸發器）
   - **Function**（處理訊息）
   - **Telegram Send Message**（發送回覆）

3. **配置 Webhook**：
   ```
   HTTP Method: POST
   Path: telegram
   Response Code: 200
   ```

4. **配置 Function 節點**：
   ```javascript
   return {
     message_id: $input.first().input.message.message_id,
     chat_id: $input.first().input.message.chat.id,
     text: "收到您的訊息！"
   };
   ```

5. **配置 Telegram Send Message**：
   ```
   Token: 8982238347:AAEvvIrMe_o8XifY6LGxQPRLBGCNNHlQBRI
   Chat ID: 6119894493
   Message: 你好！我收到了您的訊息
   ```

6. **保存並啟用**

---

### **Step 3: 測試**

1. **打開 Telegram**

2. **給您的 bot 發送訊息**

3. **應該會收到回覆**

4. **完成！** ✅

---

## ✅ **就這麼簡單！**

沒有複雜的配置，沒有 LINE Developers，只需 3 步就能運行一個工作的 Telegram bot。

---

## 🆘 **如果有問題**

### **503 或 502 錯誤？**
- 檢查 Ngrok 是否還在運行
- 檢查 n8n 是否在線
- 重新運行 Step 1 的 PowerShell 命令

### **沒有收到訊息？**
- 確保 Webhook 節點已啟用
- 確保整個 workflow 已啟用（綠色）
- 檢查 n8n Executions 日誌

### **收不到回覆？**
- 檢查 Telegram Token 是否正確
- 檢查 Chat ID 是否正確
- 查看 n8n Function 節點有無錯誤

---

## 💡 **優勢**

✅ 最簡單 - 只需 3 個節點  
✅ 最快 - 5 分鐘部署  
✅ 最可靠 - Telegram 比 LINE 簡單  
✅ 可擴展 - 之後可以添加更多功能

---

**現在就開始吧！** 👈

有任何問題隨時問我！
