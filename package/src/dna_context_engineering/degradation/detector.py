"""
上下文腐化检测器 - 检测各种腐化信号
"""
import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from .metrics import (
    DegradationSignal,
    ExplosionRisk,
    CorruptionRisk,
    DegradationReport,
    DegradationType,
    SeverityLevel
)


class DegradationDetector:
    """上下文腐化检测器"""

    def __init__(self):
        self.baseline_metrics = {}  # 基线指标
        self.historical_data = {}  # 历史数据

    def detect_degradation(
        self,
        context_id: str,
        context_content: str,
        previous_metrics: Optional[Dict] = None
    ) -> DegradationReport:
        """
        检测上下文腐化

        Args:
            context_id: 上下文标识符
            context_content: 上下文内容
            previous_metrics: 上次检测的指标

        Returns:
            DegradationReport: 腐化检测报告
        """
        print(f"检测上下文腐化: {context_id}")

        report = DegradationReport(context_id=context_id)

        # 1. 检测爆炸风险
        explosion_risk = self._detect_explosion_risk(context_content, previous_metrics)
        report.explosion_risk = explosion_risk

        if explosion_risk.is_critical:
            report.signals.append(DegradationSignal(
                signal_type=DegradationType.EXPLOSION,
                severity=explosion_risk.risk_level,
                description=f"上下文爆炸风险: 大小={explosion_risk.current_size}, 增长率={explosion_risk.growth_rate:.1%}",
                metrics={
                    'size': explosion_risk.current_size,
                    'growth_rate': explosion_risk.growth_rate,
                    'redundancy': explosion_risk.redundancy_ratio
                },
                recommendations=[
                    "立即压缩上下文内容",
                    "删除冗余信息",
                    "提取核心信息"
                ]
            ))

        # 2. 检测腐化风险
        corruption_risk = self._detect_corruption_risk(context_content, previous_metrics)
        report.corruption_risk = corruption_risk

        if corruption_risk.is_critical:
            report.signals.append(DegradationSignal(
                signal_type=DegradationType.CORRUPTION,
                severity=corruption_risk.risk_level,
                description=f"上下文腐化风险: 清晰度={corruption_risk.clarity_score:.2f}, 质量下降={corruption_risk.quality_decline_rate:.1%}",
                metrics={
                    'clarity': corruption_risk.clarity_score,
                    'consistency': corruption_risk.consistency_score,
                    'decline_rate': corruption_risk.quality_decline_rate
                },
                recommendations=[
                    "改进内容组织结构",
                    "统一术语使用",
                    "提升表述清晰度"
                ]
            ))

        # 3. 检测不一致
        inconsistency_signals = self._detect_inconsistency(context_content)
        report.signals.extend(inconsistency_signals)

        # 4. 检测过时内容
        obsolescence_signals = self._detect_obsolescence(context_content)
        report.signals.extend(obsolescence_signals)

        # 5. 检测碎片化
        fragmentation_signals = self._detect_fragmentation(context_content)
        report.signals.extend(fragmentation_signals)

        # 6. 计算整体风险等级
        report.overall_risk_level = self._calculate_overall_risk(report.signals)
        report.health_score = self._calculate_health_score(report)

        # 7. 生成建议行动
        report.recommended_actions = self._generate_actions(report)

        return report

    def _detect_explosion_risk(
        self,
        content: str,
        previous_metrics: Optional[Dict]
    ) -> ExplosionRisk:
        """检测爆炸风险"""
        # 计算token数量（粗略估计：中文1字符≈0.5 token）
        current_size = int(len(content) / 2)

        # 计算增长率
        growth_rate = 0.0
        if previous_metrics and 'size' in previous_metrics:
            previous_size = previous_metrics['size']
            if previous_size > 0:
                growth_rate = (current_size - previous_size) / previous_size

        # 检测冗余
        redundancy_ratio = self._calculate_redundancy(content)

        # 确定风险等级
        if current_size > 50000 or growth_rate > 0.5 or redundancy_ratio > 0.5:
            risk_level = SeverityLevel.CRITICAL
        elif current_size > 30000 or growth_rate > 0.3 or redundancy_ratio > 0.4:
            risk_level = SeverityLevel.HIGH
        elif current_size > 20000 or growth_rate > 0.2 or redundancy_ratio > 0.3:
            risk_level = SeverityLevel.MEDIUM
        else:
            risk_level = SeverityLevel.LOW

        return ExplosionRisk(
            current_size=current_size,
            growth_rate=growth_rate,
            redundancy_ratio=redundancy_ratio,
            risk_level=risk_level
        )

    def _detect_corruption_risk(
        self,
        content: str,
        previous_metrics: Optional[Dict]
    ) -> CorruptionRisk:
        """检测腐化风险"""
        # 评估清晰度
        clarity_score = self._assess_clarity(content)

        # 评估一致性
        consistency_score = self._assess_consistency(content)

        # 计算质量下降率
        decline_rate = 0.0
        if previous_metrics and 'quality_score' in previous_metrics:
            previous_quality = previous_metrics['quality_score']
            current_quality = (clarity_score + consistency_score) / 2
            if previous_quality > 0:
                decline_rate = (previous_quality - current_quality) / previous_quality

        # 确定风险等级
        if clarity_score < 0.3 or consistency_score < 0.3 or decline_rate > 0.3:
            risk_level = SeverityLevel.CRITICAL
        elif clarity_score < 0.5 or consistency_score < 0.5 or decline_rate > 0.2:
            risk_level = SeverityLevel.HIGH
        elif clarity_score < 0.7 or consistency_score < 0.7 or decline_rate > 0.1:
            risk_level = SeverityLevel.MEDIUM
        else:
            risk_level = SeverityLevel.LOW

        return CorruptionRisk(
            clarity_score=clarity_score,
            consistency_score=consistency_score,
            quality_decline_rate=decline_rate,
            risk_level=risk_level
        )

    def _detect_inconsistency(self, content: str) -> List[DegradationSignal]:
        """检测不一致"""
        signals = []

        # 检测术语冲突（简单示例）
        # 同一概念的多种表述
        term_variations = {
            '用户': ['账号', '账户', '使用者', 'User'],
            '登录': ['登入', 'signin', '登录系统'],
            '认证': ['验证', 'auth', '身份验证']
        }

        for concept, variations in term_variations.items():
            found_terms = [concept]
            for var in variations:
                if var in content:
                    found_terms.append(var)

            if len(found_terms) > 2:  # 发现多个变体
                signals.append(DegradationSignal(
                    signal_type=DegradationType.INCONSISTENCY,
                    severity=SeverityLevel.MEDIUM,
                    description=f"术语不一致: '{concept}' 有多个变体: {', '.join(found_terms)}",
                    metrics={'variations_count': len(found_terms)},
                    recommendations=[f"统一使用 '{concept}' 作为标准术语"]
                ))

        return signals

    def _detect_obsolescence(self, content: str) -> List[DegradationSignal]:
        """检测过时内容"""
        signals = []

        # 检测可能的过时标记
        obsolete_markers = [
            r'待更新',
            r'TODO',
            r'FIXME',
            r'旧版本',
            r'deprecated',
            r'版本\d+\.'
        ]

        for marker in obsolete_markers:
            if re.search(marker, content, re.IGNORECASE):
                signals.append(DegradationSignal(
                    signal_type=DegradationType.OBSOLESCENCE,
                    severity=SeverityLevel.LOW,
                    description=f"发现可能的过时内容: {marker}",
                    recommendations=["审查并更新过时内容"]
                ))

        return signals

    def _detect_fragmentation(self, content: str) -> List[DegradationSignal]:
        """检测碎片化"""
        signals = []

        # 检查结构标记
        has_structure = (
            '#' in content and  # 有标题
            ('```' in content or '```' in content)  # 有代码块
        )

        if not has_structure and len(content) > 1000:
            signals.append(DegradationSignal(
                signal_type=DegradationType.FRAGMENTATION,
                severity=SeverityLevel.MEDIUM,
                description="内容缺乏结构化组织，难以理解",
                metrics={'has_headers': '#' in content, 'has_code_blocks': '```' in content},
                recommendations=[
                    "添加标题层次结构",
                    "使用代码块突出重要内容",
                    "使用列表组织信息"
                ]
            ))

        return signals

    def _calculate_redundancy(self, content: str) -> float:
        """计算冗余比例"""
        # 简单方法：检测重复的句子或段落
        lines = content.split('\n')
        unique_lines = set(lines)
        if len(lines) > 0:
            return 1.0 - (len(unique_lines) / len(lines))
        return 0.0

    def _assess_clarity(self, content: str) -> float:
        """评估清晰度"""
        score = 0.5  # 基础分

        # 有结构加分
        if '##' in content:
            score += 0.15
        if '```' in content:
            score += 0.15
        if '-' in content or '*' in content:  # 有列表
            score += 0.10

        # 内容过长扣分
        if len(content) > 10000:
            score -= 0.10
        if len(content) > 30000:
            score -= 0.20

        return max(0.0, min(1.0, score))

    def _assess_consistency(self, content: str) -> float:
        """评估一致性"""
        score = 0.8  # 基础分（假设大部分内容是一致的）

        # 检测术语冲突
        conflicts = len(self._detect_inconsistency(content))
        score -= conflicts * 0.1

        return max(0.0, min(1.0, score))

    def _calculate_overall_risk(self, signals: List[DegradationSignal]) -> SeverityLevel:
        """计算整体风险等级"""
        if not signals:
            return SeverityLevel.LOW

        # 统计各级别信号数量
        critical_count = sum(1 for s in signals if s.severity == SeverityLevel.CRITICAL)
        high_count = sum(1 for s in signals if s.severity == SeverityLevel.HIGH)
        medium_count = sum(1 for s in signals if s.severity == SeverityLevel.MEDIUM)

        if critical_count > 0:
            return SeverityLevel.CRITICAL
        elif high_count >= 2:
            return SeverityLevel.HIGH
        elif high_count >= 1 or medium_count >= 3:
            return SeverityLevel.MEDIUM
        else:
            return SeverityLevel.LOW

    def _calculate_health_score(self, report: DegradationReport) -> float:
        """计算健康度评分"""
        score = 1.0

        # 根据信号数量和严重程度扣分
        for signal in report.signals:
            if signal.severity == SeverityLevel.CRITICAL:
                score -= 0.3
            elif signal.severity == SeverityLevel.HIGH:
                score -= 0.15
            elif signal.severity == SeverityLevel.MEDIUM:
                score -= 0.05

        # 根据风险等级调整
        if report.explosion_risk and report.explosion_risk.is_critical:
            score -= 0.2
        if report.corruption_risk and report.corruption_risk.is_critical:
            score -= 0.2

        return max(0.0, min(1.0, score))

    def _generate_actions(self, report: DegradationReport) -> List[str]:
        """生成建议行动"""
        actions = []

        if report.requires_immediate_action:
            actions.append("🚨 立即执行上下文优化")

        if report.explosion_risk and report.explosion_risk.redundancy_ratio > 0.3:
            actions.append("🗑️ 删除冗余内容")

        if report.corruption_risk and report.corruption_risk.clarity_score < 0.6:
            actions.append("✍️ 改进内容清晰度")

        if any(s.signal_type == DegradationType.INCONSISTENCY for s in report.signals):
            actions.append("🔧 统一术语使用")

        if not actions:
            actions.append("✅ 上下文健康，继续监控")

        return actions
