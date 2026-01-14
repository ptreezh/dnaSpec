#!/usr/bin/env node

/**
 * DNASPEC CLI入口点
 * 提供命令行接口来使用DNASPEC技能
 * 
 * 版本: Dynamic from package.json
 * 支持的功能:
 * - 双部署系统（标准化 + Slash命令）
 * - 13种上下文工程技能
 * - AI安全工作流
 * - Git集成
 */

const { execSync, spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// 尝试加载可选依赖，如果失败则使用简化版本
let fsExtra, commander;
try {
  fsExtra = require('fs-extra');
  commander = require('commander');
} catch (error) {
  console.log('⚠️  部分依赖未安装，将使用简化模式');
  console.log('请运行: npm install 安装所有依赖\n');
  fsExtra = require('fs');
  commander = null;
}

// 读取package.json获取版本信息
const packageJson = require(path.join(__dirname, '..', 'package.json'));
const VERSION = packageJson.version;  // Dynamic from package.json
const DESCRIPTION = 'DNA SPEC Context System (dnaspec) - Context Engineering Skills';

// 简化的命令行解析器（当commander不可用时）
function simpleCommandParser() {
  const args = process.argv.slice(2);
  const command = args[0] || '';
  const subcommand = args[1] || '';
  
  return {
    command,
    subcommand,
    args: args.slice(1),
    hasCommand: !!command
  };
}

// 定义program变量
const program = commander || null;

// 简化的帮助函数
function showSimpleHelp() {
  console.log(DESCRIPTION);
  console.log(`版本: ${VERSION}\n`);
  console.log('用法: dnaspec <命令> [选项]');
  console.log('\n可用命令:');
  console.log('  --version              显示版本信息');
  console.log('  --help                 显示此帮助信息');
  console.log('  tips                   显示使用提示');
  console.log('  list                   列出可用技能');
  console.log('  exec <命令>            执行DNASPEC技能命令');
  console.log('  shell                  启动交互式Shell');
  console.log('  slash                  Slash命令模式');
  console.log('  validate               验证DNASPEC集成');
  console.log('  deploy                 智能扩展部署');
  console.log('  integrate              智能集成和部署');
  console.log('  security               安全测试和验证');
  console.log('\n示例:');
  console.log('  dnaspec tips           # 查看使用提示');
  console.log('  dnaspec list           # 列出技能');
  console.log('  dnaspec --version      # 查看版本');
  console.log('\n💡 提示: 请运行 "npm install" 安装所有依赖以获得完整功能');
}

// 如果commander可用，使用它；否则使用简化版本
if (commander) {
  // 设置commander
  commander
    .name('dnaspec')
    .description(DESCRIPTION)
    .version(VERSION);
}

// 检查Python环境
function checkPythonEnvironment() {
  try {
    execSync('python --version', { stdio: 'ignore' });
    return true;
  } catch (error) {
    console.error('❌ Python未安装或不在PATH中');
    console.error('请安装Python 3.8+并确保在PATH中');
    return false;
  }
}

// 检查DNASPEC依赖
function checkDependencies() {
  try {
    // 检查基本的文件系统功能
    if (typeof fs === 'undefined') {
      console.error('❌ 文件系统模块不可用');
      return false;
    }
    
    // 检查DNASPEC包目录是否存在
    const dnaspecRoot = path.join(__dirname, '..');
    if (!fs.existsSync(dnaspecRoot)) {
      console.error('❌ DNASPEC包目录不存在');
      return false;
    }
    
    // 检查核心Python脚本是否存在
    const pythonScript = path.join(dnaspecRoot, 'src', 'dna_spec_kit_integration', 'cli.py');
    if (!fs.existsSync(pythonScript)) {
      console.error('❌ DNASPEC核心脚本不存在');
      return false;
    }
    
    return true;
  } catch (error) {
    console.error('❌ 检查依赖时出错:', error.message);
    return false;
  }
}

// 执行Python脚本
function runPythonScript(scriptPath, args = []) {
  try {
    const fullScriptPath = path.join(__dirname, '..', scriptPath);
    const command = `python "${fullScriptPath}" ${args.join(' ')}`;
    
    console.log(`🚀 正在执行: ${command}`);
    
    const result = execSync(command, {
      encoding: 'utf8',
      cwd: path.join(__dirname, '..'),
      stdio: 'inherit'
    });
    
    return result;
  } catch (error) {
    console.error('❌ 执行Python脚本时出错:', error.message);
    process.exit(1);
  }
}

// 显示安装提示
function showInstallationTips() {
  console.log(`\n🎉 DNASPEC v${VERSION} 安装成功！\n`);
  console.log('📋 快速开始:');
  console.log('  dnaspec --help           # 查看所有可用命令');
  console.log('  dnaspec list             # 列出可用技能');
  console.log('  dnaspec deploy           # 部署到AI编辑器');
  console.log('\n🔧 部署系统:');
  console.log('  • 标准化部署: 复制技能目录到.claude/skills/');
  console.log('  • 智能部署: 使用 dnaspec deploy 自动部署');
  console.log('\n📚 使用技能（在AI编辑器中）:');
  console.log('  /dnaspec.agent-creator "创建AI智能体"');
  console.log('  /dnaspec.task-decomposer "分解任务"');
  console.log('  /dnaspec.context-analysis "分析文本质量"');
  console.log('\n💡 提示: 技能在AI编辑器（如Claude、Cursor、Qwen）中通过Slash命令调用');
  console.log('\n📖 更多信息: https://github.com/ptreezh/dnaSpec');
}

// 主要命令（仅当commander可用时）
if (commander) {
  program
    .command('exec <command>')
    .description('执行DNASPEC技能命令')
    .action((command) => {
      if (!checkPythonEnvironment()) {
        process.exit(1);
      }
      
      runPythonScript('src/dna_spec_kit_integration/cli.py', ['exec', command]);
    });

  program
    .command('shell')
    .description('启动交互式Shell')
    .action(() => {
      if (!checkPythonEnvironment()) {
        process.exit(1);
      }
      runPythonScript('src/dna_spec_kit_integration/cli.py', ['shell']);
    });

  program
    .command('list')
    .description('列出所有可用技能')
    .action(() => {
      showSkillsList();
    });

  program
    .command('slash [skill_name...]')
    .description('[已弃用] Slash命令仅用于在AI编辑器中调用，不通过CLI执行')
    .action((skillArgs) => {
      console.log('⚠️  Slash命令仅在AI编辑器中使用\n');
      console.log('正确的使用方式:');
      console.log('  1. 在AI编辑器（如Claude、Cursor）中输入:');
      console.log('     /dnaspec.agent-creator "创建AI智能体"');
      console.log('     /dnaspec.task-decomposer "分解任务"');
      console.log('  2. 或使用 dnaspec deploy 命令部署技能\n');
      console.log('💡 提示: 技能需要在支持的AI编辑器中使用Slash命令格式调用');
    });

  program
    .command('validate')
    .description('验证DNASPEC集成')
    .option('--stigmergy', '验证Stigmergy集成')
    .action((options) => {
      if (!checkPythonEnvironment() || !checkDependencies()) {
        process.exit(1);
      }
      
      const args = options.stigmergy ? ['validate', '--stigmergy'] : ['validate'];
      runPythonScript('src/dna_spec_kit_integration/cli.py', args);
    });

  program
    .command('deploy')
    .description('智能扩展部署')
    .option('--force-stigmergy', '强制全局Stigmergy模式')
    .option('--force-project', '强制项目级模式')
    .option('--verify', '验证部署和安全性')
    .option('--list', '显示部署状态')
    .action((options) => {
      if (!checkPythonEnvironment() || !checkDependencies()) {
        process.exit(1);
      }
      
      const args = ['deploy'];
      if (options.forceStigmergy) args.push('--force-stigmergy');
      if (options.forceProject) args.push('--force-project');
      if (options.verify) args.push('--verify');
      if (options.list) args.push('--list');
      
      runPythonScript('src/dna_spec_kit_integration/cli.py', args);
    });

  program
    .command('integrate')
    .description('智能集成和部署')
    .option('--platform <platform>', '目标平台')
    .option('--list', '列出可用平台')
    .option('--stigmergy', '强制Stigmergy模式')
    .option('--project', '强制项目级部署')
    .option('--status', '显示部署状态')
    .action((options) => {
      if (!checkPythonEnvironment() || !checkDependencies()) {
        process.exit(1);
      }
      
      const args = ['integrate'];
      if (options.platform) args.push('--platform', options.platform);
      if (options.list) args.push('--list');
      if (options.stigmergy) args.push('--stigmergy');
      if (options.project) args.push('--project');
      if (options.status) args.push('--status');
      
      runPythonScript('src/dna_spec_kit_integration/cli.py', args);
    });

  program
    .command('security')
    .description('安全测试和验证')
    .option('--test', '运行安全测试')
    .option('--validate', '验证安全配置')
    .option('--audit', '生成安全审计报告')
    .action((options) => {
      if (!checkPythonEnvironment() || !checkDependencies()) {
        process.exit(1);
      }
      
      const args = ['security'];
      if (options.test) args.push('--test');
      if (options.validate) args.push('--validate');
      if (options.audit) args.push('--audit');
      
      runPythonScript('src/dna_spec_kit_integration/cli.py', args);
    });

  program
    .command('tips')
    .description('显示安装提示和使用指南')
    .action(() => {
      showInstallationTips();
    });
}

// 处理命令行参数
if (commander) {
  // 使用commander
  if (!process.argv.slice(2).length) {
    console.log(DESCRIPTION);
    console.log(`版本: ${VERSION}\n`);
    commander.outputHelp();
    console.log('\n💡 提示: 使用 "dnaspec tips" 查看详细使用指南');
  }
  commander.parse(process.argv);
} else {
  // 使用简化解析器
  const parsed = simpleCommandParser();
  
  // 处理内置命令
  switch (parsed.command) {
    case '--version':
    case 'version':
      console.log(`DNA SPEC Context System (dnaspec) ${VERSION}`);
      break;
      
    case '--help':
    case 'help':
    case '':
      showSimpleHelp();
      break;
      
    case 'tips':
      showInstallationTips();
      break;
      
    case 'list':
      showSkillsList();
      break;
      
    case 'slash':
      // Slash命令已在AI编辑器中使用，不通过CLI调用
      console.log('⚠️  Slash命令仅在AI编辑器中使用\n');
      console.log('正确的使用方式:');
      console.log('  在AI编辑器（如Claude、Cursor、Qwen）中输入:');
      console.log('    /dnaspec.agent-creator "创建AI智能体"');
      console.log('    /dnaspec.task-decomposer "分解任务"');
      console.log('    /dnaspec.context-analysis "分析文本"\n');
      console.log('💡 提示: 使用 dnaspec deploy 命令将技能部署到AI编辑器');
      break;
      
    default:
      console.log(`❌ 未知命令: ${parsed.command}`);
      console.log('使用 "dnaspec --help" 查看可用命令');
      break;
  }
}

// 显示技能列表的函数
function showSkillsList() {
  console.log('🛠️  可用的DNASPEC技能:\n');

  const skills = [
    'context-analysis       - 上下文分析技能',
    'context-optimization   - 上下文优化技能',
    'cognitive-template     - 认知模板技能',
    'agent-creator          - 智能体创建技能',
    'task-decomposer        - 任务分解技能',
    'constraint-generator   - 约束生成技能',
    'api-checker           - API检查技能',
    'modulizer            - 模块化技能',
    'system-architect      - 系统架构技能',
    'simple-architect      - 简单架构技能',
    'git-operations        - Git操作技能',
    'temp-workspace       - 临时工作区技能',
    'liveness             - 活跃度技能'
  ];

  skills.forEach(skill => console.log(`  • ${skill}`));

  console.log('\n💡 使用方式:');
  console.log('  技能在AI编辑器（如Claude、Cursor、Qwen）中通过Slash命令调用');
  console.log('\n  示例:');
  console.log('    /dnaspec.agent-creator "创建AI智能体"');
  console.log('    /dnaspec.task-decomposer "分解复杂任务"');
  console.log('    /dnaspec.context-analysis "分析这段文本"');
  console.log('\n  部署命令:');
  console.log('    dnaspec deploy           # 自动部署到AI编辑器');
  console.log('    dnaspec integrate        # 智能集成和部署');
}