from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class ContextMetrics:
    token_count: int
    complexity_score: float
    analysis_dimensions: List[str]
    recommended_level: str
    recommendations: List[str]

class ContextAnalysisCalculator:
    def calculate(self, request: str, context: Optional[Dict] = None) -> ContextMetrics:
        token_count = int(len(request) / 2.5)
        complexity = min(len(request) / 1000, 1.0)

        # 检测分析维度
        dimensions = []
        keywords = {
            'clarity': ['清晰度', 'clarity', '明确', '清晰'],
            'relevance': ['相关性', 'relevance', '相关'],
            'completeness': ['完整性', 'completeness', '完整'],
            'consistency': ['一致性', 'consistency', '一致'],
            'efficiency': ['效率', 'efficiency', '简洁'],
        }

        for dim, kw_list in keywords.items():
            if any(kw in request.lower() for kw in kw_list):
                dimensions.append(dim)

        # 推荐级别
        if complexity < 0.3:
            level = '00'
        elif complexity < 0.6:
            level = '01'
        elif len(dimensions) <= 2:
            level = '01'
        else:
            level = '02' if len(dimensions) <= 4 else '03'

        recommendations = []
        if not dimensions:
            recommendations.append("请明确需要分析的质量维度")

        return ContextMetrics(
            token_count=token_count,
            complexity_score=complexity,
            analysis_dimensions=dimensions,
            recommended_level=level,
            recommendations=recommendations
        )
