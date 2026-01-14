from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class ContextAnalysis:
    primary_dimension: str
    analysis_type: str
    detected_issues: List[str]
    recommendations: List[str]

class ContextAnalysisAnalyzer:
    def analyze(self, request: str, context: Optional[Dict] = None) -> ContextAnalysis:
        request_lower = request.lower()

        # 检测主要维度
        dimensions = {
            'clarity': ['清晰度', 'clarity'],
            'relevance': ['相关性', 'relevance'],
            'completeness': ['完整性', 'completeness'],
            'consistency': ['一致性', 'consistency'],
            'efficiency': ['效率', 'efficiency'],
        }

        detected = []
        for dim, keywords in dimensions.items():
            if any(kw in request_lower for kw in keywords):
                detected.append(dim)

        primary = detected[0] if detected else 'general'

        # 检测分析类型
        if '爆炸' in request or 'explosion' in request_lower:
            analysis_type = 'explosion_risk'
        elif '腐化' in request or 'corruption' in request_lower:
            analysis_type = 'corruption_risk'
        elif '演化' in request or 'evolution' in request_lower:
            analysis_type = 'evolution_monitoring'
        else:
            analysis_type = 'quality_assessment'

        # 检测潜在问题
        issues = []
        if '模糊' in request or 'unclear' in request_lower:
            issues.append('clarity_issue')
        if '不一致' in request or 'inconsistent' in request_lower:
            issues.append('consistency_issue')
        if '缺失' in request or 'missing' in request_lower:
            issues.append('completeness_issue')

        recommendations = []
        if not detected:
            recommendations.append("请指定需要分析的质量维度")

        return ContextAnalysis(
            primary_dimension=primary,
            analysis_type=analysis_type,
            detected_issues=issues,
            recommendations=recommendations
        )
