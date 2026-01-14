# Context Analyzer Examples

## Example 1: Requirements Document Analysis

### Input Context
```
用户认证系统需要支持手机号和邮箱登录，必须确保密码安全，应该包含验证码功能。
登录失败时提供错误提示，但不透露具体错误原因。系统需要处理并发请求，
性能要求是响应时间小于500ms，同时支持1000个并发用户。
```

### Expected Output
```json
{
  "quantitative_analysis": {
    "clarity": {"score": 0.8, "issues": ["部分表述不够具体"]},
    "relevance": {"score": 0.9, "details": {"relevance_density": 0.6}},
    "completeness": {"score": 0.7, "missing_elements": ["具体的约束条件"]},
    "consistency": {"score": 0.9, "detected_contradictions": []},
    "efficiency": {"score": 0.8, "information_density": 0.4}
  },
  "qualitative_assessment": {
    "semantic_coherence": {"score": 0.8},
    "contextual_relevance": {"score": 0.9},
    "structural_quality": {"score": 0.7},
    "actionability": {"score": 0.8}
  },
  "overall_score": 0.82,
  "priority_suggestions": [
    "补充完整的约束条件",
    "明确技术实现细节"
  ]
}
```

## Example 2: Technical Communication

### Input Context
```
我们需要优化API性能。可能需要增加缓存层，大概要用Redis。
也许还要优化数据库查询，好像响应时间有点慢。
```

### Expected Output
```json
{
  "quantitative_analysis": {
    "clarity": {"score": 0.3, "ambiguity_ratio": 0.8},
    "relevance": {"score": 0.6, "relevance_count": 3},
    "completeness": {"score": 0.2, "completeness_count": 1},
    "consistency": {"score": 0.8, "contradiction_count": 0},
    "efficiency": {"score": 0.5, "information_density": 0.25}
  },
  "qualitative_assessment": {
    "semantic_coherence": {"score": 0.4, "issues": ["表达过于模糊"]},
    "contextual_relevance": {"score": 0.7},
    "structural_quality": {"score": 0.6},
    "actionability": {"score": 0.3, "issues": ["缺乏具体行动步骤"]})
  },
  "overall_score": 0.47,
  "priority_suggestions": [
    "明确优化目标和指标",
    "提供具体的技术方案",
    "消除模糊表达"
  ]
}
```

## Example 3: User Documentation

### Input Context
```
# 用户注册指南

1. 点击注册按钮
2. 填写用户信息（用户名、邮箱、密码）
3. 验证邮箱地址
4. 完成注册流程

注意：用户名必须唯一，密码长度至少8位，邮箱必须是有效邮箱格式。
```

### Expected Output
```json
{
  "quantitative_analysis": {
    "clarity": {"score": 0.9, "clarity_ratio": 0.8},
    "relevance": {"score": 0.7, "relevance_count": 4},
    "completeness": {"score": 0.8, "completeness_count": 6},
    "consistency": {"score": 1.0, "contradiction_count": 0},
    "efficiency": {"score": 0.6, "information_density": 0.3}
  },
  "qualitative_assessment": {
    "semantic_coherence": {"score": 0.9, "evidence": ["步骤清晰", "逻辑合理"]},
    "contextual_relevance": {"score": 0.8},
    "structural_quality": {"score": 0.9, "evidence": ["结构清晰", "层次分明"]},
    "actionability": {"score": 0.9, "evidence": ["指导明确", "可执行性强"]}
  },
  "overall_score": 0.82,
  "priority_suggestions": [
    "可以添加常见问题解答",
    "考虑添加截图或示例"
  ]
}
```

## Example Usage Patterns

### Quick Assessment
适用于快速检查，重点关注：
- Clarity score (>= 0.6)
- Overall score (>= 0.5)

### Comprehensive Evaluation
适用于正式文档评估，重点关注：
- All dimensions >= 0.7
- Quantitative + Qualitative consistency
- Actionability score >= 0.8

### Quality Improvement
适用于文档优化，重点关注：
- Low-scoring dimensions
- Specific issues and suggestions
- Priority improvement recommendations