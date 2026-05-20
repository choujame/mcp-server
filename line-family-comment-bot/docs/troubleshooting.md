# 常見問題

## LINE Developers Verify 失敗

請檢查：

- n8n workflow 是否已啟用。
- Webhook URL 是否使用 Production URL，不是 Test URL。
- n8n 是否能被外網連到。
- 如果是本機 n8n，Ngrok 是否正在執行。
- LINE Developers 裡的網址是否是 `https://.../webhook/linebot`，不是 `localhost`。
- `Webhook` 節點 path 是否仍是 `linebot`。

## 昨天可以，今天突然不回

如果你使用本機 n8n 加 Ngrok，最常見原因是 Ngrok 臨時網址變了。

請依序檢查：

- n8n 是否正在執行。
- Ngrok 是否正在執行。
- Ngrok 畫面上的 `https://...` 網址是否和 LINE Developers 裡的 Webhook URL 一樣。
- 如果不同，請把新的網址加上 `/webhook/linebot` 後貼回 LINE Developers。

想避免這個問題，請設定 Ngrok static domain，或改用 n8n Cloud。

## LINE 有收到訊息但 bot 不回

請檢查：

- `CHANNEL_ACCESS_TOKEN` 是否正確。
- `LINE Config` 是否有儲存。
- n8n execution log 裡哪個節點紅色。
- LINE reply token 只能用一次，重跑舊 execution 通常不能再次回 LINE。

## 文字會回，圖片不會回

請檢查：

- LLM 模型是否支援圖片理解。
- `Vision LLM Chain` 是否有連到支援 vision 的模型。
- LINE 圖片下載節點是否成功。

## 回覆太吵或亂插話

可以調整：

- `BOT_MENTION_NAME`：要求家人呼叫名字才回。
- `General Chat Whitelist`：只允許特定長輩或被 mention 時回。
- `General Chat Intent Judge` prompt：把判斷寫得更保守。

建議一開始先不要放進家庭群組。請先把 bot 加為自己的 LINE 好友測試，確認它不會每句都回，再邀請進群組。

## 回覆變慢或 API 費用變高

請檢查 `Simple Memory` 節點的 `contextWindowLength`。

- 一般建議 5 到 10。
- 本地硬體不強建議 3 以下。
- 最省資源可以設 0 或移除記憶連線。

記憶越長，token 消耗越多，回覆也可能越慢。

## 免費 API 額度用完

可能會看到 rate limit 或 quota 錯誤。

處理方式：

- 等額度重置。
- 換比較輕量的模型。
- 改用 LM Studio 本地模型。
- 開啟付費方案前，先確認價格。
