"""
System Architect Calculator
负责计算架构设计指标
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import re


@dataclass
class ArchitectureMetrics:
    """架构指标"""
    # 基础指标
    token_count: int
    character_count: int

    # 复杂度指标
    complexity_score: float  # 0.0-1.0

    # 架构类型指标
    has_monolith_arch: bool
    has_microservice_arch: bool
    has_serverless_arch: bool
    has_distributed_arch: bool

    # 质量指标
    clarity_score: float  # 0.0-1.0
    completeness_score: float  # 0.0-1.0

    # 推荐指标
    recommended_level: str
    estimated_modules: int
    recommendations: List[str]


class ArchitectureCalculator:
    """架构计算器"""

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}

    def calculate(self, request: str, context: Optional[Dict] = None) -> ArchitectureMetrics:
        """计算指标"""
        # 1. 基础指标
        character_count = len(request)
        token_count = self._estimate_tokens(request)

        # 2. 复杂度指标
        complexity_score = self._calculate_complexity_score(request, context)

        # 3. 架构类型检测
        has_monolith = self._has_monolith_arch(request)
        has_microservice = self._has_microservice_arch(request)
        has_serverless = self._has_serverless_arch(request)
        has_distributed = self._has_distributed_arch(request)

        # 4. 质量指标
        clarity_score = self._calculate_clarity_score(request)
        completeness_score = self._calculate_completeness_score(request)

        # 5. 推荐层次
        recommended_level = self._recommend_level(complexity_score, token_count)

        # 6. 估算模块数量
        estimated_modules = self._estimate_modules(request)

        # 7. 生成建议
        recommendations = self._generate_recommendations(
            has_monolith, has_microservice, has_serverless,
            clarity_score, completeness_score
        )

        return ArchitectureMetrics(
            token_count=token_count,
            character_count=character_count,
            complexity_score=complexity_score,
            has_monolith_arch=has_monolith,
            has_microservice_arch=has_microservice,
            has_serverless_arch=has_serverless,
            has_distributed_arch=has_distributed,
            clarity_score=clarity_score,
            completeness_score=completeness_score,
            recommended_level=recommended_level,
            estimated_modules=estimated_modules,
            recommendations=recommendations
        )

    def _estimate_tokens(self, text: str) -> int:
        """估算token数量"""
        return int(len(text) / 2.5)

    def _calculate_complexity_score(self, request: str, context: Optional[Dict]) -> float:
        """计算复杂度"""
        score = 0.0

        # 因素1：请求长度
        if len(request) > 500:
            score += 0.2

        # 因素2：架构类型数量
        arch_types = 0
        if '单体' in request or 'monolith' in request.lower():
            arch_types += 1
        if '微服务' in request or 'microservice' in request.lower():
            arch_types += 1
        if '无服务器' in request or 'serverless' in request.lower():
            arch_types += 1
        if '分布式' in request or 'distributed' in request.lower():
            arch_types += 1

        score += min(arch_types * 0.15, 0.4)

        # 因素3：有上下文
        if context:
            score += 0.2

        # 因素4：包含具体技术
        tech_keywords = ['数据库', 'database', 'API', '缓存', 'cache', '队列', 'queue']
        if any(kw in request.lower() for kw in tech_keywords):
            score += 0.2

        return min(score, 1.0)

    def _has_monolith_arch(self, request: str) -> bool:
        """检测单体架构"""
        keywords = ['单体', 'monolith', '单体应用', 'single application']
        return any(kw in request.lower() for kw in keywords)

    def _has_microservice_arch(self, request: str) -> bool:
        """检测微服务架构"""
        keywords = ['微服务', 'microservice', 'micro-service', '服务拆分']
        return any(kw in request.lower() for kw in keywords)

    def _has_serverless_arch(self, request: str) -> bool:
        """检测无服务器架构"""
        keywords = ['无服务器', 'serverless', '函数计算', 'lambda', 'FaaS']
        return any(kw in request.lower() for kw in keywords)

    def _has_distributed_arch(self, request: str) -> bool:
        """检测分布式架构"""
        keywords = ['分布式', 'distributed', '集群', 'cluster', '负载均衡', 'load balance']
        return any(kw in request.lower() for kw in keywords)

    def _calculate_clarity_score(self, request: str) -> float:
        """计算清晰度分数"""
        score = 0.5

        # 有具体技术名称
        tech_names = ['React', 'Vue', 'Python', 'Java', 'Node.js', 'PostgreSQL', 'MongoDB']
        if any(name in request for name in tech_names):
            score += 0.2

        # 有具体指标
        if re.search(r'\d+', request):
            score += 0.2

        # 使用专业术语
        arch_terms = ['API', 'REST', 'GraphQL', 'MVC', 'DDD']
        if any(term in request for term in arch_terms):
            score += 0.1

        return min(score, 1.0)

    def _calculate_completeness_score(self, request: str) -> float:
        """计算完整性分数"""
        score = 0.5

        # 包含多个要素
        if len(request) > 50:
            score += 0.2

        # 提到多个方面
        aspects = 0
        if '前端' in request or 'frontend' in request.lower():
            aspects += 1
        if '后端' in request or 'backend' in request.lower():
            aspects += 1
        if '数据库' in request or 'database' in request.lower():
            aspects += 1

        if aspects >= 2:
            score += 0.2

        return min(score, 1.0)

    def _recommend_level(self, complexity: float, tokens: int) -> str:
        """推荐提示词层次"""
        if complexity < 0.3 and tokens < 1000:
            return "00"
        elif complexity < 0.5 and tokens < 3000:
            return "01"
        elif complexity < 0.7 or tokens < 5000:
            return "02"
        else:
            return "03"

    def _estimate_modules(self, request: str) -> int:
        """估算模块数量"""
        # 简化：每识别到一个关键词，估算2-3个模块
        module_keywords = ['用户', '订单', '商品', '支付', '物流', '管理']
        count = sum(request.count(kw) for kw in module_keywords)
        return max(count * 2, 5)  # 至少5个模块

    def _generate_recommendations(
        self,
        has_monolith, has_microservice, has_serverless,
        clarity, completeness
    ) -> List[str]:
        """生成建议"""
        recommendations = []

        if has_microservice:
            recommendations.append("微服务架构需要考虑服务拆分、通信、数据一致性等问题")

        if has_serverless:
            recommendations.append("无服务器架构适合事件驱动、突发流量场景")

        if clarity < 0.7:
            recommendations.append("建议明确技术栈选型和具体需求")

        if completeness < 0.7:
            recommendations.append("建议详细描述前后端、数据库等各个方面")

        if not recommendations:
            recommendations.append("架构需求描述清晰")

        return recommendations
