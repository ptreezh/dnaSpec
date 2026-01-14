---
name: cognitive-templater
description: Applies structured cognitive frameworks to enhance reasoning and problem-solving. Use when you need systematic thinking approaches, logical analysis, or structured problem decomposition.
license: MIT
compatibility: Claude Code, VS Code, and any Agent Skills compatible environment
metadata:
  author: DNASPEC Team
  version: "2.0.0"
  category: cognitive-enhancement
  supported_templates: [chain_of_thought, verification, few_shot, role_playing, understanding]
  frameworks: [systematic_thinking, structured_reasoning, perspective_analysis]
---

# Cognitive Templater Skill

## 工作流程

1. **Template Selection**: Analyze problem characteristics and select optimal cognitive template
2. **Framework Loading**: Load deterministic structure via tools/template_executor.py
3. **Structured Application**: Apply step-by-step cognitive framework
4. **Quality Validation**: Verify reasoning quality and coherence
5. **Result Enhancement**: Apply AI reasoning for complex aspects (Layer 3 loading)

## 关键决策点

- **Template Choice**: Which cognitive framework best matches problem complexity and type
- **Depth Level**: Basic framework application vs. deep cognitive enhancement
- **Validation Criteria**: How to measure reasoning quality
- **Integration Strategy**: How to combine multiple templates when needed

## 基本使用方法

Describe your problem or task. The skill will:

1. **Layer 1**: Load metadata and identify problem characteristics
2. **Layer 2**: Execute deterministic template via template_executor.py
3. **Layer 3**: Apply AI reasoning for nuanced aspects
4. **Layer 4**: Generate structured, enhanced output

## 认知模板详解

### 1. Chain of Thought (思维链)
**确定性结构：**
- Problem Understanding → Step Decomposition → Intermediate Reasoning → Solution Verification
**应用场景：** 复杂问题解决、算法设计、逻辑推理

### 2. Verification Template (验证模板)
**确定性结构：**
- Assumption Analysis → Logic Validation → Evidence Evaluation → Alternative Consideration
**应用场景：** 方案审查、质量检查、风险评估

### 3. Few-Shot Learning (少样本学习)
**确定性结构：**
- Example Selection → Pattern Extraction → Application → Validation
**应用场景：** 模式识别、类比推理、经验借鉴

### 4. Role-Playing (角色扮演)
**确定性结构：**
- Role Definition → Perspective Taking → Expertise Application → Integration
**应用场景：** 多角度分析、用户体验设计、冲突解决

### 5. Understanding Framework (理解框架)
**确定性结构：**
- Concept Identification → Relationship Mapping → Context Analysis → Synthesis
**应用场景：** 概念理解、知识整合、深度分析

## 常见模式

### Problem Solving
- **Complex Analysis**: Chain of Thought + Verification
- **Creative Solutions**: Role-Playing + Understanding
- **Pattern Recognition**: Few-Shot + Understanding

### Decision Making
- **Risk Assessment**: Verification + Role-Playing
- **Strategic Planning**: Chain of Thought + Understanding
- **Technical Decisions**: Verification + Chain of Thought

### Learning and Analysis
- **Concept Mastery**: Understanding + Few-Shot
- **Skill Development**: Role-Playing + Chain of Thought
- **Knowledge Integration**: Understanding + Verification

## 输出格式

Structured JSON output with:
- Applied cognitive template(s)
- Step-by-step reasoning process
- Confidence scoring
- Alternative perspectives
- Validation results
- Actionable insights

## 性能指标

- **Template Selection**: <100ms for template matching
- **Framework Execution**: <300ms for standard templates
- **Quality Assurance**: Consistent structured reasoning
- **Scalability**: Handles complex problems up to 5000 characters