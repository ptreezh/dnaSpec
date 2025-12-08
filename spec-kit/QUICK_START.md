# spec.kit 快捷方式和帮助系统

## 概述

本系统为spec.kit提供更友好的用户交互界面，包括：
1. 简化命令别名/快捷方式
2. 内联帮助系统
3. 使用示例和最佳实践

## 快捷方式映射

### 核心spec.kit技能快捷方式
- `/speckit.specify` → `/spec` - 规格创建
- `/speckit.plan` → `/plan` - 规划
- `/speckit.tasks` → `/tasks` - 任务分解
- `/speckit.implement` → `/impl` - 实施
- `/speckit.constitution` → `/const` - 项目宪法

### Context Engineering 快捷方式
- `/context-analysis` → `/ca` - 上下文分析
- `/context-optimization` → `/co` - 上下文优化
- `/cognitive-template` → `/ct` - 认知模板
- `/context-analysis-enhanced` → `/cae` - 增强上下文分析
- `/context-optimization-enhanced` → `/coe` - 增强上下文优化
- `/cognitive-template-enhanced` → `/cte` - 增强认知模板
- `/context-engineering-workflow` → `/cew` - 上下文工程工作流

### DNASPEC 快捷方式
- `/dnaspec-architect` → `/da` - DNASPEC架构师
- `/dnaspec-system-architect` → `/dsa` - DNASPEC系统架构师
- `/dnaspec-agent-creator` → `/dac` - DNASPEC智能体创建器
- `/dnaspec-constraint-generator` → `/dcg` - DNASPEC约束生成器
- `/dnaspec-task-decomposer` → `/dtd` - DNASPEC任务分解器
- `/dnaspec-modulizer` → `/dm` - DNASPEC模块化验证器
- `/dnaspec-dapi-checker` → `/ddc` - DNASPEC接口检查器

## 帮助命令

### 通用帮助
- `/speckit.help` - 显示所有spec.kit命令帮助
- `/speckit.list` - 列出所有可用命令

### 分类帮助
- `/speckit.core` - 核心spec.kit帮助
- `/speckit.context` - 上下文工程帮助
- `/speckit.dnaspec` - DNASPEC技能帮助

## 详细帮助提示词

### Core Spec-Driven Skills
- **/spec** - `/spec [需求描述]` - 将需求转换为详细规格，专注于"什么"和"为什么"
- **/plan** - `/plan [规格或需求]` - 为实现制定技术计划，包括技术栈选择
- **/tasks** - `/tasks [规格或计划]` - 将复杂需求分解为可执行的任务
- **/impl** - `/impl [任务描述]` - 基于规格和计划提供实施指导
- **/const** - `/const [项目类型或领域]` - 建立项目原则、编码标准和开发实践

### Context Engineering Skills
- **/ca** - `/ca [待分析上下文]` - 分析上下文质量，提供清晰度、相关性、完整性评分
- **/co** - `/co [待优化上下文]` - 基于特定目标优化上下文质量
- **/ct** - `/ct [模板名] [上下文]` - 应用认知模板进行结构化思考
- **/cae** - `/cae [待分析上下文]` - 使用Context Engineering方法的增强分析
- **/coe** - `/coe [待优化上下文]` - 使用Context Engineering方法的增强优化
- **/cew** - `/cew [待处理上下文]` - 完整的上下文工程工作流（分析→优化→认知增强）

### DNASPEC Skills
- **/da** - `/da [项目需求]` - 为复杂项目设计分层架构
- **/dsa** - `/dsa [系统需求]` - 设计系统架构，选择技术栈，定义模块划分
- **/dac** - `/dac [智能体需求]` - 创建和配置智能体，定义角色和行为
- **/dcg** - `/dcg [项目需求]` - 生成系统约束、API规范约束、数据约束
- **/dtd** - `/dtd [复杂需求]` - 将复杂需求分解为原子任务
- **/dm** - `/dm [系统组件]` - 自底向上进行模块成熟度检查和模块化封装
- **/ddc** - `/ddc [系统组件]` - 检查系统组件间接口一致性

## 使用最佳实践

### 新手指南
1. **项目启动**: `/const [项目类型]` → `/spec [需求]` → `/plan [规格]`
2. **任务管理**: `/tasks [计划]` → `/impl [任务]`
3. **质量检查**: `/ca [文档]` → `/co [文档]` 
4. **复杂系统**: `/da [需求]` → `/dtd [架构]`

### 高级用法
1. **完整上下文工程**: `/cew [内容]` - 一次性完成分析、优化、认知增强
2. **架构设计**: `/da [需求]` → `/dsa [架构]` → `/dcg [架构]`
3. **智能体系统**: `/dac [需求]` → `/dnaspec-task-decomposer [智能体任务]`