#!/usr/bin/env node

/**
 * DNASPEC Uninstall Dry Run Script - 模拟卸载过程
 * 仅显示将要删除的内容，不执行实际删除操作
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

class DNASPECDryRun {
    constructor() {
        this.initialDir = process.cwd();
        this.homeDir = os.homedir();
        this.wouldRemoveItems = [];
        this.notFoundItems = [];

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
            found: '✅',
            notfound: '❌',
            warning: '⚠️'
        };
        console.log(`${icons[type]} ${message}`);
    }

    checkFile(filePath, description) {
        try {
            if (fs.existsSync(filePath)) {
                const stats = fs.statSync(filePath);
                this.wouldRemoveItems.push({
                    type: stats.isDirectory() ? 'directory' : 'file',
                    path: filePath,
                    description: description,
                    size: stats.isDirectory() ? 'N/A' : `${stats.size} bytes`
                });
                this.log(`发现: ${description}`, 'found');
                return true;
            } else {
                this.notFoundItems.push(description);
                this.log(`未找到: ${description}`, 'notfound');
                return false;
            }
        } catch (error) {
            this.notFoundItems.push(description);
            this.log(`无法访问: ${description} - ${error.message}`, 'warning');
            return false;
        }
    }

    checkPythonPackages() {
        this.log('\n🐍 检查 Python 包...', 'info');

        const pythonCommands = ['python', 'python3', 'py'];

        pythonCommands.forEach(pythonCmd => {
            try {
                execSync(`${pythonCmd} --version`, { stdio: 'pipe' });

                this.pythonPackages.forEach(pkg => {
                    try {
                        const result = execSync(`${pythonCmd} -m pip show ${pkg}`, {
                            encoding: 'utf-8',
                            stdio: 'pipe'
                        });

                        const lines = result.split('\n');
                        const version = lines.find(line => line.startsWith('Version:'))?.split(': ')[1] || 'Unknown';
                        const location = lines.find(line => line.startsWith('Location:'))?.split(': ')[1] || 'Unknown';

                        this.wouldRemoveItems.push({
                            type: 'python-package',
                            name: pkg,
                            version: version,
                            location: location,
                            python: pythonCmd,
                            command: `${pythonCmd} -m pip uninstall -y ${pkg}`
                        });

                        this.log(`发现 Python 包: ${pkg} (版本: ${version})`, 'found');
                    } catch (error) {
                        this.notFoundItems.push(`Python 包: ${pkg}`);
                    }
                });

                // Also check with pip directly
                this.pythonPackages.forEach(pkg => {
                    try {
                        const result = execSync(`pip show ${pkg}`, {
                            encoding: 'utf-8',
                            stdio: 'pipe'
                        });

                        const lines = result.split('\n');
                        const version = lines.find(line => line.startsWith('Version:'))?.split(': ')[1] || 'Unknown';
                        const location = lines.find(line => line.startsWith('Location:'))?.split(': ')[1] || 'Unknown';

                        this.wouldRemoveItems.push({
                            type: 'python-package',
                            name: pkg,
                            version: version,
                            location: location,
                            python: 'pip',
                            command: `pip uninstall -y ${pkg}`
                        });

                        this.log(`发现 Python 包 (pip): ${pkg} (版本: ${version})`, 'found');
                    } catch (error) {
                        // Already checked with python -m pip
                    }
                });

                return;
            } catch (error) {
                // Python command not found, try next
            }
        });
    }

    checkNPMPackages() {
        this.log('\n📦 检查 NPM 包...', 'info');

        this.npmPackages.forEach(pkg => {
            // Check global packages
            try {
                const result = execSync(`npm list -g --depth=0 ${pkg}`, {
                    encoding: 'utf-8',
                    stdio: 'pipe'
                });

                const lines = result.split('\n');
                const versionLine = lines.find(line => line.includes(pkg));
                if (versionLine) {
                    const version = versionLine.match(/@(.+)$/)?.[1] || 'Unknown';
                    this.wouldRemoveItems.push({
                        type: 'npm-global-package',
                        name: pkg,
                        version: version,
                        command: `npm uninstall -g ${pkg}`
                    });
                    this.log(`发现全局 NPM 包: ${pkg} (版本: ${version})`, 'found');
                }
            } catch (error) {
                this.notFoundItems.push(`全局 NPM 包: ${pkg}`);
            }

            // Check local packages
            try {
                const result = execSync(`npm list --depth=0 ${pkg}`, {
                    encoding: 'utf-8',
                    stdio: 'pipe'
                });

                const lines = result.split('\n');
                const versionLine = lines.find(line => line.includes(pkg));
                if (versionLine) {
                    const version = versionLine.match(/@(.+)$/)?.[1] || 'Unknown';
                    this.wouldRemoveItems.push({
                        type: 'npm-local-package',
                        name: pkg,
                        version: version,
                        command: `npm uninstall ${pkg}`
                    });
                    this.log(`发现本地 NPM 包: ${pkg} (版本: ${version})`, 'found');
                }
            } catch (error) {
                this.notFoundItems.push(`本地 NPM 包: ${pkg}`);
            }
        });
    }

    checkPlatformConfigurations() {
        this.log('\n🔧 检查平台配置...', 'info');

        Object.entries(this.platforms).forEach(([platform, dirs]) => {
            dirs.forEach(dir => {
                const platformPath = path.join(this.homeDir, dir);

                if (fs.existsSync(platformPath)) {
                    try {
                        const files = fs.readdirSync(platformPath, { withFileTypes: true });
                        let foundDNASPECFiles = false;

                        files.forEach(file => {
                            const fileName = file.name;
                            const filePath = path.join(platformPath, fileName);

                            if (fileName.toLowerCase().includes('dnaspec') ||
                                fileName.toLowerCase().includes('dna-spec') ||
                                fileName.toLowerCase().includes('dna_context') ||
                                (fileName.includes('skill') && fileName.includes('dna'))) {

                                this.wouldRemoveItems.push({
                                    type: 'platform-config',
                                    platform: platform,
                                    name: fileName,
                                    path: filePath,
                                    itemType: file.isDirectory() ? 'directory' : 'file'
                                });

                                this.log(`发现 ${platform} 配置: ${fileName}`, 'found');
                                foundDNASPECFiles = true;
                            }
                        });

                        if (foundDNASPECFiles) {
                            this.log(`在 ${platform} 平台目录中发现了 DNASPEC 配置`, 'warning');
                        }
                    } catch (error) {
                        this.log(`无法读取 ${platform} 平台目录: ${error.message}`, 'warning');
                    }
                } else {
                    this.notFoundItems.push(`${platform} 平台目录: ${dir}`);
                }
            });
        });
    }

    checkProjectConfigurations() {
        this.log('\n📁 检查项目配置...', 'info');

        // Check config files
        this.configFiles.forEach(configFile => {
            this.checkFile(
                path.join(this.initialDir, configFile),
                `项目配置文件: ${configFile}`
            );
        });

        // Check Python build files
        const pythonBuildPatterns = ['__pycache__', '*.pyc', '*.pyo', 'build', 'dist', '*.egg-info'];

        try {
            const items = fs.readdirSync(this.initialDir);
            items.forEach(item => {
                if (item === '__pycache__' || item === 'build' || item === 'dist') {
                    this.checkFile(
                        path.join(this.initialDir, item),
                        `Python 构建目录: ${item}`
                    );
                } else if (item.endsWith('.pyc') || item.endsWith('.pyo')) {
                    this.checkFile(
                        path.join(this.initialDir, item),
                        `Python 缓存文件: ${item}`
                    );
                } else if (item.includes('.egg-info')) {
                    this.checkFile(
                        path.join(this.initialDir, item),
                        `Python egg-info: ${item}`
                    );
                }
            });
        } catch (error) {
            this.log('无法读取项目目录', 'warning');
        }

        // Recursively check for __pycache__ directories
        this.checkPyCacheDirectories(this.initialDir);
    }

    checkPyCacheDirectories(dir) {
        try {
            const items = fs.readdirSync(dir);
            items.forEach(item => {
                const itemPath = path.join(dir, item);
                const stats = fs.statSync(itemPath);

                if (stats.isDirectory()) {
                    if (item === '__pycache__') {
                        this.checkFile(itemPath, `Python 缓存目录: ${itemPath}`);
                    } else if (!item.startsWith('.') && !item.startsWith('node_modules')) {
                        // Recursively check subdirectories (skip hidden and node_modules)
                        this.checkPyCacheDirectories(itemPath);
                    }
                }
            });
        } catch (error) {
            // Can't read directory, skip
        }
    }

    checkTempDirectories() {
        this.log('\n🗑️  检查临时目录...', 'info');

        this.tempDirs.forEach(pattern => {
            if (pattern.includes('*')) {
                const basePattern = pattern.replace('*', '');
                try {
                    const items = fs.readdirSync(this.initialDir);
                    items.forEach(item => {
                        if (item.startsWith(basePattern)) {
                            this.checkFile(
                                path.join(this.initialDir, item),
                                `临时目录: ${item}`
                            );
                        }
                    });
                } catch (error) {
                    // Directory doesn't exist or can't read
                }
            } else {
                this.checkFile(
                    path.join(this.initialDir, pattern),
                    `临时目录: ${pattern}`
                );
            }
        });
    }

    checkNPMConfiguration() {
        this.log('\n⚙️  检查 NPM 配置...', 'info');

        const globalNpmrcPath = path.join(this.homeDir, '.npmrc');
        if (fs.existsSync(globalNpmrcPath)) {
            try {
                const npmrcContent = fs.readFileSync(globalNpmrcPath, 'utf8');
                const lines = npmrcContent.split('\n');
                let foundDNASPECConfig = false;

                lines.forEach((line, index) => {
                    if (line.includes('dnaspec') ||
                        line.includes('dna-spec') ||
                        line.includes('dna_context')) {
                        this.wouldRemoveItems.push({
                            type: 'npm-config',
                            file: globalNpmrcPath,
                            lineNumber: index + 1,
                            content: line.trim()
                        });
                        this.log(`发现 NPM 配置: ${line.trim()}`, 'found');
                        foundDNASPECConfig = true;
                    }
                });

                if (!foundDNASPECConfig) {
                    this.notFoundItems.push('NPM 配置中的 DNASPEC 设置');
                }
            } catch (error) {
                this.log(`无法读取 NPM 配置: ${error.message}`, 'warning');
            }
        } else {
            this.notFoundItems.push('全局 NPM 配置文件');
        }
    }

    generateDryRunReport() {
        this.log('\n📋 干运行报告', 'info');
        console.log('='.repeat(60));

        // Statistics
        const totalFound = this.wouldRemoveItems.length;
        const totalNotFound = this.notFoundItems.length;

        console.log(`\n📊 统计信息:`);
        console.log(`  将删除项目: ${totalFound} 个`);
        console.log(`  未找到项目: ${totalNotFound} 个`);

        if (totalFound > 0) {
            console.log(`\n✅ 将要删除的内容:`);

            // Group by type
            const grouped = this.wouldRemoveItems.reduce((acc, item) => {
                const type = item.type;
                if (!acc[type]) acc[type] = [];
                acc[type].push(item);
                return acc;
            }, {});

            Object.entries(grouped).forEach(([type, items]) => {
                console.log(`\n  📂 ${type.toUpperCase()} (${items.length} 个):`);
                items.forEach(item => {
                    if (type.includes('package')) {
                        console.log(`    - ${item.name} v${item.version}`);
                        console.log(`      命令: ${item.command}`);
                    } else if (type === 'platform-config') {
                        console.log(`    - ${item.platform}/${item.name}`);
                    } else {
                        console.log(`    - ${item.description || item.path}`);
                    }
                });
            });
        }

        if (totalNotFound > 0) {
            console.log(`\n❌ 未找到的内容 (${totalNotFound} 个):`);
            this.notFoundItems.forEach(item => {
                console.log(`    - ${item}`);
            });
        }

        console.log(`\n⚠️  重要说明:`);
        console.log(`  - 这是干运行模式，没有执行任何删除操作`);
        console.log(`  - 要执行实际删除，请运行: node uninstall.js`);
        console.log(`  - 某些项目可能需要手动删除`);
        console.log(`  - 建议在执行实际删除前备份重要数据`);

        // Save dry run report
        const reportContent = {
            timestamp: new Date().toISOString(),
            mode: 'dry-run',
            wouldRemoveItems: this.wouldRemoveItems,
            notFoundItems: this.notFoundItems,
            statistics: {
                totalFound,
                totalNotFound
            }
        };

        try {
            const reportPath = path.join(this.initialDir, 'dnaspec-dry-run-report.json');
            fs.writeFileSync(reportPath, JSON.stringify(reportContent, null, 2));
            this.log(`干运行报告已保存到: ${reportPath}`, 'info');
        } catch (error) {
            this.log('保存干运行报告失败', 'warning');
        }
    }

    async run() {
        console.log('🔍 DNASPEC 卸载干运行工具');
        console.log('=' * 60);
        console.log('ℹ️  仅显示将要删除的内容，不执行实际删除操作\n');

        // Run checks
        this.checkTempDirectories();
        this.checkPythonPackages();
        this.checkNPMPackages();
        this.checkPlatformConfigurations();
        this.checkProjectConfigurations();
        this.checkNPMConfiguration();

        // Generate report
        this.generateDryRunReport();

        console.log('\n🎉 干运行完成!');
    }
}

// Run dry run if called directly
if (require.main === module) {
    const dryRun = new DNASPECDryRun();
    dryRun.run().catch(error => {
        console.error('干运行过程中发生错误:', error);
        process.exit(1);
    });
}

module.exports = DNASPECDryRun;