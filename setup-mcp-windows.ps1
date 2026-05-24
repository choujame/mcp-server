# Taiwan Legal MCP Server - Windows setup script
$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $projectPath ".venv\Scripts\python.exe"

& $python -c @"
import json, os, sys

project = r'$projectPath'
python  = r'$python'
path    = os.path.join(os.environ['USERPROFILE'], '.claude', 'settings.json')
os.makedirs(os.path.dirname(path), exist_ok=True)

settings = {}
if os.path.exists(path):
    try:
        settings = json.loads(open(path, encoding='utf-8').read())
    except Exception:
        pass

settings.setdefault('mcpServers', {})['taiwan-legal-db'] = {
    'command': python,
    'args': ['-m', 'mcp_server.server'],
    'cwd': project
}

open(path, 'w', encoding='utf-8').write(json.dumps(settings, indent=2, ensure_ascii=False))
print('Done:', path)
print('Python:', python)
"@
