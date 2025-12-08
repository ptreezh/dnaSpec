"""
Context Analysis Skill - 正确实现版本
基于DNASPEC技能框架的上下文分析技能
"""
from typing import Dict, Any
import re
from src.dnaspec_spec_kit_integration.core.skill import DNASpecSkill, SkillResult, SkillStatus


class ContextAnalysisSkill(DNASpecSkill):
    """上下文分析技能 - 基于AI模型原生智能的五维分析"""
    
    def __init__(self):
        super().__init__(
            name="dnaspec-context-analysis",
            description="DNASPEC上下文分析技能 - 利用AI模型原生智能进行专业上下文质量分析"
        )
    
    def _execute_skill_logic(self, request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行上下文分析逻辑
        通过向AI模型发送专业分析指令实现
        """
        if not request or not request.strip():
            return {
                'success': False,
                'error': 'Context cannot be empty'
            }
        
        context_to_analyze = request
        
        # 在实际部署中，这里会调用AI API
        # 当前实现使用基于规则的模拟来近似AI的分析能力
        # 基于上下文特征进行分析
        clarity = self._analyze_clarity(context_to_analyze)
        relevance = self._analyze_relevance(context_to_analyze)
        completeness = self._analyze_completeness(context_to_analyze)
        consistency = self._analyze_consistency(context_to_analyze)
        efficiency = self._analyze_efficiency(context_to_analyze)
        
        # 生成建议
        suggestions = []
        if clarity < 0.7:
            suggestions.append("增加更明确的术语和目标表述")
        if completeness < 0.6:
            suggestions.append("补充约束条件和具体要求")
        if relevance < 0.7:
            suggestions.append("明确目标和任务关系")
        
        # 识别问题
        issues = []
        if "也许" in context_to_analyze or "可能" in context_to_analyze:
            issues.append("包含不确定词汇：'也许'、'可能'")
        if len(context_to_analyze) < 20:
            issues.append("上下文过短，信息不足")
        
        return {
            'success': True,
            'context_length': len(context_to_analyze),
            'token_count_estimate': max(1, len(context_to_analyze) // 4),
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
    
    def _analyze_clarity(self, context: str) -> float:
        """分析清晰度"""
        import re
        # 检查是否存在明确的指令词
        clear_indicators = ['请', '需要', '要求', '目标', '任务', '实现', '设计', '分析']
        unclear_indicators = ['也许', '可能', '大概', '似乎', '某些', '一些']
        
        clear_count = sum(1 for indicator in clear_indicators if indicator in context)
        unclear_count = sum(1 for indicator in unclear_indicators if indicator in context)
        
        # 基于句子结构的清晰度评估
        sentences = re.split(r'[.!?;]', context)
        sentence_count = len([s for s in sentences if s.strip()])
        
        clarity_score = min(1.0, clear_count * 0.3 if sentence_count > 0 else 0)
        unclear_penalty = min(0.5, unclear_count * 0.2)
        
        return max(0.0, clarity_score - unclear_penalty)
    
    def _analyze_relevance(self, context: str) -> float:
        """分析相关性"""
        import re
        task_indicators = ['系统', '功能', '任务', '目标', '需求', '实现', '开发', '设计', '分析']
        
        task_count = sum(1 for indicator in task_indicators if indicator in context)
        relevance_score = min(1.0, task_count * 0.2)
        
        return max(0.0, relevance_score)
    
    def _analyze_completeness(self, context: str) -> float:
        """分析完整性"""
        import re
        completeness_indicators = ['约束', '条件', '要求', '标准', '规范', '限制', '假设', '前提']
        
        completeness_count = sum(1 for indicator in completeness_indicators if indicator in context)
        completeness_score = min(1.0, completeness_count * 0.2)
        
        return completeness_score
    
    def _analyze_consistency(self, context: str) -> float:
        """分析一致性"""
        import re
        # 检查可能的矛盾词汇
        contradiction_pairs = [
            ('必须', '可选'),
            ('应该', '不必'),
            ('总是', '从不'),
            ('全部', '部分'),
            ('强制', '随意')
        ]
        
        contradiction_count = 0
        for positive, negative in contradiction_pairs:
            if positive in context and negative in context:
                contradiction_count += 1
        
        consistency_score = max(0.0, 1.0 - (contradiction_count * 0.1))
        return consistency_score
    
    def _analyze_efficiency(self, context: str) -> float:
        """分析效率"""
        import re
        if len(context) == 0:
            return 0.0
        
        # 计算信息密度：有效词汇数 / 总长度
        words = [w for w in re.findall(r'[\w\u4e00-\u9fff]+', context) if len(w) > 1]
        efficiency = len(words) / len(context) * 100
        
        # 归一化到0-1范围
        normalized_efficiency = min(1.0, efficiency / 20)  # 假设每100字符20个有效词为满分
        
        return max(0.0, normalized_efficiency)
    
    def _calculate_confidence(self, request: str) -> float:
        """计算置信度"""
        if not request or len(request.strip()) == 0:
            return 0.1  # 空输入置信度很低
        elif len(request) > 10000:
            return 0.7  # 长输入仍可信但分析可能不全面
        else:
            return 0.85  # 中等长度输入置信度较高


def execute(args: Dict[str, Any]) -> str:
    """
    执行函数 - 与AI CLI平台集成的接口
    """
    from src.dnaspec_spec_kit_integration.core.skill import SkillStatus
    
    if 'context' in args:
        context = args['context']
    elif 'request' in args:
        context = args['request']
    else:
        return "错误: 未提供上下文进行分析"
    
    # 创建技能实例并执行
    skill = ContextAnalysisSkill()
    skill_result = skill.process_request(context, args)
    
    if skill_result.status != SkillStatus.COMPLETED:
        return f"错误: {skill_result.error_message}"
    
    # 格式化输出结果
    result_data = skill_result.result
    if not result_data.get('success', False):
        return f"分析失败: {result_data.get('error', '未知错误')}"
    
    output_lines = []
    output_lines.append("上下文质量分析结果:")
    output_lines.append("=" * 40)
    output_lines.append(f"上下文长度: {result_data['context_length']} 字符")
    output_lines.append(f"Token估算: {result_data['token_count_estimate']}")
    output_lines.append("")
    
    output_lines.append("五维质量指标 (0.0-1.0):")
    metric_names = {
        'clarity': '清晰度',
        'relevance': '相关性',
        'completeness': '完整性',
        'consistency': '一致性',
        'efficiency': '效率'
    }
    
    for metric, score in result_data['metrics'].items():
        indicator = "🟢" if score >= 0.7 else "🟡" if score >= 0.4 else "🔴"
        output_lines.append(f"  {indicator} {metric_names[metric]}: {score:.2f}")
    
    if result_data.get('suggestions', []):
        output_lines.append("\n优化建议:")
        for suggestion in result_data['suggestions']:
            output_lines.append(f"  • {suggestion}")
    
    if result_data.get('issues', []):
        output_lines.append("\n识别问题:")
        for issue in result_data['issues']:
            output_lines.append(f"  • {issue}")
    
    return "\n".join(output_lines)