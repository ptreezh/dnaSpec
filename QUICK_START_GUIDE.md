# DNASPEC Context Engineering Skills - 快速上手指南

## 概述

本指南将帮助您快速开始使用DSGS (Dynamic Specification Growth System) Context Engineering Skills系统。该系统提供AI辅助开发技能、Git操作和安全的AI工作流管理，基于AI原生设计理念而非依赖外部的spec.kit系统。

## 快速安装

### 1. 克隆并安装DSGS项目
```bash
# 克隆项目
git clone https://github.com/ptreezh/dnaSpec.git
cd dnaSpec

# 安装项目
pip install -e .
```

## 快速开始使用

### 1. 命令行使用
```bash
# 使用上下文分析技能
/speckit.dnaspec.context-analysis "分析这个需求文档的质量"

# 使用认知模板技能
/speckit.dnaspec.cognitive-template "如何提高系统性能 template=verification"

# 使用Git技能（在CLI中）
/speckit.dnaspec.git-skill "operation=status"

# 使用临时工作区技能
/speckit.dnaspec.temp-workspace "operation=create-workspace"
```

### 2. Python API使用
```python
from clean_skills.context_analysis import execute as context_analysis_execute
from clean_skills.git_skill import execute as git_execute
from clean_skills.temp_workspace_skill import execute as temp_workspace_execute

# 1. 上下文分析
result = context_analysis_execute({
    'context': '设计一个用户登录系统，需要验证用户名和密码',
    'mode': 'enhanced'  # 启用增强模式
})
print(result)

# 2. Git操作
result = git_execute({'operation': 'status'})
print(result)

# 3. AI安全工作流
# 创建临时工作区
result = temp_workspace_execute({'operation': 'create-workspace'})
print(result)

# 生成和添加文件
temp_workspace_execute({
    'operation': 'add-file',
    'file_path': 'feature.py',
    'file_content': '# AI生成的代码'
})

# 确认文件（验证后）
temp_workspace_execute({
    'operation': 'confirm-file',
    'confirm_file': 'feature.py'
})

# 清理临时区
temp_workspace_execute({'operation': 'clean-workspace'})
```

## 最重要的功能

### 1. 上下文工程技能
- **context-analysis**: 分析文本质量（清晰度、相关性、完整性等）
- **context-optimization**: 优化文本内容
- **cognitive-template**: 应用认知模板（思维链、验证等）

### 2. AI安全工作流（防止项目污染）
- **临时工作区**: AI生成的内容首先存入临时区
- **文件限制**: 超过20个临时文件时自动提醒
- **确认机制**: 验证后才能移至主项目
- **自动清理**: 完成后自动清理临时区

### 3. Git操作
- **基本操作**: status, add, commit, push, pull
- **高级功能**: worktree管理，支持隔离开发

## 常用命令

```python
# 标准/增强模式切换
context_analysis_execute({'context': '...', 'mode': 'standard'})  # 标准模式
context_analysis_execute({'context': '...', 'mode': 'enhanced'})  # 增强模式

# 临时工作区管理
temp_workspace_execute({'operation': 'create-workspace'})  # 创建
temp_workspace_execute({'operation': 'list-files'})        # 列出文件
temp_workspace_execute({'operation': 'auto-manage'})       # 自动管理
temp_workspace_execute({'operation': 'clean-workspace'})   # 清理

# Git操作
git_execute({'operation': 'status'})     # 查看状态
git_execute({'operation': 'commit', 'message': '...', 'files': '.'})  # 提交
```

## 最佳实践

1. **使用AI时**: 始终先创建临时工作区
2. **验证内容**: 在确认前仔细检查AI生成的内容
3. **定期整理**: 监控临时文件数量
4. **Git提交**: 使用有意义的提交信息

## 故障排除

- **找不到模块**: 确保正确安装并激活虚拟环境
- **Git操作失败**: 检查当前目录是否为Git仓库
- **临时工作区错误**: 确保已创建工作区再执行其他操作

## 下一步

- 查看 `INSTALL_GUIDE.md` 获取完整安装说明
- 查看 `AI_SAFETY_GUIDELINES.md` 了解安全工作流详情
- 查看 `README.md` 了解所有可用技能