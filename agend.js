#!/usr/bin/env node
/**
 * agend.js — AgEnD 多代理人艦隊 MCP 伺服器
 * 純 Node.js 內建模組，無需 npm 安裝任何套件。
 * 參考: github.com/suzuke/AgEnD
 *
 * 啟動方式: node agend.js
 * Claude Code 設定 (claude_desktop_config.json):
 *   { "mcpServers": { "agend": { "command": "node", "args": ["/path/to/agend.js"] } } }
 */

'use strict';

const readline = require('readline');
const { spawnSync, execFileSync } = require('child_process');

// ── 工具定義 ─────────────────────────────────────────────────────────────────

const PREFIX = 'agend-';

const TOOLS = [
  {
    name: 'agend_list_agents',
    description: '列出所有正在執行的 AgEnD 代理人 tmux 工作階段。',
    inputSchema: { type: 'object', properties: {}, required: [] },
  },
  {
    name: 'agend_start_agent',
    description: '在隔離的 tmux 工作階段中啟動新代理人。',
    inputSchema: {
      type: 'object',
      properties: {
        name: { type: 'string', description: '代理人唯一名稱（例如 "backend"）' },
        project_path: { type: 'string', description: '專案目錄的絕對路徑' },
        cli: {
          type: 'string',
          description: 'CLI 後端：claude | gemini | codex | opencode（預設：claude）',
          default: 'claude',
        },
      },
      required: ['name', 'project_path'],
    },
  },
  {
    name: 'agend_send_message',
    description: '向指定代理人的 tmux 工作階段傳送提示訊息。',
    inputSchema: {
      type: 'object',
      properties: {
        name: { type: 'string', description: '代理人名稱' },
        message: { type: 'string', description: '要傳送的訊息內容' },
      },
      required: ['name', 'message'],
    },
  },
  {
    name: 'agend_get_output',
    description: '擷取代理人最近的終端機輸出。',
    inputSchema: {
      type: 'object',
      properties: {
        name: { type: 'string', description: '代理人名稱' },
        lines: { type: 'number', description: '擷取行數（預設：50）', default: 50 },
      },
      required: ['name'],
    },
  },
  {
    name: 'agend_stop_agent',
    description: '終止代理人的 tmux 工作階段。',
    inputSchema: {
      type: 'object',
      properties: {
        name: { type: 'string', description: '代理人名稱' },
      },
      required: ['name'],
    },
  },
  {
    name: 'agend_broadcast',
    description: '向所有正在執行的代理人廣播訊息。',
    inputSchema: {
      type: 'object',
      properties: {
        message: { type: 'string', description: '廣播內容' },
      },
      required: ['message'],
    },
  },
];

// ── tmux 輔助函式 ─────────────────────────────────────────────────────────────

function tmuxAvailable() {
  const r = spawnSync('which', ['tmux'], { encoding: 'utf8' });
  return r.status === 0;
}

function tmux(...args) {
  const r = spawnSync('tmux', args, { encoding: 'utf8' });
  return { ok: r.status === 0, stdout: (r.stdout || '').trim(), stderr: (r.stderr || '').trim() };
}

function listAgents() {
  if (!tmuxAvailable()) return { error: 'tmux 未安裝' };
  const r = tmux('list-sessions', '-F', '#{session_name}|#{session_id}|#{session_created}');
  if (!r.ok) {
    if (r.stderr.includes('no server running') || r.stderr.includes('No such file')) return [];
    return { error: r.stderr };
  }
  return r.stdout.split('\n')
    .filter(l => l.startsWith(PREFIX))
    .map(l => {
      const [session, id, created] = l.split('|');
      return { name: session.slice(PREFIX.length), session, id, created };
    });
}

function startAgent(name, projectPath, cli = 'claude') {
  if (!tmuxAvailable()) return { error: 'tmux 未安裝' };
  const session = PREFIX + name;
  const check = tmux('has-session', '-t', session);
  if (check.ok) return { error: `代理人 '${name}' 已在執行中` };

  const { existsSync, statSync } = require('fs');
  if (!existsSync(projectPath) || !statSync(projectPath).isDirectory()) {
    return { error: `目錄不存在: ${projectPath}` };
  }

  const r = tmux('new-session', '-d', '-s', session, '-c', projectPath, cli);
  if (!r.ok) return { error: r.stderr };
  return { status: 'started', agent: name, session, cli };
}

function sendMessage(name, message) {
  if (!tmuxAvailable()) return { error: 'tmux 未安裝' };
  const session = PREFIX + name;
  if (!tmux('has-session', '-t', session).ok) return { error: `代理人 '${name}' 未在執行` };
  const r = tmux('send-keys', '-t', session, message, 'Enter');
  if (!r.ok) return { error: r.stderr };
  return { status: 'sent', agent: name };
}

function getOutput(name, lines = 50) {
  if (!tmuxAvailable()) return { error: 'tmux 未安裝' };
  const session = PREFIX + name;
  if (!tmux('has-session', '-t', session).ok) return { error: `代理人 '${name}' 未在執行` };
  const r = tmux('capture-pane', '-p', '-t', session, '-S', `-${lines}`);
  if (!r.ok) return { error: r.stderr };
  return { agent: name, output: r.stdout };
}

function stopAgent(name) {
  if (!tmuxAvailable()) return { error: 'tmux 未安裝' };
  const session = PREFIX + name;
  if (!tmux('has-session', '-t', session).ok) return { error: `代理人 '${name}' 未在執行` };
  const r = tmux('kill-session', '-t', session);
  if (!r.ok) return { error: r.stderr };
  return { status: 'stopped', agent: name };
}

function broadcast(message) {
  if (!tmuxAvailable()) return { error: 'tmux 未安裝' };
  const agents = listAgents();
  if (!Array.isArray(agents)) return agents;
  if (agents.length === 0) return { status: '目前沒有執行中的代理人' };
  return agents.map(a => {
    const r = tmux('send-keys', '-t', a.session, message, 'Enter');
    return { agent: a.name, ok: r.ok, error: r.ok ? null : r.stderr };
  });
}

// ── 工具分派 ─────────────────────────────────────────────────────────────────

function callTool(name, args) {
  switch (name) {
    case 'agend_list_agents':    return listAgents();
    case 'agend_start_agent':    return startAgent(args.name, args.project_path, args.cli);
    case 'agend_send_message':   return sendMessage(args.name, args.message);
    case 'agend_get_output':     return getOutput(args.name, args.lines);
    case 'agend_stop_agent':     return stopAgent(args.name);
    case 'agend_broadcast':      return broadcast(args.message);
    default:                     return { error: `未知工具: ${name}` };
  }
}

// ── MCP JSON-RPC over stdio ───────────────────────────────────────────────────

function send(obj) {
  process.stdout.write(JSON.stringify(obj) + '\n');
}

function handle(msg) {
  const { jsonrpc, id, method, params } = msg;

  if (method === 'initialize') {
    return send({
      jsonrpc, id,
      result: {
        protocolVersion: '2024-11-05',
        capabilities: { tools: {} },
        serverInfo: { name: 'agend', version: '1.0.0' },
      },
    });
  }

  if (method === 'notifications/initialized') return; // 不需回應

  if (method === 'ping') {
    return send({ jsonrpc, id, result: {} });
  }

  if (method === 'tools/list') {
    return send({ jsonrpc, id, result: { tools: TOOLS } });
  }

  if (method === 'tools/call') {
    const result = callTool(params.name, params.arguments || {});
    return send({
      jsonrpc, id,
      result: {
        content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
      },
    });
  }

  // 未知方法
  send({
    jsonrpc, id,
    error: { code: -32601, message: `Method not found: ${method}` },
  });
}

// ── 主程式 ────────────────────────────────────────────────────────────────────

const rl = readline.createInterface({ input: process.stdin, terminal: false });

rl.on('line', line => {
  line = line.trim();
  if (!line) return;
  try {
    handle(JSON.parse(line));
  } catch (e) {
    send({ jsonrpc: '2.0', id: null, error: { code: -32700, message: 'Parse error' } });
  }
});

rl.on('close', () => process.exit(0));
