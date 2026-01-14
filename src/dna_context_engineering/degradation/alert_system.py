"""
告警系统 - 管理和发送告警
"""
from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass

from .metrics import DegradationReport, DegradationSignal, SeverityLevel


@dataclass
class Alert:
    """告警"""
    alert_id: str
    context_id: str
    severity: SeverityLevel
    message: str
    created_at: datetime
    signals: List[DegradationSignal]
    recommended_actions: List[str]
    acknowledged: bool = False
    resolved: bool = False


class AlertManager:
    """告警管理器"""

    def __init__(self):
        self.alerts = []  # List[Alert]
        self.alert_rules = self._init_rules()

    def create_alert_from_report(self, report: DegradationReport) -> Optional[Alert]:
        """从检测报告创建告警"""
        if not report.needs_attention:
            return None

        alert_id = f"ALERT-{report.context_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # 生成告警消息
        message = self._generate_alert_message(report)

        alert = Alert(
            alert_id=alert_id,
            context_id=report.context_id,
            severity=report.overall_risk_level,
            message=message,
            created_at=datetime.now(),
            signals=report.signals,
            recommended_actions=report.recommended_actions
        )

        self.alerts.append(alert)
        return alert

    def _generate_alert_message(self, report: DegradationReport) -> str:
        """生成告警消息"""
        if report.requires_immediate_action:
            prefix = "🚨 严重告警"
        elif report.overall_risk_level == SeverityLevel.MEDIUM:
            prefix = "⚠️ 警告"
        else:
            prefix = "ℹ️ 通知"

        message = f"{prefix}: 上下文 '{report.context_id}' 检测到问题\n"
        message += f"健康度: {report.health_score:.2f}, 检测到 {len(report.signals)} 个信号"

        if report.explosion_risk and report.explosion_risk.is_critical:
            message += f"\n- 爆炸风险: 大小={report.explosion_risk.current_size}, 增长率={report.explosion_risk.growth_rate:.1%}"

        if report.corruption_risk and report.corruption_risk.is_critical:
            message += f"\n- 腐化风险: 清晰度={report.corruption_risk.clarity_score:.2f}"

        return message

    def get_active_alerts(self) -> List[Alert]:
        """获取活跃告警（未解决）"""
        return [a for a in self.alerts if not a.resolved]

    def get_critical_alerts(self) -> List[Alert]:
        """获取严重告警"""
        return [
            a for a in self.alerts
            if a.severity in [SeverityLevel.HIGH, SeverityLevel.CRITICAL]
            and not a.resolved
        ]

    def acknowledge_alert(self, alert_id: str):
        """确认告警"""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.acknowledged = True
                break

    def resolve_alert(self, alert_id: str):
        """解决告警"""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.resolved = True
                break

    def _init_rules(self) -> Dict:
        """初始化告警规则"""
        return {
            'explosion_threshold': 30000,  # 超过3万token告警
            'growth_rate_threshold': 0.3,  # 增长率超过30%告警
            'quality_decline_threshold': 0.15,  # 质量下降超过15%告警
            'redundancy_threshold': 0.35,  # 冗余超过35%告警
        }

    def check_rules(self, report: DegradationReport) -> bool:
        """检查告警规则"""
        rules = self.alert_rules

        # 规则1: 上下文大小
        if report.explosion_risk:
            if report.explosion_risk.current_size > rules['explosion_threshold']:
                return True

        # 规则2: 增长率
        if report.explosion_risk:
            if report.explosion_risk.growth_rate > rules['growth_rate_threshold']:
                return True

        # 规则3: 质量下降
        if report.corruption_risk:
            if report.corruption_risk.quality_decline_rate > rules['quality_decline_threshold']:
                return True

        # 规则4: 冗余
        if report.explosion_risk:
            if report.explosion_risk.redundancy_ratio > rules['redundancy_threshold']:
                return True

        return False
