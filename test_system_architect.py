"""
DNASPEC System Architect End-to-End Test
完整的端到端测试
"""

import sys
from pathlib import Path

skills_dir = Path(__file__).parent / "skills" / "dnaspec-system-architect"
if str(skills_dir) not in sys.path:
    sys.path.insert(0, str(skills_dir))

from scripts.executor import SystemArchitectExecutor
from scripts.validator import SystemArchitectValidator
from scripts.calculator import ArchitectureCalculator
from scripts.analyzer import ArchitectureAnalyzer


def test_basic_execution():
    """测试1: 基本执行功能"""
    print("\n" + "="*70)
    print("测试 1: 基本执行功能")
    print("="*70)

    executor = SystemArchitectExecutor()
    result = executor.execute("请设计一个Web应用架构")

    assert result["success"] == True, "执行应该成功"
    assert "prompt_level" in result, "结果应包含提示词层次"
    assert "prompt_content" in result, "结果应包含提示词内容"

    print(f"✅ 提示词层次: {result['prompt_level']}")
    print(f"✅ 提示词长度: {len(result['prompt_content'])} 字符")
    print("✅ 测试通过: 基本执行功能正常")


def test_validation():
    """测试2: 验证功能"""
    print("\n" + "="*70)
    print("测试 2: 验证功能")
    print("="*70)

    validator = SystemArchitectValidator()

    # 测试有效请求
    valid_result = validator.validate("设计一个微服务架构，包含用户服务和订单服务")
    assert valid_result.is_valid == True, "有效请求应该通过验证"
    print("✅ 有效请求验证通过")

    # 测试空请求
    empty_result = validator.validate("")
    assert empty_result.is_valid == False, "空请求应该验证失败"
    print("✅ 空请求验证正确拒绝")

    print("✅ 测试通过: 验证功能正常")


def test_metrics_calculation():
    """测试3: 指标计算"""
    print("\n" + "="*70)
    print("测试 3: 指标计算")
    print("="*70)

    calculator = ArchitectureCalculator()

    # 测试单体架构
    monolith_metrics = calculator.calculate("设计一个单体Web应用架构")
    assert monolith_metrics.has_monolith_arch == True, "应该检测到单体架构"
    print(f"✅ 单体架构: 复杂度={monolith_metrics.complexity_score:.2f}")

    # 测试微服务架构
    microservice_metrics = calculator.calculate("设计一个微服务架构，包含多个服务")
    assert microservice_metrics.has_microservice_arch == True, "应该检测到微服务架构"
    print(f"✅ 微服务架构: 复杂度={microservice_metrics.complexity_score:.2f}")

    print("✅ 测试通过: 指标计算正常")


def test_analysis():
    """测试4: 分析功能"""
    print("\n" + "="*70)
    print("测试 4: 分析功能")
    print("="*70)

    analyzer = ArchitectureAnalyzer()

    # 测试架构分析
    analysis = analyzer.analyze("设计一个分布式微服务架构")
    assert hasattr(analysis, 'detected_types'), "应该有检测到的类型"
    assert hasattr(analysis, 'architecture_style'), "应该有架构风格"
    print(f"✅ 架构风格: {analysis.architecture_style}")
    print(f"✅ 质量分数: {analysis.quality_scores}")

    print("✅ 测试通过: 分析功能正常")


def test_level_selection():
    """测试5: 提示词层次选择"""
    print("\n" + "="*70)
    print("测试 5: 提示词层次选择")
    print("="*70)

    executor = SystemArchitectExecutor()

    # 简单请求
    simple_result = executor.execute("请设计Web应用架构")
    assert simple_result["success"] == True, "执行应该成功"
    print(f"✅ 简单请求 → 层次 {simple_result['prompt_level']}")

    # 复杂请求
    complex_result = executor.execute(
        "设计一个企业级微服务架构，包含服务发现、配置管理、熔断降级等组件"
    )
    assert complex_result["success"] == True, "执行应该成功"
    print(f"✅ 复杂请求 → 层次 {complex_result['prompt_level']}")

    print("✅ 测试通过: 层次选择正常")


def test_architecture_patterns():
    """测试6: 架构模式识别"""
    print("\n" + "="*70)
    print("测试 6: 架构模式识别")
    print("="*70)

    executor = SystemArchitectExecutor()

    patterns = [
        ("单体架构", "设计一个单体应用架构"),
        ("微服务架构", "设计微服务架构，拆分服务"),
        ("无服务器架构", "请设计无服务器架构方案")
    ]

    for name, request in patterns:
        result = executor.execute(request)
        assert result["success"] == True
        print(f"✅ {name}: 层次 {result['prompt_level']}")

    print("✅ 测试通过: 架构模式识别正常")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*70)
    print("DNASPEC SYSTEM ARCHITECT 测试套件")
    print("="*70)

    tests = [
        test_basic_execution,
        test_validation,
        test_metrics_calculation,
        test_analysis,
        test_level_selection,
        test_architecture_patterns
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            failed += 1
            print(f"\n❌ 测试失败: {test.__name__}")
            print(f"   错误: {e}")
        except Exception as e:
            failed += 1
            print(f"\n❌ 测试错误: {test.__name__}")
            print(f"   异常: {e}")

    print("\n" + "="*70)
    print("测试总结")
    print("="*70)
    print(f"总计: {len(tests)} 个测试")
    print(f"✅ 通过: {passed}")
    print(f"❌ 失败: {failed}")

    if failed == 0:
        print("\n🎉 所有测试通过！DNASPEC SYSTEM ARCHITECT 技能就绪。")
        return 0
    else:
        print(f"\n⚠️  有 {failed} 个测试失败，需要修复。")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
