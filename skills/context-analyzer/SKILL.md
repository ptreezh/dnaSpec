---
name: context-analyzer
description: Analyzes context quality across 5 dimensions using quantitative metrics and qualitative assessment. Use when evaluating document quality, requirement completeness, or communication effectiveness.
license: MIT
compatibility: Claude Code, VS Code, and any Agent Skills compatible environment
metadata:
  author: DNASPEC Team
  version: "2.0.0"
  category: quality-assessment
  supported_languages: [en, zh-CN, zh-TW, ja, ko]
  analysis_dimensions: [clarity, relevance, completeness, consistency, efficiency]
  quantitative_metrics: true
  qualitative_assessment: true
---

# Context Analyzer Skill

## 工作流程

1. **Input Validation**: Check context validity and prepare analysis
2. **Quantitative Analysis**: Execute deterministic metrics calculation via tools/quantitative_analyzer.py
3. **Qualitative Assessment**: Apply AI reasoning for complex evaluation (Layer 2 loading)
4. **Score Integration**: Combine quantitative and qualitative results
5. **Recommendation Generation**: Provide actionable improvement suggestions

## 关键决策点

- **Analysis Depth**: Quick assessment vs. comprehensive evaluation
- **Context Type**: Document, requirements, communication, or code
- **Quality Standards**: Academic, business, or technical benchmarks
- **Improvement Priority**: Which dimensions need immediate attention

## 基本使用方法

Provide context for analysis. The skill will automatically:

1. **Layer 1**: Load metadata and basic context (always present)
2. **Layer 2**: Execute quantitative analysis via quantitative_analyzer.py (deterministic)
3. **Layer 3**: Apply qualitative AI assessment if needed (on-demand)
4. **Layer 4**: Generate integrated report and recommendations (final output)

## 定量分析 (工具调用)

The skill automatically calls `quantitative_analyzer.py` for:

- **Clarity**: Sentence structure analysis, clear/ambiguous indicator detection
- **Relevance**: Domain-specific keyword density calculation  
- **Completeness**: Required elements coverage assessment
- **Consistency**: Contradiction and conflict detection
- **Efficiency**: Information density and redundancy analysis

## 定性评估 (AI推理)

When quantitative analysis is insufficient, AI assessment covers:

- **Semantic coherence**: Logical flow and meaning consistency
- **Contextual relevance**: Alignment with intended purpose and audience
- **Structural quality**: Organization and presentation effectiveness
- **Actionability**: Practical value and implementability

## 常见模式

### Document Quality Assessment
- Requirements documents (technical, completeness focus)
- Technical specifications (clarity, consistency focus)
- User documentation (relevance, efficiency focus)
- Project proposals (all dimensions balanced)

### Communication Analysis
- Email effectiveness (clarity, relevance priority)
- Meeting summaries (efficiency, completeness priority)
- Status reports (consistency, clarity priority)
- Stakeholder communications (relevance, actionability priority)

### Content Optimization
- Web content quality (efficiency, relevance focus)
- Training materials (clarity, completeness focus)
- Knowledge base articles (consistency, relevance focus)
- API documentation (technical completeness, clarity focus)

## 输出格式

Standard JSON output with:
- Quantitative scores (0-1 scale)
- Qualitative assessments
- Dimension-specific insights
- Prioritized improvement recommendations
- Overall quality score