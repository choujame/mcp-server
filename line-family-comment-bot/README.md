# LINE Family Comment Bot

這是一個給家庭 LINE 群組使用的 n8n 聊天機器人模板。

它的設計目標很單純：當家人分享文字、圖片、生活近況、健康問題或長輩常見的轉傳訊息時，機器人可以用溫和、尊重、不敷衍的語氣回應。

你不需要是工程師。建議你把這個 GitHub repo 網址貼給 Codex、Claude Code、Gemini CLI 或其他 coding agent，請它依照 [AGENTS.md](AGENTS.md) 一步一步帶你安裝。

## 安裝時主要看這些

- `workflows/LINE_FAMILY_COMMENT_BOT.public.json`：可匯入 n8n 的公開版工作流。
- `docs/setup-line.md`：LINE Developers 設定教學。
- `docs/setup-n8n.md`：n8n 匯入與設定教學。
- `docs/setup-ngrok.md`：本機 n8n 對外網址與固定網址設定教學。
- `docs/setup-llm.md`：LLM 模型選擇，包含 LM Studio、本地模型、Google Gemini API。
- `docs/privacy-and-safety.md`：隱私、安全、不要公開 token 的提醒。
- `docs/troubleshooting.md`：常見錯誤排查。
- `docs/advanced-agent-deployment.md`：進階使用者讓 agent 透過 n8n API/MCP 協助部署的提醒。

## 維護者才需要看

如果你只是安裝使用，不需要理會這一段。

- `docs/publish-to-github.md`：想改作自己的公開 repo 時，發布到 GitHub 前的安全提醒。
- `security/sanitization-checklist.md`：公開前檢查清單。
- `scripts/security-scan.sh`：簡易敏感資料掃描腳本。

## 最快開始方式

如果你完全沒有用過 n8n、也沒有申請過 LINE Bot，請不要緊張。請先看 [docs/beginner-roadmap.md](docs/beginner-roadmap.md)，照順序慢慢做。

1. 安裝或打開 n8n。
2. 匯入 `workflows/LINE_FAMILY_COMMENT_BOT.public.json`。
3. 到 LINE Developers 建立 Messaging API channel。
4. 把 LINE 的 channel access token、channel secret、channel id 填進 n8n 的 `LINE Config` 節點。
5. 設定 LLM。新手建議先選其中一條：
   - 隱私優先：LM Studio 本地模型。
   - 設定簡單：Google Gemini API。
   - 已有 API key：OpenAI-compatible 服務。
6. 如果你用本機 n8n，先設定 Ngrok 公開網址。請看 [docs/setup-ngrok.md](docs/setup-ngrok.md)。
7. 把 n8n webhook URL 貼回 LINE Developers。
8. 啟用 workflow，傳訊息測試。

## 使用前先知道

這個 bot 建議不要太吵。家庭群組裡如果每個人講一句它都回，大家很快會覺得煩。

目前 workflow 已經刻意做得比較保守：通常需要特定長輩、醫療關鍵字、圖片，或明確叫到 bot 名字才會回。建議你先把機器人加為自己的 LINE 好友，測試文字和圖片都正常後，再放進家庭群組。

如果你使用本機 n8n，LINE 需要一個可以從外網連進來的網址。新手最常用 Ngrok。請注意：免費臨時網址重開後可能會改變，LINE Developers 裡的 Webhook URL 也要跟著更新。想避免每天改網址，請設定 Ngrok static domain 或改用 n8n Cloud。

這個 bot 有簡單記憶功能，預設會記得同一段對話最近約 5 則上下文。你可以到 n8n 的 `Simple Memory` 節點調整 `contextWindowLength`：

- 一般新手：建議 5 到 10。
- 想省 token：建議 3 到 5。
- 本地電腦不強：建議 3 以下。
- 只想單句回覆、不想記憶：可以設 0 或移除記憶連線。

記憶越長，回覆越能接上下文，但 token 用量、API 費用和本地模型負擔也會增加。家庭群組通常不建議超過 10。

## 很重要的安全提醒

不要把以下資料貼到公開地方，也不要交給不信任的人或 agent：

- LINE channel access token
- LINE channel secret
- LINE user id、group id、room id
- OpenAI、Google、OpenRouter、Groq 等 API key
- 真實家庭成員姓名、電話、email、地址
- n8n 的 `database.sqlite`、`config`、log 檔

這個 repo 附的是公開模板，不包含作者原本的私人 token 與家庭資料。

## 進階使用者

一般使用者不需要設定 n8n API key 或 n8n MCP。照 README 匯入 workflow、手動填設定就可以。

如果你很熟 agent，也理解 API key 權限風險，可以看 [docs/advanced-agent-deployment.md](docs/advanced-agent-deployment.md)，讓 agent 透過 n8n API 或 MCP 協助部署與檢查。

## 適合誰

- 想幫家庭 LINE 群組做一個溫和陪聊 bot 的人。
- 不熟程式，但願意照步驟操作的人。
- 想用 agent 協助安裝 n8n workflow 的人。

## 不適合誰

- 想讓 bot 取代醫師、藥師或專業診斷的人。
- 想把家人聊天紀錄大量上傳雲端但沒有告知家人的人。
- 不願意保管 API key 或 token 的人。

醫療相關回覆只能當一般資訊與關心提醒，不能當診斷或治療建議。

## 卡住時怎麼辦

遇到困難不要害怕，也不要急著放棄。你可以直接把錯誤畫面、錯誤訊息，或目前卡住的步驟貼給 Codex、Claude Code、Gemini CLI 或其他 agent，問它：

```text
我照這個 repo 安裝 LINE Family Comment Bot，目前卡在這一步。
請用繁體中文、一步一步告訴我接下來怎麼辦。
```

Codex、Claude 這類 agent 都很擅長陪你看錯誤訊息、檢查設定、帶你走下一步。很多時候不是你不會，只是少了一個人在旁邊把下一步講清楚。

願各位群組和諧，父母健康快樂。
