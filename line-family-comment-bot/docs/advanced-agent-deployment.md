# 進階：讓 Agent 協助部署 n8n

一般使用者不需要看這份文件。

如果你只是想把這個 LINE bot 跑起來，請照 README、`setup-n8n.md`、`setup-line.md`、`setup-ngrok.md` 手動操作即可。

這份文件是給比較進階的使用者：你想讓 Codex、Claude Code 或其他 agent 透過 n8n API / MCP 直接讀取、匯入、修改、檢查 workflow。

## 先講風險

n8n API key 或 MCP 連線通常可以讓 agent 操作你的 n8n。

可能包含：

- 讀取 workflow。
- 建立 workflow。
- 修改 workflow。
- 啟用或停用 workflow。
- 讀取部分設定或節點內容。

因此請記住：

- 不要把 n8n API key 貼到公開 GitHub、Threads、issue、公開聊天室。
- 不要把 n8n API key 寫進 workflow JSON。
- 不要把 n8n API key commit 到 repo。
- 只給你信任的 agent 使用。
- 用完後，如果不確定是否安全，可以撤銷或重建 API key。

## 什麼情況不需要

以下情況不需要 n8n API key 或 MCP：

- 你只是要匯入 `LINE_FAMILY_COMMENT_BOT.public.json`。
- 你願意在 n8n UI 裡手動填 `LINE Config`。
- 你只是照文件一步一步設定 LINE、LLM、Ngrok。
- 你是第一次使用 n8n。

## 什麼情況可以考慮

以下情況可以考慮進階方式：

- 你已經熟悉 n8n。
- 你想讓 agent 幫你檢查 workflow 節點。
- 你想讓 agent 幫你修改 prompt 或節點設定。
- 你想讓 agent 幫你匯入、更新 workflow。
- 你知道如何撤銷 n8n API key。

## 建議給 Agent 的提示詞

你可以對 agent 說：

```text
我想用進階方式讓你協助我部署這個 n8n workflow。
請先說明 n8n API key / MCP 的風險。
不要要求我把 key 貼到公開地方。
每一步都請先解釋用途，等我確認後再繼續。
```

如果你只是想讓 agent 指導，而不是直接操作，可以說：

```text
請不要直接操作我的 n8n。
只用文字一步一步指導我在 n8n UI 裡完成設定。
```

## n8n API key 大方向

不同 n8n 版本和部署方式的 UI 可能不同。請以你當下 n8n 畫面為準。

大方向通常是：

1. 進入 n8n 個人設定或 API 設定頁。
2. 建立 API key。
3. 複製 API key 到本機安全位置。
4. 讓 agent 使用該 key 連線 n8n API。
5. 完成部署後，視情況撤銷 API key。

請不要把 API key 存到這個 repo。

## n8n MCP 大方向

如果你的 agent 支援 n8n MCP，通常會需要：

- n8n 的網址。
- n8n API key 或其他授權資訊。
- MCP server 設定。

請讓 agent 依照它自己的 MCP 設定方式處理。不同 agent 的設定檔位置不同，不建議在這份新手 repo 寫死。

## 最安全的進階流程

1. 先用 UI 手動匯入 workflow。
2. 用 agent 檢查 public workflow JSON，而不是直接讀你的私人 n8n。
3. 真的需要操作 n8n 時，再建立短期 API key。
4. agent 完成後，撤銷 API key。
5. 執行 `scripts/security-scan.sh`，確認 repo 沒有不小心留下 key。

## 如果你不確定

不要設定 API key 或 MCP。

你可以直接問 agent：

```text
我不確定是否需要 n8n API key 或 MCP。
請先判斷我的情境，如果不是必要，請帶我用 n8n UI 手動安裝。
```

