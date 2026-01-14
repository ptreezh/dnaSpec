"""测试 dnaspec-context-optimization 技能"""
import sys
from pathlib import Path

skill_dir = Path(__file__).parent / 'skills' / 'dnaspec-context-optimization'
if str(skill_dir) not in sys.path:
    sys.path.insert(0, str(skill_dir))

import scripts.executor as executor_module
OptimizationExecutor = executor_module.OptimizationExecutor

def test_basic_execution():
    print("测试: test_basic_execution")
    executor = OptimizationExecutor()
    result = executor.execute("请优化上下文的清晰度")

    assert result["success"] == True
    assert result["validation"].is_valid == True
    print(f"  ✅ Level: {result['prompt_level']}, Optimization: {result['analysis'].primary_optimization}")

def test_optimization_type_detection():
    print("\n测试: test_optimization_type_detection")
    executor = OptimizationExecutor()

    test_cases = [
        ("压缩优化", "请压缩冗余的上下文内容"),
        ("结构化", "请重组上下文的结构化组织"),
        ("术语统一", "请统一文档中的术语使用"),
    ]

    for name, request in test_cases:
        result = executor.execute(request)
        assert result["success"] == True
        print(f"  ✅ {name}: {result['analysis'].primary_optimization}")

def test_validation():
    print("\n测试: test_validation")
    executor = OptimizationExecutor()

    result = executor.execute("")
    assert result["success"] == False
    print("  ✅ 空请求正确拒绝")

def test_force_level():
    print("\n测试: test_force_level")
    executor = OptimizationExecutor()

    for level in ["00", "01", "02", "03"]:
        result = executor.execute("请全面优化上下文质量", force_level=level)
        assert result["success"] == True
        assert result["prompt_level"] == level
    print("  ✅ 所有强制级别测试通过")

if __name__ == "__main__":
    print("=" * 60)
    print("DNASPEC Context-Optimization 技能测试")
    print("=" * 60)

    try:
        test_basic_execution()
        test_optimization_type_detection()
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
