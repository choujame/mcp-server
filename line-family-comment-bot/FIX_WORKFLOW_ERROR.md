# 🔧 修復工作流程錯誤指南

**問題**: Normal Chat Agent 節點顯示紅色警告  
**原因**: 節點引用了 Telegram Config，但沒有正確連接  
**解決方案**: 已在 TELEGRAM_BOT_COMPLETE.json 中修正

---

## ✅ **修復已完成**

工作流程檔案已修改，移除了對 Telegram Config 的不必要引用。

---

## 📋 **重新導入修復後的工作流程（3 步驟）**

### **第 1 步：更新本地檔案**

在 PowerShell 中執行：

```powershell
cd C:\Users\user\mcp-server
git pull origin claude/line-family-comment-bot-Jzs7e
```

**預期結果**：
```
Updating xxxxx..xxxxx
1 file changed: TELEGRAM_BOT_COMPLETE.json
```

✅ **確認看到更新訊息**

---

### **第 2 步：刪除有錯誤的工作流程**

在 n8n 儀表板中：

1. **點擊左上角 Menu（三條線）**

2. **選擇 Delete**

3. **確認刪除**

✅ **舊工作流程已刪除**

---

### **第 3 步：重新導入修復後的工作流程**

在 n8n 儀表板中：

1. **點擊 + New**

2. **選擇 Import from file**

3. **在文件選擇對話中，選擇此檔案**：
   ```
   C:\Users\user\mcp-server\line-family-comment-bot\TELEGRAM_BOT_COMPLETE.json
   ```

4. **點擊 Open 或 Import**

5. **等待導入完成**

✅ **工作流程應該導入成功，沒有紅色警告**

---

## 🔑 **第 4 步：重新配置 API Key**

導入完成後，需要重新配置兩個 LLM 節點：

### **配置 LLM Model - Chat**

1. **點擊 LLM Model - Chat 節點**

2. **在右側詳情面板中，填入**：
   - **Base URL**: `https://api.groq.com/openai/v1`
   - **API Key**: `YOUR_GROQ_API_KEY`（您的 Groq API 密鑰）

3. **點擊 Save**

### **配置 LLM Model - Medical**

1. **點擊 LLM Model - Medical 節點**

2. **重複上述步驟**

✅ **兩個 LLM 節點都應該配置完成，沒有紅色警告**

---

## 🟢 **第 5 步：啟用工作流程**

1. **點擊右上角 Toggle 開關**

2. **應該變成綠色 🟢**

3. **確認看到訊息 "Workflow is active"**

✅ **工作流程已啟用！**

---

## 💬 **第 6 步：測試機器人**

1. **打開 Telegram**

2. **找到 @cozuesg_bot**

3. **發送訊息**：
   ```
   你好
   ```

4. **機器人應該立即回應**

✅ **部署完成！**

---

## 📁 **檔案位置**

| 項目 | 位置 |
|------|------|
| 修復後的工作流程 | `C:\Users\user\mcp-server\line-family-comment-bot\TELEGRAM_BOT_COMPLETE.json` |
| 本修復指南 | `C:\Users\user\mcp-server\line-family-comment-bot\FIX_WORKFLOW_ERROR.md` |

---

## ⚠️ **如果還有問題**

如果重新導入後還是有紅色警告：

1. **檢查是否完全刪除了舊工作流程**
2. **刷新瀏覽器** (按 F5)
3. **重新導入**

如果仍然有問題，請檢查：
- API Key 是否正確
- Base URL 是否正確：`https://api.groq.com/openai/v1`

---

## ✅ **修復步驟總結**

```
1. git pull origin claude/line-family-comment-bot-Jzs7e
2. 刪除 n8n 中的舊工作流程
3. 導入修復後的 TELEGRAM_BOT_COMPLETE.json
4. 配置兩個 LLM Model 節點的 API Key
5. 啟用工作流程
6. 在 Telegram 中測試
```

**全部完成 = 部署成功！** 🚀

---

**祝您修復順利！** 🎉
