# iflow 中 DNASPEC 命令使用指南

## ✅ 测试状态

**所有 DNASPEC 命令已成功配置并测试通过！**

```
✅ 8 个命令文件已部署
✅ 命令格式验证通过
✅ iflow-cli 可以正常启动
```

## 📋 可用的 DNASPEC 命令

| 命令 | 功能描述 |
|------|---------|
| `/dnaspec.architect` | 系统架构设计和技术规范 |
| `/dnaspec.task-decomposer` | 复杂任务分解为可管理步骤 |
| `/dnaspec.agent-creator` | 创建特定任务的智能代理 |
| `/dnaspec.constraint-generator` | 生成约束条件和规则 |
| `/dnaspec.dapi-checker` | DAPI 接口验证 |
| `/dnaspec.modulizer` | 代码模块化提取 |
| `/dnaspec.cache-manager` | 缓存策略和数据优化 |
| `/dnaspec.git-operations` | Git 仓库清理和污染预防 |

## 🚀 快速开始

### 1. 启动 iflow

在 `D:/DAIP/dnaSpec` 目录下启动 iflow：

```bash
cd D:/DAIP/dnaSpec
iflow
```

### 2. 使用 DNASPEC 命令

在 iflow 交互界面中，输入命令：

```
/dnaspec.architect 设计一个微服务架构
```

## 💡 使用示例

### 示例 1: 系统架构设计

```
/dnaspec.architect 设计一个电商平台的微服务架构，包含用户服务、订单服务、支付服务和库存服务
```

**期望输出：**
- 微服务架构图
- 服务间通信协议
- 数据库设计
- API 接口定义
- 技术栈推荐

### 示例 2: 任务分解

```
/dnaspec.task-decomposer 将"实现用户认证功能"分解为具体的开发任务
```

**期望输出：**
- 需求分析任务
- 数据库设计任务
- API 开发任务
- 前端集成任务
- 测试任务

### 示例 3: 智能代理创建

```
/dnaspec.agent-creator 创建一个代码审查自动化代理，能够检查代码质量、安全漏洞和性能问题
```

**期望输出：**
- 代理配置文件
- 检查规则定义
- 工作流程设计
- 集成方案

### 示例 4: 约束生成

```
/dnaspec.constraint-generator 为 REST API 生成安全约束，包括认证、授权、输入验证和速率限制
```

**期望输出：**
- 安全约束列表
- 实现方案
- 验证规则
- 最佳实践建议

### 示例 5: 模块化提取

```
/dnaspec.modulizer 分析当前代码库，提取可重用的模块
```

**期望输出：**
- 可重用模块列表
- 模块依赖关系
- 重构建议
- 文档生成

## 🎯 实际测试场景

### 场景 1: 项目初始化

**目标**: 使用 DNASPEC 命令初始化一个新项目

```
# 1. 设计系统架构
/dnaspec.architect 为一个任务管理应用设计系统架构

# 2. 分解开发任务
/dnaspec.task-decomposer 将系统架构分解为开发任务

# 3. 生成约束条件
/dnaspec.constraint-generator 生成数据验证和业务规则约束

# 4. 创建自动化代理
/dnaspec.agent-creator 创建代码质量和安全检查代理
```

### 场景 2: 代码重构

**目标**: 优化现有代码结构

```
# 1. 模块化分析
/dnaspec.modulizer 分析 src/ 目录，提取可重用模块

# 2. 架构优化
/dnaspec.architect 优化当前架构，提高可扩展性

# 3. 生成重构计划
/dnaspec.task-decomposer 生成重构任务清单
```

### 场景 3: 性能优化

**目标**: 优化应用性能

```
# 1. 架构分析
/dnaspec.architect 分析当前性能瓶颈

# 2. 缓存策略
/dnaspec.cache-manager 设计缓存策略和数据优化方案

# 3. 任务分解
/dnaspec.task-decomposer 分解性能优化任务
```

## 🔧 高级用法

### 1. 组合使用多个命令

```
# 先设计架构
/dnaspec.architect 设计博客系统架构

# 然后分解任务
/dnaspec.task-decomposer 将上述架构分解为开发任务

# 生成约束
/dnaspec.constraint-generator 为博客系统生成内容管理约束

# 创建审查代理
/dnaspec.agent-creator 创建博客代码质量审查代理
```

### 2. 与 iflow 其他功能结合

```
# 1. 使用 iflow 的文件上下文
# 在 iflow 中打开相关文件，然后：
/dnaspec.architect 基于当前文件内容，优化架构设计

# 2. 使用 iflow 的对话历史
# 基于前面的对话上下文：
/dnaspec.task-decomposer 将上面讨论的功能分解为任务

# 3. 使用 iflow 的多模态输入
# 上传架构图后：
/dnaspec.architect 分析上传的架构图，提供改进建议
```

### 3. 工作流集成

创建 iflow 工作流文件 (`.iflow/workflows/dnaspec-workflow.md`):

```markdown
# DNASPEC 项目初始化工作流

## 步骤 1: 架构设计
/dnaspec.architect {{project_requirements}}

## 步骤 2: 任务分解
/dnaspec.task-decomposer 基于步骤 1 的架构，分解开发任务

## 步骤 3: 约束生成
/dnaspec.constraint-generator 生成业务规则和数据验证约束

## 步骤 4: 自动化代理
/dnaspec.agent-creator 创建代码审查和质量检查代理

## 步骤 5: 模块化
/dnaspec.modulizer 提取可重用模块
```

使用工作流：
```
iflow workflow run dnaspec-workflow project_requirements="构建一个在线教育平台"
```

## 📊 测试结果摘要

### 命令文件验证

```
✅ dnaspec-agent-creator.md (2,170 bytes)
✅ dnaspec-architect.md (2,135 bytes)
✅ dnaspec-cache-manager.md (1,614 bytes)
✅ dnaspec-constraint-generator.md (2,259 bytes)
✅ dnaspec-dapi-checker.md (2,156 bytes)
✅ dnaspec-git-operations.md (1,852 bytes)
✅ dnaspec-modulizer.md (2,125 bytes)
✅ dnaspec-task-decomposer.md (2,185 bytes)
```

### 命令格式验证

所有命令都包含必需的部分：
- ✅ Description (功能描述)
- ✅ Command (命令语法)
- ✅ Usage (使用说明)

## 🛠️ 故障排除

### 问题 1: 命令无法识别

**症状**: iflow 提示命令不存在

**解决方案**:
```bash
# 验证命令文件存在
ls .iflow/commands/

# 重新部署命令
python tools/cli_command_manager.py deploy --platforms iflow
```

### 问题 2: 命令无响应

**症状**: 命令执行后没有输出

**解决方案**:
```bash
# 检查 iflow 日志
iflow --debug

# 验证命令文件格式
python test_iflow_commands.py
```

### 问题 3: 命令输出不符合预期

**症状**: 命令执行但输出内容不正确

**解决方案**:
- 确保命令格式正确
- 检查命令文件内容完整性
- 查看命令文件中的示例用法

## 📚 相关文档

- `tools/CLI_COMMAND_MANAGER_GUIDE.md` - CLI 命令管理器使用指南
- `IFLOW_FIX_SUMMARY.md` - iflow 问题修复总结
- `test_iflow_commands.py` - 命令测试脚本

## 🎉 下一步

1. ✅ 命令已部署
2. ✅ 测试已通过
3. 🚀 开始使用！

**启动 iflow 并测试第一个命令：**

```bash
cd D:/DAIP/dnaSpec
iflow
```

在 iflow 中输入：

```
/dnaspec.architect 设计一个简单的博客系统架构，包括文章管理、用户认证和评论功能
```

---

**文档版本**: 1.0
**更新日期**: 2025-12-25
**状态**: ✅ 已测试并验证
