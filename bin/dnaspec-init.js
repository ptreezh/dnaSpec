#!/usr/bin/env node

/**
 * DNASPEC初始化脚本
 * 用于安装后配置和环境检测
 */

const { execSync } = require('child_process');
const path = require('path');

// 尝试加载可选依赖，如果失败则使用简化版本
let fsExtra, inquirer;
try {
  fsExtra = require('fs-extra');
  inquirer = require('inquirer');
} catch (error) {
  console.log('⚠️  部分依赖未安装，将使用简化模式');
  fsExtra = require('fs');
  inquirer = null;
}

const VERSION = '2.0.0';

// 检测已安装的AI CLI工具
function detectAICLITools() {
  const tools = [];
  
  // 检查常见的AI CLI工具
  const toolChecks = [
    { name: 'Claude Code', command: 'claude --version' },
    { name: 'Stigmergy', command: 'stigmergy --version' },
    { name: 'npx', command: 'npx --version' },
    { name: 'Node.js', command: 'node --version' },
    { name: 'npm', command: 'npm --version' },
    { name: 'Git', command: 'git --version' }
  ];
  
  console.log('🔍 检测AI CLI工具...\n');
  
  for (const tool of toolChecks) {
    try {
      const result = execSync(tool.command, { 
        encoding: 'utf8', 
        stdio: 'pipe' 
      }).trim();
      console.log(`✅ ${tool.name}: ${result}`);
      tools.push({ name: tool.name, available: true, version: result });
    } catch (error) {
      console.log(`❌ ${tool.name}: 未安装`);
      tools.push({ name: tool.name, available: false, version: null });
    }
  }
  
  return tools;
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

// 安装Python依赖
function installPythonDependencies() {
  console.log('\n📦 安装Python依赖...\n');
  
  try {
    execSync('pip install -e .', {
      encoding: 'utf8',
      stdio: 'inherit',
      cwd: path.join(__dirname, '..')
    });
    console.log('✅ Python依赖安装成功');
    return true;
  } catch (error) {
    console.log('❌ Python依赖安装失败');
    console.log('请手动运行: pip install -e .');
    return false;
  }
}

// 生成配置文件
function generateConfig(tools, projectPath) {
  console.log('\n⚙️  生成配置文件...\n');
  
  const config = {
    version: VERSION,
    timestamp: new Date().toISOString(),
    detectedTools: tools,
    projectPath: projectPath,
    installationMode: 'npm-global'
  };
  
  const configPath = path.join(projectPath, 'dnaspec-config.json');
  
  try {
    fsExtra.writeJsonSync(configPath, config, { spaces: 2 });
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

// 交互式安装流程
async function interactiveSetup() {
  console.log('\n🎯 DNASPEC v2.0.0 交互式安装向导\n');
  
  if (!inquirer) {
    console.log('💡 inquirer未安装，使用默认设置');
    console.log('将检测工具、安装依赖、显示指南\n');
    return {
      detectTools: true,
      installDeps: true,
      showGuide: true
    };
  }
  
  const answers = await inquirer.prompt([
    {
      type: 'confirm',
      name: 'detectTools',
      message: '是否检测已安装的AI CLI工具？',
      default: true
    },
    {
      type: 'confirm', 
      name: 'installDeps',
      message: '是否安装Python依赖？',
      default: true
    },
    {
      type: 'confirm',
      name: 'showGuide',
      message: '是否显示部署指南？',
      default: true
    }
  ]);
  
  return answers;
}

// 主函数
async function main() {
  console.log('🔧 DNASPEC Context System v2.0.0 安装程序');
  console.log('=' .repeat(50));
  
  try {
    // 检测环境
    const tools = detectAICLITools();
    const pythonAvailable = checkPythonEnvironment();
    
    // 交互式选择
    const answers = await interactiveSetup();
    
    let depsInstalled = false;
    
    if (answers.installDeps && pythonAvailable) {
      depsInstalled = installPythonDependencies();
    }
    
    // 生成配置文件
    const projectPath = path.join(__dirname, '..');
    generateConfig(tools, projectPath);
    
    // 显示部署指南
    if (answers.showGuide) {
      showDeploymentGuide();
    }
    
    // 完成提示
    console.log('\n🎉 DNASPEC安装完成！\n');
    console.log('下一步:');
    console.log('1. 选择部署模式 (标准化 或 CLI)');
    console.log('2. 运行: dnaspec --help 查看所有命令');
    console.log('3. 开始使用: dnaspec slash <技能名>');
    
    console.log('\n💡 提示: 使用 "dnaspec tips" 随时查看使用指南');
    
  } catch (error) {
    console.error('\n❌ 安装过程中出错:', error.message);
    console.error('请查看错误信息并手动解决，或提交issue到:');
    console.error('https://github.com/ptreezh/dnaSpec/issues');
    process.exit(1);
  }
}

// 如果直接运行此脚本
if (require.main === module) {
  main();
}

module.exports = { main, detectAICLITools, checkPythonEnvironment };