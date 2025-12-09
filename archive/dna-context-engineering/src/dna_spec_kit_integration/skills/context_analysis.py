"""
Context Analysis Skill - 符合DNASPEC原始规范的实现
为AI CLI平台提供上下文分析能力，与原始技能保持一致的接口
"""
from typing import Dict, Any
import re


def execute(args: Dict[str, Any]) -> str:
    """
    执行上下文分析 - 与DNASPEC原始技能接口保持一致
    """
    context = args.get("context", "") or args.get("request", "") or args.get("description", "")
    
    if not context.strip():
        return "错误: 未提供要分析的上下文"
    
    # 执行上下文分析 - 构造AI指令
    analysis_result = _analyze_context_with_ai(context)
    
    # 格式化输出结果
    output_lines = []
    output_lines.append("上下文质量分析结果:")
    output_lines.append(f"长度: {analysis_result['context_length']} 字符")
    output_lines.append(f"Token估算: {analysis_result['token_count_estimate']}")
    output_lines.append("")
    
    output_lines.append("五维质量指标 (0.0-1.0):")
    metric_names = {
        'clarity': '清晰度', 
        'relevance': '相关性',
        'completeness': '完整性', 
        'consistency': '一致性',
        'efficiency': '效率'
    }
    
    for metric, score in analysis_result['metrics'].items():
        indicator = "🟢" if score >= 0.7 else "🟡" if score >= 0.4 else "🔴"
        output_lines.append(f"  {indicator} {metric_names.get(metric, metric)}: {score:.2f}")
    
    if analysis_result['suggestions']:
        output_lines.append("\n优化建议:")
        for suggestion in analysis_result['suggestions'][:5]:  # 只显示前5个建议
            output_lines.append(f"  • {suggestion}")
    
    if analysis_result['issues']:
        output_lines.append("\n识别问题:")
        for issue in analysis_result['issues']:
            output_lines.append(f"  • {issue}")
    
    return "\n".join(output_lines)


def _analyze_context_with_ai(context: str) -> Dict[str, Any]:
    """
    使用AI模型分析上下文质量（模拟实现）
    """
    # 在实际实现中，这会调用AI API并解析响应
    # 当前实现基于上下文特征进行模拟分析
    clarity = _analyze_clarity(context)
    relevance = _analyze_relevance(context)
    completeness = _analyze_completeness(context)
    consistency = _analyze_consistency(context)
    efficiency = _analyze_efficiency(context)
    
    # 生成建议
    suggestions = []
    if clarity < 0.7:
        suggestions.append("增加更明确的术语和目标表述")
    if completeness < 0.6:
        suggestions.append("补充约束条件和具体要求")
    if relevance < 0.7:
        suggestions.append("明确目标和任务关联性")
    
    # 识别问题
    issues = []
    if "也许" in context or "可能" in context or "大概" in context:
        issues.append("包含不确定词汇：'也许'、'可能'、'大概'")
    if len(context) < 20:
        issues.append("上下文过短，信息不足")
    if "但是" in context and "因此" not in context:
        issues.append("包含转折但缺少结论逻辑")
    
    return {
        'context_length': len(context),
        'token_count_estimate': max(1, len(context) // 4),
        'metrics': {
            'clarity': round(clarity, 2),
            'relevance': round(relevance, 2),
            'completeness': round(completeness, 2),
            'consistency': round(consistency, 2),
            'efficiency': round(efficiency, 2)
        },
        'suggestions': suggestions,
        'issues': issues
    }


def _analyze_clarity(context: str) -> float:
    """分析清晰度"""
    clear_indicators = ['请', '需要', '要求', '目标', '任务', '实现', '设计', '分析', '如何', '怎样', '明确']
    unclear_indicators = ['也许', '可能', '大概', '似乎', '某些', '一些', '部分', '等等']
    
    clear_count = sum(1 for indicator in clear_indicators if indicator in context)
    unclear_count = sum(1 for indicator in unclear_indicators if indicator in context)
    
    # 基于句子和明确指令词计算清晰度
    sentences = re.split(r'[。！？.!?;；]', context)
    sentence_count = len([s for s in sentences if s.strip() and len(s.strip()) > 3])
    
    clarity_score = min(1.0, (clear_count * 0.3 + sentence_count * 0.05) if sentence_count > 0 else 0)
    unclear_penalty = min(0.5, unclear_count * 0.2)
    
    return max(0.0, clarity_score - unclear_penalty)


def _analyze_relevance(context: str) -> float:
    """分析相关性"""
    task_indicators = ['系统', '功能', '任务', '目标', '需求', '实现', '开发', '设计', '分析', '管理', '处理', '支持']
    
    task_count = sum(1 for indicator in task_indicators if indicator in context)
    relevance_score = min(1.0, task_count * 0.15)
    
    return max(0.0, relevance_score)


def _analyze_completeness(context: str) -> float:
    """分析完整性"""
    completeness_indicators = ['约束', '条件', '要求', '标准', '规范', '限制', '假设', '前提', '约束', '目标', '验收']
    
    completeness_count = sum(1 for indicator in completeness_indicators if indicator in context)
    completeness_score = min(1.0, completeness_count * 0.15)
    
    return completeness_score


def _analyze_consistency(context: str) -> float:
    """分析一致性"""
    # 检查逻辑矛盾
    contradiction_pairs = [
        ('必须', '可选'),
        ('应该', '不必'),
        ('总是', '从不'),
        ('全部', '部分'),
        ('强制', '随意'),
        ('要求', '可选'),
        ('必须', '可以')
    ]
    
    contradiction_count = 0
    for positive, negative in contradiction_pairs:
        if positive in context and negative in context:
            contradiction_count += 1
    
    # 一致性越高分数越高，矛盾越多分数越低
    consistency_score = max(0.0, 1.0 - (contradiction_count * 0.2))
    return consistency_score


def _analyze_efficiency(context: str) -> float:
    """分析效率（信息密度）"""
    if len(context) == 0:
        return 0.0
    
    # 计算信息密度：有效词汇数 / 总字符数
    words = [w for w in re.findall(r'[\w\u4e00-\u9fff]+', context) if len(w) > 1]
    efficiency = len(words) / len(context) * 100
    
    # 归一化到0-1范围（假设每100字符理想有25个有效词为满分）
    normalized_efficiency = min(1.0, efficiency / 25)
    
    return max(0.0, normalized_efficiency)