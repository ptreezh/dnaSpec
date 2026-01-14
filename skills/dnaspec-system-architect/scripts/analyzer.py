"""
System Architect Analyzer
负责分析架构设计需求
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


class ArchitectureType(Enum):
    MONOLITH = "monolith"
    MICROSERVICE = "microservice"
    SERVERLESS = "serverless"
    DISTRIBUTED = "distributed"
    HYBRID = "hybrid"


@dataclass
class ArchitectureAnalysis:
    """架构分析"""
    detected_types: List[ArchitectureType]
    quality_scores: Dict[str, float]
    architecture_style: str
    recommendations: List[str]


class ArchitectureAnalyzer:
    """架构分析器"""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}

    def analyze(self, request: str, context: Optional[Dict] = None) -> ArchitectureAnalysis:
        """分析"""
        # 1. 检测架构类型
        detected_types = self._detect_architecture_types(request)

        # 2. 计算质量分数
        quality_scores = self._calculate_quality_scores(request)

        # 3. 确定架构风格
        architecture_style = self._determine_style(detected_types)

        # 4. 生成建议
        recommendations = self._generate_recommendations(detected_types, quality_scores)

        return ArchitectureAnalysis(
            detected_types=detected_types,
            quality_scores=quality_scores,
            architecture_style=architecture_style,
            recommendations=recommendations
        )

    def _detect_architecture_types(self, request: str) -> List[ArchitectureType]:
        """检测架构类型"""
        types = []

        if '单体' in request or 'monolith' in request.lower():
            types.append(ArchitectureType.MONOLITH)

        if '微服务' in request or 'microservice' in request.lower():
            types.append(ArchitectureType.MICROSERVICE)

        if '无服务器' in request or 'serverless' in request.lower():
            types.append(ArchitectureType.SERVERLESS)

        if '分布式' in request or 'distributed' in request.lower():
            types.append(ArchitectureType.DISTRIBUTED)

        if len(types) > 1:
            types.append(ArchitectureType.HYBRID)

        return types if types else [ArchitectureType.MONOLITH]

    def _calculate_quality_scores(self, request: str) -> Dict[str, float]:
        """计算质量分数"""
        return {
            "clarity": self._assess_clarity(request),
            "completeness": self._assess_completeness(request),
            "specificity": self._assess_specificity(request)
        }

    def _assess_clarity(self, request: str) -> float:
        """评估清晰度"""
        score = 0.5
        tech_terms = ['API', '数据库', '缓存', '架构', '模块']
        if any(term in request for term in tech_terms):
            score += 0.3
        return min(score, 1.0)

    def _assess_completeness(self, request: str) -> float:
        """评估完整性"""
        score = 0.5
        if len(request) > 50:
            score += 0.3
        return min(score, 1.0)

    def _assess_specificity(self, request: str) -> float:
        """评估具体性"""
        score = 0.5
        import re
        if re.search(r'\d+', request):
            score += 0.3
        return min(score, 1.0)

    def _determine_style(self, types: List[ArchitectureType]) -> str:
        """确定架构风格"""
        if ArchitectureType.HYBRID in types:
            return "混合架构"
        elif ArchitectureType.MICROSERVICE in types:
            return "微服务架构"
        elif ArchitectureType.SERVERLESS in types:
            return "无服务器架构"
        elif ArchitectureType.DISTRIBUTED in types:
            return "分布式架构"
        else:
            return "单体架构"

    def _generate_recommendations(
        self,
        types: List[ArchitectureType],
        scores: Dict[str, float]
    ) -> List[str]:
        """生成建议"""
        recommendations = []

        if ArchitectureType.MICROSERVICE in types:
            recommendations.append("微服务架构需要考虑服务发现、配置管理、熔断降级")

        if ArchitectureType.SERVERLESS in types:
            recommendations.append("无服务器架构适合事件驱动、按需付费场景")

        if scores.get('clarity', 0) < 0.7:
            recommendations.append("建议明确技术栈和具体需求")

        return recommendations
