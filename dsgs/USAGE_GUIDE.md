# DSGS 使用说明文档

## 📋 项目概览

**DSGS** (Dynamic Specification Growth System) 是一个智能的动态规范增长系统，能够根据任务上下文自动生成和管理约束规则。系统采用先进的上下文工程技术，结合神经场理论和认知工具编排，为软件开发提供智能化的约束管理解决方案。

## 🎯 用户界面和交互方式

DSGS 提供多种使用方式，满足不同用户的需求：

### 1. 📝 编程接口 (API)
**主要交互方式**，适合开发者集成到现有系统中

### 2. 💻 命令行工具 (CLI)
**简单直接**，适合快速测试和脚本化使用

### 3. 🔧 VS Code 插件
**开发环境集成**，提供实时的开发建议

### 4. 🤖 MCP 工具
**AI 助手集成**，与各种 AI 编程助手配合使用

---

## 🚀 快速开始

### 环境要求
- Node.js >= 18.0.0
- npm 或 yarn
- TypeScript (开发环境)

### 安装步骤

#### 1. 克隆项目
```bash
git clone <repository-url>
cd dsgs
```

#### 2. 安装依赖
```bash
npm install
```

#### 3. 构建项目
```bash
npm run build
```

#### 4. 验证安装
```bash
npm test
```

---

## 📖 详细使用指南

### 方式一：编程接口 (API)

#### 基础使用
```typescript
import { 
  ContextEngineeringIntegration, 
  createTCC 
} from './src/index';

// 1. 创建集成实例
const integration = new ContextEngineeringIntegration({
  cognitive: {
    enableVerboseLogging: true,
    confidenceThreshold: 0.6
  }
});

// 2. 创建任务上下文
const taskContext = createTCC(
  'task-001',
  'Implement secure authentication system',
  'SECURITY'
);

// 3. 生成约束
const result = await integration.generateConstraints(taskContext, {
  includeReasoning: true,
  maxConstraints: 10
});

console.log('Generated constraints:', result.constraints);
console.log('Confidence:', result.confidence);
console.log('Reasoning:', result.reasoning);
```

#### 高级配置
```typescript
import { 
  ContextEngineeringIntegration,
  createNeuralField,
  createCognitiveToolOrchestrator,
  createProtocolEngine
} from './src/core/utils/factory';

// 1. 创建神经场
const neuralField = createNeuralField({
  learningRate: 0.1,
  resonanceThreshold: 0.8,
  fieldDimension: 256
});

// 2. 创建认知工具编排器
const cognitiveTools = createCognitiveToolOrchestrator(neuralField, {
  enableVerboseLogging: true,
  maxExecutionTime: 30000
});

// 3. 创建协议引擎
const protocolEngine = createProtocolEngine(cognitiveTools, neuralField);

// 4. 创建高级集成实例
const advancedIntegration = new ContextEngineeringIntegration({
  cognitive: {
    enableVerboseLogging: true,
    confidenceThreshold: 0.7,
    maxExecutionTime: 45000
  },
  neuralField,
  cognitiveTools,
  protocolEngine
});
```

#### 模块化使用
```typescript
// 只使用需要的模块
import { TemplateEvolver } from './src/core/constraint/TemplateEvolver';
import { ConstraintNeuralField } from './src/core/neural-field/ConstraintNeuralField';
import { CognitiveToolOrchestrator } from './src/core/cognitive-tools/CognitiveToolOrchestrator';

// 模板进化器
const evolver = new TemplateEvolver();

// 神经场
const neuralField = new ConstraintNeuralField();

// 认知工具编排器
const orchestrator = new CognitiveToolOrchestrator(neuralField);
```

### 方式二：命令行工具 (CLI)

#### 基础命令
```bash
# 查看帮助
node src/modules/contract/cli-simple.js --help

# 生成契约
node src/modules/contract/cli-simple.js generate \
  --source ./src \
  --output ./dist/contract.yaml \
  --format openapi

# 验证契约
node src/modules/contract/cli-simple.js validate \
  --contract ./dist/contract.yaml

# 发布契约
node src/modules/contract/cli-simple.js publish \
  --contract ./dist/contract.yaml
```

#### 运行测试
```bash
# 运行所有测试
npm test

# 运行单位测试
npm run test:unit

# 运行属性测试
npm run test:property

# 运行集成测试
npm run test:integration

# 运行性能测试
npm run test:performance
```

#### 开发模式
```bash
# 启动开发服务器
npm run dev

# 构建项目
npm run build

# 查看项目状态
npm run view:state
```

### 方式三：VS Code 插件

#### 安装插件
```bash
# 在 VS Code 中安装
# 1. 打开 Extensions 面板 (Ctrl+Shift+X)
# 2. 搜索 "DSGS"
# 3. 点击 "Install"
```

#### 使用插件功能
```typescript
// 插件会自动提供以下功能：
// 1. 实时代码约束检查
// 2. 智能代码建议
// 3. 约束违规提示
// 4. 重构建议
// 5. 代码质量评估
```

#### 配置插件
```json
// .vscode/settings.json
{
  "dsgs.enable": true,
  "dsgs.severity": "warning",
  "dsgs.maxConstraints": 10,
  "dsgs.confidenceThreshold": 0.6,
  "dsgs.enableVerboseLogging": false
}
```

### 方式四：MCP 工具

#### 配置 MCP 服务器
```json
// mcp-settings.json
{
  "mcpServers": {
    "dsgs": {
      "command": "node",
      "args": ["./src/mcp/server.js"],
      "env": {
        "NODE_ENV": "production"
      }
    }
  }
}
```

#### 在 AI 助手中使用
```javascript
// 在 Cline 或其他 AI 助手中使用
// 1. 配置 MCP 服务器
// 2. AI 助手会自动调用 DSGS 功能
// 3. 获得智能的代码约束和建议
```

---

## 🎨 实际应用示例

### 示例 1：代码审查助手
```typescript
import { ContextEngineeringIntegration, createTCC } from './src/index';

async function codeReviewAssistant(sourceCode: string, filePath: string) {
  const integration = new ContextEngineeringIntegration();
  
  const taskContext = createTCC(
    `review-${filePath}`,
    `Review code for quality and best practices`,
    'CODE_REVIEW'
  );
  
  // 添加代码上下文
  taskContext.context.codebaseContext = {
    dependencies: ['express', 'typescript', 'jest'],
    architecture: 'layered',
    technologyStack: ['Node.js', 'TypeScript', 'Express']
  };
  
  const result = await integration.generateConstraints(taskContext, {
    includeReasoning: true,
    maxConstraints: 15
  });
  
  return {
    constraints: result.constraints,
    suggestions: result.reasoning,
    confidence: result.confidence
  };
}

// 使用示例
const reviewResult = await codeReviewAssistant(
  `function authenticateUser(username, password) {
    // 实现代码
  }`,
  'auth.service.ts'
);
```

### 示例 2：架构规范管理
```typescript
import { ContextEngineeringIntegration, createTCC } from './src/index';

async function architectureStandardsManager(projectConfig) {
  const integration = new ContextEngineeringIntegration({
    cognitive: {
      enableVerboseLogging: true,
      confidenceThreshold: 0.8
    }
  });
  
  const taskContext = createTCC(
    'architecture-standards',
    `Generate architecture standards for ${projectConfig.type}`,
    'ARCHITECTURE'
  );
  
  // 添加项目上下文
  taskContext.context.codebaseContext = {
    dependencies: projectConfig.dependencies,
    architecture: projectConfig.architecture,
    technologyStack: projectConfig.technologyStack
  };
  
  taskContext.context.phaseContext = {
    phase: 'DEVELOPMENT',
    teamSize: projectConfig.teamSize,
    complexity: projectConfig.complexity
  };
  
  const result = await integration.generateConstraints(taskContext, {
    includeReasoning: true,
    maxConstraints: 20
  });
  
  return {
    standards: result.constraints,
    guidelines: result.reasoning,
    confidence: result.confidence
  };
}
```

### 示例 3：测试用例生成
```typescript
import { ContextEngineeringIntegration, createTCC } from './src/index';

async function testCaseGenerator(functionCode, functionSignature) {
  const integration = new ContextEngineeringIntegration();
  
  const taskContext = createTCC(
    `test-${functionSignature.name}`,
    `Generate test cases for ${functionSignature.name}`,
    'TESTING'
  );
  
  // 添加函数上下文
  taskContext.context.codebaseContext = {
    dependencies: ['jest', 'typescript'],
    architecture: 'unit-testing',
    technologyStack: ['Jest', 'TypeScript']
  };
  
  const result = await integration.generateConstraints(taskContext, {
    includeReasoning: true,
    maxConstraints: 12
  });
  
  // 将约束转换为测试用例
  const testCases = result.constraints.map(constraint => {
    return {
      description: constraint.name,
      test: generateTestFromConstraint(constraint),
      priority: constraint.severity
    };
  });
  
  return {
    testCases,
    coverage: result.confidence,
    suggestions: result.reasoning
  };
}
```

---

## 🔧 配置选项

### 基础配置
```typescript
interface ContextEngineeringConfig {
  cognitive: {
    enableVerboseLogging: boolean;
    confidenceThreshold: number;
    maxExecutionTime?: number;
  };
  protocol: {
    enableVerboseLogging: boolean;
    maxSteps?: number;
  };
}
```

### 高级配置
```typescript
interface AdvancedConfig extends ContextEngineeringConfig {
  neuralField?: {
    dimension: number;
    learningRate: number;
    resonanceThreshold: number;
  };
  cognitiveTools?: {
    enableTool: string[];
    maxExecutionTime: number;
  };
  constraintGeneration?: {
    maxConstraints: number;
    minRelevanceThreshold: number;
    enableReasoning: boolean;
  };
}
```

### 环境配置
```typescript
// 开发环境
const devConfig = {
  cognitive: {
    enableVerboseLogging: true,
    confidenceThreshold: 0.5
  },
  protocol: {
    enableVerboseLogging: true
  }
};

// 生产环境
const prodConfig = {
  cognitive: {
    enableVerboseLogging: false,
    confidenceThreshold: 0.8,
    maxExecutionTime: 30000
  },
  protocol: {
    enableVerboseLogging: false,
    maxSteps: 50
  }
};
```

---

## 🐛 故障排除

### 常见问题

#### 1. 依赖安装失败
```bash
# 解决方案
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

#### 2. TypeScript 编译错误
```bash
# 解决方案
npm run build
# 检查 TypeScript 版本兼容性
```

#### 3. 测试失败
```bash
# 解决方案
npm test
# 查看详细错误信息
npm test -- --verbose
```

#### 4. 内存不足
```bash
# 解决方案
# 增加 Node.js 内存限制
node --max-old-space-size=4096 index.js
```

### 调试模式
```typescript
// 启用详细日志
const integration = new ContextEngineeringIntegration({
  cognitive: {
    enableVerboseLogging: true
  },
  protocol: {
    enableVerboseLogging: true
  }
});

// 添加错误处理
try {
  const result = await integration.generateConstraints(taskContext);
} catch (error) {
  console.error('Constraint generation failed:', error);
  // 实现错误恢复逻辑
}
```

---

## 📚 API 参考

### 核心类

#### ContextEngineeringIntegration
```typescript
class ContextEngineeringIntegration {
  constructor(config?: Partial<ContextEngineeringConfig>);
  
  async generateConstraints(
    taskContext: TaskContextCapsule,
    options?: {
      includeReasoning?: boolean;
      maxConstraints?: number;
    }
  ): Promise<ConstraintGenerationResult>;
  
  getSystemState(): SystemState;
  getNeuralField(): ConstraintNeuralField;
  getCognitiveTools(): CognitiveToolOrchestrator;
}
```

#### TaskContextCapsule
```typescript
interface TaskContextCapsule {
  taskId: string;
  goal: string;
  taskType: string;
  context: {
    relevantConstraints: string[];
    systemState: SystemState;
    creationTime: string;
    source: string;
    priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
    codebaseContext?: CodebaseContext;
    phaseContext?: PhaseContext;
  };
}
```

#### ConstraintGenerationResult
```typescript
interface ConstraintGenerationResult {
  constraints: any[];
  confidence: number;
  reasoning: string[];
  executionTime: number;
}
```

### 工厂函数
```typescript
// 创建默认实例
function createDefaultContextEngineeringIntegration(): ContextEngineeringIntegration;

// 创建自定义实例
function createCustomContextEngineeringIntegration(config: any): ContextEngineeringIntegration;

// 创建神经场
function createNeuralField(dynamics?: any): ConstraintNeuralField;

// 创建认知工具编排器
function createCognitiveToolOrchestrator(neuralField: ConstraintNeuralField, config?: any): CognitiveToolOrchestrator;
```

---

## 🚀 最佳实践

### 1. 性能优化
```typescript
// 重用实例
const integration = new ContextEngineeringIntegration(config);

// 批量处理
const tasks = [task1, task2, task3];
const results = await Promise.all(
  tasks.map(task => integration.generateConstraints(task))
);
```

### 2. 错误处理
```typescript
// 实现重试机制
async function generateWithRetry(integration, taskContext, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await integration.generateConstraints(taskContext);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
}
```

### 3. 配置管理
```typescript
// 环境特定的配置
const configs = {
  development: { /* ... */ },
  staging: { /* ... */ },
  production: { /* ... */ }
};

const config = configs[process.env.NODE_ENV || 'development'];
const integration = new ContextEngineeringIntegration(config);
```

### 4. 监控和日志
```typescript
// 添加性能监控
const startTime = Date.now();
const result = await integration.generateConstraints(taskContext);
const endTime = Date.now();

console.log(`Constraint generation took ${endTime - startTime}ms`);
console.log(`Generated ${result.constraints.length} constraints`);
```

---

## 📞 支持和社区

### 获取帮助
- 📧 邮件: support@dsgs.com
- 💬 Discord: [DSGS Community](https://discord.gg/dsgs)
- 🐛 问题报告: [GitHub Issues](https://github.com/dsgs/issues)
- 📖 文档: [DSGS Documentation](https://docs.dsgs.com)

### 贡献指南
1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 创建 Pull Request
5. 等待审查

### 版本信息
- 当前版本: 2.0.0
- Node.js 要求: >= 18.0.0
- 许可证: MIT

---

## 🎉 总结

DSGS 提供了多种使用方式，从简单的 API 调用到复杂的 AI 助手集成。无论您是开发者、架构师还是 QA 工程师，都能找到适合的使用方式。

**推荐的使用路径**:
1. **新手**: 从 CLI 工具开始，了解基本功能
2. **开发者**: 使用 API 集成到现有项目中
3. **团队**: 配置 VS Code 插件，实现团队标准化
4. **AI 用户**: 通过 MCP 工具与 AI 助手配合使用

通过合理配置和使用，DSGS 可以显著提高代码质量、减少技术债务、提升开发效率。

---
**文档版本**: 2.0.0  
**最后更新**: 2025-08-10  
**维护者**: DSGS Architecture Team