# DSGS Context Engineering Skills - DSGS上下文工程技能系统
## 项目概述

本项目是DSGS (Dynamic Specification Growth System) Context Engineering Skills系统，提供专业的上下文工程增强工具集。系统基于AI原生设计理念，通过标准化指令模板，实现上下文分析、优化和结构化功能，包含完整的上下文工程技能、Git操作技能和临时工作区管理系统，专门设计用于安全的AI辅助开发流程。
本项目实现了一套独立的技能系统，专注于上下文工程领域，而非依赖外部的spec.kit系统。
## 功能特性
- **专业技能系统**: 专注上下文分析、优化和认知模板应用的专业技能
- **上下文工程增强**: 新增上下文分析、优化和认知模板应用技能
- **AI安全工作流**: 通过临时工作区管理系统，防止AI生成的临时文件污染主项目
- **Git操作集成**: 完整的Git工作流支持，包括worktree和CI/CD功能
- **跨平台支持**: 支持Claude CLI、Gemini CLI、Qwen CLI等多种AI工具
- **统一接口**: 提供统一的斜杠命令接口 (/speckit.dsgs.*)
- **智能匹配**: 保持DSGS智能匹配和Hook系统的独特优势
## 核心技能集

### 上下文工程技能
1. **Context Analysis Skill** (`dsgs-context-analysis`)
   - 分析上下文的有效性
   - 评估五维质量指标（清晰度、相关性、完整性、一致性、效率）
   - 提供优化建议
   - 支持标准和增强两种模式
2. **Context Optimization Skill** (`dsgs-context-optimization`) 
   - 基于分析结果优化上下文质量
   - 改进清晰度、相关性、完整性和简洁性
   - 支持Token预算优化和记忆集成考量
   - 支持标准和增强两种模式
3. **Cognitive Template Skill** (`dsgs-cognitive-template`)
   - 应用认知模板到上下文工程任务
   - 提供思维链、少示例学习、验证检查等框架
   - 支持标准和增强两种模式
### Git操作技能
4. **Git Skill** (`dsgs-git-skill`)
   - 基本操作：status, add, commit, push, pull
   - 分支管理：create, switch, merge
   - 高级功能：worktree管理, stash, diff, log
   - CI/CD集成：支持自动化提交流程

### 临时工作区管理技能
5. **Temporary Workspace Skill** (`dsgs-temp-workspace-skill`)
   - **AI文件隔离**：AI生成的文件首先存放在临时工作区
   - **自动整理**：当临时文件超过20个时触发整理提醒
   - **确认机制**：文件经过验证后才能移到确认区域
   - **Git集成**：确认文件可直接同步到Git仓库
   - **自动清理**：完成工作后自动清理临时工作区
### 管理和系统技能
6. **Context Engineering Manager** (`dsgs-context-engineering-manager`)
   - 统一管理上下文工程技能
7. **Context Engineering System** (`dsgs-context-engineering-system`)
   - 完整的上下文工程解决方案
   - 支持项目分解和AI Agentic架构上下文管理
## AI安全工作流
AI生成内容遵循以下安全流程，防止项目被临时文件污染：
1. **生成阶段**：AI输出首先存入临时工作区
2. **整理阶段**：当临时文件超过20个时自动提醒
3. **确认阶段**：人工验证后文件移至确认区域
4. **提交阶段**：确认文件可安全提交到Git仓库
5. **清理阶段**：自动清理临时工作区

## 作者信息
- **作者**: pTree Dr.Zhang
- **机构**: AI Persona Lab 2025 (人工智能人格实验室2025)
- **联系邮箱**: 3061176@qq.com
- **官方网站**: https://AgentPsy.com
- **开源协议**: MIT License
- **版本**: v1.0.2

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

## 使用方法

### 命令行使用
```bash
# 使用斜杠命令调用技能
/speckit.dsgs.context-analysis "分析这段需求文档的质量"
/speckit.dsgs.context-optimization "优化这段需求的清晰度"
/speckit.dsgs.cognitive-template "如何提高性能 template=verification"
/speckit.dsgs.git-skill "operation=status"
/speckit.dsgs.temp-workspace "operation=create-workspace"
```

### 作为库使用
```python
from clean_skills.context_analysis import execute as context_analysis_execute

# 标准模式
result = context_analysis_execute({'context': '待分析文本', 'mode': 'standard'})

# 增强模式
result = context_analysis_execute({'context': '待分析文本', 'mode': 'enhanced'})
```

### Git操作示例

```python
from clean_skills.git_skill import execute as git_execute

# 查看Git状态
result = git_execute({'operation': 'status'})

# 提交文件
result = git_execute({'operation': 'commit', 'message': '提交信息', 'files': '.'})

# 创建工作树（隔离实验性开发）
result = git_execute({
    'operation': 'worktree-add', 
    'branch': 'feature/new-feature'
})
```

### 临时工作区使用示例
```python
from clean_skills.temp_workspace_skill import execute as temp_workspace_execute

# 创建临时工作区（AI生成前必须）
result = temp_workspace_execute({'operation': 'create-workspace'})

# 添加AI生成的文件
result = temp_workspace_execute({
    'operation': 'add-file', 
    'file_path': 'generated_code.py', 
    'file_content': '# 代码内容'
})

# 确认文件（验证后）
result = temp_workspace_execute({'operation': 'confirm-file', 'confirm_file': 'generated_code.py'})

# 清理临时工作区
result = temp_workspace_execute({'operation': 'clean-workspace'})
```

## 贡献

欢迎贡献！请遵循以下指南：
1. Fork项目并Clone到本地
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 开启Pull Request

## 支持

- 问题报告: https://github.com/ptreezh/dnaSpec/issues
- 联系邮箱: 3061176@qq.com
- 官方网站: https://AgentPsy.com

---
DSGS Context Engineering Skills - 专业的AI辅助开发工具套件 
© 2025 AI Persona Lab. Released under MIT License.