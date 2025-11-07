"""
Context Optimization Skill - 符合DSGS原始规范的实现
为AI CLI平台提供上下文优化能力
"""
from typing import Dict, Any
import re


def execute(args: Dict[str, Any]) -> str:
    """
    执行上下文优化 - 与DSGS原始技能接口保持一致
    """
    context = args.get("context", "") or args.get("request", "") or args.get("description", "")
    optimization_goals = args.get("optimization_goals", "clarity,completeness")
    
    if not context.strip():
        return "错误: 未提供要优化的上下文"
    
    # 解析优化目标
    goals_list = [goal.strip() for goal in optimization_goals.split(",")]
    
    # 执行上下文优化
    optimization_result = _optimize_context_with_ai(context, goals_list)
    
    # 格式化输出结果
    output_lines = []
    output_lines.append("上下文优化结果:")
    output_lines.append(f"原始长度: {optimization_result['original_length']} 字符")
    output_lines.append(f"优化后长度: {optimization_result['optimized_length']} 字符")
    output_lines.append("")
    
    output_lines.append("应用的优化措施:")
    for optimization in optimization_result['applied_optimizations']:
        output_lines.append(f"  • {optimization}")
    
    output_lines.append("\n优化改进指标:")
    for metric, improvement in optimization_result['improvement_metrics'].items():
        direction = "↗️" if improvement > 0 else "↘️" if improvement < 0 else "➡️"
        change_str = f"{improvement:+.2f}" if improvement != 0 else f"{improvement:.2f}"
        output_lines.append(f"  {direction} {metric}: {change_str}")
    
    output_lines.append("\n优化后上下文:")
    output_lines.append(optimization_result['optimized_context'])
    
    return "\n".join(output_lines)


def _optimize_context_with_ai(context: str, goals: list) -> Dict[str, Any]:
    """
    使用AI模型优化上下文（模拟实现）
    """
    optimized_context = context
    applied_optimizations = []
    
    # 根据优化目标执行优化
    if 'clarity' in goals:
        optimized_context, clarity_ops = _apply_clarity_optimization(optimized_context)
        applied_optimizations.extend(clarity_ops)
    
    if 'relevance' in goals:
        optimized_context, relevance_ops = _apply_relevance_optimization(optimized_context)
        applied_optimizations.extend(relevance_ops)
    
    if 'completeness' in goals:
        optimized_context, completeness_ops = _apply_completeness_optimization(optimized_context)
        applied_optimizations.extend(completeness_ops)
    
    if 'conciseness' in goals:
        optimized_context, conciseness_ops = _apply_conciseness_optimization(optimized_context)
        applied_optimizations.extend(conciseness_ops)
    
    # 计算改进指标
    improvement_metrics = _calculate_improvements(context, optimized_context, applied_optimizations)
    
    return {
        'original_context': context,
        'optimized_context': optimized_context,
        'original_length': len(context),
        'optimized_length': len(optimized_context),
        'applied_optimizations': applied_optimizations,
        'improvement_metrics': improvement_metrics
    }


def _apply_clarity_optimization(context: str) -> tuple:
    """应用清晰度优化"""
    optimizations = []
    optimized = context
    
    # 替换模糊词汇为明确表述
    replacements = {
        '需要': '请明确需要',
        '大概': '具体为',
        '可能': '在特定条件下为',
        '也许': '在某些情况下为',
        '一些': '具体数量的',
        '某些': '特定的'
    }
    
    for old_word, new_phrase in replacements.items():
        if old_word in context:
            optimized = optimized.replace(old_word, new_phrase)
            optimizations.append(f"提升清晰度: 将'{old_word}'替换为'{new_phrase}'")
    
    # 增加明确指令前缀
    if not any(indicator in optimized for indicator in ['请', '要求', '目标']):
        optimized = f"请明确 {optimized}"
        optimizations.append("增加明确指令前缀: 添加'请明确'")
    
    return optimized, optimizations


def _apply_relevance_optimization(context: str) -> tuple:
    """应用相关性优化"""
    optimizations = []
    optimized = context
    
    # 增加与目标的相关表述
    if '系统' in context and '目标' not in context:
        optimized += " 目标是创建高效、可靠的系统。"
        optimizations.append("增强相关性: 补充系统目标说明")
    
    if '功能' in context and '用户' not in context and '客户' not in context:
        optimized += " 主要考虑用户需求和体验。"
        optimizations.append("增强相关性: 补充用户视角")
    
    return optimized, optimizations


def _apply_completeness_optimization(context: str) -> tuple:
    """应用完整性优化"""
    optimizations = []
    optimized = context
    
    # 补充常见缺失要素
    if not any(indicator in context for indicator in ['约束', '要求', '条件', '限制']):
        optimized += "\n\n约束条件: 需要在指定时间内完成"
        optimizations.append("补充约束条件")
    
    if not any(indicator in context for indicator in ['目标', '目的', '成功标准', '验收标准']):
        optimized += "\n明确目标: 实现预期功能并满足质量要求"
        optimizations.append("补充明确目标")
    
    if not any(indicator in context for indicator in ['假设', '前提', '基础条件']):
        optimized += "\n前置假设: 具备必要的开发资源和技术支持"
        optimizations.append("补充前提假设")
    
    return optimized, optimizations


def _apply_conciseness_optimization(context: str) -> tuple:
    """应用简洁性优化"""
    optimizations = []
    optimized = context
    
    # 去除重复内容（简单实现）
    sentences = re.split(r'([。！？.!?]+)', context)
    
    # 合并句子和标点
    parts = []
    for i in range(0, len(sentences), 2):
        if i + 1 < len(sentences):
            parts.append(sentences[i] + sentences[i+1])
        elif i < len(sentences):
            parts.append(sentences[i])
    
    # 去除重复句子（简单去重）
    unique_parts = []
    seen = set()
    for part in parts:
        clean_part = re.sub(r'\s+', ' ', part.strip())
        if clean_part and clean_part not in seen:
            unique_parts.append(part)
            seen.add(clean_part)
    
    if len(unique_parts) < len(parts):
        optimized = ''.join(unique_parts)
        optimizations.append("移除重复内容")
    
    # 简化冗长表述
    simplifications = [
        ('尽可能的', ''),
        ('最大程度上', ''),
        ('在某种程度上', ''),
        ('可以说', ''),
        ('基本上', '')
    ]
    
    for old_expr, new_expr in simplifications:
        original_len = len(optimized)
        optimized = optimized.replace(old_expr, new_expr)
        if len(optimized) < original_len:
            optimizations.append(f"简化表述: 移除'{old_expr}'")
    
    return optimized, optimizations


def _calculate_improvements(original: str, optimized: str, applied_optimizations: list) -> Dict[str, float]:
    """
    计算优化改进指标
    """
    # 简化实现：基于优化措施的数量和类型评估改进
    improvements = {}
    
    optimization_types = [op.split(':')[0] for op in applied_optimizations]
    
    improvements['clarity'] = 0.0
    improvements['relevance'] = 0.0
    improvements['completeness'] = 0.0
    improvements['conciseness'] = 0.0
    
    for opt_type in optimization_types:
        if '清晰度' in opt_type or '明确' in opt_type:
            improvements['clarity'] += 0.15
        elif '相关性' in opt_type:
            improvements['relevance'] += 0.1
        elif '完整性' in opt_type or '补充' in opt_type:
            improvements['completeness'] += 0.2
        elif '简洁性' in opt_type or '简化' in opt_type or '移除' in opt_type:
            # 简洁性改进：基于长度变化
            improvements['conciseness'] = (len(original) - len(optimized)) / len(original) if original else 0
    
    # 限制改进值在合理范围内
    for key in improvements:
        improvements[key] = max(-0.5, min(0.5, improvements[key]))
    
    return improvements