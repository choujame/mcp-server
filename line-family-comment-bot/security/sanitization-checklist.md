# 公開前安全檢查清單

這份清單是給想把修改後的專案重新公開到 GitHub 的維護者。

如果你只是安裝使用這個 bot，不需要執行這份清單。

公開到 GitHub 前，請確認：

- [ ] 沒有 `database.sqlite`
- [ ] 沒有 n8n `config`
- [ ] 沒有 n8n log 檔
- [ ] 沒有 `.env`
- [ ] 沒有 LINE channel access token
- [ ] 沒有 LINE channel secret
- [ ] 沒有 OpenAI / Google / OpenRouter / Groq API key
- [ ] 沒有真實家庭成員姓名
- [ ] 沒有 LINE user id、group id、room id
- [ ] 沒有家庭聊天截圖
- [ ] workflow 裡只有 placeholder，不是真實 secret
- [ ] Git history 裡沒有曾經上傳過的 secret

建議執行：

```bash
bash scripts/security-scan.sh
```
