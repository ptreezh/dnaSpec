#!/usr/bin/env node

/**
 * DNASPEC初始化脚本 - 简化版
 * 用于安装后配置和环境检测
 */

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const VERSION = '2.0.0';

console.log('🔧 DNASPEC Context System v2.0.0 安装程序');
console.log('='.repeat(50));

// 检测已安装的AI CLI工具
function detectAICLITools() {
  console.log('\n🔍 检测AI CLI工具...\n');
  
  const toolChecks = [
    { name: 'Claude Code', command: 'claude --version' },
    { name: 'Stigmergy', command: 'stigmergy --version' },
    { name: 'npx', command: 'npx --version' },
    { name: 'Node.js', command: 'node --version' },
    { name: 'npm', command: 'npm --version' },
    { name: 'Git', command: 'git --version' }
  ];
  
  for (const tool of toolChecks) {
    try {
      const result = execSync(tool.command, { 
        encoding: 'utf8', 
        stdio: 'pipe' 
      }).trim();
      console.log(`✅ ${tool.name}: ${result}`);
    } catch (error) {
      console.log(`❌ ${tool.name}: 未安装`);
    }
  }
}

// 检测Python环境
function checkPythonEnvironment() {
  console.log('\n🐍 检测Python环境...\n');
  
  try {
    const pythonVersion = execSync('python --version', { 
      encoding: 'utf8', 
      stdio: 'pipe' 
    }).trim();
    console.log(`✅ Python: ${pythonVersion}`);
    
    try {
      const pipVersion = execSync('pip --version', { 
        encoding: 'utf8', 
        stdio: 'pipe' 
      }).trim();
      console.log(`✅ pip: ${pipVersion.split(' ')[1]}`);
      return true;
    } catch (error) {
      console.log('❌ pip: 未找到');
      return false;
    }
  } catch (error) {
    console.log('❌ Python: 未安装或不在PATH中');
    return false;
  }
}

// 生成配置文件
function generateConfig() {
  console.log('\n⚙️  生成配置文件...\n');
  
  const projectPath = path.join(__dirname, '..');
  const config = {
    version: VERSION,
    timestamp: new Date().toISOString(),
    installationMode: 'npm-global',
    projectPath: projectPath
  };
  
  const configPath = path.join(projectPath, 'dnaspec-config.json');
  
  try {
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
    console.log('✅ 配置文件生成成功:', configPath);
    return true;
  } catch (error) {
    console.log('❌ 配置文件生成失败:', error.message);
    return false;
  }
}

// 显示部署指南
function showDeploymentGuide() {
  console.log('\n🚀 DNASPEC v2.0.0 部署指南\n');
  console.log('='.repeat(50));
  
  console.log('\n📋 双部署系统选项:\n');
  
  console.log('1️⃣  标准化部署 (推荐用于Claude Code用户)');
  console.log('   创建技能目录: mkdir -p .claude/skills');
  console.log('   复制技能文件: cp -r skills/* .claude/skills/');
  
  console.log('\n2️⃣  CLI模式部署 (推荐用于命令行用户)');
  console.log('   直接使用: dnaspec slash <技能名>');
  console.log('   例如: dnaspec slash context-analysis "分析文本"');
  
  console.log('\n3️⃣  Stigmergy集成 (跨CLI协作)');
  console.log('   检查可用性: dnaspec integrate --list');
  console.log('   启用集成: dnaspec integrate --stigmergy');
  
  console.log('\n🛠️  常用命令:\n');
  console.log('   dnaspec --help           # 查看帮助');
  console.log('   dnaspec list             # 列出技能');
  console.log('   dnaspec tips             # 显示提示');
  console.log('   dnaspec validate         # 验证安装');
  console.log('   dnaspec deploy           # 部署技能');
  
  console.log('\n📚 技能列表:\n');
  const skills = [
    'context-analysis       - 分析上下文质量',
    'context-optimization   - 优化上下文',
    'cognitive-template     - 认知模板应用',
    'agent-creator          - 创建AI智能体',
    'task-decomposer        - 分解复杂任务',
    'constraint-generator   - 生成约束',
    'api-checker           - API接口检查',
    'modulizer            - 系统模块化',
    'system-architect      - 系统架构设计'
  ];
  
  skills.forEach(skill => console.log(`   • ${skill}`));
  
  console.log('\n💡 使用示例:\n');
  console.log('   # 分析代码质量');
  console.log('   dnaspec slash context-analysis "这段代码质量如何？"');
  console.log('');
  console.log('   # 设计系统架构');
  console.log('   dnaspec slash architect "设计一个电商系统"');
  console.log('');
  console.log('   # 创建智能体');
  console.log('   dnaspec slash agent-creator "创建一个数据分析助手"');
  
  console.log('\n🔗 更多信息:');
  console.log('   项目地址: https://github.com/ptreezh/dnaSpec');
  console.log('   文档: https://github.com/ptreezh/dnaSpec#readme');
  console.log('   问题反馈: https://github.com/ptreezh/dnaSpec/issues');
}

// 主函数
function main() {
  try {
    // 检测环境
    detectAICLITools();
    checkPythonEnvironment();
    
    // 生成配置文件
    generateConfig();
    
    // 显示部署指南
    showDeploymentGuide();
    
    // 完成提示
    console.log('\n🎉 DNASPEC安装完成！\n');
    console.log('下一步:');
    console.log('1. 选择部署模式 (标准化 或 CLI)');
    console.log('2. 运行: dnaspec --help 查看所有命令');
    console.log('3. 开始使用: dnaspec slash <技能名>');
    
    console.log('\n💡 提示: 使用 "dnaspec tips" 随时查看使用指南');
    
  } catch (error) {
    console.error('\n❌ 安装过程中出错:', error.message);
    console.error('但包已安装成功，DNASPEC功能仍可正常使用');
    console.error('问题反馈: https://github.com/ptreezh/dnaSpec/issues');
  }
}

// 如果直接运行此脚本
if (require.main === module) {
  main();
}

module.exports = { main, detectAICLITools, checkPythonEnvironment };