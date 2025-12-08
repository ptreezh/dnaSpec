# DNASPEC Context Engineering Skills API Specification

## 1. API Overview

The DNASPEC Context Engineering Skills API provides programmatic access to context analysis, optimization, and cognitive template application capabilities. The API follows the DNASPEC skill execution pattern and returns standardized results.

### Base URL
```
https://api.dnaspec.example.com/v1/contexts
```

### Authentication
All API endpoints require authentication using DNASPEC authentication tokens.

### Content Type
All requests and responses use JSON format with UTF-8 encoding.

## 2. Common Data Structures

### 2.1 SkillResult Object
```json
{
  "skill_name": "string",
  "status": "PENDING | ACTIVE | COMPLETED | ERROR",
  "result": "any",
  "confidence": 0.0 - 1.0,
  "execution_time": 0.0,  // in seconds
  "error_message": "string",  // optional
  "metadata": {
    "processed_at": "timestamp",
    "request_length": 0,
    "additional_info": "any"  // optional
  }
}
```

### 2.2 AnalysisResult Object
```json
{
  "context_length": 0,
  "token_count": 0,
  "metrics": {
    "clarity": 0.0 - 1.0,
    "relevance": 0.0 - 1.0,
    "completeness": 0.0 - 1.0,
    "consistency": 0.0 - 1.0,
    "efficiency": 0.0 - 1.0
  },
  "suggestions": ["string"],
  "issues": ["string"]
}
```

### 2.3 OptimizationResult Object
```json
{
  "original_context": "string",
  "optimized_context": "string",
  "original_analysis": "AnalysisResult",
  "optimized_analysis": "AnalysisResult",
  "applied_optimizations": ["string"],
  "improvement_metrics": {
    "clarity": -1.0 - 1.0,
    "relevance": -1.0 - 1.0,
    "completeness": -1.0 - 1.0,
    "consistency": -1.0 - 1.0,
    "efficiency": -1.0 - 1.0,
    "conciseness": -1.0 - 1.0
  }
}
```

## 3. API Endpoints

### 3.1 Context Analysis Skill

#### POST /analyze
Analyze the quality of input context and provide metrics and recommendations.

**Request**:
```json
{
  "context": "string",
  "context_params": {}  // Additional parameters for analysis
}
```

**Response**:
```json
{
  "skill_name": "dnaspec-context-analysis",
  "status": "COMPLETED",
  "result": {
    "context_length": 100,
    "token_count": 25,
    "metrics": {
      "clarity": 0.75,
      "relevance": 0.90,
      "completeness": 0.50,
      "consistency": 1.00,
      "efficiency": 0.80
    },
    "suggestions": [
      "增加更明确的指令和目标描述",
      "添加更多约束条件和要求说明"
    ],
    "issues": [
      "缺少关键信息元素: 目标, 要求"
    ]
  },
  "confidence": 0.85,
  "execution_time": 0.123,
  "metadata": {
    "processed_at": "2025-11-05T23:45:00.123Z",
    "request_length": 100
  }
}
```

**HTTP Status Codes**:
- 200: Analysis completed successfully
- 400: Invalid request parameters
- 500: Internal server error during analysis

### 3.2 Context Optimization Skill

#### POST /optimize
Optimize the input context based on analysis and user-defined goals.

**Request**:
```json
{
  "context": "string",
  "context_params": {
    "optimization_goals": ["clarity", "relevance", "completeness"]
  }
}
```

**Response**:
```json
{
  "skill_name": "dnaspec-context-optimization",
  "status": "COMPLETED",
  "result": {
    "original_context": "需要设计一个系统...",
    "optimized_context": "需要设计一个系统... [优化后的内容]",
    "original_analysis": {
      // AnalysisResult object
    },
    "optimized_analysis": {
      // AnalysisResult object
    },
    "applied_optimizations": [
      "替换模糊词汇: 一些 -> 具体数量",
      "添加缺失元素: 约束条件"
    ],
    "improvement_metrics": {
      "completeness": 1.00,
      "consistency": 0.00,
      "clarity": 0.00
    }
  },
  "confidence": 0.80,
  "execution_time": 0.234,
  "metadata": {
    "processed_at": "2025-11-05T23:45:01.234Z",
    "request_length": 100
  }
}
```

### 3.3 Cognitive Template Skill

#### POST /apply-template
Apply cognitive templates to structure reasoning and improve context.

**Request**:
```json
{
  "context": "string",
  "context_params": {
    "template": "chain_of_thought | few_shot | verification | role_playing | understanding",
    "role": "string"  // for role_playing template
  }
}
```

**Response**:
```json
{
  "skill_name": "dnaspec-cognitive-template",
  "status": "COMPLETED",
  "result": {
    "success": true,
    "template_name": "chain_of_thought",
    "template_description": "将复杂问题分解为步骤序列",
    "original_context": "如何提高系统安全性？",
    "enhanced_context": "### 思维链分析\n请使用以下思维链步骤分析问题：\n\n1. **问题理解**: 如何提高系统安全性？\n...",
    "structure": [
      "问题理解",
      "步骤分解",
      "中间推理",
      "验证检查",
      "最终答案"
    ]
  },
  "confidence": 0.90,
  "execution_time": 0.056,
  "metadata": {
    "processed_at": "2025-11-05T23:45:02.056Z",
    "request_length": 15
  }
}
```

### 3.4 Context Engineering System

#### POST /system-operation
Execute system-level operations including project decomposition and agentic context enhancement.

**Request**:
```json
{
  "context": "string",
  "context_params": {
    "function": "enhance_context_for_project | enhance_agentic_context | run_context_audit"
  }
}
```

**Response (enhance_context_for_project)**:
```json
{
  "skill_name": "dnaspec-context-engineering-system",
  "status": "COMPLETED",
  "result": {
    "success": true,
    "original_description": "开发电商平台...",
    "suggested_decomposition": [
      "1. 问题理解: 开发电商平台包含用户注册、商品展示等功能",
      "2. 步骤分解: [详细分解步骤]"
    ],
    "optimized_context": "优化后的项目描述...",
    "decomposition_context": "结构化的分解上下文..."
  },
  "confidence": 0.85,
  "execution_time": 0.456,
  "metadata": {
    "processed_at": "2025-11-05T23:45:03.456Z",
    "request_length": 200
  }
}
```

## 4. Error Handling

### 4.1 Error Response Format
All error responses follow this format:
```json
{
  "skill_name": "string",
  "status": "ERROR",
  "result": null,
  "confidence": 0.0,
  "execution_time": 0.0,
  "error_message": "Human-readable error message",
  "metadata": {
    "processed_at": "timestamp",
    "error_type": "ErrorClass",
    "request_length": 0
  }
}
```

### 4.2 Common Error Codes
- `CONTEXT_TOO_LONG`: Input context exceeds maximum allowed length
- `INVALID_TEMPLATE`: Requested template does not exist
- `INVALID_PARAMETERS`: Required parameters missing or invalid
- `PROCESSING_ERROR`: Internal error during skill execution

## 5. Performance Characteristics

### 5.1 Response Time SLAs
- Context Analysis: < 200ms (95th percentile)
- Context Optimization: < 300ms (95th percentile)  
- Cognitive Template Application: < 100ms (95th percentile)
- System Operations: < 500ms (95th percentile)

### 5.2 Rate Limiting
- Default: 100 requests per minute per API key
- Burst: Up to 200 requests per minute
- Exceeding limits results in 429 status code

## 6. Security Considerations

### 6.1 Input Validation
- All text inputs are validated for length (max 50,000 characters)
- Special characters are sanitized to prevent injection
- Context content is not stored or logged

### 6.2 Authentication
- All endpoints require valid DNASPEC API tokens
- Tokens expire every 24 hours by default
- Support for API key rotation

## 7. Client Implementation Guidelines

### 7.1 Recommended Retry Strategy
- Exponential backoff with jitter
- Initial delay: 100ms, max delay: 5 seconds
- Retry on 5xx responses and network errors

### 7.2 Caching Recommendations
- Cache results for static contexts
- TTL: 1 hour for analysis results
- Implement cache invalidation on context changes

## 8. Versioning

### 8.1 API Versioning
- Version specified in URL path: `/v1/contexts/`
- Maintains backward compatibility within major versions
- Breaking changes result in new major version

### 8.2 Skill Versioning
- Each skill has internal version (1.0.0)
- Version reported in SkillResult metadata
- Version compatibility maintained within major frameworks