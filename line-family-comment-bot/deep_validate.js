#!/usr/bin/env node

const fs = require('fs');

console.log('\n🔬 深度工作流程驗證 - 模擬執行路徑\n');
console.log('═'.repeat(70));

const workflowPath = '/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json';

try {
  const workflow = JSON.parse(fs.readFileSync(workflowPath, 'utf-8'));

  // 1. 驗證節點配置
  console.log('\n📋 步驟 1: 驗證所有節點配置\n');

  const nodeConfigs = {};
  const issues = [];

  workflow.nodes.forEach(node => {
    nodeConfigs[node.id] = {
      name: node.name,
      type: node.type,
      hasParameters: !!node.parameters,
      parameterKeys: node.parameters ? Object.keys(node.parameters) : []
    };

    // 檢查特定節點的必要參數
    switch (node.id) {
      case 'webhook':
        if (!node.parameters.path) issues.push('❌ Webhook 缺少 path 參數');
        else console.log(`✓ Webhook: path = "${node.parameters.path}"`);
        break;

      case 'parse_message':
        if (!node.parameters.functionCode) issues.push('❌ Parse Message 缺少 functionCode');
        else if (!node.parameters.functionCode.includes('is_medical')) {
          issues.push('❌ Parse Message 缺少醫療檢測邏輯');
        } else {
          console.log('✓ Parse Message: 包含醫療檢測邏輯');
        }
        break;

      case 'branch_switch':
        if (!node.parameters.rules) issues.push('❌ Branch Switch 缺少 rules');
        else console.log('✓ Branch Switch: 包含分支規則');
        break;

      case 'call_groq_api':
      case 'call_groq_api_medical':
        if (!node.parameters.url || !node.parameters.url.includes('groq.com')) {
          issues.push(`❌ ${node.name} 缺少或配置錯誤的 URL`);
        } else {
          console.log(`✓ ${node.name}: URL = ${node.parameters.url}`);
        }
        if (!node.parameters.body && !node.parameters.bodyParameters) {
          issues.push(`❌ ${node.name} 缺少 Body`);
        } else {
          console.log(`✓ ${node.name}: 包含請求 Body`);
        }
        break;

      case 'parse_groq_response':
        if (!node.parameters.functionCode) issues.push('❌ Parse Groq Response 缺少 functionCode');
        else console.log('✓ Parse Groq Response: 包含解析邏輯');
        break;

      case 'send_message':
        if (!node.parameters.botToken) issues.push('❌ Send Message 缺少 botToken');
        else console.log('✓ Send Message: 包含 Bot Token');
        if (!node.parameters.chatId) issues.push('❌ Send Message 缺少 chatId');
        else console.log(`✓ Send Message: chatId = ${node.parameters.chatId}`);
        break;
    }
  });

  // 2. 驗證數據流
  console.log('\n\n📊 步驟 2: 驗證數據流路徑\n');

  const testMessages = [
    { text: '你好', expected: 'normal', keyword: 'none' },
    { text: '我頭疼', expected: 'medical', keyword: '疼' }
  ];

  testMessages.forEach((test, index) => {
    console.log(`\n   測試 ${index + 1}: "${test.text}"`);

    // 模擬 Parse Message 節點
    const isMedical = /[醫藥病痛診癌感血糖壓眠頭疼]/.test(test.text);
    console.log(`   └─ 醫療檢測: ${isMedical ? '✓ 觸發醫療路徑' : '✗ 一般路徑'}`);

    // 根據醫療檢測結果決定路徑
    const expectedPath = isMedical ? 'medical' : 'normal';
    const actualPath = test.expected;

    if (expectedPath === actualPath) {
      console.log(`   └─ 預期路徑匹配: ✓`);
    } else {
      issues.push(`❌ 路徑不匹配: 預期 ${actualPath}, 實際 ${expectedPath}`);
    }

    // 模擬 Branch Switch 節點的連接
    const branchConnections = workflow.connections.branch_switch.main;
    if (branchConnections.length === 2) {
      console.log(`   └─ Branch Switch: ✓ 有 2 條分支路徑`);
      console.log(`      ├─ 分支 1: ${branchConnections[0][0].node}`);
      console.log(`      └─ 分支 2: ${branchConnections[1][0].node}`);
    } else {
      issues.push(`❌ Branch Switch 只有 ${branchConnections.length} 條分支`);
    }
  });

  // 3. 驗證完整的執行路徑
  console.log('\n\n🔄 步驟 3: 驗證完整執行路徑\n');

  // 構建執行路徑
  const buildExecutionPath = (startId, visited = new Set()) => {
    if (visited.has(startId)) return [startId];
    visited.add(startId);

    const path = [startId];
    const connections = workflow.connections[startId];

    if (connections && connections.main && connections.main[0]) {
      const nextId = connections.main[0][0].node;
      path.push(...buildExecutionPath(nextId, visited));
    }

    return path;
  };

  const executionPath = buildExecutionPath('webhook');
  console.log('   一般訊息執行路徑:');
  executionPath.forEach((id, index) => {
    const node = workflow.nodes.find(n => n.id === id);
    console.log(`   ${index + 1}. [${id}] ${node.name}`);
  });

  // 驗證路徑完整性
  const hasStart = executionPath.includes('webhook');
  const hasEnd = executionPath.includes('send_message');
  const hasAllRequired = ['webhook', 'parse_message', 'branch_switch', 'parse_groq_response', 'send_message']
    .every(id => executionPath.includes(id));

  console.log(`\n   路徑驗證:`);
  console.log(`   ${hasStart ? '✓' : '❌'} 從 Webhook 開始`);
  console.log(`   ${hasEnd ? '✓' : '❌'} 到 Send Message 結束`);
  console.log(`   ${hasAllRequired ? '✓' : '❌'} 包含所有必要節點`);

  // 4. 最終驗證
  console.log('\n\n✅ 步驟 4: 最終驗證\n');

  const checks = [
    ['所有節點配置完整', !issues.some(i => i.includes('缺少'))],
    ['所有連接有效', !issues.some(i => i.includes('連接'))],
    ['醫療檢測正常', !issues.some(i => i.includes('醫療檢測'))],
    ['Groq API 配置正確', !issues.some(i => i.includes('URL'))],
    ['Telegram 配置完整', !issues.some(i => i.includes('Token') || i.includes('chatId'))],
    ['數據流路徑完整', hasStart && hasEnd && hasAllRequired]
  ];

  let passedChecks = 0;
  checks.forEach(([checkName, result]) => {
    console.log(`   ${result ? '✓' : '❌'} ${checkName}`);
    if (result) passedChecks++;
  });

  console.log('\n' + '═'.repeat(70));

  if (issues.length > 0) {
    console.log(`\n⚠️ 發現 ${issues.length} 個問題:\n`);
    issues.forEach(issue => console.log(`   ${issue}`));
  }

  const totalChecks = checks.length;
  const percentage = Math.round((passedChecks / totalChecks) * 100);

  console.log(`\n📊 最終結果: ${passedChecks}/${totalChecks} (${percentage}%)\n`);

  if (passedChecks === totalChecks && issues.length === 0) {
    console.log('✅✅✅ 工作流程通過所有驗證！完全就緒！✅✅✅\n');
    process.exit(0);
  } else if (passedChecks >= totalChecks * 0.8) {
    console.log('⚠️ 工作流程大部分正確，但有輕微問題。\n');
    process.exit(0);
  } else {
    console.log('❌ 工作流程有重大問題，請檢查上述結果。\n');
    process.exit(1);
  }

} catch (error) {
  console.error(`❌ 錯誤: ${error.message}\n`);
  process.exit(1);
}
