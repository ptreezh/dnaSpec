# DNASPEC 函数和类调用字典

## 📖 快速查找指南

### 🔍 按功能查找
- [约束生成](#约束生成)
- [认知工具](#认知工具)
- [神经场操作](#神经场操作)
- [协议执行](#协议执行)
- [模板匹配](#模板匹配)

### 🔍 按模块查找
- [ContextEngineeringIntegration](#contextengineeringintegration)
- [CognitiveToolOrchestrator](#cognitivetoolorchestrator)
- [ConstraintNeuralField](#constraintneuralfield)
- [EnhancedTemplateMatcher](#enhancedtemplatematcher)
- [ProtocolEngine](#protocolengine)

---

## 🎯 约束生成

### ContextEngineeringIntegration.generateConstraints()

**功能**: 生成约束的主要入口点

```typescript
// 📁 位置: src/core/ContextEngineeringIntegration.ts
// 📥 参数: 
//   - taskContext: TaskContextCapsule (必需)
//   - options?: { includeReasoning?: boolean, maxConstraints?: number }

// 📤 返回: Promise<ConstraintGenerationResult>
// 📤 结果结构: { constraints: any[], confidence: number, reasoning: string[], executionTime: number }

// ✅ 正确使用:
const result = await integration.generateConstraints(taskContext, {
  includeReasoning: true,
  maxConstraints: 10
});

// ❌ 常见错误:
// 1. 忘记 await (返回 Promise)
// 2. 传入错误的 taskContext 结构
// 3. 期望返回约束数组而不是结果对象
```

### ConstraintGenerator.generateConstraints()

**功能**: 底层约束生成器

```typescript
// 📁 位置: src/core/constraint/ConstraintGenerator.ts
// 📥 参数: TemplateMatcher, TemplateScorer, TemplateEvolver, config?
// 📤 返回: ConstraintGenerator 实例

// ✅ 正确使用:
const generator = new ConstraintGenerator(templateMatcher, scorer, evolver, {
  maxConstraints: 10,
  minRelevanceThreshold: 0.3
});
```

---

## 🧠 认知工具

### CognitiveToolOrchestrator.executeTool()

**功能**: 执行特定的认知工具

```typescript
// 📁 位置: src/core/cognitive-tools/CognitiveToolOrchestrator.ts
// 📥 参数:
//   - toolName: string (必需)
//   - input: any (必需)

// 📤 返回: Promise<CognitiveResult>
// 📤 结果结构: { status: 'success'|'failed', result: any, error?: string }

// ✅ 正确使用:
const result = await orchestrator.executeTool('understandProblem', {
  code: 'function test() { return true; }',
  context: taskContext
});

// 🛠️ 可用工具列表:
// - 'understandProblem': 问题理解
// - 'recallRelated': 相关回忆
// - 'examineSolution': 方案检查
// - 'backtrackError': 错误回溯
```

### ProblemUnderstandingTool.analyzeProblem()

**功能**: 分析代码问题

```typescript
// 📁 位置: src/core/cognitive-tools/ProblemUnderstandingTool.ts
// 📥 参数: code: string, context: TaskContextCapsule
// 📤 返回: Promise<ProblemAnalysis>

// ✅ 正确使用:
const analysis = await understandingTool.analyzeProblem(code, taskContext);
// analysis 包含: complexity, type, patterns, suggestions
```

---

## 🔀 神经场操作

### ConstraintNeuralField.addAttractor()

**功能**: 添加约束吸引子

```typescript
// 📁 位置: src/core/neural-field/ConstraintNeuralField.ts
// 📥 参数: attractor: ConstraintAttractor
// 📤 返回: void

// ✅ 正确使用:
neuralField.addAttractor({
  id: 'auth-security',
  coreRule: 'Always validate authentication',
  strength: 0.9,
  basinWidth: 0.8,
  stability: 0.95,
  relatedConstraints: ['auth-001', 'security-012'],
  semanticFeatures: [0.1, 0.8, 0.2, 0.9]
});
```

### ConstraintNeuralField.calculateResonance()

**功能**: 计算输入与神经场的共振

```typescript
// 📁 位置: src/core/neural-field/ConstraintNeuralField.ts
// 📥 参数: input: any
// 📤 返回: number (0-1)

// ✅ 正确使用:
const resonance = neuralField.calculateResonance({
  taskType: 'SECURITY',
  goal: 'Implement authentication',
  context: taskContext
});
```

---

## 📋 模板匹配

### EnhancedTemplateMatcher.matchTemplates()

**功能**: 智能模板匹配

```typescript
// 📁 位置: src/core/constraint/EnhancedTemplateMatcher.ts
// 📥 参数: options: EnhancedTemplateMatchingOptions
// 📤 返回: Promise<EnhancedTemplateMatchResult[]>

// ✅ 正确使用:
const matches = await templateMatcher.matchTemplates({
  taskType: 'SECURITY',
  goal: 'Implement authentication system',
  systemState: { loadLevel: 'MEDIUM', dependencies: ['express'] },
  threshold: 0.5,
  maxResults: 5,
  useNeuralField: true,
  useCognitiveTools: true
});

// 📤 结果示例:
// [
//   {
//     template: { id: 'auth-001', name: 'Authentication Template' },
//     relevance: 0.85,
//     confidence: 0.92,
//     reasons: ['Task type match', 'High semantic similarity'],
//     neuralFieldInfo: { resonance: 0.78, attractors: [...] },
//     cognitiveAnalysis: { problemType: 'SECURITY', complexity: 'medium' }
//   }
// ]
```

### TemplateMatcher.loadTemplates()

**功能**: 从文件系统加载模板

```typescript
// 📁 位置: src/core/constraint/TemplateMatcher.ts
// 📥 参数: templateDir: string
// 📤 返回: Promise<ConstraintTemplate[]>

// ✅ 正确使用:
const templates = await templateMatcher.loadTemplates('./src/core/constraint/templates');
```

---

## ⚙️ 协议执行

### ProtocolEngine.executeProtocol()

**功能**: 执行约束应用协议

```typescript
// 📁 位置: src/core/protocol-engine/ProtocolEngine.ts
// 📥 参数: protocol: ProtocolShell, input: ProtocolInput
// 📤 返回: Promise<ProtocolExecutionResult>

// ✅ 正确使用:
const result = await protocolEngine.executeProtocol(protocol, {
  taskContext: taskContext,
  constraints: generatedConstraints,
  options: { strictMode: false, enableLogging: true }
});

// 📤 结果结构:
// {
//   success: boolean,
//   output: ProtocolOutput,
//   executionTime: number,
//   errors: string[],
//   stepResults: Map<string, any>
// }
```

---

## 🏭 工厂函数

### createDefaultContextEngineeringIntegration()

**功能**: 创建默认配置的集成实例

```typescript
// 📁 位置: src/core/utils/factory.ts
// 📥 参数: 无
// 📤 返回: ContextEngineeringIntegration

// ✅ 正确使用:
const integration = createDefaultContextEngineeringIntegration();
```

### createCustomContextEngineeringIntegration()

**功能**: 创建自定义配置的集成实例

```typescript
// 📁 位置: src/core/utils/factory.ts
// 📥 参数: config: Partial<ContextEngineeringConfig>
// 📤 返回: ContextEngineeringIntegration

// ✅ 正确使用:
const integration = createCustomContextEngineeringIntegration({
  cognitive: { enableVerboseLogging: true },
  protocol: { enableVerboseLogging: false }
});
```

### createNeuralField()

**功能**: 创建神经场实例

```typescript
// 📁 位置: src/core/utils/factory.ts
// 📥 参数: dynamics?: Partial<AttractorDynamics>
// 📤 返回: ConstraintNeuralField

// ✅ 正确使用:
const neuralField = createNeuralField({
  decayRate: 0.1,
  resonanceBandwidth: 0.8,
  boundaryPermeability: 0.2,
  formationThreshold: 0.5,
  enableVerboseLogging: true
});
```

### createCognitiveToolOrchestrator()

**功能**: 创建认知工具编排器

```typescript
// 📁 位置: src/core/utils/factory.ts
// 📥 参数: neuralField: ConstraintNeuralField, config?: any
// 📤 返回: CognitiveToolOrchestrator

// ✅ 正确使用:
const orchestrator = createCognitiveToolOrchestrator(neuralField, {
  enableVerboseLogging: true
});
```

### createEnhancedTemplateMatcher()

**功能**: 创建增强模板匹配器

```typescript
// 📁 位置: src/core/utils/factory.ts
// 📥 参数: neuralField: ConstraintNeuralField, cognitiveTools: CognitiveToolOrchestrator, weights?: Partial<EnhancedMatchingWeights>
// 📤 返回: EnhancedTemplateMatcher

// ✅ 正确使用:
const matcher = createEnhancedTemplateMatcher(neuralField, cognitiveTools, {
  typeMatch: 0.25,
  semanticScore: 0.25,
  contextFit: 0.15,
  historicalEffectiveness: 0.15,
  neuralFieldResonance: 0.1,
  cognitiveAnalysis: 0.1
});
```

---

## 📊 状态查询函数

### ContextEngineeringIntegration.getSystemState()

**功能**: 获取系统状态

```typescript
// 📁 位置: src/core/ContextEngineeringIntegration.ts
// 📥 参数: 无
// 📤 返回: any

// ✅ 正确使用:
const state = integration.getSystemState();
// 返回: { status: 'healthy', config: {...}, timestamp: string }
```

### CognitiveToolOrchestrator.getAvailableTools()

**功能**: 获取可用工具列表

```typescript
// 📁 位置: src/core/cognitive-tools/CognitiveToolOrchestrator.ts
// 📥 参数: 无
// 📤 返回: string[]

// ✅ 正确使用:
const tools = orchestrator.getAvailableTools();
// 返回: ['understandProblem', 'recallRelated', 'examineSolution', 'backtrackError']
```

---

## ⚠️ 错误处理模式

### 标准异步错误处理

```typescript
// ✅ 推荐模式
try {
  const result = await someAsyncFunction(params);
  // 处理成功结果
} catch (error) {
  if (error instanceof Error) {
    console.error(`Operation failed: ${error.message}`);
    // 特定错误处理
  } else {
    console.error('Unknown error occurred');
  }
}

// ❌ 避免模式
someAsyncFunction(params).then(result => {
  // 处理结果
}).catch(error => {
  // 错误处理
});
```

### 类型安全检查

```typescript
// ✅ 推荐模式
function processTask(task: TaskContextCapsule | null) {
  if (!task) {
    throw new Error('Task context is required');
  }
  
  // 安全访问
  const constraints = task.context?.relevantConstraints || [];
  const systemState = task.systemState || { loadLevel: 'LOW', dependencies: [] };
}

// ❌ 避免模式
function processTask(task: any) {
  // 不安全的类型使用
  const constraints = task.context.constraints; // 可能为 undefined
}
```

---

## 🔄 更新历史

### v1.0 (2025-08-11)
- 初始版本，包含核心函数调用
- 建立标准使用模式
- 添加错误处理指导

### 维护说明
- 每次添加新函数时更新此字典
- 保持示例代码的准确性
- 定期审查和更新最佳实践