from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class OptimizationAnalysis:
    primary_optimization: str
    target_dimension: str
    optimization_details: List[str]
    recommendations: List[str]

class OptimizationAnalyzer:
    def analyze(self, request: str, context: Optional[Dict] = None) -> OptimizationAnalysis:
        request_lower = request.lower()

        optimizations = {
            'compression': ['压缩', 'compression', '精简'],
            'structure': ['结构化', 'structure', '重组'],
            'terminology': ['术语', 'terminology', '统一'],
            'clarity': ['清晰度', 'clarity'],
            'completeness': ['完整性', 'completeness'],
        }

        detected = []
        for opt, keywords in optimizations.items():
            if any(kw in request_lower for kw in keywords):
                detected.append(opt)

        primary = detected[0] if detected else 'general'

        # 检测目标维度
        dimensions = {
            'clarity': ['清晰度', 'clarity'],
            'relevance': ['相关性', 'relevance'],
            'completeness': ['完整性', 'completeness'],
            'consistency': ['一致性', 'consistency'],
            'efficiency': ['效率', 'efficiency'],
        }

        target = 'general'
        for dim, keywords in dimensions.items():
            if any(kw in request_lower for kw in keywords):
                target = dim
                break

        details = []
        if 'compression' in detected:
            details.append('删除冗余内容')
        if 'structure' in detected:
            details.append('改进组织结构')
        if 'terminology' in detected:
            details.append('统一术语使用')

        recommendations = []
        if not detected:
            recommendations.append("请明确需要的优化类型")

        return OptimizationAnalysis(
            primary_optimization=primary,
            target_dimension=target,
            optimization_details=details,
            recommendations=recommendations
        )
