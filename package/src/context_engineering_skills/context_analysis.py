"""
Context Analysis Skill
用于分析和评估上下文的有效性
"""
from typing import Dict, Any, List, Optional
import re
from src.dsgs_spec_kit_integration.core.skill import DSGSSkill, SkillResult, SkillStatus


class ContextAnalysisSkill(DSGSSkill):
    """
    上下文分析技能
    分析当前上下文的有效性，识别缺失信息，并推荐优化策略
    """
    
    def __init__(self):
        super().__init__(
            name="dsgs-context-analysis",
            description="DSGS上下文分析器 - 分析上下文有效性和质量的专家"
        )
        self.analysis_metrics = [
            'clarity',      # 清晰度
            'relevance',    # 相关性
            'completeness', # 完整性
            'consistency',  # 一致性
            'efficiency'    # 效率
        ]
    
    def _execute_skill_logic(self, request: str, context: Dict[str, Any]) -> Any:
        """
        执行上下文分析逻辑
        """
        context_to_analyze = request  # request参数是我们要分析的上下文
        
        # 如果是空上下文，直接返回默认值
        if not context_to_analyze:
            return {
                'context_length': 0,
                'token_count': 0,
                'metrics': {metric: 0.0 for metric in self.analysis_metrics},
                'suggestions': [],
                'issues': []
            }
        
        results = {
            'context_length': len(context_to_analyze),
            'token_count': self._estimate_tokens(context_to_analyze),
            'metrics': {},
            'suggestions': [],
            'issues': []
        }
        
        # 分析各项指标
        results['metrics']['clarity'] = self._analyze_clarity(context_to_analyze)
        results['metrics']['relevance'] = self._analyze_relevance(context_to_analyze)
        results['metrics']['completeness'] = self._analyze_completeness(context_to_analyze)
        results['metrics']['consistency'] = self._analyze_consistency(context_to_analyze)
        results['metrics']['efficiency'] = self._analyze_efficiency(context_to_analyze)
        
        # 生成建议和问题
        results['suggestions'] = self._generate_suggestions(results)
        results['issues'] = self._identify_issues(context_to_analyze)
        
        return results
    
    def _estimate_tokens(self, text: str) -> int:
        """
        估算token数量（使用粗略估算）
        """
        # 简单估算：每4个字符约等于1个token
        return max(1, len(text) // 4)
    
    def _analyze_clarity(self, context: str) -> float:
        """
        分析上下文的清晰度
        """
        # 检查句子结构和明确性
        sentences = re.split(r'[.!?]+', context)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0.0
        
        # 计算明确指令的比例
        clear_indicators = ['请', '需要', '要求', '目标', '任务', '执行', '实现']
        ambiguous_indicators = ['也许', '可能', '大概', '似乎', '好像']
        
        clear_count = sum(1 for s in sentences for indicator in clear_indicators if indicator in s)
        ambiguous_count = sum(1 for s in sentences for indicator in ambiguous_indicators if indicator in s)
        
        clarity_score = max(0, min(1, clear_count / len(sentences) if sentences else 0))
        ambiguity_penalty = min(0.5, ambiguous_count / len(sentences) if sentences else 0)
        
        return max(0, clarity_score - ambiguity_penalty)
    
    def _analyze_relevance(self, context: str) -> float:
        """
        分析上下文的相关性
        """
        # 这里可以使用更复杂的算法，如TF-IDF或语义分析
        # 简单实现：检查是否有明确的上下文主题相关词汇
        task_indicators = [
            '任务', '目标', '问题', '需求', '功能', '系统', '项目', '开发', '设计', '分析'
        ]
        
        relevance_count = sum(1 for indicator in task_indicators if indicator in context)
        return min(1.0, relevance_count / max(1, len(task_indicators) / 5))
    
    def _analyze_completeness(self, context: str) -> float:
        """
        分析上下文的完整性
        """
        completeness_indicators = [
            '假设', '约束', '要求', '条件', '规则', '限制', '规范', '标准'
        ]
        
        completeness_count = sum(1 for indicator in completeness_indicators if indicator in context)
        return min(1.0, completeness_count / max(1, len(completeness_indicators) / 3))
    
    def _analyze_consistency(self, context: str) -> float:
        """
        分析上下文的一致性
        """
        # 检查是否有矛盾的表述
        contradictions = [
            ('必须', '可以'), ('应该', '不必'), ('总是', '从不'), ('所有', '没有')
        ]
        
        contradiction_count = 0
        for pos, neg in contradictions:
            if pos in context and neg in context:
                contradiction_count += 1
        
        # 计算一致性得分
        consistency_score = 1.0 - (contradiction_count * 0.2)  # 每个矛盾减少0.2分
        return max(0.0, consistency_score)
    
    def _analyze_efficiency(self, context: str) -> float:
        """
        分析上下文的效率（信息密度）
        """
        if len(context) == 0:
            return 0.0
        
        # 简单计算：有效信息词数 / 总字符数
        words = re.findall(r'[\w]+', context)
        useful_words = [w for w in words if len(w) > 2]  # 过滤短词
        
        efficiency = len(useful_words) / len(context) * 100
        return min(1.0, efficiency / 10)  # 标准化到0-1范围
    
    def _generate_suggestions(self, analysis: Dict[str, Any]) -> List[str]:
        """
        根据分析结果生成建议
        """
        suggestions = []
        
        metrics = analysis['metrics']
        
        if metrics['clarity'] < 0.5:
            suggestions.append("增加更明确的指令和目标描述")
        
        if metrics['relevance'] < 0.5:
            suggestions.append("确保上下文与任务高度相关")
        
        if metrics['completeness'] < 0.5:
            suggestions.append("添加更多约束条件和要求说明")
        
        if metrics['consistency'] < 0.8:
            suggestions.append("检查并消除上下文中的矛盾信息")
        
        if metrics['efficiency'] < 0.5:
            suggestions.append("精简冗余信息，提高信息密度")
        
        return suggestions
    
    def _identify_issues(self, context: str) -> List[str]:
        """
        识别上下文中的问题
        """
        issues = []
        
        # 检查过长的上下文
        if len(context) > 4000:  # 假设超过4000字符为过长
            issues.append("上下文过长，可能超出模型上下文窗口限制")
        
        # 检查模糊用词
        ambiguous_words = ['一些', '某些', '很多', '大量', '部分', '很多']
        for word in ambiguous_words:
            if word in context:
                issues.append(f"使用了模糊词汇: '{word}'，建议具体化")
        
        # 检查缺少关键信息
        required_elements = ['目标', '要求', '约束']
        missing_elements = [elem for elem in required_elements if elem not in context]
        if missing_elements:
            issues.append(f"缺少关键信息元素: {', '.join(missing_elements)}")
        
        return issues
    
    def _calculate_confidence(self, request: str) -> float:
        """
        计算分析置信度
        """
        if len(request) < 10:
            return 0.3  # 上下文太短，置信度低
        elif len(request) > 10000:
            return 0.6  # 上下文太长，分析可能不准确
        else:
            return 0.85  # 适中长度，高置信度


def execute(args: Dict[str, Any]) -> str:
    """
    执行上下文分析技能 - 兼容现有接口
    """
    context_to_analyze = args.get("context", "") or args.get("request", "")
    if not context_to_analyze:
        return "错误: 未提供需要分析的上下文"
    
    skill = ContextAnalysisSkill()
    result = skill.process_request(context_to_analyze, args)
    
    if result.status == SkillStatus.ERROR:
        return f"错误: {result.error_message}"
    
    # 格式化输出结果
    analysis = result.result
    output = []
    output.append("上下文分析结果:")
    output.append(f"上下文长度: {analysis['context_length']} 字符")
    output.append(f"估算Token数: {analysis['token_count']}")
    output.append("")
    
    output.append("各项指标评分 (0.0-1.0):")
    for metric, score in analysis['metrics'].items():
        metric_names = {
            'clarity': '清晰度',
            'relevance': '相关性', 
            'completeness': '完整性',
            'consistency': '一致性',
            'efficiency': '效率'
        }
        output.append(f"  {metric_names.get(metric, metric)}: {score:.2f}")
    output.append("")
    
    if analysis['issues']:
        output.append("识别到的问题:")
        for issue in analysis['issues']:
            output.append(f"  • {issue}")
        output.append("")
    
    if analysis['suggestions']:
        output.append("优化建议:")
        for suggestion in analysis['suggestions']:
            output.append(f"  • {suggestion}")
    
    return "\n".join(output)