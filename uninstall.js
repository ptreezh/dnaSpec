#!/usr/bin/env node

/**
 * DNASPEC Uninstall Script - Complete cleanup utility
 * Removes all files, configurations, and dependencies created during installation
 */

const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

class DNASPECUninstaller {
    constructor() {
        this.initialDir = process.cwd();
        this.homeDir = os.homedir();
        this.removedItems = [];
        this.failedItems = [];

        // Platforms and paths to check
        this.platforms = {
            claude: ['.claude/'],
            cursor: ['.cursor/', '.cursorrules'],
            copilot: ['.copilot/'],
            qwen: ['.qwen/'],
            gemini: ['.gemini/'],
            iflow: ['.iflow/'],
            codebuddy: ['.codebuddy/'],
            qodercli: ['.qodercli/']
        };

        this.pythonPackages = [
            'dnaspec-context-engineering-skills',
            'dna-context-engineering-skills',
            'dna-spec-kit-integration',
            'dnaspec-spec-kit-integration'
        ];

        this.npmPackages = ['dnaspec', 'stigmergy'];

        this.tempDirs = [
            'dnaspec-install-tmp',
            'dnaspec-temp-*',
            'dnaspec-workspace-*'
        ];

        this.configFiles = [
            '.dnaspec-config.json',
            '.dnaspec-status.json',
            '.dna-spec-integration.json',
            'dnaspec-integration-report.json'
        ];
    }

    log(message, type = 'info') {
        const icons = {
            info: '🔍',
            success: '✅',
            warning: '⚠️',
            error: '❌'
        };
        console.log(`${icons[type]} ${message}`);
    }

    runCommand(cmd, description, ignoreError = false) {
        this.log(`执行: ${description}...`);
        try {
            const result = execSync(cmd, {
                encoding: 'utf-8',
                stdio: 'pipe',
                cwd: this.initialDir
            });
            this.log(`${description}成功`, 'success');
            return true;
        } catch (error) {
            if (ignoreError) {
                this.log(`${description}未找到或已删除`, 'warning');
                return true;
            } else {
                this.log(`${description}失败: ${error.message}`, 'error');
                this.failedItems.push({ item: description, error: error.message });
                return false;
            }
        }
    }

    safeRemove(itemPath, description) {
        try {
            if (fs.existsSync(itemPath)) {
                const stats = fs.statSync(itemPath);
                if (stats.isDirectory()) {
                    fs.rmSync(itemPath, { recursive: true, force: true });
                } else {
                    fs.unlinkSync(itemPath);
                }
                this.log(`删除 ${description}`, 'success');
                this.removedItems.push(description);
                return true;
            } else {
                this.log(`${description}不存在`, 'warning');
                return true;
            }
        } catch (error) {
            this.log(`删除 ${description} 失败: ${error.message}`, 'error');
            this.failedItems.push({ item: description, error: error.message });
            return false;
        }
    }

    removeTempDirectories() {
        this.log('\n🗑️  清理临时目录...', 'info');

        // Clean temp directories in current project
        this.tempDirs.forEach(pattern => {
            if (pattern.includes('*')) {
                // Handle wildcard patterns
                const basePattern = pattern.replace('*', '');
                try {
                    const items = fs.readdirSync(this.initialDir);
                    items.forEach(item => {
                        if (item.startsWith(basePattern)) {
                            this.safeRemove(
                                path.join(this.initialDir, item),
                                `临时目录: ${item}`
                            );
                        }
                    });
                } catch (error) {
                    // Directory doesn't exist or can't read
                }
            } else {
                this.safeRemove(
                    path.join(this.initialDir, pattern),
                    `临时目录: ${pattern}`
                );
            }
        });

        // Clean temp directories in home directory
        Object.values(this.platforms).flat().forEach(dir => {
            const tempDirPath = path.join(this.homeDir, dir, 'temp');
            this.safeRemove(tempDirPath, `临时目录: ${dir}temp`);
        });
    }

    removePythonPackages() {
        this.log('\n🐍 卸载 Python 包...', 'info');

        // Try different Python commands
        const pythonCommands = ['python', 'python3', 'py'];

        pythonCommands.forEach(pythonCmd => {
            try {
                // Check if Python command exists
                execSync(`${pythonCmd} --version`, { stdio: 'pipe' });

                this.pythonPackages.forEach(pkg => {
                    this.runCommand(
                        `${pythonCmd} -m pip uninstall -y ${pkg}`,
                        `卸载 Python 包: ${pkg}`,
                        true
                    );
                });

                // Also try with pip directly
                this.pythonPackages.forEach(pkg => {
                    this.runCommand(
                        `pip uninstall -y ${pkg}`,
                        `卸载 Python 包: ${pkg}`,
                        true
                    );
                });

                return; // Stop after finding working Python command
            } catch (error) {
                // Python command not found, try next
            }
        });
    }

    removeNPMPackages() {
        this.log('\n📦 卸载 NPM 包...', 'info');

        this.npmPackages.forEach(pkg => {
            // Try global uninstall
            this.runCommand(
                `npm uninstall -g ${pkg}`,
                `卸载全局 NPM 包: ${pkg}`,
                true
            );

            // Try local uninstall
            this.runCommand(
                `npm uninstall ${pkg}`,
                `卸载本地 NPM 包: ${pkg}`,
                true
            );
        });
    }

    removePlatformConfigurations() {
        this.log('\n🔧 清理平台配置...', 'info');

        Object.entries(this.platforms).forEach(([platform, dirs]) => {
            dirs.forEach(dir => {
                const platformPath = path.join(this.homeDir, dir);

                // Remove platform-specific configurations
                if (fs.existsSync(platformPath)) {
                    // Remove DNASPEC-related files from platform directories
                    try {
                        const files = fs.readdirSync(platformPath, { withFileTypes: true });

                        files.forEach(file => {
                            const fileName = file.name;
                            const filePath = path.join(platformPath, fileName);

                            // Remove DNASPEC-related files
                            if (fileName.toLowerCase().includes('dnaspec') ||
                                fileName.toLowerCase().includes('dna-spec') ||
                                fileName.toLowerCase().includes('dna_context') ||
                                fileName.includes('skill') && fileName.includes('dna')) {

                                if (file.isDirectory()) {
                                    this.safeRemove(filePath, `${platform} 配置目录: ${fileName}`);
                                } else {
                                    this.safeRemove(filePath, `${platform} 配置文件: ${fileName}`);
                                }
                            }
                        });
                    } catch (error) {
                        // Can't read directory, skip
                    }
                }
            });
        });
    }

    removeProjectConfigurations() {
        this.log('\n📁 清理项目配置...', 'info');

        // Remove config files in current directory
        this.configFiles.forEach(configFile => {
            this.safeRemove(
                path.join(this.initialDir, configFile),
                `配置文件: ${configFile}`
            );
        });

        // Remove Python cache and build files
        const pythonBuildDirs = [
            '__pycache__',
            '*.pyc',
            '*.pyo',
            'build',
            'dist',
            '*.egg-info'
        ];

        pythonBuildDirs.forEach(pattern => {
            if (pattern.includes('*')) {
                try {
                    const items = fs.readdirSync(this.initialDir);
                    items.forEach(item => {
                        if (item.endsWith('.pyc') ||
                            item.endsWith('.pyo') ||
                            item.endsWith('.egg-info') ||
                            item === 'build' ||
                            item === 'dist') {
                            this.safeRemove(
                                path.join(this.initialDir, item),
                                `Python 构建文件: ${item}`
                            );
                        }
                    });
                } catch (error) {
                    // Directory doesn't exist or can't read
                }
            } else {
                // Remove __pycache__ directories recursively
                this.removePyCacheDirectories(this.initialDir);
            }
        });
    }

    removePyCacheDirectories(dir) {
        try {
            const items = fs.readdirSync(dir);
            items.forEach(item => {
                const itemPath = path.join(dir, item);
                const stats = fs.statSync(itemPath);

                if (stats.isDirectory()) {
                    if (item === '__pycache__') {
                        this.safeRemove(itemPath, `Python 缓存目录: ${itemPath}`);
                    } else {
                        // Recursively check subdirectories
                        this.removePyCacheDirectories(itemPath);
                    }
                }
            });
        } catch (error) {
            // Can't read directory, skip
        }
    }

    removeEnvironmentVariables() {
        this.log('\n🌍 环境变量清理说明...', 'info');
        console.log('注意: 以下环境变量需要手动清理:');
        console.log('  - NPM_AUTH_TOKEN (如果设置了)');
        console.log('  - DNASPEC_* 相关环境变量');
        console.log('  - DNA_SPEC_* 相关环境变量');
    }

    cleanupNPMConfiguration() {
        this.log('\n⚙️  清理 NPM 配置...', 'info');

        try {
            const globalNpmrcPath = path.join(this.homeDir, '.npmrc');
            if (fs.existsSync(globalNpmrcPath)) {
                const npmrcContent = fs.readFileSync(globalNpmrcPath, 'utf8');

                // Remove DNASPEC-related configurations
                const lines = npmrcContent.split('\n');
                const filteredLines = lines.filter(line => {
                    return !line.includes('dnaspec') &&
                           !line.includes('dna-spec') &&
                           !line.includes('dna_context');
                });

                if (filteredLines.length !== lines.length) {
                    fs.writeFileSync(globalNpmrcPath, filteredLines.join('\n'));
                    this.log('清理全局 .npmrc 中的 DNASPEC 配置', 'success');
                    this.removedItems.push('NPM 配置清理');
                }
            }
        } catch (error) {
            this.log('清理 NPM 配置失败', 'error');
            this.failedItems.push({ item: 'NPM 配置清理', error: error.message });
        }
    }

    generateCleanupReport() {
        this.log('\n📋 清理报告', 'info');
        console.log('=' * 50);

        console.log(`\n✅ 成功删除的项目 (${this.removedItems.length}):`);
        if (this.removedItems.length > 0) {
            this.removedItems.forEach(item => {
                console.log(`  ✓ ${item}`);
            });
        } else {
            console.log('  (无)');
        }

        console.log(`\n❌ 删除失败的项目 (${this.failedItems.length}):`);
        if (this.failedItems.length > 0) {
            this.failedItems.forEach(item => {
                console.log(`  ✗ ${item.item}: ${item.error}`);
            });
        } else {
            console.log('  (无)');
        }

        console.log('\n💡 手动清理建议:');
        console.log('  1. 检查并手动删除任何残留的配置文件');
        console.log('  2. 清理环境变量 (如 NPM_AUTH_TOKEN)');
        console.log('  3. 重启终端或 IDE 以确保所有配置生效');
        console.log('  4. 检查 AI 工具中的自定义命令配置');

        // Save cleanup report
        const reportContent = {
            timestamp: new Date().toISOString(),
            removedItems: this.removedItems,
            failedItems: this.failedItems,
            platforms: this.platforms,
            pythonPackages: this.pythonPackages,
            npmPackages: this.npmPackages
        };

        try {
            const reportPath = path.join(this.initialDir, 'dnaspec-uninstall-report.json');
            fs.writeFileSync(reportPath, JSON.stringify(reportContent, null, 2));
            this.log(`清理报告已保存到: ${reportPath}`, 'success');
        } catch (error) {
            this.log('保存清理报告失败', 'warning');
        }
    }

    async run() {
        console.log('🚀 DNASPEC 完全卸载工具');
        console.log('=' * 50);
        console.log('⚠️  警告: 此操作将删除所有 DNASPEC 相关的文件和配置!');

        // Ask for confirmation
        const readline = require('readline');
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });

        const answer = await new Promise(resolve => {
            rl.question('\n确定要继续吗? (y/N): ', resolve);
        });
        rl.close();

        if (answer.toLowerCase() !== 'y' && answer.toLowerCase() !== 'yes') {
            console.log('卸载操作已取消');
            process.exit(0);
        }

        console.log('\n🔄 开始清理...\n');

        // Execute cleanup steps
        this.removeTempDirectories();
        this.removePythonPackages();
        this.removeNPMPackages();
        this.removePlatformConfigurations();
        this.removeProjectConfigurations();
        this.cleanupNPMConfiguration();
        this.removeEnvironmentVariables();

        // Generate report
        this.generateCleanupReport();

        console.log('\n🎉 DNASPEC 卸载完成!');
        console.log('💡 建议重启终端以确保所有更改生效');
    }
}

// Run uninstaller if called directly
if (require.main === module) {
    const uninstaller = new DNASPECUninstaller();
    uninstaller.run().catch(error => {
        console.error('卸载过程中发生错误:', error);
        process.exit(1);
    });
}

module.exports = DNASPECUninstaller;