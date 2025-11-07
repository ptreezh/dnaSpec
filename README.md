# DSGS与spec.kit整合项目

## 项目概述

本项目旨在将DSGS (Dynamic Specification Growth System) 技能系统与GitHub spec.kit工具包进行深度整合，创建一个既具备专业技能又支持多平台的AI辅助开发系统。

## 功能特性

- **专业技能系统**: 集成DSGS的架构设计、智能体创建等专业技能
- **上下文工程增强**: 新增上下文分析、优化和认知模板应用技能
- **跨平台支持**: 支持Claude CLI、Gemini CLI、Qwen CLI等多种AI工具
- **统一接口**: 提供统一的斜杠命令接口(/speckit.dsgs.*)
- **智能匹配**: 保持DSGS智能匹配和Hook系统的独特优势

## 新增的上下文工程技能

本项目现已集成完整的上下文工程技能集，用于优化项目分解和AI Agentic架构系统的上下文管理：

1. **Context Analysis Skill** (`dsgs-context-analysis`)
   - 分析上下文的有效性
   - 评估各项指标（清晰度、相关性、完整性等）
   - 提供优化建议

2. **Context Optimization Skill** (`dsgs-context-optimization`) 
   - 基于分析结果优化上下文质量
   - 改进清晰度、相关性、完整性和简洁性

3. **Cognitive Template Skill** (`dsgs-cognitive-template`)
   - 应用认知模板到上下文工程任务
   - 提供思维链、少示例学习等框架

4. **Context Engineering Manager** (`dsgs-context-engineering-manager`)
   - 统一管理上下文工程技能

5. **Context Engineering System** (`dsgs-context-engineering-system`)
   - 完整的上下文工程解决方案
   - 支持项目分解和AI Agentic架构上下文管理

## 安装要求

- Python 3.8+
- uv工具包管理器
- Git版本控制系统

## 安装步骤

```bash
# 安装uv工具
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 安装specify-cli
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# 安装本项目
pip install -e .
```

## 使用方法

### 命令行使用

```bash
# 使用斜杠命令调用技能
/speckit.dsgs.architect "设计一个电商系统架构"
/speckit.dsgs.agent-creator "创建订单处理智能体"
/speckit.dsgs.context-analysis "分析系统设计文档的质量"
/speckit.dsgs.context-optimization "优化需求描述的清晰度"
```

### 作为库使用

```python
from dsgs_spec_kit_integration import ContextAnalysisSkill

# 初始化上下文分析技能
skill = ContextAnalysisSkill()

# 分析上下文
result = skill.process_request("系统需要高性能和高可用性", {})
print(result.result)
```