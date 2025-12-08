# TDD驱动的任务分解 - 第一阶段：基础设施建设

## 1. 任务概述
实现npm包管理和初始化工具，使用户可以通过npm安装并初始化DSGS与spec.kit的集成。

## 2. TDD测试驱动开发计划

### 2.1 package.json创建测试
```javascript
// test/package.test.js
const fs = require('fs');
const path = require('path');

describe('Package Configuration', () => {
  test('should have valid package.json', () => {
    const packagePath = path.join(__dirname, '../package.json');
    expect(fs.existsSync(packagePath)).toBe(true);
    
    const packageJson = JSON.parse(fs.readFileSync(packagePath, 'utf8'));
    expect(packageJson.name).toBe('dnaspec-spec-kit');
    expect(packageJson.version).toMatch(/^\d+\.\d+\.\d+$/);
    expect(packageJson.bin).toBeDefined();
  });
  
  test('should have required scripts', () => {
    const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
    expect(packageJson.scripts.init).toBe('node bin/init.js');
    expect(packageJson.scripts.test).toBe('node bin/test.js');
  });
});
```

### 2.2 初始化工具功能测试
```javascript
// test/init.test.js
const { spawn } = require('child_process');

describe('Initialization Tool', () => {
  test('should detect system environment', async () => {
    const result = await runCommand('node bin/init.js --check-env');
    expect(result.stdout).toContain('Python version');
    expect(result.stdout).toContain('Git version');
  });
  
  test('should detect AI CLI tools', async () => {
    const result = await runCommand('node bin/init.js --detect-clis');
    expect(result.stdout).toMatch(/(claude|gemini|qwen)/);
  });
  
  test('should generate config file', async () => {
    const result = await runCommand('node bin/init.js --generate-config');
    expect(result.stdout).toContain('Configuration file generated');
  });
});

function runCommand(command) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, { shell: true });
    let stdout = '';
    let stderr = '';
    
    child.stdout.on('data', (data) => {
      stdout += data.toString();
    });
    
    child.stderr.on('data', (data) => {
      stderr += data.toString();
    });
    
    child.on('close', (code) => {
      resolve({ code, stdout, stderr });
    });
    
    child.on('error', (error) => {
      reject(error);
    });
  });
}
```

## 3. SOLID原则任务分解

### 3.1 单一职责原则 (SRP)
**任务1: package.json管理器**
- 职责: 管理npm包配置
- 依赖: 无
- 接口:
  ```javascript
  class PackageManager {
    validatePackageJson() { }
    updateVersion(version) { }
    addScript(name, command) { }
  }
  ```

**任务2: 环境检测器**
- 职责: 检测系统环境
- 依赖: child_process, os
- 接口:
  ```javascript
  class EnvironmentDetector {
    detectPython() { }
    detectGit() { }
    detectNode() { }
    getSystemInfo() { }
  }
  ```

**任务3: CLI检测器**
- 职责: 检测AI CLI工具
- 依赖: child_process
- 接口:
  ```javascript
  class CliDetector {
    detectClaude() { }
    detectGemini() { }
    detectQwen() { }
    getAllDetected() { }
  }
  ```

### 3.2 开放封闭原则 (OCP)
**任务4: 可扩展的CLI检测器**
- 设计: 支持插件化添加新的CLI检测
- 接口:
  ```javascript
  class ExtensibleCliDetector {
    registerDetector(name, detectorFunction) { }
    detectAll() { }
  }
  ```

### 3.3 里氏替换原则 (LSP)
**任务5: 检测器基类**
- 设计: 所有检测器遵循统一接口
- 接口:
  ```javascript
  class BaseDetector {
    detect() { }
    getVersion() { }
    isValid() { }
  }
  ```

### 3.4 接口隔离原则 (ISP)
**任务6: 最小接口设计**
- 设计: 每个模块只暴露必要的接口
- 示例:
  ```javascript
  // 只暴露初始化相关接口
  module.exports = {
    initialize: () => {},
    getConfig: () => {},
    saveConfig: (config) => {}
  };
  ```

### 3.5 依赖倒置原则 (DIP)
**任务7: 依赖注入**
- 设计: 通过构造函数注入依赖
- 示例:
  ```javascript
  class InitTool {
    constructor(detector, configManager) {
      this.detector = detector;
      this.configManager = configManager;
    }
  }
  ```

## 4. 具体实施任务清单

### 4.1 第一周任务

#### 任务1: 创建Node.js项目结构
**测试**: package.json存在性测试
**实现**:
```bash
mkdir node
cd node
npm init -y
```

**验收标准**:
- [ ] package.json文件创建成功
- [ ] 包含正确的name、version字段
- [ ] 包含bin和scripts配置

#### 任务2: 实现环境检测功能
**测试**: 环境检测功能测试
**实现**:
```javascript
// lib/environment.js
const { execSync } = require('child_process');

class EnvironmentDetector {
  detectPython() {
    try {
      const version = execSync('python --version', { encoding: 'utf8' });
      return { installed: true, version: version.trim() };
    } catch {
      return { installed: false };
    }
  }
  
  detectGit() {
    try {
      const version = execSync('git --version', { encoding: 'utf8' });
      return { installed: true, version: version.trim() };
    } catch {
      return { installed: false };
    }
  }
}
```

**验收标准**:
- [ ] 能正确检测Python安装状态
- [ ] 能正确检测Git安装状态
- [ ] 返回格式化的版本信息

#### 任务3: 实现基础CLI检测
**测试**: CLI检测功能测试
**实现**:
```javascript
// lib/cli-detector.js
class CliDetector {
  detectClaude() {
    try {
      const version = execSync('claude --version', { encoding: 'utf8' });
      return { installed: true, version: version.trim() };
    } catch {
      return { installed: false };
    }
  }
  
  // 类似实现其他CLI检测
}
```

**验收标准**:
- [ ] 能检测Claude CLI
- [ ] 能检测Gemini CLI
- [ ] 能检测Qwen CLI
- [ ] 返回检测结果和版本信息

### 4.2 第二周任务

#### 任务4: 实现配置文件生成
**测试**: 配置文件生成测试
**实现**:
```javascript
// lib/config-manager.js
class ConfigManager {
  generateConfig(detectedTools) {
    const config = {
      version: "1.0.0",
      platforms: this.mapPlatforms(detectedTools),
      skills: this.getDefaultSkills()
    };
    return config;
  }
  
  saveConfig(config, path) {
    fs.writeFileSync(path, YAML.stringify(config));
  }
}
```

**验收标准**:
- [ ] 生成标准YAML配置文件
- [ ] 包含检测到的CLI工具信息
- [ ] 包含默认技能配置
- [ ] 支持自定义保存路径

#### 任务5: 实现交互式初始化向导
**测试**: 交互式向导测试
**实现**:
```javascript
// bin/init.js
const inquirer = require('inquirer');

async function runInteractiveWizard() {
  const answers = await inquirer.prompt([
    {
      type: 'confirm',
      name: 'autoDetect',
      message: '自动检测AI CLI工具?',
      default: true
    },
    // 更多问题...
  ]);
  
  return answers;
}
```

**验收标准**:
- [ ] 支持自动检测模式
- [ ] 支持手动选择模式
- [ ] 提供友好的用户界面
- [ ] 生成用户确认的配置

#### 任务6: 实现命令行接口
**测试**: CLI命令测试
**实现**:
```javascript
// bin/cli.js
const { program } = require('commander');

program
  .name('dnaspec-spec-kit')
  .description('DNASPEC Skills for spec.kit integration')
  .version('1.0.0');

program
  .command('init')
  .description('Initialize DNASPEC spec.kit integration')
  .action(() => {
    // 初始化逻辑
  });

program.parse();
```

**验收标准**:
- [ ] 支持init命令
- [ ] 支持--help选项
- [ ] 支持版本查询
- [ ] 提供清晰的帮助信息

## 5. 质量保证措施

### 5.1 代码质量
- 使用ESLint进行代码检查
- 遵循JavaScript标准风格
- 100%测试覆盖率要求

### 5.2 文档质量
- 每个函数都有JSDoc注释
- 提供使用示例
- 包含错误处理说明

### 5.3 性能要求
- 初始化过程<30秒
- 内存使用<100MB
- 支持并发检测

## 6. 风险缓解

### 6.1 技术风险
- **跨平台兼容性**: 使用cross-spawn等跨平台库
- **权限问题**: 提供清晰的权限说明和错误提示
- **依赖管理**: 明确依赖版本，提供安装脚本

### 6.2 进度风险
- **功能复杂度**: 采用MVP方式，优先核心功能
- **测试覆盖**: TDD驱动，边开发边测试
- **代码审查**: 定期代码审查，确保质量

## 7. 交付物清单

### 7.1 代码交付物
- package.json配置文件
- bin/目录下的CLI工具
- lib/目录下的核心库
- test/目录下的测试文件

### 7.2 文档交付物
- README.md使用说明
- API文档
- 安装指南
- 故障排除指南

### 7.3 测试交付物
- 单元测试覆盖率报告
- 集成测试结果
- 性能测试报告
- 跨平台兼容性测试结果