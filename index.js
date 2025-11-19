#!/usr/bin/env node

/**
 * DSGS Context Engineering Skills - npm安装入口点
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

function installAndConfigure() {
    console.log('🚀 开始DSGS Context Engineering Skills安装和配置...\n');

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

    // 运行自动配置
    console.log('⚙️  运行自动配置...');
    console.log('   执行: python run_auto_config.py');

    const configProcess = spawn('python', ['run_auto_config.py'], {
        stdio: 'inherit',
        cwd: projectDir, // 确保在项目目录中运行
        env: {
            ...process.env,
            PYTHONIOENCODING: 'utf-8',  // 设置Python编码为UTF-8以避免GBK错误
            LANG: 'en_US.UTF-8'         // 设置语言环境
        }
    });

    configProcess.on('close', (code) => {
        if (!isProjectDir) {
            // 如果不是原始项目目录，清理临时目录
            process.chdir(initialDir);
            const tempDir = path.join(initialDir, 'dsgs-install-tmp');
            if (fs.existsSync(tempDir)) {
                fs.rmSync(tempDir, { recursive: true, force: true });
            }
        }

        if (code === 0) {
            console.log('\n🎉 安装和配置成功完成！');
            console.log('\n现在您可以在AI CLI工具中使用以下命令：');
            console.log('  /speckit.dsgs.context-analysis [上下文] - 分析上下文质量');
            console.log('  /speckit.dsgs.context-optimization [上下文] - 优化上下文');
            console.log('  /speckit.dsgs.cognitive-template [任务] - 应用认知模板');
            console.log('  /speckit.dsgs.architect [需求] - 系统架构设计');
            console.log('  ...以及其他DSGS专业技能');
            console.log('\n欢迎使用 dsgs-cli 工具！可以通过命令 `dsgs` 重新运行配置。');
        } else {
            console.error(`\n❌ 配置过程失败，退出码: ${code}`);
            process.exit(1);
        }
    });

    configProcess.on('error', (err) => {
        if (!isProjectDir) {
            // 如果不是原始项目目录，清理临时目录
            process.chdir(initialDir);
            const tempDir = path.join(initialDir, 'dsgs-install-tmp');
            if (fs.existsSync(tempDir)) {
                fs.rmSync(tempDir, { recursive: true, force: true });
            }
        }

        console.error(`\n❌ 运行配置时出错: ${err.message}`);
        process.exit(1);
    });
}

// 运行安装和配置
installAndConfigure();