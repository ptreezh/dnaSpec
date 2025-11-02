# TDD角色和任务计划 (更新版)

## 📊 **当前状态**

**整体进度**: 
- ✅ **已完成**: ContractGenerator、TemplateMatcher编译错误修复
- 🔄 **进行中**: API不匹配问题分析和修复
- 📋 **待处理**: 6个测试套件的API重写

**测试通过率**: 47.1% (8/17 测试套件)

---

## 🎯 **TDD修复策略调整**

### 📋 **问题重新分类**

#### 🔴 **API不匹配问题** (影响6个测试套件)
**根本原因**: 实际源码API与测试期望API完全不同
**解决方案**: 基于实际源码API重写测试

#### 🟡 **SystemState类型问题** (影响1个测试套件)  
**根本原因**: 缺少必需字段
**解决方案**: 添加memory、activeComponents、constraints字段

#### 🟢 **逻辑问题** (影响1个测试套件)
**根本原因**: 功能逻辑错误
**解决方案**: 分析并修复逻辑错误

---

## 📝 **详细任务分配**

### 🚨 **紧急任务** (基于实际API重写测试)

#### 任务1: TemplateReevaluator.test.ts 重写
**负责人**: TDD团队  
**优先级**: 🔴 最高
**工作量**: 2-3小时

**实际API**:
```typescript
public async trackEffectiveness(template, tcc, outcome): Promise<void>
public async processUserFeedback(template, tcc, feedback): Promise<void>
```

**需要删除的错误API**:
- `evolveTemplate()` - 不存在
- `addTemplate/removeTemplate()` - 不存在  
- `updateTemplate()` - 不存在
- `getTemplates/getTemplate()` - 不存在
- `getPerformanceMetrics()` - 不存在

#### 任务2: TemplateEvolver.integration.test.ts 重写
**负责人**: TDD团队
**优先级**: 🔴 最高  
**工作量**: 2-3小时

**实际API**:
```typescript
public async trackEffectiveness(template, tcc, outcome): Promise<void>
public async processUserFeedback(template, tcc, feedback): Promise<void>
public getTemplateMetrics(templateId): TemplateMetrics | undefined
```

**需要删除的错误API**:
- `evolveTemplate()` - 不存在
- `improveTemplate()` - 不存在
- `optimizeTemplate()` - 不存在
- `balanceTemplate()` - 不存在
- `evolveRelatedTemplates()` - 不存在

#### 任务3: TemplateEvolver.e2e.test.ts 重写
**负责人**: TDD团队
**优先级**: 🔴 最高
**工作量**: 3-4小时

**实际API**:
```typescript
public async processUserFeedback(template, tcc, feedback): Promise<void>
public async trackEffectiveness(template, tcc, outcome): Promise<void>
```

**需要修复的错误API**:
- `processFeedback()` → `processUserFeedback()`
- `evolveTemplate()` → 删除
- `getEvolutionMetrics()` → 删除

#### 任务4: ContextEngineeringIntegration相关测试重写
**负责人**: TDD团队
**优先级**: 🔴 最高
**工作量**: 2-3小时

**实际API**:
```typescript
public async generateConstraints(taskContext, options): Promise<ConstraintGenerationResult>
public getSystemState(): any
```

**需要删除的错误API**:
- `getNeuralField()` - 不存在
- `getCognitiveTools()` - 不存在
- `getTemplateMatcher()` - 不存在
- `getProtocolEngine()` - 不存在

### 🟡 **高优先级任务**

#### 任务5: McpAdapter.test.ts SystemState修复
**负责人**: TDD团队
**优先级**: 🟡 高
**工作量**: 1小时

**需要添加的字段**:
```typescript
systemState: {
  loadLevel: 'LOW' | 'MED' | 'HIGH';
  dependencies: string[];
  resourceAvailability: { cpu: number; memory: number; network: number; };
  environment: 'DEVELOPMENT' | 'TESTING' | 'PRODUCTION';
  memory: number; // 添加
  activeComponents: string[]; // 添加
  constraints: EnvironmentConstraint[]; // 添加
}
```

#### 任务6: DSGS_EndToEnd.test.ts 重写
**负责人**: TDD团队  
**优先级**: 🟡 高
**工作量**: 4-5小时

**需要修复的问题**:
- SystemState字段缺失
- `getWorkflowTime()` - 不存在
- `contextEngineeringIntegration` 变量名错误
- 大量语法错误

### 🟢 **中优先级任务**

#### 任务7: SpecificationManager逻辑修复
**负责人**: TDD团队
**优先级**: 🟢 中
**工作量**: 2-3小时

**需要解决的问题**:
- 3个功能测试失败
- 逻辑错误，非编译错误

---

## 📅 **时间线安排**

### **第一天** (紧急任务)
- [ ] 完成TemplateReevaluator.test.ts重写
- [ ] 完成TemplateEvolver.integration.test.ts重写
- [ ] 验证修复效果

### **第二天** (继续API修复)
- [ ] 完成TemplateEvolver.e2e.test.ts重写
- [ ] 完成ContextEngineeringIntegration相关测试重写
- [ ] 修复McpAdapter.test.ts SystemState问题

### **第三天** (收尾工作)
- [ ] 完成DSGS_EndToEnd.test.ts重写
- [ ] 修复SpecificationManager逻辑问题
- [ ] 全面测试验证

---

## 🎯 **成功标准**

### **目标状态**
- 测试套件通过率: 85%+ (14/17+)
- API不匹配错误: 0个
- SystemState类型错误: 0个

### **质量门禁**
- 每次修复后运行 `npm test` 验证
- 不引入新的失败测试
- 保持现有测试的功能完整性

---

## 📚 **参考资料**

### **API文档**
- `docs/API_DICTIONARY_UPDATED.md` - 实际API分析结果
- `src/core/constraint/TemplateEvolver.ts` - TemplateEvolver实际源码
- `src/core/ContextEngineeringIntegration.ts` - ContextEngineeringIntegration实际源码

### **类型定义**
- `src/core/types/TCC.ts` - SystemState类型定义

### **工作状态**
- `TDD_WORK_STATUS.md` - 当前工作状态和进度