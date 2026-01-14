"""
Constraint Generator Analyzer
负责分析约束需求
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


class ConstraintType(Enum):
    PERFORMANCE = "performance"
    SECURITY = "security"
    FUNCTIONAL = "functional"
    TECHNICAL = "technical"
    COMPLIANCE = "compliance"


@dataclass
class ConstraintAnalysis:
    """约束分析"""
    detected_types: List[ConstraintType]
    quality_scores: Dict[str, float]
    potential_conflicts: List[str]
    recommendations: List[str]


class ConstraintAnalyzer:
    """约束分析器"""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}

    def analyze(self, request: str, context: Optional[Dict] = None) -> ConstraintAnalysis:
        """分析"""
        # 1. 检测约束类型
        detected_types = self._detect_constraint_types(request)

        # 2. 计算质量分数
        quality_scores = self._calculate_quality_scores(request)

        # 3. 检测潜在冲突
        conflicts = self._detect_conflicts(request)

        # 4. 生成建议
        recommendations = self._generate_recommendations(
            detected_types, quality_scores, conflicts
        )

        return ConstraintAnalysis(
            detected_types=detected_types,
            quality_scores=quality_scores,
            potential_conflicts=conflicts,
            recommendations=recommendations
        )

    def _detect_constraint_types(self, request: str) -> List[ConstraintType]:
        """检测约束类型"""
        types = []

        if '性能' in request or 'performance' in request.lower():
            types.append(ConstraintType.PERFORMANCE)

        if '安全' in request or 'security' in request.lower():
            types.append(ConstraintType.SECURITY)

        if '功能' in request or 'function' in request.lower():
            types.append(ConstraintType.FUNCTIONAL)

        if '技术' in request or 'technical' in request.lower():
            types.append(ConstraintType.TECHNICAL)

        if '合规' in request or 'compliance' in request.lower():
            types.append(ConstraintType.COMPLIANCE)

        return types

    def _calculate_quality_scores(self, request: str) -> Dict[str, float]:
        """计算质量分数"""
        scores = {
            "clarity": self._assess_clarity(request),
            "completeness": self._assess_completeness(request),
            "verifiability": self._assess_verifiability(request),
            "prioritization": self._assess_prioritization(request)
        }

        return scores

    def _assess_clarity(self, request: str) -> float:
        """评估清晰度"""
        score = 0.5

        # 有具体数字
        import re
        if re.search(r'\d+', request):
            score += 0.2

        # 有明确单位
        units = ['ms', '秒', 'QPS', '%']
        if any(unit in request for unit in units):
            score += 0.2

        # 使用专业术语
        tech_terms = ['API', '响应时间', '吞吐量', '延迟', '加密']
        if any(term in request for term in tech_terms):
            score += 0.1

        return min(score, 1.0)

    def _assess_completeness(self, request: str) -> float:
        """评估完整性"""
        score = 0.5

        # 包含多个要素
        if len(request) > 50:
            score += 0.2

        # 提到验证方法
        verification_words = ['测试', '验证', '监控']
        if any(word in request for word in verification_words):
            score += 0.2

        # 有明确目标
        goal_words = ['目标', '要求', '必须', 'should']
        if any(word in request for word in goal_words):
            score += 0.1

        return min(score, 1.0)

    def _assess_verifiability(self, request: str) -> float:
        """评估可验证性"""
        score = 0.5

        # 包含数字指标（可测量）
        import re
        if re.search(r'\d+\s*(ms|秒|%|QPS|TPS)', request):
            score += 0.3

        # 提到测试
        if '测试' in request or 'test' in request.lower():
            score += 0.2

        return min(score, 1.0)

    def _assess_prioritization(self, request: str) -> float:
        """评估优先级明确性"""
        score = 0.5

        # 提到优先级
        priority_words = ['优先', 'priority', '关键', 'critical', '重要', 'important']
        if any(word in request for word in priority_words):
            score += 0.3

        # 有时间限制
        time_words = ['立即', '尽快', '本季度', '本月']
        if any(word in request for word in time_words):
            score += 0.2

        return min(score, 1.0)

    def _detect_conflicts(self, request: str) -> List[str]:
        """检测潜在冲突"""
        conflicts = []

        # 检测"快"与"安全"的冲突
        if '快' in request and '安全' in request:
            conflicts.append("性能优化可能影响安全性（如加密开销）")

        # 检测"低成本"与"高质量"的冲突
        if '低成本' in request and '高质量' in request:
            conflicts.append("成本约束可能与质量目标冲突")

        # 检测"快速上线"与"完整功能"的冲突
        if '快速' in request and '完整' in request:
            conflicts.append("快速交付可能需要分阶段实现功能")

        return conflicts

    def _generate_recommendations(
        self,
        types: List[ConstraintType],
        scores: Dict[str, float],
        conflicts: List[str]
    ) -> List[str]:
        """生成建议"""
        recommendations = []

        # 基于约束类型的建议
        if ConstraintType.PERFORMANCE in types:
            recommendations.append("建议使用性能测试工具（JMeter, Locust）验证性能约束")

        if ConstraintType.SECURITY in types:
            recommendations.append("建议参考OWASP安全标准和OWASP ZAP工具")

        if ConstraintType.FUNCTIONAL in types:
            recommendations.append("建议使用用户故事和验收标准（Given-When-Then）格式")

        # 基于质量分数的建议
        if scores.get('clarity', 0) < 0.7:
            recommendations.append("建议使用SMART原则使约束更具体、可测量")

        if scores.get('verifiability', 0) < 0.7:
            recommendations.append("建议为每个约束明确验证方法和验收标准")

        # 基于冲突的建议
        if conflicts:
            recommendations.append(f"检测到{len(conflicts)}个潜在冲突，建议优先级排序或分阶段实现")

        return recommendations


if __name__ == "__main__":
    # 测试
    analyzer = ConstraintAnalyzer()

    test_cases = [
        "API性能要好",
        "系统需要高安全性和快速响应",
        "响应时间小于100ms，支持1000 QPS"
    ]

    for request in test_cases:
        analysis = analyzer.analyze(request)
        print(f"请求: {request}")
        print(f"检测到的类型: {[t.value for t in analysis.detected_types]}")
        print(f"质量分数: {analysis.quality_scores}")
        print(f"潜在冲突: {analysis.potential_conflicts}")
        print(f"建议: {analysis.recommendations}")
        print()
