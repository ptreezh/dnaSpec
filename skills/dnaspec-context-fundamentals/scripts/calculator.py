"""
Context Fundamentals Calculator

负责计算上下文相关指标
提供确定性的定量计算
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import re
import json


@dataclass
class ContextMetrics:
    """上下文指标"""
    # 基础指标
    token_count: int
    character_count: int
    word_count: int
    line_count: int

    # 复杂度指标
    complexity_score: float  # 0.0-1.0
    information_density: float  # 0.0-1.0
    structure_quality: float  # 0.0-1.0

    # 相关性指标
    relevance_score: float  # 0.0-1.0
    keyword_overlap: float  # 0.0-1.0

    # 健康度指标
    completeness_score: float  # 0.0-1.0
    consistency_score: float  # 0.0-1.0
    freshness_score: float  # 0.0-1.0

    # 推荐指标
    recommended_prompt_level: str  # "00", "01", "02", "03"
    recommended_actions: List[str]
    warnings: List[str]


class ContextFundamentalsCalculator:
    """上下文基础计算器"""

    # Token估算常量
    CHARS_PER_TOKEN_EN = 4.0  # 英文
    CHARS_PER_TOKEN_CN = 1.5  # 中文
    CHARS_PER_TOKEN_MIXED = 2.5  # 中英混合

    # 阈值定义
    OPTIMAL_TOKEN_COUNT = 10000
    MAX_TOKEN_COUNT = 50000
    WARNING_TOKEN_COUNT = 30000

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化计算器

        Args:
            config: 配置参数
        """
        self.config = config or {}

    def calculate(self, request: str, context: Optional[Dict[str, Any]] = None) -> ContextMetrics:
        """
        计算上下文指标

        Args:
            request: 用户请求
            context: 附加上下文

        Returns:
            ContextMetrics: 计算结果
        """
        # 1. 计算基础指标
        character_count = len(request)
        word_count = self._count_words(request)
        line_count = self._count_lines(request)
        token_count = self._estimate_tokens(request)

        if context:
            context_str = str(context)
            character_count += len(context_str)
            token_count += self._estimate_tokens(context_str)

        # 2. 计算复杂度指标
        complexity_score = self._calculate_complexity_score(request, context)
        information_density = self._calculate_information_density(request)
        structure_quality = self._calculate_structure_quality(request, context)

        # 3. 计算相关性指标
        relevance_score = self._calculate_relevance_score(request, context)
        keyword_overlap = self._calculate_keyword_overlap(request, context)

        # 4. 计算健康度指标
        completeness_score = self._calculate_completeness_score(request, context)
        consistency_score = self._calculate_consistency_score(context)
        freshness_score = self._calculate_freshness_score(context)

        # 5. 推荐提示词层次
        recommended_level = self._recommend_prompt_level(
            complexity_score, token_count, information_density
        )

        # 6. 生成推荐操作和警告
        recommended_actions = self._generate_recommendations(
            token_count, complexity_score, relevance_score, completeness_score
        )
        warnings = self._generate_warnings(
            token_count, complexity_score, consistency_score
        )

        return ContextMetrics(
            token_count=token_count,
            character_count=character_count,
            word_count=word_count,
            line_count=line_count,
            complexity_score=complexity_score,
            information_density=information_density,
            structure_quality=structure_quality,
            relevance_score=relevance_score,
            keyword_overlap=keyword_overlap,
            completeness_score=completeness_score,
            consistency_score=consistency_score,
            freshness_score=freshness_score,
            recommended_prompt_level=recommended_level,
            recommended_actions=recommended_actions,
            warnings=warnings
        )

    def _count_words(self, text: str) -> int:
        """计算字数（中文按字符，英文按单词）"""
        # 中文
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        # 英文单词
        english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
        return chinese_chars + english_words

    def _count_lines(self, text: str) -> int:
        """计算行数"""
        return len(text.split('\n'))

    def _estimate_tokens(self, text: str) -> int:
        """估算token数量"""
        # 检测语言比例
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        total_chars = len(text)
        chinese_ratio = chinese_chars / total_chars if total_chars > 0 else 0

        # 根据语言比例选择估算方法
        if chinese_ratio > 0.7:
            # 主要中文
            chars_per_token = self.CHARS_PER_TOKEN_CN
        elif chinese_ratio < 0.3:
            # 主要英文
            chars_per_token = self.CHARS_PER_TOKEN_EN
        else:
            # 混合
            chars_per_token = self.CHARS_PER_TOKEN_MIXED

        estimated_tokens = int(total_chars / chars_per_token)
        return estimated_tokens

    def _calculate_complexity_score(self, request: str, context: Optional[Dict[str, Any]]) -> float:
        """计算复杂度分数（0.0-1.0）"""
        score = 0.0

        # 因素1：请求长度（0-0.25）- 增加权重
        request_len = len(request)
        if request_len < 50:
            length_score = 0.0
        elif request_len < 100:
            length_score = 0.05
        elif request_len < 200:
            length_score = 0.10
        elif request_len < 500:
            length_score = 0.15
        elif request_len < 1000:
            length_score = 0.20
        else:
            length_score = 0.25
        score += length_score

        # 因素2：问题数量（0-0.15）
        question_count = sum(request.count(marker) for marker in ['？', '?', '如何', '怎么', 'what', 'how'])
        if question_count <= 1:
            question_score = 0.0
        elif question_count <= 2:
            question_score = 0.08
        elif question_count <= 4:
            question_score = 0.12
        else:
            question_score = 0.15
        score += question_score

        # 因素3：技术术语密度（0-0.2）
        tech_terms = [
            'context', '上下文', 'token', 'AI', 'model', '系统', '架构', 'algorithm',
            '分布式', '微服务', '失效', '模式', '动态', '缓存', '版本控制', '性能优化',
            '安全性', '协作', '智能'
        ]
        tech_term_count = sum(1 for term in tech_terms if term.lower() in request.lower())
        tech_score = min(tech_term_count * 0.03, 0.2)
        score += tech_score

        # 因素4：上下文复杂度（0-0.2）
        if context:
            context_str = str(context)
            context_size = len(context_str)

            # 检查上下文中的数值（如services: 50）
            import re
            numbers = re.findall(r'\b\d+\b', context_str)
            has_large_numbers = any(int(n) > 10 for n in numbers)

            if context_size < 100:
                context_score = 0.05
            elif context_size < 1000:
                context_score = 0.10
            elif has_large_numbers or context_size < 5000:
                context_score = 0.15
            else:
                context_score = 0.20
        else:
            context_score = 0.0
        score += context_score

        # 因素5：抽象程度和复合度（0-0.2）
        abstract_keywords = [
            '原理', '机制', '设计', '架构', '优化', '最佳实践', 'pattern', 'design',
            '分布式', '多个', '多种', '同时', '集成', '实现', '策略', '考虑'
        ]
        abstract_count = sum(request.count(keyword) for keyword in abstract_keywords)
        abstract_score = min(abstract_count * 0.03, 0.2)
        score += abstract_score

        return min(score, 1.0)

    def _calculate_information_density(self, request: str) -> float:
        """计算信息密度（0.0-1.0）"""
        if not request:
            return 0.0

        # 计算有效字符比例（字母、数字、中文）
        valid_chars = sum(1 for c in request if c.isalnum() or '\u4e00' <= c <= '\u9fff')
        density = valid_chars / len(request)

        return min(density, 1.0)

    def _calculate_structure_quality(self, request: str, context: Optional[Dict[str, Any]]) -> float:
        """计算结构质量（0.0-1.0）"""
        score = 0.0

        # 因素1：是否有结构标记（0-0.4）
        structure_markers = ['\n', '，', '。', '.', ',', '、', ';', '；']
        marker_count = sum(request.count(marker) for marker in structure_markers)
        structure_score = min(marker_count / 20, 0.4)
        score += structure_score

        # 因素2：上下文结构（0-0.3）
        if context and isinstance(context, dict):
            # 有结构的上下文
            if len(context.keys()) > 0:
                score += 0.3

        # 因素3：逻辑连贯性（0-0.3）
        # 简化：检查是否有连接词
        connectives = ['因为', '所以', '但是', '然后', 'because', 'therefore', 'however', 'then']
        connective_count = sum(1 for word in connectives if word in request)
        connective_score = min(connective_count * 0.1, 0.3)
        score += connective_score

        return min(score, 1.0)

    def _calculate_relevance_score(self, request: str, context: Optional[Dict[str, Any]]) -> float:
        """计算相关性分数（0.0-1.0）"""
        # 简化实现：基于关键词匹配
        # 实际应该使用语义相似度

        # 基础相关性（0.5）
        score = 0.5

        if not context:
            return score

        # 提取请求中的关键词
        request_words = set(re.findall(r'\w+', request.lower()))

        # 计算上下文中的关键词
        context_str = str(context).lower()
        context_words = set(re.findall(r'\w+', context_str))

        # 计算重叠率
        if request_words:
            overlap = len(request_words & context_words)
            relevance = overlap / len(request_words)
            score += relevance * 0.5

        return min(score, 1.0)

    def _calculate_keyword_overlap(self, request: str, context: Optional[Dict[str, Any]]) -> float:
        """计算关键词重叠度（0.0-1.0）"""
        if not context:
            return 0.0

        # 提取关键词
        request_keywords = set(re.findall(r'\w+', request.lower()))
        context_str = str(context).lower()
        context_keywords = set(re.findall(r'\w+', context_str))

        if not request_keywords:
            return 0.0

        # 计算Jaccard相似度
        intersection = len(request_keywords & context_keywords)
        union = len(request_keywords | context_keywords)

        if union == 0:
            return 0.0

        return intersection / union

    def _calculate_completeness_score(self, request: str, context: Optional[Dict[str, Any]]) -> float:
        """计算完整性分数（0.0-1.0）"""
        score = 0.0

        # 因素1：请求长度是否合理（0-0.3）
        request_len = len(request)
        if 20 <= request_len <= 1000:
            score += 0.3
        elif request_len >= 10:
            score += 0.15

        # 因素2：是否有上下文（0-0.3）
        if context:
            score += 0.3

        # 因素3：问题是否明确（0-0.4）
        # 检查是否有问号或疑问词
        has_question = any(marker in request for marker in ['？', '?', '如何', '怎么', 'what', 'how'])
        if has_question:
            score += 0.4

        return min(score, 1.0)

    def _calculate_consistency_score(self, context: Optional[Dict[str, Any]]) -> float:
        """计算一致性分数（0.0-1.0）"""
        if not context:
            return 1.0  # 没有上下文，视为一致

        # 简化实现：检查是否有明显的矛盾
        # 实际应该更复杂
        score = 1.0

        # 检查是否有版本冲突
        if 'version' in str(context).lower():
            # 可能有多个版本信息
            score -= 0.2

        return max(score, 0.0)

    def _calculate_freshness_score(self, context: Optional[Dict[str, Any]]) -> float:
        """计算新鲜度分数（0.0-1.0）"""
        if not context:
            return 1.0

        # 简化实现：如果上下文包含时间戳，检查是否新鲜
        # 实际应该解析时间戳
        score = 1.0

        context_str = str(context)
        if 'timestamp' in context_str or '时间' in context_str:
            # 有时间信息，假设是新鲜的
            score = 0.9

        return score

    def _recommend_prompt_level(self, complexity_score: float, token_count: int, information_density: float) -> str:
        """推荐提示词层次"""
        # 根据复杂度、token数量、信息密度推荐

        # Level 00: 核心概念（最简单）
        if complexity_score < 0.3 and token_count < 5000:
            return "00"

        # Level 01: 基础应用（常见场景）
        elif complexity_score < 0.5 and token_count < 10000:
            return "01"

        # Level 02: 中级场景（复杂任务）
        elif complexity_score < 0.7 or token_count < 20000:
            return "02"

        # Level 03: 高级应用（大规模系统）
        else:
            return "03"

    def _generate_recommendations(self, token_count: int, complexity: float, relevance: float, completeness: float) -> List[str]:
        """生成推荐操作"""
        recommendations = []

        # Token相关建议
        if token_count > self.WARNING_TOKEN_COUNT:
            recommendations.append("考虑精简上下文或分解任务")
        elif token_count < 1000:
            recommendations.append("可以添加更多细节以获得更好的回答")

        # 复杂度相关建议
        if complexity > 0.7:
            recommendations.append("复杂任务，建议使用task-decomposer技能分解")

        # 相关性相关建议
        if relevance < 0.5:
            recommendations.append("上下文相关性较低，建议移除无关信息")

        # 完整性相关建议
        if completeness < 0.6:
            recommendations.append("请求不够完整，建议添加更多背景信息")

        # 如果没有问题
        if not recommendations:
            recommendations.append("上下文状态良好")

        return recommendations

    def _generate_warnings(self, token_count: int, complexity: float, consistency: float) -> List[str]:
        """生成警告"""
        warnings = []

        if token_count > self.MAX_TOKEN_COUNT:
            warnings.append("⚠️ 上下文过大，可能导致性能下降")

        if complexity > 0.8:
            warnings.append("⚠️ 任务复杂度很高，建议分步进行")

        if consistency < 0.7:
            warnings.append("⚠️ 上下文可能存在矛盾信息")

        return warnings


# 便捷函数
def calculate_metrics(request: str, context: Optional[Dict[str, Any]] = None) -> ContextMetrics:
    """
    计算指标的便捷函数

    Args:
        request: 用户请求
        context: 附加上下文

    Returns:
        ContextMetrics: 计算结果
    """
    calculator = ContextFundamentalsCalculator()
    return calculator.calculate(request, context)


if __name__ == "__main__":
    # 测试
    test_cases = [
        ("什么是上下文？", None),
        ("如何优化AI系统的上下文管理？请详细说明最佳实践", {"context": "系统架构"}),
        ("我需要在一个包含100个文件的项目中进行大规模重构，需要考虑上下文管理、团队协作、性能优化等多个方面", {"size": "large"}),
    ]

    for request, context in test_cases:
        print(f"\n{'='*60}")
        print(f"请求: {request}")
        print(f"上下文: {context}")
        print('='*60)

        metrics = calculate_metrics(request, context)

        print(f"\n📊 基础指标:")
        print(f"  Token数量: {metrics.token_count:,}")
        print(f"  字符数: {metrics.character_count:,}")
        print(f"  字数: {metrics.word_count:,}")
        print(f"  行数: {metrics.line_count}")

        print(f"\n🎯 复杂度指标:")
        print(f"  复杂度分数: {metrics.complexity_score:.2f}")
        print(f"  信息密度: {metrics.information_density:.2f}")
        print(f"  结构质量: {metrics.structure_quality:.2f}")

        print(f"\n🔗 相关性指标:")
        print(f"  相关性分数: {metrics.relevance_score:.2f}")
        print(f"  关键词重叠: {metrics.keyword_overlap:.2f}")

        print(f"\n✅ 健康度指标:")
        print(f"  完整性分数: {metrics.completeness_score:.2f}")
        print(f"  一致性分数: {metrics.consistency_score:.2f}")
        print(f"  新鲜度分数: {metrics.freshness_score:.2f}")

        print(f"\n💡 推荐:")
        print(f"  提示词层次: Level {metrics.recommended_prompt_level}")
        print(f"  操作建议:")
        for action in metrics.recommended_actions:
            print(f"    - {action}")

        if metrics.warnings:
            print(f"  警告:")
            for warning in metrics.warnings:
                print(f"    {warning}")
