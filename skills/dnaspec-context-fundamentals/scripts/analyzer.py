"""
Context Fundamentals Analyzer

负责分析上下文的深度特征
提供确定性的分析逻辑
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum
import re


class ContextFailureMode(Enum):
    """上下文失效模式"""
    LOST_IN_THE_MIDDLE = "lost_in_the_middle"
    POISONING = "poisoning"
    DISTRACTION = "distraction"
    CLASH = "clash"
    OVERFLOW = "overflow"
    FRAGMENTATION = "fragmentation"


@dataclass
class FailureModeDetection:
    """失效模式检测结果"""
    mode: ContextFailureMode
    severity: str  # "low", "medium", "high"
    evidence: List[str]
    suggestions: List[str]


@dataclass
class ContextPattern:
    """上下文模式"""
    pattern_type: str  # "incremental", "layered", "on_demand", "isolated"
    confidence: float  # 0.0-1.0
    description: str


@dataclass
class ContextAnalysis:
    """上下文分析结果"""
    # 失效模式检测
    detected_failures: List[FailureModeDetection]

    # 模式识别
    recognized_patterns: List[ContextPattern]

    # 质量分析
    quality_scores: Dict[str, float]

    # 优化建议
    optimization_suggestions: List[str]

    # 推荐策略
    recommended_strategy: str


class ContextFundamentalsAnalyzer:
    """上下文基础分析器"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化分析器

        Args:
            config: 配置参数
        """
        self.config = config or {}

    def analyze(self, request: str, context: Optional[Dict[str, Any]] = None) -> ContextAnalysis:
        """
        分析上下文

        Args:
            request: 用户请求
            context: 附加上下文

        Returns:
            ContextAnalysis: 分析结果
        """
        # 1. 检测失效模式
        detected_failures = self._detect_failure_modes(request, context)

        # 2. 识别上下文模式
        recognized_patterns = self._recognize_patterns(context)

        # 3. 计算质量分数
        quality_scores = self._calculate_quality_scores(request, context)

        # 4. 生成优化建议
        optimization_suggestions = self._generate_optimization_suggestions(
            detected_failures, quality_scores
        )

        # 5. 推荐策略
        recommended_strategy = self._recommend_strategy(
            detected_failures, recognized_patterns, quality_scores
        )

        return ContextAnalysis(
            detected_failures=detected_failures,
            recognized_patterns=recognized_patterns,
            quality_scores=quality_scores,
            optimization_suggestions=optimization_suggestions,
            recommended_strategy=recommended_strategy
        )

    def _detect_failure_modes(self, request: str, context: Optional[Dict[str, Any]]) -> List[FailureModeDetection]:
        """检测失效模式"""
        detections = []

        # 1. Lost-in-the-Middle检测
        lost_middle = self._detect_lost_in_the_middle(context)
        if lost_middle:
            detections.append(lost_middle)

        # 2. 上下文毒化检测
        poisoning = self._detect_poisoning(context)
        if poisoning:
            detections.append(poisoning)

        # 3. 上下文分心检测
        distraction = self._detect_distraction(context)
        if distraction:
            detections.append(distraction)

        # 4. 上下文冲突检测
        clash = self._detect_clash(context)
        if clash:
            detections.append(clash)

        # 5. 上下文溢出检测
        overflow = self._detect_overflow(context)
        if overflow:
            detections.append(overflow)

        # 6. 上下文碎片化检测
        fragmentation = self._detect_fragmentation(context)
        if fragmentation:
            detections.append(fragmentation)

        return detections

    def _detect_lost_in_the_middle(self, context: Optional[Dict[str, Any]]) -> Optional[FailureModeDetection]:
        """检测Lost-in-the-Middle现象"""
        if not context:
            return None

        context_str = str(context)
        context_len = len(context_str)

        # 检测条件：上下文很长且包含大量列表或数组
        evidence = []
        severity = "low"

        # 检查长度
        if context_len > 50000:
            evidence.append(f"上下文很长（{context_len:,}字符）")
            severity = "medium"

        # 检查是否有长列表
        list_matches = re.findall(r'\[.*?\]', context_str)
        long_lists = [m for m in list_matches if len(m) > 100]
        if len(long_lists) > 3:
            evidence.append(f"包含{len(long_lists)}个长列表")
            severity = "high"

        # 检查是否有大量项
        if 'items' in str(context) or 'list' in str(context).lower():
            # 可能有很多项
            pass

        if evidence and severity != "low":
            return FailureModeDetection(
                mode=ContextFailureMode.LOST_IN_THE_MIDDLE,
                severity=severity,
                evidence=evidence,
                suggestions=[
                    "将关键信息放在开头或结尾",
                    "使用分段处理，避免一次性加载过多信息",
                    "使用渐进式信息披露",
                    "明确指出关键信息的位置"
                ]
            )

        return None

    def _detect_poisoning(self, context: Optional[Dict[str, Any]]) -> Optional[FailureModeDetection]:
        """检测上下文毒化"""
        if not context:
            return None

        evidence = []
        severity = "low"

        context_str = str(context).lower()

        # 检查是否有版本矛盾
        version_indicators = ['v1', 'v2', 'version', '版本', 'old', 'new']
        version_count = sum(context_str.count(indicator) for indicator in version_indicators)
        if version_count > 2:
            evidence.append("检测到多个版本信息")
            severity = "medium"

        # 检查是否有矛盾关键词
        contradiction_pairs = [
            ('true', 'false'),
            ('enabled', 'disabled'),
            ('allow', 'deny'),
            ('成功', '失败'),
            ('是', '否')
        ]
        for word1, word2 in contradiction_pairs:
            if word1 in context_str and word2 in context_str:
                evidence.append(f"检测到矛盾信息: {word1} vs {word2}")
                severity = "high"
                break

        if evidence:
            return FailureModeDetection(
                mode=ContextFailureMode.POISONING,
                severity=severity,
                evidence=evidence,
                suggestions=[
                    "明确版本控制，使用最新版本",
                    "移除过时信息",
                    "使用明确的优先级标记",
                    "验证信息一致性"
                ]
            )

        return None

    def _detect_distraction(self, context: Optional[Dict[str, Any]]) -> Optional[FailureModeDetection]:
        """检测上下文分心"""
        if not context:
            return None

        evidence = []
        severity = "low"

        context_str = str(context)
        context_len = len(context_str)

        # 检查上下文是否过大
        if context_len > 100000:  # 100K字符
            evidence.append(f"上下文很大（{context_len:,}字符）")
            severity = "medium"

        # 检查是否有大量重复内容
        # 简化：检查是否有重复的句子
        sentences = context_str.split('。')
        unique_sentences = set(sentences)
        if len(sentences) > 10 and len(unique_sentences) / len(sentences) < 0.7:
            evidence.append("检测到大量重复内容")
            severity = "medium"

        if evidence:
            return FailureModeDetection(
                mode=ContextFailureMode.DISTRACTION,
                severity=severity,
                evidence=evidence,
                suggestions=[
                    "过滤无关信息",
                    "使用相关性评分筛选",
                    "只保留核心内容",
                    "使用references/目录存储详细信息"
                ]
            )

        return None

    def _detect_clash(self, context: Optional[Dict[str, Any]]) -> Optional[FailureModeDetection]:
        """检测上下文冲突"""
        if not context or not isinstance(context, dict):
            return None

        evidence = []
        severity = "low"

        # 检查是否有多个源提供不同信息
        if 'sources' in context or '来源' in str(context):
            evidence.append("检测到多个信息源")
            severity = "medium"

        # 检查是否有不一致的数据
        # 简化：检查数值矛盾
        values = []
        def extract_values(obj):
            if isinstance(obj, dict):
                for v in obj.values():
                    extract_values(v)
            elif isinstance(obj, list):
                for item in obj:
                    extract_values(item)
            elif isinstance(obj, (int, float)):
                values.append(obj)

        extract_values(context)
        # 如果有大量数值，检查是否有明显矛盾
        # 这里简化处理

        if evidence:
            return FailureModeDetection(
                mode=ContextFailureMode.CLASH,
                severity=severity,
                evidence=evidence,
                suggestions=[
                    "明确信息优先级",
                    "使用统一的数据源",
                    "解决冲突标记不一致",
                    "建立冲突解决协议"
                ]
            )

        return None

    def _detect_overflow(self, context: Optional[Dict[str, Any]]) -> Optional[FailureModeDetection]:
        """检测上下文溢出"""
        if not context:
            return None

        evidence = []
        severity = "low"

        context_str = str(context)
        context_len = len(context_str)

        # 估算token数量（中文约1.5字符/token，英文约4字符/token）
        estimated_tokens = int(context_len / 2.5)

        if estimated_tokens > 100000:  # 100K tokens
            evidence.append(f"估算token数量: {estimated_tokens:,}")
            severity = "high"
        elif estimated_tokens > 50000:
            evidence.append(f"估算token数量: {estimated_tokens:,}")
            severity = "medium"

        if evidence:
            return FailureModeDetection(
                mode=ContextFailureMode.OVERFLOW,
                severity=severity,
                evidence=evidence,
                suggestions=[
                    "立即分解任务",
                    "使用独立工作区",
                    "应用原子化原则",
                    "实施渐进式披露"
                ]
            )

        return None

    def _detect_fragmentation(self, context: Optional[Dict[str, Any]]) -> Optional[FailureModeDetection]:
        """检测上下文碎片化"""
        if not context:
            return None

        evidence = []
        severity = "low"

        context_str = str(context)

        # 检查是否有大量短片段
        fragments = re.split(r'[,\n]', context_str)
        short_fragments = [f for f in fragments if 0 < len(f.strip()) < 20]
        if len(short_fragments) > 20:
            evidence.append(f"检测到{len(short_fragments)}个短片段")
            severity = "medium"

        # 检查结构是否松散
        # 简化：检查是否有足够的连接词
        connectives = ['因为', '所以', '但是', '因此', 'because', 'therefore', 'however']
        connective_count = sum(context_str.count(c) for c in connectives)
        if len(fragments) > 10 and connective_count < len(fragments) / 10:
            evidence.append("缺少逻辑连接")
            severity = "medium"

        if evidence:
            return FailureModeDetection(
                mode=ContextFailureMode.FRAGMENTATION,
                severity=severity,
                evidence=evidence,
                suggestions=[
                    "重组上下文结构",
                    "添加逻辑连接词",
                    "使用层次化组织",
                    "创建主题分组"
                ]
            )

        return None

    def _recognize_patterns(self, context: Optional[Dict[str, Any]]) -> List[ContextPattern]:
        """识别上下文模式"""
        patterns = []

        if not context:
            return patterns

        context_str = str(context)

        # 1. 增量模式（Incremental）
        if 'step' in context_str.lower() or 'phase' in context_str.lower() or '阶段' in context_str:
            patterns.append(ContextPattern(
                pattern_type="incremental",
                confidence=0.8,
                description="增量式上下文：分阶段逐步增加信息"
            ))

        # 2. 层次化模式（Layered）
        if 'layer' in context_str.lower() or 'level' in context_str.lower() or '层次' in context_str or '级别' in context_str:
            patterns.append(ContextPattern(
                pattern_type="layered",
                confidence=0.9,
                description="层次化上下文：按抽象级别组织"
            ))

        # 3. 按需模式（On-demand）
        if 'lazy' in context_str.lower() or 'dynamic' in context_str.lower() or '按需' in context_str:
            patterns.append(ContextPattern(
                pattern_type="on_demand",
                confidence=0.7,
                description="按需上下文：动态加载和卸载"
            ))

        # 4. 隔离模式（Isolated）
        if 'workspace' in context_str.lower() or 'isolated' in context_str.lower() or '隔离' in context_str:
            patterns.append(ContextPattern(
                pattern_type="isolated",
                confidence=0.85,
                description="隔离上下文：独立工作区，避免干扰"
            ))

        return patterns

    def _calculate_quality_scores(self, request: str, context: Optional[Dict[str, Any]]) -> Dict[str, float]:
        """计算质量分数"""
        scores = {}

        # 1. 完整性（0.0-1.0）
        completeness = 0.5
        if context:
            completeness += 0.3
        if len(request) > 20:
            completeness += 0.2
        scores['completeness'] = min(completeness, 1.0)

        # 2. 相关性（0.0-1.0）
        relevance = 0.6  # 默认中等相关
        if context:
            # 简化：基于关键词重叠
            request_words = set(re.findall(r'\w+', request.lower()))
            context_words = set(re.findall(r'\w+', str(context).lower()))
            if request_words:
                overlap = len(request_words & context_words) / len(request_words)
                relevance = 0.5 + overlap * 0.5
        scores['relevance'] = min(relevance, 1.0)

        # 3. 组织性（0.0-1.0）
        organization = 0.5
        if context and isinstance(context, dict):
            organization += 0.3  # 有结构的上下文
        # 检查是否有格式化
        if '\n' in request or '，' in request:
            organization += 0.2
        scores['organization'] = min(organization, 1.0)

        # 4. 清晰度（0.0-1.0）
        clarity = 0.5
        # 检查是否有明确的问题
        if any(marker in request for marker in ['？', '?', '如何', '怎么', 'what', 'how']):
            clarity += 0.3
        # 检查长度是否合理
        if 10 < len(request) < 1000:
            clarity += 0.2
        scores['clarity'] = min(clarity, 1.0)

        return scores

    def _generate_optimization_suggestions(
        self,
        failures: List[FailureModeDetection],
        scores: Dict[str, float]
    ) -> List[str]:
        """生成优化建议"""
        suggestions = []

        # 基于失效模式的建议
        for failure in failures:
            suggestions.extend(failure.suggestions)

        # 基于质量分数的建议
        if scores.get('completeness', 0) < 0.7:
            suggestions.append("补充更多背景信息和需求细节")

        if scores.get('relevance', 0) < 0.7:
            suggestions.append("移除无关信息，提高上下文相关性")

        if scores.get('organization', 0) < 0.7:
            suggestions.append("使用清晰的结构组织上下文")

        if scores.get('clarity', 0) < 0.7:
            suggestions.append("用明确的语言描述问题和需求")

        # 去重
        suggestions = list(set(suggestions))

        return suggestions

    def _recommend_strategy(
        self,
        failures: List[FailureModeDetection],
        patterns: List[ContextPattern],
        scores: Dict[str, float]
    ) -> str:
        """推荐策略"""
        # 检查是否有严重失效
        critical_failures = [f for f in failures if f.severity == "high"]

        if critical_failures:
            return "立即修复：首先解决严重的上下文失效模式"

        # 检查是否有已识别的模式
        if patterns:
            best_pattern = max(patterns, key=lambda p: p.confidence)
            return f"优化现有模式：{best_pattern.description}"

        # 检查整体质量
        avg_quality = sum(scores.values()) / len(scores) if scores else 0.5

        if avg_quality > 0.8:
            return "保持现状：上下文质量良好"

        elif avg_quality > 0.6:
            return "渐进优化：逐步改进上下文质量"

        else:
            return "重构上下文：使用推荐的4层渐进式架构"


# 便捷函数
def analyze_context(request: str, context: Optional[Dict[str, Any]] = None) -> ContextAnalysis:
    """
    分析上下文的便捷函数

    Args:
        request: 用户请求
        context: 附加上下文

    Returns:
        ContextAnalysis: 分析结果
    """
    analyzer = ContextFundamentalsAnalyzer()
    return analyzer.analyze(request, context)


if __name__ == "__main__":
    # 测试
    test_cases = [
        ("什么是上下文？", None),
        ("在一个大项目中如何管理上下文？", {"project": "large", "files": ["file1", "file2", "file3"] * 100}),
        ("版本v1说使用A方法，但v2说使用B方法，应该听哪个？", {"v1": "method A", "v2": "method B"}),
    ]

    for request, context in test_cases:
        print(f"\n{'='*60}")
        print(f"请求: {request}")
        print('='*60)

        analysis = analyze_context(request, context)

        # 失效模式
        if analysis.detected_failures:
            print(f"\n⚠️ 检测到的失效模式:")
            for failure in analysis.detected_failures:
                print(f"\n  {failure.mode.value} ({failure.severity}):")
                print(f"    证据:")
                for evidence in failure.evidence:
                    print(f"      - {evidence}")
                print(f"    建议:")
                for suggestion in failure.suggestions:
                    print(f"      - {suggestion}")
        else:
            print(f"\n✅ 未检测到失效模式")

        # 识别的模式
        if analysis.recognized_patterns:
            print(f"\n🔍 识别的上下文模式:")
            for pattern in analysis.recognized_patterns:
                print(f"  - {pattern.pattern_type} (置信度: {pattern.confidence:.2f})")
                print(f"    {pattern.description}")

        # 质量分数
        print(f"\n📊 质量分数:")
        for metric, score in analysis.quality_scores.items():
            print(f"  {metric}: {score:.2f}")

        # 优化建议
        if analysis.optimization_suggestions:
            print(f"\n💡 优化建议:")
            for suggestion in analysis.optimization_suggestions:
                print(f"  - {suggestion}")

        # 推荐策略
        print(f"\n🎯 推荐策略:")
        print(f"  {analysis.recommended_strategy}")
