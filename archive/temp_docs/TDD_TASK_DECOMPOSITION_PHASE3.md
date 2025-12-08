# TDD驱动的任务分解 - 第三阶段：智能集成

## 1. 任务概述
实现AI CLI工具的自动检测、配置和集成验证功能，使用户可以轻松地将DSGS技能集成到各种AI编码工具中。

## 2. TDD测试驱动开发计划

### 2.1 AI CLI检测器测试
```javascript
// test/cli-detector.test.js
const { CliDetector } = require('../lib/cli-detector');

describe('CLI Detector', () => {
  let detector;
  
  beforeEach(() => {
    detector = new CliDetector();
  });
  
  test('should detect Claude CLI', async () => {
    const result = await detector.detectClaude();
    expect(result.installed).toBe(true);
    expect(result.version).toMatch(/\d+\.\d+\.\d+/);
  });
  
  test('should detect all installed CLIs', async () => {
    const results = await detector.detectAll();
    expect(results).toHaveProperty('claude');
    expect(results).toHaveProperty('gemini');
    expect(results).toHaveProperty('qwen');
  });
  
  test('should handle detection errors gracefully', async () => {
    // 模拟检测失败
    const result = await detector.detectUnknownCli('nonexistent');
    expect(result.installed).toBe(false);
  });
});
```

### 2.2 配置生成器测试
```javascript
// test/config-generator.test.js
const { ConfigGenerator } = require('../lib/config-generator');

describe('Config Generator', () => {
  let generator;
  
  beforeEach(() => {
    generator = new ConfigGenerator();
  });
  
  test('should generate config for detected tools', () => {
    const detectedTools = {
      claude: { installed: true, version: '1.0.0' },
      gemini: { installed: false }
    };
    
    const config = generator.generate(detectedTools);
    expect(config.platforms).toHaveLength(1);
    expect(config.platforms[0].name).toBe('claude');
    expect(config.platforms[0].enabled).toBe(true);
  });
  
  test('should save config to file', () => {
    const config = { version: '1.0.0' };
    const result = generator.save(config, './test-config.yaml');
    expect(result).toBe(true);
    // 验证文件是否存在
  });
  
  test('should validate config structure', () => {
    const validConfig = {
      version: '1.0.0',
      platforms: [],
      skills: {}
    };
    
    expect(generator.validate(validConfig)).toBe(true);
    
    const invalidConfig = { version: '1.0.0' };
    expect(generator.validate(invalidConfig)).toBe(false);
  });
});
```

### 2.3 集成验证器测试
```javascript
// test/integration-validator.test.js
const { IntegrationValidator } = require('../lib/integration-validator');

describe('Integration Validator', () => {
  let validator;
  
  beforeEach(() => {
    validator = new IntegrationValidator();
  });
  
  test('should validate Claude integration', async () => {
    const result = await validator.validateClaudeIntegration();
    expect(result.valid).toBe(true);
    expect(result.skills).toContain('dnaspec-architect');
  });
  
  test('should run performance test', async () => {
    const result = await validator.runPerformanceTest();
    expect(result.averageResponseTime).toBeLessThan(2000); // 2秒
    expect(result.successRate).toBeGreaterThan(0.95); // 95%成功率
  });
  
  test('should generate validation report', () => {
    const results = {
      claude: { valid: true },
      gemini: { valid: false, error: 'Not installed' }
    };
    
    const report = validator.generateReport(results);
    expect(report).toContain('Integration Validation Report');
    expect(report).toContain('Claude: ✓');
    expect(report).toContain('Gemini: ✗');
  });
});
```

## 3. SOLID原则任务分解

### 3.1 单一职责原则 (SRP)

#### 任务1: CLI检测器
- **职责**: 检测各种AI CLI工具的安装状态
- **依赖**: child_process
- **接口**:
  ```javascript
  class CliDetector {
    detectClaude() { }
    detectGemini() { }
    detectQwen() { }
    detectAll() { }
  }
  ```

#### 任务2: 配置生成器
- **职责**: 根据检测结果生成配置文件
- **依赖**: fs, yaml
- **接口**:
  ```javascript
  class ConfigGenerator {
    generate(detectedTools) { }
    save(config, filePath) { }
    validate(config) { }
  }
  ```

#### 任务3: 集成验证器
- **职责**: 验证AI CLI工具与DSGS技能的集成
- **依赖**: 技能执行器
- **接口**:
  ```javascript
  class IntegrationValidator {
    validateClaudeIntegration() { }
    validateGeminiIntegration() { }
    runPerformanceTest() { }
    generateReport(validationResults) { }
  }
  ```

### 3.2 开放封闭原则 (OCP)

#### 任务4: 可扩展的检测器
- **设计**: 支持插件化添加新的CLI检测
- **接口**:
  ```javascript
  class ExtensibleCliDetector {
    registerDetector(name, detectorFunction) { }
    detect(name) { }
    getAllDetectors() { }
  }
  ```

### 3.3 里氏替换原则 (LSP)

#### 任务5: 检测器基类
- **设计**: 所有CLI检测器遵循统一接口
- **接口**:
  ```javascript
  class BaseCliDetector {
    detect() { }
    getVersion() { }
    getInstallPath() { }
  }
  ```

### 3.4 接口隔离原则 (ISP)

#### 任务6: 最小接口设计
- **设计**: 每个模块只暴露必要的接口
- **示例**:
  ```javascript
  // 只暴露配置管理相关接口
  module.exports = {
    generateConfig: (tools) => {},
    saveConfig: (config, path) => {},
    loadConfig: (path) => {}
  };
  ```

### 3.5 依赖倒置原则 (DIP)

#### 任务7: 依赖注入
- **设计**: 通过构造函数注入依赖
- **示例**:
  ```javascript
  class AutoConfigurator {
    constructor(cliDetector, configGenerator, validator) {
      this.cliDetector = cliDetector;
      this.configGenerator = configGenerator;
      this.validator = validator;
    }
  }
  ```

## 4. 具体实施任务清单

### 4.1 第一周任务

#### 任务1: 实现完整的CLI检测器
**测试**: CLI检测功能测试
**实现**:
```javascript
// lib/cli-detector.js
const { execSync } = require('child_process');
const { platform } = require('os');

class CliDetector {
  constructor() {
    this.detectors = {
      claude: this.detectClaude.bind(this),
      gemini: this.detectGemini.bind(this),
      qwen: this.detectQwen.bind(this),
      copilot: this.detectCopilot.bind(this),
      cursor: this.detectCursor.bind(this)
    };
  }
  
  async detectClaude() {
    try {
      const version = execSync('claude --version', {
        encoding: 'utf8',
        stdio: ['pipe', 'pipe', 'ignore']
      }).trim();
      
      const installPath = this.getInstallPath('claude');
      
      return {
        installed: true,
        version: version,
        installPath: installPath,
        configPath: this.getClaudeConfigPath()
      };
    } catch (error) {
      return {
        installed: false,
        error: error.message
      };
    }
  }
  
  async detectGemini() {
    try {
      const version = execSync('gemini --version', {
        encoding: 'utf8',
        stdio: ['pipe', 'pipe', 'ignore']
      }).trim();
      
      return {
        installed: true,
        version: version,
        installPath: this.getInstallPath('gemini'),
        configPath: this.getGeminiConfigPath()
      };
    } catch (error) {
      return {
        installed: false,
        error: error.message
      };
    }
  }
  
  async detectQwen() {
    try {
      const version = execSync('qwen --version', {
        encoding: 'utf8',
        stdio: ['pipe', 'pipe', 'ignore']
      }).trim();
      
      return {
        installed: true,
        version: version,
        installPath: this.getInstallPath('qwen'),
        configPath: this.getQwenConfigPath()
      };
    } catch (error) {
      return {
        installed: false,
        error: error.message
      };
    }
  }
  
  async detectAll() {
    const results = {};
    
    for (const [name, detector] of Object.entries(this.detectors)) {
      try {
        results[name] = await detector();
      } catch (error) {
        results[name] = {
          installed: false,
          error: error.message
        };
      }
    }
    
    return results;
  }
  
  getInstallPath(cliName) {
    try {
      const whichResult = execSync(`which ${cliName}`, {
        encoding: 'utf8',
        stdio: ['pipe', 'pipe', 'ignore']
      }).trim();
      return whichResult;
    } catch {
      return null;
    }
  }
  
  getClaudeConfigPath() {
    const home = process.env.HOME || process.env.USERPROFILE;
    if (platform() === 'win32') {
      return `${home}\\.config\\claude\\skills\\`;
    } else {
      return `${home}/.config/claude/skills/`;
    }
  }
  
  getGeminiConfigPath() {
    const home = process.env.HOME || process.env.USERPROFILE;
    if (platform() === 'win32') {
      return `${home}\\.local\\share\\gemini\\extensions\\`;
    } else {
      return `${home}/.local/share/gemini/extensions/`;
    }
  }
  
  getQwenConfigPath() {
    const home = process.env.HOME || process.env.USERPROFILE;
    if (platform() === 'win32') {
      return `${home}\\.qwen\\plugins\\`;
    } else {
      return `${home}/.qwen/plugins/`;
    }
  }
}
```

**验收标准**:
- [ ] 能检测Claude CLI安装状态
- [ ] 能检测Gemini CLI安装状态
- [ ] 能检测Qwen CLI安装状态
- [ ] 能检测其他主流AI CLI工具
- [ ] 返回详细的安装信息和配置路径
- [ ] 优雅处理检测错误

#### 任务2: 实现配置生成器
**测试**: 配置生成功能测试
**实现**:
```javascript
// lib/config-generator.js
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

class ConfigGenerator {
  constructor() {
    this.defaultConfig = {
      version: "1.0.0",
      createdAt: new Date().toISOString(),
      platforms: [],
      skills: this.getDefaultSkills(),
      settings: {
        autoUpdate: true,
        verboseLogging: false,
        maxRetries: 3
      }
    };
  }
  
  generate(detectedTools) {
    const config = JSON.parse(JSON.stringify(this.defaultConfig));
    
    // 根据检测结果配置平台
    for (const [platformName, toolInfo] of Object.entries(detectedTools)) {
      if (toolInfo.installed) {
        config.platforms.push({
          name: platformName,
          enabled: true,
          version: toolInfo.version,
          installPath: toolInfo.installPath,
          configPath: toolInfo.configPath,
          skills: this.getPlatformSkills(platformName)
        });
      }
    }
    
    return config;
  }
  
  save(config, filePath) {
    try {
      const yamlContent = yaml.dump(config, {
        indent: 2,
        lineWidth: -1
      });
      
      // 确保目录存在
      const dir = path.dirname(filePath);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      
      fs.writeFileSync(filePath, yamlContent, 'utf8');
      return true;
    } catch (error) {
      console.error('Failed to save config:', error.message);
      return false;
    }
  }
  
  load(filePath) {
    try {
      if (!fs.existsSync(filePath)) {
        return null;
      }
      
      const yamlContent = fs.readFileSync(filePath, 'utf8');
      return yaml.load(yamlContent);
    } catch (error) {
      console.error('Failed to load config:', error.message);
      return null;
    }
  }
  
  validate(config) {
    if (!config) return false;
    
    const requiredFields = ['version', 'platforms', 'skills'];
    for (const field of requiredFields) {
      if (!config.hasOwnProperty(field)) {
        return false;
      }
    }
    
    if (!Array.isArray(config.platforms)) return false;
    
    return true;
  }
  
  getDefaultSkills() {
    return {
      architect: {
        command: "/speckit.dnaspec.architect",
        description: "系统架构设计专家",
        enabled: true
      },
      'agent-creator': {
        command: "/speckit.dnaspec.agent-creator",
        description: "智能体创建专家",
        enabled: true
      },
      'task-decomposer': {
        command: "/speckit.dnaspec.task-decomposer",
        description: "任务分解专家",
        enabled: true
      },
      'constraint-generator': {
        command: "/speckit.dnaspec.constraint-generator",
        description: "约束生成专家",
        enabled: true
      },
      'dapi-checker': {
        command: "/speckit.dnaspec.dapi-checker",
        description: "接口检查专家",
        enabled: true
      },
      'modulizer': {
        command: "/speckit.dnaspec.modulizer",
        description: "模块化专家",
        enabled: true
      }
    };
  }
  
  getPlatformSkills(platformName) {
    // 不同平台可能有不同的技能配置
    const platformSkills = {
      claude: {
        skillPath: "skills/",
        template: "claude-skill-template.json"
      },
      gemini: {
        skillPath: "extensions/",
        template: "gemini-extension-template.yaml"
      },
      qwen: {
        skillPath: "plugins/",
        template: "qwen-plugin-template.json"
      }
    };
    
    return platformSkills[platformName] || {};
  }
}
```

**验收标准**:
- [ ] 根据检测结果生成配置
- [ ] 包含所有默认技能配置
- [ ] 支持YAML格式保存和加载
- [ ] 验证配置结构完整性
- [ ] 支持不同平台的特定配置

#### 任务3: 实现集成验证器
**测试**: 集成验证功能测试
**实现**:
```javascript
// lib/integration-validator.js
const { SkillExecutor } = require('./skill-executor');

class IntegrationValidator {
  constructor(skillExecutor) {
    this.skillExecutor = skillExecutor;
  }
  
  async validatePlatformIntegration(platformName, config) {
    const platform = config.platforms.find(p => p.name === platformName);
    if (!platform || !platform.enabled) {
      return {
        valid: false,
        error: `Platform ${platformName} not enabled or not found`
      };
    }
    
    // 验证配置路径是否存在
    const configPathExists = this.validateConfigPath(platform.configPath);
    if (!configPathExists) {
      return {
        valid: false,
        error: `Config path does not exist: ${platform.configPath}`
      };
    }
    
    // 验证技能文件是否存在
    const skillsValid = await this.validateSkills(platform);
    if (!skillsValid.valid) {
      return skillsValid;
    }
    
    // 执行基本技能测试
    const skillTest = await this.testBasicSkill(platformName);
    
    return {
      valid: skillTest.success,
      platform: platformName,
      configPath: platform.configPath,
      skills: skillsValid.skills,
      testResult: skillTest,
      timestamp: new Date().toISOString()
    };
  }
  
  validateConfigPath(configPath) {
    try {
      const fs = require('fs');
      return fs.existsSync(configPath);
    } catch {
      return false;
    }
  }
  
  async validateSkills(platform) {
    try {
      // 检查技能文件是否存在
      const fs = require('fs');
      const path = require('path');
      
      const skills = Object.keys(platform.skills || {});
      const existingSkills = [];
      const missingSkills = [];
      
      for (const skill of skills) {
        const skillPath = path.join(platform.configPath, `${skill}.json`);
        if (fs.existsSync(skillPath)) {
          existingSkills.push(skill);
        } else {
          missingSkills.push(skill);
        }
      }
      
      return {
        valid: missingSkills.length === 0,
        skills: existingSkills,
        missing: missingSkills,
        total: skills.length
      };
    } catch (error) {
      return {
        valid: false,
        error: error.message
      };
    }
  }
  
  async testBasicSkill(platformName) {
    try {
      // 测试一个基本技能
      const result = await this.skillExecutor.execute('architect', 'test system');
      return {
        success: result.success,
        responseTime: result.responseTime || 0,
        result: result.result
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
  
  async runPerformanceTest(iterations = 5) {
    const results = [];
    const startTime = Date.now();
    
    for (let i = 0; i < iterations; i++) {
      const iterationStart = Date.now();
      try {
        const result = await this.skillExecutor.execute('architect', `test system ${i}`);
        const iterationTime = Date.now() - iterationStart;
        
        results.push({
          iteration: i,
          success: result.success,
          time: iterationTime,
          error: result.error
        });
      } catch (error) {
        const iterationTime = Date.now() - iterationStart;
        results.push({
          iteration: i,
          success: false,
          time: iterationTime,
          error: error.message
        });
      }
    }
    
    const totalTime = Date.now() - startTime;
    const successfulTests = results.filter(r => r.success).length;
    const successRate = successfulTests / iterations;
    const averageTime = totalTime / iterations;
    
    return {
      iterations: iterations,
      successful: successfulTests,
      successRate: successRate,
      averageResponseTime: averageTime,
      totalTime: totalTime,
      details: results
    };
  }
  
  async validateAllIntegrations(config) {
    const results = {};
    
    for (const platform of config.platforms) {
      if (platform.enabled) {
        results[platform.name] = await this.validatePlatformIntegration(
          platform.name, 
          config
        );
      }
    }
    
    return results;
  }
  
  generateReport(validationResults) {
    let report = '# DNASPEC Integration Validation Report\n\n';
    report += `Generated at: ${new Date().toISOString()}\n\n`;
    
    for (const [platformName, result] of Object.entries(validationResults)) {
      report += `## ${platformName.toUpperCase()} Integration\n`;
      
      if (result.valid) {
        report += `✅ Status: Valid\n`;
        report += `📁 Config Path: ${result.configPath}\n`;
        report += `📊 Skills: ${result.skills.length} skills configured\n`;
        if (result.testResult && result.testResult.success) {
          report += `⚡ Test: Passed (Response time: ${result.testResult.responseTime}ms)\n`;
        }
      } else {
        report += `❌ Status: Invalid\n`;
        report += `📝 Error: ${result.error}\n`;
      }
      
      report += '\n';
    }
    
    return report;
  }
  
  saveReport(report, filePath) {
    try {
      const fs = require('fs');
      fs.writeFileSync(filePath, report, 'utf8');
      return true;
    } catch (error) {
      console.error('Failed to save report:', error.message);
      return false;
    }
  }
}
```

**验收标准**:
- [ ] 验证各平台集成状态
- [ ] 检查配置路径有效性
- [ ] 验证技能文件存在性
- [ ] 执行基本技能测试
- [ ] 提供性能测试功能
- [ ] 生成详细的验证报告

### 4.2 第二周任务

#### 任务4: 实现自动配置器
**测试**: 自动配置功能测试
**实现**:
```javascript
// lib/auto-configurator.js
const { CliDetector } = require('./cli-detector');
const { ConfigGenerator } = require('./config-generator');
const { IntegrationValidator } = require('./integration-validator');

class AutoConfigurator {
  constructor(cliDetector, configGenerator, validator) {
    this.cliDetector = cliDetector;
    this.configGenerator = configGenerator;
    this.validator = validator;
  }
  
  async autoConfigure(options = {}) {
    console.log('🚀 Starting automatic configuration...');
    
    // 1. 检测已安装的CLI工具
    console.log('🔍 Detecting installed AI CLI tools...');
    const detectedTools = await this.cliDetector.detectAll();
    this.printDetectionResults(detectedTools);
    
    // 2. 生成配置文件
    console.log('⚙️  Generating configuration...');
    const config = this.configGenerator.generate(detectedTools);
    
    // 3. 保存配置文件
    const configPath = options.configPath || './.dnaspec/config.yaml';
    console.log(`💾 Saving configuration to ${configPath}...`);
    const saveResult = this.configGenerator.save(config, configPath);
    
    if (!saveResult) {
      throw new Error('Failed to save configuration');
    }
    
    console.log('✅ Configuration saved successfully!');
    
    // 4. 验证集成
    if (options.validate !== false) {
      console.log('🧪 Validating integrations...');
      const validationResults = await this.validator.validateAllIntegrations(config);
      
      // 生成验证报告
      const report = this.validator.generateReport(validationResults);
      const reportPath = options.reportPath || './dnaspec-validation-report.md';
      this.validator.saveReport(report, reportPath);
      
      this.printValidationResults(validationResults);
      
      return {
        success: true,
        config: config,
        configPath: configPath,
        validation: validationResults,
        reportPath: reportPath
      };
    }
    
    return {
      success: true,
      config: config,
      configPath: configPath
    };
  }
  
  printDetectionResults(detectedTools) {
    console.log('\nDetection Results:');
    for (const [name, info] of Object.entries(detectedTools)) {
      if (info.installed) {
        console.log(`  ✅ ${name}: ${info.version}`);
      } else {
        console.log(`  ❌ ${name}: Not installed`);
      }
    }
    console.log();
  }
  
  printValidationResults(validationResults) {
    console.log('\nValidation Results:');
    for (const [platform, result] of Object.entries(validationResults)) {
      if (result.valid) {
        console.log(`  ✅ ${platform}: Valid`);
      } else {
        console.log(`  ❌ ${platform}: ${result.error}`);
      }
    }
    console.log();
  }
  
  async interactiveConfigure() {
    const inquirer = require('inquirer');
    
    console.log('🧙 Welcome to DNASPEC Interactive Configuration Wizard\n');
    
    // 询问是否自动检测
    const { autoDetect } = await inquirer.prompt([
      {
        type: 'confirm',
        name: 'autoDetect',
        message: 'Automatically detect installed AI CLI tools?',
        default: true
      }
    ]);
    
    let detectedTools = {};
    if (autoDetect) {
      console.log('🔍 Detecting AI CLI tools...');
      detectedTools = await this.cliDetector.detectAll();
      this.printDetectionResults(detectedTools);
    } else {
      // 手动选择平台
      const platformChoices = [
        { name: 'Claude CLI', value: 'claude' },
        { name: 'Gemini CLI', value: 'gemini' },
        { name: 'Qwen CLI', value: 'qwen' },
        { name: 'GitHub Copilot CLI', value: 'copilot' },
        { name: 'Cursor CLI', value: 'cursor' }
      ];
      
      const { selectedPlatforms } = await inquirer.prompt([
        {
          type: 'checkbox',
          name: 'selectedPlatforms',
          message: 'Select platforms to configure:',
          choices: platformChoices
        }
      ]);
      
      // 手动检测选中的平台
      for (const platform of selectedPlatforms) {
        console.log(`🔍 Detecting ${platform}...`);
        detectedTools[platform] = await this.cliDetector.detectors[platform]();
      }
    }
    
    // 询问配置选项
    const { configPath, validate } = await inquirer.prompt([
      {
        type: 'input',
        name: 'configPath',
        message: 'Configuration file path:',
        default: './.dnaspec/config.yaml'
      },
      {
        type: 'confirm',
        name: 'validate',
        message: 'Run integration validation after configuration?',
        default: true
      }
    ]);
    
    // 执行配置
    return await this.autoConfigure({
      configPath: configPath,
      validate: validate
    });
  }
}
```

**验收标准**:
- [ ] 支持全自动配置模式
- [ ] 支持交互式配置向导
- [ ] 提供详细的配置过程反馈
- [ ] 生成配置文件和验证报告
- [ ] 处理配置过程中的错误

#### 任务5: 实现CLI集成命令
**测试**: CLI集成命令测试
**实现**:
```javascript
// bin/integrate.js
#!/usr/bin/env node

const { Command } = require('commander');
const { CliDetector } = require('../lib/cli-detector');
const { ConfigGenerator } = require('../lib/config-generator');
const { IntegrationValidator } = require('../lib/integration-validator');
const { AutoConfigurator } = require('../lib/auto-configurator');
const { SkillExecutor } = require('../lib/skill-executor');

const program = new Command();

program
  .name('dnaspec-spec-kit integrate')
  .description('Integrate DNASPEC skills with AI CLI tools')
  .version('1.0.0');

program
  .command('detect')
  .description('Detect installed AI CLI tools')
  .option('-v, --verbose', 'Show detailed information')
  .action(async (options) => {
    const detector = new CliDetector();
    const results = await detector.detectAll();
    
    console.log('Installed AI CLI Tools:');
    for (const [name, info] of Object.entries(results)) {
      if (info.installed) {
        console.log(`  ✅ ${name}: ${info.version}`);
        if (options.verbose) {
          console.log(`     Path: ${info.installPath}`);
          console.log(`     Config: ${info.configPath}`);
        }
      } else {
        console.log(`  ❌ ${name}: Not installed`);
        if (options.verbose && info.error) {
          console.log(`     Error: ${info.error}`);
        }
      }
    }
  });

program
  .command('configure')
  .description('Configure DNASPEC integration')
  .option('-a, --auto', 'Automatic configuration')
  .option('-i, --interactive', 'Interactive configuration wizard')
  .option('-c, --config <path>', 'Configuration file path')
  .option('--no-validate', 'Skip integration validation')
  .action(async (options) => {
    const detector = new CliDetector();
    const generator = new ConfigGenerator();
    const executor = new SkillExecutor(); // 需要实际实现
    const validator = new IntegrationValidator(executor);
    const configurator = new AutoConfigurator(detector, generator, validator);
    
    try {
      if (options.interactive) {
        await configurator.interactiveConfigure();
      } else if (options.auto) {
        await configurator.autoConfigure({
          configPath: options.config,
          validate: options.validate
        });
      } else {
        console.log('Please specify configuration mode:');
        console.log('  --auto for automatic configuration');
        console.log('  --interactive for interactive wizard');
      }
    } catch (error) {
      console.error('Configuration failed:', error.message);
      process.exit(1);
    }
  });

program
  .command('validate')
  .description('Validate DNASPEC integration')
  .option('-c, --config <path>', 'Configuration file path', './.dnaspec/config.yaml')
  .option('-p, --platform <name>', 'Validate specific platform')
  .option('-r, --report <path>', 'Validation report path')
  .option('--performance', 'Run performance tests')
  .action(async (options) => {
    const generator = new ConfigGenerator();
    const config = generator.load(options.config);
    
    if (!config) {
      console.error(`Configuration file not found: ${options.config}`);
      process.exit(1);
    }
    
    const executor = new SkillExecutor(); // 需要实际实现
    const validator = new IntegrationValidator(executor);
    
    try {
      if (options.performance) {
        console.log('🏃 Running performance tests...');
        const perfResults = await validator.runPerformanceTest();
        console.log(`Performance Results:`);
        console.log(`  Success Rate: ${(perfResults.successRate * 100).toFixed(1)}%`);
        console.log(`  Average Response Time: ${perfResults.averageResponseTime.toFixed(0)}ms`);
        console.log(`  Total Time: ${perfResults.totalTime}ms`);
      } else if (options.platform) {
        const result = await validator.validatePlatformIntegration(options.platform, config);
        if (result.valid) {
          console.log(`✅ ${options.platform} integration is valid`);
        } else {
          console.log(`❌ ${options.platform} integration is invalid: ${result.error}`);
        }
      } else {
        const results = await validator.validateAllIntegrations(config);
        const report = validator.generateReport(results);
        
        if (options.report) {
          validator.saveReport(report, options.report);
          console.log(`Report saved to: ${options.report}`);
        } else {
          console.log(report);
        }
      }
    } catch (error) {
      console.error('Validation failed:', error.message);
      process.exit(1);
    }
  });

program.parse();
```

**验收标准**:
- [ ] 支持detect命令检测CLI工具
- [ ] 支持configure命令配置集成
- [ ] 支持validate命令验证集成
- [ ] 提供详细的帮助信息
- [ ] 处理命令执行错误

#### 任务6: 实现跨平台兼容性
**测试**: 跨平台兼容性测试
**实现**:
```javascript
// lib/platform-utils.js
const os = require('os');
const path = require('path');

class PlatformUtils {
  static getPlatform() {
    return os.platform();
  }
  
  static isWindows() {
    return this.getPlatform() === 'win32';
  }
  
  static isMac() {
    return this.getPlatform() === 'darwin';
  }
  
  static isLinux() {
    return this.getPlatform() === 'linux';
  }
  
  static getUserHome() {
    return process.env.HOME || process.env.USERPROFILE;
  }
  
  static getStandardPaths() {
    const home = this.getUserHome();
    
    if (this.isWindows()) {
      return {
        config: path.join(home, '.dnaspec'),
        temp: process.env.TEMP || process.env.TMP || 'C:\\temp',
        data: path.join(home, 'AppData', 'Local', 'dnaspec')
      };
    } else {
      return {
        config: path.join(home, '.dnaspec'),
        temp: '/tmp',
        data: path.join(home, '.local', 'share', 'dnaspec')
      };
    }
  }
  
  static getConfigPath(platformName) {
    const home = this.getUserHome();
    const standardPaths = this.getStandardPaths();
    
    const platformPaths = {
      claude: this.isWindows() 
        ? path.join(home, '.config', 'claude', 'skills')
        : path.join(home, '.config', 'claude', 'skills'),
      gemini: this.isWindows()
        ? path.join(home, '.local', 'share', 'gemini', 'extensions')
        : path.join(home, '.local', 'share', 'gemini', 'extensions'),
      qwen: this.isWindows()
        ? path.join(home, '.qwen', 'plugins')
        : path.join(home, '.qwen', 'plugins')
    };
    
    return platformPaths[platformName] || standardPaths.config;
  }
  
  static async checkPermissions(filePath) {
    const fs = require('fs').promises;
    
    try {
      await fs.access(filePath, fs.constants.R_OK | fs.constants.W_OK);
      return { readable: true, writable: true };
    } catch {
      try {
        await fs.access(filePath, fs.constants.R_OK);
        return { readable: true, writable: false };
      } catch {
        return { readable: false, writable: false };
      }
    }
  }
  
  static async ensureDirectoryExists(dirPath) {
    const fs = require('fs').promises;
    
    try {
      await fs.mkdir(dirPath, { recursive: true });
      return true;
    } catch (error) {
      console.error(`Failed to create directory ${dirPath}:`, error.message);
      return false;
    }
  }
  
  static async copyFileWithBackup(source, destination) {
    const fs = require('fs').promises;
    
    // 创建备份
    if (await this.fileExists(destination)) {
      const backupPath = `${destination}.backup.${Date.now()}`;
      try {
        await fs.copyFile(destination, backupPath);
        console.log(`Backup created: ${backupPath}`);
      } catch (error) {
        console.warn(`Failed to create backup: ${error.message}`);
      }
    }
    
    // 复制文件
    try {
      await fs.copyFile(source, destination);
      return true;
    } catch (error) {
      console.error(`Failed to copy file: ${error.message}`);
      return false;
    }
  }
  
  static async fileExists(filePath) {
    const fs = require('fs').promises;
    
    try {
      await fs.access(filePath);
      return true;
    } catch {
      return false;
    }
  }
}

module.exports = { PlatformUtils };
```

**验收标准**:
- [ ] 支持Windows、macOS、Linux平台
- [ ] 正确处理不同平台的路径分隔符
- [ ] 正确处理权限检查
- [ ] 提供标准目录结构
- [ ] 支持文件备份和恢复

## 5. 质量保证措施

### 5.1 代码质量
- 使用ESLint进行代码检查
- 遵循JavaScript标准风格
- 100%测试覆盖率要求

### 5.2 跨平台测试
- Windows 10/11测试
- macOS测试
- Ubuntu/Linux测试
- 不同Node.js版本兼容性测试

### 5.3 性能要求
- CLI检测时间<5秒
- 配置生成时间<2秒
- 集成验证时间<10秒

## 6. 风险缓解

### 6.1 技术风险
- **权限问题**: 提供清晰的权限说明和错误处理
- **路径问题**: 使用跨平台路径处理库
- **依赖管理**: 明确依赖版本，提供安装脚本

### 6.2 兼容性风险
- **不同版本CLI工具**: 实现版本兼容性检测
- **配置文件格式**: 支持多种配置格式
- **错误处理**: 提供详细的错误信息和解决方案

## 7. 交付物清单

### 7.1 代码交付物
- lib/cli-detector.js CLI检测器
- lib/config-generator.js 配置生成器
- lib/integration-validator.js 集成验证器
- lib/auto-configurator.js 自动配置器
- lib/platform-utils.js 平台工具
- bin/integrate.js 集成CLI命令

### 7.2 测试交付物
- test/cli-detector.test.js CLI检测测试
- test/config-generator.test.js 配置生成测试
- test/integration-validator.test.js 集成验证测试
- test/auto-configurator.test.js 自动配置测试
- test/cross-platform.test.js 跨平台测试

### 7.3 文档交付物
- 集成指南 - 详细集成步骤
- 故障排除 - 常见集成问题解决
- 平台兼容性说明 - 各平台支持情况
- 性能优化指南 - 提升集成性能的建议