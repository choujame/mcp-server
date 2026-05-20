# 發布到 GitHub 前

這份文件是給想修改本專案、再發布成自己公開 repo 的維護者或進階使用者。

如果你只是要安裝使用這個 bot，不需要看這份文件。

## 建議做法

請只把 `line-family-comment-bot/` 這個乾淨資料夾上傳到 GitHub。

不要把上一層 n8n 資料夾整包上傳，因為上一層可能有：

- n8n 資料庫
- n8n config
- log 檔
- binaryData
- 私人 credentials

## 上傳前檢查

在 `line-family-comment-bot/` 裡執行：

```bash
bash scripts/security-scan.sh
```

如果看到可疑 token，先停下來，不要 push。

## 建議 repo 名稱

可以用：

```text
line-family-comment-bot
```

這個名字比「長輩 bot」溫和，也比較不會讓家人覺得被標籤化。
