# DNASPEC 项目接口文档

## 📋 目录
1. [核心模块接口](#核心模块接口)
2. [类型定义字典](#类型定义字典)
3. [函数调用字典](#函数调用字典)
4. [模块依赖关系](#模块依赖关系)
5. [API 使用规范](#api使用规范)

---

## 🏗️ 核心模块接口

### 1. ContextEngineeringIntegration
**文件**: `src/core/ContextEngineeringIntegration.ts`
**职责**: 主要的集成器，协调所有认知工具和约束生成

```typescript
interface ContextEngineeringIntegration {
  // 主要方法
  generateConstraints(taskContext: TaskContextCapsule, options?: GenerateOptions): Promise<ConstraintGenerationResult>
  getSystemState(): any
  updateConfig(config: Partial<ContextEngineeringConfig>): void
}
```

### 2. CognitiveToolOrchestrator
**文件**: `src/core/cognitive-tools/CognitiveToolOrchestrator.ts`
**职责**: 管理和执行各种认知工具

```typescript
interface CognitiveToolOrchestrator {
  executeTool(toolName: string, input: any): Promise<CognitiveResult>
  getAvailableTools(): string[]
}
```

### 3. ConstraintNeuralField
**文件**: `src/core/neural-field/ConstraintNeuralField.ts`
**职责**: 神经场计算，约束吸引子管理

```typescript
interface ConstraintNeuralField {
  addAttractor(attractor: ConstraintAttractor): void
  getAttractors(): ConstraintAttractor[]
  calculateResonance(input: any): number
}
```

### 4. EnhancedTemplateMatcher
**文件**: `src/core/constraint/EnhancedTemplateMatcher.ts`
**职责**: 智能模板匹配，集成神经场和认知工具

```typescript
interface EnhancedTemplateMatcher {
  matchTemplates(options: EnhancedTemplateMatchingOptions): Promise<EnhancedTemplateMatchResult[]>
  updateWeights(weights: Partial<EnhancedMatchingWeights>): void
}
```

### 5. ProtocolEngine
**文件**: `src/core/protocol-engine/ProtocolEngine.ts`
**职责**: 协议执行引擎，处理约束应用流程

```typescript
interface ProtocolEngine {
  executeProtocol(protocol: ProtocolShell, input: ProtocolInput): Promise<ProtocolExecutionResult>
  getExecutionContext(): ExecutionContext
}
```

---

## 📚 类型定义字典

### 核心类型

#### TaskContextCapsule (TCC)
**文件**: `src/core/types/TCC.ts`
**用途**: 任务上下文封装，包含所有任务相关信息

```typescript
interface TaskContextCapsule {
  taskType: string;
  goal: string;
  context: {
    relevantConstraints: string[];
    systemState: SystemState;
    creationTime: string;
    source: string;
    priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
    codebaseContext?: CodebaseContext;
    phaseContext?: PhaseContext;
    teamExpertise?: TeamExpertise;
    environment?: 'DEVELOPMENT' | 'STAGING' | 'PRODUCTION' | 'TESTING';
  };
  size: number;
  version: string;
}
```

#### SystemState
**文件**: `src/core/types/TCC.ts`
**用途**: 系统状态信息

```typescript
interface SystemState {
  loadLevel: 'LOW' | 'MEDIUM' | 'HIGH';
  dependencies: string[];
  activeComponents?: string[];
  // 其他系统状态属性
}
```

#### ConstraintTemplate
**文件**: `src/core/constraint/templates/types.ts`
**用途**: 约束模板定义

```typescript
interface ConstraintTemplate {
  id: string;
  name: string;
  description: string;
  category: string;
  applicableTasks: string[];
  rule: string;
  severity: 'ERROR' | 'WARNING' | 'INFO';
}
```

### 约束相关类型

#### ConstraintGenerationResult
**文件**: `src/core/ContextEngineeringIntegration.ts`
**用途**: 约束生成结果

```typescript
interface ConstraintGenerationResult {
  constraints: any[];
  confidence: number;
  reasoning: string[];
  executionTime: number;
}
```

#### EnhancedTemplateMatchingOptions
**文件**: `src/core/constraint/EnhancedTemplateMatcher.ts`
**用途**: 增强模板匹配选项

```typescript
interface EnhancedTemplateMatchingOptions {
  taskType: string;
  goal: string;
  systemState: SystemState;
  taskContext?: TaskContextCapsule;
  includeHistoricalData?: boolean;
  useNeuralField?: boolean;
  useCognitiveTools?: boolean;
  threshold?: number;
  maxResults?: number;
}
```

### 协议相关类型

#### ProtocolShell
**文件**: `src/core/protocol-engine/ProtocolShell.ts`
**用途**: 协议定义

```typescript
interface ProtocolShell {
  id: string;
  name: string;
  description: string;
  steps: ProcessStep[];
  config: ProtocolConfig;
}
```

#### ExecutionContext
**文件**: `src/core/protocol-engine/ProtocolShell.ts`
**用途**: 协议执行上下文

```typescript
interface ExecutionContext {
  protocol: ProtocolShell;
  input: ProtocolInput;
  stepResults: Map<string, any>;
  neuralField: any;
  cognitiveTools: any;
  config: ProtocolConfig;
  status: {
    currentStep?: string;
    startTime: Date;
    endTime?: Date;
    error?: string;
  };
  [key: string]: any; // 动态属性访问
}
```

---

## 🔍 函数调用字典

### 工厂函数 (Factory Functions)

#### 创建 ContextEngineeringIntegration 实例
```typescript
// 文件: src/core/utils/factory.ts
import { createDefaultContextEngineeringIntegration, createCustomContextEngineeringIntegration } from './core/utils/factory';

// 默认配置
const integration = createDefaultContextEngineeringIntegration();

// 自定义配置
const customIntegration = createCustomContextEngineeringIntegration({
  cognitive: { enableVerboseLogging: true },
  protocol: { enableVerboseLogging: false }
});
```

#### 创建神经场实例
```typescript
// 文件: src/core/utils/factory.ts
import { createNeuralField } from './core/utils/factory';

const neuralField = createNeuralField({
  decayRate: 0.1,
  resonanceBandwidth: 0.8,
  boundaryPermeability: 0.2,
  formationThreshold: 0.5,
  enableVerboseLogging: true
});
```

#### 创建认知工具编排器
```typescript
// 文件: src/core/utils/factory.ts
import { createCognitiveToolOrchestrator } from './core/utils/factory';

const orchestrator = createCognitiveToolOrchestrator(neuralField, {
  enableVerboseLogging: true
});
```

### 约束生成相关

#### 生成约束
```typescript
// 文件: src/core/ContextEngineeringIntegration.ts
const result = await integration.generateConstraints(taskContext, {
  includeReasoning: true,
  maxConstraints: 10
});

// 结果结构
console.log(result.constraints);    // 约束数组
console.log(result.confidence);     // 置信度 (0-1)
console.log(result.reasoning);      // 推理说明
console.log(result.executionTime); // 执行时间 (ms)
```

#### 模板匹配
```typescript
// 文件: src/core/constraint/EnhancedTemplateMatcher.ts
const matches = await templateMatcher.matchTemplates({
  taskType: 'SECURITY',
  goal: 'Implement authentication',
  systemState: { loadLevel: 'MEDIUM', dependencies: ['express'] },
  threshold: 0.5,
  maxResults: 5
});

// 结果结构
matches.forEach(match => {
  console.log(match.template);      // 匹配的模板
  console.log(match.relevance);     // 相关性分数
  console.log(match.confidence);    // 置信度
  console.log(match.reasons);       // 匹配原因
});
```

### 协议执行相关

#### 执行协议
```typescript
// 文件: src/core/protocol-engine/ProtocolEngine.ts
const result = await protocolEngine.executeProtocol(protocol, {
  taskContext: taskContext,
  constraints: constraints,
  options: { strictMode: false }
});

// 结果结构
console.log(result.success);        // 是否成功
console.log(result.output);         // 输出结果
console.log(result.executionTime);  // 执行时间
console.log(result.errors);         // 错误信息
```

### 认知工具相关

#### 执行认知工具
```typescript
// 文件: src/core/cognitive-tools/CognitiveToolOrchestrator.ts
const result = await orchestrator.executeTool('understandProblem', {
  code: 'function test() { return true; }',
  context: taskContext
});

// 可用工具列表
const tools = orchestrator.getAvailableTools();
// ['understandProblem', 'recallRelated', 'examineSolution', 'backtrackError']
```

---

## 🕸️ 模块依赖关系

### 核心依赖图

```
ContextEngineeringIntegration (主入口)
├── CognitiveToolOrchestrator
│   ├── ProblemUnderstandingTool
│   ├── RelatedRecallTool
│   ├── SolutionExaminationTool
│   └── ErrorBacktrackTool
├── ConstraintNeuralField
├── EnhancedTemplateMatcher
│   ├── TemplateMatcher
│   ├── SemanticAnalyzer
│   └── ConstraintNeuralField
└── ProtocolEngine
```

### 导入路径规范

```typescript
// 核心模块 - 使用 @core/* 别名
import { ContextEngineeringIntegration } from '@core/ContextEngineeringIntegration';
import { TaskContextCapsule } from '@core/types/TCC';

// 相对导入 - 仅用于同一模块内部
import { ProblemUnderstandingTool } from './ProblemUnderstandingTool';
import { TemplateMatcher } from '../constraint/TemplateMatcher';

// 工具函数 - 从工厂导入
import { createDefaultContextEngineeringIntegration } from '@core/utils/factory';
```

---

## 📝 API 使用规范

### 1. 错误处理规范

```typescript
// 正确的错误处理
try {
  const result = await integration.generateConstraints(taskContext);
  // 处理结果
} catch (error) {
  if (error instanceof Error) {
    console.error(`Constraint generation failed: ${error.message}`);
    // 特定错误处理
  } else {
    console.error('Unknown error occurred');
  }
}
```

### 2. 类型安全规范

```typescript
// 避免隐式 any
// ❌ 错误
function processData(data: any) {
  // 处理数据
}

// ✅ 正确
interface ProcessData {
  id: string;
  value: number;
}

function processData(data: ProcessData) {
  // 处理数据
}
```

### 3. 异步操作规范

```typescript
// 始终使用 async/await
// ❌ 错误
someFunction().then(result => {
  // 处理结果
}).catch(error => {
  // 处理错误
});

// ✅ 正确
try {
  const result = await someFunction();
  // 处理结果
} catch (error) {
  // 处理错误
}
```

### 4. 配置对象规范

```typescript
// 使用接口定义配置
interface IntegrationConfig {
  cognitive?: {
    enableVerboseLogging?: boolean;
  };
  protocol?: {
    enableVerboseLogging?: boolean;
  };
}

// 正确的使用方式
const config: IntegrationConfig = {
  cognitive: { enableVerboseLogging: true }
};
```

---

## 🔄 更新日志

### v1.0 (2025-08-11)
- 初始版本，包含核心模块接口
- 建立类型定义字典
- 创建函数调用字典
- 定义模块依赖关系

### 维护说明
- 每次 API 变更时更新此文档
- 新增模块时添加到依赖图
- 定期审查和更新类型定义