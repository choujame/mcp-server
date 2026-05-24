# Taiwan Legal MCP Server - Windows 設定腳本
# 在 PowerShell 中執行此腳本即可完成設定

$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonPath = Join-Path $projectPath ".venv\Scripts\python.exe"
$claudeDir = Join-Path $env:USERPROFILE ".claude"
$settingsPath = Join-Path $claudeDir "settings.json"

# 建立 .claude 目錄
New-Item -ItemType Directory -Force -Path $claudeDir | Out-Null

# 讀取現有設定（若存在）
$settings = @{}
if (Test-Path $settingsPath) {
    $settings = Get-Content $settingsPath -Raw | ConvertFrom-Json -AsHashtable
}

# 加入 MCP Server
if (-not $settings.ContainsKey("mcpServers")) {
    $settings["mcpServers"] = @{}
}
$settings["mcpServers"]["taiwan-legal-db"] = @{
    command = $pythonPath
    args    = @("-m", "mcp_server.server")
    cwd     = $projectPath
}

# 寫入設定檔
$settings | ConvertTo-Json -Depth 10 | Set-Content -Path $settingsPath -Encoding UTF8

Write-Host ""
Write-Host "✓ 設定完成！" -ForegroundColor Green
Write-Host "  設定檔：$settingsPath"
Write-Host "  Python：$pythonPath"
Write-Host "  專案：$projectPath"
Write-Host ""
Write-Host "請重新啟動 Claude Desktop，然後在 Code 模式開新 session 測試。"
