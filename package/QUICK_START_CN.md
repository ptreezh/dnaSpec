# DSGS Context Engineering Skills - 快速上手指南 (Chinese)

## 项目概述

DSGS (Dynamic Specification Growth System) Context Engineering Skills 是一个专业的AI辅助开发工具包，专门为AI CLI平台设计，提供上下文分析、优化和认知模板功能，具有AI安全工作流。

## 核心改进

### 1. 统一技能结构
- **统一实现**: 标准版和增强版技能合并为单一实现
- **模式切换**: 通过 `mode` 参数控制功能级别 ('standard' 或 'enhanced')
- **单一入口**: 简化接口，避免重复功能

### 2. 扁平化目录结构
- **一技能一目录**: 每个技能独立目录，无多余嵌套
- **简化组织**: 直观的技能布局，易于维护
- **减少混淆**: 清晰的技能边界，无功能重叠

### 3. AI安全工作流
- **临时工作区**: AI生成内容首先存入临时区
- **自动整理**: 文件超过20个时自动提醒
- **确认机制**: 验证后内容才能移至主项目
- **自动清理**: 任务完成后自动清理临时区

## 安装

```bash
# 克隆仓库
git clone https://github.com/ptreezh/dnaSpec.git
cd dsgs-context-engineering

# 安装
pip install -e .
```

## 使用方法

### CLI命令
```
/speckit.dsgs.context-analysis "分析这段需求文档的质量" mode=enhanced
/speckit.dsgs.cognitive-template "如何提高性能" template=verification
/speckit.dsgs.context-optimization "优化这个需求" optimization_goals=clarity,relevance
/speckit.dsgs.architect "设计电商系统架构"
/speckit.dsgs.git-skill operation=status
/speckit.dsgs.temp-workspace operation=create-workspace
```

### Python API
```python
from clean_skills.context_analysis import execute as context_analysis_execute

# 标准模式
result = context_analysis_execute({
    'context': '设计用户登录功能',
    'mode': 'standard'
})

# 增强模式  
result = context_analysis_execute({
    'context': '设计高安全性用户登录功能',
    'mode': 'enhanced'
})
```

## AI安全最佳实践

1. **AI生成前**: 始终创建临时工作区
2. **验证内容**: 使用确认机制验证AI生成内容
3. **定期整理**: 监控临时文件数量
4. **完成清理**: 任务完成后清理临时区

---
*作者: pTree Dr.Zhang*  
*机构: AI Persona Lab 2025*  
*联系: 3061176@qq.com*  
*网站: https://AgentPsy.com*