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

## 快速安装（推荐）

### npm方式（最简单）
```bash
# 从npm安装（推荐）
npm install -g dnaspec

# 或从GitHub仓库直接安装（需要先安装Git）
npm install -g ptreezh/dnaSpec

# 然后运行短命令
dnaspec
```

### 或者下载后本地安装
```bash
git clone https://github.com/ptreezh/dnaSpec.git
cd dnaSpec

# 本地安装为全局命令（提供短命令 dnaspec）
npm install -g .

# 然后运行短命令
dnaspec
```

### 或运行脚本（一行命令完成）
```bash
# 直接运行安装脚本（自动完成所有步骤）
git clone https://github.com/ptreezh/dnaSpec.git && cd dnaSpec && node index.js
```

注意：运行安装命令后，系统会：
1. 自动检测Python和Git环境
2. 克隆或使用项目代码
3. 安装Python依赖包
4. 自动检测已安装的AI CLI工具
5. 生成相应配置文件

安装命令：
```bash
# 推荐安装方式
npm install -g dnaspec
dnaspec
```

### Windows系统
```bash
# 方式一：运行一键安装脚本
curl -O https://raw.githubusercontent.com/ptreezh/dnaSpec/main/install_and_configure.bat
install_and_configure.bat

# 方式二：使用短命令启动（需要先安装Node.js）
npm install -g ptreezh/dnaSpec
dsgs
```

### Linux/Mac系统
```bash
# 方式一：运行一键安装脚本
curl -O https://raw.githubusercontent.com/ptreezh/dnaSpec/main/install_and_configure.sh
chmod +x install_and_configure.sh
./install_and_configure.sh

# 方式二：使用短命令启动（需要先安装Node.js）
npm install -g ptreezh/dnaSpec
dsgs
```

## 手动安装

如果需要手动安装：

### 方式一：完整安装
```bash
# 克隆项目
git clone https://github.com/ptreezh/dnaSpec.git
cd dnaSpec

# 安装本项目
pip install -e .

# 运行自动配置
python run_auto_config.py
```

### 方式二：短命令安装（推荐）
```bash
# 克隆项目
git clone https://github.com/ptreezh/dnaSpec.git
cd dnaSpec

# 本地安装为全局命令（提供短命令 dsgs）
npm install -g .

# 或运行安装脚本（自动完成所有步骤）
./index.js
# 或
node index.js
```

使用方式二，您可以直接运行 `dsgs` 命令来进行安装和配置。

### 方式三：使用启动脚本（Windows用户）
下载并使用启动脚本，可从任何位置运行：
```bash
# 下载启动脚本
curl -O https://raw.githubusercontent.com/ptreezh/dnaSpec/main/launch_dsgs.bat

# 运行安装配置
launch_dsgs.bat
```

将 `launch_dsgs.bat` 文件放在系统PATH中的目录中，即可从任何位置运行 `launch_dsgs.bat` 命令。

## 使用方法

### 自动配置（推荐）
```bash
# 首次安装后运行自动配置，检测并配置本地AI CLI工具
python run_auto_config.py
```

### 命令行使用
```bash
# 使用斜杠命令调用技能
/speckit.dsgs.context-analysis "分析这段需求文档的质量"
/speckit.dsgs.context-optimization "优化这段需求的清晰度"
/speckit.dsgs.cognitive-template "如何提高性能 template=verification"
/speckit.dsgs.architect "设计电商系统架构"
/speckit.dsgs.agent-creator "创建AI智能体"
/speckit.dsgs.task-decomposer "分解复杂任务"
/speckit.dsgs.constraint-generator "生成系统约束"
/speckit.dsgs.dapi-checker "检查API接口"
/speckit.dsgs.modulizer "模块化系统设计"
/speckit.dsgs.git-skill "operation=status"
/speckit.dsgs.temp-workspace "operation=create-workspace"
```

### Python API使用
```python
from src.dsgs_context_engineering.skills_system_clean import ContextAnalysisSkill

# 使用上下文分析技能
skill = ContextAnalysisSkill()
result = skill.execute_with_ai("设计一个用户认证系统", {})
print(result)
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

## 一键安装配置特性

本项目实现了"一次安装，自动识别本地的各种CLI编程工具，自动配置完整"的目标：

✅ **环境依赖自动安装** - 通过 `pip install -e .` 自动处理所有Python依赖
✅ **CLI工具自动检测** - 自动扫描系统中安装的AI CLI工具（Claude, Qwen, Gemini, Copilot, Cursor等）
✅ **自动配置生成** - 根据检测结果自动生成配置文件
✅ **一键运行脚本** - 提供 `install_and_configure.py` 一键完成安装和配置
✅ **跨平台支持** - Windows, Linux, Mac 全平台支持

---
DSGS Context Engineering Skills - 专业的AI辅助开发工具套件
© 2025 AI Persona Lab. Released under MIT License.