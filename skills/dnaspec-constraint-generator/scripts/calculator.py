"""
Constraint Generator Calculator
负责计算约束相关指标
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import re


@dataclass
class ConstraintMetrics:
    """约束指标"""
    # 基础指标
    token_count: int
    character_count: int

    # 复杂度指标
    complexity_score: float  # 0.0-1.0

    # 约束类型指标
    has_performance_constraint: bool
    has_security_constraint: bool
    has_functional_constraint: bool
    has_technical_constraint: bool

    # 质量指标
    specificity_score: float  # 0.0-1.0
    measurability_score: float  # 0.0-1.0

    # 推荐指标
    recommended_level: str
    constraint_count_estimate: int
    recommendations: List[str]


class ConstraintCalculator:
    """约束计算器"""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}

    def calculate(self, request: str, context: Optional[Dict] = None) -> ConstraintMetrics:
        """计算指标"""
        # 1. 基础指标
        character_count = len(request)
        token_count = self._estimate_tokens(request)

        # 2. 复杂度指标
        complexity_score = self._calculate_complexity_score(request, context)

        # 3. 约束类型检测
        has_performance = self._has_performance_constraint(request)
        has_security = self._has_security_constraint(request)
        has_functional = self._has_functional_constraint(request)
        has_technical = self._has_technical_constraint(request)

        # 4. 质量指标
        specificity_score = self._calculate_specificity_score(request)
        measurability_score = self._calculate_measurability_score(request)

        # 5. 推荐层次
        recommended_level = self._recommend_level(complexity_score, token_count)

        # 6. 估算约束数量
        constraint_count = self._estimate_constraint_count(request)

        # 7. 生成建议
        recommendations = self._generate_recommendations(
            has_performance, has_security, has_functional, has_technical,
            specificity_score, measurability_score
        )

        return ConstraintMetrics(
            token_count=token_count,
            character_count=character_count,
            complexity_score=complexity_score,
            has_performance_constraint=has_performance,
            has_security_constraint=has_security,
            has_functional_constraint=has_functional,
            has_technical_constraint=has_technical,
            specificity_score=specificity_score,
            measurability_score=measurability_score,
            recommended_level=recommended_level,
            constraint_count_estimate=constraint_count,
            recommendations=recommendations
        )

    def _estimate_tokens(self, text: str) -> int:
        """估算token数量"""
        # 简化：中英混合约2.5字符/token
        return int(len(text) / 2.5)

    def _calculate_complexity_score(self, request: str, context: Optional[Dict]) -> float:
        """计算复杂度"""
        score = 0.0

        # 因素1：请求长度
        if len(request) > 500:
            score += 0.2

        # 因素2：约束类型数量
        types = 0
        if '性能' in request or 'performance' in request.lower():
            types += 1
        if '安全' in request or 'security' in request.lower():
            types += 1
        if '功能' in request or 'function' in request.lower():
            types += 1
        if '技术' in request or 'technical' in request.lower():
            types += 1

        score += min(types * 0.15, 0.4)

        # 因素3：有上下文
        if context:
            score += 0.2

        # 因素4：包含数字（可能是有具体指标）
        numbers = re.findall(r'\d+', request)
        if len(numbers) > 0:
            score += 0.2

        return min(score, 1.0)

    def _has_performance_constraint(self, request: str) -> bool:
        """检测性能约束"""
        keywords = ['性能', 'performance', '响应时间', 'response time', '延迟', 'latency',
                     '吞吐量', 'throughput', 'QPS', '并发', 'concurrent']
        return any(kw in request.lower() for kw in keywords)

    def _has_security_constraint(self, request: str) -> bool:
        """检测安全约束"""
        keywords = ['安全', 'security', '认证', 'authentication', '授权', 'authorization',
                     '加密', 'encryption', '密码', 'password', '权限', 'permission']
        return any(kw in request.lower() for kw in keywords)

    def _has_functional_constraint(self, request: str) -> bool:
        """检测功能约束"""
        keywords = ['功能', 'function', '需求', 'requirement', '必须', 'must',
                     '应该', 'should', '支持', 'support']
        return any(kw in request.lower() for kw in keywords)

    def _has_technical_constraint(self, request: str) -> bool:
        """检测技术约束"""
        keywords = ['技术', 'technical', '架构', 'architecture', '框架', 'framework',
                     '语言', 'language', '数据库', 'database', '平台', 'platform']
        return any(kw in request.lower() for kw in keywords)

    def _calculate_specificity_score(self, request: str) -> float:
        """计算具体性分数"""
        score = 0.0

        # 包含数字
        if re.search(r'\d+', request):
            score += 0.3

        # 包含单位
        units = ['ms', '秒', 'second', 'MB', 'GB', '%', 'QPS', 'TPS']
        if any(unit in request for unit in units):
            score += 0.3

        # 包含比较符
        comparisons = ['<', '>', '≤', '>=', '<=', '=>']
        if any(comp in request for comp in comparisons):
            score += 0.4

        return min(score, 1.0)

    def _calculate_measurability_score(self, request: str) -> float:
        """计算可测量性分数"""
        score = 0.0

        # 有明确指标
        if self._has_performance_constraint(request):
            score += 0.4

        # 有验证方法关键词
        verification_keywords = ['测试', 'test', '验证', 'verify', '监控', 'monitor',
                                  '检查', 'check', '审计', 'audit']
        if any(kw in request for kw in verification_keywords):
            score += 0.3

        # 有时间限制
        time_keywords = ['月', 'month', '周', 'week', '天', 'day']
        if any(kw in request for kw in time_keywords):
            score += 0.3

        return min(score, 1.0)

    def _recommend_level(self, complexity: float, tokens: int) -> str:
        """推荐提示词层次"""
        if complexity < 0.3 and tokens < 5000:
            return "00"
        elif complexity < 0.5 and tokens < 10000:
            return "01"
        elif complexity < 0.7 or tokens < 20000:
            return "02"
        else:
            return "03"

    def _estimate_constraint_count(self, request: str) -> int:
        """估算约束数量"""
        # 简化：每识别到一个约束类型，估算1-3个约束
        types = sum([
            self._has_performance_constraint(request),
            self._has_security_constraint(request),
            self._has_functional_constraint(request),
            self._has_technical_constraint(request)
        ])

        return types * 2  # 平均每个类型2个约束

    def _generate_recommendations(
        self, has_perf, has_sec, has_func, has_tech,
        specificity, measurability
    ) -> List[str]:
        """生成建议"""
        recommendations = []

        if has_perf:
            recommendations.append("建议包含明确的性能指标（如P95响应时间）")
        if has_sec:
            recommendations.append("建议参考安全最佳实践（如OWASP Top 10）")
        if has_func:
            recommendations.append("建议使用用户故事格式描述功能约束")

        if specificity < 0.5:
            recommendations.append("建议增加具体数值和单位，提高约束的具体性")

        if measurability < 0.5:
            recommendations.append("建议明确验证方法和验收标准")

        if not recommendations:
            recommendations.append("约束需求描述清晰")

        return recommendations


if __name__ == "__main__":
    # 测试
    calculator = ConstraintCalculator()

    test_cases = [
        "生成API性能约束",
        "系统需要高安全性和高性能",
        "响应时间要小于100毫秒，支持1000 QPS"
    ]

    for request in test_cases:
        metrics = calculator.calculate(request)
        print(f"请求: {request}")
        print(f"复杂度: {metrics.complexity_score:.2f}")
        print(f"推荐层次: {metrics.recommended_level}")
        print(f"估算约束数: {metrics.constraint_count_estimate}")
        print()
