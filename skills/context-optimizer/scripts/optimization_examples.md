# Context Optimizer Examples

## Example 1: Clarity Enhancement

### Input Context
```
用户登录系统需要一些功能，可能包含验证码，大概要支持多种登录方式。
```

### Optimization Goals
```json
["clarity", "relevance"]
```

### Expected Output
```json
{
  "original_context": "用户登录系统需要一些功能，可能包含验证码，大概要支持多种登录方式。",
  "optimized_context": "请执行以下操作：用户登录系统需要具体的功能，在特定条件下包含验证码，大约(精确)要支持多种登录方式。",
  "optimization_goals": ["clarity", "relevance"],
  "applied_rules": [
    {
      "rule": "add_clear_instruction",
      "instruction": "请执行以下操作：",
      "position": "beginning"
    },
    {
      "rule": "replace_ambiguous_terms",
      "pattern": "\\b一些\\b",
      "replacement": "具体的",
      "count": 1
    },
    {
      "rule": "replace_ambiguous_terms", 
      "pattern": "\\b可能\\b",
      "replacement": "在特定条件下",
      "count": 1
    },
    {
      "rule": "replace_ambiguous_terms",
      "pattern": "\\b大概\\b", 
      "replacement": "大约(精确)",
      "count": 1
    }
  ],
  "change_summary": {
    "replacements": 3,
    "additions": 1,
    "removals": 0,
    "restructures": 0
  },
  "improvements": {
    "length_reduction": 0.05,
    "vocabulary_improvement": 2,
    "optimization_intensity": 0.05
  }
}
```

## Example 2: Completeness & Consistency Enhancement

### Input Context
```
API接口需要返回用户数据，所有字段都是字符串，不包含数字类型。
系统必须包含用户ID和创建时间，可以包含额外字段。
```

### Optimization Goals
```json
["completeness", "consistency"]
```

### Expected Output
```json
{
  "original_context": "API接口需要返回用户数据，所有字段都是字符串，不包含数字类型。系统必须包含用户ID和创建时间，可以包含额外字段。",
  "optimized_context": "API接口需要返回用户数据，所有字段都是字符串，不包含数字类型。系统必须包含用户ID和创建时间，在特定情况下不包含额外字段。\n\n约束条件：基本约束条件\n边界条件：考虑极端情况和异常处理场景",
  "optimization_goals": ["completeness", "consistency"],
  "applied_rules": [
    {
      "rule": "resolve_contradiction",
      "positive_term": "必须",
      "negative_term": "可以",
      "resolution": "add_condition_qualifier"
    },
    {
      "rule": "add_constraint_conditions",
      "type": "general",
      "constraint": "基本约束条件"
    },
    {
      "rule": "add_boundary_conditions",
      "suggestion": "\\n边界条件：考虑极端情况和异常处理场景"
    }
  ],
  "change_summary": {
    "replacements": 1,
    "additions": 2,
    "removals": 0,
    "restructures": 0
  }
}
```

## Example 3: Multi-Goal Optimization

### Input Context
```
开发一个电商系统，as well as 支持支付功能。in order to 提高用户体验，需要优化界面设计。基本上来说，需要进行数据库优化和代码重构。
```

### Optimization Goals
```json
["clarity", "efficiency", "conciseness"]
```

### Expected Output
```json
{
  "original_context": "开发一个电商系统，as well as 支持支付功能。in order to 提高用户体验，需要优化界面设计。基本上来说，需要进行数据库优化和代码重构。",
  "optimized_context": "请执行以下操作：开发一个电商系统，以及支持支付功能。为了提高用户体验，需要优化界面设计。进行数据库优化和代码重构。",
  "optimization_goals": ["clarity", "efficiency", "conciseness"],
  "applied_rules": [
    {
      "rule": "add_clear_instruction",
      "instruction": "请执行以下操作：",
      "position": "beginning"
    },
    {
      "rule": "remove_redundancy",
      "pattern": "\\bas\\s+well\\s+as\\b",
      "replacement": "以及",
      "count": 1
    },
    {
      "rule": "remove_redundancy",
      "pattern": "\\bin\\s+order\\s+to\\b", 
      "replacement": "为了",
      "count": 1
    },
    {
      "rule": "remove_filler_words",
      "filler_word": "\\b基本上来说\\b",
      "count": 1
    }
  ],
  "change_summary": {
    "replacements": 3,
    "additions": 1,
    "removals": 1,
    "restructures": 0
  },
  "improvements": {
    "length_reduction": 0.15,
    "vocabulary_improvement": 1,
    "optimization_intensity": 0.15
  }
}
```

## Example 4: Domain-Specific Optimization

### Input Context (Technical Document)
```
The application processes user information. It needs to handle multiple requests. Performance requirements include response time.
```

### Optimization Goals
```json
["relevance", "completeness"]
```

### Expected Output
```json
{
  "original_context": "The application processes user information. It needs to handle multiple requests. Performance requirements include response time.",
  "optimized_context": "The application processes user information. It needs to handle multiple requests, 技术实现方案. Performance requirements include response time.\n\n约束条件：性能约束：响应时间<500ms，并发数>1000",
  "applied_rules": [
    {
      "rule": "enhance_domain_relevance",
      "domain": "technical", 
      "enhancement": "技术实现方案"
    },
    {
      "rule": "add_constraint_conditions",
      "type": "performance",
      "constraint": "性能约束：响应时间<500ms，并发数>1000"
    }
  ]
}
```

## Usage Patterns

### Quick Optimization
适用于快速改进，主要目标：
- Remove obvious ambiguities
- Fix major contradictions
- Add essential constraints

### Comprehensive Enhancement
适用于正式文档优化：
- Apply all applicable rules
- Ensure terminology consistency
- Add complete constraint sets

### Style Preservation
适用于保持原文风格：
- Conservative replacements only
- Minimal structural changes
- Focus on clarity improvements

### Aggressive Optimization
适用于内容重构：
- Maximum rule application
- Significant restructuring
- Complete terminology standardization