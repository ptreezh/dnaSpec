"""
评估框架核心指标定义
"""
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
from datetime import datetime

class MetricType(Enum):
    """指标类型"""
    QUALITY = "quality"  # 质量指标
    PERFORMANCE = "performance"  # 性能指标
    USABILITY = "usability"  # 可用性指标
    RELIABILITY = "reliability"  # 可靠性指标

class ScoreLevel(Enum):
    """评分等级"""
    EXCELLENT = "excellent"  # 优秀 (0.9-1.0)
    GOOD = "good"  # 良好 (0.75-0.9)
    SATISFACTORY = "satisfactory"  # 满意 (0.6-0.75)
    NEEDS_IMPROVEMENT = "needs_improvement"  # 需改进 (0.4-0.6)
    POOR = "poor"  # 差 (0.0-0.4)

@dataclass
class QualityScore:
    """质量评分"""
    clarity: float  # 清晰度 (0-1)
    completeness: float  # 完整性 (0-1)
    consistency: float  # 一致性 (0-1)
    efficiency: float  # 效率 (0-1)
    relevance: float  # 相关性 (0-1)

    @property
    def overall(self) -> float:
        """总体评分（加权平均）"""
        weights = {
            'clarity': 0.25,
            'completeness': 0.25,
            'consistency': 0.20,
            'efficiency': 0.15,
            'relevance': 0.15
        }
        return (
            self.clarity * weights['clarity'] +
            self.completeness * weights['completeness'] +
            self.consistency * weights['consistency'] +
            self.efficiency * weights['efficiency'] +
            self.relevance * weights['relevance']
        )

    @property
    def level(self) -> ScoreLevel:
        """评分等级"""
        score = self.overall
        if score >= 0.9:
            return ScoreLevel.EXCELLENT
        elif score >= 0.75:
            return ScoreLevel.GOOD
        elif score >= 0.6:
            return ScoreLevel.SATISFACTORY
        elif score >= 0.4:
            return ScoreLevel.NEEDS_IMPROVEMENT
        else:
            return ScoreLevel.POOR

@dataclass
class PerformanceMetrics:
    """性能指标"""
    execution_time: float  # 执行时间（秒）
    memory_usage: float  # 内存使用（MB）
    token_count: int  # Token数量
    success_rate: float  # 成功率 (0-1)

@dataclass
class SkillEvaluationResult:
    """技能评估结果"""
    skill_name: str
    version: str
    evaluated_at: datetime = field(default_factory=datetime.now)

    # 质量评分
    quality_score: Optional[QualityScore] = None

    # 性能指标
    performance_metrics: Optional[PerformanceMetrics] = None

    # 测试结果
    tests_passed: int = 0
    tests_total: int = 0
    test_success_rate: float = 0.0

    # 问题列表
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

    @property
    def overall_score(self) -> float:
        """综合评分"""
        if self.quality_score:
            return self.quality_score.overall
        return 0.0

@dataclass
class SystemEvaluationResult:
    """系统评估结果"""
    evaluated_at: datetime = field(default_factory=datetime.now)

    # 技能评估结果
    skill_evaluations: Dict[str, SkillEvaluationResult] = field(default_factory=dict)

    # 系统整体指标
    total_skills: int = 0
    skills_passing_threshold: int = 0
    average_quality_score: float = 0.0

    # 协作评估
    collaboration_score: float = 0.0  # 技能协作评分

    # 用户体验
    usability_score: float = 0.0  # 可用性评分
    user_satisfaction: float = 0.0  # 用户满意度

    # 系统健康度
    health_status: str = "unknown"  # healthy, warning, critical

@dataclass
class TrendData:
    """趋势数据"""
    metric_name: str
    values: List[float] = field(default_factory=list)
    timestamps: List[datetime] = field(default_factory=list)

    @property
    def trend(self) -> str:
        """趋势方向"""
        if len(self.values) < 2:
            return "insufficient_data"
        recent = self.values[-3:] if len(self.values) >= 3 else self.values
        if all(recent[i] <= recent[i+1] for i in range(len(recent)-1)):
            return "improving"
        elif all(recent[i] >= recent[i+1] for i in range(len(recent)-1)):
            return "declining"
        else:
            return "stable"
