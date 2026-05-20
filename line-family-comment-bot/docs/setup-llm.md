# LLM 設定

這個 bot 需要一個語言模型來回覆文字與圖片。你可以選本地模型，也可以選雲端 API。

## 路線 A：LM Studio，本地隱私優先

適合：

- 不想把家庭聊天內容送到雲端 API。
- 願意讓自己的電腦開著跑模型。
- 可以接受速度取決於電腦硬體。

設定方向：

1. 安裝 LM Studio。
2. 下載一個適合自己電腦的模型。
3. 在 LM Studio 啟動 Local Server。
4. 在 n8n 的 OpenAI-compatible credentials 設定：
   - Base URL：`http://localhost:1234/v1`
   - API key：LM Studio 通常可填任意字串，例如 `lm-studio`
   - Model：填你在 LM Studio 載入的模型名稱

硬體建議：

- 8GB RAM：先試 3B 到 4B 模型。
- 16GB RAM：可試 7B 到 8B 模型。
- 32GB RAM 以上或有獨立 GPU：可試更大的模型。
- 圖片理解通常需要 vision model；如果模型不支援圖片，圖片節點會比較容易失敗。

LM Studio 官方文件提到它支援 OpenAI-compatible endpoint，常見 local server port 是 `1234`。

## 路線 B：Google Gemini API，設定相對簡單

適合：

- 想快速開始。
- 可接受聊天內容送到 Google API。
- 想使用免費額度測試。

注意：Google 免費額度、可用模型和 rate limit 常變。安裝當天請查官方 Google AI 文件確認。

目前官方文件顯示 Gemini API 有 Free tier，rate limit 依模型不同而不同。若只想先測試，通常可從 Flash 或 Flash-Lite 類模型開始。

n8n 設定方式有兩種：

1. 使用 n8n 的 Google Gemini / Google AI 節點。
2. 使用支援 Gemini 的 OpenAI-compatible gateway。

如果你是新手，建議請 agent 幫你依照當天 n8n 版本選最簡單的節點。

## 路線 C：其他 OpenAI-compatible API

適合：

- 已經有 OpenRouter、Groq、Together、Fireworks、Mistral 等 API key。
- 想直接沿用 workflow 裡的 OpenAI-compatible model 節點。

請準備：

- API key
- Base URL
- Model 名稱

免費額度常變，不要把文件裡看到的免費方案當成永久承諾。

## 新手建議

如果你不知道選哪個：

1. 想保護家庭聊天隱私：先試 LM Studio。
2. 想最快跑起來：先試 Google Gemini API。
3. 已經有 OpenRouter 或 Groq key：用 OpenAI-compatible API。

