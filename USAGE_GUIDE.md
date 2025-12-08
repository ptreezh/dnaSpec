# DNASPEC Context Engineering Skills - 使用指南

## 概述

DNASPEC Context Engineering Skills 是一个专业的AI辅助开发工具集，提供上下文分析、优化和认知模板等功能。它能够自动检测、配置和集成各种AI CLI工具（如Claude CLI、Qwen CLI、Gemini CLI等）。

## 安装

```bash
# 克隆项目
git clone https://github.com/ptreezh/dnaSpec.git
cd dnaSpec

# 安装项目（推荐使用可编辑模式）
pip install -e .
```

## 自动配置

安装后，您可以运行自动配置脚本来检测和配置本地的AI CLI工具：

```bash
# 运行自动配置
python run_auto_config.py
```

这个脚本会：
1. 自动检测系统中安装的AI CLI工具（Claude, Qwen, Gemini, Copilot, Cursor等）
2. 生成相应的配置文件
3. 验证集成状态
4. 创建验证报告

## 使用方法

### 1. 命令行使用

在支持的AI CLI工具中，您可以使用以下命令：

#### 上下文分析
```
/speckit.dnaspec.context-analysis 分析这个需求文档的质量
```

#### 上下文优化
```
/speckit.dnaspec.context-optimization 优化这个需求描述 clarity,completeness
```

#### 认知模板应用
```
/speckit.dnaspec.cognitive-template 如何提高系统性能 template=verification
```

#### 其他可用技能
- `/speckit.dnaspec.architect` - 系统架构设计专家
- `/speckit.dnaspec.agent-creator` - 智能体创建专家
- `/speckit.dnaspec.task-decomposer` - 任务分解专家
- `/speckit.dnaspec.constraint-generator` - 约束生成专家
- `/speckit.dnaspec.dapi-checker` - 接口检查专家
- `/speckit.dnaspec.modulizer` - 模块化专家

### 2. Python API使用

您也可以在Python代码中直接使用这些技能：

```python
from src.dnaspec_context_engineering.skills_system_clean import (
    ContextAnalysisSkill, 
    ContextOptimizationSkill, 
    CognitiveTemplateSkill
)

# 上下文分析
skill = ContextAnalysisSkill()
result = skill.execute_with_ai("设计一个用户认证系统", {})
print(result)

# 上下文优化
optimizer = ContextOptimizationSkill()
result = optimizer.execute_with_ai("优化这个需求描述", {
    "optimization_goals": ["clarity", "completeness"]
})
print(result)

# 认知模板应用
template_skill = CognitiveTemplateSkill()
result = template_skill.execute_with_ai("如何提高系统性能", {
    "template": "verification"
})
print(result)
```

### 3. 交互式Shell

您也可以启动交互式Shell使用所有功能：

```bash
# 通过Python运行CLI
python -c "from dnaspec_spec_kit_integration.cli import main; import sys; sys.argv=['cli', 'shell']; main()"
```

## 支持的AI CLI平台

- Claude CLI
- Qwen CLI  
- Gemini CLI
- GitHub Copilot CLI
- Cursor
- 以及其他支持自定义命令的AI CLI工具

## 配置文件

自动配置会在项目根目录创建以下文件：
- `.dnaspec/config.yaml` - 主配置文件
- `dnaspec-validation-report.md` - 集成验证报告

## 故障排除

如果遇到问题：
1. 确保已正确安装所有依赖
2. 检查系统PATH中是否有相关CLI工具
3. 查看生成的验证报告以了解集成状态

## 开发和扩展

要添加新的技能或扩展功能：
1. 在 `src/dnaspec_context_engineering/skills` 目录下创建新技能
2. 在 `src/dnaspec_spec_kit_integration/skills` 中添加CLI接口
3. 更新 `SkillMapper` 以注册新技能

## 技能说明

### 上下文分析技能 (Context Analysis)
- 分析上下文质量的五个维度：清晰度、相关性、完整性、一致性和效率
- 提供优化建议和问题识别

### 上下文优化技能 (Context Optimization)  
- 根据指定目标优化上下文
- 提供改进指标和应用的优化措施

### 认知模板技能 (Cognitive Template)
- 应用多种认知框架：思维链、少样本学习、验证检查、角色扮演、深度理解
- 提供结构化的问题分析方法