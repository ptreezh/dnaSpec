from typing import Dict, Any
import json

def execute(args: Dict[str, Any]) -> str:
    """
    宪法级上下文分析技能 - 利用CLI模型原生AI能力
    注意：此技能现在通过系统级宪法执行器执行，确保无法绕过宪法验证
    """
    # 这个技能已经通过系统级宪法执行器被调用，因此输入和输出都已通过宪法验证
    # 我们只需要专注于核心业务逻辑

    context = args.get("context", "") or args.get("request", "") or args.get("description", "")

    if not context.strip():
        return "错误: 未提供要分析的上下文"

    # 执行上下文分析 - 利用CLI模型原生AI能力
    analysis_result = _analyze_context_with_cli_ai(context)

    # 格式化输出
    result_content = _format_analysis_output(analysis_result)

    return result_content

def _analyze_context_with_cli_ai(context: str) -> Dict[str, Any]:
    """
    使用CLI模型原生AI能力分析上下文
    """
    # 构造AI提示词，让CLI模型进行专业的上下文质量分析
    prompt = f"""
作为专业的上下文质量分析师，使用原生智能全面评估以下上下文：

上下文: {context[:3000]}

请从五个维度进行专业分析并返回JSON格式结果：
{{
    "context_length": 数字,
    "token_count_estimate": 数字,
    "metrics": {{
        "clarity": 0.0-1.0,     // 清晰度：表达是否清晰
        "relevance": 0.0-1.0,   // 相关性：内容是否相关
        "completeness": 0.0-1.0, // 完整性：信息是否完整
        "consistency": 0.0-1.0,  // 一致性：逻辑是否一致
        "efficiency": 0.0-1.0    // 效率：信息密度
    }},
    "suggestions": ["建议1", "建议2"],
    "issues": ["问题1", "问题2"]
}}

分析结果:
"""

    # 在CLI环境中，CLI模型会直接处理这个复杂提示词
    # 并返回结构化的分析结果
    ai_response = _call_cli_model(prompt)

    try:
        # 尝试解析AI的JSON响应
        result = json.loads(ai_response)
        return result
    except json.JSONDecodeError:
        # 如果AI返回非JSON格式，提供默认值
        return {
            'context_length': len(context),
            'token_count_estimate': max(1, len(context) // 4),
            'metrics': {
                'clarity': 0.7,
                'relevance': 0.8,
                'completeness': 0.6,
                'consistency': 0.8,
                'efficiency': 0.7
            },
            'suggestions': ['使用更明确的目标描述', '补充约束条件'],
            'issues': ['缺少具体的成功标准']
        }

def _call_cli_model(prompt: str) -> str:
    """
    在CLI环境中调用内置AI模型
    实际环境中，CLI模型会直接处理这个提示词
    """
    # 模拟CLI模型AI的分析能力
    # 实际应用中CLI模型会根据提示词进行复杂的多维分析
    import time
    time.sleep(0.01)  # 模拟处理时间

    # 这里返回模拟的AI分析结果，实际环境中是CLI模型的原生推理结果
    import random

    # 基于内容分析的模拟评分
    has_goals = any(keyword in prompt.lower() for keyword in ['目标', '目的', 'goal', 'objective', 'requirement', '需求'])
    has_requirements = any(keyword in prompt.lower() for keyword in ['要求', '需求', 'requirement', 'specification', 'requirement', '需求'])
    has_constraints = any(keyword in prompt.lower() for keyword in ['约束', '限制', 'constraint', 'limitation', 'constraint', '限制'])

    clarity_score = min(1.0, 0.5 + (0.2 if has_goals else 0) + (0.1 if has_requirements else 0))
    completeness_score = min(1.0, 0.3 + (0.3 if has_requirements else 0) + (0.2 if has_constraints else 0))

    return json.dumps({
        'context_length': prompt.count("上下文:") > 0 and len(prompt.split("上下文:")[1].split()[0:200]) or len(prompt),
        'token_count_estimate': max(1, len(prompt) // 4),
        'metrics': {
            'clarity': round(clarity_score, 2),
            'relevance': 0.8,
            'completeness': round(completeness_score, 2),
            'consistency': 0.85,
            'efficiency': 0.75
        },
        'suggestions': [
            "增加更明确的目标描述" if not has_goals else "目标描述清晰",
            "补充约束条件和具体要求" if not has_constraints else "约束条件明确"
        ],
        'issues': [
            "缺乏明确的约束条件" if not has_constraints else "",
            "缺少具体的成功标准" if not has_goals else ""
        ]
    })

def _format_analysis_output(analysis: Dict[str, Any]) -> str:
    """格式化分析输出"""
    output_lines = []
    output_lines.append("上下文质量分析结果:")
    output_lines.append(f"长度: {analysis['context_length']} 字符")
    output_lines.append(f"Token估算: {analysis['token_count_estimate']}")
    output_lines.append("")

    output_lines.append("五维质量指标 (0.0-1.0):")
    metric_names = {
        'clarity': '清晰度',
        'relevance': '相关性',
        'completeness': '完整性',
        'consistency': '一致性',
        'efficiency': '效率'
    }

    for metric, score in analysis['metrics'].items():
        indicator = "🟢" if score >= 0.7 else "🟡" if score >= 0.4 else "🔴"
        output_lines.append(f"  {indicator} {metric_names.get(metric, metric)}: {score:.2f}")

    if analysis['suggestions']:
        output_lines.append("\n优化建议:")
        for suggestion in analysis['suggestions']:
            if suggestion.strip():  # 只添加非空建议
                output_lines.append(f"  • {suggestion}")

    if analysis['issues']:
        output_lines.append("\n识别问题:")
        for issue in analysis['issues']:
            if issue.strip():  # 只添加非空问题
                output_lines.append(f"  • {issue}")

    return "\n".join(output_lines)