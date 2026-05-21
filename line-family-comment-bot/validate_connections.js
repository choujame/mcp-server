#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('🔍 n8n 工作流程連接驗證工具\n');
console.log('=' .repeat(60));

// 讀取工作流程檔案
const workflowPath = '/home/user/mcp-server/line-family-comment-bot/TELEGRAM_BOT_READY.json';

try {
  const workflowContent = fs.readFileSync(workflowPath, 'utf-8');
  const workflow = JSON.parse(workflowContent);

  console.log(`\n✓ 檔案已讀取: ${workflowPath}\n`);

  // 驗證基本信息
  console.log('📋 基本信息:');
  console.log(`   工作流程名稱: ${workflow.name}`);
  console.log(`   節點總數: ${workflow.nodes.length}`);
  console.log(`   連接定義數: ${Object.keys(workflow.connections).length}`);
  console.log('');

  // 列出所有節點
  console.log('📌 所有節點:');
  const nodeMap = {};
  workflow.nodes.forEach((node, index) => {
    nodeMap[node.id] = { name: node.name, type: node.type };
    console.log(`   ${index + 1}. [${node.id}] ${node.name}`);
  });
  console.log('');

  // 驗證所有連接
  console.log('🔗 連接驗證:');
  console.log('');

  let validConnections = 0;
  let totalConnections = 0;
  const connectionDetails = [];

  Object.entries(workflow.connections).forEach(([sourceId, connections]) => {
    // 驗證source節點存在
    if (!nodeMap[sourceId]) {
      console.log(`   ❌ 來源節點不存在: ${sourceId}`);
      return;
    }

    connections.main.forEach((group, groupIndex) => {
      group.forEach((connection, connIndex) => {
        totalConnections++;
        const targetId = connection.node;

        // 驗證target節點存在
        if (!nodeMap[targetId]) {
          console.log(`   ❌ 目標節點不存在: ${sourceId} → ${targetId}`);
          return;
        }

        validConnections++;
        connectionDetails.push({
          from: sourceId,
          to: targetId,
          fromName: nodeMap[sourceId].name,
          toName: nodeMap[targetId].name
        });
      });
    });
  });

  // 顯示所有連接
  connectionDetails.forEach((conn, index) => {
    console.log(`   ✓ 連接 ${index + 1}: [${conn.from}] ${conn.fromName}`);
    console.log(`               ↓`);
    console.log(`               [${conn.to}] ${conn.toName}`);
    console.log('');
  });

  // 驗證連接完整性
  console.log('✅ 連接驗證結果:');
  console.log(`   有效連接: ${validConnections}/${totalConnections}`);

  if (validConnections === totalConnections && totalConnections > 0) {
    console.log(`   ✓ 所有連接都有效！\n`);
  } else {
    console.log(`   ❌ 有連接無效！\n`);
  }

  // 驗證工作流程完整性
  console.log('🔍 工作流程完整性檢查:');

  // 檢查是否有Webhook入口
  const hasWebhook = workflow.nodes.some(n => n.type === 'n8n-nodes-base.webhook');
  console.log(`   ${hasWebhook ? '✓' : '❌'} Webhook入口存在`);

  // 檢查是否有Telegram輸出
  const hasTelegram = workflow.nodes.some(n => n.type === 'n8n-nodes-base.telegram');
  console.log(`   ${hasTelegram ? '✓' : '❌'} Telegram輸出存在`);

  // 檢查是否有醫療檢測
  const parseNode = workflow.nodes.find(n => n.id === 'parse_message');
  const hasMedicalDetection = parseNode && parseNode.parameters.functionCode.includes('is_medical');
  console.log(`   ${hasMedicalDetection ? '✓' : '❌'} 醫療檢測邏輯存在`);

  // 檢查Branch Switch是否有兩條路徑
  const branchNode = workflow.nodes.find(n => n.id === 'branch_switch');
  const hasBothPaths = branchNode && workflow.connections.branch_switch.main.length === 2;
  console.log(`   ${hasBothPaths ? '✓' : '❌'} 分支路由（醫療+一般）存在`);

  // 檢查Groq API配置
  const groqNodes = workflow.nodes.filter(n => n.type === 'n8n-nodes-base.httpRequest');
  const bothGroqConfigured = groqNodes.length === 2 &&
    groqNodes.every(n => n.parameters.url && n.parameters.url.includes('groq.com'));
  console.log(`   ${bothGroqConfigured ? '✓' : '❌'} 兩個Groq API節點已配置`);

  console.log('');
  console.log('=' .repeat(60));

  // 最終結果
  const allChecks = [
    hasWebhook,
    hasTelegram,
    hasMedicalDetection,
    hasBothPaths,
    bothGroqConfigured,
    validConnections === totalConnections && totalConnections > 0
  ];

  const passedChecks = allChecks.filter(x => x).length;
  const totalChecks = allChecks.length;

  console.log(`\n📊 最終驗證: ${passedChecks}/${totalChecks} 檢查通過\n`);

  if (passedChecks === totalChecks) {
    console.log('✅✅✅ 工作流程完全就緒！所有節點和連接都正確！✅✅✅\n');
    process.exit(0);
  } else {
    console.log('⚠️ 工作流程還有問題，請檢查上述結果。\n');
    process.exit(1);
  }

} catch (error) {
  console.error(`❌ 錯誤: ${error.message}`);
  console.error(`檔案路徑: ${workflowPath}`);
  process.exit(1);
}
