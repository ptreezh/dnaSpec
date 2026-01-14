from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class CoordinationMetrics:
    token_count: int
    complexity_score: float
    has_multi_layer: bool
    has_skill_coord: bool
    recommended_level: str
    estimated_skills: int
    recommendations: List[str]

class CoordinationCalculator:
    def calculate(self, request: str, context: Optional[Dict] = None) -> CoordinationMetrics:
        token_count = int(len(request) / 2.5)
        complexity = min(len(request) / 1000, 1.0)
        
        has_multi_layer = any(kw in request.lower() for kw in ['层级', 'layer', '多层', 'multi'])
        has_skill_coord = any(kw in request.lower() for kw in ['技能', 'skill', '协调', 'coord'])
        
        level = '00' if complexity < 0.3 else '01' if complexity < 0.6 else '02'
        
        return CoordinationMetrics(
            token_count=token_count,
            complexity_score=complexity,
            has_multi_layer=has_multi_layer,
            has_skill_coord=has_skill_coord,
            recommended_level=level,
            estimated_skills=1,
            recommendations=[]
        )
