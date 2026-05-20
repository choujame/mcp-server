# 完全新手路線圖

如果你從來沒用過 n8n，也沒有申請過 LINE Bot，請照這個順序走。

## 先理解三個東西

你會用到三個服務：

- LINE Developers：建立一個 LINE 機器人帳號。
- n8n：負責接收 LINE 訊息，並決定要怎麼回。
- LLM：負責產生自然語言回覆，例如 LM Studio 本地模型或 Google Gemini API。
- Ngrok：如果你用本機 n8n，它負責給你的電腦一個外網可以連進來的網址。

你可以把它想成：

```text
LINE 群組訊息 -> n8n workflow -> LLM 產生回覆 -> n8n 回傳到 LINE
```

## 建議順序

1. 先準備 n8n。
2. 匯入這個 repo 的 workflow。
3. 申請 LINE Messaging API channel。
4. 把 LINE token 填進 n8n 的 `LINE Config`。
5. 設定 LLM。
6. 如果是本機 n8n，設定 Ngrok 公開網址。
7. 把 n8n webhook URL 貼到 LINE Developers。
8. 先把 bot 加成自己的 LINE 好友測試。
9. 文字和圖片都正常後，再邀請進家庭群組。

## 本機 n8n 為什麼需要 Ngrok

LINE 在雲端，它要把訊息送到你的 n8n。可是如果 n8n 跑在你自己的電腦，LINE 預設找不到你的電腦。

Ngrok 的作用是給你的本機 n8n 一個公開 HTTPS 網址，例如：

```text
https://something.ngrok-free.app
```

你再把這個網址加上 `/webhook/linebot`，貼到 LINE Developers。

請注意：免費臨時網址重開後可能會變。若網址變了，LINE Developers 的 Webhook URL 也要一起更新。想穩定使用，請設定 Ngrok static domain，或使用 n8n Cloud。

## 為什麼不要一開始就加進群組

家庭群組很敏感。機器人如果太愛回話，大家會覺得被打擾。

請先用自己的 LINE 跟 bot 測試：

- 叫它的名字時會不會回。
- 傳圖片會不會回。
- 不叫它時會不會安靜。
- 回覆語氣是不是你能接受。

確定沒問題後，再放進家庭群組。

## 記憶功能要怎麼想

workflow 裡有一個 `Simple Memory` 節點，會讓 bot 記得最近幾輪對話。

建議值：

- 0：完全不記憶，最省資源。
- 3：適合本地硬體較弱，或只想短短接話。
- 5：適合一般家庭群組。
- 10：已經算很多，token 用量會增加。

不建議超過 10。記憶越多，花費和電腦負擔越高，也越可能把不相關的舊對話帶進來。

## 請 agent 協助你時，可以這樣說

```text
請依照這個 repo 的 AGENTS.md，用繁體中文一步一步帶我安裝。
我完全沒有用過 n8n，也沒有申請過 LINE Bot。
每一步請先解釋我要做什麼，等我完成再進下一步。
```

## 卡住時不要放棄

如果你遇到錯誤，不代表你不適合做這件事。n8n、LINE Developers、API key 這些東西本來就有很多小設定，第一次卡住很正常。

你可以把目前畫面或錯誤訊息貼給 agent，直接問：

```text
我卡住了，請看這個錯誤訊息，告訴我下一步怎麼辦。
請不要一次給我太多步驟，一次帶我做一小步。
```

Codex、Claude 這類 agent 都很強，很適合陪你排除安裝問題。不要因為第一個錯誤就放棄，這個 bot 做起來之後很值得。

願各位群組和諧，父母健康快樂。
