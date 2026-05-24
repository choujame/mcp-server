# Taiwan Legal MCP Server - Windows setup script
# Run in PowerShell: powershell -ExecutionPolicy Bypass -File setup-mcp-windows.ps1

$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonPath  = Join-Path $projectPath ".venv\Scripts\python.exe"
$claudeDir   = Join-Path $env:USERPROFILE ".claude"
$settingsPath = Join-Path $claudeDir "settings.json"

New-Item -ItemType Directory -Force -Path $claudeDir | Out-Null

$mcpEntry = @"
{
  "mcpServers": {
    "taiwan-legal-db": {
      "command": "$($pythonPath -replace '\\','\\\\',2)",
      "args": ["-m", "mcp_server.server"],
      "cwd": "$($projectPath -replace '\\','\\\\',2)"
    }
  }
}
"@

# Merge with existing settings if present
if (Test-Path $settingsPath) {
    $existing = Get-Content $settingsPath -Raw | ConvertFrom-Json
    $newEntry  = $mcpEntry | ConvertFrom-Json

    if (-not ($existing | Get-Member -Name mcpServers -MemberType NoteProperty)) {
        $existing | Add-Member -Name mcpServers -MemberType NoteProperty -Value @{}
    }
    $existing.mcpServers | Add-Member -Name "taiwan-legal-db" -MemberType NoteProperty -Value $newEntry.mcpServers."taiwan-legal-db" -Force
    $existing | ConvertTo-Json -Depth 10 | Out-File -FilePath $settingsPath -Encoding utf8
} else {
    $mcpEntry | Out-File -FilePath $settingsPath -Encoding utf8
}

Write-Host "Done: $settingsPath"
Write-Host "Python: $pythonPath"
Write-Host "Project: $projectPath"
