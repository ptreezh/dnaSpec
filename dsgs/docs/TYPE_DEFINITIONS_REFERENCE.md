# DSGS 类型定义快速参考

## 📋 目录
1. [核心类型](#核心类型)
2. [约束相关类型](#约束相关类型)
3. [认知工具类型](#认知工具类型)
4. [神经场类型](#神经场类型)
5. [协议引擎类型](#协议引擎类型)
6. [常用工具类型](#常用工具类型)

---

## 🎯 核心类型

### TaskContextCapsule (TCC)
**文件**: `src/core/types/TCC.ts`  
**用途**: 任务上下文封装，包含任务的所有相关信息

```typescript
interface TaskContextCapsule {
  /** 任务类型 */
  taskType: string;
  
  /** 任务目标 */
  goal: string;
  
  /** 上下文信息 */
  context: {
    /** 相关约束 ID 列表 */
    relevantConstraints: string[];
    
    /** 系统状态 */
    systemState: SystemState;
    
    /** 创建时间 */
    creationTime: string;
    
    /** 来源 */
    source: string;
    
    /** 优先级 */
    priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
    
    /** 代码库上下文 (可选) */
    codebaseContext?: {
      dependencies: string[];
      architecture: string;
      technologyStack: string[];
    };
    
    /** 阶段上下文 (可选) */
    phaseContext?: {
      phase: 'PROTOTYPING' | 'DEVELOPMENT' | 'STAGING' | 'PRODUCTION';
    };
    
    /** 团队专业技能 (可选) */
    teamExpertise?: {
      domainExpertise: 'BEGINNER' | 'INTERMEDIATE' | 'EXPERT';
      technologyExpertise: 'BEGINNER' | 'INTERMEDIATE' | 'EXPERT';
    };
    
    /** 环境上下文 (可选) */
    environment?: 'DEVELOPMENT' | 'STAGING' | 'PRODUCTION' | 'TESTING';
  };
  
  /** 大小 (字节) */
  size: number;
  
  /** 版本 */
  version: string;
}
```

### SystemState
**文件**: `src/core/types/TCC.ts`  
**用途**: 系统状态信息

```typescript
interface SystemState {
  /** 负载级别 */
  loadLevel: 'LOW' | 'MEDIUM' | 'HIGH';
  
  /** 依赖列表 */
  dependencies: string[];
  
  /** 活跃组件 (可选) */
  activeComponents?: string[];
}
```

---

## 🔗 约束相关类型

### ConstraintTemplate
**文件**: `src/core/constraint/templates/types.ts`  
**用途**: 约束模板定义

```typescript
interface ConstraintTemplate {
  /** 模板 ID */
  id: string;
  
  /** 模板名称 */
  name: string;
  
  /** 模板描述 */
  description: string;
  
  /** 模板类别 */
  category: string;
  
  /** 适用任务列表 */
  applicableTasks: string[];
  
  /** 约束规则 */
  rule: string;
  
  /** 严重级别 */
  severity: 'ERROR' | 'WARNING' | 'INFO';
}
```

### ConstraintGenerationResult
**文件**: `src/core/ContextEngineeringIntegration.ts`  
**用途**: 约束生成结果

```typescript
interface ConstraintGenerationResult {
  /** 生成的约束列表 */
  constraints: any[];
  
  /** 置信度 (0-1) */
  confidence: number;
  
  /** 推理说明 */
  reasoning: string[];
  
  /** 执行时间 (毫秒) */
  executionTime: number;
}
```

### EnhancedTemplateMatchingOptions
**文件**: `src/core/constraint/EnhancedTemplateMatcher.ts`  
**用途**: 增强模板匹配选项

```typescript
interface EnhancedTemplateMatchingOptions {
  /** 任务类型 */
  taskType: string;
  
  /** 任务目标 */
  goal: string;
  
  /** 系统状态 */
  systemState: SystemState;
  
  /** 任务上下文 (可选) */
  taskContext?: TaskContextCapsule;
  
  /** 包含历史数据 (可选) */
  includeHistoricalData?: boolean;
  
  /** 使用神经场 (可选) */
  useNeuralField?: boolean;
  
  /** 使用认知工具 (可选) */
  useCognitiveTools?: boolean;
  
  /** 阈值 (可选) */
  threshold?: number;
  
  /** 最大结果数 (可选) */
  maxResults?: number;
}
```

### EnhancedTemplateMatchResult
**文件**: `src/core/constraint/EnhancedTemplateMatcher.ts`  
**用途**: 增强模板匹配结果

```typescript
interface EnhancedTemplateMatchResult {
  /** 匹配的模板 */
  template: ConstraintTemplate;
  
  /** 相关性分数 */
  relevance: number;
  
  /** 置信度 */
  confidence: number;
  
  /** 匹配原因 */
  reasons: string[];
  
  /** 神经场信息 (可选) */
  neuralFieldInfo?: {
    resonance: number;
    attractors: any[];
    fieldStability: number;
  };
  
  /** 认知分析结果 (可选) */
  cognitiveAnalysis?: {
    problemType: string;
    complexity: string;
    understandingConfidence: number;
  };
}
```

---

## 🧠 认知工具类型

### CognitiveTool
**文件**: `src/core/cognitive-tools/CognitiveTool.ts`  
**用途**: 认知工具接口

```typescript
interface CognitiveTool {
  /** 工具名称 */
  name: string;
  
  /** 工具描述 */
  description: string;
  
  /** 执行方法 */
  execute(input: any): Promise<CognitiveResult>;
}
```

### CognitiveResult
**文件**: `src/core/cognitive-tools/CognitiveTool.ts`  
**用途**: 认知工具执行结果

```typescript
interface CognitiveResult {
  /** 执行状态 */
  status: 'success' | 'failed';
  
  /** 执行结果 */
  result: any;
  
  /** 错误信息 (可选) */
  error?: string;
}
```

### ProblemAnalysis
**文件**: `src/core/cognitive-tools/ProblemUnderstandingTool.ts`  
**用途**: 问题分析结果

```typescript
interface ProblemAnalysis {
  /** 问题类型 */
  type: string;
  
  /** 复杂度 */
  complexity: 'simple' | 'moderate' | 'complex';
  
  /** 识别的模式 */
  patterns: string[];
  
  /** 建议的解决方案 */
  suggestions: string[];
}
```

---

## 🌊 神经场类型

### ConstraintAttractor
**文件**: `src/core/neural-field/ConstraintAttractor.ts`  
**用途**: 约束吸引子定义

```typescript
interface ConstraintAttractor {
  /** 吸引子 ID */
  id: string;
  
  /** 核心规则 */
  coreRule: string;
  
  /** 强度 (0-1) */
  strength: number;
  
  /** 盆地宽度 */
  basinWidth: number;
  
  /** 稳定性 (0-1) */
  stability: number;
  
  /** 相关约束模板 ID */
  relatedConstraints: string[];
  
  /** 语义特征向量 */
  semanticFeatures: number[];
  
  /** 吸引子类型 */
  type: 'SECURITY' | 'PERFORMANCE' | 'ARCHITECTURE' | 'BUSINESS_LOGIC';
}
```

### AttractorDynamics
**文件**: `src/core/neural-field/ConstraintAttractor.ts`  
**用途**: 吸引子动态参数

```typescript
interface AttractorDynamics {
  /** 强度衰减率 */
  decayRate: number;
  
  /** 共振带宽 */
  resonanceBandwidth: number;
  
  /** 边界渗透性 */
  boundaryPermeability: number;
  
  /** 吸引子形成阈值 */
  formationThreshold: number;
  
  /** 启用详细日志 (可选) */
  enableVerboseLogging?: boolean;
}
```

### FieldState
**文件**: `src/core/neural-field/ConstraintAttractor.ts`  
**用途**: 场状态信息

```typescript
interface FieldState {
  /** 场稳定性 */
  stability: number;
  
  /** 活跃吸引子数量 */
  activeAttractorCount: number;
  
  /** 总能量 */
  totalEnergy: number;
  
  /** 最后更新时间 */
  lastUpdated: Date;
}
```

---

## ⚙️ 协议引擎类型

### ProtocolShell
**文件**: `src/core/protocol-engine/ProtocolShell.ts`  
**用途**: 协议定义

```typescript
interface ProtocolShell {
  /** 协议 ID */
  id: string;
  
  /** 协议名称 */
  name: string;
  
  /** 协议描述 */
  description: string;
  
  /** 处理步骤 */
  steps: ProcessStep[];
  
  /** 协议配置 */
  config: ProtocolConfig;
}
```

### ProcessStep
**文件**: `src/core/protocol-engine/ProtocolShell.ts`  
**用途**: 处理步骤定义

```typescript
interface ProcessStep {
  /** 步骤 ID */
  id: string;
  
  /** 步骤名称 */
  name: string;
  
  /** 步骤描述 */
  description: string;
  
  /** 步骤处理器 */
  processor: (context: ExecutionContext) => Promise<StepResult>;
  
  /** 是否必需 */
  required: boolean;
  
  /** 超时时间 (毫秒) */
  timeout?: number;
}
```

### ExecutionContext
**文件**: `src/core/protocol-engine/ProtocolShell.ts`  
**用途**: 协议执行上下文

```typescript
interface ExecutionContext {
  /** 协议 */
  protocol: ProtocolShell;
  
  /** 输入 */
  input: ProtocolInput;
  
  /** 步骤结果 */
  stepResults: Map<string, any>;
  
  /** 神经场 */
  neuralField: any;
  
  /** 认知工具 */
  cognitiveTools: any;
  
  /** 配置 */
  config: ProtocolConfig;
  
  /** 执行状态 */
  status: {
    currentStep?: string;
    startTime: Date;
    endTime?: Date;
    error?: string;
  };
  
  /** 动态属性访问 */
  [key: string]: any;
}
```

### ProtocolExecutionResult
**文件**: `src/core/protocol-engine/ProtocolEngine.ts`  
**用途**: 协议执行结果

```typescript
interface ProtocolExecutionResult {
  /** 是否成功 */
  success: boolean;
  
  /** 输出结果 */
  output: ProtocolOutput;
  
  /** 执行时间 (毫秒) */
  executionTime: number;
  
  /** 错误列表 */
  errors: string[];
  
  /** 步骤结果 */
  stepResults: Map<string, any>;
}
```

---

## 🛠️ 常用工具类型

### ContextEngineeringConfig
**文件**: `src/core/ContextEngineeringIntegration.ts`  
**用途**: Context-Engineering 配置

```typescript
interface ContextEngineeringConfig {
  /** 认知工具配置 */
  cognitive: {
    enableVerboseLogging: boolean;
  };
  
  /** 协议引擎配置 */
  protocol: {
    enableVerboseLogging: boolean;
  };
}
```

### GenerateOptions
**文件**: `src/core/ContextEngineeringIntegration.ts`  
**用途**: 约束生成选项

```typescript
interface GenerateOptions {
  /** 包含推理说明 */
  includeReasoning?: boolean;
  
  /** 最大约束数量 */
  maxConstraints?: number;
}
```

### ValidationCondition
**文件**: `src/modules/contract/ContractValidator.ts`  
**用途**: 验证条件

```typescript
interface ValidationCondition {
  /** 条件描述 */
  description: string;
  
  /** 验证函数 */
  validate: (value: any) => boolean;
  
  /** 错误消息 */
  errorMessage: string;
  
  /** 严重级别 */
  severity: 'ERROR' | 'WARNING' | 'INFO';
}
```

### ComponentMetrics
**文件**: `src/modules/monitoring/HealthCheckService.ts`  
**用途**: 组件指标

```typescript
interface ComponentMetrics {
  /** 组件名称 */
  name: string;
  
  /** 状态 */
  status: 'healthy' | 'warning' | 'critical';
  
  /** 响应时间 (毫秒) */
  responseTime: number;
  
  /** 错误率 */
  errorRate: number;
  
  /** 最后检查时间 */
  lastChecked: Date;
}
```

---

## 📝 类型使用最佳实践

### 1. 类型导入规范

```typescript
// ✅ 正确: 使用 type 关键字导入类型
import type { TaskContextCapsule } from '@core/types/TCC';
import type { ConstraintTemplate } from './templates/types';

// ✅ 正确: 导入接口和类
import { ContextEngineeringIntegration } from '@core/ContextEngineeringIntegration';
import { CognitiveToolOrchestrator } from '@core/cognitive-tools/CognitiveToolOrchestrator';

// ❌ 避免: 混合类型和值导入
import { TaskContextCapsule } from '@core/types/TCC'; // 如果只需要类型，使用 type
```

### 2. 类型安全检查

```typescript
// ✅ 正确: 使用类型守卫
function isTaskContextCapsule(obj: any): obj is TaskContextCapsule {
  return obj && typeof obj.taskType === 'string' && typeof obj.goal === 'string';
}

// ✅ 正确: 使用可选链操作符
function processTask(task: TaskContextCapsule | null) {
  const constraints = task?.context?.relevantConstraints || [];
  const systemState = task?.systemState || { loadLevel: 'LOW', dependencies: [] };
}

// ❌ 避免: 不安全的类型假设
function processTask(task: any) {
  const constraints = task.context.constraints; // 可能为 undefined
}
```

### 3. 泛型类型使用

```typescript
// ✅ 正确: 使用泛型约束
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  save(entity: T): Promise<T>;
  delete(id: string): Promise<void>;
}

// ✅ 正确: 使用泛型工具类型
type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

// ❌ 避免: 过度复杂的泛型约束
interface ComplexRepository<T extends { id: string }, U = keyof T> {
  // 过于复杂，难以理解和维护
}
```

### 4. 联合类型和类型守卫

```typescript
// ✅ 正确: 使用联合类型
type TaskStatus = 'pending' | 'running' | 'completed' | 'failed';

// ✅ 正确: 使用类型守卫
function isCompleted(status: TaskStatus): status is 'completed' {
  return status === 'completed';
}

// ✅ 正确: 使用可辨识联合
interface SuccessResult {
  type: 'success';
  data: any;
}

interface ErrorResult {
  type: 'error';
  error: string;
}

type Result = SuccessResult | ErrorResult;

function handleResult(result: Result) {
  if (result.type === 'success') {
    console.log(result.data);
  } else {
    console.error(result.error);
  }
}
```

---

## 🔄 类型定义更新日志

### v1.0 (2025-08-11)
- 初始版本，包含核心类型定义
- 建立类型使用规范
- 添加最佳实践指导

### 维护说明
- 每次添加新类型时更新此文档
- 保持类型定义的一致性
- 定期审查和优化类型结构

---

## 📚 相关文档

- [API 接口文档](./API_INTERFACE_DOCUMENTATION.md)
- [函数调用字典](./FUNCTION_CALL_DICTIONARY.md)
- [模块依赖关系](./MODULE_DEPENDENCY_GRAPH.md)
- [架构设计文档](./ARCHITECTURE.md)

---

**文档版本**: v1.0  
**最后更新**: 2025-08-11  
**维护者**: 开发团队