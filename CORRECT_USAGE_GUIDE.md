# ⚠️ 重要更正：DNASPEC 正确使用方式

## 错误的命令格式（不要使用）

❌ **错误**: `dnaspec slash <技能名> [参数]`
❌ **错误**: `dnaspec agent-creator "任务"`
❌ **错误**: `dnaspec task-decomposer "任务"`

这些命令格式是**错误的**，不会正确执行技能。

---

## 正确的使用方式

### 1. CLI命令（命令行工具）

CLI 用于部署和管理技能，不是直接执行技能：

```bash
# 查看版本
dnaspec --version

# 查看帮助
dnaspec --help

# 列出所有可用技能
dnaspec list

# 部署技能到AI编辑器
dnaspec deploy

# 验证安装
dnaspec validate

# 集成到平台
dnaspec integrate --platform <platform-name>
```

### 2. 在AI编辑器中使用技能

**正确的方式**：在支持的AI编辑器中使用 Slash 命令格式：

```bash
# Claude, Cursor, Qwen, IFLOW 等编辑器
/dnaspec.agent-creator "创建AI智能体"

/dnaspec.task-decomposer "分解复杂任务"

/dnaspec.constraint-generator "生成系统约束"

/dnaspec.system-architect "设计系统架构"

/dnaspec.context-analysis "分析这段文本"
```

### 3. 部署步骤

**完整的部署流程**：

```bash
# 步骤1: 安装DNASPEC
npm install -g dnaspec

# 步骤2: 验证安装
dnaspec --version
dnaspec list

# 步骤3: 部署到AI编辑器
dnaspec deploy

# 步骤4: 在AI编辑器中使用
# 打开 Claude/Cursor/Qwen，输入:
/dnaspec.agent-creator "创建数据分析专家"
```

---

## 支持的AI编辑器

| 平台 | Slash命令格式 | 状态 |
|------|--------------|------|
| **Claude** | `/dnaspec.agent-creator` | ✅ 支持 |
| **Cursor** | `/dnaspec.agent-creator` | ✅ 支持 |
| **Qwen** | `/dnaspec.agent-creator` | ✅ 支持 |
| **IFLOW** | `/dnaspec.agent-creator` | ✅ 支持 |
| **CodeBuddy** | `/dnaspec.agent-creator` | ✅ 支持 |
| **QoderCLI** | `/dnaspec.agent-creator` | ✅ 支持 |

---

## 常见错误和纠正

### 错误1: 使用CLI直接执行技能

❌ **错误**:
```bash
dnaspec agent-creator "创建智能体"
```

✅ **正确**:
```bash
# CLI: 部署技能
dnaspec deploy

# 然后在AI编辑器中使用
/dnaspec.agent-creator "创建智能体"
```

### 错误2: 使用slash命令

❌ **错误**:
```bash
dnaspec slash agent-creator "创建智能体"
```

✅ **正确**:
```bash
# CLI: 列出技能
dnaspec list

# 然后在AI编辑器中使用
/dnaspec.agent-creator "创建智能体"
```

### 错误3: 期望CLI输出技能执行结果

❌ **错误期望**:
```bash
dnaspec task-decomposer "分解任务"
# 期望: 输出任务分解结果
```

✅ **正确理解**:
```bash
# CLI命令用于管理，不直接执行技能
dnaspec list      # 查看有哪些技能
dnaspec deploy    # 部署技能到编辑器

# 技能执行在AI编辑器中进行
```

---

## 可用的DNASPEC技能

### 智能体创建
```bash
/dnaspec.agent-creator "创建数据分析专家"
```

### 任务管理
```bash
/dnaspec.task-decomposer "分解项目任务"
```

### 约束管理
```bash
/dnaspec.constraint-generator "生成性能约束"
```

### 架构设计
```bash
/dnaspec.system-architect "设计微服务架构"
/dnaspec.simple-architect "设计简单架构"
```

### 上下文工程
```bash
/dnaspec.context-analysis "分析文本上下文"
/dnaspec.context-optimization "优化上下文"
/dnaspec.cognitive-template "应用认知框架"
```

### 开发工具
```bash
/dnaspec.modulizer "模块化代码"
/dnaspec.git-operations "Git操作"
/dnaspec.temp-workspace "创建工作区"
```

### 质量保证
```bash
/dnaspec.api-checker "检查API设计"
```

---

## 技术说明

### 为什么不能通过CLI直接执行技能？

DNASPEC 技能是设计为在 **AI 编辑器环境**中运行的 Slash 命令，它们需要：

1. **AI上下文**: 技能需要与AI模型交互，处理上下文
2. **编辑器集成**: 技能利用编辑器的API和功能
3. **实时交互**: 技能需要与用户的编辑会话实时交互

CLI 工具（`dnaspec`）的作用是：
- ✅ 管理技能文件
- ✅ 部署到AI编辑器
- ✅ 验证安装
- ❌ **不直接执行技能**（因为缺少AI环境）

### Slash命令的两种格式

**格式1: dnaspec前缀**（推荐）
```bash
/dnaspec.agent-creator "创建智能体"
/dnaspec.task-decomposer "分解任务"
```

**格式2: speckit前缀**（兼容）
```bash
/speckit.dnaspec.agent-creator "创建智能体"
/speckit.dnaspec.task-decomposer "分解任务"
```

两种格式等效，第一种更简洁。

---

## 快速参考

| 任务 | 命令 | 位置 |
|------|------|------|
| 查看技能列表 | `dnaspec list` | CLI |
| 部署技能 | `dnaspec deploy` | CLI |
| 验证安装 | `dnaspec validate` | CLI |
| 执行技能 | `/dnaspec.xxx "任务"` | AI编辑器 |
| 查看版本 | `dnaspec --version` | CLI |
| 查看帮助 | `dnaspec --help` | CLI |

---

## 需要帮助？

- **完整文档**: README_MAIN.md
- **部署指南**: DEPLOYMENT_GUIDE.md
- **故障排除**: TROUBLESHOOTING.md
- **GitHub Issues**: https://github.com/ptreezh/dnaSpec/issues

---

**版本**: v2.0.5
**更新日期**: 2025-12-26
**状态**: ✅ 准确信息
