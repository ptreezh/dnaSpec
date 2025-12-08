#!/usr/bin/env node

/**
 * Dynamic Specification Growth System (dnaspec) - npm安装入口点
 * 提供基于npm的一键安装和自动配置功能
 */

const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

function runCommand(cmd, description) {
    console.log(`🔧 ${description}...`);
    try {
        const result = execSync(cmd, { encoding: 'utf-8', stdio: 'inherit' });
        console.log(`✅ ${description}成功\n`);
        return true;
    } catch (error) {
        console.error(`❌ ${description}失败:`);
        console.error(error.message);
        return false;
    }
}

function checkDependencies() {
    console.log('🔍 检查依赖...');

    // 检查Python
    try {
        execSync('python --version', { stdio: 'pipe' });
        console.log('✅ 检测到Python');
    } catch (error) {
        try {
            execSync('python3 --version', { stdio: 'pipe' });
            console.log('✅ 检测到Python3');
        } catch (error2) {
            console.error('❌ 未找到Python或Python3，请先安装Python 3.8+');
            return false;
        }
    }

    // 检查Git
    try {
        execSync('git --version', { stdio: 'pipe' });
        console.log('✅ 检测到Git');
    } catch (error) {
        console.error('❌ 未找到Git，请先安装Git');
        return false;
    }

    console.log('✅ 依赖检查通过\n');
    return true;
}

function determineCommand() {
    // 分析命令行参数
    const args = process.argv.slice(2);
    if (args.length > 0) {
        return args[0].toLowerCase();
    }
    return 'init'; // 默认命令
}

function installAndConfigure() {
    const command = determineCommand();

    // 根据命令决定执行的Python脚本
    let pythonScript;
    let description;

    switch(command) {
        case 'init':
        case 'install':
            pythonScript = 'run_auto_config.py';
            description = '安装和配置';
            break;
        case 'deploy':
            pythonScript = 'deploy_cli.py';
            description = '部署技能';
            break;
        case 'integrate':
            pythonScript = 'src/dsgs_spec_kit_integration/cli.py';
            description = '集成验证';
            break;
        case 'list':
        case 'validate':
        case '--list':
        case '--version':
        case 'help':
            pythonScript = 'standalone_cli.py';
            description = '执行命令';
            break;
        default:
            pythonScript = 'run_auto_config.py';
            description = '安装和配置';
    }

    console.log(`🚀 开始Dynamic Specification Growth System (dnaspec)${description}...\n`);

    // 检查依赖
    if (!checkDependencies()) {
        process.exit(1);
    }

    // 获取当前工作目录
    const initialDir = process.cwd();

    // 检查当前目录是否是项目目录（通过检查关键文件）
    const isProjectDir = fs.existsSync('src') &&
                         fs.existsSync('pyproject.toml') &&
                         fs.existsSync('package.json');

    let projectDir = initialDir;

    if (!isProjectDir) {
        // 如果不在项目目录，创建临时目录并克隆项目
        const tempDir = 'dsgs-install-tmp';

        // 创建并进入临时目录
        if (!fs.existsSync(tempDir)) {
            fs.mkdirSync(tempDir);
        }
        process.chdir(tempDir);

        // 克隆项目
        const repoDir = 'dsgs-context-engineering';
        if (fs.existsSync(repoDir) && fs.lstatSync(repoDir).isDirectory()) {
            console.log('🔄 更新现有项目...');
            process.chdir(repoDir);
        } else {
            console.log('📦 克隆项目...');
            if (!runCommand('git clone https://github.com/ptreezh/dnaSpec.git .', '克隆项目')) {
                process.chdir(initialDir);
                fs.rmSync(tempDir, { recursive: true, force: true });
                process.exit(1);
            }
        }

        projectDir = process.cwd(); // 更新项目目录为克隆的目录
    } else {
        console.log('📋 检测到已在项目目录中...');
    }

    // 安装Python包
    if (!runCommand('pip install -e .', '安装DSGS包')) {
        // 尝试使用python -m pip
        if (!runCommand('python -m pip install -e .', '安装DSGS包（备用方式）')) {
            if (!runCommand('python3 -m pip install -e .', '安装DSGS包（备用方式2）')) {
                console.error('❌ 所有安装方式都失败了');
                if (!isProjectDir) {
                    process.chdir(initialDir);
                    const tempDir = path.join(initialDir, 'dsgs-install-tmp');
                    if (fs.existsSync(tempDir)) {
                        fs.rmSync(tempDir, { recursive: true, force: true });
                    }
                }
                process.exit(1);
            }
        }
    }

    // 运行相应脚本
    console.log(`⚙️  运行${description}...`);

    // 确定Python脚本的完整路径
    const scriptPath = path.join(projectDir, pythonScript);

    // 构建Python命令参数
    let pythonArgs = [scriptPath];
    if (command !== 'init' && command !== 'install' && !command.startsWith('-')) {
        pythonArgs.push(command);
        // 添加其他参数
        const additionalArgs = process.argv.slice(3);
        pythonArgs = pythonArgs.concat(additionalArgs);
    }

    console.log(`   执行: python ${pythonArgs.join(' ')}`);

    const commandProcess = spawn('python', pythonArgs, {
        stdio: 'inherit',
        cwd: projectDir, // 确保在项目目录中运行
        env: {
            ...process.env,
            PYTHONIOENCODING: 'utf-8',  // 设置Python编码为UTF-8以避免GBK错误
            LANG: 'en_US.UTF-8'         // 设置语言环境
        }
    });

    commandProcess.on('close', (code) => {
        if (!isProjectDir) {
            // 如果不是原始项目目录，清理临时目录
            process.chdir(initialDir);
            const tempDir = path.join(initialDir, 'dsgs-install-tmp');
            if (fs.existsSync(tempDir)) {
                fs.rmSync(tempDir, { recursive: true, force: true });
            }
        }

        if (code === 0) {
            // 根据命令显示不同信息
            if (command === 'deploy') {
                console.log('\n🎉 DSGS Skills deployment completed successfully!');
                console.log('\nNow you can use DSGS skills in your AI CLI tools:');
                console.log('  /speckit.dsgs.context-analysis [context] - Analyze context quality');
                console.log('  /speckit.dsgs.context-optimization [context] - Optimize context');
                console.log('  /speckit.dsgs.cognitive-template [task] - Apply cognitive template');
            } else if (command === 'integrate') {
                console.log('\n🎉 DSGS Integration completed successfully!');
            } else if (command === 'list' || command === '--list') {
                console.log('\n🎉 DSGS Command listing completed successfully!');
            } else if (command === 'validate' || command === '--version') {
                console.log('\n🎉 DSGS Validation completed successfully!');
            } else {
                console.log('\n🎉 Installation and configuration completed successfully!');

                // Show post-installation guide
                console.log('\nDSGS Context Engineering Skills - POST-INSTALLATION GUIDE');
                console.log('='.repeat(80));
                console.log('');
                console.log('Thank you for installing DSGS (Dynamic Specification Growth System)!');
                console.log('');
                console.log('DSGS is a professional context engineering toolkit that enhances your AI-assisted');
                console.log('development experience by providing advanced context analysis, optimization,');
                console.log('and cognitive template application capabilities.');
                console.log('');
                console.log('KEY FEATURES:');
                console.log('  ✓ Context Quality Analysis: 5-dimensional assessment (clarity, relevance,');
                console.log('                               completeness, consistency, efficiency)');
                console.log('  ✓ Context Optimization: AI-driven improvements based on specific goals');
                console.log('  ✓ Cognitive Templates: Professional thinking frameworks (CoT, Verification, etc.)');
                console.log('  ✓ Agentic Design: System architecture and task decomposition skills');
                console.log('  ✓ Safety Workflows: Secure AI interaction with temporary workspaces');
                console.log('  ✓ Multi-Platform Support: Claude, Qwen, Gemini, Cursor, Copilot');
                console.log('');
                console.log('GETTING STARTED - Next Steps:');
                console.log('');
                console.log('  1. Run automatic validation:');
                console.log('     dnaspec validate');
                console.log('');
                console.log('  2. Deploy skills to AI platforms (if you have AI CLI tools installed):');
                console.log('     dnaspec deploy');
                console.log('');
                console.log('  3. View all available commands:');
                console.log('     dnaspec list');
                console.log('');
                console.log('USAGE EXAMPLES in AI CLI Tools:');
                console.log('  /speckit.dsgs.context-analysis "Analyze this requirement: ..."');
                console.log('  /speckit.dsgs.context-optimization "Optimize this context: ..."');
                console.log('  /speckit.dsgs.cognitive-template "Apply template to: ..." template=verification');
                console.log('  /speckit.dsgs.architect "Design system for: ..."');
                console.log('');
                console.log('COMMAND REFERENCE:');
                console.log('  dnaspec validate          - Check integration status');
                console.log('  dnaspec deploy            - Deploy skills to AI platforms');
                console.log('  dnaspec deploy --list     - List detected AI platforms');
                console.log('  dnaspec list              - Show all available skills');
                console.log('  dnaspec help              - Show help information');
                console.log('');
                console.log('For support, visit: https://github.com/ptreezh/dnaSpec');
                console.log('Report issues at: https://github.com/ptreezh/dnaSpec/issues');
            }
        } else {
            console.error(`\n❌ ${description} process failed, exit code: ${code}`);
            process.exit(1);
        }
    });

    commandProcess.on('error', (err) => {
        if (!isProjectDir) {
            // 如果不是原始项目目录，清理临时目录
            process.chdir(initialDir);
            const tempDir = path.join(initialDir, 'dsgs-install-tmp');
            if (fs.existsSync(tempDir)) {
                fs.rmSync(tempDir, { recursive: true, force: true });
            }
        }

        console.error(`\n❌ Error running ${description}: ${err.message}`);
        process.exit(1);
    });
}

// 运行安装和配置
installAndConfigure();