# Telegram Bot 简单部署指南

这是最简单的部署方式，只需 3 个步骤！

## 📋 **您的配置信息**

```
Telegram Token: 8982238347:AAEvvIrMe_o8XifY6LGxQPRLBGCNNHlQBRI
Chat ID: 6119894493
Ngrok URL: https://outlet-oxford-clothing.ngrok-free.dev
```

---

## 🚀 **3 步快速部署**

### **Step 1: 设置 Telegram Webhook（复制粘贴）**

在 PowerShell 运行：

```powershell
$token = "8982238347:AAEvvIrMe_o8XifY6LGxQPRLBGCNNHlQBRI"
$url = "https://outlet-oxford-clothing.ngrok-free.dev/webhook/telegram"
$api = "https://api.telegram.org/bot$token/setWebhook?url=$url"
curl $api
```

应该显示：`{"ok":true,"result":true}`

---

### **Step 2: 在 n8n 中创建简单 Workflow**

**在 n8n 中：**

1. **点击 "Create"** → **"New Workflow"**

2. **添加节点**：
   - **Webhook**（触发器）
   - **Function**（处理消息）
   - **Telegram Send Message**（发送回复）

3. **配置 Webhook**：
   ```
   HTTP Method: POST
   Path: telegram
   Response Code: 200
   ```

4. **配置 Function 节点**：
   ```javascript
   return {
     message_id: $input.first().input.message.message_id,
     chat_id: $input.first().input.message.chat.id,
     text: "收到您的消息！"
   };
   ```

5. **配置 Telegram Send Message**：
   ```
   Token: 8982238347:AAEvvIrMe_o8XifY6LGxQPRLBGCNNHlQBRI
   Chat ID: 6119894493
   Message: 你好！我收到了您的消息
   ```

6. **保存并启用**

---

### **Step 3: 测试**

1. **打开 Telegram**

2. **给您的 bot 发送消息**

3. **应该会收到回复**

4. **完成！** ✅

---

## ✅ **就这么简单！**

没有复杂的配置，没有 LINE Developers，只需 3 步就能运行一个工作的 Telegram bot。

---

## 🆘 **如果有问题**

### **503 或 502 错误？**
- 检查 Ngrok 是否还在运行
- 检查 n8n 是否在线
- 重新运行 Step 1 的 PowerShell 命令

### **没有收到消息？**
- 确保 Webhook 节点已启用
- 确保整个 workflow 已启用（绿色）
- 检查 n8n Executions 日志

### **收不到回复？**
- 检查 Telegram Token 是否正确
- 检查 Chat ID 是否正确
- 查看 n8n Function 节点有无错误

---

## 💡 **优势**

✅ 最简单 - 只需 3 个节点  
✅ 最快 - 5 分钟部署  
✅ 最可靠 - Telegram 比 LINE 简单  
✅ 可扩展 - 之后可以添加更多功能

---

**现在就开始吧！** 👈

有任何问题随时问我！
