"""测试 dnaspec-context-analysis 技能"""
import sys
from pathlib import Path

skill_dir = Path(__file__).parent / 'skills' / 'dnaspec-context-analysis'
if str(skill_dir) not in sys.path:
    sys.path.insert(0, str(skill_dir))

import scripts.executor as executor_module
ContextAnalysisExecutor = executor_module.ContextAnalysisExecutor

def test_basic_execution():
    print("测试: test_basic_execution")
    executor = ContextAnalysisExecutor()
    result = executor.execute("请分析上下文的清晰度")

    assert result["success"] == True
    assert result["validation"].is_valid == True
    print(f"  ✅ Level: {result['prompt_level']}, Dimension: {result['analysis'].primary_dimension}")

def test_dimension_detection():
    print("\n测试: test_dimension_detection")
    executor = ContextAnalysisExecutor()

    test_cases = [
        ("清晰度", "请分析文档内容的清晰度"),
        ("完整性", "请检查需求信息的完整性"),
        ("一致性", "请验证术语使用的一致性"),
    ]

    for name, request in test_cases:
        result = executor.execute(request)
        assert result["success"] == True
        print(f"  ✅ {name}: {result['analysis'].primary_dimension}")

def test_analysis_type_detection():
    print("\n测试: test_analysis_type_detection")
    executor = ContextAnalysisExecutor()

    test_cases = [
        ("质量评估", "请评估上下文的整体质量"),
        ("爆炸风险", "请分析上下文爆炸风险"),
        ("腐化风险", "请检测上下文腐化风险"),
    ]

    for name, request in test_cases:
        result = executor.execute(request)
        assert result["success"] == True
        print(f"  ✅ {name}: Type={result['analysis'].analysis_type}")

def test_validation():
    print("\n测试: test_validation")
    executor = ContextAnalysisExecutor()

    result = executor.execute("")
    assert result["success"] == False
    print("  ✅ 空请求正确拒绝")

def test_force_level():
    print("\n测试: test_force_level")
    executor = ContextAnalysisExecutor()

    for level in ["00", "01", "02", "03"]:
        result = executor.execute("请全面分析上下文质量", force_level=level)
        assert result["success"] == True
        assert result["prompt_level"] == level
    print("  ✅ 所有强制级别测试通过")

if __name__ == "__main__":
    print("=" * 60)
    print("DNASPEC Context-Analysis 技能测试")
    print("=" * 60)

    try:
        test_basic_execution()
        test_dimension_detection()
        test_analysis_type_detection()
        test_validation()
        test_force_level()

        print("\n" + "=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
