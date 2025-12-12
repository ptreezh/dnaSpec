#!/usr/bin/env node

/**
 * DNA SPEC Context System (dnaspec) - npm安装入口点
 * 提供基于npm的一键安装和自动配置功能
 */

const { execSync, spawn, spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function runCommand(cmd, description) {
    console.log(`[SETUP] ${description}...`);
    try {
        const result = execSync(cmd, { encoding: 'utf-8', stdio: 'inherit' });
        console.log(`[SUCCESS] ${description} completed\n`);
        return true;
    } catch (error) {
        console.error(`[ERROR] ${description} failed:`);
        console.error(error.message);
        return false;
    }
}

function checkDependencies() {
    console.log('[CHECK] Checking dependencies...');

    // Check Python
    try {
        execSync('python --version', { stdio: 'pipe' });
        console.log('[OK] Python detected');
    } catch (error) {
        try {
            execSync('python3 --version', { stdio: 'pipe' });
            console.log('[OK] Python3 detected');
        } catch (error2) {
            console.error('[ERROR] Python or Python3 not found, please install Python 3.8+');
            return false;
        }
    }

    // Check Git
    try {
        execSync('git --version', { stdio: 'pipe' });
        console.log('[OK] Git detected');
    } catch (error) {
        console.error('[ERROR] Git not found, please install Git');
        return false;
    }

    console.log('[SUCCESS] All dependencies passed\n');
    return true;
}

function runQueryCommand(command, pythonScript, description) {
    // For query commands, run installed Python packages directly
    console.log(`[QUERY] Processing ${command} command...`);

    // Check dependencies
    if (!checkDependencies()) {
        process.exit(1);
    }

    // Run Python script directly using installed modules
    // Use installed package entry point instead of src directory
    const commandProcess = spawn('python', ['-c', `
import subprocess
import sys
import os

# Run query command using installed package entry point
command_result = subprocess.run([
    sys.executable,
    '-m', 'dnaspec_spec_kit_integration.cli',
    '${command}'
], capture_output=False, text=True, env=os.environ.copy())

sys.exit(command_result.returncode)
    `], {
        stdio: 'inherit',
        env: {
            ...process.env,
            PYTHONIOENCODING: 'utf-8',
            LANG: 'en_US.UTF-8'
        }
    });

    commandProcess.on('close', (code) => {
        if (code === 0) {
            console.log(`✅ ${command} command executed successfully!`);
        } else {
            // If direct call fails, try using standalone_cli
            console.log(`⚠️  Trying fallback method for ${command}...`);
            
            const fallbackProcess = spawn('python', ['-c', `
import sys
sys.path.insert(0, '.')
from src.dnaspec_spec_kit_integration.cli import main
import sys as pysys
pysys.argv = ['dnaspec', '${command}']
try:
    main()
except SystemExit:
    pass
            `], {
                stdio: 'inherit',
                env: {
                    ...process.env,
                    PYTHONIOENCODING: 'utf-8',
                    LANG: 'en_US.UTF-8'
                }
            });

            fallbackProcess.on('close', (fallbackCode) => {
                if (fallbackCode === 0) {
                    console.log(`✅ ${command} command executed successfully!`);
                } else {
                    console.error(`❌ ${command} command execution failed, exit code: ${fallbackCode}`);
                    process.exit(fallbackCode);
                }
            });
        }
    });

    commandProcess.on('error', (err) => {
        console.error(`❌ Error running ${command} command: ${err.message}`);
        process.exit(1);
    });
}

function installAndConfigure() {
    const command = determineCommand();
    
    // Get current working directory (declare once)
    const initialDir = process.cwd();

    // Check if current directory is project directory (by checking key files)
    const isProjectDir = fs.existsSync('src') &&
                         fs.existsSync('pyproject.toml') &&
                         fs.existsSync('package.json');

    // For query commands (no installation needed), use installed modules directly
    const queryCommands = ['list', 'validate', '--list', '--version', 'help'];
    const shouldRunFullInstall = !queryCommands.includes(command);

    let projectDir = initialDir;
    let pythonScript;
    let description;

    switch(command) {
        case 'init':
        case 'install':
            // 确保初始化命令执行完整安装流程
            pythonScript = 'run_auto_config.py';
            description = 'Installation and Configuration';
            break;
        case 'deploy':
            // 部署命令也需要完整安装
            pythonScript = 'deploy_cli.py';
            description = 'Deployment';
            break;
        case 'integrate':
            // 集成命令也需要完整安装
            pythonScript = 'src/dnaspec_spec_kit_integration/cli.py';
            description = 'Integration';
            break;
        case 'list':
        case 'validate':
        case '--list':
        case '--version':
        case 'help':
            // 查询命令：使用已安装的包
            console.log(`🔍 Processing ${command} command...`);
            pythonScript = 'src/dnaspec_spec_kit_integration/cli.py';
            description = 'Query';
            
            // 直接运行已安装的模块，不安装
            runQueryCommand(command, pythonScript, description);
            return;
        default:
            // 其他命令：执行完整安装流程
            pythonScript = 'run_auto_config.py';
            description = 'Installation and Configuration';
    }

    console.log(`🚀 Starting DNA SPEC Context System (dnaspec) ${description}...\n`);

    // 检查依赖
    if (!checkDependencies()) {
        process.exit(1);
    }


    if (!isProjectDir) {
        // 如果不在项目目录，创建临时目录并克隆项目
        const tempDir = 'dnaspec-install-tmp';

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
    if (!runCommand('pip install -e .', 'Install DNASPEC package')) {
        console.error('❌ Failed to install DNASPEC package');
        if (!isProjectDir) {
            process.chdir(initialDir);
            const tempDir = path.join(initialDir, 'dnaspec-install-tmp');
            if (fs.existsSync(tempDir)) {
                fs.rmSync(tempDir, { recursive: true, force: true });
            }
        }
        process.exit(1);
    }
    
    console.log('✅ DNASPEC package installed successfully\n');

    // 确保使用正确的脚本路径（在可能更新了projectDir后）
    const scriptPath = path.join(projectDir, pythonScript);
    
    console.log(`⚙️  Running ${description}...`);
    console.log(`   Executing: python ${scriptPath}`);

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
            const tempDir = path.join(initialDir, 'dnaspec-install-tmp');
            if (fs.existsSync(tempDir)) {
                fs.rmSync(tempDir, { recursive: true, force: true });
            }
        }

        if (code === 0) {
            // 显示英文ANSI兼容的输出
            console.log('\n🎉 Installation and configuration completed successfully!');

            // Show post-installation guide
            console.log('\nDNASPEC Context Engineering Skills - POST-INSTALLATION GUIDE');
            console.log('='.repeat(80));
            console.log('');
            console.log('Thank you for installing DNASPEC (DNA SPEC Context System)!');
            console.log('');
            console.log('DNASPEC is a professional context engineering toolkit that enhances your AI-assisted');
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
            console.log('  /speckit.dnaspec.context-analysis "Analyze this requirement: ..."');
            console.log('  /speckit.dnaspec.context-optimization "Optimize this context: ..."');
            console.log('  /speckit.dnaspec.cognitive-template "Apply template to: ..." template=verification');
            console.log('  /speckit.dnaspec.architect "Design system for: ..."');
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
                const tempDir = path.join(initialDir, 'dnaspec-install-tmp');
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
            const tempDir = path.join(initialDir, 'dnaspec-install-tmp');
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