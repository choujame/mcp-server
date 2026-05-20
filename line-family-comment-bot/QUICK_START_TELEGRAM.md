# ⚡ Telegram Bot 一頁紙快速開始

**總共只需 5 分鐘！**

---

## 🎯 **您已經準備好的東西**

✅ n8n 已啟動（localhost:5678）  
✅ Ngrok 已運行（outlet-oxford-clothing.ngrok-free.dev）  
✅ Telegram Token 和 Chat ID 已有  

---

## 📋 **3 個命令 + 2 分鐘配置**

### **命令 1：設定 Telegram Webhook**

複製貼上到 PowerShell：

```powershell
$token="8982238347:AAEvvIrMe_o8XifY6LGxQPRLBGCNNHlQBRI";$url="https://outlet-oxford-clothing.ngrok-free.dev/webhook/telegram";$api="https://api.telegram.org/bot$token/setWebhook?url=$url";curl $api
```

**等待顯示**：`{"ok":true,"result":true}` ✓

---

## 🔧 **配置 2：匯入 Workflow（複製 JSON）**

### **在 n8n 中**：

1. 點擊 **"Create"** → **"New Workflow"**
2. 點擊菜單 → **"Import"**
3. 選擇檔案：**TELEGRAM_BOT_SIMPLE.json**
4. 等待匯入完成

### **或者手動建立**（3 個節點，2 分鐘）：

**節點 1：Webhook**
- HTTP Method: `POST`
- Path: `telegram`

**節點 2：Function**（可選，只是顯示訊息）
- 直接連到節點 3

**節點 3：Telegram Send Message**
- Token: `8982238347:AAEvvIrMe_o8XifY6LGxQPRLBGCNNHlQBRI`
- Chat ID: `6119894493`
- Message: `你好！我收到您的訊息`

連接順序：Webhook → Function → Telegram Send Message

---

## ✅ **配置 3：啟用並測試**

1. **保存 Workflow**
2. **點擊啟用**（變綠色）
3. **打開 Telegram**
4. **給 bot 發送任意訊息**
5. **應該立即收到回覆！** ✅

---

## 🎉 **完成！**

您現在有一個**完全工作的 Telegram 聊天機器人**！

---

## 📱 **下一步（可選）**

想要更複雜的功能？添加：
- ✨ 命令處理（/start, /help）
- 🤖 AI 整合（Groq）
- 💾 訊息記錄
- 🔍 關鍵字識別

---

## 🆘 **遇到問題？**

| 問題 | 解決 |
|------|------|
| **502 錯誤** | 檢查 Ngrok 是否運行：`.\ngrok.exe http 5678` |
| **沒有收到回覆** | 確保 Workflow 啟用（綠色開關） |
| **Telegram 返回錯誤** | 檢查 Token 和 Chat ID 是否正確 |
| **Webhook 驗證失敗** | 重新運行命令 1 的 PowerShell 命令 |

---

**就這麼簡單！現在就試試吧！** 🚀
