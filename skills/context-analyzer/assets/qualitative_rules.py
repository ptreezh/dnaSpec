"""
Context Analyzer - Qualitative Assessment Rules
定性评估规则提示词模板
用于AI推理部分的定性分析
"""

QUALITATIVE_ASSESSMENT_PROMPT = """
# Context Analyzer - Qualitative Assessment

## 评估维度和规则

### 语义连贯性 (Semantic Coherence)
评估文本的逻辑流畅性和语义一致性：

**评估标准：**
- **高(0.8-1.0)**: 逻辑清晰，思路连贯，无明显断裂
- **中(0.5-0.7)**: 基本连贯，偶有跳跃，整体可理解
- **低(0.0-0.4)**: 逻辑混乱，语义不清，难以理解

**重点关注：**
- 主题一致性
- 逻辑递进关系
- 过渡自然度
- 结论与论据的对应关系

### 上下文相关性 (Contextual Relevance)
评估内容与预期目标的相关程度：

**评估标准：**
- **高(0.8-1.0)**: 高度相关，精准匹配目标需求
- **中(0.5-0.7)**: 基本相关，包含有效信息
- **低(0.0-0.4)**: 相关性低，偏离核心目标

**重点关注：**
- 目标契合度
- 领域专业性
- 信息有效性
- 用户需求满足度

### 结构质量 (Structural Quality)
评估信息的组织结构合理性：

**评估标准：**
- **高(0.8-1.0)**: 结构清晰，层次分明，易于理解
- **中(0.5-0.7)**: 结构基本合理，可读性尚可
- **低(0.0-0.4)**: 结构混乱，无明确逻辑层次

**重点关注：**
- 信息组织逻辑
- 层次结构清晰度
- 段落划分合理性
- 重点信息突出度

### 可操作性 (Actionability)
评估内容的实际应用价值和执行可行性：

**评估标准：**
- **高(0.8-1.0)**: 高度可操作，具体可行，指导明确
- **中(0.5-0.7)**: 具备一定操作性，需要细化补充
- **低(0.0-0.4)**: 缺乏可操作性，过于抽象或模糊

**重点关注：**
- 指导明确性
- 执行可行性
- 资源需求合理性
- 预期效果可量化性

## 评估流程

1. **综合理解**: 全面理解上下文内容和目标
2. **维度评分**: 按上述标准对各维度评分
3. **证据收集**: 为每个评分收集具体证据
4. **权衡平衡**: 考虑各维度的重要性和相互影响
5. **总体判断**: 形成整体质量评估

## 输出格式

```json
{
  "qualitative_assessment": {
    "semantic_coherence": {
      "score": 0.8,
      "evidence": ["逻辑清晰", "思路连贯"],
      "issues": [],
      "suggestions": []
    },
    "contextual_relevance": {
      "score": 0.7,
      "evidence": ["相关度高"],
      "issues": ["部分偏离"],
      "suggestions": ["加强相关性"]
    },
    "structural_quality": {
      "score": 0.6,
      "evidence": ["结构基本合理"],
      "issues": ["层次不够分明"],
      "suggestions": ["优化结构层次"]
    },
    "actionability": {
      "score": 0.5,
      "evidence": ["具备指导性"],
      "issues": ["缺乏具体步骤"],
      "suggestions": ["补充执行细节"]
    }
  },
  "overall_qualitative_score": 0.65,
  "qualitative_insights": [
    "语义表达清晰",
    "结构需要优化"
  ],
  "priority_improvements": [
    "增强可操作性",
    "完善结构层次"
  ]
}
```
"""

def get_qualitative_assessment_prompt(context: str, context_type: str = "general") -> str:
    """生成具体的定性评估提示词"""
    
    return f"""{QUALITATIVE_ASSESSMENT_PROMPT}

## 当前分析任务

**上下文类型**: {context_type}
**待分析内容**:
---
{context}
---

请根据上述评估标准，对该上下文进行全面的定性分析，并按照指定的JSON格式输出结果。

重点关注：
1. 结合上下文类型的特点进行评估
2. 提供具体的证据和改进建议
3. 确保评分的客观性和一致性
4. 识别关键的改进机会
"""