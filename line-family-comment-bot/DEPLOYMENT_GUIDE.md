# LINE Family Comment Bot - 本地部署指南

这是一个完整的本地部署指南，指导您在 Windows 电脑上部署 LINE Family Comment Bot。

## 📋 前置要求

- ✅ Windows 10 或更新版本
- ✅ Node.js v16 或更新版本（[下载](https://nodejs.org/)）
- ✅ 互联网连接
- ✅ LINE 机器人的 credentials（已有：token、secret、channel ID）

## 🚀 快速部署（5 分钟）

### 方法 1：自动部署脚本（推荐）

1. **打开文件夹**
   ```
   在 Windows 中打开此项目的 line-family-comment-bot 文件夹
   ```

2. **运行部署脚本**
   ```
   双击：deploy-windows.bat
   ```

3. **等待完成**
   - n8n 会自动启动
   - 浏览器会打开 http://localhost:5678
   - 您会看到 n8n 的管理界面

### 方法 2：手动部署

如果脚本不工作，请手动执行以下步骤：

#### Step 1: 安装 n8n

打开 PowerShell（Win + X，选择 PowerShell）：

```powershell
npm install -g n8n
```

#### Step 2: 启动 n8n

```powershell
n8n start
```

n8n 会在 http://localhost:5678 启动

#### Step 3: 打开浏览器

访问 http://localhost:5678

---

## 🔧 配置步骤

现在 n8n 已经启动，您需要导入并配置 workflow：

### Step 1: 导入 Workflow

1. 在 n8n 首页，点击 **"Create"** 或 **"New Workflow"**
2. 点击 **"Import from File"**
3. 选择：`workflows/LINE_FAMILY_COMMENT_BOT.public.json`
4. 点击 **"Import"**

workflow 会被导入，您会看到所有的节点。

### Step 2: 配置 LINE Config 节点

1. 在 workflow 中找到 **"LINE Config"** 节点
2. 双击打开编辑
3. 填入以下信息（已为您准备）：

```json
{
  "CHANNEL_ACCESS_TOKEN": "YvG97w24JgWQK4knsCs+E/FdEOa8uYcqSxwzHJS+RSfMLv2A1FCB5hsUwIRFhKNAW2bIAJ4ZWc1wS1f1CJU0P3ymiqfww79I+wQtEr4L+rlj3MGA/OOnitS/dFEemkiCbWjob1J5d7itw68VFLKj8wdB04t89/1O/w1cDnyilFU=",
  "CHANNEL_SECRET": "0754be9c82f1ccfad2a4a65b669aa894",
  "CHANNEL_ID": "2009899010",
  "BOT_MENTION_NAME": "家庭分身",
  "BOT_PERSONA_NAME": "小明",
  "ELDER_A_DISPLAY_NAME": "媽媽",
  "ELDER_A_ADDRESS": "媽媽",
  "ELDER_B_DISPLAY_NAME": "爸爸",
  "ELDER_B_ADDRESS": "爸爸"
}
```

4. 点击 **"Save"**

### Step 3: 配置 LLM 节点

找到 workflow 中的 **"OpenAI-compatible Model"** 或 **"Chat"** 节点：

**使用 Groq（已配置）**：

1. 节点设置：
   - Base URL: `https://api.groq.com/openai/v1`
   - API Key: `YOUR_GROQ_API_KEY_HERE`
   - Model: `mixtral-8x7b-32768`

2. 点击 **"Save"**

**或者使用 LM Studio（如果您有）**：

1. 节点设置：
   - Base URL: `http://localhost:1234/v1`
   - API Key: `lm-studio`
   - Model: [您的模型名]

2. 点击 **"Save"**

### Step 4: 配置 Webhook

1. 找到 **"Webhook"** 节点
2. 点击 **"Execute"** 按钮
3. 复制 **"Production URL"**：
   ```
   https://...
   ```

4. **重要**：在 LINE Developers 中设置 Webhook URL
   - 访问：https://developers.line.biz/
   - 找到您的 Messaging API channel
   - 进入 **"Messaging API"** 设置
   - 粘贴 Production URL 到 **"Webhook URL"** 字段
   - 点击 **"Verify"** 测试连接

### Step 5: 配置记忆长度

1. 找到 **"Simple Memory"** 节点
2. 设置 `contextWindowLength` 为 `5`（推荐）
3. 点击 **"Save"**

### Step 6: 启用 Workflow

1. 点击 workflow 顶部的 **"Save"** 按钮
2. 点击 **"Active"** 切换（应该变成绿色）

现在 workflow 已启用！

---

## ✅ 测试

### 方法 1：LINE 好友测试（推荐）

1. 将 bot 添加为 LINE 好友
   - 点击 "Add Friend"
   - 搜索您的 bot（应该在 LINE Developers 中找到）

2. 发送测试消息：
   ```
   家庭分身 今天天气怎么样？
   ```

3. Bot 应该会回复

### 方法 2：n8n 测试

1. 在 n8n 中找到 **"Webhook"** 节点
2. 点击 **"Execute"** 测试 webhook
3. 查看执行日志

### 方法 3：检查 n8n 日志

如果有问题，查看 n8n 中的执行记录：

1. 点击 workflow 顶部的 **"Executions"**
2. 查看最近的执行记录
3. 点击行项查看详细日志

---

## 🐛 常见问题

### Q: n8n 无法启动
**A:** 
- 检查 Node.js 是否正确安装：`node --version`
- 检查端口 5678 是否被占用
- 尝试手动删除 n8n 数据：`rmdir %USERPROFILE%\.n8n` (Windows)

### Q: Webhook 验证失败
**A:**
- 确保 Channel Access Token 正确（没有多余空格）
- 确保 Webhook URL 正确（来自 n8n Production URL）
- 在 LINE Developers 中点击 "Verify" 测试

### Q: Bot 不回应消息
**A:**
- 检查 workflow 是否启用（应该显示绿色 "Active"）
- 检查 LLM API key 是否正确
- 查看 n8n 执行日志找错误
- 确保消息包含 bot 名字（"家庭分身"）

### Q: "Groq API key invalid" 错误
**A:**
- 确保 API key 完整且正确，并且没有多余的空格
- 检查是否有过期或速率限制
- 访问 https://console.groq.com/ 验证 key

### Q: 如何停止 n8n？
**A:**
- 关闭 n8n 的 PowerShell 窗口（按 Ctrl+C）
- 或在浏览器中点击左上角菜单 → "Settings" → 关闭

---

## 🔐 安全提醒

⚠️ **重要**：

- ✅ 这些 credentials 只存储在您的本地电脑
- ✅ 不要把 .env 或配置提交到 Git
- ✅ 不要在公开地方分享 Channel Secret 或 API keys
- ✅ 定期检查 LINE Developers 中的日志
- ✅ 如果 credentials 泄露，立即在 LINE Developers 中重生成

---

## 📱 加入家庭群组

在个人好友测试成功后，您可以：

1. 创建一个 LINE 群组
2. 将 bot 添加到群组
3. 在群组中测试 bot
4. 调整 bot 的回复频率（在 workflow 中）

---

## 🎯 下一步

1. ✅ 完成上述所有步骤
2. ✅ 作为 LINE 好友充分测试
3. ✅ 加入家庭群组并监控
4. ✅ 根据需要调整 bot 的性格和回复

---

## 💡 高级配置

### 修改 Bot 性格

在 workflow 中编辑 System Prompt：
```
你是一个温和、尊重的家庭聊天机器人。
你的名字是 {{BOT_MENTION_NAME}}。
你要回应家人的日常对话...
```

### 更改记忆长度

在 "Simple Memory" 节点中修改 `contextWindowLength`：
- 0-2：最省资源
- 3-5：想省 token
- 5-10：推荐值
- >10：不推荐

### 使用不同的 LLM

替换 LLM 节点配置：
- LM Studio：`http://localhost:1234/v1`
- Google Gemini：使用 Google Gemini 节点
- OpenRouter：`https://api.openrouter.ai/v1`

---

## 📚 相关文档

- `docs/troubleshooting.md` - 更详细的故障排除
- `docs/setup-n8n.md` - n8n 详细指南
- `docs/setup-llm.md` - LLM 选项详解
- `DEVELOPER_GUIDE.md` - 开发者指南

---

## 🆘 获取帮助

如果遇到问题：

1. 查看 "常见问题" 部分
2. 查看 `docs/troubleshooting.md`
3. 检查 n8n 执行日志
4. 查看 LINE Developers 的 webhook 日志

---

**祝您部署成功！** 🎉

如有任何问题，请参考相关文档或查看日志以获取更多信息。
