#!/usr/bin/env node

/**
 * DNASPEC 依赖分析工具
 * 分析和验证项目依赖配置
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class DependencyAnalyzer {
  constructor() {
    this.projectRoot = path.join(__dirname, '..');
    this.packageJson = path.join(this.projectRoot, 'package.json');
    this.analysisResults = {
      used: new Set(),
      declared: new Set(),
      unused: new Set(),
      missing: new Set(),
      critical: new Set(),
      optional: new Set()
    };
  }

  // 分析实际使用的依赖
  analyzeUsedDependencies() {
    console.log('🔍 扫描项目中的依赖使用情况...\n');

    const jsFiles = this.findJavaScriptFiles();
    const requiredDeps = new Set();

    jsFiles.forEach(file => {
      const content = fs.readFileSync(file, 'utf8');
      
      // 匹配 require 语句
      const requireMatches = content.match(/require\(['"]([^'"]+)['"]\)/g) || [];
      
      requireMatches.forEach(match => {
        const dep = match.match(/require\(['"]([^'"]+)['"]\)/)[1];
        
        // 过滤掉Node.js内置模块和相对路径
        if (!this.isBuiltInModule(dep) && !dep.startsWith('./') && !dep.startsWith('../')) {
          requiredDeps.add(dep);
        }
      });
    });

    this.analysisResults.used = requiredDeps;
    return requiredDeps;
  }

  // 检查是否为Node.js内置模块
  isBuiltInModule(moduleName) {
    const builtInModules = [
      'assert', 'async_hooks', 'buffer', 'child_process', 'cluster',
      'console', 'constants', 'crypto', 'dgram', 'dns', 'domain', 'events',
      'fs', 'http', 'http2', 'https', 'inspector', 'module', 'net', 'os',
      'path', 'perf_hooks', 'process', 'punycode', 'querystring', 'readline',
      'repl', 'stream', 'string_decoder', 'sys', 'timers', 'tls', 'trace_events',
      'tty', 'url', 'util', 'v8', 'vm', 'wasi', 'worker_threads', 'zlib'
    ];
    
    return builtInModules.includes(moduleName);
  }

  // 查找所有JavaScript文件
  findJavaScriptFiles() {
    const jsFiles = [];
    
    function scanDirectory(dir) {
      const items = fs.readdirSync(dir);
      
      items.forEach(item => {
        const fullPath = path.join(dir, item);
        const stat = fs.statSync(fullPath);
        
        if (stat.isDirectory() && !item.startsWith('.') && item !== 'node_modules') {
          scanDirectory(fullPath);
        } else if (stat.isFile() && item.endsWith('.js')) {
          jsFiles.push(fullPath);
        }
      });
    }
    
    scanDirectory(this.projectRoot);
    return jsFiles;
  }

  // 读取package.json中的依赖
  readDeclaredDependencies() {
    if (!fs.existsSync(this.packageJson)) {
      throw new Error('package.json not found');
    }

    const packageData = JSON.parse(fs.readFileSync(this.packageJson, 'utf8'));
    const declared = new Set();

    // 收集所有依赖
    ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies'].forEach(depType => {
      if (packageData[depType]) {
        Object.keys(packageData[depType]).forEach(dep => {
          declared.add(dep);
        });
      }
    });

    this.analysisResults.declared = declared;
    return declared;
  }

  // 分类依赖
  categorizeDependencies() {
    const used = this.analysisResults.used;
    const declared = this.analysisResults.declared;

    // 未使用的依赖
    this.analysisResults.unused = new Set([...declared].filter(dep => !used.has(dep)));

    // 缺失的依赖
    this.analysisResults.missing = new Set([...used].filter(dep => !declared.has(dep)));

    // 关键依赖（实际使用且已声明）
    this.analysisResults.critical = new Set([...used].filter(dep => declared.has(dep)));

    // 可选依赖（在CLI中有try-catch处理的）
    const optionalDeps = ['fs-extra', 'commander', 'inquirer'];
    this.analysisResults.optional = new Set(optionalDeps.filter(dep => declared.has(dep)));
  }

  // 生成分析报告
  generateReport() {
    console.log('📊 依赖分析报告\n');
    console.log('='.repeat(50));

    // 关键依赖
    if (this.analysisResults.critical.size > 0) {
      console.log('\n✅ 关键依赖 (实际使用):');
      [...this.analysisResults.critical].sort().forEach(dep => {
        console.log(`  • ${dep}`);
      });
    }

    // 可选依赖
    if (this.analysisResults.optional.size > 0) {
      console.log('\n🔄 可选依赖 (带回退机制):');
      [...this.analysisResults.optional].sort().forEach(dep => {
        console.log(`  • ${dep} (有简化模式)`);
      });
    }

    // 未使用的依赖
    if (this.analysisResults.unused.size > 0) {
      console.log('\n⚠️  未使用的依赖:');
      [...this.analysisResults.unused].sort().forEach(dep => {
        console.log(`  • ${dep} (建议移除)`);
      });
    }

    // 缺失的依赖
    if (this.analysisResults.missing.size > 0) {
      console.log('\n❌ 缺失的依赖:');
      [...this.analysisResults.missing].sort().forEach(dep => {
        console.log(`  • ${dep} (需要添加到package.json)`);
      });
    }

    // 统计信息
    console.log('\n📈 统计信息:');
    console.log(`  总计声明: ${this.analysisResults.declared.size}`);
    console.log(`  实际使用: ${this.analysisResults.used.size}`);
    console.log(`  关键依赖: ${this.analysisResults.critical.size}`);
    console.log(`  可选依赖: ${this.analysisResults.optional.size}`);
    console.log(`  未使用: ${this.analysisResults.unused.size}`);
    console.log(`  缺失: ${this.analysisResults.missing.size}`);
  }

  // 生成优化的package.json建议
  generateOptimizationSuggestions() {
    console.log('\n💡 优化建议:\n');

    // 检查依赖版本
    console.log('1. 版本优化:');
    const currentPackage = JSON.parse(fs.readFileSync(this.packageJson, 'utf8'));
    
    if (currentPackage.dependencies) {
      Object.entries(currentPackage.dependencies).forEach(([dep, version]) => {
        if (version.includes('^')) {
          console.log(`   • ${dep}: 当前使用 ^${version.slice(1)} (建议固定版本以确保稳定性)`);
        }
      });
    }

    // 依赖分类建议
    console.log('\n2. 依赖分类:');
    console.log('   • 将 "commander", "fs-extra", "inquirer" 移至 optionalDependencies');
    console.log('   • 保持 "execa", "glob" 在 dependencies 中');

    // 安装后验证
    console.log('\n3. 安装后验证:');
    console.log('   • 添加依赖验证脚本');
    console.log('   • 检查关键依赖是否正确安装');
  }

  // 验证当前依赖状态
  validateDependencies() {
    console.log('\n🔍 验证依赖状态...\n');

    try {
      // 检查关键依赖
      const criticalDeps = ['fs-extra', 'commander'];
      criticalDeps.forEach(dep => {
        try {
          require(dep);
          console.log(`✅ ${dep}: 可用`);
        } catch (error) {
          console.log(`⚠️  ${dep}: 不可用 (${error.code})`);
        }
      });

      // 检查包完整性
      try {
        execSync('npm list --depth=0', { stdio: 'pipe' });
        console.log('✅ 包完整性检查通过');
      } catch (error) {
        console.log('❌ 包完整性检查失败');
        console.log('建议运行: npm install');
      }

    } catch (error) {
      console.log('❌ 依赖验证失败:', error.message);
    }
  }

  // 运行完整分析
  run() {
    console.log('🚀 DNASPEC 依赖分析工具 v2.0.0\n');

    try {
      this.analyzeUsedDependencies();
      this.readDeclaredDependencies();
      this.categorizeDependencies();
      this.generateReport();
      this.generateOptimizationSuggestions();
      this.validateDependencies();

      console.log('\n✅ 依赖分析完成!');
      
    } catch (error) {
      console.error('❌ 分析失败:', error.message);
      process.exit(1);
    }
  }
}

// 如果直接运行此脚本
if (require.main === module) {
  const analyzer = new DependencyAnalyzer();
  analyzer.run();
}

module.exports = DependencyAnalyzer;