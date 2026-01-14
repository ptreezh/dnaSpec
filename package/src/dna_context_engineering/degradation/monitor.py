"""
上下文监控器 - 持续监控上下文质量
"""
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import deque

from .detector import DegradationDetector
from .metrics import DegradationReport, SeverityLevel


class ContextMonitor:
    """上下文监控器"""

    def __init__(self, history_size: int = 100):
        self.detector = DegradationDetector()
        self.history_size = history_size
        self.contexts = {}  # context_id -> ContextState

    def monitor_context(
        self,
        context_id: str,
        context_content: str
    ) -> DegradationReport:
        """
        监控上下文

        Args:
            context_id: 上下文标识符
            context_content: 上下文内容

        Returns:
            DegradationReport: 检测报告
        """
        # 获取或创建上下文状态
        if context_id not in self.contexts:
            self.contexts[context_id] = ContextState(
                context_id=context_id,
                history_size=self.history_size
            )

        state = self.contexts[context_id]

        # 获取上次指标
        previous_metrics = state.get_latest_metrics()

        # 执行检测
        report = self.detector.detect_degradation(
            context_id=context_id,
            context_content=context_content,
            previous_metrics=previous_metrics
        )

        # 更新状态
        state.add_report(report)

        # 检查是否需要触发告警
        if report.needs_attention:
            self._trigger_alert(context_id, report)

        return report

    def get_context_health(self, context_id: str) -> Optional[Dict]:
        """获取上下文健康状态"""
        if context_id not in self.contexts:
            return None

        state = self.contexts[context_id]
        latest = state.get_latest_report()

        if not latest:
            return None

        return {
            'context_id': context_id,
            'health_score': latest.health_score,
            'risk_level': latest.overall_risk_level.value,
            'signal_count': len(latest.signals),
            'last_checked': latest.scanned_at.isoformat()
        }

    def get_all_contexts_health(self) -> Dict[str, Dict]:
        """获取所有上下文健康状态"""
        return {
            ctx_id: self.get_context_health(ctx_id)
            for ctx_id in self.contexts.keys()
        }

    def get_health_trend(self, context_id: str, window: int = 10) -> Dict:
        """获取健康度趋势"""
        if context_id not in self.contexts:
            return {'trend': 'unknown', 'data': []}

        state = self.contexts[context_id]
        reports = state.get_recent_reports(window)

        if len(reports) < 2:
            return {'trend': 'insufficient_data', 'data': []}

        scores = [r.health_score for r in reports]
        timestamps = [r.scanned_at for r in reports]

        # 计算趋势
        recent = scores[-3:] if len(scores) >= 3 else scores
        if all(recent[i] <= recent[i+1] for i in range(len(recent)-1)):
            trend = 'declining'  # 健康度下降（坏趋势）
        elif all(recent[i] >= recent[i+1] for i in range(len(recent)-1)):
            trend = 'improving'  # 健康度提升（好趋势）
        else:
            trend = 'stable'

        return {
            'trend': trend,
            'current_score': scores[-1],
            'average_score': sum(scores) / len(scores),
            'data': [
                {
                    'timestamp': ts.isoformat(),
                    'score': score
                }
                for ts, score in zip(timestamps, scores)
            ]
        }

    def _trigger_alert(self, context_id: str, report: DegradationReport):
        """触发告警"""
        severity = report.overall_risk_level.value

        print(f"\n{'🚨' if report.requires_immediate_action else '⚠️'} "
              f"上下文告警 [{severity.upper()}]: {context_id}")
        print(f"  健康度: {report.health_score:.2f}")
        print(f"  信号数: {len(report.signals)}")

        if report.signals:
            print("  检测到的问题:")
            for signal in report.signals[:3]:  # 只显示前3个
                print(f"    - {signal.description}")

        if report.recommended_actions:
            print("  建议行动:")
            for action in report.recommended_actions[:3]:
                print(f"    {action}")

    def save_monitoring_state(self, output_file: Path):
        """保存监控状态"""
        state_data = {}

        for ctx_id, ctx_state in self.contexts.items():
            reports_data = []
            for report in ctx_state.report_history:
                reports_data.append({
                    'context_id': report.context_id,
                    'scanned_at': report.scanned_at.isoformat(),
                    'health_score': report.health_score,
                    'risk_level': report.overall_risk_level.value,
                    'signal_count': len(report.signals)
                })

            state_data[ctx_id] = {
                'context_id': ctx_id,
                'reports': reports_data[-10:]  # 只保存最近10条
            }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f, indent=2, ensure_ascii=False)

        print(f"✅ 监控状态已保存: {output_file}")


class ContextState:
    """上下文状态"""

    def __init__(self, context_id: str, history_size: int = 100):
        self.context_id = context_id
        self.report_history = deque(maxlen=history_size)
        self.metrics_history = deque(maxlen=history_size)

    def add_report(self, report: DegradationReport):
        """添加报告"""
        self.report_history.append(report)

        # 保存指标用于下次比较
        self.metrics_history.append({
            'size': report.explosion_risk.current_size if report.explosion_risk else 0,
            'quality_score': (
                (report.corruption_risk.clarity_score + report.corruption_risk.consistency_score) / 2
                if report.corruption_risk else 0.8
            )
        })

    def get_latest_report(self) -> Optional[DegradationReport]:
        """获取最新报告"""
        return self.report_history[-1] if self.report_history else None

    def get_latest_metrics(self) -> Optional[Dict]:
        """获取最新指标"""
        return self.metrics_history[-1] if self.metrics_history else None

    def get_recent_reports(self, count: int = 10) -> List[DegradationReport]:
        """获取最近的报告"""
        reports = list(self.report_history)
        return reports[-count:] if len(reports) >= count else reports
