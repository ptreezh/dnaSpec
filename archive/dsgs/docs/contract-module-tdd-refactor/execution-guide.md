# Contract Module TDD重构 - 执行指南

## 🚀 快速开始

本文档提供Contract Module TDD重构的详细执行指南，遵循kiro spec规范和TDD原则。

## 📋 执行前准备

### 1. 环境检查
```bash
# 检查Node.js版本
node --version  # 需要 >= 16.0.0

# 检查TypeScript版本
npx tsc --version  # 需要 >= 4.9.0

# 检查项目依赖
npm list --depth=0
```

### 2. 创建工作分支
```bash
# 创建功能分支
git checkout -b feature/contract-module-tdd-refactor

# 推送到远程
git push -u origin feature/contract-module-tdd-refactor
```

### 3. 安装开发依赖
```bash
# 安装测试相关依赖
npm install --save-dev jest @types/jest ts-jest

# 安装代码质量工具
npm install --save-dev eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin

# 安装其他工具
npm install --save-dev husky lint-staged
```

## 🎯 TDD执行流程

### Red-Green-Refactor循环

#### 1. Red阶段 - 编写失败的测试
```bash
# 创建测试文件
touch test/unit/ContractGenerator.test.ts

# 编写失败的测试用例
```

**示例**：
```typescript
describe('ContractGenerator', () => {
  it('should generate contract from TypeScript source', async () => {
    // Arrange - 准备测试数据
    const generator = new ContractGenerator();
    const request: GenerateContractRequest = {
      sourcePaths: ['./test/fixtures/sample.ts'],
      format: 'openapi',
      options: { includePrivate: false, includeExamples: true, validate: true, version: '1.0.0' }
    };
    
    // Act - 执行测试
    const result = await generator.generate(request);
    
    // Assert - 验证结果
    expect(result.success).toBe(true);
    expect(result.contract).toBeDefined();
    expect(result.contract.endpoints).toHaveLength(1);
  });
});
```

#### 2. Green阶段 - 让测试通过
```bash
# 运行测试（应该失败）
npm test -- test/unit/ContractGenerator.test.ts

# 实现最小功能让测试通过
```

#### 3. Refactor阶段 - 重构代码
```bash
# 确保测试仍然通过
npm test

# 重构代码，保持测试通过
```

## 📝 任务执行指南

### TASK-001: 修复ContractGenerator.ts编译错误

#### 步骤1: 分析编译错误
```bash
# 运行编译检查
npm run build

# 查看详细错误信息
npx tsc --noEmit
```

#### 步骤2: 创建测试验证编译错误
```typescript
// test/unit/ContractGeneratorCompilation.test.ts
describe('ContractGenerator Compilation', () => {
  it('should compile without errors', () => {
    // 这个测试会验证模块是否能正确编译
    expect(() => {
      require('../../src/modules/contract/ContractGenerator');
    }).not.toThrow();
  });
});
```

#### 步骤3: 修复编译错误
```typescript
// 修复类型定义不匹配
export interface GenerateContractRequest {
  sourcePaths: string[];
  outputPath?: string;
  format: 'openapi' | 'json-schema' | 'markdown';
  options: GenerationOptions;
}

// 修复导入路径
import { TypeAnalyzer } from '../utils/TypeAnalyzer';
```

#### 步骤4: 验证修复结果
```bash
# 运行编译测试
npm test -- test/unit/ContractGeneratorCompilation.test.ts

# 运行完整编译
npm run build
```

### TASK-004: 建立基础测试框架

#### 步骤1: 配置Jest
```json
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src', '<rootDir>/test'],
  testMatch: ['**/__tests__/**/*.ts', '**/?(*.)+(spec|test).ts'],
  transform: {
    '^.+\\.ts$': 'ts-jest',
  },
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/**/*.test.ts',
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 90,
      statements: 90,
    },
  },
};
```

#### 步骤2: 创建测试工具类
```typescript
// test/utils/TestHelpers.ts
export class TestHelpers {
  static createMockTypeScriptFile(content: string): string {
    const fileName = `temp_${Date.now()}.ts`;
    fs.writeFileSync(fileName, content);
    return fileName;
  }
  
  static cleanupTestFiles(files: string[]): void {
    files.forEach(file => {
      if (fs.existsSync(file)) {
        fs.unlinkSync(file);
      }
    });
  }
}
```

#### 步骤3: 创建测试数据
```typescript
// test/fixtures/TypeScriptSamples.ts
export interface SampleInterface {
  id: string;
  name: string;
  value: number;
}

export class SampleClass {
  constructor(private data: SampleInterface) {}
  
  getData(): SampleInterface {
    return this.data;
  }
}
```

#### 步骤4: 编写基础测试
```typescript
// test/unit/ContractGenerator.test.ts
describe('ContractGenerator', () => {
  let generator: ContractGenerator;
  let testFiles: string[];
  
  beforeEach(() => {
    generator = new ContractGenerator();
    testFiles = [];
  });
  
  afterEach(() => {
    TestHelpers.cleanupTestFiles(testFiles);
  });
  
  it('should generate contract from simple interface', async () => {
    // Arrange
    const sampleCode = `
      export interface User {
        id: string;
        name: string;
        email: string;
      }
    `;
    const testFile = TestHelpers.createMockTypeScriptFile(sampleCode);
    testFiles.push(testFile);
    
    const request: GenerateContractRequest = {
      sourcePaths: [testFile],
      format: 'openapi',
      options: {
        includePrivate: false,
        includeExamples: true,
        validate: true,
        version: '1.0.0'
      }
    };
    
    // Act
    const result = await generator.generate(request);
    
    // Assert
    expect(result.success).toBe(true);
    expect(result.contract).toBeDefined();
    expect(result.contract.dataModels).toHaveLength(1);
    expect(result.contract.dataModels[0].name).toBe('User');
  });
});
```

## 🔧 代码重构指南

### 重构原则
1. **单一职责**：每个类只负责一个功能
2. **开闭原则**：对扩展开放，对修改关闭
3. **依赖倒置**：依赖抽象，不依赖具体实现
4. **接口隔离**：使用小而专的接口

### 重构步骤

#### 1. 提取类
```typescript
// 重构前
class ContractGenerator {
  async generate(request: GenerateContractRequest): Promise<GenerateContractResponse> {
    // 所有逻辑都在一个类中
  }
}

// 重构后
class ContractGenerator {
  constructor(
    private analyzer: SourceCodeAnalyzer,
    private validator: ContractValidator,
    private formatter: OutputFormatter
  ) {}
  
  async generate(request: GenerateContractRequest): Promise<GenerateContractResponse> {
    const analysis = await this.analyzer.analyze(request.sourcePaths);
    const contract = this.formatter.format(analysis, request.format);
    const validation = await this.validator.validate(contract);
    
    return {
      success: validation.isValid,
      contract,
      warnings: validation.warnings,
      metadata: {
        generatedAt: new Date().toISOString(),
        sourceFiles: request.sourcePaths,
        generationTime: Date.now()
      }
    };
  }
}
```

#### 2. 提取接口
```typescript
// 重构前
class SourceCodeAnalyzer {
  async analyze(paths: string[]): Promise<AnalysisResult> {
    // 具体实现
  }
}

// 重构后
interface ISourceCodeAnalyzer {
  analyze(paths: string[]): Promise<AnalysisResult>;
}

class TypeScriptAnalyzer implements ISourceCodeAnalyzer {
  async analyze(paths: string[]): Promise<AnalysisResult> {
    // TypeScript具体实现
  }
}

class MockAnalyzer implements ISourceCodeAnalyzer {
  async analyze(paths: string[]): Promise<AnalysisResult> {
    // 测试用模拟实现
  }
}
```

#### 3. 依赖注入
```typescript
// 重构前
const generator = new ContractGenerator();

// 重构后
const analyzer = new TypeScriptAnalyzer();
const validator = new ContractValidator();
const formatter = new OpenApiFormatter();
const generator = new ContractGenerator(analyzer, validator, formatter);
```

## 📊 测试策略

### 单元测试
```typescript
describe('TypeScriptAnalyzer', () => {
  it('should extract interface definitions', async () => {
    // Arrange
    const analyzer = new TypeScriptAnalyzer();
    const testFile = TestHelpers.createMockTypeScriptFile(`
      export interface TestInterface {
        property: string;
      }
    `);
    
    // Act
    const result = await analyzer.analyze([testFile]);
    
    // Assert
    expect(result.interfaces).toHaveLength(1);
    expect(result.interfaces[0].name).toBe('TestInterface');
  });
});
```

### 集成测试
```typescript
describe('ContractGenerator Integration', () => {
  it('should generate and validate contract', async () => {
    // Arrange
    const generator = new ContractGenerator();
    const testFile = TestHelpers.createMockTypeScriptFile(`
      export interface User {
        id: string;
        name: string;
      }
    `);
    
    // Act
    const result = await generator.generate({
      sourcePaths: [testFile],
      format: 'openapi',
      options: { includePrivate: false, includeExamples: true, validate: true, version: '1.0.0' }
    });
    
    // Assert
    expect(result.success).toBe(true);
    expect(result.contract).toBeDefined();
    expect(result.contract.dataModels).toHaveLength(1);
  });
});
```

### 端到端测试
```typescript
describe('CLI E2E', () => {
  it('should generate contract via CLI command', async () => {
    // Arrange
    const testFile = TestHelpers.createMockTypeScriptFile(`
      export interface Product {
        id: string;
        name: string;
        price: number;
      }
    `);
    
    // Act
    const result = await execAsync(`npm run contract:generate -- ${testFile}`);
    
    // Assert
    expect(result.stdout).toContain('Contract generated successfully');
    expect(fs.existsSync('./output/contract.json')).toBe(true);
  });
});
```

## 🚨 错误处理

### 编译错误处理
```typescript
// 检查编译状态
async function checkCompilation(): Promise<boolean> {
  try {
    await execAsync('npm run build');
    return true;
  } catch (error) {
    console.error('Compilation failed:', error);
    return false;
  }
}
```

### 测试失败处理
```typescript
// 运行测试并处理失败
async function runTests(): Promise<boolean> {
  try {
    await execAsync('npm test');
    return true;
  } catch (error) {
    console.error('Tests failed:', error);
    // 生成测试报告
    await execAsync('npm run test:coverage');
    return false;
  }
}
```

## 📈 进度跟踪

### 每日检查清单
```bash
# 检查编译状态
npm run build

# 检查测试状态
npm test

# 检查测试覆盖率
npm run test:coverage

# 检查代码质量
npm run lint

# 提交进度
git add .
git commit -m "feat: complete TASK-001 - fix ContractGenerator compilation"
```

### 进度报告模板
```markdown
## 日常进度报告 - YYYY-MM-DD

### 完成的任务
- [x] TASK-001.1 - 分析编译错误
- [x] TASK-001.2 - 修复类型定义不匹配

### 进行中的任务
- [ ] TASK-001.3 - 修复导入路径错误
- [ ] TASK-001.4 - 验证修复结果

### 遇到的问题
- 问题1：类型定义不匹配
- 解决方案：统一接口定义

### 明日计划
- 完成TASK-001剩余任务
- 开始TASK-002
```

## 🎯 验收检查

### 编译验收
```bash
# 检查编译
npm run build

# 检查类型
npx tsc --noEmit
```

### 测试验收
```bash
# 运行所有测试
npm test

# 检查覆盖率
npm run test:coverage

# 运行特定测试
npm test -- --testNamePattern="ContractGenerator"
```

### 功能验收
```bash
# 测试CLI功能
npm run contract:generate

# 测试契约验证
npm run contract:validate
```

---

**执行指南版本**：1.0  
**创建日期**：2025-08-11  
**最后更新**：2025-08-11  
**作者**：DNASPEC团队  
**状态**：待执行