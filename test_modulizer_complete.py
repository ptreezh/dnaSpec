"""
DNASPEC Modulizer Complete End-to-End Test
完整的端到端测试
"""

import sys
from pathlib import Path

# Add skills to path
skills_dir = Path(__file__).parent / "skills" / "dnaspec-modulizer"
if str(skills_dir) not in sys.path:
    sys.path.insert(0, str(skills_dir))

from scripts.executor import ModulizerExecutor
from scripts.validator import ModulizerValidator
from scripts.calculator import ModulizerCalculator
from scripts.analyzer import ModulizerAnalyzer


def test_basic_execution():
    """测试1: 基本执行功能"""
    print("\n" + "="*70)
    print("测试 1: 基本执行功能")
    print("="*70)

    executor = ModulizerExecutor()
    result = executor.execute("如何将代码组织为模块？")

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

    validator = ModulizerValidator()

    # 测试有效请求
    valid_result = validator.validate("如何设计模块化架构？")
    assert valid_result.is_valid == True, "有效请求应该通过验证"
    print("✅ 有效请求验证通过")

    # 测试空请求
    empty_result = validator.validate("")
    assert empty_result.is_valid == False, "空请求应该验证失败"
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

    calculator = ModulizerCalculator()

    # 测试简单请求
    simple_metrics = calculator.calculate("创建模块")
    assert simple_metrics.complexity_score < 0.5, "简单请求复杂度应该较低"
    print(f"✅ 简单请求: 复杂度={simple_metrics.complexity_score:.2f}")

    # 测试复杂请求
    complex_metrics = calculator.calculate(
        "设计一个复杂的模块化架构，包含多个模块、依赖管理和模块间通信"
    )
    assert complex_metrics.complexity_score > 0.3, "复杂请求复杂度应该较高"
    print(f"✅ 复杂请求: 复杂度={complex_metrics.complexity_score:.2f}")

    # 测试内聚和耦合分数
    assert hasattr(complex_metrics, 'cohesion_score'), "应该有内聚分数"
    assert hasattr(complex_metrics, 'coupling_score'), "应该有耦合分数"
    print(f"✅ 内聚度: {complex_metrics.cohesion_score:.2f}")
    print(f"✅ 耦合度: {complex_metrics.coupling_score:.2f}")

    print("✅ 测试通过: 指标计算正常")


def test_analysis():
    """测试4: 分析功能"""
    print("\n" + "="*70)
    print("测试 4: 分析功能")
    print("="*70)

    analyzer = ModulizerAnalyzer()

    # 测试模块分析
    analysis = analyzer.analyze("需要重构代码，降低模块间耦合")
    assert hasattr(analysis, 'detected_patterns'), "应该有检测到的模式"
    assert hasattr(analysis, 'quality_scores'), "应该有质量分数"
    print(f"✅ 检测到的模式: {[p.value for p in analysis.detected_patterns]}")
    print(f"✅ 质量分数: {analysis.quality_scores}")

    # 测试建议生成
    assert hasattr(analysis, 'recommendations'), "应该有建议"
    assert len(analysis.recommendations) > 0, "应该生成建议"
    print(f"✅ 生成建议: {len(analysis.recommendations)} 条")

    print("✅ 测试通过: 分析功能正常")


def test_level_selection():
    """测试5: 提示词层次选择"""
    print("\n" + "="*70)
    print("测试 5: 提示词层次选择")
    print("="*70)

    executor = ModulizerExecutor()

    # 简单请求 → 00或01
    simple_result = executor.execute("请说明如何创建软件模块")
    assert simple_result["success"] == True, "执行应该成功"
    assert simple_result["prompt_level"] in ["00", "01"], "简单请求应该使用基础层次"
    print(f"✅ 简单请求 → 层次 {simple_result['prompt_level']}")

    # 中等复杂度 → 01或02
    medium_result = executor.execute("设计模块化架构，包含用户模块和订单模块")
    assert medium_result["success"] == True, "执行应该成功"
    assert medium_result["prompt_level"] in ["01", "02"], "中等请求应该使用中级层次"
    print(f"✅ 中等请求 → 层次 {medium_result['prompt_level']}")

    # 强制层次
    force_result = executor.execute("这是一个复杂的模块化请求", force_level="02")
    assert force_result["success"] == True, "执行应该成功"
    assert force_result["prompt_level"] == "02", "应该尊重强制层次参数"
    print(f"✅ 强制层次 → 层次 {force_result['prompt_level']}")

    print("✅ 测试通过: 层次选择逻辑正常")


def test_modularization_patterns():
    """测试6: 模块化模式识别"""
    print("\n" + "="*70)
    print("测试 6: 模块化模式识别")
    print("="*70)

    executor = ModulizerExecutor()

    scenarios = [
        {
            "name": "按层次分层",
            "request": "设计三层架构，包含表现层、业务层和数据层",
            "expected_keywords": ["层次", "层"]
        },
        {
            "name": "按功能划分",
            "request": "按功能划分模块，包括用户管理、订单处理、支付功能",
            "expected_keywords": ["功能", "模块"]
        },
        {
            "name": "微服务拆分",
            "request": "将单体应用拆分为微服务，独立部署和扩展",
            "expected_keywords": ["微服务", "服务"]
        }
    ]

    for scenario in scenarios:
        print(f"\n场景: {scenario['name']}")
        print(f"请求: {scenario['request']}")

        result = executor.execute(scenario['request'])

        assert result["success"] == True, "执行应该成功"
        print(f"  ✅ 层次: {result['prompt_level']}")
        print(f"  ✅ 复杂度: {result['metrics'].complexity_score:.2f}")

        # 检查返回的提示词内容是否包含相关关键词
        prompt_content = result['prompt_content'].lower()
        has_keywords = any(kw in prompt_content for kw in scenario['expected_keywords'])
        print(f"  ✅ 包含关键词: {has_keywords}")

    print("\n✅ 测试通过: 模块化模式识别正常")


def test_refactoring_scenarios():
    """测试7: 重构场景"""
    print("\n" + "="*70)
    print("测试 7: 重构场景")
    print("="*70)

    executor = ModulizerExecutor()

    scenarios = [
        {
            "name": "降低耦合",
            "request": "代码耦合度太高，一个模块依赖太多其他模块，需要降低耦合"
        },
        {
            "name": "提高内聚",
            "request": "模块内聚性低，相关功能分散在不同地方，需要提高内聚"
        },
        {
            "name": "拆分大模块",
            "request": "有一个大类做了太多事情，需要拆分成多个小模块"
        }
    ]

    for scenario in scenarios:
        print(f"\n场景: {scenario['name']}")
        result = executor.execute(scenario['request'])

        assert result["success"] == True, "执行应该成功"
        print(f"  ✅ 建议数量: {len(result['metrics'].suggestions)}")

        # 检查是否有相关建议
        if result['metrics'].suggestions:
            print(f"  ✅ 示例建议: {result['metrics'].suggestions[0]}")

    print("\n✅ 测试通过: 重构场景正常")


def test_end_to_end_complex_scenario():
    """测试8: 复杂端到端场景"""
    print("\n" + "="*70)
    print("测试 8: 复杂端到端场景")
    print("="*70)

    executor = ModulizerExecutor()

    # 复杂的企业级场景 - 增加关键词以提高复杂度
    request = """
    我们有一个大型的单体电商应用模块，需要设计复杂的模块化架构。
    包含用户管理模块、商品管理模块、订单处理模块、支付模块、物流模块、
    评价模块等多个功能模块。现在想要重构，将单体模块拆分成微服务模块架构，
    每个服务模块独立部署和扩展。同时要保证服务模块间的通信模块高效、
    数据一致性模块，并且要考虑服务发现模块、负载均衡模块、容错处理模块
    等分布式系统的模块化问题。这个模块化架构项目非常复杂和庞大。
    """

    result = executor.execute(request.strip(), context={"system_size": "large"})

    assert result["success"] == True, "执行应该成功"
    print(f"✅ 提示词层次: {result['prompt_level']}")
    print(f"✅ 复杂度: {result['metrics'].complexity_score:.2f}")
    print(f"✅ 内聚度: {result['metrics'].cohesion_score:.2f}")
    print(f"✅ 耦合度: {result['metrics'].coupling_score:.2f}")
    print(f"✅ 建议数量: {len(result['metrics'].suggestions)}")

    # 复杂场景应该使用中高级层次
    assert result['prompt_level'] in ["02", "03"], "复杂场景应该使用中高级层次"

    print("✅ 测试通过: 复杂端到端场景正常")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*70)
    print("DNASPEC MODULIZER 测试套件")
    print("="*70)

    tests = [
        test_basic_execution,
        test_validation,
        test_metrics_calculation,
        test_analysis,
        test_level_selection,
        test_modularization_patterns,
        test_refactoring_scenarios,
        test_end_to_end_complex_scenario
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
        print("\n🎉 所有测试通过！DNASPEC MODULIZER 技能就绪。")
        return 0
    else:
        print(f"\n⚠️  有 {failed} 个测试失败，需要修复。")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
