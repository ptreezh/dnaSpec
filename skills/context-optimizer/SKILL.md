---
name: context-optimizer
description: Optimizes context quality using quantitative rules and AI-driven improvements based on specific goals. Use when enhancing clarity, relevance, completeness, consistency, or efficiency.
license: MIT
compatibility: Claude Code, VS Code, and any Agent Skills compatible environment
metadata:
  author: DNASPEC Team
  version: "2.0.0"
  category: optimization
  supported_goals: [clarity, relevance, completeness, consistency, efficiency, conciseness]
  optimization_methods: [rule_based, ai_enhanced, hybrid]
---

# Context Optimizer Skill

## 工作流程

1. **Goal Specification**: Parse and validate optimization goals
2. **Pre-Optimization Analysis**: Run context-analyzer for baseline metrics
3. **Rule-Based Optimization**: Apply deterministic optimization rules via tools/
4. **AI Enhancement**: Apply qualitative improvements (Layer 2 loading)
5. **Post-Optimization Analysis**: Measure improvement effectiveness
6. **Change Validation**: Validate optimization quality and coherence

## 关键决策点

- **Goal Prioritization**: Which optimization goals are most critical
- **Optimization Strategy**: Conservative vs. aggressive changes
- **Style Preservation**: How much to maintain original style and intent
- **Quality Thresholds**: Minimum acceptable improvement levels
- **Validation Criteria**: How to measure optimization success

## 基本使用方法

Provide context and specify optimization goals. The skill will:

1. **Layer 1**: Load metadata and optimization parameters
2. **Layer 2**: Execute quantitative optimization via rule_based_optimizer.py
3. **Layer 3**: Apply AI-driven enhancements for complex improvements
4. **Layer 4**: Generate before/after comparison and improvement metrics

## 优化目标详解

### Clarity Enhancement (清晰度增强)
**确定性规则：**
- 替换模糊词汇为具体表达
- 增加明确的指令和行动动词
- 优化句子结构和逻辑流
- 消除歧义表达

### Relevance Improvement (相关性提升)
**确定性规则：**
- 增加领域特定关键词密度
- 移除偏离主题的内容
- 强化目标导向的表达
- 优化受众匹配度

### Completeness Fulfillment (完整性完善)
**确定性规则：**
- 识别并补充缺失的约束条件
- 添加必要的上下文信息
- 完善边界条件和异常情况
- 增强实施细节

### Consistency Resolution (一致性解决)
**确定性规则：**
- 标准化术语使用
- 解决逻辑矛盾
- 统一时间表达
- 消除冲突性表述

### Efficiency Enhancement (效率优化)
**确定性规则：**
- 移除冗余表达和重复内容
- 提高信息密度
- 优化结构组织
- 简化复杂表达

## 常见模式

### Document Enhancement
- **Requirements**: Focus on clarity, completeness
- **Technical Specs**: Focus on consistency, relevance
- **User Documentation**: Focus on clarity, efficiency
- **Business Proposals**: Focus on relevance, completeness

### Communication Optimization
- **Email**: Focus on clarity, efficiency
- **Reports**: Focus on relevance, consistency
- **Presentations**: Focus on clarity, relevance
- **Technical Documentation**: Focus on completeness, consistency

## 输出格式

Standard JSON output with:
- Original vs. optimized context
- Applied optimization rules
- Before/after quality metrics
- Improvement quantification
- Change tracking and validation

## 性能指标

- **Optimization Speed**: <500ms for typical contexts
- **Improvement Measurement**: Quantified dimension improvements
- **Quality Preservation**: Maintain original intent and core meaning
- **Consistency Validation**: Ensure optimization coherence