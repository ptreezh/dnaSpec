# spec.kit - 规格驱动开发工具包

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/ptreezh/spec-kit/graphs/commit-activity)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/ptreezh/spec-kit/pulls)

## 🚀 项目概述

**spec.kit** 是一个全面的"规格驱动开发"(Spec-Driven Development)工具包，它让规格成为开发的主要驱动力，而不是代码。该工具包标准化了规格、规划、任务分解和实施过程，并将它们集成到AI代理(如Claude Code、GitHub Copilot等)中，通过可执行的斜杠命令。

### 🎯 核心理念

- **规格先行**: 规格成为可执行的产物，直接生成工作实现
- **AI增强**: 利用AI代理的智能能力辅助开发全流程
- **标准化流程**: 将开发过程分解为标准化、可重复的步骤
- **渐进式展开**: 从原子技能到复合工作流的层次架构
- **多环境兼容**: 支持Claude Skills及其它AI CLI环境

## 📊 项目架构

```
spec-kit/
├── skills/                 # Claude Skills 实现
│   ├── speckit-specify/    # 规格创建
│   ├── speckit-plan/       # 技术规划
│   ├── speckit-tasks/      # 任务分解
│   ├── speckit-implement/  # 实施指导
│   ├── speckit-constitution/ # 项目宪法
│   ├── context-analysis/   # 上下文分析
│   ├── context-optimization/ # 上下文优化
│   ├── cognitive-template/ # 认知模板
│   ├── context-analysis-enhanced/ # 增强上下文分析
│   ├── context-optimization-enhanced/ # 增强上下文优化
│   ├── cognitive-template-enhanced/ # 增强认知模板
│   ├── dsgs-architect/     # DSGS架构师
│   ├── dsgs-system-architect/ # DSGS系统架构师
│   ├── dsgs-agent-creator/ # DSGS智能体创建器
│   ├── dsgs-constraint-generator/ # DSGS约束生成器
│   ├── dsgs-task-decomposer/ # DSGS任务分解器
│   ├── dsgs-modulizer/     # DSGS模块化验证器
│   └── dsgs-dapi-checker/  # DSGS接口检查器
├── scripts/                # Python脚本实现
│   ├── context_analyzer.py  # 上下文分析引擎
│   ├── context_optimizer.py # 上下文优化引擎
│   ├── task_decomposer.py   # 任务分解引擎
│   ├── constraint_generator.py # 约束生成引擎
│   ├── dapi_checker.py      # 接口检查引擎
│   ├── agent_creator.py     # 智能体创建引擎
│   ├── architect_coordinator.py # 架构协调引擎
│   ├── system_architect_designer.py # 系统架构设计引擎
│   └── modulizer.py         # 模块化验证引擎
├── docs/                   # 文档
├── commands/               # 其它AI CLI命令
├── tests/                  # 测试
├── README.md               # 项目说明
├── LICENSE                 # Apache 2.0许可证
├── CONTRIBUTING.md         # 贡献指南
└── CODE_OF_CONDUCT.md      # 行为准则
```

## ✨ 功能特性

### 1. 核心规格驱动功能 (5个技能)
- `/speckit.specify` - 规格创建，专注"什么"和"为什么"
- `/speckit.plan` - 技术规划，技术栈选择和架构决策
- `/speckit.tasks` - 任务分解，将规格拆分为可执行任务
- `/speckit.implement` - 实施指导，基于规格的实施建议
- `/speckit.constitution` - 项目宪法，建立开发标准

### 2. 上下文工程功能 (7个技能)
- `/context-analysis` - 基础上下文分析 (清晰度、相关性、完整性、一致性、效率)
- `/context-optimization` - 基础上下文优化 (基于特定目标)
- `/cognitive-template` - 认知模板应用 (链式思维、少样本学习、验证框架)
- `/context-analysis-enhanced` - 增强上下文分析 (Context Engineering方法)
- `/context-optimization-enhanced` - 增强上下文优化 (Context Engineering方法)
- `/cognitive-template-enhanced` - 增强认知模板 (Context Engineering方法)
- `/context-engineering-workflow` - 完整工作流 (分析→优化→认知增强)

### 3. DSGS智能架构师功能 (7个技能)
- `/dsgs-architect` - DSGS智能架构师 (复杂系统架构设计)
- `/dsgs-system-architect` - DSGS系统架构师 (系统架构设计和技栈选择)
- `/dsgs-agent-creator` - DSGS智能体创建器 (创建智能代理)
- `/dsgs-constraint-generator` - DSGS约束生成器 (生成系统约束)
- `/dsgs-task-decomposer` - DSGS任务分解器 (分解复杂需求)
- `/dsgs-modulizer` - DSGS模块化验证器 (模块成熟度检查)
- `/dsgs-dapi-checker` - DSGS接口检查器 (API一致性验证)

## 🛠️ 安装与使用

### 先决条件
- Claude Code 或支持Claude Skills的AI平台
- Python 3.8+ (用于脚本增强功能)

### 安装
1. **克隆仓库**
   ```bash
   git clone https://github.com/ptreezh/spec-kit.git
   ```

2. **配置Claude Skills** (如果支持)
   - 按照Claude平台的技能安装说明进行配置

3. **为其它AI环境配置命令**
   ```bash
   # 复到Claude命令目录
   cp -r commands/ ~/.claude/commands/
   ```

### 快速开始
```bash
# 1. 建立项目宪法
/speckit.constitution Web应用开发项目

# 2. 创建规格
/speckit.specify 用户需要能够注册、登录、浏览商品

# 3. 技术规划
/speckit.plan 电商平台技术实现

# 4. 任务分解
/speckit.tasks 电商平台开发任务

# 5. 开始实施
/speckit.implement 用户注册功能
```

### 内容工程工作流
```bash
# 分析内容质量
/context-analysis 这是需要分析的技术文档

# 优化内容质量
/context-optimization 这是需要优化的文档内容

# 完整上下文工程流程
/context-engineering-workflow 完整的文档内容
```

## 📚 使用示例

### 项目开发工作流
```bash
# 完整的规格驱动开发流程
/speckit.constitution [项目类型]
/speckit.specify [需求描述] 
/speckit.plan [规格内容]
/speckit.tasks [计划内容]
# 然后执行具体任务
```

### 系统设计工作流
```bash
# 系统架构设计流程
/dsgs-architect [系统需求]
/dsgs-task-decomposer [架构设计]
/dsgs-constraint-generator [系统约束]
```

### 内容优化工作流
```bash
# 内质量保证流程
/context-analysis [初始内容]
/context-optimization [优化后内容]
/context-analysis-enhanced [进一步分析]
/context-engineering-workflow [完整流程]
```

## 🔧 技术架构

### 渐进式展开架构
1. **原子技能层**: 专注单一功能的基础技能
2. **增强技能层**: 原子技能的增强版本
3. **领域技能层**: 特定领域的专业化技能  
4. **工作流技能层**: 多技能组合的复合流程

### 脚本增强功能
多个技能包含Python脚本支持，提供更精确的分析、计算和处理：
- `context_analyzer.py` - 定量分析引擎
- `task_decomposer.py` - 任务分解引擎
- `constraint_generator.py` - 约束生成引擎
- 等等

### 上下文工程集成
- **Token预算管理**: 优化模型token使用
- **记忆集成**: 支持长上下文窗口操作
- **推理架构**: 支持多步推理和验证

## 🤝 贡献

欢迎任何形式的贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细信息。

### 开发环境设置
```bash
# 克装依赖
pip install -r requirements.txt

# 运行测试
pytest tests/
```

## 📄 许可证

本项目使用 Apache 2.0 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 👥 维护者

- **作者**: ptreezh
- **邮箱**: 3061176@qq.com
- **机构**: AI人格实验室 (AI Persona Lab)
- **网站**: https://Agentpsy.com

## 🏢 机构信息

**AI人格实验室** (AI Persona Lab) 是一家致力于AI代理和人格化AI系统研究的实验室，专注于开发更智能、更人性化的AI工具和服务。

---

**spec.kit** - Transform specifications into executable implementations with AI assistance.