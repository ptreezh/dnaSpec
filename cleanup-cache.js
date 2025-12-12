#!/usr/bin/env node

/**
 * DNASPEC Cache Cleanup Script
 * 清理 Python 缓存、构建文件和过期内容
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

class CacheCleaner {
    constructor() {
        this.initialDir = process.cwd();
        this.cleanedItems = [];
        this.failedItems = [];
    }

    log(message, type = 'info') {
        const icons = {
            info: '🔍',
            success: '✅',
            warning: '⚠️',
            error: '❌',
            cleaning: '🧹'
        };
        console.log(`${icons[type]} ${message}`);
    }

    safeRemove(itemPath, description) {
        try {
            if (fs.existsSync(itemPath)) {
                const stats = fs.statSync(itemPath);
                if (stats.isDirectory()) {
                    const files = fs.readdirSync(itemPath);
                    const fileSize = files.reduce((total, file) => {
                        const filePath = path.join(itemPath, file);
                        try {
                            return total + fs.statSync(filePath).size;
                        } catch (e) {
                            return total;
                        }
                    }, 0);

                    fs.rmSync(itemPath, { recursive: true, force: true });
                    this.log(`删除 ${description} (${files.length} 个文件, ${(fileSize / 1024).toFixed(1)} KB)`, 'success');
                    this.cleanedItems.push({ item: description, type: 'directory', files: files.length, size: fileSize });
                } else {
                    const stats = fs.statSync(itemPath);
                    fs.unlinkSync(itemPath);
                    this.log(`删除 ${description} (${(stats.size / 1024).toFixed(1)} KB)`, 'success');
                    this.cleanedItems.push({ item: description, type: 'file', size: stats.size });
                }
                return true;
            } else {
                this.log(`${description} 不存在`, 'warning');
                return true;
            }
        } catch (error) {
            this.log(`删除 ${description} 失败: ${error.message}`, 'error');
            this.failedItems.push({ item: description, error: error.message });
            return false;
        }
    }

    cleanPythonCache() {
        this.log('\n🧹 清理 Python 缓存...', 'cleaning');

        const patterns = [
            '**/__pycache__',
            '**/*.pyc',
            '**/*.pyo'
        ];

        patterns.forEach(pattern => {
            if (pattern.includes('*')) {
                this.cleanPattern(pattern);
            }
        });
    }

    cleanPattern(pattern) {
        const isRecursive = pattern.includes('**/');
        const basePattern = pattern.replace('**/', '');

        try {
            const items = fs.readdirSync(this.initialDir);
            items.forEach(item => {
                const itemPath = path.join(this.initialDir, item);

                if (fs.statSync(itemPath).isDirectory()) {
                    if (item === 'node_modules' || item.startsWith('.git')) {
                        return; // Skip important directories
                    }

                    if (basePattern === '__pycache__') {
                        this.cleanPyCacheDirectories(itemPath);
                    } else if (basePattern.endsWith('.pyc') || basePattern.endsWith('.pyo')) {
                        this.cleanFilesByPattern(itemPath, basePattern);
                    }
                } else {
                    // Handle files in root directory
                    if (basePattern.endsWith('.pyc') || basePattern.endsWith('.pyo')) {
                        if (item.endsWith('.pyc') || item.endsWith('.pyo')) {
                            this.safeRemove(itemPath, `Python 缓存文件: ${item}`);
                        }
                    }
                }
            });
        } catch (error) {
            this.log('读取目录失败', 'error');
        }
    }

    cleanPyCacheDirectories(dir) {
        try {
            const items = fs.readdirSync(dir);
            items.forEach(item => {
                const itemPath = path.join(dir, item);
                const stats = fs.statSync(itemPath);

                if (stats.isDirectory()) {
                    if (item === '__pycache__') {
                        this.safeRemove(itemPath, `Python 缓存目录: ${path.relative(this.initialDir, itemPath)}`);
                    } else if (!item.startsWith('.') && item !== 'node_modules') {
                        // Recursively clean subdirectories
                        this.cleanPyCacheDirectories(itemPath);
                    }
                }
            });
        } catch (error) {
            // Can't read directory, skip
        }
    }

    cleanFilesByPattern(dir, pattern) {
        try {
            const items = fs.readdirSync(dir);
            items.forEach(item => {
                if (item.endsWith('.pyc') || item.endsWith('.pyo')) {
                    const itemPath = path.join(dir, item);
                    this.safeRemove(itemPath, `Python 缓存文件: ${path.relative(this.initialDir, itemPath)}`);
                }
            });
        } catch (error) {
            // Can't read directory, skip
        }
    }

    cleanBuildArtifacts() {
        this.log('\n🏗️  清理构建文件...', 'cleaning');

        const buildDirs = ['build', 'dist'];
        buildDirs.forEach(dir => {
            this.safeRemove(path.join(this.initialDir, dir), `构建目录: ${dir}`);
        });

        // Clean .egg-info directories
        try {
            const items = fs.readdirSync(this.initialDir);
            items.forEach(item => {
                if (item.endsWith('.egg-info')) {
                    this.safeRemove(path.join(this.initialDir, item), `Egg-info 目录: ${item}`);
                }
            });
        } catch (error) {
            // Can't read directory, skip
        }
    }

    cleanTempFiles() {
        this.log('\n🗂️  清理临时文件...', 'cleaning');

        const tempPatterns = [
            '*.tmp',
            '*.temp',
            '*.log',
            'dnaspec-install-tmp*',
            'dnaspec-temp-*',
            'coverage*',
            '.coverage',
            'nosetests.xml'
        ];

        tempPatterns.forEach(pattern => {
            this.safeRemove(path.join(this.initialDir, pattern), `临时文件: ${pattern}`);
        });
    }

    cleanBackupFiles() {
        this.log('\n💾 清理备份文件...', 'cleaning');

        const backupPatterns = [
            '*.bak',
            '*.backup',
            '*~',
            '*.orig',
            '*.swp',
            '*.swo'
        ];

        backupPatterns.forEach(pattern => {
            this.safeRemove(path.join(this.initialDir, pattern), `备份文件: ${pattern}`);
        });
    }

    cleanIDEFiles() {
        this.log('\n💻 清理 IDE 文件...', 'cleaning');

        const idePatterns = [
            '.vscode/settings.json',
            '.vscode/launch.json',
            '.vscode/extensions.json',
            '.idea/*',
            '*.sublime-*'
        ];

        // Only clean IDE settings, not workspace files
        const filesToClean = ['.vscode/settings.json', '.vscode/launch.json', '.vscode/extensions.json'];
        filesToClean.forEach(file => {
            this.safeRemove(path.join(this.initialDir, file), `IDE 配置: ${file}`);
        });
    }

    cleanNodeModulesCache() {
        this.log('\n📦 清理 NPM 缓存...', 'cleaning');

        try {
            // Clean npm cache
            execSync('npm cache clean --force', { stdio: 'pipe' });
            this.log('NPM 缓存已清理', 'success');
            this.cleanedItems.push({ item: 'NPM 缓存', type: 'cache' });
        } catch (error) {
            this.log('清理 NPM 缓存失败', 'error');
            this.failedItems.push({ item: 'NPM 缓存', error: error.message });
        }

        // Clean node_modules/.cache if exists
        const nodeCachePath = path.join(this.initialDir, 'node_modules', '.cache');
        this.safeRemove(nodeCachePath, 'Node.js 缓存目录');
    }

    cleanPythonPackages() {
        this.log('\n🐍 清理重复的 Python 包...', 'cleaning');

        // Check for duplicate packages and clean up
        const pythonCommands = ['python', 'python3', 'py'];

        pythonCommands.forEach(pythonCmd => {
            try {
                execSync(`${pythonCmd} --version`, { stdio: 'pipe' });

                // Get list of installed packages
                try {
                    const result = execSync(`${pythonCmd} -m pip list`, {
                        encoding: 'utf-8',
                        stdio: 'pipe'
                    });

                    const packages = result.split('\n')
                        .filter(line => line.includes('dnaspec') || line.includes('dna-context') || line.includes('dna-spec'))
                        .map(line => line.split(/\s+/)[0]);

                    if (packages.length > 0) {
                        this.log(`发现 ${packages.length} 个 DNASPEC 相关的 Python 包`, 'warning');
                        packages.forEach(pkg => {
                            this.log(`  - ${pkg}`, 'info');
                        });
                    }
                } catch (error) {
                    this.log('无法获取 Python 包列表', 'warning');
                }

                return; // Stop after finding working Python command
            } catch (error) {
                // Python command not found, try next
            }
        });
    }

    generateCleanupReport() {
        this.log('\n📋 清理报告', 'info');
        console.log('='.repeat(50));

        const totalFiles = this.cleanedItems.length;
        const totalFailed = this.failedItems.length;

        // Calculate total size cleaned
        const totalSize = this.cleanedItems.reduce((total, item) => {
            return total + (item.size || 0);
        }, 0);

        const totalFilesCount = this.cleanedItems.reduce((total, item) => {
            return total + (item.files || (item.type === 'file' ? 1 : 0));
        }, 0);

        console.log(`\n📊 清理统计:`);
        console.log(`  删除项目: ${totalFiles} 个`);
        console.log(`  删除文件: ${totalFilesCount} 个`);
        console.log(`  释放空间: ${(totalSize / 1024).toFixed(1)} KB`);
        console.log(`  失败项目: ${totalFailed} 个`);

        if (totalFiles > 0) {
            console.log(`\n✅ 成功清理的项目:`);
            this.cleanedItems.forEach(item => {
                let description = `  - ${item.item}`;
                if (item.type === 'directory' && item.files) {
                    description += ` (${item.files} 个文件)`;
                }
                console.log(description);
            });
        }

        if (totalFailed > 0) {
            console.log(`\n❌ 清理失败的项目:`);
            this.failedItems.forEach(item => {
                console.log(`  - ${item.item}: ${item.error}`);
            });
        }

        console.log(`\n💡 建议:`);
        console.log(`  - 定期运行此清理脚本以保持项目整洁`);
        console.log(`  - 考虑将清理命令添加到 git hooks 中`);
        console.log(`  - 大文件已清理，项目大小将显著减少`);

        // Save cleanup report
        const reportContent = {
            timestamp: new Date().toISOString(),
            cleanedItems: this.cleanedItems,
            failedItems: this.failedItems,
            statistics: {
                totalItems: totalFiles,
                totalFiles: totalFilesCount,
                totalSizeBytes: totalSize,
                totalSizeKB: Math.round(totalSize / 1024 * 100) / 100,
                totalFailed: totalFailed
            }
        };

        try {
            const reportPath = path.join(this.initialDir, 'dnaspec-cleanup-report.json');
            fs.writeFileSync(reportPath, JSON.stringify(reportContent, null, 2));
            this.log(`清理报告已保存到: ${reportPath}`, 'success');
        } catch (error) {
            this.log('保存清理报告失败', 'warning');
        }
    }

    async run() {
        console.log('🧹 DNASPEC 缓存清理工具');
        console.log('=' * 50);
        console.log('此工具将清理 Python 缓存、构建文件和临时内容\n');

        // Run cleanup steps
        this.cleanPythonCache();
        this.cleanBuildArtifacts();
        this.cleanTempFiles();
        this.cleanBackupFiles();
        this.cleanIDEFiles();
        this.cleanNodeModulesCache();
        this.cleanPythonPackages();

        // Generate report
        this.generateCleanupReport();

        console.log('\n🎉 缓存清理完成!');
        console.log('💡 建议运行 git status 查看清理后的文件状态');
    }
}

// Run cleanup if called directly
if (require.main === module) {
    const cleaner = new CacheCleaner();
    cleaner.run().catch(error => {
        console.error('清理过程中发生错误:', error);
        process.exit(1);
    });
}

module.exports = CacheCleaner;