@echo off
REM LINE Family Comment Bot - Windows 部署脚本
REM 使用方式：双击运行此脚本

setlocal enabledelayedexpansion

echo.
echo ╔═══════════════════════════════════════════════════════╗
echo ║   LINE Family Comment Bot - Windows 自動部署         ║
echo ╚═══════════════════════════════════════════════════════╝
echo.

REM 檢查 Node.js
echo [1/5] 檢查 Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Node.js 未安裝。請先從 https://nodejs.org/ 安裝
    pause
    exit /b 1
)
echo ✓ Node.js 已安裝:
node --version

REM 安裝 n8n
echo.
echo [2/5] 安裝 n8n...
npm install -g n8n
if errorlevel 1 (
    echo ✗ n8n 安裝失敗
    pause
    exit /b 1
)
echo ✓ n8n 安裝完成

REM 檢查配置檔案
echo.
echo [3/5] 檢查配置檔案...
if not exist "n8n-line-bot-config.json" (
    echo ✗ 找不到 n8n-line-bot-config.json
    pause
    exit /b 1
)
echo ✓ 配置檔案正確

REM 啟動 n8n
echo.
echo [4/5] 啟動 n8n...
start cmd /k "n8n start"
timeout /t 3

REM 打開瀏覽器
echo.
echo [5/5] 打開 n8n 管理界面...
start http://localhost:5678

echo.
echo ╔═══════════════════════════════════════════════════════╗
echo ║              部署完成！後續步驟：                    ║
echo ╠═══════════════════════════════════════════════════════╣
echo ║ 1. n8n 應該在幾秒內打開（http://localhost:5678）    ║
echo ║ 2. 匯入 workflows/LINE_FAMILY_COMMENT_BOT.public.json ║
echo ║ 3. 在 n8n 中配置 LINE Config 節點                   ║
echo ║ 4. 配置 LLM 節點（已用 Groq）                       ║
echo ║ 5. 複製 Webhook Production URL 到 LINE Developers    ║
echo ║ 6. 啟用 workflow 並測試                              ║
echo ╚═══════════════════════════════════════════════════════╝
echo.

pause
