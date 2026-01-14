from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class TemplateMetrics:
    token_count: int
    complexity_score: float
    template_types: List[str]
    recommended_level: str
    recommendations: List[str]

class TemplateCalculator:
    def calculate(self, request: str, context: Optional[Dict] = None) -> TemplateMetrics:
        token_count = int(len(request) / 2.5)
        complexity = min(len(request) / 1000, 1.0)

        types = []
        keywords = {
            'understanding': ['理解', 'understanding', '分析', ' comprehend'],
            'reasoning': ['推理', 'reasoning', '推导', ' logic'],
            'verification': ['验证', 'verification', '检查', ' test'],
            'design': ['设计', 'design', '架构', ' architecture'],
            'problem_solving': ['解决问题', 'problem solving', '解决', ' solve'],
        }

        for t_type, kw_list in keywords.items():
            if any(kw in request.lower() for kw in kw_list):
                types.append(t_type)

        level = '00' if complexity < 0.3 else '01' if complexity < 0.6 else '02'
        recommendations = []
        if not types:
            recommendations.append("请明确需要的模板类型（理解/推理/验证/设计）")

        return TemplateMetrics(
            token_count=token_count,
            complexity_score=complexity,
            template_types=types,
            recommended_level=level,
            recommendations=recommendations
        )
