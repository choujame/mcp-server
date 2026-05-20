# LINE Family Comment Bot - Developer Guide

本指南适合想要自定义或扩展 LINE Family Comment Bot 的开发者。

## 🏗️ 项目结构

```
line-family-comment-bot/
├── workflows/
│   └── LINE_FAMILY_COMMENT_BOT.public.json    # n8n workflow JSON
├── docs/
│   ├── setup-line.md                          # LINE 配置教程
│   ├── setup-n8n.md                           # n8n 设置教程
│   ├── setup-llm.md                           # LLM 选项对比
│   ├── setup-ngrok.md                         # Webhook 配置
│   ├── troubleshooting.md                     # 故障排除
│   ├── privacy-and-safety.md                  # 隐私提醒
│   ├── advanced-agent-deployment.md           # 进阶部署
│   ├── publish-to-github.md                   # 发布指南
│   ├── beginner-roadmap.md                    # 初学者路线
├── scripts/
│   └── security-scan.sh                       # 安全扫描脚本
├── security/
│   └── sanitization-checklist.md              # 公开前检查清单
├── env/
│   └── .env.example                           # 环境变量示例
├── setup_helper.py                            # 设置辅助脚本（新增）
├── LICENSE
├── README.md
└── AGENTS.md
```

## 🔧 核心组件

### 1. n8n Workflow

**文件**: `workflows/LINE_FAMILY_COMMENT_BOT.public.json`

主要节点：
- **Webhook** - 接收 LINE 消息
- **LINE Parsing** - 解析 LINE 消息格式
- **Intent Judge** - 判断是否需要回复
- **General Chat Intent Judge** - 判断通用对话意图
- **Chat with Assistants** - LLM 聊天节点
- **Image Analysis** - 图片理解
- **Simple Memory** - 对话记忆
- **LINE Response** - 发送回复给 LINE

**修改 workflow 的方式**：
1. 在 n8n UI 中打开 workflow
2. 修改相关节点
3. 导出为 JSON
4. 覆盖原 JSON 文件
5. 更新版本号和 changelog

### 2. 环境配置

**LINE Config 节点参数**：
```json
{
  "CHANNEL_ACCESS_TOKEN": "从 LINE Developers 获取",
  "CHANNEL_SECRET": "从 LINE Developers 获取",
  "CHANNEL_ID": "从 LINE Developers 获取",
  "BOT_MENTION_NAME": "在群组中叫 bot 的名字",
  "BOT_PERSONA_NAME": "bot 模拟的人物名字",
  "ELDER_A_DISPLAY_NAME": "长辈在 LINE 的显示名",
  "ELDER_A_ADDRESS": "对长辈的称呼",
  "ELDER_B_DISPLAY_NAME": "另一位长辈的显示名",
  "ELDER_B_ADDRESS": "对另一位长辈的称呼"
}
```

### 3. LLM 集成

支持三种 LLM 后端：

#### LM Studio (OpenAI-compatible)
```
Base URL: http://localhost:1234/v1
API Key: lm-studio
Model: [从 LM Studio 加载的模型名]
```

#### Google Gemini API
```
需要 Google AI API Key
模型: gemini-2.0-flash (或其他可用模型)
```

#### 其他 OpenAI-compatible API
```
Base URL: [服务商提供]
API Key: [您的 API key]
Model: [选择的模型]
```

## 🎯 常见定制

### 修改 bot 的回复风格

编辑 n8n workflow 中的 `System Prompt`：

```
你是一个温和、尊重的家庭聊天机器人。
你的名字是 {{BOT_MENTION_NAME}}。
你要回应家人的日常对话...
```

### 添加新的触发条件

在 workflow 中编辑 `General Chat Intent Judge` 节点：
- 添加新的关键词
- 修改匹配逻辑
- 调整触发阈值

### 修改对话记忆长度

编辑 `Simple Memory` 节点的 `contextWindowLength` 参数：
```json
{
  "contextWindowLength": 5
}
```

### 支持更多长辈

在 workflow 中复制 `ELDER_A` 节点群组，创建 `ELDER_C` 等：
1. 在 n8n 中选择相关节点
2. 复制 (Ctrl+C)
3. 粘贴 (Ctrl+V)
4. 修改变量名 (ELDER_C_*)
5. 在 LINE Config 中添加新参数

### 启用高级功能

查看 `docs/advanced-agent-deployment.md` 了解：
- n8n API 集成
- MCP (Model Context Protocol) 部署
- 多账户支持
- 备份和恢复策略

## 🐛 调试

### 查看 n8n 执行日志

1. 打开 n8n UI
2. 找到 workflow 执行记录
3. 点击执行条目查看详细日志
4. 查找错误信息和堆栈追踪

### 常见 n8n 错误

| 错误 | 原因 | 解决方案 |
|------|------|--------|
| Webhook validation failed | LINE 配置不正确 | 检查 token 和 secret |
| Model timeout | LLM 响应太慢 | 增加超时或换更小的模型 |
| Memory node error | 内存配置不对 | 检查 contextWindowLength |
| 401 Unauthorized | API key 无效 | 验证和更新 API key |

### 本地调试技巧

```bash
# 启用 n8n 调试日志
export NODE_DEBUG=n8n
n8n

# 监视 ngrok 连接
ngrok http 5678 --log=stdout

# 测试 webhook
curl -X POST https://your-ngrok-url/webhook/linebot \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'
```

## 📊 性能优化

### 降低延迟
1. 使用更小的 LLM 模型
2. 减少 context window 长度
3. 缓存常见回复

### 节省成本
1. 如果用云端 API，选择更便宜的模型
2. 减少不必要的 API 调用
3. 使用本地 LM Studio 消除 API 成本

### 减少 token 使用
1. 简化 system prompt
2. 减少 context window
3. 使用更小的模型

## 🔒 安全加固

### 部署前检查清单

```
□ 所有 API keys 都在 .env 中（不在代码中）
□ .env 文件在 .gitignore 中
□ 没有硬编码的真实 tokens
□ 没有硬编码的家庭成员名字
□ 没有测试时的 debug 日志
□ 使用了 Ngrok static domain 或 n8n Cloud
□ 定期轮换 API keys
```

### 敏感数据处理

**不要提交到 Git 的文件**：
- `.env`
- `n8n/database.sqlite`
- `n8n/config`
- n8n 的 log 文件

**公开 repo 时要删除的**：
- 所有示例 tokens
- 真实的家庭成员名字
- 医疗或财务相关的测试数据

## 📈 扩展功能

### 添加新的 LLM 提供商

在 workflow 中添加新的 LLM 节点：
1. 添加新的 `OpenAI-compatible Model` 节点
2. 配置新的 credentials
3. 在 intent judge 中添加切换逻辑
4. 测试新的提供商

### 集成其他服务

例如发送到数据库、slack、邮件等：
1. 在 workflow 中添加新节点
2. 配置服务认证
3. 映射数据字段
4. 测试端到端流程

### 多语言支持

修改 system prompt 来支持多语言：
```
你可以用中文、英文或日文回复。
根据用户的语言选择合适的语言回复...
```

## 🧪 测试

### 单元测试

在 n8n 中测试个别节点：
1. 选择节点
2. 点击"Execute Node"
3. 查看输出

### 集成测试

测试完整的 workflow：
1. 启用 workflow
2. 在 LINE 中发送测试消息
3. 验证响应

### 负载测试

```bash
# 用 Apache Bench 进行简单负载测试
ab -n 100 -c 10 https://your-ngrok-url/webhook/linebot
```

## 📝 版本管理

### 更新工作流

1. 修改 n8n workflow
2. 在 n8n UI 导出 JSON
3. 备份当前版本：`cp LINE_FAMILY_COMMENT_BOT.public.json LINE_FAMILY_COMMENT_BOT.public.v1.json`
4. 替换新版本
5. 更新 CHANGELOG

### Changelog 格式

```markdown
## [1.2.0] - 2026-05-20

### Added
- 支持图片理解的新 vision model
- 新的内存节点配置选项

### Changed
- 改进的 intent judge 逻辑
- 更自然的回复 prompt

### Fixed
- 修复了在某些情况下的 webhook 验证问题
```

## 🤝 贡献指南

如果想改进这个项目：

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开 Pull Request

**提交前检查**：
- 所有敏感信息已移除
- 通过了安全扫描 (`scripts/security-scan.sh`)
- 文档已更新
- 测试通过

## 📚 相关资源

- [n8n 文档](https://docs.n8n.io/)
- [LINE Messaging API 文档](https://developers.line.biz/en/docs/messaging-api/)
- [LM Studio 文档](https://lmstudio.ai/)
- [Google Gemini API 文档](https://ai.google.dev/)

## 💡 技巧和窍门

### 加快开发周期
```bash
# 导出 workflow（自动化）
curl -X GET http://localhost:5678/api/workflows/1 \
  -H "X-N8N-API-KEY: your-api-key" | jq . > workflow.json
```

### 快速测试 LLM 响应
```bash
# 直接测试 LM Studio
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "model-name",
    "messages": [{"role": "user", "content": "你好"}]
  }'
```

### 监视 webhook 活动
```bash
# 在另一个终端监视 ngrok
ngrok http 5678 --log=stdout
```

祝您开发愉快！🚀
