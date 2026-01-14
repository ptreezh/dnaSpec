"""
上下文腐化检测系统 - 核心指标定义
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime


class DegradationType(Enum):
    """腐化类型"""
    EXPLOSION = "explosion"  # 上下文爆炸（内容过多）
    CORRUPTION = "corruption"  # 上下文腐化（质量下降）
    INCONSISTENCY = "inconsistency"  # 不一致（术语冲突）
    OBSOLESCENCE = "obsolescence"  # 过时（内容过时）
    FRAGMENTATION = "fragmentation"  # 碎片化（结构混乱)


class SeverityLevel(Enum):
    """严重程度"""
    LOW = "low"  # 低（警告）
    MEDIUM = "medium"  # 中（需要注意）
    HIGH = "high"  # 高（必须处理）
    CRITICAL = "critical"  # 严重（立即处理）


class RiskFactor(Enum):
    """风险因子"""
    SIZE_GROWTH = "size_growth"  # 大小增长
    QUALITY_DECLINE = "quality_decline"  # 质量下降
    REDUNDANCY_INCREASE = "redundancy_increase"  # 冗余增加
    COMPLEXITY_SPIKE = "complexity_spike"  # 复杂度激增


@dataclass
class DegradationSignal:
    """腐化信号"""
    signal_type: DegradationType
    severity: SeverityLevel
    description: str
    detected_at: datetime = field(default_factory=datetime.now)
    metrics: Dict[str, float] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class ExplosionRisk:
    """爆炸风险指标"""
    current_size: int  # 当前大小（tokens）
    growth_rate: float  # 增长率（相对于上次）
    redundancy_ratio: float  # 冗余比例（0-1）
    risk_level: SeverityLevel

    @property
    def is_critical(self) -> bool:
        """是否处于危险水平"""
        return (
            self.current_size > 50000 or
            self.growth_rate > 0.3 or
            self.redundancy_ratio > 0.4
        )


@dataclass
class CorruptionRisk:
    """腐化风险指标"""
    clarity_score: float  # 清晰度（0-1）
    consistency_score: float  # 一致性（0-1）
    quality_decline_rate: float  # 质量下降率
    risk_level: SeverityLevel

    @property
    def is_critical(self) -> bool:
        """是否处于危险水平"""
        return (
            self.clarity_score < 0.5 or
            self.consistency_score < 0.5 or
            self.quality_decline_rate > 0.2
        )


@dataclass
class DegradationReport:
    """腐化检测报告"""
    context_id: str
    scanned_at: datetime = field(default_factory=datetime.now)

    # 检测到的信号
    signals: List[DegradationSignal] = field(default_factory=list)

    # 风险评估
    explosion_risk: Optional[ExplosionRisk] = None
    corruption_risk: Optional[CorruptionRisk] = None

    # 整体评估
    overall_risk_level: SeverityLevel = SeverityLevel.LOW
    health_score: float = 1.0  # 健康度（0-1）

    # 建议行动
    recommended_actions: List[str] = field(default_factory=list)

    @property
    def needs_attention(self) -> bool:
        """是否需要注意"""
        return self.overall_risk_level in [SeverityLevel.MEDIUM, SeverityLevel.HIGH, SeverityLevel.CRITICAL]

    @property
    def requires_immediate_action(self) -> bool:
        """是否需要立即行动"""
        return self.overall_risk_level in [SeverityLevel.HIGH, SeverityLevel.CRITICAL]
