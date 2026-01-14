# DNASPEC Init 技能使用指南

## 🎯 技能概述

`dnaspec_init` 是DNASPEC项目协调机制的专门初始化和管理技能，它能够：

- ✅ **自动检测项目状态** - 智能识别项目类型和现有配置
- ✅ **初始化协调机制** - 创建项目宪法、配置和目录结构
- ✅ **管理项目配置** - 提供配置查看、修改和重置功能
- ✅ **支持多种项目类型** - Web应用、API服务、移动应用等
- ✅ **可扩展功能集** - 缓存、Git钩子、CI/CD、监控、安全

## 📋 安装和部署

### 方法1: 作为独立技能使用
```bash
# 复制技能文件到DNASPEC技能目录
cp spec-kit/skills/dna-dnaspec-init/scripts/* /path/to/your/dnaspec/skills/
```

### 方法2: 直接命令行使用
```bash
# 直接运行独立执行接口
python spec-kit/skills/dna-dnaspec-init/scripts/dnaspec_init.py --help
```

### 方法3: 在现有技能系统中使用
```bash
# 作为技能调用
/dnaspec.dnaspec-init "operation=init-project"
```

## 🚀 核心功能

### 1. 项目初始化

#### 基础初始化
```bash
# 使用默认设置初始化项目
/dnaspec.dnaspec-init "operation=init-project"

# 指定项目类型
/dnaspec.dnaspec-init "operation=init-project project_type=web_application"

# 指定初始化类型
/dnaspec.dnaspec-init "operation=init-project init_type=team"
```

#### 高级初始化
```bash
# 启用特定功能
/dnaspec.dnaspec-init "operation=init-project features=caching,git_hooks,ci_cd"

# 使用模板
/dnaspec.dnaspec-init "operation=init-project template=react_enterprise"

# 强制重新初始化
/dnaspec.dnaspec-init "operation=init-project force=true"
```

### 2. 项目状态检测

#### 快速检测
```bash
# 检测项目当前状态
/dnaspec.dnaspec-init "operation=detect"

# 获取详细状态报告
/dnaspec.dnaspec-init "operation=status"
```

#### 状态输出示例
```
✅ 项目状态: complete

✅ 已存在文件 (4):
   - PROJECT_CONSTITUTION.md
   - .dnaspec/config.json
   - .dnaspec/cache
   - .dnaspec/meta

🔍 检测到的项目特征:
   🏷️ 编程语言: javascript, python
   🛠️ 开发工具: ci_cd
```

### 3. 配置管理

#### 查看配置
```bash
# 获取当前配置信息
/dnaspec.dnaspec-init "operation=get-config"

# JSON格式输出
/dnaspec.dnaspec-init "operation=get-config output_format=json"
```

#### 重置配置
```bash
# 重置协调机制（需要确认）
/dnaspec.dnaspec-init "operation=reset confirm=true"

# 带备份的重置
/dnaspec.dnaspec-init "operation=reset confirm=true backup=true"
```

### 4. 升级和维护

#### 升级协调机制
```bash
# 升级到最新版本
/dnaspec.dnaspec-init "operation=upgrade"

# 强制升级
/dnaspec.dnaspec-init "operation=upgrade force=true"
```

## 🎛️ 详细参数说明

### 初始化参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `operation` | string | required | 操作类型 |
| `init_type` | string | "auto" | 初始化类型 |
| `project_type` | string | "generic" | 项目类型 |
| `features` | list | [] | 启用功能列表 |
| `force` | boolean | false | 强制重新初始化 |
| `template` | string | null | 初始化模板 |

### 初始化类型

- **project**: 标准项目初始化
- **team**: 团队协作项目初始化
- **enterprise**: 企业级项目初始化
- **solo**: 个人项目初始化
- **auto**: 自动检测并初始化

### 项目类型

- **web_application**: Web应用项目
- **mobile_app**: 移动应用项目
- **api_service**: API服务项目
- **desktop_app**: 桌面应用项目
- **library**: 库/框架项目
- **microservice**: 微服务项目
- **data_science**: 数据科学项目
- **ml_project**: 机器学习项目
- **generic**: 通用项目

### 功能特性

- **caching**: 启用缓存系统
- **git_hooks**: 配置Git钩子
- **ci_cd**: 生成CI/CD模板
- **monitoring**: 启用监控系统
- **security**: 启用安全配置

## 📊 输出格式

### 文本格式（默认）
```bash
✅ project 项目初始化完成
📋 初始化类型: project
🏗️ 项目类型: web_application
⚙️ 启用的特性: caching, git-hooks

📁 创建的文件:
   - .dnaspec/
   - PROJECT_CONSTITUTION.md
   - .dnaspec/config.json
   - .dnaspec/cache/
   - .dnaspec/hooks/
```

### JSON格式
```bash
/dnaspec.dnaspec-init "operation=detect output_format=json"
```

```json
{
  "status": "complete",
  "existing_files": [
    "PROJECT_CONSTITUTION.md",
    ".dnaspec/config.json",
    ".dnaspec/cache"
  ],
  "missing_files": [],
  "project_features": {
    "languages": ["javascript", "python"],
    "tools": ["ci_cd"]
  }
}
```

## 🔧 使用场景示例

### 场景1: 新建Web应用项目
```bash
# 1. 创建项目目录
mkdir my-web-app && cd my-web-app

# 2. 初始化DNASPEC协调机制
/dnaspec.dnaspec-init "operation=init-project init_type=project project_type=web_application features=caching,git_hooks"

# 3. 开始使用DNASPEC技能
/dnaspec.architect "system_type=web_application framework=react"
```

### 场景2: 团队协作项目
```bash
# 1. 检测现有项目
/dnaspec.dnaspec-init "operation=detect"

# 2. 为团队初始化
/dnaspec.dnaspec-init "operation=init-project init_type=team features=caching,ci_cd,monitoring"

# 3. 查看团队配置
/dnaspec.dnaspec-init "operation=get-config"
```

### 场景3: 企业级项目
```bash
# 1. 企业级初始化
/dnaspec.dnaspec-init "operation=init-project init_type=enterprise features=all"

# 2. 获取详细状态
/dnaspec.dnaspec-init "operation=status"

# 3. 监控项目状态
/dnaspec.dnaspec-init "operation=status output_format=json"
```

### 场景4: 现有项目升级
```bash
# 1. 检测当前状态
/dnaspec.dnaspec-init "operation=detect"

# 2. 升级协调机制
/dnaspec.dnaspec-init "operation=upgrade"

# 3. 启用新功能
/dnaspec.dnaspec-init "operation=init-project features=monitoring,security force=true"
```

## 📁 生成的文件结构

初始化后会创建以下文件结构：

```
project-root/
├── PROJECT_CONSTITUTION.md          # 项目协调宪法
├── .dnaspec/                        # DNASPEC配置目录
│   ├── config.json                  # 主配置文件
│   ├── cache/                       # 缓存系统
│   │   ├── temp/                    # 临时缓存
│   │   ├── staging/                 # 暂存缓存
│   │   ├── meta/                    # 缓存元数据
│   │   └── config.json              # 缓存配置
│   ├── hooks/                       # Git钩子
│   ├── logs/                        # 执行日志
│   ├── cicd/                        # CI/CD模板
│   ├── monitoring/                  # 监控配置
│   └── security/                    # 安全配置
```

## 🔗 与其他技能的集成

### 与协调框架集成
```python
# 检测协调状态后使用技能
status = skill.execute("operation=detect")
if status["status"] == "complete":
    # 启用协调模式
    result = coordination_manager.execute_workflow(skill_requests)
else:
    # 使用独立模式
    result = skill_executor.execute_independent(skill_request)
```

### 与现有技能集成
```bash
# 1. 先初始化项目
/dnaspec.dnaspec-init "operation=init-project"

# 2. 使用其他技能（自动启用协调模式）
/dnaspec.architect "system_type=web_application"
/dnaspec.task-decomposer "task=implement_feature"
/dnaspec.constraint-generator "domain=performance"
```

## 🛠️ 故障排除

### 常见问题

#### 1. 初始化失败
```bash
# 检查权限
ls -la .dnaspec/

# 重新初始化
/dnaspec.dnaspec-init "operation=init-project force=true"
```

#### 2. 配置错误
```bash
# 查看详细错误
/dnaspec.dnaspec-init "operation=get-config output_format=json"

# 重置配置
/dnaspec.dnaspec-init "operation=reset confirm=true"
```

#### 3. 状态不一致
```bash
# 检测完整状态
/dnaspec.dnaspec-init "operation=status"

# 修复缺失文件
/dnaspec.dnaspec-init "operation=init-project force=true"
```

### 调试模式
```bash
# 启用详细输出
/dnaspec.dnaspec-init "operation=init-project verbose=true"

# 查看所有配置
/dnaspec.dnaspec-init "operation=get-config output_format=json"
```

## 📈 最佳实践

### 1. 项目初始化最佳实践
- ✅ **先检测再初始化**: 使用 `detect` 了解当前状态
- ✅ **选择合适的初始化类型**: 根据项目规模选择 `project`, `team`, `enterprise`
- ✅ **启用必要功能**: 根据项目需求启用 `caching`, `git_hooks`, `ci_cd`
- ✅ **使用版本控制**: 将配置文件加入Git管理

### 2. 团队协作最佳实践
- ✅ **统一初始化**: 团队成员使用相同的初始化命令
- ✅ **启用团队功能**: 启用 `ci_cd`, `monitoring`, `git_hooks`
- ✅ **定期检查状态**: 使用 `status` 命令监控项目健康
- ✅ **配置模板化**: 使用模板确保一致性

### 3. 维护最佳实践
- ✅ **定期升级**: 使用 `upgrade` 命令保持最新功能
- ✅ **备份重要配置**: 重置前备份现有配置
- ✅ **监控性能**: 关注缓存命中率和执行时间
- ✅ **文档化自定义**: 记录对配置的自定义修改

## 🎯 总结

`dnaspec_init` 技能为DNASPEC项目提供了完整的协调机制初始化和管理功能。通过智能检测、灵活配置和全面的状态管理，它确保了DNASPEC技能能够在项目中高效、协调地工作。

**核心优势:**
- 🚀 **一键初始化**: 快速启动协调机制
- 🎯 **智能检测**: 自动识别项目特征和需求
- 🔧 **灵活配置**: 支持多种项目和团队场景
- 📊 **全面管理**: 状态检测、配置管理、升级维护
- 🔗 **无缝集成**: 与现有DNASPEC技能完美配合

立即使用 `/dnaspec.dnaspec-init` 开始您的智能项目协调之旅！

---

**版本**: 1.0.0  
**更新日期**: 2025-12-21  
**维护者**: DNASPEC团队
