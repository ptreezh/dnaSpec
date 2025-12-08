#!/usr/bin/env node

/**
 * Dynamic Specification Growth System (dnaspec) - npm安装入口点
 * 提供基于npm的一键安装和自动配置功能
 */

const { execSync, spawn, spawnSync } = require('child_process');
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

function installAndConfigure() {
    const command = determineCommand();
    
    // 获取当前工作目录（只声明一次）
    const initialDir = process.cwd();

    // 检查当前目录是否是项目目录（通过检查关键文件）
    const isProjectDir = fs.existsSync('src') &&
                         fs.existsSync('pyproject.toml') &&
                         fs.existsSync('package.json');

    let projectDir = initialDir;

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


    if (!isProjectDir) {
        // 如果不在项目目录，创建临时目录并克隆项目
        const tempDir = 'dsgs-install-tmp';

        // 创建并进入临时目录
        if (!fs.existsSync(tempDir)) {
            fs.mkdirSync(tempDir);
        }
        process.chdir(tempDir);

        // 克隆项目 - 增加多源支持和重试机制
        const repoDir = 'dnaSpec';
        if (fs.existsSync(repoDir) && fs.lstatSync(repoDir).isDirectory()) {
            console.log('🔄 更新现有项目...');
            process.chdir(repoDir);
        } else {
            console.log('📦 克隆项目...');

            // 尝试多个源和备用源
            const gitUrls = [
                'https://github.com/ptreezh/dnaSpec.git',
                'https://gitclone.com/github.com/ptreezh/dnaSpec.git',  // 备用镜像
                'https://hub.fastgit.xyz/ptreezh/dnaSpec.git'          // 备用镜像
            ];

            let cloneSuccess = false;

            for (let i = 0; i < gitUrls.length; i++) {
                const url = gitUrls[i];
                console.log(`尝试源 ${i+1}/${gitUrls.length}: ${url}`);

                try {
                    const result = spawnSync('git', ['clone', url, '.'], {
                        stdio: 'inherit',
                        encoding: 'utf-8',
                        timeout: 120000  // 2分钟超时
                    });

                    if (result.status === 0) {
                        cloneSuccess = true;
                        break;
                    } else {
                        console.log(`源 ${i+1} 克隆失败，尝试下一个...`);
                    }
                } catch (error) {
                    console.log(`源 ${i+1} 克隆出错: ${error.message}，尝试下一个...`);
                }
            }

            if (!cloneSuccess) {
                console.error('❌ 所有源都无法克隆项目');
                process.chdir(initialDir);
                const cleanupDir = path.join(initialDir, tempDir);
                if (fs.existsSync(cleanupDir)) {
                    fs.rmSync(cleanupDir, { recursive: true, force: true });
                }
                process.exit(1);
            }
        }

        projectDir = process.cwd(); // 更新项目目录为克隆的目录
    } else {
        console.log('📋 检测到已在项目目录中...');
    }

    // 安装Python包
    if (!runCommand('pip install -e .', '安装DSGS包')) {
        console.error('❌ 安装DSGS包失败');
        if (!isProjectDir) {
            process.chdir(initialDir);
            const tempDir = path.join(initialDir, 'dsgs-install-tmp');
            if (fs.existsSync(tempDir)) {
                fs.rmSync(tempDir, { recursive: true, force: true });
            }
        }
        process.exit(1);
    }
    
    console.log('✅ 安装DSGS包成功\n');

    // 确保使用正确的脚本路径（在可能更新了projectDir后）
    const scriptPath = path.join(projectDir, pythonScript);
    
    console.log(`⚙️  运行${description}...`);
    console.log(`   执行: python ${scriptPath}`);

    const commandProcess = spawn('python', [scriptPath], {
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
            // 显示英文ANSI兼容的输出
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
            console.log('  dnaspec deploy            - Deploy skills to AI platforms');
            console.log('  dnaspec deploy --list     - List detected AI platforms');
            console.log('  dnaspec validate          - Check integration status');
            console.log('  dnaspec list              - Show all available skills');
            console.log('  dnaspec help              - Show help information');
            console.log('');
            console.log('For support, visit: https://github.com/ptreezh/dnaSpec');
            console.log('Report issues at: https://github.com/ptreezh/dnaSpec/issues');
        } else {
            console.error(`\n❌ ${description} process failed, exit code: ${code}`);
            if (!isProjectDir) {
                process.chdir(initialDir);
                const tempDir = path.join(initialDir, 'dsgs-install-tmp');
                if (fs.existsSync(tempDir)) {
                    fs.rmSync(tempDir, { recursive: true, force: true });
                }
            }
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

function determineCommand() {
    // 分析命令行参数
    const args = process.argv.slice(2);
    if (args.length > 0) {
        return args[0].toLowerCase();
    }
    return 'init'; // 默认命令
}

// 运行安装和配置
installAndConfigure();