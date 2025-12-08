# DSGS Context Engineering Skills - 专业功能详解手册

## 🎯 产品核心价值
DSGS Context Engineering Skills 是一个为AI CLI环境设计的上下文工程增强系统，通过AI原生智能实现专业级的上下文分析、优化和结构化，提升AI辅助开发的效率和质量。

## 📋 完整功能列表

### 1. 核心上下文工程技能

#### 1.1 Context Analysis (上下文分析)
- **功能**: 对提供的上下文进行五维质量评估
- **AI CLI使用**: `/speckit.dsgs.context-analysis "待分析内容"`
- **输出**:
  - 五维指标评分 (清晰度、相关性、完整性、一致性、效率)
  - 优化建议
  - 识别问题
  - Token估算

#### 1.2 Context Optimization (上下文优化)
- **功能**: 基于分析结果优化上下文质量
- **AI CLI使用**: `/speckit.dsgs.context-optimization "待优化内容"`
- **输出**:
  - 优化后的内容
  - 应用的优化措施
  - 改进指标

#### 1.3 Cognitive Template (认知模板)
- **功能**: 应用专业认知框架到任务
- **AI CLI使用**: `/speckit.dsgs.cognitive-template "任务描述" template=verification`
- **可用模板**:
  - `chain_of_thought`: 思维链推理
  - `few_shot`: 少样本学习
  - `verification`: 验证检查
  - `role_playing`: 角色扮演
  - `understanding`: 深度理解

### 2. 高级专业功能

#### 2.1 Agentic 设计功能
- **代理创建**: 根据需求创建专业AI代理
  - **API调用**: `create_agent_with_context_analysis(goals, constraints)`
  - **功能**: 创建具有上下文分析能力的智能代理
  - **输出**: 代理规格、能力定义、行为策略

- **任务分解代理**:
  - **API调用**: `decompose_complex_task(task_description)`
  - **功能**: 自动分解复杂任务为可执行子任务
  - **输出**: 任务层次结构、依赖关系、预计耗时、所需技能

#### 2.2 项目结构设计功能
- **智能目录设计**:
  - **API调用**: `design_project_structure(requirements)`
  - **功能**: 根据需求生成项目目录结构
  - **输出**: 推荐目录结构、模块边界定义、最佳实践建议

- **架构模式推荐**:
  - **API调用**: `design_project_structure(requirements)`
  - **功能**: 推荐适合的架构模式
  - **输出**: 架构推荐、实现指南、最佳实践

#### 2.3 约束生成与验证功能
- **约束生成**:
  - **API调用**: `generate_constraints_from_requirements(requirements)`
  - **功能**: 从需求生成系统约束
  - **输出**: 功能约束、非功能约束、架构约束、业务约束

- **API规范验证**:
  - **API调用**: `generate_constraints_from_requirements(requirements)` (用于API约束)
  - **功能**: 检查API接口设计质量
  - **输出**: 规范性检查、最佳实践验证、改进建议、安全要求

### 3. AI安全工作流功能

#### 3.1 临时工作区管理
- **功能**: 隔离AI生成的临时文件，防止项目污染
- **AI CLI使用**:
  - 创建: `/speckit.dsgs.temp-workspace "operation=create-workspace"`
  - 添加文件: `/speckit.dsgs.temp-workspace "operation=add-file path=gen.py content=# code"`
  - 确认文件: `/speckit.dsgs.temp-workspace "operation=confirm-file file=gen.py"`
  - 清理: `/speckit.dsgs.temp-workspace "operation=clean-workspace"`

- **工作流程**:
  1. AI生成内容 → 临时工作区隔离
  2. 人工验证 → 移至确认区域
  3. 安全提交 → 到Git仓库
  4. 自动清理 → 临时工作区

#### 3.2 Git操作集成
- **功能**: 完整的Git工作流支持，与AI工作流集成
- **AI CLI使用**: `/speckit.dsgs.git-skill "operation=status"`
- **支持操作**:
  - 基础操作: status, add, commit, push, pull
  - 分支管理: create, switch, merge
  - 高级功能: worktree管理、stash、diff
  - CI/CD集成: 自动化提交流程

### 4. 透明化交互功能

#### 4.1 智能解析器
- **功能**: 自动识别用户意图，透明调用合适技能
- **AI CLI使用**: 直接输入自然语言
  - `"帮我分析这段代码有什么问题"` → 自动执行context-analysis
  - `"优化这个需求描述"` → 自动执行context-optimization
  - `"用专业模板分析设计"` → 自动执行cognitive-template

#### 4.2 简化命令
- **快捷功能**:
  - `/speckit.dsgs.context-optimization "内容"` → 自动优化
  - `/speckit.dsgs.context-analysis "内容"` → 自动分析
  - `/speckit.dsgs.context-analysis "内容" goals=review` → 自动审查
  - `/speckit.dsgs.cognitive-template "描述" template=chain_of_thought` → 智能处理

### 5. 专业工作流功能

#### 5.1 任务分拆功能
- **功能**: 智能分解复杂任务为可管理的子任务
- **AI CLI使用**: `/speckit.dsgs.architect "分解开发用户认证模块 task=decompose"`
- **输出**:
  - 任务分解层级
  - 资源估算
  - 风险评估
  - 执行策略
  - 进度跟踪定义

#### 5.2 上下文优化策略
- **功能**: 多维度上下文增强和优化
- **策略类型**:
  - 清晰度: 提升表达明确性
  - 完整性: 补充必要信息
  - 结构化: 优化组织结构
  - 相关性: 强化目标关联
  - 效率: 优化信息密度
- **AI CLI使用**: `/speckit.dsgs.context-optimization "内容" strategies="clarity,completeness"`

## 🚀 AI CLI环境专业使用指南

### 专业开发场景

#### 场景1: 需求分析与优化
```
用户: "分析这个需求：需要一个电商系统，支持用户购买功能"
AI: (自动识别为分析意图)
AI: /speckit.dsgs.context-analysis "需要一个电商系统，支持用户购买功能"
AI: (返回)
  清晰度: 0.5 ⚠️ (建议明确验证方式)
  相关性: 0.9 ✅ (高度相关)
  完整性: 0.4 ⚠️ (缺少约束条件)
  建议: 补充性能指标、安全要求、具体功能列表
```

#### 场景2: 代码审查与优化
```
用户: "帮我优化这段代码的性能"
用户: "def get_user(id): return db.get_user(id)"
AI: (自动识别为优化意图)
AI: /speckit.dsgs.context-optimization "def get_user(id): return db.get_user(id)" goals="performance,clarity"
AI: (返回优化建议)
```

#### 场景3: 架构设计助手
```
用户: "用设计模式分析这个系统"
用户: "订单管理系统，需要支持多种支付方式"
AI: (自动应用认知模板)
AI: /speckit.dsgs.cognitive-template "订单管理系统，需要支持多种支付方式" template=understanding
AI: (返回结构化分析)
```

### 企业级使用场景

#### 场景A: 项目启动阶段
```
AI CLI: 
# 1. 需求质量评估
/speckit.dsgs.context-analysis "项目需求文档内容"

# 2. 生成项目结构
/speckit.dsgs.modulizer "项目需求"

# 3. 生成系统约束
/speckit.dsgs.constraint-generator "项目需求"

# 4. 创建开发代理
/speckit.dsgs.agent-creator "针对项目需求的开发代理"
```

#### 场景B: 代码开发阶段
```
AI CLI: 
# 1. 安全工作区创建
/speckit.dsgs.temp-workspace "operation=create-workspace"

# 2. 代码分析
/speckit.dsgs.context-analysis "代码片段"

# 3. 任务分解
/speckit.dsgs.task-decomposer "复杂功能实现"

# 4. 代码优化
/speckit.dsgs.context-optimization "代码片段" goals="clarity,performance"

# 5. 提交验证
/speckit.dsgs.temp-workspace "operation=confirm-file file=code.py"
/speckit.dsgs.git-skill "operation=commit message='功能实现'"
```

## 🎨 特色功能亮点

### 1. AI原生智能
- 不依赖本地模型，完全利用AI模型原生能力
- 智能指令构造和响应解析
- 持续受益于AI模型升级

### 2. 专业上下文工程
- 五维质量分析框架
- 多目标优化策略
- 认知模板结构化思维

### 3. AI安全工作流
- 临时工作区隔离机制
- 多层验证流程
- 自动清理保护

### 4. 透明化交互
- 自然语言意图识别
- 简化命令映射
- 智能错误纠正

### 5. 企业级功能
- Agentic代理设计
- 任务分解与跟踪
- 项目结构智能生成
- 约束条件自动生成

## 📝 使用技巧

### 提示1: 最佳实践模式
- **分析前先优化**: 先用`context-optimization`优化需求，再用`context-analysis`分析
- **模板辅助**: 复杂任务使用`cognitive-template`应用认知框架
- **安全流程**: AI生成内容始终先放入临时工作区验证

### 提示2: 高效工作流
```
1. 需求澄清: /speckit.dsgs.context-analysis "需求"
2. 需求优化: /speckit.dsgs.context-optimization "需求" 
3. 架构设计: /speckit.dsgs.architect "需求"
4. 任务分解: /speckit.dsgs.task-decomposer "架构"
5. 开发支持: 按需使用其他技能
```

### 提示3: 专业模式
- 对于复杂项目，使用`agent-creator`创建专用智能代理
- 利用`modulizer`进行架构级别的模块化设计
- 使用`constraint-generator`提前定义系统边界

这份功能详解手册提供了DSGS Context Engineering Skills在AI CLI环境中的完整使用指南，涵盖了从基础功能到高级专业功能的所有特性。用户可以根据具体需求选择合适的技能和组合使用。