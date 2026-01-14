"""
DNASPEC Context Analyzer Skill - 符合AgentSkills.io标准
基于TDD实现，遵循KISS、SOLID、YAGNI原则
"""
import json
import re
from typing import Dict, Any, List, Optional
from skills.dnaspec_skill_framework import (
    DNASpecSkillBase, 
    track_execution,
    create_quality_metrics,
    validate_text_input,
    SkillValidationError
)


@track_execution
class ContextAnalyzerSkill(DNASpecSkillBase):
    """
    上下文分析技能 - 多维度质量评估
    
    符合AgentSkills.io规范：
    - name: context-analyzer
    - description: Analyzes context quality across 5 dimensions
    - 支持5维质量分析：清晰度、相关性、完整性、一致性、效率性
    """
    
    def __init__(self):
        super().__init__(
            name="context-analyzer",
            description="Analyzes context quality across 5 dimensions (clarity, relevance, completeness, consistency, efficiency). Use when you need to evaluate document quality, assess requirement completeness, check communication effectiveness, or validate content before processing.",
            version="2.0.0"
        )
        
        # 质量阈值定义
        self.quality_thresholds = {
            'high': 0.7,
            'medium': 0.4,
            'low': 0.0
        }
        
        # 系统关键词（用于相关性分析）
        self.system_keywords = [
            'system', 'function', 'task', 'requirement', 'feature', 'component',
            '系统', '功能', '任务', '需求', '特性', '组件'
        ]
        
        # 约束关键词（用于完整性分析）
        self.constraint_keywords = [
            'constraint', 'goal', 'specification', 'limitation', 'rule',
            '约束', '目标', '规范', '限制', '规则'
        ]
        
        # 矛盾关键词（用于一致性分析）
        self.contradiction_keywords = [
            'but', 'however', 'although', 'despite', 'nevertheless',
            '但是', '然而', '虽然', '尽管', '不过'
        ]
    
    def validate_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证输入数据
        
        Args:
            input_data: 包含要分析的上下文内容的输入数据
            
        Returns:
            验证结果字典
        """
        # 验证必需字段
        if 'input' not in input_data:
            return {
                'valid': False, 
                'error': 'Missing required field: input'
            }
        
        # 验证输入内容
        input_validation = validate_text_input(input_data['input'], 'context')
        if not input_validation['valid']:
            return input_validation
        
        # 验证可选字段
        if 'analysis_depth' in input_data:
            depth = input_data['analysis_depth']
            if depth not in ['basic', 'standard', 'comprehensive']:
                return {
                    'valid': False,
                    'error': 'Invalid analysis_depth. Must be basic, standard, or comprehensive.'
                }
        
        if 'target_audience' in input_data:
            audience = input_data['target_audience']
            valid_audiences = ['technical', 'business', 'mixed', 'general']
            if audience not in valid_audiences:
                return {
                    'valid': False,
                    'error': f'Invalid target_audience. Must be one of: {", ".join(valid_audiences)}'
                }
        
        return {'valid': True}
    
    def execute_skill(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行上下文分析核心逻辑
        
        Args:
            input_data: 验证过的输入数据
            
        Returns:
            上下文分析结果
        """
        context_text = input_data['input']
        analysis_depth = input_data.get('analysis_depth', 'standard')
        target_audience = input_data.get('target_audience', 'technical')
        
        # 基础分析
        basic_analysis = self._perform_basic_analysis(context_text)
        
        # 深度分析
        deep_analysis = self._perform_deep_analysis(
            context_text, analysis_depth, target_audience
        )
        
        # 计算总体评分
        overall_score = self._calculate_overall_score(
            basic_analysis['quality_metrics']
        )
        
        # 生成建议
        suggestions = self._generate_suggestions(
            basic_analysis['quality_metrics'], 
            deep_analysis['issues'],
            analysis_depth
        )
        
        return {
            'context_length': basic_analysis['context_length'],
            'token_count_estimate': basic_analysis['token_count_estimate'],
            'quality_metrics': basic_analysis['quality_metrics'],
            'suggestions': suggestions,
            'issues': deep_analysis['issues'],
            'overall_score': overall_score,
            'analysis_metadata': {
                'depth': analysis_depth,
                'target_audience': target_audience,
                'detected_language': self._detect_language(context_text),
                'quality_level': self._determine_quality_level(overall_score)
            }
        }
    
    def _perform_basic_analysis(self, context_text: str) -> Dict[str, Any]:
        """
        执行基础分析
        
        Args:
            context_text: 要分析的文本
            
        Returns:
            基础分析结果
        """
        # 文本统计
        context_length = len(context_text)
        token_count_estimate = max(1, context_length // 4)  # 简单的token估算
        
        # 质量指标计算
        quality_metrics = create_quality_metrics(context_text)
        
        # 针对上下文分析的特定调整
        quality_metrics = self._adjust_metrics_for_context_analysis(
            context_text, quality_metrics
        )
        
        return {
            'context_length': context_length,
            'token_count_estimate': token_count_estimate,
            'quality_metrics': quality_metrics
        }
    
    def _perform_deep_analysis(
        self, 
        context_text: str, 
        analysis_depth: str, 
        target_audience: str
    ) -> Dict[str, Any]:
        """
        执行深度分析
        
        Args:
            context_text: 要分析的文本
            analysis_depth: 分析深度
            target_audience: 目标受众
            
        Returns:
            深度分析结果
        """
        issues = []
        
        # 根据分析深度执行不同级别的分析
        if analysis_depth in ['standard', 'comprehensive']:
            issues.extend(self._detect_clarity_issues(context_text))
            issues.extend(self._detect_completeness_issues(context_text))
        
        if analysis_depth == 'comprehensive':
            issues.extend(self._detect_consistency_issues(context_text))
            issues.extend(self._detect_audience_mismatch(context_text, target_audience))
        
        # 检测通用问题
        issues.extend(self._detect_general_issues(context_text))
        
        return {
            'issues': issues,
            'detailed_insights': self._generate_insights(context_text, analysis_depth)
        }
    
    def _adjust_metrics_for_context_analysis(
        self, 
        context_text: str, 
        quality_metrics: Dict[str, float]
    ) -> Dict[str, float]:
        """
        针对上下文分析调整质量指标
        
        Args:
            context_text: 上下文文本
            quality_metrics: 原始质量指标
            
        Returns:
            调整后的质量指标
        """
        text_lower = context_text.lower()
        
        # 相关性调整
        system_relevance = sum(1 for kw in self.system_keywords if kw in text_lower)
        quality_metrics['relevance'] = min(1.0, 0.5 + system_relevance * 0.1)
        
        # 完整性调整
        constraint_relevance = sum(1 for kw in self.constraint_keywords if kw in text_lower)
        quality_metrics['completeness'] = min(1.0, 0.3 + constraint_relevance * 0.15)
        
        # 一致性调整
        contradictions = sum(1 for kw in self.contradiction_keywords if kw in text_lower)
        quality_metrics['consistency'] = max(0.0, 0.9 - contradictions * 0.15)
        
        # 效率性调整
        if len(context_text) > 500:
            quality_metrics['efficiency'] = max(0.3, quality_metrics['efficiency'] - 0.1)
        
        return quality_metrics
    
    def _detect_clarity_issues(self, context_text: str) -> List[str]:
        """检测清晰度问题"""
        issues = []
        
        # 检测过长的句子
        sentences = re.split(r'[.!?。！？]', context_text)
        long_sentences = [s for s in sentences if len(s.strip()) > 100]
        if long_sentences:
            issues.append(f"Found {len(long_sentences)} overly long sentences that reduce clarity")
        
        # 检测模糊表达
        vague_patterns = [
            r'\b(some|somehow|somewhat|rather|quite|fairly)\b',
            r'\b(可能|也许|大概|可能地|一定程度上)\b'
        ]
        
        for pattern in vague_patterns:
            matches = len(re.findall(pattern, context_text, re.IGNORECASE))
            if matches > 2:
                issues.append(f"Too many vague expressions ({matches} instances)")
        
        return issues
    
    def _detect_completeness_issues(self, context_text: str) -> List[str]:
        """检测完整性问题"""
        issues = []
        text_lower = context_text.lower()
        
        # 检测缺少必要信息
        missing_indicators = [
            'not specified', 'to be determined', 'TBD', 'tbd',
            '未指定', '待定', '尚未确定', ' TBD '
        ]
        
        for indicator in missing_indicators:
            if indicator in text_lower:
                issues.append(f"Contains incomplete information: '{indicator}'")
        
        # 检测是否缺少关键约束
        if not any(kw in text_lower for kw in self.constraint_keywords):
            issues.append("Missing constraint specifications or requirements")
        
        return issues
    
    def _detect_consistency_issues(self, context_text: str) -> List[str]:
        """检测一致性问题"""
        issues = []
        text_lower = context_text.lower()
        
        # 检测矛盾表达
        contradictions = re.findall(
            r'\b(but|however|although|despite|但是|然而|虽然|尽管)\b.*',
            text_lower
        )
        
        if len(contradictions) > 3:
            issues.append(f"Multiple contradictory expressions found ({len(contradictions)} instances)")
        
        # 检测术语不一致
        words = re.findall(r'\b\w+\b', text_lower)
        word_counts = {}
        for word in words:
            if len(word) > 3:  # 忽略短词
                word_counts[word] = word_counts.get(word, 0) + 1
        
        # 检查是否有重复的含义相似的词
        similar_groups = [
            ['system', 'systems'],
            ['requirement', 'requirements'],
            ['function', 'functions', 'functionality'],
            ['系统', '系统架构'],
            ['功能', '功能性']
        ]
        
        for group in similar_groups:
            present_words = [w for w in group if w in word_counts]
            if len(present_words) > 1:
                issues.append(f"Inconsistent terminology: {', '.join(present_words)}")
        
        return issues
    
    def _detect_audience_mismatch(
        self, 
        context_text: str, 
        target_audience: str
    ) -> List[str]:
        """检测受众不匹配问题"""
        issues = []
        text_lower = context_text.lower()
        
        if target_audience == 'technical':
            # 检查是否包含足够的技术细节
            technical_terms = [
                'api', 'database', 'architecture', 'algorithm',
                '接口', '数据库', '架构', '算法'
            ]
            technical_count = sum(1 for term in technical_terms if term in text_lower)
            if technical_count < 2:
                issues.append("Insufficient technical details for technical audience")
        
        elif target_audience == 'business':
            # 检查是否包含业务价值描述
            business_terms = [
                'benefit', 'value', 'cost', 'roi', 'business',
                '收益', '价值', '成本', '商业'
            ]
            business_count = sum(1 for term in business_terms if term in text_lower)
            if business_count < 2:
                issues.append("Missing business value context for business audience")
        
        return issues
    
    def _detect_general_issues(self, context_text: str) -> List[str]:
        """检测通用问题"""
        issues = []
        
        # 检测长度
        if len(context_text) < 10:
            issues.append("Context too short for meaningful analysis")
        elif len(context_text) > 5000:
            issues.append("Context too long may reduce analysis accuracy")
        
        # 检测特殊字符
        non_printable = len(re.findall(r'[^\x20-\x7E\u4e00-\u9fff]', context_text))
        if non_printable > 10:
            issues.append("Contains many non-printable characters")
        
        return issues
    
    def _generate_insights(self, context_text: str, analysis_depth: str) -> List[str]:
        """生成深度洞察"""
        insights = []
        
        if analysis_depth == 'comprehensive':
            # 语言检测
            language = self._detect_language(context_text)
            insights.append(f"Detected language: {language}")
            
            # 文本复杂度
            avg_word_length = sum(len(word) for word in context_text.split()) / len(context_text.split())
            if avg_word_length > 6:
                insights.append("High vocabulary complexity detected")
            elif avg_word_length < 4:
                insights.append("Simple vocabulary detected")
            
            # 情感倾向（简化版）
            positive_words = ['good', 'better', 'improve', 'success', '好', '更好', '改进', '成功']
            negative_words = ['bad', 'problem', 'error', 'fail', '坏', '问题', '错误', '失败']
            
            text_lower = context_text.lower()
            pos_count = sum(1 for word in positive_words if word in text_lower)
            neg_count = sum(1 for word in negative_words if word in text_lower)
            
            if pos_count > neg_count * 2:
                insights.append("Generally positive sentiment detected")
            elif neg_count > pos_count * 2:
                insights.append("Generally negative sentiment detected")
        
        return insights
    
    def _generate_suggestions(
        self, 
        quality_metrics: Dict[str, float], 
        issues: List[str],
        analysis_depth: str
    ) -> List[str]:
        """
        生成改进建议
        
        Args:
            quality_metrics: 质量指标
            issues: 检测到的问题
            analysis_depth: 分析深度
            
        Returns:
            建议列表
        """
        suggestions = []
        
        # 基于质量指标的建议
        for metric, score in quality_metrics.items():
            if score < self.quality_thresholds['medium']:
                if metric == 'clarity':
                    suggestions.append("Improve clarity by using simpler sentences and consistent terminology")
                elif metric == 'relevance':
                    suggestions.append("Add more relevant information and focus on main topics")
                elif metric == 'completeness':
                    suggestions.append("Include missing details and specify constraints clearly")
                elif metric == 'consistency':
                    suggestions.append("Check for contradictions and ensure consistent terminology")
                elif metric == 'efficiency':
                    suggestions.append("Remove redundant information and be more concise")
        
        # 基于具体问题的建议
        for issue in issues:
            if 'vague' in issue.lower():
                suggestions.append("Replace vague expressions with specific descriptions")
            elif 'long sentence' in issue.lower():
                suggestions.append("Break down long sentences into shorter, clearer ones")
            elif 'incomplete' in issue.lower():
                suggestions.append("Complete the missing information and provide full specifications")
        
        # 根据分析深度的建议
        if analysis_depth == 'basic':
            suggestions.append("Consider using standard or comprehensive analysis for more detailed insights")
        
        # 确保建议不重复
        suggestions = list(set(suggestions))
        
        # 如果没有问题，提供正面反馈
        if not suggestions:
            suggestions.append("Context quality is good with no major issues detected")
        
        return suggestions[:5]  # 限制建议数量
    
    def _calculate_overall_score(self, quality_metrics: Dict[str, float]) -> float:
        """计算总体质量评分"""
        if not quality_metrics:
            return 0.0
        
        # 使用加权平均
        weights = {
            'clarity': 0.25,
            'relevance': 0.25,
            'completeness': 0.20,
            'consistency': 0.15,
            'efficiency': 0.15
        }
        
        weighted_sum = sum(
            quality_metrics.get(metric, 0.0) * weight
            for metric, weight in weights.items()
        )
        
        return round(weighted_sum, 3)
    
    def _determine_quality_level(self, overall_score: float) -> str:
        """确定质量等级"""
        if overall_score >= self.quality_thresholds['high']:
            return 'high'
        elif overall_score >= self.quality_thresholds['medium']:
            return 'medium'
        else:
            return 'low'
    
    def _detect_language(self, text: str) -> str:
        """检测文本语言（简化版）"""
        if not text:
            return 'unknown'
        
        # 统计中文字符
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        total_chars = len(text)
        
        if chinese_chars / total_chars > 0.3:
            return 'zh-CN'
        elif any(char in text for char in 'あいうえおかきくけこ'):
            return 'ja'
        elif any(char in text for char in '가나다라마바사'):
            return 'ko'
        else:
            return 'en'


# 创建技能实例
context_analyzer_skill = ContextAnalyzerSkill()

# 导出Lambda处理器（符合AgentSkills.io标准）
def lambda_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """Lambda处理器入口点"""
    return context_analyzer_skill.lambda_handler(event, context)

# 导出技能实例（用于注册）
def get_skill():
    """获取技能实例"""
    return context_analyzer_skill