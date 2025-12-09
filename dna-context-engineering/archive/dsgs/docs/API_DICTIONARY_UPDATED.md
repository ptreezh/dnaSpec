# DNASPEC 函数和类调用字典 (更新版)

## 📖 重要发现

**⚠️ API字典应用失效**: 发现测试中大量使用不存在的API方法，说明API字典同步机制没有正常工作。

**🔍 需要立即修复的API不匹配问题**:

### TemplateEvolver - 实际API vs 测试期望

**实际API** (基于源码分析):
```typescript
// 📁 位置: src/core/constraint/TemplateEvolver.ts

// 构造函数
constructor(storage?: MetricsStorage)

// 主要方法
public async trackEffectiveness(
  template: ConstraintTemplate, 
  tcc: TaskContextCapsule, 
  outcome: ConstraintOutcome
): Promise<void>

public async processUserFeedback(
  template: ConstraintTemplate, 
  tcc: TaskContextCapsule, 
  feedback: UserFeedback
): Promise<void>

public getTemplateMetrics(templateId: string): TemplateMetrics | undefined

public async getTemplatesNeedingReview(): Promise<string[]>
```

**类型定义**:
```typescript
export type ConstraintOutcome = 'VIOLATION' | 'RESOLUTION'
export type UserFeedback = 'POSITIVE' | 'NEGATIVE'

export interface TemplateMetrics {
  violations: number;
  resolutions: number;
  historicalEffectiveness: number;
  userFeedback: { positive: number; negative: number };
  needsReview: boolean;
  lastUsed: string;
  usageCount: number;
}
```

**❌ 测试中错误使用的方法**:
- `evolveTemplate()` - **不存在**
- `improveTemplate()` - **不存在**  
- `addTemplate/removeTemplate()` - **不存在**
- `processFeedback()` - **应该是 processUserFeedback()`
- `getEvolutionMetrics()` - **不存在**

### ContextEngineeringIntegration - 实际API vs 测试期望

**实际API**:
```typescript
public async generateConstraints(taskContext: TaskContextCapsule, options?: any): Promise<ConstraintGenerationResult>
public getSystemState(): any
```

**❌ 测试中错误使用的方法**:
- `getNeuralField()` - **不存在**
- `getCognitiveTools()` - **不存在**
- `getTemplateMatcher()` - **不存在**
- `getProtocolEngine()` - **不存在**

### TemplateReevaluator - 实际API vs 测试期望

**❌ 测试中错误使用的方法**:
- `evolveTemplate()` - **不存在**
- `addTemplate/removeTemplate()` - **不存在**
- `updateTemplate()` - **不存在**
- `getTemplates()` - **不存在**
- `getTemplate()` - **不存在**
- `getPerformanceMetrics()` - **不存在**

---

## 🚨 紧急修复任务

1. **更新所有测试文件中的API调用**
2. **修复TemplateEvolver相关测试**
3. **修复ContextEngineeringIntegration相关测试**
4. **修复TemplateReevaluator相关测试**
5. **重新建立API字典同步机制**

---

## 📋 原始API字典内容 (待验证)

*(下面的内容需要与实际源码重新验证)*

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