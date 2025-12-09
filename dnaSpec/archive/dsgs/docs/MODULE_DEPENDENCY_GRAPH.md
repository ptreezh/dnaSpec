# DNASPEC 模块依赖关系图

## 📋 目录
1. [核心架构图](#核心架构图)
2. [模块详细依赖](#模块详细依赖)
3. [循环依赖分析](#循环依赖分析)
4. [导入路径规范](#导入路径规范)
5. [模块职责边界](#模块职责边界)

---

## 🏗️ 核心架构图

```
DNASPEC (Dynamic Specification Growth System)
│
├── 📦 src/core/ (核心模块)
│   ├── 🎯 ContextEngineeringIntegration.ts (主入口)
│   ├── 🧠 cognitive-tools/ (认知工具)
│   ├── 🔗 constraint/ (约束处理)
│   ├── 🌊 neural-field/ (神经场)
│   ├── ⚙️ protocol-engine/ (协议引擎)
│   ├── 📊 types/ (类型定义)
│   ├── 🛠️ utils/ (工具函数)
│   └── 📈 state/ (状态管理)
│
├── 📦 src/modules/ (功能模块)
│   ├── 📄 contract/ (契约管理)
│   └── 📊 monitoring/ (监控服务)
│
├── 📦 src/integration/ (集成接口)
│   ├── 💻 cli/ (命令行接口)
│   └── 🔌 mcp/ (MCP 适配器)
│
└── 📦 test/ (测试)
    ├── 📦 unit/ (单元测试)
    ├── 📦 integration/ (集成测试)
    └── 📦 e2e/ (端到端测试)
```

---

## 🔍 模块详细依赖

### 1. ContextEngineeringIntegration (主入口)

**依赖层级**: 1 (顶层)  
**文件**: `src/core/ContextEngineeringIntegration.ts`

```typescript
// 📥 导入依赖
import { TaskContextCapsule } from './types/TCC';                    // ✅ 核心类型
import { DEFAULT_CONTEXT_ENGINEERING_CONFIG } from './ContextEngineeringIntegration'; // ✅ 自身配置

// 🚫 注意: 此模块应该保持轻量，主要依赖工厂函数
// ❌ 避免直接导入具体的实现类
```

**依赖关系**:
- 📄 `types/TCC.ts` (TaskContextCapsule)
- 🛠️ `utils/factory.ts` (工厂函数)

### 2. Cognitive Tool Orchestrator (认知工具编排器)

**依赖层级**: 2  
**文件**: `src/core/cognitive-tools/CognitiveToolOrchestrator.ts`

```typescript
// 📥 导入依赖
import { ConstraintNeuralField } from '../neural-field/ConstraintNeuralField';  // ✅ 神经场
import { TaskContextCapsule } from '../types/TCC';                          // ✅ 核心类型
import { CognitiveTool, CognitiveResult, CognitiveConfig } from './CognitiveTool'; // ✅ 工具接口
```

**依赖关系**:
- 🌊 `neural-field/ConstraintNeuralField.ts`
- 📊 `types/TCC.ts`
- 🧠 `cognitive-tools/CognitiveTool.ts`

### 3. Constraint Neural Field (约束神经场)

**依赖层级**: 2  
**文件**: `src/core/neural-field/ConstraintNeuralField.ts`

```typescript
// 📥 导入依赖
import { ConstraintAttractor, AttractorDynamics, FieldState } from './ConstraintAttractor'; // ✅ 吸引子
import { SystemState } from '../types/TCC';                                      // ✅ 系统状态
```

**依赖关系**:
- 🔗 `neural-field/ConstraintAttractor.ts`
- 📊 `types/TCC.ts`

### 4. Enhanced Template Matcher (增强模板匹配器)

**依赖层级**: 2  
**文件**: `src/core/constraint/EnhancedTemplateMatcher.ts`

```typescript
// 📥 导入依赖
import { SystemState } from '@core/types/TCC';                              // ✅ 核心类型
import type { ConstraintTemplate } from './templates/types';               // ✅ 模板类型
import { SemanticAnalyzer } from './SemanticAnalyzer';                       // ✅ 语义分析
import { ConstraintNeuralField } from '../neural-field/ConstraintNeuralField'; // ✅ 神经场
import { CognitiveToolOrchestrator } from '../cognitive-tools/CognitiveToolOrchestrator'; // ✅ 认知工具
import { TaskContextCapsule } from '@core/types/TCC';                      // ✅ 任务上下文
```

**依赖关系**:
- 📊 `types/TCC.ts`
- 📄 `constraint/templates/types.ts`
- 🔍 `constraint/SemanticAnalyzer.ts`
- 🌊 `neural-field/ConstraintNeuralField.ts`
- 🧠 `cognitive-tools/CognitiveToolOrchestrator.ts`

### 5. Protocol Engine (协议引擎)

**依赖层级**: 2  
**文件**: `src/core/protocol-engine/ProtocolEngine.ts`

```typescript
// 📥 导入依赖
import { ProtocolShell, ProcessStep, ProtocolInput, ProtocolOutput, ExecutionContext } from './ProtocolShell'; // ✅ 协议定义
import { ConstraintNeuralField } from '../neural-field/ConstraintNeuralField';     // ✅ 神经场
import { CognitiveToolOrchestrator } from '../cognitive-tools/CognitiveToolOrchestrator'; // ✅ 认知工具
```

**依赖关系**:
- ⚙️ `protocol-engine/ProtocolShell.ts`
- 🌊 `neural-field/ConstraintNeuralField.ts`
- 🧠 `cognitive-tools/CognitiveToolOrchestrator.ts`

---

## 🔄 循环依赖分析

### ⚠️ 已识别的循环依赖

#### 1. 轻微循环: EnhancedTemplateMatcher ↔ CognitiveToolOrchestrator
```
EnhancedTemplateMatcher → CognitiveToolOrchestrator → EnhancedTemplateMatcher (在工具中使用)
```
**解决方案**: ✅ 已通过接口分离解决

#### 2. 潜在循环: Constraint 模块内部
```
ConstraintGenerator → TemplateMatcher → TemplateEvolver → ConstraintGenerator
```
**解决方案**: ✅ 已通过工厂模式解耦

### 🛡️ 防止循环依赖的策略

#### 1. 接口分离原则
```typescript
// ✅ 正确: 使用接口分离
interface ITemplateMatcher {
  matchTemplates(options: any): Promise<any[]>;
}

class EnhancedTemplateMatcher implements ITemplateMatcher {
  // 实现
}

// 其他模块依赖接口而不是具体实现
class SomeModule {
  constructor(private matcher: ITemplateMatcher) {}
}
```

#### 2. 事件驱动架构
```typescript
// ✅ 正确: 使用事件解耦
class TemplateMatcher {
  onTemplateMatched(callback: (result: any) => void) {
    // 事件触发时调用回调
  }
}

class CognitiveTool {
  constructor(templateMatcher: TemplateMatcher) {
    templateMatcher.onTemplateMatched((result) => {
      // 处理匹配结果，不直接依赖
    });
  }
}
```

#### 3. 依赖注入模式
```typescript
// ✅ 正确: 使用依赖注入
class ContextEngineeringIntegration {
  constructor(
    private templateMatcher: ITemplateMatcher,
    private neuralField: INeuralField,
    private cognitiveTools: ICognitiveToolOrchestrator
  ) {}
}
```

---

## 📝 导入路径规范

### 1. 路径别名使用规范

```typescript
// ✅ 核心模块 - 使用 @core/* 别名
import { TaskContextCapsule } from '@core/types/TCC';
import { ContextEngineeringIntegration } from '@core/ContextEngineeringIntegration';
import { createDefaultContextEngineeringIntegration } from '@core/utils/factory';

// ✅ 同级模块 - 使用相对路径
import { ProblemUnderstandingTool } from './ProblemUnderstandingTool';
import { TemplateMatcher } from '../constraint/TemplateMatcher';

// ✅ 子模块导入 - 使用相对路径
import { ConstraintAttractor } from './ConstraintAttractor';
import { SemanticAnalyzer } from './SemanticAnalyzer';

// ❌ 避免混合使用
import { TaskContextCapsule } from '../../core/types/TCC'; // 不要这样做
import { TaskContextCapsule } from '@core/types/TCC'; // 正确方式
```

### 2. 导入顺序规范

```typescript
// ✅ 正确的导入顺序
// 1. 第三方库
import * as fs from 'fs';
import * as path from 'path';

// 2. 核心类型和接口
import { TaskContextCapsule, SystemState } from '@core/types/TCC';

// 3. 项目内部模块 (按层级)
import { ContextEngineeringIntegration } from '@core/ContextEngineeringIntegration';
import { CognitiveToolOrchestrator } from '@core/cognitive-tools/CognitiveToolOrchestrator';

// 4. 同级模块
import { ProblemUnderstandingTool } from './ProblemUnderstandingTool';

// 5. 类型导入 (type)
import type { ConstraintTemplate } from './templates/types';
```

### 3. 类型导入规范

```typescript
// ✅ 类型导入使用 type 关键字
import type { ConstraintTemplate } from './templates/types';
import type { SystemState } from '@core/types/TCC';

// ✅ 接口导入
import { TaskContextCapsule } from '@core/types/TCC';

// ❌ 避免不必要的值导入
import { ConstraintTemplate } from './templates/types'; // 如果只需要类型，使用 type
```

---

## 🎯 模块职责边界

### 1. ContextEngineeringIntegration (主入口)
**职责**: 系统协调和对外接口  
**边界**: 
- ✅ 提供统一的 API 入口
- ✅ 协调各个子模块的工作
- ❌ 不包含具体的业务逻辑实现
- ❌ 不直接依赖具体的实现类

### 2. Cognitive Tool Orchestrator (认知工具编排器)
**职责**: 认知工具的管理和执行  
**边界**:
- ✅ 管理认知工具的生命周期
- ✅ 提供统一的工具执行接口
- ❌ 不实现具体的认知算法
- ❌ 不依赖具体的工具实现

### 3. Constraint Neural Field (约束神经场)
**职责**: 神经场计算和吸引子管理  
**边界**:
- ✅ 实现神经场的数学计算
- ✅ 管理吸引子的生命周期
- ❌ 不涉及具体的约束生成逻辑
- ❌ 不依赖认知工具

### 4. Enhanced Template Matcher (增强模板匹配器)
**职责**: 智能模板匹配和评分  
**边界**:
- ✅ 实现多维度模板匹配算法
- ✅ 集成神经场和认知工具的增强功能
- ❌ 不定义具体的模板内容
- ❌ 不直接生成约束

### 5. Protocol Engine (协议引擎)
**职责**: 约束应用协议的执行  
**边界**:
- ✅ 执行预定义的约束应用流程
- ✅ 管理协议执行的状态
- ❌ 不定义具体的协议内容
- ❌ 不实现约束的具体应用逻辑

---

## 📊 模块健康度检查

### 模块复杂度评估

| 模块 | 文件数 | 依赖数 | 循环依赖 | 复杂度 | 状态 |
|------|--------|--------|----------|--------|------|
| ContextEngineeringIntegration | 1 | 2 | 无 | 🟢 低 | 健康 |
| CognitiveToolOrchestrator | 1 | 3 | 无 | 🟢 低 | 健康 |
| ConstraintNeuralField | 1 | 2 | 无 | 🟢 低 | 健康 |
| EnhancedTemplateMatcher | 1 | 5 | 无 | 🟡 中 | 需关注 |
| ProtocolEngine | 1 | 3 | 无 | 🟢 低 | 健康 |
| Constraint 模块组 | 8 | 12 | 1个 | 🟡 中 | 需优化 |
| Contract 模块组 | 15 | 25 | 3个 | 🔴 高 | 需重构 |

### 优化建议

#### 🟡 中等复杂度模块优化

1. **EnhancedTemplateMatcher**
   - 考虑拆分为多个专门的匹配器
   - 将神经场和认知工具的集成逻辑分离

#### 🔴 高复杂度模块优化

1. **Contract 模块组**
   - 重新设计模块架构，减少耦合
   - 提取公共接口和工具函数
   - 解决循环依赖问题

---

## 🔄 更新和维护

### 依赖关系图更新流程

1. **添加新模块时**
   - 确定模块的职责边界
   - 识别依赖关系
   - 检查是否会产生循环依赖
   - 更新此文档

2. **重构现有模块时**
   - 分析当前的依赖关系
   - 设计新的依赖结构
   - 逐步重构，保持系统可用性
   - 更新文档和测试

3. **定期审查**
   - 每月审查模块依赖关系
   - 识别潜在的架构问题
   - 制定优化计划

### 工具和自动化

建议使用以下工具来自动化依赖关系分析：

1. **TypeScript 编译器**
   - 使用 `tsc --noEmit` 检查类型错误
   - 使用 `tsc --traceResolution` 分析模块解析

2. **依赖分析工具**
   - `madge` - 循环依赖检测
   - `dependency-cruiser` - 依赖关系可视化

3. **代码质量工具**
   - `sonarqube` - 架构健康度检查
   - `lighthouse` - 代码质量评估

---

## 📚 相关文档

- [API 接口文档](./API_INTERFACE_DOCUMENTATION.md)
- [函数调用字典](./FUNCTION_CALL_DICTIONARY.md)
- [类型定义参考](./TYPE_DEFINITIONS.md)
- [架构设计文档](./ARCHITECTURE.md)

---

**文档版本**: v1.0  
**最后更新**: 2025-08-11  
**维护者**: 开发团队