# DSGS Context Engineering Skills - 安装和使用指南

## 概述

DSGS (Dynamic Specification Growth System) Context Engineering Skills系统，提供专业的上下文工程增强工具集。系统基于AI原生设计理念，通过标准化指令模板，实现上下文分析、优化和结构化功能，包含完整的上下文工程技能、Git操作技能和临时工作区管理系统，专门设计用于安全的AI辅助开发流程。

本项目实现了一套独立的技能系统，专注于上下文工程领域，而非依赖外部的spec.kit系统。

## 安装要求

- Python 3.8+
- Git版本控制系统

## 安装步骤

```bash
# 克隆项目
git clone https://github.com/ptreezh/dnaSpec.git
cd dnaSpec

# 安装本项目
pip install -e .
```

## 配置

### 1. API密钥配置（可选）
如果需要使用AI模型API：

```bash
# Anthropic Claude
export ANTHROPIC_API_KEY=your-anthropic-api-key

# Google Gemini  
export GOOGLE_API_KEY=your-google-api-key

# OpenAI GPT
export OPENAI_API_KEY=your-openai-api-key

# 阿里云通义千问
export DASHSCOPE_API_KEY=your-dashscope-api-key
```

## 快速使用示例

### 1. 在Python代码中使用

```python
from clean_skills import (
    context_analysis_execute,
    git_execute,
    temp_workspace_execute
)

# 1. 上下文分析（标准模式）
result = context_analysis_execute({
    'context': '设计一个电商平台，支持用户注册、商品浏览、购物车、订单处理等功能。',
    'mode': 'standard'
})
print(result)

# 2. 上下文分析（增强模式）
result = context_analysis_execute({
    'context': '设计一个电商平台，支持用户注册、商品浏览、购物车、订单处理等功能。',
    'mode': 'enhanced'
})
print(result)

# 3. Git操作示例
result = git_execute({
    'operation': 'status'
})
print(result)

# 4. AI安全工作流示例
# 创建临时工作区
result = temp_workspace_execute({'operation': 'create-workspace'})
print(result)

# 添加AI生成的文件
result = temp_workspace_execute({
    'operation': 'add-file',
    'file_path': 'feature.py',
    'file_content': '# AI生成的代码内容'
})
print("文件添加成功")

# 确认文件
result = temp_workspace_execute({
    'operation': 'confirm-file', 
    'confirm_file': 'feature.py'
})
print("文件确认成功")

# 清理临时工作区
result = temp_workspace_execute({'operation': 'clean-workspace'})
print("临时工作区已清理")
```

### 2. 命令行使用

```bash
# 使用斜杠命令调用技能
/speckit.dsgs.context-analysis "分析系统设计文档的质量"
/speckit.dsgs.context-optimization "优化需求描述的清晰度"
/speckit.dsgs.cognitive-template "如何提高性能 template=verification"
/speckit.dsgs.git-skill "operation=status"
/speckit.dsgs.temp-workspace "operation=create-workspace"
```

## 核心功能

### 1. 上下文工程技能
- **Context Analysis Skill** (`dsgs-context-analysis`): 分析上下文的5个维度质量
- **Context Optimization Skill** (`dsgs-context-optimization`): 基于分析结果优化上下文
- **Cognitive Template Skill** (`dsgs-cognitive-template`): 应用认知模板到任务

### 2. Git操作技能
- **Git Skill** (`dsgs-git-skill`): 完整的Git操作支持
  - 基本操作：status, add, commit, push, pull
  - 分支管理：create, switch, merge
  - 高级功能：worktree管理, stash, diff, log
  - CI/CD集成：支持自动化提交流程

### 3. 临时工作区管理技能
- **Temporary Workspace Skill** (`dsgs-temp-workspace-skill`): AI安全工作流管理
  - AI文件隔离：AI生成的文件首先存放在临时工作区
  - 自动整理：当临时文件超过20个时触发整理提醒
  - 确认机制：文件经过验证后才能移到确认区域
  - Git集成：确认文件可直接同步到Git仓库
  - 自动清理：完成工作后自动清理临时工作区

## AI安全开发工作流

AI生成内容遵循以下安全流程，防止项目被临时文件污染：

1. **生成阶段**：AI输出首先存入临时工作区
2. **整理阶段**：当临时文件超过20个时自动提醒
3. **确认阶段**：人工验证后文件移至确认区域
4. **提交阶段**：确认文件可安全提交到Git仓库
5. **清理阶段**：自动清理临时工作区

### 安全工作流示例

```python
from clean_skills.temp_workspace_skill import execute as temp_workspace_execute
from clean_skills.git_skill import execute as git_execute

def safe_ai_workflow(requirement):
    # 1. 创建临时工作区
    temp_workspace_execute({'operation': 'create-workspace'})
    
    try:
        # 2. AI生成内容到临时区
        # ... AI生成过程 ...
        
        # 3. 监控临时文件数量
        result = temp_workspace_execute({'operation': 'auto-manage'})
        
        # 4. 验证后确认文件
        # ... 验证和确认过程 ...
        
        # 5. 提交到Git
        git_execute({
            'operation': 'add-commit', 
            'message': 'Add AI generated feature', 
            'files': 'confirmed_file.py'
        })
    
    finally:
        # 6. 清理临时工作区
        temp_workspace_execute({'operation': 'clean-workspace'})
```

## 系统集成

### 与AI CLI平台集成
技能系统设计为可以与各种AI CLI平台集成：

- Claude CLI: 通过 `/speckit.dsgs.*` 指令集成
- Gemini CLI: 通过自定义指令集成  
- 通义CLI: 通过自定义指令集成
- 其他平台: 通过统一接口集成

### 工作流程
1. 用户发出技能请求
2. 系统选择适当技能
3. 根据参数执行标准或增强模式
4. 返回结构化结果

## 性能指标

- **响应时间**: 本地操作即时响应，AI相关操作依赖模型响应时间
- **兼容性**: 支持所有主流AI CLI平台
- **安全性**: 临时工作区有效防止项目污染
- **可扩展性**: 支持新的技能和功能扩展

## 故障排除

### 常见问题
- **模块导入错误**: 确认安装路径正确
- **Git操作失败**: 检查是否有Git仓库和权限
- **临时工作区错误**: 确认创建了临时工作区后再执行其他操作

### 错误处理
系统提供详细的错误信息和状态码，便于调试集成问题。

## 许可证

MIT License - 详见 LICENSE 文件