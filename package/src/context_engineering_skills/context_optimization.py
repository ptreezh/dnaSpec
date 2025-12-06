"""
Context Optimization Skill
用于优化和改进上下文质量
"""
from typing import Dict, Any, List
from src.dsgs_spec_kit_integration.core.skill import DSGSSkill, SkillResult, SkillStatus
from .context_analysis import ContextAnalysisSkill
import re


class ContextOptimizationSkill(DSGSSkill):
    """
    上下文优化技能
    基于分析结果优化上下文质量
    """
    
    def __init__(self):
        super().__init__(
            name="dsgs-context-optimization",
            description="DSGS上下文优化器 - 基于分析结果优化上下文质量的专家"
        )
        self.context_analyzer = ContextAnalysisSkill()
    
    def _execute_skill_logic(self, request: str, context: Dict[str, Any]) -> Any:
        """
        执行上下文优化逻辑
        """
        context_to_optimize = request
        optimization_goals = context.get('optimization_goals', ['clarity', 'relevance', 'completeness'])
        
        if isinstance(optimization_goals, str):
            optimization_goals = [goal.strip() for goal in optimization_goals.split(',')]
        
        # 分析原始上下文
        analysis_result = self.context_analyzer.process_request(context_to_optimize, context)
        original_analysis = analysis_result.result if analysis_result.status == SkillStatus.COMPLETED else {}
        
        # 根据目标进行优化
        optimized_context = context_to_optimize
        applied_optimizations = []
        
        if 'clarity' in optimization_goals:
            optimized_context, clarity_ops = self._optimize_clarity(optimized_context)
            applied_optimizations.extend(clarity_ops)
        
        if 'relevance' in optimization_goals:
            optimized_context, relevance_ops = self._optimize_relevance(optimized_context)
            applied_optimizations.extend(relevance_ops)
        
        if 'completeness' in optimization_goals:
            optimized_context, completeness_ops = self._optimize_completeness(optimized_context)
            applied_optimizations.extend(completeness_ops)
        
        if 'conciseness' in optimization_goals:
            optimized_context, conciseness_ops = self._optimize_conciseness(optimized_context)
            applied_optimizations.extend(conciseness_ops)
        
        # 分析优化后的上下文
        analysis_result_opt = self.context_analyzer.process_request(optimized_context, context)
        optimized_analysis = analysis_result_opt.result if analysis_result_opt.status == SkillStatus.COMPLETED else {}
        
        return {
            'original_context': context_to_optimize,
            'optimized_context': optimized_context,
            'original_analysis': original_analysis,
            'optimized_analysis': optimized_analysis,
            'applied_optimizations': applied_optimizations,
            'improvement_metrics': self._calculate_improvements(
                original_analysis, optimized_analysis
            )
        }
    
    def _optimize_clarity(self, context: str) -> tuple:
        """
        优化上下文的清晰度
        """
        operations = []
        
        # 将模糊词汇替换为具体词汇
        replacements = {
            r'\b一些\b': '具体数量',
            r'\b某些\b': '指定的',
            r'\b很多\b': '大量(例如100个以上)',
            r'\b部分\b': '特定部分',
            r'\b可能\b': '在特定条件下',
            r'\b也许\b': '在某些情况下'
        }
        
        optimized = context
        for pattern, replacement in replacements.items():
            if re.search(pattern, optimized):
                optimized = re.sub(pattern, replacement, optimized)
                operations.append(f"替换模糊词汇: {pattern} -> {replacement}")
        
        # 增加明确的指令
        if not any(indicator in optimized for indicator in ['请', '需要', '要求']):
            # 在上下文中添加明确指令
            sentences = re.split(r'[.!?]+', optimized)
            if sentences and len(sentences[0]) > 0:
                # 在开头添加明确指令
                instruction_added = f"请明确地 {sentences[0].strip()}" + ''.join([f"{s}." for s in sentences[1:] if s.strip()])
                if instruction_added != optimized:
                    optimized = instruction_added
                    operations.append("增加明确指令前缀")
        
        return optimized, operations
    
    def _optimize_relevance(self, context: str) -> tuple:
        """
        优化上下文的相关性
        """
        operations = []
        optimized = context
        
        # 移除不相关信息
        irrelevant_patterns = [
            r'\s*与任务无关的背景信息[^。]*[。]?',
            r'\s*这与主要目标没有任何关系[^。]*[。]?',
            r'\s*无关紧要的细节[^。]*[。]?'
        ]
        
        for pattern in irrelevant_patterns:
            matches = re.findall(pattern, optimized)
            if matches:
                operations.append(f"移除不相关信息: {matches[0][:50]}...")
                optimized = re.sub(pattern, '', optimized)
        
        return optimized, operations
    
    def _optimize_completeness(self, context: str) -> tuple:
        """
        优化上下文的完整性
        """
        operations = []
        optimized = context
        
        # 添加缺失的元素
        missing_elements = []
        
        if not any(indicator in context for indicator in ['约束', '限制', '要求']):
            missing_elements.append('约束条件')
        
        if not any(indicator in context for indicator in ['目标', '目的', '任务']):
            missing_elements.append('明确目标')
        
        if not any(indicator in context for indicator in ['假设', '前提', '条件']):
            missing_elements.append('前提假设')
        
        if missing_elements:
            additions = []
            for element in missing_elements:
                if element == '约束条件':
                    additions.append('约束条件: 需要在指定时间内完成')
                elif element == '明确目标':
                    additions.append('明确目标: 实现预期功能')
                elif element == '前提假设':
                    additions.append('前提假设: 有必要的资源支持')
            
            if additions:
                optimized += "\n\n" + "\n".join(additions)
                operations.extend([f"添加缺失元素: {element}" for element in missing_elements])
        
        return optimized, operations
    
    def _optimize_conciseness(self, context: str) -> tuple:
        """
        优化上下文的简洁性
        """
        operations = []
        optimized = context
        
        # 移除重复内容
        sentences = re.split(r'([.!?]+)', optimized)
        # 合并句子和标点
        parts = []
        for i in range(0, len(sentences), 2):
            if i + 1 < len(sentences):
                parts.append(sentences[i] + sentences[i+1])
            elif i < len(sentences):
                parts.append(sentences[i])
        
        unique_parts = []
        seen = set()
        for part in parts:
            clean_part = re.sub(r'\s+', ' ', part.strip())
            if clean_part and clean_part not in seen:
                unique_parts.append(part)
                seen.add(clean_part)
        
        if len(unique_parts) < len(parts):
            optimized = ''.join(unique_parts)
            operations.append("移除重复句子")
        
        # 移除冗余词语
        redundant_patterns = [
            r'\s+的\s+的\s+',  # 双重"的"
            r'\s+地\s+地\s+',  # 双重"地"
        ]
        
        for pattern in redundant_patterns:
            if re.search(pattern, optimized):
                optimized = re.sub(pattern, ' 的 ', optimized)
                operations.append(f"移除冗余词语: {pattern}")
        
        return optimized, operations
    
    def _calculate_improvements(self, original_analysis: Dict, optimized_analysis: Dict) -> Dict[str, float]:
        """
        计算优化改进指标
        """
        improvements = {}
        for metric in original_analysis.get('metrics', {}):
            original_score = original_analysis['metrics'].get(metric, 0)
            optimized_score = optimized_analysis['metrics'].get(metric, 0)
            improvements[metric] = optimized_score - original_score
        
        # 计算简洁度改进（通过长度变化）
        original_length = original_analysis.get('context_length', 0)
        optimized_length = optimized_analysis.get('context_length', 0)
        improvements['conciseness'] = (original_length - optimized_length) / original_length if original_length > 0 else 0
        
        return improvements
    
    def _calculate_confidence(self, request: str) -> float:
        """
        计算优化置信度
        """
        if len(request) < 10:
            return 0.4  # 上下文太短，优化效果有限
        elif len(request) > 10000:
            return 0.6  # 上下文太长，优化可能影响整体
        else:
            return 0.8  # 适中长度，合理置信度


def execute(args: Dict[str, Any]) -> str:
    """
    执行上下文优化技能 - 兼容现有接口
    """
    context_to_optimize = args.get("context", "") or args.get("request", "")
    if not context_to_optimize:
        return "错误: 未提供需要优化的上下文"
    
    # 准备上下文参数
    context_params = {
        'optimization_goals': args.get('optimization_goals', 'clarity,relevance,completeness')
    }
    
    skill = ContextOptimizationSkill()
    result = skill.process_request(context_to_optimize, context_params)
    
    if result.status == SkillStatus.ERROR:
        return f"错误: {result.error_message}"
    
    # 格式化输出结果
    optimization = result.result
    output = []
    output.append("上下文优化结果:")
    output.append(f"原始长度: {optimization['original_analysis']['context_length']} 字符")
    output.append(f"优化后长度: {optimization['optimized_analysis']['context_length']} 字符")
    output.append("")
    
    output.append("优化改进:")
    for metric, improvement in optimization['improvement_metrics'].items():
        if improvement > 0:
            output.append(f"  {metric}: +{improvement:.2f} (提升)")
        elif improvement < 0:
            output.append(f"  {metric}: {improvement:.2f} (下降)")
        else:
            output.append(f"  {metric}: {improvement:.2f} (无变化)")
    output.append("")
    
    output.append("应用的优化操作:")
    for op in optimization['applied_optimizations']:
        output.append(f"  • {op}")
    output.append("")
    
    output.append("优化后的上下文:")
    output.append(optimization['optimized_context'])
    
    return "\n".join(output)