from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class OptimizationMetrics:
    token_count: int
    complexity_score: float
    optimization_types: List[str]
    recommended_level: str
    recommendations: List[str]

class OptimizationCalculator:
    def calculate(self, request: str, context: Optional[Dict] = None) -> OptimizationMetrics:
        token_count = int(len(request) / 2.5)
        complexity = min(len(request) / 1000, 1.0)

        types = []
        keywords = {
            'compression': ['压缩', 'compression', '精简', '缩短'],
            'structure': ['结构化', 'structure', '重组', '组织'],
            'terminology': ['术语', 'terminology', '统一', '一致性'],
            'clarity': ['清晰度', 'clarity', '简化', '明确'],
            'completeness': ['完整性', 'completeness', '补充', '完善'],
        }

        for opt_type, kw_list in keywords.items():
            if any(kw in request.lower() for kw in kw_list):
                types.append(opt_type)

        level = '00' if complexity < 0.3 else '01' if complexity < 0.6 else '02'
        recommendations = []
        if not types:
            recommendations.append("请明确需要优化的目标（压缩/结构化/术语统一）")

        return OptimizationMetrics(
            token_count=token_count,
            complexity_score=complexity,
            optimization_types=types,
            recommended_level=level,
            recommendations=recommendations
        )
