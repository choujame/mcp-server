# 🔄 重新啟動服務指南 - ngrok 和 n8n

**目的**: 在部署過程中重新啟動 ngrok 和 n8n 服務  
**適用情況**: 修改工作流程後、修復錯誤後、或服務無回應時

---

## ⏹️ **第 1 步：停止 ngrok**

### **在第一個 PowerShell 視窗中**

按下鍵盤組合：
```
Ctrl + C
```

**預期結果**：
```
^C
[error] Connection refused
ngrok tunnel session ended
```

✅ **ngrok 已停止**

---

## ⏹️ **第 2 步：停止 n8n**

### **在第二個 PowerShell 視窗中**

按下鍵盤組合：
```
Ctrl + C
```

**預期結果**：
```
^C
Shutting down...
Server stopped
```

✅ **n8n 已停止**

---

## 🚀 **第 3 步：重新啟動 ngrok**

### **在第一個 PowerShell 視窗中**

執行命令：
```powershell
ngrok http 5678
```

**等待看到**：
```
Session Status                online
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://outlet-oxford-clothing.ngrok-free.dev -> http://localhost:5678
```

✅ **ngrok 已重新啟動**

---

## 🚀 **第 4 步：重新啟動 n8n**

### **在第二個 PowerShell 視窗中**

執行命令：
```powershell
n8n start
```

**等待看到**：
```
n8n ready on http://localhost:5678
Server started on port 5678
```

✅ **n8n 已重新啟動**

---

## ✅ **第 5 步：驗證服務運行**

### **檢查清單**

- [ ] 第一個 PowerShell 視窗：ngrok 顯示 "Forwarding" 且為綠色
- [ ] 第二個 PowerShell 視窗：n8n 顯示 "Server started on port 5678"
- [ ] 在瀏覽器中訪問 `http://localhost:5678`（應該看到 n8n 儀表板）

✅ **兩個服務都已成功重新啟動**

---

## 📋 **完整重新啟動流程（快速參考）**

| 步驟 | 操作 | 預期結果 |
|------|------|--------|
| 1 | 在第一個 PowerShell 按 Ctrl+C | ngrok 停止 |
| 2 | 在第二個 PowerShell 按 Ctrl+C | n8n 停止 |
| 3 | 在第一個 PowerShell 執行 `ngrok http 5678` | 看到 Forwarding URL |
| 4 | 在第二個 PowerShell 執行 `n8n start` | 看到 Server started |
| 5 | 驗證兩個服務都在運行 | 可以訪問 http://localhost:5678 |

---

## 🔄 **何時需要重新啟動**

### **修復工作流程錯誤後**
按照 `FIX_WORKFLOW_ERROR.md` 中的步驟完成後，需要重新啟動這兩個服務，然後導入修復的工作流程。

### **修改 n8n 工作流程後**
如果在 n8n 儀表板中修改了工作流程或配置，重新啟動可以確保所有變更都已生效。

### **服務無回應**
如果 ngrok 或 n8n 無法正常工作，重新啟動通常能解決問題。

### **長時間運行後**
在長期運行後重新啟動服務可以確保系統穩定性。

---

## 🔗 **相關文檔**

| 文件 | 用途 |
|------|------|
| `START_HERE.md` | 初始部署指南 |
| `FIX_WORKFLOW_ERROR.md` | 修復工作流程錯誤 |
| `RESTART_SERVICES.md` | **本文件** - 重新啟動服務 |
| `WINDOWS_DEPLOYMENT.md` | 簡略部署指南 |

---

## ⚠️ **常見問題**

### **Ctrl+C 無反應**
→ 連續按 2-3 次 Ctrl+C  
→ 或關閉 PowerShell 視窗並打開新視窗

### **重新啟動後 ngrok 或 n8n 無法啟動**
→ 檢查埠 5678 是否被其他程序佔用  
→ 如果是，需要結束該程序或更改埠號

### **ngrok 的 Forwarding URL 改變了**
→ 這是正常現象。每次重新啟動時，ngrok 會分配一個新的 URL  
→ 如果使用新的 URL，需要更新 Telegram Bot Webhook 設定

### **http://localhost:5678 無法訪問**
→ 確認 n8n 已完全啟動（看到 "Server started on port 5678"）  
→ 等待 10-15 秒後再嘗試  
→ 刷新瀏覽器 (按 F5)

---

## ✨ **完全重新啟動流程（包含工作流程修復）**

1. **停止服務**
   ```
   第一個 PowerShell：Ctrl+C (停止 ngrok)
   第二個 PowerShell：Ctrl+C (停止 n8n)
   ```

2. **重新啟動服務**
   ```
   第一個 PowerShell：ngrok http 5678
   第二個 PowerShell：n8n start
   ```

3. **驗證服務**
   ```
   - 檢查 ngrok 的 Forwarding URL
   - 檢查 n8n 的 Server started 訊息
   - 在瀏覽器訪問 http://localhost:5678
   ```

4. **修復工作流程**（如果需要）
   ```
   按照 FIX_WORKFLOW_ERROR.md 中的步驟進行
   ```

5. **測試工作流程**
   ```
   在 Telegram 中向機器人發送訊息
   確認收到回應
   ```

✅ **全部完成 = 服務已成功重新啟動！**

---

## 📁 **文件位置**

| 項目 | 位置 |
|------|------|
| 本重新啟動指南 | `C:\Users\user\mcp-server\line-family-comment-bot\RESTART_SERVICES.md` |
| 工作流程文件 | `C:\Users\user\mcp-server\line-family-comment-bot\TELEGRAM_BOT_COMPLETE.json` |
| 修復錯誤指南 | `C:\Users\user\mcp-server\line-family-comment-bot\FIX_WORKFLOW_ERROR.md` |
| 部署指南 | `C:\Users\user\mcp-server\line-family-comment-bot\START_HERE.md` |

---

**記住**: 
- ✅ 總是有兩個 PowerShell 視窗同時開啟
- ✅ 重新啟動前確認已停止舊的服務
- ✅ 等待新的服務完全啟動後再進行下一步
- ✅ 按照文檔中的預期結果進行驗證

**祝您重新啟動順利！** 🚀
