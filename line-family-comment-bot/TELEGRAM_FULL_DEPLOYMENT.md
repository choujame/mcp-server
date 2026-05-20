# Telegram Family Bot - 完整功能部署指南

这是一个**功能完整的家庭 Telegram 机器人**，包含所有高级功能！

---

## ✨ **包含的功能**

✅ **对话记忆** - 记住最近的对话上下文  
✅ **LLM 集成** - 使用 Groq AI 智能回复  
✅ **图片理解** - 可以识别和分析图片  
✅ **智能判断** - 判断是否需要回复（避免过度回复）  
✅ **医疗搜索** - 健康相关咨询  
✅ **温暖语气** - 像真人一样温和地回应  

---

## 🚀 **快速部署（10 分钟）**

### **Step 1: 设置 Webhook**

在 PowerShell 运行：

```powershell
$token="8982238347:AAEvvIrMe_o8XifY6LGxQPRLBGCNNHlQBRI";$url="https://outlet-oxford-clothing.ngrok-free.dev/webhook/telegram";$api="https://api.telegram.org/bot$token/setWebhook?url=$url";curl $api
```

结果应该是：`{"ok":true,"result":true}` ✓

---

### **Step 2: 导入完整 Workflow**

在 n8n 中：

1. **点击 "Create"** → **"New Workflow"**
2. **点击菜单** → **"Import"**
3. **选择文件**：`TELEGRAM_BOT_FULL.json`
4. **等待导入完成**

---

### **Step 3: 配置关键参数**

导入后，需要配置这些节点：

#### **LLM Chat 节点**

检查这些参数是否正确：

```json
{
  "model": "mixtral-8x7b-32768",
  "baseUrl": "https://api.groq.com/openai/v1",
  "apiKey": "YOUR_GROQ_API_KEY"
}
```

**如果需要修改**：
- 双击 "LLM Chat" 节点
- 检查 Model、Base URL、API Key

#### **Send Telegram Message 节点**

```json
{
  "token": "8982238347:AAEvvIrMe_o8XifY6LGxQPRLBGCNNHlQBRI",
  "chatId": "6119894493"
}
```

---

### **Step 4: 启用并测试**

1. **点击 "Save"** 保存 workflow
2. **点击启用**（绿色开关）
3. **打开 Telegram**
4. **给 bot 发送消息**
5. **应该收到智能回复！** ✅

---

## 🔧 **完整功能说明**

### **1. 对话记忆（Simple Memory）**

```
Bot 会记住最近的对话，理解上下文。

例：
您: 我今天不舒服
Bot: 请告诉我您哪里不舒服

您: 头疼
Bot: 我很遗憾听说您头疼。建议...
```

**配置**：已内置，记忆长度为 5 条消息

### **2. LLM 集成（Groq）**

```
使用 Groq 的 Mixtral 模型进行智能回复

特点：
- 快速响应
- 支持长文本
- 理解中文和英文
- 免费额度充足
```

**如果要换 LLM**：
- Google Gemini：改 baseUrl 和 model
- OpenRouter：改 apiKey 和 baseUrl
- LM Studio（本地）：baseUrl: `http://localhost:1234/v1`

### **3. 智能判断（Intent Judge）**

```
根据关键词判断是否需要回复

触发回复的情况：
- 包含问候词（你好、早、晚等）
- 包含求助词（帮助、医生、症状等）
- 消息长度超过 3 个字

避免过度回复，只在有意义的时候才回应
```

### **4. 消息解析（Parse Message）**

```
提取消息信息：
- 聊天 ID
- 用户名
- 消息内容
- 是否有图片
- 时间戳
```

### **5. 对话记录**

```
消息格式：
您: [用户输入的消息]

家庭助手: [AI 的回复]

这样可以清楚地看到对话流程
```

---

## ⚙️ **高级配置**

### **修改回复风格**

在 LLM Chat 节点的 System Prompt 中修改：

```
默认：
"你是一个温和、尊重的家庭聊天机器人。用简洁、自然的语言回应。"

可以改为：
"你是一个年轻的家庭成员，用活泼的语气回应。"
或
"你是一个专业的医疗咨询顾问。"
```

### **修改回复条件**

在 Intent Judge 节点中修改关键词：

```javascript
const keywords = ['你好', '早', '晚', '医生', '症状', '疼', '不舒服'];
// 添加或删除关键词来改变触发条件
```

### **修改记忆长度**

在 Simple Memory 节点中设置 `contextWindowLength`：

```
推荐值：
- 5：标准（平衡性能和记忆）
- 3：省资源
- 10：更长的对话历史
```

---

## 🆘 **故障排除**

### **问题 1: 502 Bad Gateway**

**原因**：n8n 崩溃或没有响应  
**解决**：
```
1. 检查 n8n 是否在运行
2. 查看 Executions 日志中的错误
3. 重启 n8n 服务
4. 查看 console 中的错误信息
```

### **问题 2: 没有收到回复**

**原因**：Workflow 没有启用或有错误  
**解决**：
```
1. 确保 Workflow 启用（绿色开关）
2. 在 Telegram 中发送更明确的消息（包含关键词）
3. 检查 Intent Judge 的条件
4. 查看 Executions 中的执行记录
```

### **问题 3: Groq 返回错误**

**原因**：API Key 无效或额度用完  
**解决**：
```
1. 确认 API Key 正确
2. 访问 https://console.groq.com/ 检查额度
3. 换用其他 LLM（Google Gemini 或本地 LM Studio）
4. 减少对话历史长度以节省 tokens
```

### **问题 4: Telegram 消息没有发出**

**原因**：Token 或 Chat ID 错误  
**解决**：
```
1. 确认 Token: 8982238347:AAEvvIrMe...（前面）
2. 确认 Chat ID: 6119894493
3. 确保没有多余空格
4. 重新运行 webhook 设置命令
```

---

## 💡 **使用提示**

### **最佳实践**

✅ 先在个人 Telegram 测试  
✅ 定期检查 API 额度  
✅ 调整回复关键词以避免过度回复  
✅ 保持 ngrok 一直运行  
✅ 定期查看 Executions 日志  

### **自定义建议**

想要个性化？可以：
- 改变 bot 的性格（在 System Prompt）
- 添加新的关键词触发
- 集成其他服务（天气、新闻等）
- 添加命令支持（/start, /help）
- 记录对话到数据库

---

## 📊 **工作流程图**

```
用户发送消息
    ↓
Webhook 接收
    ↓
解析消息（用户名、内容、时间）
    ↓
Simple Memory 获取对话历史
    ↓
Intent Judge 判断是否需要回复
    ↓（是）
LLM Chat 生成智能回复
    ↓
Send Telegram Message 发送回复
    ↓
用户收到回复 ✅
```

---

## ✨ **完成！**

您现在有一个**完全功能的智能 Telegram 家庭机器人**！

支持：
- 🧠 记忆对话上下文
- 🤖 AI 智能回复
- 💭 理解自然语言
- 🎯 智能判断回复时机
- 📱 随时随地聊天

---

**有任何问题或想要调整，随时告诉我！** 🚀
