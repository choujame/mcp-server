# ⚡ Telegram Bot 一页纸快速开始

**总共只需 5 分钟！**

---

## 🎯 **您已经准备好的东西**

✅ n8n 已启动（localhost:5678）  
✅ Ngrok 已运行（outlet-oxford-clothing.ngrok-free.dev）  
✅ Telegram Token 和 Chat ID 已有  

---

## 📋 **3 个命令 + 2 分钟配置**

### **命令 1：设置 Telegram Webhook**

复制粘贴到 PowerShell：

```powershell
$token="8982238347:AAEvvIrMe_o8XifY6LGxQPRLBGCNNHlQBRI";$url="https://outlet-oxford-clothing.ngrok-free.dev/webhook/telegram";$api="https://api.telegram.org/bot$token/setWebhook?url=$url";curl $api
```

**等待显示**：`{"ok":true,"result":true}` ✓

---

## 🔧 **配置 2：导入 Workflow（复制 JSON）**

### **在 n8n 中**：

1. 点击 **"Create"** → **"New Workflow"**
2. 点击菜单 → **"Import"**
3. 选择文件：**TELEGRAM_BOT_SIMPLE.json**
4. 等待导入完成

### **或者手动创建**（3 个节点，2 分钟）：

**节点 1：Webhook**
- HTTP Method: `POST`
- Path: `telegram`

**节点 2：Function**（可选，只是显示消息）
- 直接连到节点 3

**节点 3：Telegram Send Message**
- Token: `8982238347:AAEvvIrMe_o8XifY6LGxQPRLBGCNNHlQBRI`
- Chat ID: `6119894493`
- Message: `你好！我收到您的消息`

连接顺序：Webhook → Function → Telegram Send Message

---

## ✅ **配置 3：启用并测试**

1. **保存 Workflow**
2. **点击启用**（变绿色）
3. **打开 Telegram**
4. **给 bot 发送任意消息**
5. **应该立即收到回复！** ✅

---

## 🎉 **完成！**

您现在有一个**完全工作的 Telegram 聊天机器人**！

---

## 📱 **下一步（可选）**

想要更复杂的功能？添加：
- ✨ 命令处理（/start, /help）
- 🤖 AI 集成（Groq）
- 💾 消息记录
- 🔍 关键字识别

---

## 🆘 **遇到问题？**

| 问题 | 解决 |
|------|------|
| **502 错误** | 检查 Ngrok 是否运行：`.\ngrok.exe http 5678` |
| **没有收到回复** | 确保 Workflow 启用（绿色开关） |
| **Telegram 返回错误** | 检查 Token 和 Chat ID 是否正确 |
| **Webhook 验证失败** | 重新运行命令 1 的 PowerShell 命令 |

---

**就这么简单！现在就试试吧！** 🚀
