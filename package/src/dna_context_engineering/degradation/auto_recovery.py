"""
自动修复流程 - 集成analysis和optimization
"""
import sys
from pathlib import Path
from typing import Optional, Dict, List

# 添加src到路径
src_dir = Path(__file__).parent.parent.parent.parent / 'src'
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from .detector import DegradationDetector
from .monitor import ContextMonitor
from .alert_system import AlertManager
from .metrics import DegradationReport, SeverityLevel


class AutoRecoveryManager:
    """自动修复管理器"""

    def __init__(self, dnaspec_root: Optional[Path] = None):
        if dnaspec_root is None:
            dnaspec_root = Path(__file__).parent.parent.parent.parent

        self.dnaspec_root = Path(dnaspec_root)
        self.monitor = ContextMonitor()
        self.alert_manager = AlertManager()
        self.detector = DegradationDetector()

    def monitor_and_recover(
        self,
        context_id: str,
        context_content: str,
        auto_optimize: bool = False
    ) -> Dict:
        """
        监控并自动修复

        Args:
            context_id: 上下文标识符
            context_content: 上下文内容
            auto_optimize: 是否自动优化

        Returns:
            Dict: 处理结果
        """
        result = {
            'context_id': context_id,
            'actions_taken': [],
            'alerts': [],
            'optimization_performed': False
        }

        # 1. 监控上下文
        print(f"\n{'='*60}")
        print(f"监控上下文: {context_id}")
        print(f"{'='*60}")

        report = self.monitor.monitor_context(context_id, context_content)

        result['health_score'] = report.health_score
        result['risk_level'] = report.overall_risk_level.value

        # 2. 创建告警（如果需要）
        alert = self.alert_manager.create_alert_from_report(report)
        if alert:
            result['alerts'].append({
                'alert_id': alert.alert_id,
                'severity': alert.severity.value,
                'message': alert.message
            })

        # 3. 决定是否需要自动修复
        if auto_optimize and report.requires_immediate_action:
            print(f"\n检测到严重问题，启动自动修复流程...")

            # 执行分析
            analysis_result = self._run_context_analysis(context_content)
            result['actions_taken'].append('context_analysis')
            result['analysis'] = analysis_result

            # 执行优化
            optimization_result = self._run_context_optimization(context_content, report)
            result['actions_taken'].append('context_optimization')
            result['optimization'] = optimization_result
            result['optimization_performed'] = True

        # 4. 保存监控状态
        state_file = self.dnaspec_root / 'reports' / 'monitoring_state.json'
        state_file.parent.mkdir(exist_ok=True)
        self.monitor.save_monitoring_state(state_file)

        return result

    def _run_context_analysis(self, context_content: str) -> Dict:
        """运行上下文分析"""
        print("\n[1/2] 运行上下文质量分析...")

        try:
            # 导入context-analysis技能
            from dna_context_engineering.skills_system_final import SkillExecutor

            executor = SkillExecutor()
            result = executor.execute_skill(
                skill_name='context-analysis',
                request='分析上下文质量，检测清晰度、完整性、一致性问题',
                context={'content': context_content[:1000]}  # 只传入前1000字符作为示例
            )

            return {
                'success': result.get('success', False),
                'analysis': result.get('analysis', {}),
                'recommendations': result.get('recommendations', [])
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _run_context_optimization(
        self,
        context_content: str,
        report: DegradationReport
    ) -> Dict:
        """运行上下文优化"""
        print("[2/2] 运行上下文优化...")

        # 根据检测报告确定优化策略
        optimization_type = self._determine_optimization_type(report)

        try:
            from dna_context_engineering.skills_system_final import SkillExecutor

            executor = SkillExecutor()
            result = executor.execute_skill(
                skill_name='context-optimization',
                request=f'优化上下文，执行{optimization_type}优化',
                context={
                    'content': context_content[:1000],
                    'issues': [s.description for s in report.signals[:3]]
                }
            )

            return {
                'success': result.get('success', False),
                'optimization_type': optimization_type,
                'result': result.get('result', {})
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _determine_optimization_type(self, report: DegradationReport) -> str:
        """确定优化类型"""
        if report.explosion_risk and report.explosion_risk.current_size > 30000:
            return '压缩'

        if any(s.signal_type.value == 'inconsistency' for s in report.signals):
            return '术语统一'

        if report.corruption_risk and report.corruption_risk.clarity_score < 0.6:
            return '清晰度提升'

        return '综合优化'

    def generate_recovery_report(self, results: List[Dict]) -> str:
        """生成修复报告"""
        lines = [
            "",
            "=" * 60,
            "上下文自动修复报告",
            "=" * 60,
            "",
        ]

        total_processed = len(results)
        critical_count = sum(1 for r in results if r.get('risk_level') in ['high', 'critical'])
        optimized_count = sum(1 for r in results if r.get('optimization_performed'))

        lines.append(f"处理上下文总数: {total_processed}")
        lines.append(f"发现严重问题: {critical_count}")
        lines.append(f"执行自动优化: {optimized_count}")
        lines.append("")

        # 详细报告
        for result in results:
            context_id = result['context_id']
            health = result['health_score']
            risk = result['risk_level']

            lines.append(f"上下文: {context_id}")
            lines.append(f"  健康度: {health:.2f}")
            lines.append(f"  风险等级: {risk}")

            if result.get('alerts'):
                lines.append(f"  告警: {len(result['alerts'])} 个")
                for alert in result['alerts']:
                    lines.append(f"    - {alert['message']}")

            if result.get('optimization_performed'):
                lines.append(f"  优化: 已执行")

            lines.append("")

        lines.append("=" * 60)

        return "\n".join(lines)


def demo_auto_recovery():
    """演示自动修复流程"""
    print("=" * 60)
    print("DNASPEC 上下文腐化检测与自动修复演示")
    print("=" * 60)

    manager = AutoRecoveryManager()

    # 模拟上下文内容
    test_context_1 = """
    # 用户认证系统

    这是一个用户认证系统。用户可以登录，也可以注册。
    账号可以登录，也可以注册。使用者可以登入系统。

    系统支持多种认证方式：
    - 用户名密码登录
    - 账号密码登录
    - 使用者名密码登入

    待更新：添加OAuth支持
    TODO: 实现多因素认证
    """ * 10  # 重复内容模拟冗余

    test_context_2 = """
    系统架构设计

    这个系统采用微服务架构。包括：
    - 用户服务
    - 订单服务
    - 支付服务

    所有服务通过REST API通信。
    所有服务通过HTTP接口通信。
    所有服务通过Web服务调用。

    系统保证99.99%可用性。
    系统保证高可用性。
    系统保证不宕机。
    """

    test_contexts = {
        'context-1': test_context_1,
        'context-2': test_context_2
    }

    results = []

    for context_id, content in test_contexts.items():
        result = manager.monitor_and_recover(
            context_id=context_id,
            context_content=content,
            auto_optimize=True
        )
        results.append(result)

    # 生成报告
    report = manager.generate_recovery_report(results)
    print(report)

    return results


if __name__ == '__main__':
    demo_auto_recovery()
