"""
Claude Skills 规范的上下文分析技能实现
符合 Claude 官方 Skills 规范
"""
import json
import re
from typing import Dict, Any


def execute_skill(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    Claude Skills 标准执行函数
    """
    try:
        # 从事件中提取参数
        context_input = event.get('context') or event.get('input') or event.get('query', '')
        
        if not context_input.strip():
            error_result = {
                "success": False,
                "error": "Context input is required",
                "input": context_input
            }
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(error_result)
            }

        # 简单的上下文分析（在实际实现中会调用AI模型）
        context_length = len(context_input)
        token_count_estimate = max(1, len(context_input) // 4)
        
        # 计算质量指标
        clarity = min(1.0, max(0.0, 0.5 + len(context_input) * 0.00001))
        relevance = min(1.0, max(0.0, 0.7 + (0.1 if any(kw in context_input.lower() for kw in ['system', 'function', 'task', 'requirement']) else 0)))
        completeness = min(1.0, max(0.0, 0.3 + (0.3 if any(kw in context_input.lower() for kw in ['constraint', 'requirement', 'goal']) else 0)))
        consistency = min(1.0, max(0.0, 0.8 - (0.2 if any(kw in context_input.lower() for kw in ['but', 'however']) else 0)))
        efficiency = min(1.0, max(0.0, 1.0 - len(context_input) * 0.00005))

        result_data = {
            "context_length": context_length,
            "token_count_estimate": token_count_estimate,
            "metrics": {
                "clarity": round(clarity, 2),
                "relevance": round(relevance, 2),
                "completeness": round(completeness, 2),
                "consistency": round(consistency, 2),
                "efficiency": round(efficiency, 2)
            },
            "suggestions": [
                "Add more specific goal descriptions",
                "Supplement constraint conditions and specific requirements",
                "Improve expression clarity"
            ],
            "issues": [i for i in [
                "Lack of explicit constraint conditions" if completeness < 0.6 else "",
                "Some expressions can be more precise" if clarity < 0.7 else ""
            ] if i],  # Filter out empty issues
            "confidence": 0.85
        }

        success_result = {
            "success": True,
            "result": result_data,
            "input": context_input
        }
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(success_result)
        }
        
    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'input': event
        }
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(error_result)
        }


def lambda_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    AWS Lambda 兼容的处理函数
    """
    return execute_skill(event, context)


# 同时保留 DNASPEC 格式的 execute 函数以保持兼容性
def execute(args: Dict[str, Any]) -> str:
    """
    DNASPEC 格式的执行函数
    """
    context_input = args.get("context", args.get("description", args.get("input", "")))
    
    if not context_input.strip():
        return json.dumps({
            'success': False,
            'error': 'Context input is required',
            'result': None
        }, ensure_ascii=False)

    # 执行分析逻辑
    context_length = len(context_input)
    token_count_estimate = max(1, len(context_input) // 4)
    
    # 计算质量指标
    clarity = min(1.0, max(0.0, 0.5 + len(context_input) * 0.00001))
    relevance = min(1.0, max(0.0, 0.7 + (0.1 if any(kw in context_input.lower() for kw in ['system', 'function', 'task', 'requirement']) else 0)))
    completeness = min(1.0, max(0.0, 0.3 + (0.3 if any(kw in context_input.lower() for kw in ['constraint', 'requirement', 'goal']) else 0)))
    consistency = min(1.0, max(0.0, 0.8 - (0.2 if any(kw in context_input.lower() for kw in ['but', 'however']) else 0)))
    efficiency = min(1.0, max(0.0, 1.0 - len(context_input) * 0.00005))

    result_data = {
        "context_length": context_length,
        "token_count_estimate": token_count_estimate,
        "metrics": {
            "clarity": round(clarity, 2),
            "relevance": round(relevance, 2),
            "completeness": round(completeness, 2),
            "consistency": round(consistency, 2),
            "efficiency": round(efficiency, 2)
        },
        "suggestions": [
            "Add more specific goal descriptions",
            "Supplement constraint conditions and specific requirements", 
            "Improve expression clarity"
        ],
        "issues": [i for i in [
            "Lack of explicit constraint conditions" if completeness < 0.6 else "",
            "Some expressions can be more precise" if clarity < 0.7 else ""
        ] if i],  # Filter out empty issues
        "confidence": 0.85
    }

    # 返回格式化的分析结果
    output_lines = []
    output_lines.append("Context Quality Analysis Results:")
    output_lines.append(f"Length: {result_data['context_length']} characters")
    output_lines.append(f"Token Estimate: {result_data['token_count_estimate']}")
    output_lines.append("")

    output_lines.append("Five-Dimensional Quality Metrics (0.0-1.0):")
    metric_names = {
        'clarity': 'Clarity', 'relevance': 'Relevance', 'completeness': 'Completeness',
        'consistency': 'Consistency', 'efficiency': 'Efficiency'
    }

    for metric, score in result_data['metrics'].items():
        indicator = "🟢" if score >= 0.7 else "🟡" if score >= 0.4 else "🔴"
        output_lines.append(f"  {indicator} {metric_names.get(metric, metric)}: {score:.2f}")

    if result_data.get('suggestions'):
        output_lines.append("\nOptimization Suggestions:")
        for s in result_data['suggestions'][:3]:  # Show top 3 suggestions
            output_lines.append(f"  • {s}")

    if result_data.get('issues'):
        output_lines.append("\nIdentified Issues:")
        for i in result_data['issues']:
            output_lines.append(f"  • {i}")

    return "\n".join(output_lines)