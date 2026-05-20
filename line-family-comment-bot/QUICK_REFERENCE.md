# LINE Family Comment Bot - Quick Reference

快速查询常用命令和配置。

## 🚀 5 分钟快速开始

```bash
# 1. 运行设置助手
cd line-family-comment-bot
python setup_helper.py

# 2. 查看设置清单
mcp_tool get_line_bot_setup_checklist

# 3. 生成配置模板
mcp_tool generate_line_bot_config_template

# 4. 验证配置
mcp_tool verify_line_config \
  --channel_access_token "YOUR_TOKEN" \
  --channel_secret "YOUR_SECRET" \
  --channel_id "YOUR_ID"

# 5. 测试 n8n 连接
mcp_tool validate_n8n_connection \
  --n8n_base_url "http://localhost:5678"
```

## 📋 关键文件位置

| 文件 | 用途 |
|------|------|
| `workflows/LINE_FAMILY_COMMENT_BOT.public.json` | n8n workflow |
| `docs/setup-line.md` | LINE Developers 教程 |
| `docs/setup-n8n.md` | n8n 配置指南 |
| `docs/setup-llm.md` | LLM 选项对比 |
| `docs/setup-ngrok.md` | Webhook 配置 |
| `setup_helper.py` | 交互式设置脚本 |
| `DEVELOPER_GUIDE.md` | 开发者指南 |

## 🔧 核心配置参数

### LINE Config 节点
```json
{
  "CHANNEL_ACCESS_TOKEN": "来自 LINE Developers",
  "CHANNEL_SECRET": "来自 LINE Developers",
  "CHANNEL_ID": "来自 LINE Developers",
  "BOT_MENTION_NAME": "你想要的 bot 名字",
  "BOT_PERSONA_NAME": "bot 模拟的人物",
  "ELDER_A_DISPLAY_NAME": "长辈名字",
  "ELDER_A_ADDRESS": "对长辈的称呼"
}
```

### Simple Memory 节点
```json
{
  "contextWindowLength": 5  // 推荐 5-10
}
```

### OpenAI-compatible Model 节点
```json
{
  "baseUrl": "http://localhost:1234/v1",  // LM Studio 地址
  "apiKey": "lm-studio",
  "model": "模型名称"
}
```

## 🛠️ MCP Server 工具

### verify_line_config
验证 LINE 配置的有效性
```bash
mcp_tool verify_line_config \
  --channel_access_token "token" \
  --channel_secret "secret" \
  --channel_id "id"
```

### validate_n8n_connection
测试 n8n 连接
```bash
mcp_tool validate_n8n_connection \
  --n8n_base_url "http://localhost:5678"
```

### generate_line_bot_config_template
生成完整配置模板
```bash
mcp_tool generate_line_bot_config_template
```

### get_line_bot_setup_checklist
获取分步骤的设置清单
```bash
mcp_tool get_line_bot_setup_checklist
```

## 📊 LLM 配置对比

| 方案 | 隐私 | 成本 | 难度 | 说明 |
|------|------|------|------|------|
| **LM Studio** | ⭐⭐⭐⭐⭐ | 免费 | 中等 | 本地模型，最隐私 |
| **Google Gemini** | ⭐⭐ | 免费* | 低 | 简单快速，有额度限制 |
| **OpenRouter** | ⭐⭐⭐ | $$ | 低 | 按用量收费，支持多模型 |
| **Groq** | ⭐⭐⭐ | 免费* | 低 | 快速推理，有额度限制 |

*免费额度可能会变，请查看官方文档

## ⚠️ 常见错误排查

| 问题 | 检查点 |
|------|--------|
| Webhook 验证失败 | • Token 是否正确<br/>• Ngrok 是否运行<br/>• n8n 是否启用 |
| Bot 不回应 | • n8n 执行日志<br/>• LLM API key<br/>• LINE webhook URL |
| 消息解析错误 | • 查看 n8n 执行记录<br/>• 检查 message format<br/>• 看是否有 error node |
| 超时问题 | • 增加 LLM 超时<br/>• 用更小的模型<br/>• 检查网络连接 |

## 🔐 安全检查清单

- [ ] 所有敏感信息在 .env 文件中
- [ ] .env 在 .gitignore 中
- [ ] 没有把 token 提交到 git
- [ ] 没有硬编码真实家庭成员名字
- [ ] 定期轮换 API keys
- [ ] 使用 Ngrok static domain 或 n8n Cloud
- [ ] 不共享 n8n 数据库文件

## 📱 LINE 群组最佳实践

✅ 做这些：
- 回应被提到的消息
- 用温和、尊重的语气
- 定期监控对话质量

❌ 避免这些：
- 对每条消息都回应
- 过度解释或说教
- 在群组中分享敏感信息

## 🐛 调试命令

```bash
# 查看 n8n 日志
tail -f ~/.n8n/logs/

# 监视 ngrok
ngrok http 5678 --log=stdout

# 测试 webhook
curl -X POST https://your-url/webhook/linebot \
  -H "Content-Type: application/json" \
  -d '{"test": "message"}'

# 检查 LM Studio
curl http://localhost:1234/v1/models
```

## 📚 文档导航

| 我想... | 查看... |
|--------|--------|
| 快速开始 | LINE_FAMILY_COMMENT_BOT_INTEGRATION.md |
| 配置 LINE | docs/setup-line.md |
| 配置 n8n | docs/setup-n8n.md |
| 选择 LLM | docs/setup-llm.md |
| 配置 Webhook | docs/setup-ngrok.md |
| 解决问题 | docs/troubleshooting.md |
| 自定义代码 | DEVELOPER_GUIDE.md |
| 保护隐私 | docs/privacy-and-safety.md |

## 💬 快速问题

**Q: 需要多少技术能力？**
A: 不需要编程，但需要能跟步骤。用 setup_helper.py 会更简单。

**Q: 能在手机上运行吗？**
A: 不能。n8n 需要在电脑或服务器上运行。

**Q: 家庭成员会看到什么？**
A: 只看到 bot 的回复。他们不会看到配置、API keys、或技术细节。

**Q: 我的消息会上传到云端吗？**
A: 取决于你选择的 LLM。使用 LM Studio 则完全本地；使用 API 则会上传。

**Q: 成本是多少？**
A: 完全免费（如果用 LM Studio）或按 API 用量收费。

**Q: 多久更新一次？**
A: 根据 n8n 和 LLM 服务的更新。建议定期检查。

## 🎯 下一步

1. ✅ 查看 LINE_FAMILY_COMMENT_BOT_INTEGRATION.md
2. ✅ 运行 python setup_helper.py
3. ✅ 按照检查清单完成设置
4. ✅ 作为 LINE 好友测试
5. ✅ 加入家庭群组

---

**需要帮助？** 查看 docs/troubleshooting.md 或查看具体的设置文档。
