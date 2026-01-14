# DNA SPEC Context System - DNA规格系统

## 项目概述

本项目是DNA SPEC Context System (DNA规格系统) - 一个AI Agentic Complexity Growth Platform，专门设计用于支持系统从简单Idea到复杂智能化系统的自动化复杂度增长。系统基于生物学DNA启发，采用综合集成研讨厅架构，融合定性定量两种处理方式，通过局部智能体（Agentic）架构和分级审核机制，构建真正智能化的软件开发环境。

系统遵循认知过程的格式塔原则，将确定性逻辑用代码和算法固化，不确定性分析通过智能体处理，需要用户决策的模糊问题以最直观的决策问答形式呈现给用户界面。未来每个系统都将是综合集成研讨厅，定性部分以思维链和提示词优化为主，以置信度审核和多源多维度思考的共识计算为判断准则；定量部分则通过明确的、可固化的逻辑和算法，以代码方式实现。

本项目实现了一套独立的技能系统，专注于上下文工程和AI辅助开发领域，而非依赖外部的spec.kit系统。

## 功能特性

- **综合集成研讨厅架构**: 融合定性定量处理方式，实现智能化与自动化的平衡
- **专业技能系统**: 专注上下文分析、优化、认知模板应用以及任务分解、约束生成、API检查等全套技能
- **上下文工程增强**: 新增上下文分析、优化和认知模板应用技能，防止上下文膨胀/腐蚀
- **Agentic智能体架构**: 实现局部智能体处理复杂意图，避免全局上下文膨胀
- **AI安全工作流**: 通过临时工作区管理系统，防止AI生成的临时文件污染主项目
- **格式塔认知原则**: 遵循接近性、相似性、连续性、闭合性认知原则，确保统一连贯的体验
- **自顶向下任务分解**: 从整体概念到具体可执行模块的结构化分解
- **分级审核机制**: 模块/子系统/系统级的多层级审核架构
- **宪法需求管理**: 基于初始宪法的动态约束和需求对齐管理
- **Git操作集成**: 完整的Git工作流支持，包括worktree和CI/CD功能
- **跨平台支持**: 支持Claude CLI、Gemini CLI、Qwen CLI等多种AI工具
- **统一接口**: 提供统一的斜杠命令接口 (/dnaspec.*)
- **智能匹配**: 保持DNA Spec System智能匹配和Hook系统的独特优势
- **渐进式增长**: 从简单Idea到复杂智能系统的平稳演进

## 综合集成研讨厅核心理念

未来每个系统都将是综合集成研讨厅，融合定性定量两种处理方式，实现智能化与自动化的平衡。系统的核心架构包括：

### 定性处理模块
- **思维链和提示词优化**: 处理复杂、模糊或不确定性问题
- **置信度审核机制**: 对推理过程进行验证和确认
- **多源多维度思考的共识计算**: 提高判断的准确性和可靠性
- **认知模板应用**: 如链式思维、少样本学习、验证、角色扮演等

### 定量处理模块
- **确定性逻辑固化**: 通过代码和算法固定可固化的逻辑
- **算法实现**: 处理明确的计算任务
- **性能计算**: 量化的性能指标
- **接口协议**: 明确的API定义和通信规范

### 智能体社会架构
- **局部智能体**: 专门处理特定领域任务，避免全局上下文膨胀
- **任务专业化**: 每个智能体专注特定领域任务
- **模块化设计**: 便于维护和扩展
- **可扩展性**: 支持系统复杂度的有序增长

### 分级审核机制
- **模块级审核**: 独立模块功能验证
- **子系统级审核**: 跨模块集成验证
- **系统级审核**: 整体架构一致性验证
- **跨系统审核**: 与外部系统的接口验证

## 核心技能集

### 上下文工程技能

1. **Context Analysis Skill** (`/dnaspec.context-analysis`)
   - 分析上下文的有效性
   - 评估五维质量指标（清晰度、相关性、完整性、一致性、效率）
   - 提供优化建议
   - 支持标准和增强两种模式
   - **应用**: 确保从简单Idea到复杂系统的每个阶段需求清晰明确

2. **Context Optimization Skill** (`/dnaspec.context-optimization`)
   - 基于分析结果优化上下文质量
   - 改进清晰度、相关性、完整性和简洁性
   - 支持Token预算优化和记忆集成考量
   - 支持标准和增强两种模式
   - **应用**: 优化整个开发过程中的上下文质量，防止上下文膨胀

3. **Cognitive Template Skill** (`/dnaspec.cognitive-template`)
   - 应用认知模板到上下文工程任务
   - 提供思维链、少示例学习、验证检查、角色扮演等框架
   - 支持标准和增强两种模式
   - **应用**: 应用格式塔认知原则，结构化复杂任务

### 系统设计技能

4. **Architect Skill** (`/dnaspec.architect`)
   - 系统架构设计和组件规划
   - 支持微服务、单体、事件驱动等多种架构风格
   - **应用**: 支持从简单到复杂的架构演进

5. **Simple Architect Skill** (`/dnaspec.simple-architect`)
   - 为简单项目提供基础架构设计
   - **应用**: Idea初期和需求规范化阶段的快速架构

6. **System Architect Skill** (`/dnaspec.system-architect`)
   - 高级系统架构设计和详细设计
   - **应用**: 复杂系统的架构设计和智能体集成架构

### 智能体（Agentic）技能

7. **Agent Creator Skill** (`/dnaspec.agent-creator`)
   - 创建专门的AI智能体，处理特定任务
   - 避免整个系统上下文膨胀
   - **应用**: 实现局部智能体架构，执行专项任务

8. **Task Decomposer Skill** (`/dnaspec.task-decomposer`)
   - 将复杂任务分解为遵循KISS/YAGNI/SOLID原则的原子任务
   - 创建独立工作区实现上下文隔离
   - **应用**: 任务分解与上下文隔离，防止任务爆炸

9. **Constraint Generator Skill** (`/dnaspec.constraint-generator`)
   - 基于初始宪法需求生成动态约束
   - 实现需求版本管理和时间点恢复机制
   - **应用**: 宪法需求版本控制，需求对齐检查，变更追溯

10. **API Checker Skill** (`/dnaspec.api-checker`)
    - 实现模块级、子系统级、系统级的分级审核
    - 验证不同层级间的调用对齐和作用域管理
    - **应用**: 分级接口对齐验证，多层级调用一致性检查

### 模块化技能

11. **Modulizer Skill** (`/dnaspec.modulizer`)
    - 将系统分解为可重用模块
    - 应用模块化设计原则
    - **应用**: 系统模块化分解，实现自底向上模块化

### 基础设施技能

12. **Git Skill** (`/dnaspec.git-skill`)
    - 基本操作：status, add, commit, push, pull
    - 分支管理：create, switch, merge
    - 高级功能：worktree管理, stash, diff, log
    - CI/CD集成：支持自动化提交流程

13. **Temporary Workspace Skill** (`/dnaspec.temp-workspace-skill`)
    - **AI文件隔离**：AI生成的文件首先存放在临时工作区
    - **自动整理**：当临时文件超过20个时触发整理提醒
    - **确认机制**：文件经过验证后才能移到确认区域
    - **Git集成**：确认文件可直接同步到Git仓库
    - **自动清理**：完成工作后自动清理临时工作区
    - **应用**: 实现AI安全工作流，防止临时文件污染主项目

### 管理和系统技能

14. **Context Engineering Manager** (`/dnaspec.context-engineering-manager`)
    - 统一管理上下文工程技能

15. **Context Engineering System** (`/dnaspec.context-engineering-system`)
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
- **版本**: v2.0.5

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
dnaspec
```

### Linux/Mac系统

```bash
# 方式一：运行一键安装脚本
curl -O https://raw.githubusercontent.com/ptreezh/dnaSpec/main/install_and_configure.sh
chmod +x install_and_configure.sh
./install_and_configure.sh

# 方式二：使用短命令启动（需要先安装Node.js）
npm install -g ptreezh/dnaSpec
dnaspec
```

## 使用方法

### 自动配置（推荐）

```bash
# 首次安装后运行自动配置，检测并配置本地AI CLI工具
python run_auto_config.py
```

### 命令行使用

```bash
# 使用斜杠命令调用技能
/dnaspec.context-analysis "分析这段需求文档的质量"
/dnaspec.context-optimization "优化这段需求的清晰度"
/dnaspec.cognitive-template "如何提高性能 template=verification"
/dnaspec.architect "设计电商系统架构"
/dnaspec.agent-creator "创建AI智能体"
/dnaspec.task-decomposer "分解复杂任务"
/dnaspec.constraint-generator "生成系统约束"
/dnaspec.dapi-checker "检查API接口"
/dnaspec.modulizer "模块化系统设计"
/dnaspec.git-skill "operation=status"
/dnaspec.temp-workspace "operation=create-workspace"
```

### Python API使用

```python
from src.dna_spec_kit_integration.skills.context_analysis import ContextAnalysisSkill

# 使用上下文分析技能
skill = ContextAnalysisSkill()
result = skill.execute("设计一个用户认证系统", {})
print(result)
```

### 作为库使用

```python
from clean_skills.context_analysis import execute as context_analysis_execute

# 标准模式
result = context_analysis_execute({'context': '待分析文本', 'mode': 'standard'})

# 增强模式
result = context_analysis_execute({'context': '待分析文本', 'mode': 'enhanced'})

# 任务分解技能示例
from clean_skills.task_decomposer import execute_task_decomposer
result = execute_task_decomposer({
    'requirements': '构建一个电商系统',
    'max_depth': 2
})

# 约束生成技能示例
from clean_skills.constraint_generator import execute_constraint_generator
result = execute_constraint_generator({
    'requirements': '金融系统，需要高安全性和可靠性',
    'change_request': '添加新的支付方式'
})

# API检查技能示例
from clean_skills.api_checker import execute_api_checker
result = execute_api_checker({
    'api_specs': {
        'version': '1.0',
        'endpoints': [
            {'path': '/api/users', 'method': 'GET'},
            {'path': '/api/users', 'method': 'POST'}
        ]
    }
})
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
✅ **修复配置路径问题** - 解决npm安装过程中找不到配置脚本的路径问题 (v1.0.3)

---

DNA Spec System - 专业的AI辅助开发工具套件
© 2025 AI Persona Lab. Released under MIT License.
