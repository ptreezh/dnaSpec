"""
DNASPEC Constraint Generator End-to-End Test
完整的端到端测试
"""

import sys
from pathlib import Path

# Add skills to path
skills_dir = Path(__file__).parent / "skills" / "dnaspec-constraint-generator"
if str(skills_dir) not in sys.path:
    sys.path.insert(0, str(skills_dir))

from scripts.executor import ConstraintExecutor
from scripts.validator import ConstraintValidator
from scripts.calculator import ConstraintCalculator
from scripts.analyzer import ConstraintAnalyzer


def test_basic_execution():
    """测试1: 基本执行功能"""
    print("\n" + "="*70)
    print("测试 1: 基本执行功能")
    print("="*70)

    executor = ConstraintExecutor()
    result = executor.execute("生成API性能约束，响应时间小于100ms")

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

    validator = ConstraintValidator()

    # 测试有效请求
    valid_result = validator.validate("生成API性能约束，响应时间小于100ms")
    assert valid_result.is_valid == True, "有效请求应该通过验证"
    print("✅ 有效请求验证通过")

    # 测试空请求
    empty_result = validator.validate("")
    assert empty_result.is_valid == False, "空请求应该验证失败"
    assert any(issue.severity.value == "critical" for issue in empty_result.issues), \
        "空请求应该有critical级别问题"
    print("✅ 空请求验证正确拒绝")

    # 测试太短的请求
    short_result = validator.validate("测试")
    assert short_result.is_valid == False, "太短的请求应该验证失败"
    print("✅ 短请求验证正确拒绝")

    print("✅ 测试通过: 验证功能正常")


def test_metrics_calculation():
    """测试3: 指标计算"""
    print("\n" + "="*70)
    print("测试 3: 指标计算")
    print("="*70)

    calculator = ConstraintCalculator()

    # 测试性能约束
    perf_metrics = calculator.calculate("API响应时间小于100ms，支持1000 QPS")
    assert perf_metrics.has_performance_constraint == True, "应该检测到性能约束"
    assert perf_metrics.specificity_score > 0.5, "具体性分数应该较高（有数字和单位）"
    print(f"✅ 性能约束: 复杂度={perf_metrics.complexity_score:.2f}, 具体性={perf_metrics.specificity_score:.2f}")

    # 测试安全约束
    sec_metrics = calculator.calculate("系统需要高安全性，使用加密和认证")
    assert sec_metrics.has_security_constraint == True, "应该检测到安全约束"
    print(f"✅ 安全约束: 复杂度={sec_metrics.complexity_score:.2f}")

    # 测试多约束类型
    multi_metrics = calculator.calculate("系统需要高性能和高安全性，支持认证和加密")
    type_count = sum([
        multi_metrics.has_performance_constraint,
        multi_metrics.has_security_constraint,
        multi_metrics.has_functional_constraint,
        multi_metrics.has_technical_constraint
    ])
    assert type_count >= 2, "应该检测到多种约束类型"
    print(f"✅ 多约束类型: {type_count} 种")

    print("✅ 测试通过: 指标计算正常")


def test_analysis():
    """测试4: 分析功能"""
    print("\n" + "="*70)
    print("测试 4: 分析功能")
    print("="*70)

    analyzer = ConstraintAnalyzer()

    # 测试约束类型检测
    analysis = analyzer.analyze("系统需要高性能和高安全性")
    detected_types = [t.value for t in analysis.detected_types]
    assert "performance" in detected_types, "应该检测到性能类型"
    assert "security" in detected_types, "应该检测到安全类型"
    print(f"✅ 检测到的类型: {detected_types}")

    # 测试质量分数
    assert "clarity" in analysis.quality_scores, "应该有清晰度分数"
    assert "completeness" in analysis.quality_scores, "应该有完整性分数"
    assert "verifiability" in analysis.quality_scores, "应该有可验证性分数"
    print(f"✅ 质量分数: {analysis.quality_scores}")

    # 测试冲突检测
    conflict_analysis = analyzer.analyze("系统要快但也要非常安全")
    assert len(conflict_analysis.potential_conflicts) > 0, "应该检测到性能与安全的潜在冲突"
    print(f"✅ 检测到冲突: {conflict_analysis.potential_conflicts}")

    # 测试建议生成
    assert len(analysis.recommendations) > 0, "应该生成建议"
    print(f"✅ 生成建议: {len(analysis.recommendations)} 条")

    print("✅ 测试通过: 分析功能正常")


def test_level_selection():
    """测试5: 提示词层次选择"""
    print("\n" + "="*70)
    print("测试 5: 提示词层次选择")
    print("="*70)

    executor = ConstraintExecutor()

    # 简单请求 → 00或01
    simple_result = executor.execute("生成API性能约束条件")
    assert simple_result["success"] == True, "执行应该成功"
    assert simple_result["prompt_level"] in ["00", "01"], "简单请求应该使用基础层次"
    print(f"✅ 简单请求 → 层次 {simple_result['prompt_level']}")

    # 中等复杂度 → 01或02
    medium_result = executor.execute("生成API性能和安全约束，需要认证和加密")
    assert medium_result["success"] == True, "执行应该成功"
    assert medium_result["prompt_level"] in ["01", "02"], "中等请求应该使用中级层次"
    print(f"✅ 中等请求 → 层次 {medium_result['prompt_level']}")

    # 有冲突 → 03
    conflict_result = executor.execute("系统要快但也要完全安全，低成本但高质量")
    assert conflict_result["success"] == True, "执行应该成功"
    assert conflict_result["prompt_level"] == "03", "有冲突的请求应该使用高级层次"
    print(f"✅ 冲突请求 → 层次 {conflict_result['prompt_level']}")

    # 强制层次
    force_result = executor.execute("这是一个复杂的请求内容", force_level="01")
    assert force_result["success"] == True, "执行应该成功"
    assert force_result["prompt_level"] == "01", "应该尊重强制层次参数"
    print(f"✅ 强制层次 → 层次 {force_result['prompt_level']}")

    print("✅ 测试通过: 层次选择逻辑正常")


def test_end_to_end_scenarios():
    """测试6: 端到端场景"""
    print("\n" + "="*70)
    print("测试 6: 端到端场景")
    print("="*70)

    executor = ConstraintExecutor()

    scenarios = [
        {
            "name": "简单性能约束",
            "request": "API响应时间要小于100ms",
            "expected_level": ["00", "01"]
        },
        {
            "name": "复杂多约束",
            "request": "系统需要高性能（P95<200ms）、高安全性（加密+认证）、高可用性（99.99%），支持10000 QPS",
            "expected_level": ["02", "03"]
        },
        {
            "name": "有冲突的约束",
            "request": "低成本但高质量，快速上线但功能完整",
            "expected_level": ["03"]
        }
    ]

    for scenario in scenarios:
        print(f"\n场景: {scenario['name']}")
        print(f"请求: {scenario['request']}")

        result = executor.execute(scenario['request'])

        assert result["success"] == True, "执行应该成功"
        assert result["prompt_level"] in scenario["expected_level"], \
            f"层次 {result['prompt_level']} 应该在 {scenario['expected_level']} 中"

        print(f"  ✅ 层次: {result['prompt_level']}")
        print(f"  ✅ 复杂度: {result['metrics'].complexity_score:.2f}")
        print(f"  ✅ 约束类型: {len(result['analysis'].detected_types)} 种")
        print(f"  ✅ 建议: {len(result['recommendations'])} 条")

    print("\n✅ 测试通过: 端到端场景正常")


def test_recommendations():
    """测试7: 建议生成"""
    print("\n" + "="*70)
    print("测试 7: 建议生成")
    print("="*70)

    executor = ConstraintExecutor()

    # 低具体性 → 应该有SMART建议
    low_specificity = executor.execute("系统性能要好，响应速度快")
    assert low_specificity["success"] == True, "执行应该成功"
    assert any("SMART" in rec or "具体" in rec for rec in low_specificity["recommendations"]), \
        "低具体性应该建议使用SMART原则"
    print("✅ 低具体性生成SMART建议")

    # 有冲突 → 应该有冲突处理建议
    has_conflicts = executor.execute("系统要快速但也要非常安全，需要权衡")
    assert has_conflicts["success"] == True, "执行应该成功"
    assert any("冲突" in rec or "优先级" in rec for rec in has_conflicts["recommendations"]), \
        "有冲突应该建议优先级排序"
    print("✅ 冲突生成处理建议")

    # 高复杂度 → 应该有分阶段建议
    high_complexity = executor.execute(
        "这是一个极其复杂的企业级分布式系统，"
        "包含高性能要求（支持10万并发）、"
        "高安全性要求（满足SOC2和GDPR合规）、"
        "高可用性要求（99.999%）、"
        "复杂的功能要求（支持多种业务场景和工作流）、"
        "复杂的技术栈（微服务架构、多语言、多数据库）、"
        "以及严格的业务规则和技术限制，"
        "需要满足多个合规性要求，"
        "同时要考虑成本约束和交付时间限制",
        context={"project_size": "enterprise", "team_size": 100}
    )
    assert high_complexity["success"] == True, "执行应该成功"
    assert any("阶段" in rec or "分步" in rec for rec in high_complexity["recommendations"]), \
        "高复杂度应该建议分阶段处理"
    print("✅ 高复杂度生成分阶段建议")

    print("✅ 测试通过: 建议生成正常")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*70)
    print("DNASPEC CONSTRAINT GENERATOR 测试套件")
    print("="*70)

    tests = [
        test_basic_execution,
        test_validation,
        test_metrics_calculation,
        test_analysis,
        test_level_selection,
        test_end_to_end_scenarios,
        test_recommendations
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

    # 总结
    print("\n" + "="*70)
    print("测试总结")
    print("="*70)
    print(f"总计: {len(tests)} 个测试")
    print(f"✅ 通过: {passed}")
    print(f"❌ 失败: {failed}")

    if failed == 0:
        print("\n🎉 所有测试通过！DNASPEC CONSTRAINT GENERATOR 技能就绪。")
        return 0
    else:
        print(f"\n⚠️  有 {failed} 个测试失败，需要修复。")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
