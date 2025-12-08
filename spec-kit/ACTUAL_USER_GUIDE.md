# spec.kit 实际可用功能和使用指南

## 重要说明 - 当前实际可用功能

### 实际支持的命令结构

#### Claude Skills 环境（完整命令）
- `/speckit.specify` - 规格创建
- `/speckit.plan` - 技术规划
- `/speckit.tasks` - 任务分解
- `/speckit.implement` - 实施指导
- `/speckit.constitution` - 项目宪法

#### Context Engineering Skills
- `/context-analysis` - 上下文分析
- `/context-optimization` - 上下文优化
- `/cognitive-template` - 认知模板
- `/context-analysis-enhanced` - 增强上下文分析
- `/context-optimization-enhanced` - 增强上下文优化
- `/cognitive-template-enhanced` - 增强认知模板

#### DNASPEC Intelligent Architect Skills
- `/dnaspec-architect` - DNASPEC架构师
- `/dnaspec-system-architect` - DNASPEC系统架构师
- `/dnaspec-agent-creator` - DNASPEC智能体创建器
- `/dnaspec-constraint-generator` - DNASPEC约束生成器
- `/dnaspec-task-decomposer` - DNASPEC任务分解器
- `/dnaspec-modulizer` - DNASPEC模块化验证器
- `/dnaspec-dapi-checker` - DNASPEC接口检查器

#### Workflow Skills
- `/context-engineering-workflow` - 上下文工程工作流

---

## 实际可用的用户体验改进

### 1. 交互提示词增强

虽然无法创建快捷方式，但可以通过以下方式提高效率：

#### 提示词模板（可复制使用）
```
请使用 dnaspec-architect 技能为以下需求设计系统架构：
[在此插入您的项目需求]
```

```
请使用 context-analysis 技能分析以下内容：
[在此插入您要分析的内容]
```

### 2. 工作流优化建议

#### 标准开发流程
1. `/speckit.constitution` - 建立项目开发规范
2. `/speckit.specify` - 创建项目规格
3. `/speckit.plan` - 制定技术计划
4. `/speckit.tasks` - 分解实施任务
5. `/speckit.implement` - 指导具体实施

#### 内容优化流程
1. `/context-analysis` - 分析内容质量
2. `/context-optimization` - 优化内容
3. `/cognitive-template` - 应用认知模式

### 3. 使用提醒

#### 最佳实践
- 在使用任何技能前，先清楚了解其功能描述
- 对于复杂任务，可结合多个技能形成工作流
- 使用增强版技能获得更专业的结果

#### 注意事项
- 所有技能都需要提供明确的输入参数
- 结果质量取决于输入描述的清晰度
- 某些技能可能需要额外的上下文信息

---

## 高效使用技巧

### 1. 参数优化
在使用技能时，提供尽可能详细的参数：
```
正确: /speckit.specify 电商网站需要用户注册、商品浏览、购物车、支付功能...
更好: /speckit.specify 我需要开发一个电商网站，主要功能包括：用户注册/登录、商品分类浏览、购物车管理、安全支付、订单跟踪...
```

### 2. 结果解读
- 仔细阅读技能返回的结果
- 注意技能提供的建议和最佳实践
- 根据项目实际情况调整建议

### 3. 错误处理
如果某个技能没有产生预期结果：
- 检查输入描述是否清晰
- 尝试使用不同的技能
- 提供更多的上下文信息

---

## 实际可用的完整技能列表

### 核心 Spec-Driven Skills
- `speckit.specify`: 项目规格创建
- `speckit.plan`: 技术规划与设计
- `speckit.tasks`: 任务分解与规划
- `speckit.implement`: 实施指导
- `speckit.constitution`: 项目规范制定

### Context Engineering Skills
- `context-analysis`: 内容质量分析
- `context-optimization`: 内容优化
- `cognitive-template`: 认知模式应用
- `context-analysis-enhanced`: 高级内容分析
- `context-optimization-enhanced`: 高级内容优化
- `cognitive-template-enhanced`: 高级认知应用
- `context-engineering-workflow`: 完整工作流

### DNASPEC Intelligent Architect Skills
- `dnaspec-architect`: 系统架构设计
- `dnaspec-system-architect`: 技术架构设计
- `dnaspec-agent-creator`: 智能体创建
- `dnaspec-constraint-generator`: 约束生成
- `dnaspec-task-decomposer`: 任务分解
- `dnaspec-modulizer`: 模块化验证
- `dnaspec-dapi-checker`: 接口检查

---

## 获取帮助

对于任何技能的帮助，请查看对应技能的文档说明，或者在使用时提供更清晰的参数描述以获得更好的结果。