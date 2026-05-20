# LINE Developers 設定

## 建立 Messaging API channel

1. 打開 LINE Developers Console。
2. 建立 provider，或使用既有 provider。
3. 建立 Messaging API channel。
4. 記下：
   - Channel ID
   - Channel secret
   - Channel access token

這些資料都是私密資料，請不要貼到公開地方，也不要交給不信任的人或 agent。

如果你以前沒有申請過 LINE Bot，可以請 agent 先陪你完成這一段，不要急著跳到 n8n。LINE channel 沒建好，後面 webhook 就無法測試。

## 填入 n8n

到 n8n 的 `LINE Config` 節點，把以下欄位換成自己的：

- `CHANNEL_ACCESS_TOKEN`
- `CHANNEL_SECRET`
- `CHANNEL_ID`

## 設定 Webhook

1. 在 n8n 打開 `Webhook` 節點。
2. 複製 Production URL。
3. 回到 LINE Developers。
4. 把 Production URL 貼到 Webhook URL。
5. 開啟 Use webhook。
6. 按 Verify 測試。

如果你用本機 n8n，Webhook URL 不能是 `localhost`。你需要先用 Ngrok 取得公開網址。請看 [setup-ngrok.md](setup-ngrok.md)。

臨時 Ngrok 網址重開後可能改變。如果 LINE 昨天可以、今天不行，請先檢查 Ngrok 網址是否變了。

## 先加為好友測試

建議先把 bot 加為自己的 LINE 好友，不要一開始就放進家庭群組。

先測試：

- 傳一句有叫到 bot 名字的文字。
- 傳一張普通圖片。
- 傳一句沒有叫 bot 名字的文字，確認它不會太吵。

範例：

```text
家庭分身 今天晚餐吃什麼好？
```

如果有設定 `BOT_MENTION_NAME`，請用你自己設定的名字呼叫它。

## 再加入 LINE 群組

確認好友測試沒問題後，再把 bot 加進家庭群組。

加入後可以先用簡單句子測試：

```text
家庭分身 今天晚餐吃什麼好？
```

如果家人覺得它太常回，可以先把 `General Chat Whitelist` 與 `General Chat Intent Judge` 調得更保守，或要求只有叫到 bot 名字才回。
