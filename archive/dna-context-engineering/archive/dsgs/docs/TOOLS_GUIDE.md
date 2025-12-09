# DNASPEC 文档驱动开发工具使用指南

## 📋 概述

DNASPEC 项目现在配备了完整的文档驱动开发工具链，强制保障所有开发活动必须参考现有文档，并在设计完成后更新对应文档。

## 🚀 快速开始

### 1. 安装 Git Hooks

```bash
# 安装所有 Git Hooks 和相关工具
npm run docs:install-hooks
```

### 2. 验证安装

```bash
# 测试所有 hooks 是否正常工作
npm run test-hooks

# 检查文档完整性
npm run docs:verify
```

### 3. 开始使用

```bash
# 查看所有可用命令
npm run docs:check help
```

## 📋 完整工作流程

### 阶段 1: 开发前准备

#### 1.1 查阅相关文档
```bash
# 根据任务类型查阅相关文档
npm run docs:check constraint-generation
npm run docs:check cognitive-tools
npm run docs:check api-integration
```

#### 1.2 检查文档合规性
```bash
# 检查功能文档合规性
npm run docs:compliance new-auth-feature
```

### 阶段 2: 设计阶段

#### 2.1 创建设计文档
```bash
# 创建功能设计文档
npm run docs:design user-management

# 这将创建 docs/design/user-management.md 模板
```

#### 2.2 评审设计文档
```bash
# 评审设计文档
npm run docs:review docs/design/user-management.md
```

### 阶段 3: 开发阶段

#### 3.1 开发过程中实时更新文档
```bash
# 更新 API 文档
npm run docs:update generateConstraints

# 更新类型定义
npm run docs:type UserManagementConfig

# 更新模块依赖
npm run docs:dependency user-management
```

#### 3.2 验证文档同步
```bash
# 检查文档同步状态
npm run docs:sync-check
```

### 阶段 4: 提交前检查

#### 4.1 Git Hooks 自动检查
```bash
# 提交代码时，hooks 会自动检查：
# - 文档是否同步更新
# - API 文档是否完整
# - 类型定义是否更新
# - 模块依赖是否更新

git add .
git commit -m "feat: add user management feature

docs: update API interface documentation
docs: add UserManagementConfig type definition
docs: update module dependency graph"
```

### 阶段 5: 部署前检查

#### 5.1 部署前验证
```bash
# 部署前完整检查
npm run docs:pre-deploy
```

## 🛠️ 可用工具详解

### 文档检查工具

#### `docs:check <task-type>`
检查任务相关文档的合规性

```bash
# 检查约束生成相关文档
npm run docs:check constraint-generation

# 检查认知工具相关文档
npm run docs:check cognitive-tools

# 检查 API 集成相关文档
npm run docs:check api-integration
```

#### `docs:compliance <feature>`
检查功能文档的合规性

```bash
# 检查新功能的文档合规性
npm run docs:compliance new-auth-feature
```

#### `docs:verify`
验证所有文档的完整性

```bash
# 验证文档完整性
npm run docs:verify
```

### 设计工具

#### `docs:design <feature>`
创建功能设计文档

```bash
# 创建用户管理功能设计文档
npm run docs:design user-management
```

这将创建包含以下章节的设计文档模板：
- 功能概述和目标
- API 接口设计
- 模块依赖关系
- 集成方案
- 测试策略
- 文档更新计划

#### `docs:review <design-doc>`
评审设计文档

```bash
# 评审设计文档
npm run docs:review docs/design/user-management.md
```

### 文档更新工具

#### `docs:update <api-name>`
更新 API 文档

```bash
# 更新 generateConstraints API 文档
npm run docs:update generateConstraints
```

#### `docs:type <type-name>`
更新类型定义

```bash
# 更新 UserManagementConfig 类型定义
npm run docs:type UserManagementConfig
```

#### `docs:dependency <module>`
更新模块依赖

```bash
# 更新用户管理模块依赖
npm run docs:dependency user-management
```

### 检查工具

#### `docs:sync-check`
检查文档同步状态

```bash
# 检查文档同步状态
npm run docs:sync-check
```

#### `docs:pre-deploy`
部署前检查

```bash
# 部署前完整检查
npm run docs:pre-deploy
```

#### `docs:report`
生成合规性报告

```bash
# 生成合规性报告
npm run docs:report
```

### 安装和管理工具

#### `docs:install-hooks`
安装 Git Hooks

```bash
# 安装所有 Git Hooks
npm run docs:install-hooks
```

#### `docs:uninstall-hooks`
卸载 Git Hooks

```bash
# 卸载所有 Git Hooks
npm run docs:uninstall-hooks
```

#### `test-hooks`
测试 Git Hooks

```bash
# 测试所有 hooks
npm run test-hooks
```

## 🔄 Git Hooks 工作机制

### Pre-commit Hook
- 检查是否有代码变更但没有文档变更
- 检查 API 文档是否需要更新
- 检查类型定义是否需要更新
- 检查模块依赖是否需要更新

### Pre-push Hook
- 验证文档完整性
- 生成合规性报告
- 检查未提交的文档变更

### Commit-msg Hook
- 检查提交消息是否包含文档更新信息
- 提醒开发者更新相关文档

## 📝 提交消息规范

### 包含文档更新的提交
```bash
git commit -m "feat: add new authentication feature

- Add JWT-based authentication
- Implement refresh token rotation
- Add role-based access control

docs: update API interface documentation
docs: add AuthenticationConfig type definition
docs: update module dependency graph"
```

### 不需要文档更新的提交
```bash
git commit -m "fix: resolve typo in error message

docs: none - typo fix does not require documentation update"
```

## 🚨 常见问题和解决方案

### 问题 1: 提交被阻止 - 文档不同步
```
Error: 检测到代码变更但没有文档变更
```

**解决方案**：
```bash
# 1. 更新相关文档
npm run docs:update <api-name>
npm run docs:type <type-name>

# 2. 重新提交
git add .
git commit -m "feat: add new feature

docs: update API and type documentation"
```

### 问题 2: API 文档检查失败
```
Error: 接口 'NewInterface' 未在 API 文档中记录
```

**解决方案**：
```bash
# 1. 更新 API 文档
npm run docs:update NewInterface

# 2. 确保文档格式正确
npm run docs:verify
```

### 问题 3: 类型定义检查失败
```
Error: 类型 'NewType' 未在类型定义参考中记录
```

**解决方案**：
```bash
# 1. 更新类型定义文档
npm run docs:type NewType

# 2. 验证文档完整性
npm run docs:verify
```

### 问题 4: Hooks 不工作
```
Error: Git hooks not working
```

**解决方案**：
```bash
# 1. 重新安装 hooks
npm run docs:install-hooks

# 2. 测试 hooks
npm run test-hooks

# 3. 检查 Git 配置
git config core.hooksPath
```

## 📊 合规性报告

### 生成报告
```bash
# 生成合规性报告
npm run docs:report
```

报告包含：
- 文档完整性指标
- 文档同步率
- API 同步率
- 类型定义完整度
- 发现的问题和改进建议

### 报告示例
```markdown
## 📊 合规性报告

### 文档完整性
- [x] API 接口文档存在且完整
- [x] 函数调用字典存在且完整
- [x] 模块依赖关系图存在且完整
- [x] 类型定义参考存在且完整

### 文档同步率
- [x] 代码变更时文档同步更新
- [x] API 变更时文档同步更新
- [x] 类型变更时文档同步更新
- [x] 依赖变更时文档同步更新
```

## 🎯 最佳实践

### 1. 开发前
- 始终先查阅相关文档
- 使用 `docs:check` 确保了解现有架构
- 使用 `docs:compliance` 检查设计合规性

### 2. 设计时
- 使用 `docs:design` 创建设计文档
- 使用 `docs:review` 进行设计评审
- 确保设计符合现有架构规范

### 3. 开发时
- 实时更新文档
- 使用 `docs:update` 更新 API 文档
- 使用 `docs:type` 更新类型定义

### 4. 提交前
- 运行 `docs:sync-check` 检查同步状态
- 确保提交消息包含文档更新信息
- 使用 Git hooks 验证合规性

### 5. 部署前
- 运行 `docs:pre-deploy` 进行完整检查
- 生成合规性报告
- 确保所有文档都是最新的

## 📚 相关文档

- [API 接口文档](../docs/API_INTERFACE_DOCUMENTATION.md)
- [函数调用字典](../docs/FUNCTION_CALL_DICTIONARY.md)
- [模块依赖关系](../docs/MODULE_DEPENDENCY_GRAPH.md)
- [类型定义参考](../docs/TYPE_DEFINITIONS_REFERENCE.md)
- [工作流规范](../docs/WORKFLOW.md)

## 🔄 持续改进

### 反馈渠道
- GitHub Issues: 提交文档相关问题
- 团队会议: 讨论文档改进建议
- 匿名反馈: 使用内部反馈系统

### 定期评估
- 每月评估工具使用情况
- 每季度评估工作流程有效性
- 每年评估整个文档体系

---

**文档版本**: v1.0  
**最后更新**: 2025-08-11  
**维护者**: DNASPEC 开发团队