# Ngrok 設定

## 什麼時候需要 Ngrok

如果你使用 n8n Cloud，通常不需要 Ngrok，因為 n8n Cloud 本身就有公開網址。

如果你使用本機 n8n，例如在自己的 Mac、Windows 或家裡電腦上跑 `http://localhost:5678`，你就需要一個公開 HTTPS 網址，LINE 才能把訊息送進來。新手最常用 Ngrok。

## 先理解一件重要的事

Ngrok 有兩種常見用法：

- 臨時網址：適合測試。重開 Ngrok 或重開電腦後，網址可能改變。
- Static domain：適合長期使用。網址固定，LINE Developers 的 Webhook URL 不用每天改。

如果你只是先試玩，可以用臨時網址。  
如果你要放進家庭群組長期使用，建議設定 static domain，或直接使用 n8n Cloud。

## 基本測試流程

假設你的 n8n 在本機：

```text
http://localhost:5678
```

啟動 Ngrok：

```bash
ngrok http 5678
```

畫面會出現一個 `https://...` 開頭的公開網址，例如：

```text
https://example.ngrok-free.app
```

你的 LINE webhook URL 就是：

```text
https://example.ngrok-free.app/webhook/linebot
```

把這個網址貼到 LINE Developers 的 Webhook URL。

## 第一次安裝 Ngrok 時

第一次使用通常需要：

1. 建立或登入 Ngrok 帳號。
2. 安裝 ngrok。
3. 到 Ngrok dashboard 複製 authtoken。
4. 在電腦上設定 authtoken。

常見指令像這樣：

```bash
ngrok config add-authtoken 你的_ngrok_authtoken
```

Ngrok 介面與指令可能更新，請讓 agent 依照當天官方文件確認。

## 重開機後怎麼辦

如果你使用臨時網址：

1. 先啟動 n8n。
2. 再執行 `ngrok http 5678`。
3. 複製新的 `https://...` 網址。
4. 到 n8n 的 `Webhook` 節點確認 Production URL。
5. 到 LINE Developers 更新 Webhook URL。
6. 按 Verify 測試。

如果網址變了但 LINE Developers 沒更新，LINE 會打到舊網址，bot 就不會回。

## 固定網址建議

若你要長期使用，請 agent 幫你設定 Ngrok static domain。大方向是：

1. 登入 Ngrok 帳號。
2. 在 Ngrok dashboard 建立 static domain。
3. 讓本機 Ngrok 使用該 static domain 啟動。
4. 將 n8n 的公開 webhook base URL 設成該固定網址。
5. 將 LINE Developers 的 Webhook URL 設為：

```text
https://你的固定-ngrok-domain/webhook/linebot
```

Ngrok 的方案、介面與指令可能會更新。請 agent 在安裝當天查 Ngrok 官方文件確認最新指令。

常見啟動方式可能類似：

```bash
ngrok http --url=你的固定-ngrok-domain 5678
```

有些版本或文件可能使用 `--domain`。如果指令失敗，不要硬猜，請把錯誤貼給 agent，請它查目前 Ngrok 正確指令。

## n8n 的 WEBHOOK_URL

如果 n8n 顯示的 Production URL 仍然是 `localhost`，代表 n8n 不知道自己的公開網址。

本機或 Docker 部署時，通常需要設定：

```text
WEBHOOK_URL=https://你的公開網址/
```

注意最後通常要有 `/`。設定後重啟 n8n，再重新打開 `Webhook` 節點確認 Production URL 是否變成公開網址。

如果你不確定自己是哪種安裝方式，請直接問 agent：

```text
我用本機 n8n 安裝 LINE bot，現在需要設定 Ngrok 和 WEBHOOK_URL。
請先判斷我的 n8n 是怎麼啟動的，再一步一步帶我設定。
```

## 常見錯誤

### LINE Verify 失敗

請檢查：

- n8n 有沒有正在執行。
- Ngrok 有沒有正在執行。
- LINE Developers 裡貼的是 `https://.../webhook/linebot`，不是 `http://localhost:5678/...`。
- workflow 是否已啟用。
- n8n 的 Production URL 是否使用公開網址。

### 昨天可以，今天突然不行

最常見原因是 Ngrok 臨時網址變了。

請重新執行 `ngrok http 5678`，把新的網址更新到 LINE Developers。

### 想不要每天改網址

請設定 Ngrok static domain，或改用 n8n Cloud。
