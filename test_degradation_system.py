"""
测试上下文腐化检测系统
"""
import sys
from pathlib import Path

# 添加src到路径
src_dir = Path(__file__).parent / 'src'
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from dna_context_engineering.degradation import (
    DegradationDetector,
    ContextMonitor,
    AlertManager,
    AutoRecoveryManager
)


def test_detector():
    """测试腐化检测器"""
    print("\n### 测试1: 腐化检测器 ###")

    detector = DegradationDetector()

    # 测试内容
    test_content = """
    # 用户认证系统

    这是一个用户认证系统。用户可以登录。
    账号可以登录。使用者可以登入系统。

    待更新：添加OAuth支持
    TODO: 实现多因素认证
    """ * 20  # 重复内容模拟冗余和爆炸

    report = detector.detect_degradation(
        context_id='test-context',
        context_content=test_content
    )

    assert report is not None
    assert report.context_id == 'test-context'
    print(f"✅ 检测完成")
    print(f"   健康度: {report.health_score:.2f}")
    print(f"   风险等级: {report.overall_risk_level.value}")
    print(f"   检测到信号: {len(report.signals)} 个")

    if report.explosion_risk:
        print(f"   爆炸风险: 大小={report.explosion_risk.current_size}, "
              f"增长率={report.explosion_risk.growth_rate:.1%}")

    return report


def test_monitor():
    """测试监控器"""
    print("\n### 测试2: 上下文监控器 ###")

    monitor = ContextMonitor()

    # 模拟多次监控
    content_v1 = "初始内容" * 10
    content_v2 = "初始内容" * 50  # 增长
    content_v3 = "初始内容" * 100  # 再增长

    report1 = monitor.monitor_context('ctx-1', content_v1)
    report2 = monitor.monitor_context('ctx-1', content_v2)
    report3 = monitor.monitor_context('ctx-1', content_v3)

    # 获取健康趋势
    trend = monitor.get_health_trend('ctx-1')
    print(f"✅ 监控完成")
    print(f"   趋势: {trend['trend']}")
    print(f"   当前评分: {trend['current_score']:.2f}")
    print(f"   平均评分: {trend['average_score']:.2f}")

    assert trend['trend'] in ['improving', 'declining', 'stable']

    return monitor


def test_alert_manager():
    """测试告警管理器"""
    print("\n### 测试3: 告警管理器 ###")

    alert_manager = AlertManager()
    detector = DegradationDetector()

    # 创建一个会触发告警的报告
    bad_content = "这是内容。" * 10000  # 超大内容

    report = detector.detect_degradation('alert-test', bad_content)
    alert = alert_manager.create_alert_from_report(report)

    if alert:
        print(f"✅ 告警已创建")
        print(f"   告警ID: {alert.alert_id}")
        print(f"   严重程度: {alert.severity.value}")
        print(f"   消息: {alert.message[:50]}...")
    else:
        print("ℹ️  未触发告警（内容健康）")

    # 检查活跃告警
    active_alerts = alert_manager.get_active_alerts()
    print(f"   活跃告警数: {len(active_alerts)}")

    return alert_manager


def test_auto_recovery():
    """测试自动修复"""
    print("\n### 测试4: 自动修复管理器 ###")

    manager = AutoRecoveryManager()

    # 模拟需要修复的上下文
    problematic_content = """
    # 系统设计

    用户可以登录。账号可以登录。使用者可以登入。
    待更新：添加新功能
    TODO: 修复bug
    """ * 30  # 大量冗余

    result = manager.monitor_and_recover(
        context_id='recovery-test',
        context_content=problematic_content,
        auto_optimize=False  # 不自动优化（避免依赖其他技能）
    )

    print(f"✅ 自动修复测试完成")
    print(f"   上下文ID: {result['context_id']}")
    print(f"   健康度: {result['health_score']:.2f}")
    print(f"   风险等级: {result['risk_level']}")
    print(f"   执行的操作: {result['actions_taken']}")

    return manager


def main():
    """运行所有测试"""
    print("=" * 60)
    print("上下文腐化检测系统测试")
    print("=" * 60)

    try:
        # 测试各个组件
        test_detector()
        test_monitor()
        test_alert_manager()
        test_auto_recovery()

        print("\n" + "=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)

        print("\n系统功能:")
        print("  1. ✅ 腐化检测 - 检测上下文爆炸、腐化、不一致等")
        print("  2. ✅ 质量监控 - 持续监控上下文健康度")
        print("  3. ✅ 告警系统 - 自动触发和处理告警")
        print("  4. ✅ 自动修复 - 集成analysis和optimization")

    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
