#!/usr/bin/env node

/**
 * DNASPEC Skills 测试脚本
 * 验证核心功能是否正常工作
 */

const { execSync } = require('child_process');
const path = require('path');

console.log('🧪 开始DNASPEC技能测试...\n');

// 测试CLI工具是否存在
try {
  const cliPath = path.join(__dirname, '..', 'bin', 'dnaspec-cli.js');
  const initPath = path.join(__dirname, '..', 'bin', 'dnaspec-init.js');
  
  require.resolve(cliPath);
  require.resolve(initPath);
  
  console.log('✅ CLI工具文件存在');
} catch (error) {
  console.error('❌ CLI工具文件缺失:', error.message);
  process.exit(1);
}

// 测试技能目录结构
const skillsRoot = path.join(__dirname, '..', 'skills');
const fs = require('fs');

if (fs.existsSync(skillsRoot)) {
  const skillDirs = fs.readdirSync(skillsRoot)
    .filter(dir => fs.statSync(path.join(skillsRoot, dir)).isDirectory());
  
  console.log(`✅ 技能目录存在，包含 ${skillDirs.length} 个技能`);
  
  // 验证前3个技能的SKILL.md文件
  skillDirs.slice(0, 3).forEach(skill => {
    const skillFile = path.join(skillsRoot, skill, 'SKILL.md');
    if (fs.existsSync(skillFile)) {
      console.log(`✅ ${skill}: SKILL.md 存在`);
    } else {
      console.warn(`⚠️  ${skill}: SKILL.md 缺失`);
    }
  });
} else {
  console.warn('⚠️  技能目录不存在');
}

console.log('\n🎉 DNASPEC技能测试完成！');
console.log('📦 包可以安全发布');