#!/usr/bin/env node
/**
 * DNASPEC CLI - 统一命令行入口
 */

const { program } = require('commander');
const path = require('path');
const fs = require('fs');

// 获取项目根目录
const getRootDir = () => {
    const currentDir = __dirname;
    return path.dirname(currentDir);
};

// 技能列表
const SKILLS = [
    { name: 'dapi-checker', description: 'API检查器 - 分层API审查' },
    { name: 'git', description: 'Git管理 - 智能版本控制辅助' },
    { name: 'workspace', description: '工作区管理 - 隔离任务工作区' },
    { name: 'context-analysis', description: '上下文分析 - 质量评估' },
    { name: 'context-optimization', description: '上下文优化 - 质量提升' },
    { name: 'cognitive-template', description: '认知模板 - 可复用模式' },
    { name: 'agent-creator', description: '智能体创建器' },
    { name: 'architect', description: '架构协调器' },
    { name: 'task-decomposer', description: '任务分解器' },
    { name: 'modulizer', description: '模块化器' },
    { name: 'system-architect', description: '系统架构师' },
    { name: 'constraint-generator', description: '约束生成器' },
];

// 主程序
program
    .name('dnaspec')
    .description('DNASPEC - DNA软件开发规范套件')
    .version('2.0.0');

// list命令 - 列出所有技能
program
    .command('list')
    .description('列出所有可用技能')
    .action(() => {
        console.log('\n可用技能列表:\n');
        SKILLS.forEach((skill, index) => {
            const num = (index + 1).toString().padStart(2, '0');
            const name = skill.name.padEnd(25);
            console.log(`  ${num}. ${name} ${skill.description}`);
        });
        console.log('\n使用方式: dnaspec <skill> "<request>"');
        console.log('示例: dnaspec git "生成提交信息"\n');
    });

// info命令 - 显示系统信息
program
    .command('info')
    .description('显示DNASPEC系统信息')
    .action(() => {
        const rootDir = getRootDir();
        const pkgPath = path.join(rootDir, 'package.json');
        const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf-8'));

        console.log('\n' + '='.repeat(60));
        console.log('DNASPEC 系统信息');
        console.log('='.repeat(60));
        console.log(`版本: ${pkg.version}`);
        console.log(`名称: ${pkg.name}`);
        console.log(`描述: ${pkg.description}`);
        console.log(`安装路径: ${rootDir}`);
        console.log('='.repeat(60) + '\n');
    });

// evaluate命令 - 运行评估
program
    .command('evaluate')
    .description('评估DNASPEC系统质量')
    .option('-s, --skill <name>', '评估特定技能')
    .option('-a, --all', '评估所有技能')
    .option('--no-report', '不生成报告')
    .action((options) => {
        console.log('\n运行评估...');
        const { spawn } = require('child_process');
        const args = ['test_evaluation_framework.py'];

        if (options.skill) {
            // 评估单个技能
            console.log(`评估技能: ${options.skill}\n`);
        } else if (options.all) {
            // 评估所有技能
            console.log('评估所有技能\n');
        } else {
            // 默认：系统评估
            console.log('执行系统评估\n');
        }

        const python = process.platform === 'win32' ? 'python' : 'python3';
        const proc = spawn(python, args, {
            cwd: rootDir,
            stdio: 'inherit'
        });

        proc.on('close', (code) => {
            process.exit(code);
        });
    });

// 为每个技能创建命令
SKILLS.forEach(skill => {
    const commandName = skill.name; // 例如: 'git', 'context-analysis'

    program
        .command(commandName, '<request>')
        .description(skill.description)
        .option('-l, --level <level>', '提示级别 (00/01/02/03)')
        .option('-f, --force', '强制使用指定级别')
        .action((request, options) => {
            executeSkill(skill.name, request, options);
        });
});

// 执行技能
function executeSkill(skillName, request, options) {
    console.log(`\n执行技能: ${skillName}`);
    console.log(`请求: ${request}`);
    if (options.level) {
        console.log(`级别: ${options.level}`);
    }
    console.log('.');

    // 这里应该调用Python的技能执行器
    // 暂时显示提示信息
    const rootDir = getRootDir();
    const skillDir = path.join(rootDir, 'skills', `dnaspec-${skillName}`);

    if (!fs.existsSync(skillDir)) {
        console.error(`错误: 技能 '${skillName}' 未找到`);
        console.log(`提示: 使用 'dnaspec list' 查看可用技能`);
        process.exit(1);
    }

    console.log(`技能路径: ${skillDir}`);
    console.log('\n提示: 技能执行功能正在开发中...');
    console.log('当前版本: 请直接使用Python技能执行器\n');
}

// 解析命令行参数
program.parse(process.argv);

// 如果没有参数，显示帮助
if (!process.argv.slice(2).length) {
    program.outputHelp();
}
