# DNASPEC技能接口标准规范

## 1. 标准化输入接口

### 1.1 基本输入结构
所有技能应接受以下标准化输入参数：

```python
{
    "input": str,              # 主要输入内容（必填）
    "detail_level": str,       # 详细程度: "basic", "standard", "detailed"（可选，默认"standard"）
    "options": dict,           # 可选配置参数（可选）
    "context": dict            # 上下文信息（可选）
}
```

### 1.2 参数说明
- `input`: 技能处理的主要文本内容
- `detail_level`: 控制返回信息的详细程度
  - `basic`: 只返回核心信息
  - `standard`: 返回标准详细信息
  - `detailed`: 返回完整详细信息
- `options`: 技能特定的配置选项
- `context`: 提供额外的上下文信息

### 1.3 输入验证
技能应验证必要参数并返回标准化错误响应：

```python
{
    "status": "error",
    "error": {
        "type": "VALIDATION_ERROR",
        "message": "Missing required input parameter",
        "details": {
            "missing_fields": ["input"]
        }
    }
}
```

## 2. 标准化输出接口

### 2.1 成功响应格式
```python
{
    "status": "success",
    "data": {},                # 技能特定的返回数据
    "metadata": {
        "skill_name": str,     # 技能名称
        "execution_time": float, # 执行时间（秒）
        "confidence": float,    # 结果置信度（0.0-1.0）
        "detail_level": str    # 实际使用的详细程度
    }
}
```

### 2.2 错误响应格式
```python
{
    "status": "error",
    "error": {
        "type": str,           # 错误类型
        "message": str,        # 错误描述
        "code": str,           # 错误代码
        "details": {}          # 错误详情（可选）
    },
    "metadata": {
        "skill_name": str,
        "execution_time": float
    }
}
```

## 3. 渐进式信息披露实现

### 3.1 详细程度控制
技能应根据`detail_level`参数控制返回信息的详细程度：

- `basic`: 只返回核心结果，信息最少
- `standard`: 返回标准详细信息，平衡信息量和简洁性
- `detailed`: 返回完整信息，包括所有细节和元数据

### 3.2 示例
对于上下文分析技能：

**Basic级别**:
```python
{
    "status": "success",
    "data": {
        "overall_score": 0.75,
        "main_issues": ["缺乏明确目标", "信息不完整"]
    }
}
```

**Standard级别**:
```python
{
    "status": "success",
    "data": {
        "overall_score": 0.75,
        "metrics": {
            "clarity": 0.8,
            "completeness": 0.7,
            "relevance": 0.75
        },
        "issues": ["缺乏明确目标", "信息不完整"],
        "suggestions": ["明确任务目标", "补充约束条件"]
    }
}
```

**Detailed级别**:
```python
{
    "status": "success",
    "data": {
        "overall_score": 0.75,
        "metrics": {
            "clarity": 0.8,
            "completeness": 0.7,
            "relevance": 0.75,
            "consistency": 0.85,
            "efficiency": 0.65
        },
        "issues": ["缺乏明确目标", "信息不完整"],
        "suggestions": ["明确任务目标", "补充约束条件"],
        "detailed_analysis": {
            "clarity_breakdown": {...},
            "completeness_gaps": [...]
        }
    }
}
```

## 4. 技能实现规范

### 4.1 函数签名
```python
def execute(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行技能
    
    Args:
        args: 标准化输入参数
        
    Returns:
        标准化输出响应
    """
    pass
```

### 4.2 错误处理
所有技能应捕获异常并返回标准化错误响应：

```python
try:
    # 技能逻辑
    result = _process_skill_logic(input_text, detail_level, options)
    
    return {
        "status": "success",
        "data": result,
        "metadata": {
            "skill_name": "skill-name",
            "execution_time": execution_time,
            "confidence": confidence_score,
            "detail_level": detail_level
        }
    }
except ValidationError as e:
    return {
        "status": "error",
        "error": {
            "type": "VALIDATION_ERROR",
            "message": str(e),
            "code": "INVALID_INPUT"
        },
        "metadata": {
            "skill_name": "skill-name",
            "execution_time": execution_time
        }
    }
except Exception as e:
    return {
        "status": "error",
        "error": {
            "type": type(e).__name__,
            "message": str(e),
            "code": "EXECUTION_ERROR"
        },
        "metadata": {
            "skill_name": "skill-name",
            "execution_time": execution_time
        }
    }
```