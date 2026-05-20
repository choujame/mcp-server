# LINE Family Comment Bot - MCP Server Integration Guide

这是一个完整的指南，说明如何在 mcp-server 中集成和使用 LINE Family Comment Bot。

## 📋 概述

LINE Family Comment Bot 是一个基于 n8n 的智能家庭聊天机器人，可以：

- 在家庭 LINE 群组中进行温和、自然的对话
- 支持文字和图片理解
- 与多种 LLM 服务集成（LM Studio、Google Gemini、OpenAI-compatible）
- 保持简单的对话记忆
- 尊重用户隐私（可选择本地模型）

## 🛠️ MCP Server 提供的工具

mcp-server 现在提供了以下工具来帮助您设置和管理 LINE 机器人：

### 1. `verify_line_config`
验证 LINE Messaging API 配置的有效性。

**参数：**
- `channel_access_token`: LINE channel access token
- `channel_secret`: LINE channel secret
- `channel_id`: LINE channel ID

**示例：**
```bash
mcp_tool verify_line_config \
  --channel_access_token "your_token_here" \
  --channel_secret "your_secret_here" \
  --channel_id "your_id_here"
```

**输出：** 配置验证结果（有效/无效及错误信息）

### 2. `validate_n8n_connection`
测试与 n8n 实例的连接。

**参数：**
- `n8n_base_url`: n8n 实例的基础 URL（例如：http://localhost:5678）
- `n8n_api_key`: 可选的 n8n API key（用于进阶访问）

**示例：**
```bash
mcp_tool validate_n8n_connection \
  --n8n_base_url "http://localhost:5678"
```

**输出：** 连接状态和诊断信息

### 3. `generate_line_bot_config_template`
生成 LINE 机器人配置模板。

**示例：**
```bash
mcp_tool generate_line_bot_config_template
```

**输出：** 完整的配置模板（JSON 格式），包括：
- LINE 配置（tokens、bot 名称等）
- n8n 配置（webhook URL 等）
- LLM 配置（三种 LLM 选项的参数）

### 4. `get_line_bot_setup_checklist`
获取完整的设置检查清单。

**示例：**
```bash
mcp_tool get_line_bot_setup_checklist
```

**输出：** 分步骤的设置检查清单，包括所有必要的任务和重要提醒

## 🚀 快速开始

### 步骤 1：查看项目文件

LINE Family Comment Bot 已经安装在 `line-family-comment-bot/` 目录中：

```bash
ls -la line-family-comment-bot/
```

关键文件：
- `workflows/LINE_FAMILY_COMMENT_BOT.public.json` - n8n workflow
- `docs/` - 详细的设置文档
- `setup_helper.py` - 设置辅助脚本

### 步骤 2：运行设置辅助脚本

```bash
cd line-family-comment-bot
python setup_helper.py
```

这会生成：
- 配置模板
- 完整的设置说明
- 文件检查

### 步骤 3：准备 n8n

**选项 A：本地 n8n**
```bash
# 安装 n8n（如果还没安装）
npm install -g n8n

# 启动 n8n
n8n
```

**选项 B：使用 n8n Cloud**
访问 https://app.n8n.cloud/ 并登录

### 步骤 4：导入 Workflow

1. 在 n8n 中创建新 workflow
2. 点击"Import from File"或"Import from URL"
3. 选择 `line-family-comment-bot/workflows/LINE_FAMILY_COMMENT_BOT.public.json`
4. 导入完成后，**暂时不要启用 workflow**

### 步骤 5：配置 LINE Developers

1. 访问 https://developers.line.biz/console/
2. 创建新的 Messaging API channel
3. 复制以下信息：
   - Channel Access Token
   - Channel Secret
   - Channel ID

### 步骤 6：配置 n8n 中的 LINE Config 节点

在 n8n workflow 中找到 `LINE Config` 节点，填入：

- `CHANNEL_ACCESS_TOKEN`: [复制自 LINE Developers]
- `CHANNEL_SECRET`: [复制自 LINE Developers]
- `CHANNEL_ID`: [复制自 LINE Developers]
- `BOT_MENTION_NAME`: 您想要的 bot 名字（例如："家庭分身"）
- `BOT_PERSONA_NAME`: bot 要模拟的名字（例如："小明"）
- `ELDER_A_DISPLAY_NAME` / `ELDER_A_ADDRESS`: 长辈名字和称呼
- `ELDER_B_DISPLAY_NAME` / `ELDER_B_ADDRESS`: 另一位长辈名字和称呼

### 步骤 7：选择和配置 LLM

#### 选项 A：LM Studio（本地，隐私优先）

1. 下载 LM Studio：https://lmstudio.ai/
2. 下载一个合适的模型（推荐 7B 或更小）
3. 启动 Local Server
4. 在 n8n 中，在 `OpenAI-compatible Model` 节点配置：
   - Base URL: `http://localhost:1234/v1`
   - API Key: `lm-studio`
   - Model: [从 LM Studio 选择的模型名]

#### 选项 B：Google Gemini API（简单，免费额度）

1. 申请 API key：https://ai.google.dev/
2. 在 n8n 中使用 Google Gemini 节点，或使用 OpenAI-compatible gateway
3. 配置 API key 和模型（如 `gemini-2.0-flash`）

#### 选项 C：其他 OpenAI-compatible API

如果您已有 OpenRouter、Groq 等的 API key：

1. 在 n8n 的 `OpenAI-compatible Model` 节点中：
   - Base URL: [服务商提供]
   - API Key: [您的 API key]
   - Model: [选择的模型名]

### 步骤 8：配置 Webhook（仅本地 n8n 需要）

如果使用本地 n8n，需要设置 Ngrok 来暴露公网 URL：

1. 下载 Ngrok：https://ngrok.com/
2. 注册并获取 authtoken
3. 运行：`ngrok http 5678`
4. 复制输出的 `https://...ngrok.io` URL
5. 在 n8n 的 Webhook 节点复制 Production URL
6. 在 LINE Developers 中设置 Webhook URL

⚠️ **重要提示**：免费 Ngrok URL 在重启后会改变，需要更新 LINE Developers 的 Webhook URL。建议使用 Ngrok 的 static domain 功能或升级到 n8n Cloud。

### 步骤 9：测试连接

1. 在 n8n 中启用 workflow
2. 在 LINE Developers 中点击 "Verify" 按钮
3. 将 bot 添加为 LINE 好友
4. 发送测试消息（包含 bot 名字）
5. 验证 bot 正确响应

### 步骤 10：加入家庭群组

确认 bot 表现良好后，将其添加到家庭 LINE 群组。

## 🔧 配置文件

### 环境变量

创建 `.env` 文件来存储敏感信息：

```env
# LINE Configuration
LINE_CHANNEL_ACCESS_TOKEN=your_token_here
LINE_CHANNEL_SECRET=your_secret_here
LINE_CHANNEL_ID=your_id_here

# n8n Configuration
N8N_BASE_URL=http://localhost:5678
N8N_WEBHOOK_BASE_URL=https://your-ngrok-url.ngrok.io

# LLM Configuration (choose one)
LLM_TYPE=lm_studio  # or google_gemini or openai_compatible

# For LM Studio
LM_STUDIO_BASE_URL=http://localhost:1234/v1
LM_STUDIO_MODEL=model-name

# For Google Gemini
GOOGLE_API_KEY=your_google_api_key
GEMINI_MODEL=gemini-2.0-flash

# For OpenAI-compatible
OPENAI_BASE_URL=https://api.openrouter.ai/v1
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=model-name

# Memory Configuration
CONTEXT_WINDOW_LENGTH=5
```

## 📊 配置建议

### 对话记忆长度 (Context Window)

`contextWindowLength` 参数控制 bot 会记住多少条之前的消息：

| 配置 | 推荐场景 | 说明 |
|------|--------|------|
| 0-2  | 硬件较弱 | 最节省资源，bot 只回复当前消息 |
| 3-5  | 想省 token | 能理解简单的上下文 |
| 5-10 | 一般家庭 | **推荐值**，良好的平衡 |
| >10  | 不推荐 | 增加 token 使用和硬件负担 |

### LLM 模型选择

| 模型方案 | 隐私性 | 成本 | 速度 | 复杂度 |
|--------|------|------|------|--------|
| LM Studio | ⭐⭐⭐⭐⭐ | 免费 | 取决于硬件 | 中等 |
| Google Gemini | ⭐⭐ | 免费（有额度） | 快 | 低 |
| OpenRouter | ⭐⭐⭐ | 按用量收费 | 快 | 低 |

## 🐛 故障排除

### 常见问题

#### Q：webhook 连接失败
**A：** 检查：
1. Ngrok 是否还在运行（`ngrok http 5678`）
2. Ngrok URL 是否更新到了 LINE Developers
3. n8n workflow 是否已启用

#### Q：bot 不回应任何消息
**A：** 检查：
1. LINE 的 webhook verification 是否通过
2. n8n workflow 中 LLM 配置是否正确
3. 查看 n8n 中的执行日志看是否有错误

#### Q：提示"Invalid API key"
**A：** 检查：
1. 确保 API key 正确（复制粘贴，避免空格）
2. API key 权限是否充足
3. API key 是否已过期

#### Q：消息理解有问题
**A：** 尝试：
1. 检查 LLM 模型是否支持你使用的语言
2. 调整 prompt 或 bot persona
3. 检查模型大小是否足够

### 获取帮助

详细的故障排除指南见：`line-family-comment-bot/docs/troubleshooting.md`

## 🔐 安全最佳实践

### 必须做的：
- ✅ 将敏感信息存储在 `.env` 文件中
- ✅ 将 `.env` 添加到 `.gitignore`
- ✅ 使用环境变量加载敏感数据
- ✅ 定期轮换 API keys 和 tokens
- ✅ 只给 bot 必要的权限

### 绝对不要做的：
- ❌ 不要把 token 提交到 git
- ❌ 不要在代码中硬编码 API keys
- ❌ 不要把家庭成员信息放在公开位置
- ❌ 不要把真实名字放在 bot persona 中
- ❌ 不要分享 n8n 数据库文件（database.sqlite）

### 隐私考虑：
- 如果使用云端 LLM API，家庭聊天记录会上传
- 推荐使用 LM Studio（本地模型）来保护隐私
- 不要把医疗、财务等敏感信息作为测试数据

## 📚 相关文档

| 文档 | 内容 |
|------|------|
| `docs/setup-line.md` | LINE Developers 详细配置 |
| `docs/setup-n8n.md` | n8n workflow 配置 |
| `docs/setup-llm.md` | LLM 选项详细对比 |
| `docs/setup-ngrok.md` | Ngrok 和 webhook 设置 |
| `docs/troubleshooting.md` | 常见问题解决 |
| `docs/privacy-and-safety.md` | 隐私和安全提醒 |
| `docs/beginner-roadmap.md` | 初学者完整路线图 |

## 📞 支持

- 📖 查看本目录中的 docs/
- 🐛 检查 troubleshooting.md 中的常见问题
- 💬 在 LINE 群组中测试前，先作为个人好友测试

## ✨ 使用建议

### bot 不应该太聊天
在家庭群组中，机器人过度回复会很烦人。建议：
- 只在被提到时回复
- 关键词触发要保守
- 避免对每条消息都回复
- 定期检查对话质量

### 对话示例

✅ **好的对话**：
```
妈妈：今天天气怎么样？
Bot：媽媽，根據天氣預報，今天局部多雲，下午可能有短暫陣雨。
媽媽：那我記得帶傘了。
```

❌ **不好的对话**：
```
爸爸：我去買菜了
Bot：買菜是很好的運動！建議選擇新鮮的蔬菜...
爸爸：...我只是想說我出門了
Bot：出門是健康的生活方式，建議...
```

## 🎯 后续步骤

1. ✅ 完成初始设置
2. ✅ 作为 LINE 好友测试 bot
3. ✅ 调整 bot 配置以获得最佳表现
4. ✅ 加入家庭群组并监控
5. ✅ 根据反馈调整对话风格

祝您的家庭 LINE 群组和谐愉快！🎉
