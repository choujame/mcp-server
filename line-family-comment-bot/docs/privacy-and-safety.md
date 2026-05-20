# 隱私與安全

這個 bot 會接觸家庭群組訊息，因此公開、安裝、測試時都要保守一點。

## 不要公開的資料

- LINE channel access token
- LINE channel secret
- LINE channel id
- LINE user id、group id、room id
- API key
- 真實姓名、電話、地址、email
- 家庭群組截圖
- n8n `database.sqlite`
- n8n `config`
- n8n log 檔
- n8n API key
- n8n MCP 連線設定或任何可操作 n8n 的權杖

## 對家人透明

建議先在群組裡告知：

```text
我放了一個自動回覆機器人在群組裡，主要是幫忙回應日常分享。
如果大家覺得不舒服，我可以關掉。
```

## 醫療內容

bot 可以做一般健康資訊整理，但不能做診斷。

遇到胸痛、呼吸困難、意識改變、嚴重過敏、疑似中風、嚴重外傷等狀況，應直接提醒就醫或打當地緊急電話。

## 圖片內容

workflow 的圖片 prompt 已經刻意保守：

- 不猜人物身份。
- 不評論外貌、年齡、胖瘦、健康狀態。
- 不逐字解讀證件、帳單、通知書。

如果你要修改 prompt，請保留這些安全規則。

## n8n API key 與 MCP

n8n API key 或 MCP 連線可能讓 agent 讀取、建立、修改、啟用你的 workflow。這很方便，但也代表權限很大。

一般新手不需要設定 n8n API key 或 MCP。若你只是要安裝這個 bot，建議使用 n8n UI 手動匯入 workflow。

只有在你信任 agent、理解權限風險，而且知道如何撤銷 API key 時，才考慮進階自動部署。
