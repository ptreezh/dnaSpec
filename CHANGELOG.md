# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.5] - 2025-12-26

### 🎉 重要修复

**修复了所有文档和CLI工具中的错误命令格式**

### ✅ 修复内容

#### CLI工具修复
- ✅ 修复 `bin/dnaspec-cli.js` 显示正确的使用方式
- ✅ 当用户使用 `dnaspec slash` 时显示清晰警告
- ✅ `dnaspec list` 显示正确的Slash命令格式
- ✅ `dnaspec tips` 显示正确的部署和使用说明

#### 文档修复
- ✅ **README_MAIN.md** - 所有技能示例改为正确的Slash命令格式
- ✅ **USER_MANUAL.md** - 完整修复用户手册中的所有示例
- ✅ **DEPLOYMENT_GUIDE.md** - 更新部署指南和CI/CD示例
- ✅ **TROUBLESHOOTING.md** - 修复所有故障排除示例

#### 新增文档
- ✅ **CORRECT_USAGE_GUIDE.md** - 完整的正确使用指南
- ✅ **COMMAND_FORMAT_CLEANUP_REPORT.md** - 清理工作报告
- ✅ **FINAL_CLEANUP_REPORT.md** - 最终完成报告

### ⚠️ 重要变更

**错误的命令格式已移除**：
- ❌ `dnaspec slash <技能名>` - 不再支持
- ❌ `dnaspec agent-creator "任务"` - 不再支持
- ❌ `dnaspec task-decomposer "任务"` - 不再支持

**正确的使用方式**：
- ✅ CLI命令：`dnaspec list`, `dnaspec deploy`, `dnaspec validate`
- ✅ 在AI编辑器中：`/dnaspec.agent-creator`, `/dnaspec.task-decomposer`

### 📚 文档改进

- 明确区分CLI命令和AI编辑器Slash命令
- 所有技能示例使用正确的格式
- 添加完整的部署步骤说明
- 改进用户提示和错误信息

### 🐛 Bug修复

- 修复了用户可能被错误命令格式误导的问题
- 修复了文档中所有错误的技能调用示例
- 修复了CI/CD配置中的错误测试命令

### 💡 影响范围

- **现有用户**：CLI工具会显示正确提示，不影响现有部署
- **新用户**：不会被错误的命令格式误导
- **兼容性**：完全向后兼容，所有有效的CLI命令保持不变

---

## [2.0.4] - 2025-12-20

### 新增功能
- 双重部署系统（标准化 + Slash命令）
- 13种上下文工程技能
- 记忆系统集成（可选）
- 多平台支持（Claude, Cursor, Qwen等）

### 改进
- 优化CLI用户界面
- 增强技能执行性能
- 改进错误处理

---

## [2.0.0] - 2025-12-01

### 重大变更
- 完全重写的架构
- 新的技能系统
- 改进的部署机制

### 新增
- 13个核心技能
- 记忆系统
- 多平台支持

---

## 版本说明

### 版本格式

- **主版本（Major）**：如 2.0.0 - 重大功能变更，可能不兼容
- **次版本（Minor）**：如 2.1.0 - 新功能，向后兼容
- **补丁版本（Patch）**：如 2.0.5 - Bug修复和小改进

### 更新策略

- **补丁版本**：文档修复、Bug修复、小改进
- **次版本**：新功能、新技能、重要改进
- **主版本**：架构变更、不兼容的修改

---

## 链接

- **NPM包**: https://www.npmjs.com/package/dnaspec
- **GitHub**: https://github.com/dnaspec/dnaspec
- **文档**: https://docs.dnaspec.dev

---

**维护状态**: ✅ 积极维护
