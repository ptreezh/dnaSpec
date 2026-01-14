# DNASPEC 记忆系统 - 真实用途详解

## 记忆系统的两种用途

### 用途1: 技能记忆增强（技能学习历史经验）

**目的**: 让 DNASPEC 技能本身"记住"过去的执行经验，在后续使用中变得更聪明。

**实际含义**:
- `task-decomposer` 记住之前如何分解过类似的任务
- `architect` 记住之前设计过的架构模式
- 技能利用这些历史经验来优化后续执行

**适用场景**: 长期使用同一技能，希望技能积累经验

---

### 用途2: 项目记忆系统（为项目添加记忆）

**目的**: 为您的具体项目/系统添加持久化记忆能力。

**实际含义**:
- 您的应用程序可以"记住"用户交互、项目状态、历史决策
- 类似于给应用添加"大脑"，存储和检索重要信息
- 跨会话保持上下文

**适用场景**: 任何需要记忆功能的应用程序

---

## 具体示例对比

### 场景A: 技能记忆增强

```python
# 使用 task-decomposer 分解任务
from skills.task_decomposer.skill import task_decomposer_skill
from dna_context_engineering.memory import create_task_decomposer_with_memory

# 创建带记忆的分解器
decomposer = create_task_decomposer_with_memory(
    task_decomposer_skill,
    enable_memory=True
)

# 第一次使用：分解"用户认证系统"
result1 = decomposer.execute({
    'input': '实现用户认证系统',
    'decomposition_method': 'hierarchical'
})
# ✅ 技能记住了这个分解模式

# 第二次使用：分解类似的"权限管理系统"
result2 = decomposer.execute({
    'input': '实现权限管理系统',
    'decomposition_method': 'hierarchical'
})
# ✅ 技能会回忆起之前的"用户认证系统"分解经验
# ✅ 可能参考之前的模式来优化新的分解
```

**效果**: 技能越用越聪明，因为它记住了历史执行经验。

---

### 场景B: 项目记忆系统

```python
from dna_context_engineering.memory import MemoryManager, MemoryConfig

# 创建项目的记忆系统
config = MemoryConfig(enabled=True)
project_memory = MemoryManager(config)

# 项目执行中记录重要决策
project_memory.add_memory(
    agent_id="project-alpha",
    content="架构决策: 使用微服务架构",
    importance="HIGH"
)

# 记录用户反馈
project_memory.add_memory(
    agent_id="project-alpha",
    content="用户反馈: 需要添加实时通知功能",
    importance="MEDIUM"
)

# 记录技术选择
project_memory.add_memory(
    agent_id="project-alpha",
    content="技术栈: Node.js + PostgreSQL + Redis",
    importance="CRITICAL"
)

# 后续可以检索这些记忆
decisions = project_memory.recall_memories("project-alpha", "架构")
for decision in decisions:
    print(f"- {decision.content}")
# 输出:
# - 架构决策: 使用微服务架构
# - 技术栈: Node.js + PostgreSQL + Redis
```

**效果**: 项目有了持久化记忆，可以跨时间保持上下文。

---

## 实际应用场景

### 1. 软件开发助手（技能增强）

```python
# 任务：长期使用 task-decomposer 分解任务

# 第1天
decomposer.execute({'input': '设计用户登录模块'})
# 技能记住了这个分解模式

# 第7天
decomposer.execute({'input': '设计用户注册模块'})
# 技能回忆起登录模块的分解，参考它来分解注册模块

# 第30天
decomposer.execute({'input': '设计密码重置模块'})
# 技能已经积累了30个类似任务的分解经验
# 分解质量和一致性会提高
```

**价值**: 技能积累领域经验，执行越来越好

---

### 2. 智能客服系统（项目记忆）

```python
# 项目：客服AI系统

class CustomerServiceBot:
    def __init__(self):
        # 为这个客服系统添加记忆
        self.memory = MemoryManager(MemoryConfig(enabled=True))
        self.conversation_id = f"customer_{customer_phone}"

    def handle_complaint(self, complaint):
        # 记住客户投诉
        self.memory.add_memory(
            agent_id=self.conversation_id,
            content=f"客户投诉: {complaint}",
            importance="HIGH"
        )

        # 回忆这个客户的历史
        history = self.memory.recall_memories(
            self.conversation_id,
            "投诉"
        )

        # 根据历史经验处理
        return self.generate_response(history)

    def resolve_issue(self, solution):
        # 记住解决方案
        self.memory.add_memory(
            agent_id=self.conversation_id,
            content=f"解决方案: {solution}",
            importance="HIGH"
        )
```

**价值**:
- 记住每个客户的历史
- 提供个性化服务
- 积累解决方案知识库

---

### 3. 项目管理助手（混合使用）

```python
# 项目：管理一个长期项目

class ProjectManager:
    def __init__(self):
        # 1. 使用带记忆的规划技能
        self.planner = create_task_decomposer_with_memory(
            task_decomposer_skill,
            enable_memory=True
        )

        # 2. 为项目本身添加记忆
        self.project_memory = MemoryManager(MemoryConfig(enabled=True))
        self.project_id = "website-redesign-2024"

    def plan_phase(self, phase_description):
        # 技能层面：记住规划模式
        plan = self.planner.execute({
            'input': phase_description
        })

        # 项目层面：记住项目决策
        self.project_memory.add_memory(
            agent_id=self.project_id,
            content=f"阶段计划: {phase_description}",
            importance="HIGH"
        )

        return plan

    def make_decision(self, decision):
        # 记录重要决策
        self.project_memory.add_memory(
            agent_id=self.project_id,
            content=f"决策: {decision}",
            importance="CRITICAL"
        )

    def review_progress(self):
        # 回顾项目历史
        decisions = self.project_memory.recall_memories(
            self.project_id,
            "决策"
        )

        print(f"项目历史决策 ({len(decisions)} 条):")
        for decision in decisions:
            print(f"  - {decision.content}")
```

**价值**:
- 技能记住规划模式（提高规划质量）
- 项目记住决策历史（保持项目连贯性）

---

## 两个层次的关系

```
┌─────────────────────────────────────────────────────┐
│              您的应用程序                             │
│                                                       │
│  ┌─────────────────────────────────────────────┐   │
│  │    项目记忆（项目层面）                        │   │
│  │  - 记住项目决策                               │   │
│  │  - 记住用户交互                               │   │
│  │  - 记住业务规则                               │   │
│  └─────────────────────────────────────────────┘   │
│                       ▲                             │
│                       │ 使用                        │
│  ┌─────────────────────────────────────────────┐   │
│  │    DNASPEC 技能（工具层面）                   │   │
│  │                                              │   │
│  │  ┌──────────────────────────────────────┐  │   │
│  │  │  task-decomposer (带记忆)             │  │   │
│  │  │  - 记住任务分解模式                   │  │   │
│  │  │  - 学习优化分解策略                   │  │   │
│  │  └──────────────────────────────────────┘  │   │
│  │                                              │   │
│  │  ┌──────────────────────────────────────┐  │   │
│  │  │  architect (带记忆)                   │  │   │
│  │  │  - 记住架构设计模式                   │  │   │
│  │  │  - 学习优化设计方案                   │  │   │
│  │  └──────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────┘   │
│                                                       │
└─────────────────────────────────────────────────────┘
```

---

## 实际代码示例：智能代码审查系统

```python
from skills.task_decomposer.skill import task_decomposer_skill
from skills.architect.skill import architect_skill
from dna_context_engineering.memory import (
    create_task_decomposer_with_memory,
    create_architect_with_memory,
    MemoryManager
)

class CodeReviewSystem:
    """智能代码审查系统"""

    def __init__(self):
        # 1. 技能记忆 - 让技能记住审查经验
        self.task_analyzer = create_task_decomposer_with_memory(
            task_decomposer_skill,
            enable_memory=True
        )

        self.arch_analyzer = create_architect_with_memory(
            architect_skill,
            enable_memory=True
        )

        # 2. 项目记忆 - 记住每个项目的审查历史
        self.project_memory = MemoryManager(MemoryConfig(
            enabled=True,
            max_long_term=1000  # 保留大量历史
        ))

    def review_project(self, project_name: str, codebase_desc: str):
        """审查项目"""
        print(f"\n审查项目: {project_name}")

        # 技能层面：分析代码结构
        structure = self.task_analyzer.execute({
            'input': f'分析代码结构: {codebase_desc}'
        })

        architecture = self.arch_analyzer.execute({
            'input': f'评估架构: {codebase_desc}'
        })

        # 项目层面：记录这次审查
        self.project_memory.add_memory(
            agent_id=project_name,
            content=f"代码结构: {len(structure.get('subtasks', []))} 个模块",
            importance="MEDIUM"
        )

        self.project_memory.add_memory(
            agent_id=project_name,
            content=f"架构风格: {architecture.get('architecture_style', 'unknown')}",
            importance="MEDIUM"
        )

        # 回顾这个项目的历史审查
        history = self.project_memory.recall_memories(
            project_name,
            "审查"
        )

        print(f"历史审查记录: {len(history)} 条")

        return {
            'structure': structure,
            'architecture': architecture,
            'history': history
        }

    def record_issue(self, project_name: str, issue: str):
        """记录问题"""
        self.project_memory.add_memory(
            agent_id=project_name,
            content=f"问题: {issue}",
            importance="HIGH"
        )

    def record_fix(self, project_name: str, fix: str):
        """记录修复"""
        self.project_memory.add_memory(
            agent_id=project_name,
            content=f"修复: {fix}",
            importance="HIGH"
        )

# 使用示例
system = CodeReviewSystem()

# 审查第一个项目
system.review_project("ecommerce-api", "RESTful API for e-commerce")
system.record_issue("ecommerce-api", "缺少速率限制")
system.record_fix("ecommerce-api", "添加Redis限流")

# 审查第二个项目
system.review_project("user-service", "用户微服务")
system.record_issue("user-service", "认证逻辑重复")
system.record_fix("user-service", "提取共享认证库")

# 审查第一个项目的新版本（会记住历史）
system.review_project("ecommerce-api", "RESTful API v2")

# ✅ 技能层面：task_analyzer 和 arch_analyzer 记住了审查模式
# ✅ 项目层面：每个项目的审查历史都被保存
```

---

## 如何选择使用？

### 选择"技能记忆增强"当：

- ✅ 长期使用相同的 DNASPEC 技能
- ✅ 希望技能积累经验，执行越来越好
- ✅ 执行的任务有重复性模式
- ✅ 需要保持技能执行的一致性

**典型场景**:
- 持续集成系统（长期使用 task-decomposer）
- 架构设计团队（长期使用 architect）
- 代码审查系统（长期分解审查任务）

### 选择"项目记忆系统"当：

- ✅ 应用需要记住用户数据
- ✅ 需要跨会话保持状态
- ✅ 需要存储业务决策
- ✅ 需要个性化历史记录

**典型场景**:
- 智能客服系统
- 个人助理应用
- 项目管理系统
- 学习管理系统
- 推荐系统

### 两者结合使用当：

- ✅ 需要技能积累经验
- ✅ 同时需要项目级记忆
- ✅ 复杂的长期应用

**典型场景**:
- 企业知识管理系统
- 智能项目管理工具
- 开发团队协作平台

---

## 总结

**记忆系统不是单一功能，而是两层记忆能力**：

1. **技能层**: 让 DNASPEC 技能"学习"历史执行经验
2. **项目层**: 为您的应用添加持久化记忆功能

**您可以根据需求选择**：
- 只用技能层：让技能更聪明
- 只用项目层：给应用添加记忆
- 两者都用：智能+记忆

**关键区别**：
- 技能记忆：技能本身的能力增强（DNASPEC内部）
- 项目记忆：您应用的功能增强（您的项目）

需要我提供更多具体场景的示例吗？
