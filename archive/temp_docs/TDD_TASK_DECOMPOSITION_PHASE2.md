# TDD驱动的任务分解 - 第二阶段：命令系统增强

## 1. 任务概述
实现与spec.kit完全兼容的命令系统，支持斜杠命令解析和技能调用。

## 2. TDD测试驱动开发计划

### 2.1 命令解析器测试
```javascript
// test/command-parser.test.js
const { CommandParser } = require('../lib/command-parser');

describe('Command Parser', () => {
  let parser;
  
  beforeEach(() => {
    parser = new CommandParser();
  });
  
  test('should parse valid DNASPEC command', () => {
    const result = parser.parse('/speckit.dnaspec.architect 设计电商系统');
    expect(result).toEqual({
      command: '/speckit.dnaspec.architect',
      skill: 'architect',
      params: '设计电商系统',
      isValid: true
    });
  });
  
  test('should reject invalid command format', () => {
    const result = parser.parse('/invalid.command');
    expect(result.isValid).toBe(false);
  });
  
  test('should handle command without parameters', () => {
    const result = parser.parse('/speckit.dnaspec.agent-creator');
    expect(result.skill).toBe('agent-creator');
    expect(result.params).toBe('');
  });
});
```

### 2.2 技能调用测试
```javascript
// test/skill-executor.test.js
const { SkillExecutor } = require('../lib/skill-executor');

describe('Skill Executor', () => {
  let executor;
  
  beforeEach(() => {
    executor = new SkillExecutor();
  });
  
  test('should execute architect skill', async () => {
    const result = await executor.execute('architect', '设计系统架构');
    expect(result.success).toBe(true);
    expect(result.skill).toBe('architect');
    expect(result.result).toContain('系统架构');
  });
  
  test('should handle unknown skill', async () => {
    const result = await executor.execute('unknown', '测试参数');
    expect(result.success).toBe(false);
    expect(result.error).toContain('Skill not found');
  });
  
  test('should handle skill execution error', async () => {
    // 模拟技能执行错误
    const result = await executor.execute('failing-skill', '测试参数');
    expect(result.success).toBe(false);
  });
});
```

### 2.3 交互式Shell测试
```javascript
// test/interactive-shell.test.js
const { InteractiveShell } = require('../lib/interactive-shell');

describe('Interactive Shell', () => {
  let shell;
  
  beforeEach(() => {
    shell = new InteractiveShell();
  });
  
  test('should start REPL session', () => {
    expect(() => shell.start()).not.toThrow();
  });
  
  test('should handle exit command', () => {
    const exitSpy = jest.spyOn(process, 'exit').mockImplementation();
    shell.handleCommand('exit');
    expect(exitSpy).toHaveBeenCalledWith(0);
  });
  
  test('should show help information', () => {
    const consoleSpy = jest.spyOn(console, 'log');
    shell.handleCommand('help');
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Available commands'));
  });
});
```

## 3. SOLID原则任务分解

### 3.1 单一职责原则 (SRP)

#### 任务1: 命令解析器
- **职责**: 解析和验证斜杠命令
- **依赖**: 无外部依赖
- **接口**:
  ```javascript
  class CommandParser {
    parse(commandString) { }
    validate(commandObject) { }
    extractSkill(commandString) { }
  }
  ```

#### 任务2: 技能映射器
- **职责**: 将命令技能映射到实际技能实现
- **依赖**: 技能注册表
- **接口**:
  ```javascript
  class SkillMapper {
    map(skillName) { }
    register(skillName, implementation) { }
    getAvailableSkills() { }
  }
  ```

#### 任务3: 技能执行器
- **职责**: 执行具体的技能实现
- **依赖**: Python桥接器
- **接口**:
  ```javascript
  class SkillExecutor {
    execute(skillName, params) { }
    validateInput(skillName, params) { }
    formatOutput(result) { }
  }
  ```

### 3.2 开放封闭原则 (OCP)

#### 任务4: 可扩展的技能系统
- **设计**: 支持插件化添加新技能
- **接口**:
  ```javascript
  class ExtensibleSkillSystem {
    registerSkill(skillDefinition) { }
    unregisterSkill(skillName) { }
    getSkill(skillName) { }
  }
  ```

### 3.3 里氏替换原则 (LSP)

#### 任务5: 技能基类
- **设计**: 所有技能实现遵循统一接口
- **接口**:
  ```javascript
  class BaseSkill {
    execute(params) { }
    validate(params) { }
    getName() { }
  }
  ```

### 3.4 接口隔离原则 (ISP)

#### 任务6: 最小接口设计
- **设计**: 每个模块只暴露必要的接口
- **示例**:
  ```javascript
  // 只暴露命令处理相关接口
  module.exports = {
    parseCommand: (cmd) => {},
    executeSkill: (skill, params) => {},
    getAvailableSkills: () => {}
  };
  ```

### 3.5 依赖倒置原则 (DIP)

#### 任务7: 依赖注入
- **设计**: 通过构造函数注入依赖
- **示例**:
  ```javascript
  class CommandHandler {
    constructor(parser, executor, mapper) {
      this.parser = parser;
      this.executor = executor;
      this.mapper = mapper;
    }
  }
  ```

## 4. 具体实施任务清单

### 4.1 第一周任务

#### 任务1: 实现命令解析器
**测试**: 命令解析功能测试
**实现**:
```javascript
// lib/command-parser.js
class CommandParser {
  constructor() {
    this.pattern = /^\/speckit\.dnaspec\.([a-zA-Z0-9-]+)(?:\s+(.+))?$/;
  }
  
  parse(commandString) {
    if (!commandString || !commandString.startsWith('/speckit.dnaspec.')) {
      return { isValid: false, error: 'Invalid command prefix' };
    }
    
    const match = commandString.match(this.pattern);
    if (!match) {
      return { isValid: false, error: 'Invalid command format' };
    }
    
    return {
      command: commandString,
      skill: match[1],
      params: match[2] || '',
      isValid: true
    };
  }
  
  validate(commandObject) {
    return commandObject.isValid && 
           commandObject.skill && 
           commandObject.skill.length > 0;
  }
}
```

**验收标准**:
- [ ] 正确解析标准格式命令
- [ ] 拒绝无效命令格式
- [ ] 处理带参数和不带参数的命令
- [ ] 提供详细的错误信息

#### 任务2: 实现技能映射器
**测试**: 技能映射功能测试
**实现**:
```javascript
// lib/skill-mapper.js
class SkillMapper {
  constructor() {
    this.skillMap = {
      'architect': 'dnaspec-architect',
      'agent-creator': 'dnaspec-agent-creator',
      'task-decomposer': 'dnaspec-task-decomposer',
      'constraint-generator': 'dnaspec-constraint-generator',
      'dapi-checker': 'dnaspec-dapi-checker',
      'modulizer': 'dnaspec-modulizer'
    };
  }
  
  map(skillName) {
    return this.skillMap[skillName] || null;
  }
  
  register(customSkillName, dsgsSkillName) {
    this.skillMap[customSkillName] = dsgsSkillName;
  }
  
  getAvailableSkills() {
    return Object.keys(this.skillMap);
  }
}
```

**验收标准**:
- [ ] 正确映射所有内置技能
- [ ] 支持自定义技能映射
- [ ] 提供可用技能列表
- [ ] 处理未知技能映射

#### 任务3: 实现Python桥接器
**测试**: Python技能调用测试
**实现**:
```javascript
// lib/python-bridge.js
const { PythonShell } = require('python-shell');

class PythonBridge {
  constructor() {
    this.pythonPath = this.detectPythonPath();
    this.scriptPath = './python/skills/executor.py';
  }
  
  async executeSkill(skillName, params) {
    const options = {
      mode: 'json',
      pythonPath: this.pythonPath,
      scriptPath: this.scriptPath,
      args: [skillName, params]
    };
    
    return new Promise((resolve, reject) => {
      PythonShell.run('executor.py', options, (err, results) => {
        if (err) {
          reject(err);
        } else {
          resolve(results[0]);
        }
      });
    });
  }
  
  detectPythonPath() {
    // 检测Python路径
    return 'python';
  }
}
```

**验收标准**:
- [ ] 成功调用Python技能
- [ ] 正确传递参数
- [ ] 处理执行错误
- [ ] 返回格式化结果

### 4.2 第二周任务

#### 任务4: 实现技能执行器
**测试**: 技能执行功能测试
**实现**:
```javascript
// lib/skill-executor.js
class SkillExecutor {
  constructor(pythonBridge, skillMapper) {
    this.pythonBridge = pythonBridge;
    this.skillMapper = skillMapper;
  }
  
  async execute(skillName, params) {
    try {
      // 验证输入
      if (!this.validateInput(skillName, params)) {
        return {
          success: false,
          error: 'Invalid input parameters'
        };
      }
      
      // 映射技能名称
      const dsgsSkillName = this.skillMapper.map(skillName);
      if (!dsgsSkillName) {
        return {
          success: false,
          error: `Skill not found: ${skillName}`
        };
      }
      
      // 执行技能
      const result = await this.pythonBridge.executeSkill(dsgsSkillName, params);
      
      // 格式化输出
      return {
        success: true,
        skill: skillName,
        result: this.formatOutput(result),
        rawResult: result
      };
    } catch (error) {
      return {
        success: false,
        skill: skillName,
        error: error.message,
        stack: error.stack
      };
    }
  }
  
  validateInput(skillName, params) {
    return skillName && typeof skillName === 'string' && skillName.length > 0;
  }
  
  formatOutput(result) {
    if (typeof result === 'object' && result.result) {
      return result.result;
    }
    return result;
  }
}
```

**验收标准**:
- [ ] 成功执行所有内置技能
- [ ] 正确处理输入验证
- [ ] 提供详细的错误信息
- [ ] 格式化输出结果

#### 任务5: 实现命令处理器
**测试**: 命令处理功能测试
**实现**:
```javascript
// lib/command-handler.js
class CommandHandler {
  constructor(commandParser, skillExecutor) {
    this.commandParser = commandParser;
    this.skillExecutor = skillExecutor;
  }
  
  async handleCommand(commandString) {
    // 解析命令
    const parsedCommand = this.commandParser.parse(commandString);
    if (!parsedCommand.isValid) {
      return {
        success: false,
        error: parsedCommand.error
      };
    }
    
    // 执行技能
    return await this.skillExecutor.execute(
      parsedCommand.skill, 
      parsedCommand.params
    );
  }
  
  getAvailableCommands() {
    return [
      '/speckit.dnaspec.architect [参数] - 系统架构设计',
      '/speckit.dnaspec.agent-creator [参数] - 智能体创建',
      '/speckit.dnaspec.task-decomposer [参数] - 任务分解',
      '/speckit.dnaspec.constraint-generator [参数] - 约束生成',
      '/speckit.dnaspec.dapi-checker [参数] - 接口检查',
      '/speckit.dnaspec.modulizer [参数] - 模块化'
    ];
  }
}
```

**验收标准**:
- [ ] 正确处理所有命令格式
- [ ] 提供命令帮助信息
- [ ] 处理命令执行错误
- [ ] 返回结构化结果

#### 任务6: 实现交互式Shell
**测试**: 交互式Shell功能测试
**实现**:
```javascript
// lib/interactive-shell.js
const readline = require('readline');

class InteractiveShell {
  constructor(commandHandler) {
    this.commandHandler = commandHandler;
    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
  }
  
  start() {
    console.log('DNASPEC spec.kit Integration Shell');
    console.log('Type "help" for available commands, "exit" to quit\n');
    
    this.rl.setPrompt('DNASPEC> ');
    this.rl.prompt();
    
    this.rl.on('line', async (line) => {
      await this.handleLine(line.trim());
      this.rl.prompt();
    });
    
    this.rl.on('close', () => {
      console.log('\nGoodbye!');
      process.exit(0);
    });
  }
  
  async handleLine(line) {
    if (!line) return;
    
    switch (line.toLowerCase()) {
      case 'help':
        this.showHelp();
        break;
      case 'exit':
      case 'quit':
        this.rl.close();
        break;
      case 'list':
        this.listSkills();
        break;
      default:
        await this.executeCommand(line);
    }
  }
  
  async executeCommand(command) {
    try {
      const result = await this.commandHandler.handleCommand(command);
      if (result.success) {
        console.log('Result:', result.result);
      } else {
        console.log('Error:', result.error);
      }
    } catch (error) {
      console.log('Execution error:', error.message);
    }
  }
  
  showHelp() {
    console.log('Available commands:');
    const commands = this.commandHandler.getAvailableCommands();
    commands.forEach(cmd => console.log(`  ${cmd}`));
    console.log('\nSystem commands:');
    console.log('  help - Show this help');
    console.log('  list - List available skills');
    console.log('  exit - Exit the shell');
  }
  
  listSkills() {
    console.log('Available DNASPEC Skills:');
    const commands = this.commandHandler.getAvailableCommands();
    commands.forEach(cmd => console.log(`  ${cmd}`));
  }
}
```

**验收标准**:
- [ ] 提供交互式命令行界面
- [ ] 支持命令历史和自动补全
- [ ] 处理用户输入错误
- [ ] 提供友好的用户体验

#### 任务7: 实现CLI命令集成
**测试**: CLI命令集成测试
**实现**:
```javascript
// bin/cli.js
#!/usr/bin/env node

const { Command } = require('commander');
const { CommandHandler } = require('../lib/command-handler');
const { InteractiveShell } = require('../lib/interactive-shell');

const program = new Command();

program
  .name('dnaspec-spec-kit')
  .description('DNASPEC Skills for spec.kit integration')
  .version('1.0.0');

program
  .command('exec')
  .description('Execute a DNASPEC skill command')
  .argument('<command>', 'The command to execute')
  .action(async (command) => {
    const handler = createCommandHandler();
    const result = await handler.handleCommand(command);
    if (result.success) {
      console.log(JSON.stringify(result.result, null, 2));
    } else {
      console.error('Error:', result.error);
      process.exit(1);
    }
  });

program
  .command('shell')
  .description('Start interactive shell')
  .action(() => {
    const handler = createCommandHandler();
    const shell = new InteractiveShell(handler);
    shell.start();
  });

program
  .command('list')
  .description('List available skills')
  .action(() => {
    const handler = createCommandHandler();
    const commands = handler.getAvailableCommands();
    console.log('Available DNASPEC Skills:');
    commands.forEach(cmd => console.log(`  ${cmd}`));
  });

function createCommandHandler() {
  // 创建并配置命令处理器
  // 这里应该使用依赖注入
  return new CommandHandler();
}

program.parse();
```

**验收标准**:
- [ ] 支持exec命令执行技能
- [ ] 支持shell命令启动交互式界面
- [ ] 支持list命令列出可用技能
- [ ] 提供清晰的帮助信息

## 5. 质量保证措施

### 5.1 代码质量
- 使用ESLint进行代码检查
- 遵循JavaScript标准风格
- 100%测试覆盖率要求

### 5.2 性能要求
- 命令解析时间<100ms
- 技能执行时间<2秒
- 内存使用<50MB

### 5.3 兼容性要求
- 完全兼容spec.kit命令格式
- 支持所有6个核心技能
- 提供向后兼容性

## 6. 风险缓解

### 6.1 技术风险
- **Python依赖**: 提供详细的安装指南和错误处理
- **跨平台兼容性**: 使用跨平台库，充分测试
- **性能问题**: 实现异步处理和缓存机制

### 6.2 集成风险
- **spec.kit兼容性**: 严格按照spec.kit规范实现
- **AI CLI集成**: 提供多种集成方式和配置选项
- **错误处理**: 提供详细的错误信息和解决方案

## 7. 交付物清单

### 7.1 代码交付物
- lib/command-parser.js 命令解析器
- lib/skill-mapper.js 技能映射器
- lib/skill-executor.js 技能执行器
- lib/python-bridge.js Python桥接器
- lib/command-handler.js 命令处理器
- lib/interactive-shell.js 交互式Shell
- bin/cli.js CLI入口点

### 7.2 测试交付物
- test/command-parser.test.js 命令解析测试
- test/skill-executor.test.js 技能执行测试
- test/interactive-shell.test.js 交互式Shell测试
- test/integration.test.js 集成测试

### 7.3 文档交付物
- API文档 - 命令接口说明
- 使用指南 - 命令使用示例
- 故障排除 - 常见问题解决
- 兼容性说明 - spec.kit兼容性列表