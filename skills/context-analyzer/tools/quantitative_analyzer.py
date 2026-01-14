#!/usr/bin/env python3
"""
Context Analyzer - Quantitative Analysis Tools
确定性量化分析工具脚本
"""

import re
import json
import sys
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class AnalysisResult:
    """分析结果数据结构"""
    dimension: str
    score: float
    details: Dict[str, Any]
    issues: List[str]
    suggestions: List[str]

class ContextAnalyzer:
    """上下文分析器 - 确定性量化分析部分"""
    
    def __init__(self):
        self.analysis_functions = {
            'clarity': self.analyze_clarity,
            'relevance': self.analyze_relevance,
            'completeness': self.analyze_completeness,
            'consistency': self.analyze_consistency,
            'efficiency': self.analyze_efficiency
        }
    
    def analyze_all_dimensions(self, context: str, context_type: str = "general") -> Dict[str, AnalysisResult]:
        """分析所有维度"""
        results = {}
        
        for dimension, analysis_func in self.analysis_functions.items():
            try:
                results[dimension] = analysis_func(context, context_type)
            except Exception as e:
                results[dimension] = AnalysisResult(
                    dimension=dimension,
                    score=0.0,
                    details={"error": str(e)},
                    issues=[f"Analysis failed: {e}"],
                    suggestions=["Retry analysis or check input format"]
                )
        
        return results
    
    def analyze_clarity(self, context: str, context_type: str) -> AnalysisResult:
        """分析清晰度 - 确定性算法"""
        if not context:
            return AnalysisResult("clarity", 0.0, {}, [], ["Empty context"])
        
        sentences = re.split(r'[.!?。！？]+', context)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return AnalysisResult("clarity", 0.0, {}, [], ["No valid sentences found"])
        
        # 确定性指标
        clear_indicators = ['请', '需要', '要求', '目标', '任务', '执行', '实现', '请', '应该', '必须']
        ambiguous_indicators = ['也许', '可能', '大概', '似乎', '好像', '左右', '约', '大约']
        
        # 量化计算
        total_sentences = len(sentences)
        clear_count = sum(1 for s in sentences for indicator in clear_indicators if indicator in s)
        ambiguous_count = sum(1 for s in sentences for indicator in ambiguous_indicators if indicator in s)
        
        # 计算清晰度分数
        clarity_ratio = clear_count / total_sentences
        ambiguity_ratio = ambiguous_count / total_sentences
        base_score = clarity_ratio * 0.7  # 清晰指令权重
        ambiguity_penalty = ambiguity_ratio * 0.3  # 模糊表达惩罚
        
        final_score = max(0.0, min(1.0, base_score - ambiguity_penalty))
        
        # 生成详细分析
        issues = []
        suggestions = []
        
        if ambiguity_ratio > 0.3:
            issues.append(f"High ambiguity detected ({ambiguity_ratio:.1%})")
            suggestions.append("Replace ambiguous expressions with clear instructions")
        
        if clarity_ratio < 0.4:
            issues.append(f"Low clarity indicators ({clarity_ratio:.1%})")
            suggestions.append("Add clear action verbs and specific requirements")
        
        # 句子长度分析
        avg_sentence_length = sum(len(s) for s in sentences) / total_sentences
        if avg_sentence_length > 100:
            issues.append("Sentences too long (average complexity)")
            suggestions.append("Break down long sentences for better readability")
        
        return AnalysisResult(
            dimension="clarity",
            score=final_score,
            details={
                "total_sentences": total_sentences,
                "clear_indicators": clear_count,
                "ambiguous_indicators": ambiguous_count,
                "avg_sentence_length": avg_sentence_length,
                "clarity_ratio": clarity_ratio,
                "ambiguity_ratio": ambiguity_ratio
            },
            issues=issues,
            suggestions=suggestions
        )
    
    def analyze_relevance(self, context: str, context_type: str) -> AnalysisResult:
        """分析相关性 - 确定性算法"""
        if not context:
            return AnalysisResult("relevance", 0.0, {}, [], ["Empty context"])
        
        # 根据上下文类型选择相关指标
        task_indicators = {
            "general": ['任务', '目标', '问题', '需求', '功能', '系统', '项目', '开发', '设计', '分析'],
            "technical": ['API', '接口', '函数', '类', '方法', '参数', '返回值', '异常', '测试'],
            "business": ['业务', '客户', '用户', '市场', '产品', '服务', '流程', '规则'],
            "academic": ['研究', '理论', '方法', '实验', '数据', '结果', '结论', '文献', '假设']
        }
        
        indicators = task_indicators.get(context_type, task_indicators["general"])
        
        # 计算相关性指标
        relevance_count = sum(1 for indicator in indicators if indicator in context)
        context_words = len(re.findall(r'[\w\u4e00-\u9fff]+', context))
        
        # 相关性密度计算
        relevance_density = relevance_count / max(1, context_words / 10)  # 每10个词的相关指标数
        relevance_score = min(1.0, relevance_density * 2)  # 归一化到0-1
        
        # 生成分析详情
        issues = []
        suggestions = []
        
        if relevance_density < 0.1:
            issues.append("Low topic relevance density")
            suggestions.append("Add more domain-specific terminology")
        
        if relevance_count < 3:
            issues.append("Insufficient relevant keywords")
            suggestions.append("Include more task-related indicators")
        
        return AnalysisResult(
            dimension="relevance",
            score=relevance_score,
            details={
                "relevance_count": relevance_count,
                "context_words": context_words,
                "relevance_density": relevance_density,
                "context_type": context_type
            },
            issues=issues,
            suggestions=suggestions
        )
    
    def analyze_completeness(self, context: str, context_type: str) -> AnalysisResult:
        """分析完整性 - 确定性算法"""
        if not context:
            return AnalysisResult("completeness", 0.0, {}, [], ["Empty context"])
        
        # 完整性指标
        completeness_indicators = {
            "requirements": ['假设', '约束', '要求', '条件', '规则', '限制', '规范', '标准', '验收'],
            "technical": ['输入', '输出', '处理', '异常', '边界', '性能', '安全', '兼容'],
            "business": ['背景', '目标', '范围', '时间', '成本', '质量', '风险', '资源'],
            "general": ['假设', '约束', '要求', '条件', '规则', '限制', '规范', '标准']
        }
        
        indicators = completeness_indicators.get(context_type, completeness_indicators["general"])
        
        completeness_count = sum(1 for indicator in indicators if indicator in context)
        completeness_ratio = completeness_count / len(indicators)
        completeness_score = min(1.0, completeness_ratio * 1.5)  # 放大分数范围
        
        # 检查缺失的关键元素
        missing_elements = [ind for ind in indicators if ind not in context]
        
        issues = []
        suggestions = []
        
        if completeness_count < 3:
            issues.append(f"Insufficient completeness indicators ({completeness_count})")
            suggestions.append("Add constraints, requirements, and conditions")
        
        if len(missing_elements) > len(indicators) * 0.7:
            issues.append("Major completeness gaps detected")
            suggestions.append("Include comprehensive coverage of all aspects")
        
        return AnalysisResult(
            dimension="completeness",
            score=completeness_score,
            details={
                "completeness_count": completeness_count,
                "total_indicators": len(indicators),
                "completeness_ratio": completeness_ratio,
                "missing_elements": missing_elements[:5],  # 只显示前5个缺失元素
                "context_type": context_type
            },
            issues=issues,
            suggestions=suggestions
        )
    
    def analyze_consistency(self, context: str, context_type: str) -> AnalysisResult:
        """分析一致性 - 确定性算法"""
        if not context:
            return AnalysisResult("consistency", 0.0, {}, [], ["Empty context"])
        
        # 矛盾检测词对
        contradiction_pairs = [
            ('必须', '可以'), ('应该', '不必'), ('总是', '从不'), ('所有', '没有'),
            ('必须', '禁止'), ('要求', '不要求'), ('需要', '不需要'),
            ('包含', '排除'), ('允许', '禁止'), ('支持', '不支持')
        ]
        
        # 数字一致性检查
        number_patterns = re.findall(r'(\d+(?:\.\d+)?)\s*([个台项次遍遍])', context)
        
        contradiction_count = 0
        detected_contradictions = []
        
        for pos, neg in contradiction_pairs:
            if pos in context and neg in context:
                contradiction_count += 1
                detected_contradictions.append(f"{pos} vs {neg}")
        
        # 时间一致性检查
        time_expressions = ['今天', '昨天', '明天', '现在', '之前', '之后', '同时', '先后']
        time_conflicts = 0
        for i, expr1 in enumerate(time_expressions):
            for expr2 in time_expressions[i+1:]:
                if expr1 in context and expr2 in context:
                    time_conflicts += 1
                    break  # 只记录一个时间冲突
        
        base_score = 1.0
        contradiction_penalty = min(0.5, contradiction_count * 0.15)
        time_conflict_penalty = min(0.2, time_conflicts * 0.1)
        
        consistency_score = max(0.0, base_score - contradiction_penalty - time_conflict_penalty)
        
        issues = []
        suggestions = []
        
        if contradiction_count > 0:
            issues.append(f"Contradictions detected: {', '.join(detected_contradictions)}")
            suggestions.append("Review and resolve contradictory statements")
        
        if time_conflicts > 0:
            issues.append("Time expression conflicts found")
            suggestions.append("Ensure consistent temporal references")
        
        return AnalysisResult(
            dimension="consistency",
            score=consistency_score,
            details={
                "contradiction_count": contradiction_count,
                "detected_contradictions": detected_contradictions,
                "time_conflicts": time_conflicts,
                "contradiction_penalty": contradiction_penalty,
                "time_conflict_penalty": time_conflict_penalty
            },
            issues=issues,
            suggestions=suggestions
        )
    
    def analyze_efficiency(self, context: str, context_type: str) -> AnalysisResult:
        """分析效率 - 确定性算法"""
        if not context:
            return AnalysisResult("efficiency", 0.0, {}, [], ["Empty context"])
        
        # 信息密度计算
        total_chars = len(context)
        words = re.findall(r'[\w\u4e00-\u9fff]+', context)
        useful_words = [w for w in words if len(w) > 1]  # 过滤单字符
        
        # 冗余检测
        repeated_phrases = {}
        for word in useful_words:
            if word in repeated_phrases:
                repeated_phrases[word] += 1
            else:
                repeated_phrases[word] = 1
        
        redundancy_ratio = sum(1 for count in repeated_phrases.values() if count > 3) / max(1, len(useful_words))
        
        # 信息密度计算
        information_density = len(useful_words) / max(1, total_chars / 10)  # 每10个字符的词汇数
        
        # 效率分数
        density_score = min(1.0, information_density * 3)  # 信息密度分数
        redundancy_penalty = redundancy_ratio * 0.5  # 冗余惩罚
        efficiency_score = max(0.0, density_score - redundancy_penalty)
        
        issues = []
        suggestions = []
        
        if redundancy_ratio > 0.2:
            issues.append(f"High redundancy detected ({redundancy_ratio:.1%})")
            suggestions.append("Reduce repetitive content and improve conciseness")
        
        if information_density < 0.3:
            issues.append("Low information density")
            suggestions.append("Increase information density by removing filler content")
        
        return AnalysisResult(
            dimension="efficiency",
            score=efficiency_score,
            details={
                "total_chars": total_chars,
                "useful_words": len(useful_words),
                "information_density": information_density,
                "redundancy_ratio": redundancy_ratio,
                "repeated_phrases": {k: v for k, v in repeated_phrases.items() if v > 3}
            },
            issues=issues,
            suggestions=suggestions
        )

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("Usage: python context_analyzer.py <context_text> [context_type]")
        sys.exit(1)
    
    context_text = sys.argv[1]
    context_type = sys.argv[2] if len(sys.argv) > 2 else "general"
    
    analyzer = ContextAnalyzer()
    results = analyzer.analyze_all_dimensions(context_text, context_type)
    
    # 输出结构化结果
    output = {
        "context_type": context_type,
        "context_length": len(context_text),
        "analysis_results": {}
    }
    
    for dimension, result in results.items():
        output["analysis_results"][dimension] = {
            "score": result.score,
            "details": result.details,
            "issues": result.issues,
            "suggestions": result.suggestions
        }
    
    # 计算总体分数
    overall_score = sum(result.score for result in results.values()) / len(results)
    output["overall_score"] = overall_score
    
    # 输出JSON格式结果
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()