# DNASPEC 用户使用手册

## 目录

1. [快速入门](#快速入门)
2. [基础使用](#基础使用)
3. [核心技能详解](#核心技能详解)
4. [记忆系统使用](#记忆系统使用)
5. [高级功能](#高级功能)
6. [最佳实践](#最佳实践)
7. [常见问题](#常见问题)

---

## 快速入门

### 5分钟上手

```bash
# 1. 安装 DNASPEC
npm install -g dnaspec

# 2. 验证安装
dnaspec --version

# 3. 查看可用技能
dnaspec list

# 4. 部署到AI编辑器
dnaspec deploy

# 5. 在AI编辑器中使用第一个技能
# 打开 Claude/Cursor/Qwen，输入:
/dnaspec.agent-creator "创建一个Python开发助手"

---

## 基础使用

### CLI命令结构

DNASPEC CLI 用于部署和管理技能，不是直接执行技能。

```bash
dnaspec <command> [options]

### 常用CLI命令

```bash
# 查看全局帮助
dnaspec --help

# 列出所有技能
dnaspec list

# 部署到AI编辑器
dnaspec deploy

# 验证安装
dnaspec validate

### 在AI编辑器中使用技能

**重要**: 技能通过 Slash 命令在AI编辑器中使用

```bash
# 1. 创建智能体（在AI编辑器中）
/dnaspec.agent-creator "创建数据分析师"

# 2. 分解任务（在AI编辑器中）
/dnaspec.task-decomposer "实现用户登录功能"

# 3. 生成约束（在AI编辑器中）
/dnaspec.constraint-generator "系统需要支持万并发"

**支持的平台**: Claude, Cursor, Qwen, IFLOW, CodeBuddy 等

---

## 核心技能详解

### 1. Agent Creator（智能体创建器）

#### 功能说明
创建具有特定角色、能力和指令的 AI 智能体。

#### 使用方法

**在AI编辑器中使用**:
```bash
# 基础用法
/dnaspec.agent-creator "创建一个代码审查专家"

# 详细用法
/dnaspec.agent-creator "创建一个网络安全专家，具备漏洞扫描、安全审计和渗透测试能力"

#### CLI管理命令

```bash
# 部署此技能到AI编辑器
dnaspec deploy

# 验证技能可用
dnaspec list

#### 参数说明

| 参数 | 说明 | 必需 | 示例 |
|------|------|------|------|
| `role` | 智能体角色描述 | 是 | "数据分析师" |
| `domain` | 专业领域 | 否 | "金融" |
| `capabilities` | 能力列表 | 否 | "分析,报告,可视化" |
| `personality` | 人格类型 | 否 | "professional_precise" |

#### 人格类型选项

- `professional_precise` - 专业精确型
- `friendly_supportive` - 友好支持型
- `analytical_critical` - 分析批判型
- `creative_innovative` - 创新思维型
- `direct_efficient` - 直接高效型

#### 输出示例

```json
{
  "agent_config": {
    "id": "agent_abc123",
    "role": "代码审查专家",
    "domain": "software_development",
    "capabilities": [
      "Code review",
      "Security analysis",
      "Best practices"
    ],
    "instructions": "你是代码审查专家...",
    "interaction_guidelines": [
      "保持批判性思考",
      "关注安全和性能"
    ]
  },
  "quality_metrics": {
    "overall_quality": 0.85,
    "effectiveness": 0.9
  }
}

---

### 2. Task Decomposer（任务分解器）

#### 功能说明
将复杂任务分解为可管理的子任务，支持多种分解方法。

#### 使用方法

**在AI编辑器中使用**:
```bash
# 基础用法
/dnaspec.task-decomposer "开发一个电商平台"

# 详细用法（在Slash命令中描述需求）
/dnaspec.task-decomposer "使用层次化方法，最大深度3，分解电商平台的前端和后端开发任务"

#### 参数说明

| 参数 | 说明 | 必需 | 选项 |
|------|------|------|------|
| `method` | 分解方法 | 否 | `hierarchical`, `sequential`, `parallel`, `hybrid` |
| `max_depth` | 最大深度 | 否 | 1-10，默认3 |
| `complexity` | 复杂度目标 | 否 | `simple`, `medium`, `complex` |

#### 分解方法详解

**在AI编辑器中指定分解方法**:

```bash
# 1. Hierarchical（层次分解）
/dnaspec.task-decomposer "使用层次化方法构建系统，包括前端、后端和测试"

# 2. Sequential（顺序分解）
/dnaspec.task-decomposer "使用顺序分解方法设计用户注册流程：信息收集、验证、创建、欢迎"

# 3. Parallel（并行分解）
/dnaspec.task-decomposer "使用并行分解方法开发多个模块：A、B、C、D模块同时开发"

# 4. Hybrid（混合分解）
/dnaspec.task-decomposer "使用混合分解方法，结合层次和并行方式开发项目"
**4. Hybrid（混合分解）**
结合多种方法，适用于复杂项目。

---

### 3. Constraint Generator（约束生成器）

#### 功能说明
为系统自动生成和验证约束条件，包括性能、安全、可扩展性等维度。

#### 使用方法

**基础用法**:
```bash
/dnaspec.constraint-generator "系统需要支持10万并发用户"

**详细用法**:
```bash
/dnaspec.constraint-generator \
  --types "performance,security" \
  --priority "high" \
  --target "api-system"

#### 约束类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `performance` | 性能约束 | "响应时间 < 200ms" |
| `security` | 安全约束 | "必须使用HTTPS" |
| `scalability` | 可扩展性约束 | "支持水平扩展" |
| `reliability` | 可靠性约束 | "可用性 99.9%" |
| `compliance` | 合规性约束 | "符合GDPR" |

#### 输出示例

```json
{
  "constraints": [
    {
      "id": "constraint_001",
      "type": "performance",
      "description": "API响应时间必须小于200ms",
      "priority": "high",
      "metric": "response_time",
      "threshold": 200,
      "unit": "ms"
    },
    {
      "id": "constraint_002",
      "type": "security",
      "description": "所有通信必须使用HTTPS",
      "priority": "critical",
      "validation_method": "automated"
    }
  ],
  "validation_result": {
    "total_constraints": 2,
    "critical_count": 1,
    "high_count": 1,
    "consistency_score": 1.0
  }
}

---

## 记忆系统使用

### ⚠️ 重要说明

记忆系统是一个**简单的日志和检索系统**，不是 AI 学习系统。

### 适用场景

✅ **适合**:
- 项目日志记录
- 简单知识库
- 历史记录查询

❌ **不适合**:
- 期望技能"学习改进"
- 需要语义理解
- 大规模生产环境

### 初始化记忆系统

```bash
# 1. 运行初始化脚本
python scripts/setup_memory.py

# 2. 编辑配置文件
# config/memory_config.json
{
  "skills": {
    "task-decomposer": {
      "enabled": true,
      "max_short_term": 50,
      "max_long_term": 200
    }
  }
}

# 3. 运行示例
python examples/ci_project_helper.py

### 代码示例

```python
from dna_context_engineering.memory import MemoryManager, MemoryConfig

# 创建记忆管理器
config = MemoryConfig(enabled=True)
memory = MemoryManager(config)

# 添加记忆
memory.add_memory(
    agent_id="project-alpha",
    content="架构决策: 使用微服务",
    importance="HIGH"
)

# 检索记忆
memories = memory.recall_memories("project-alpha", "架构")

### 监控和维护

```bash
# 查看状态
python scripts/monitor_memory.py

# 备份记忆
python scripts/backup_memory.py

# 快速统计
python scripts/monitor_memory.py --quick

详细说明: `MEMORY_SYSTEM_HONEST_ANALYSIS.md`

---

## 高级功能

### 1. 技能链式调用

```bash
# 先创建智能体，再分解任务
/dnaspec.agent-creator "创建项目管理员" | \
/dnaspec.task-decomposer --method hierarchical

### 2. 配置文件

创建 `~/.dnaspec/config.json`:

```json
{
  "default_skill": "agent-creator",
  "output_format": "json",
  "log_level": "info",
  "memory_enabled": false
}

### 3. 环境变量

```bash
export DNASPEC_MEMORY_PATH=/custom/path
export DNASPEC_LOG_LEVEL=debug
export DNASPEC_DEFAULT_PLATFORM=claude

### 4. 多技能协作

在AI编辑器中，您可以连续使用多个技能来完成任务：

```bash
# 第1步：创建智能体
/dnaspec.agent-creator "创建项目管理员"

# 第2步：分解任务  
/dnaspec.task-decomposer "分解项目任务"

# 第3步：生成约束
/dnaspec.constraint-generator "生成系统约束"
```

**提示**: 技能结果会在AI编辑器中显示，您可以基于前一个技能的结果继续使用下一个技能。

## 最佳实践

### 1. 项目规划工作流

```bash
# 步骤1: 创建项目智能体
/dnaspec.agent-creator "创建系统架构师" # 在AI编辑器中执行

# 步骤2: 分解项目任务
/dnaspec.task-decomposer "设计微服务架构" # 在AI编辑器中执行

# 步骤3: 生成约束
/dnaspec.constraint-generator "支持10万并发" # 在AI编辑器中执行

# 步骤4: 查看和整合结果
cat architect.json tasks.json constraints.json

### 2. 代码审查工作流

**在AI编辑器中**:

```bash
# 创建审查智能体
/dnaspec.agent-creator "创建代码审查专家，具备安全审查、性能审查和规范检查能力"

# 分解审查任务
/dnaspec.task-decomposer "使用层次化方法分解支付模块代码审查任务"
```

### 3. 文档生成工作流

**在AI编辑器中**:

```bash
# 创建文档专家
/dnaspec.agent-creator "创建技术文档专家，负责API文档、架构文档和用户手册编写"

# 分解文档任务
/dnaspec.task-decomposer "分解API参考文档编写任务"
```

---

## 常见问题

### Q1: 安装后命令不识别？

**A**: 检查 Node.js 版本和 npm 全局路径：

```bash
# 检查版本
node --version  # 应该 >= 14.0.0
npm --version

# 查看全局安装路径
npm config get prefix

# 添加到 PATH（如果需要）
export PATH=$PATH:$(npm config get prefix)/bin

### Q2: 技能执行失败？

**A**: 检查：

```bash
# 1. 查看技能信息
dnaspec info <skill-name>

# 2. 检查Python环境
python --version  # 应该 >= 3.8

# 3. 查看日志
dnaspec <skill-name> --debug

### Q3: 记忆系统占用空间过大？

**A**: 清理记忆：

```bash
# 监控记忆大小
python scripts/monitor_memory.py

# 如果 > 500MB，建议清理
# 方法1: 删除记忆文件
rm -rf memory_storage/agents/*

# 方法2: 调整配置降低上限
# 编辑 config/memory_config.json

### Q4: 如何在代码中使用？

**A**: Python API 示例：

```python
from skills.agent_creator.skill import agent_creator_skill

# 创建智能体
result = agent_creator_skill.execute_skill({
    'agent_description': '创建数据分析师'
})

# 访问结果
config = result['agent_config']
print(config['role'])
print(config['capabilities'])

### Q5: 如何开发自定义技能？

**A**: 参考技能开发指南：

```bash
# 1. 使用技能模板
dnaspec skill-template my-skill

# 2. 编辑技能文件
# skills/my-skill/SKILL.md
# skills/my-skill/skill.py

# 3. 测试技能
dnaspec my-skill "测试任务"

---

## 附录

### A. 完整技能列表

详见 `dnaspec list` 或查看 `skills/` 目录。

### B. 退出码

| 代码 | 含义 |
|------|------|
| 0 | 成功 |
| 1 | 一般错误 |
| 2 | 输入验证失败 |
| 3 | 技能执行失败 |
| 4 | 配置错误 |

### C. 相关资源

- **项目仓库**: [GitHub](https://github.com/your-repo/dnaspec)
- **文档站点**: [docs.dnaspec.dev](https://docs.dnaspec.dev)
- **API 文档**: [API Reference](API_REFERENCE.md)
- **更新日志**: [CHANGELOG.md](CHANGELOG.md)

---

**手册版本**: v2.0.5
**最后更新**: 2025-12-26
