"""
context_analysis.py
上下文分析技能 - 符合Claude Skills规范
"""
from typing import Dict, Any, List
import re
from datetime import datetime

def execute(args: Dict[str, Any]) -> str:
    """
    Claude Skills标准执行入口
    """
    context = args.get("context", "") or args.get("request", "") or args.get("description", "")
    detailed = args.get("detailed", False)
    
    if not context.strip():
        return "❌ 错误: 未提供要分析的上下文"
    
    # 执行上下文分析
    analysis_result = perform_context_analysis(context)
    
    # 格式化输出
    return format_analysis_output(analysis_result, detailed)


def perform_context_analysis(context: str) -> Dict[str, Any]:
    """
    执行上下文分析 - 定量分析部分
    """
    # 分析上下文特征
    has_goals = bool(re.search(r'(目标|目的|goal|objective|requirement|需求)', context, re.IGNORECASE))
    has_requirements = bool(re.search(r'(要求|需求|requirement|specification|需要|需要)', context, re.IGNORECASE))
    has_constraints = bool(re.search(r'(约束|限制|constraint|limitation|限制|条件)', context, re.IGNORECASE))
    has_structure = bool(re.search(r'(^#+\s|^##+\s|^-\s|^\d+\.)', context, re.MULTILINE))
    
    # 计算五维质量指标
    clarity_score = 0.5
    if has_goals:
        clarity_score += 0.2
    if has_requirements:
        clarity_score += 0.15
    clarity_score = min(1.0, clarity_score)
    
    relevance_score = 0.7  # 基础相关性
    if has_goals or has_requirements:
        relevance_score += 0.1
    relevance_score = min(1.0, relevance_score)
    
    completeness_score = 0.3
    if has_requirements:
        completeness_score += 0.3
    if has_constraints:
        completeness_score += 0.2
    completeness_score = min(1.0, completeness_score)
    
    # 一致性：检查矛盾词汇
    contradiction_pairs = [
        ('必须', '可选'), ('应该', '不必'), ('总是', '从不'), ('全部', '部分'), ('强制', '随意')
    ]
    contradiction_count = sum(1 for pos, neg in contradiction_pairs if pos in context and neg in context)
    consistency_score = max(0.0, 0.9 - (contradiction_count * 0.15))
    
    # 效率：信息密度
    word_count = len([w for w in context.split() if len(w) > 1])
    efficiency_score = min(1.0, word_count / max(1, len(context) / 4))
    
    # 生成优化建议
    suggestions = []
    if not has_goals:
        suggestions.append("明确目标和预期结果")
    if not has_requirements:
        suggestions.append("补充具体的约束条件和要求")
    if contradiction_count > 0:
        suggestions.append(f"解决检测到的{contradiction_count}个逻辑矛盾")
    
    # 识别问题
    issues = []
    if contradiction_count > 0:
        issues.append(f"检测到逻辑矛盾: {contradiction_count}处")
    if len(context) < 20:
        issues.append("上下文过短，信息不足")
    if not has_structure and len(context) > 50:
        issues.append("缺乏清晰的结构组织")
    
    return {
        'context_length': len(context),
        'token_count_estimate': max(1, len(context) // 4),
        'metrics': {
            'clarity': round(clarity_score, 2),
            'relevance': round(relevance_score, 2),
            'completeness': round(completeness_score, 2),
            'consistency': round(consistency_score, 2),
            'efficiency': round(efficiency_score, 2)
        },
        'suggestions': suggestions,
        'issues': issues
    }


def format_analysis_output(analysis: Dict[str, Any], detailed: bool = False) -> str:
    """格式化分析输出"""
    output_lines = []
    output_lines.append("📋 上下文质量分析结果")
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
        output_lines.append("\n💡 优化建议:")
        for suggestion in analysis['suggestions'][:5]:  # 只显示前5个
            output_lines.append(f"  • {suggestion}")

    if analysis['issues']:
        output_lines.append("\n⚠️  识别问题:")
        for issue in analysis['issues']:
            output_lines.append(f"  • {issue}")

    if not detailed:
        output_lines.append("\n💡 使用 detailed=true 参数获取详细分析")
    
    return "\n".join(output_lines)


def get_manifest() -> Dict[str, Any]:
    """
    Claude Skills标准技能清单
    """
    return {
        "name": "dnaspec-context-analysis",
        "description": "分析上下文质量的技能，提供五维质量评估",
        "version": "1.0.0",
        "created_at": datetime.now().isoformat(),
        "parameters": {
            "type": "object",
            "properties": {
                "context": {
                    "type": "string",
                    "description": "要分析的上下文"
                },
                "request": {
                    "type": "string",
                    "description": "要分析的请求（context的别名）"
                },
                "description": {
                    "type": "string",
                    "description": "要分析的描述（context的别名）"
                },
                "detailed": {
                    "type": "boolean",
                    "description": "是否返回详细分析",
                    "default": False
                }
            },
            "required": ["context"]
        }
    }