# Windows 完整部署指南 - Telegram Family Bot

**狀態**: ✅ 所有測試完成，準備部署  
**核心邏輯測試**: 22/22 通過  
**API 集成測試**: 6/6 通過  

---

## 🚀 **完整部署流程（6 步驟）**

### **第 1 步：啟動 ngrok**

**打開第一個 PowerShell 視窗**，運行：

```powershell
ngrok http 5678
```

**預期結果**：
```
Forwarding                    https://outlet-oxford-clothing.ngrok-free.dev -> http://localhost:5678
```

✅ **保持此視窗開啟！不要關閉！**

---

### **第 2 步：啟動 n8n**

**打開第二個 PowerShell 視窗**，運行：

```powershell
npm run start
```

**預期結果**：
```
n8n ready on port 5678
Server started on port 5678
```

✅ **保持此視窗開啟！不要關閉！**

---

### **第 3 步：打開 n8n 儀表板**

在瀏覽器中打開：

```
http://localhost:5678
```

✅ **您應該看到 n8n 儀表板**

---

### **第 4 步：導入工作流程**

在 n8n 中：

1. 點擊 **+ New**
2. 選擇 **Import from file**
3. 選擇檔案：
   ```
   C:\Users\user\mcp-server\line-family-comment-bot\TELEGRAM_BOT_COMPLETE.json
   ```
4. 點擊 **Import**

✅ **工作流程應該出現在畫面上**

---

### **第 5 步：配置 Groq API Key**

1. 找到 **LLM Model - Chat** 節點
2. 點擊節點進行編輯
3. 輸入您的 Groq API Key（您的個人金鑰）
4. **Save**

5. 對 **LLM Model - Medical** 節點重複上述步驟

✅ **兩個 LLM 節點都應該配置完成**

---

### **第 6 步：啟用並測試**

1. 點擊右上角 **Toggle** (變綠色 🟢)
2. 在 Telegram 向 @cozuesg_bot 發送訊息
3. 機器人應該立即回應

✅ **部署完成！**

---

## 📁 **重要檔案位置**

| 項目 | 位置 |
|------|------|
| 工作流程 | `C:\Users\user\mcp-server\line-family-comment-bot\TELEGRAM_BOT_COMPLETE.json` |
| 本指南 | `C:\Users\user\mcp-server\line-family-comment-bot\WINDOWS_DEPLOYMENT.md` |

---

## ✅ **檢查清單**

- [ ] ngrok 已啟動（看到 Forwarding）
- [ ] n8n 已啟動（看到 Server started）
- [ ] 瀏覽器能訪問 http://localhost:5678
- [ ] 工作流程已導入
- [ ] Groq API Key 已配置
- [ ] Toggle 為綠色（已啟用）
- [ ] 在 Telegram 收到回應

---

**祝您部署順利！** 🚀
