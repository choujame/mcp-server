# n8n 設定

## 你要先知道

n8n 是「把一格一格節點串起來」的自動化工具。這個 bot 已經把大部分流程做好，你主要要做的是匯入 workflow，然後填入自己的 LINE 與 LLM 設定。

如果你完全沒用過 n8n，請先把它想成「機器人的控制台」。LINE 收到訊息後，會把訊息送到 n8n，n8n 再決定要不要叫 LLM 回覆。

## 匯入 workflow

1. 打開 n8n。
2. 新增 workflow。
3. 選擇匯入 JSON。
4. 匯入 `workflows/LINE_FAMILY_COMMENT_BOT.public.json`。
5. 先不要啟用，先完成下面設定。

## 設定 LINE Config 節點

打開 `LINE Config` 節點，把 placeholder 改成自己的資料：

- `CHANNEL_ACCESS_TOKEN`：LINE Developers 的 channel access token。
- `CHANNEL_SECRET`：LINE Developers 的 channel secret。
- `CHANNEL_ID`：LINE Developers 的 channel ID。
- `BOT_MENTION_NAME`：希望家人在群組裡叫 bot 的名字，例如「家庭分身」。
- `BOT_PERSONA_NAME`：bot 要模仿的家人稱呼，例如「小明」。
- `ELDER_A_DISPLAY_NAME` / `ELDER_B_DISPLAY_NAME`：長輩在 LINE 裡的顯示名稱。
- `ELDER_A_ADDRESS` / `ELDER_B_ADDRESS`：bot 回覆時要怎麼稱呼，例如「媽媽」「爸爸」「阿嬤」「阿公」。

不要把真實 token 貼到公開地方，也不要交給不信任的人或 agent。

## 設定 LLM 節點

workflow 裡有幾個 `OpenAI-compatible Model` 節點。請替它們設定同一組 credentials。

常見選擇：

- LM Studio：本機跑模型，base URL 通常是 `http://localhost:1234/v1`。
- OpenRouter / Groq / Together 等：使用服務商提供的 API key 與 base URL。
- OpenAI：使用 OpenAI API key。

Google Gemini API 不是完全等同 OpenAI-compatible；若你選 Google 路線，可能需要把模型節點改成 n8n 的 Google/Gemini 節點，或使用支援 Gemini 的 OpenAI-compatible gateway。

## 設定記憶長度

打開 `Simple Memory` 節點，看 `contextWindowLength`。

這個數字代表 bot 會記得最近多少則上下文。數字越大，越能接續前面對話，但也越花 token、越吃模型效能。

建議：

- 一般家庭群組：5 到 10。
- 想省 token：3 到 5。
- 本地硬體不強：3 以下。
- 不想記憶：設 0 或移除 `Simple Memory` 到聊天 agent 的連線。

不建議超過 10。家庭群組的 bot 重點是自然、不打擾，不是記住所有事情。

## Webhook URL

匯入後，打開 `Webhook` 節點，複製 Production URL。

如果你使用 n8n Cloud，Production URL 通常可以直接使用。

如果你使用本機 n8n，Production URL 不能是 `localhost`，因為 LINE 在雲端，找不到你自己電腦裡的 `localhost`。請先依照 [setup-ngrok.md](setup-ngrok.md) 設定 Ngrok 或其他公開網址。

通常長得像：

```text
https://你的-n8n-網址/webhook/linebot
```

把這個 URL 貼到 LINE Developers 的 Webhook URL。

## 啟用

1. 儲存 workflow。
2. 啟用 workflow。
3. 到 LINE Developers 按 Verify。
4. 先把 bot 加為自己的 LINE 好友測試。
5. 測試文字、圖片、不要太吵這三件事都正常後，再邀請進家庭群組。
