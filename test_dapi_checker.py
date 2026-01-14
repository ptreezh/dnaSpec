"""测试 dnaspec-dapi-checker 技能"""
import sys
from pathlib import Path

# Add skills to path
skill_dir = Path(__file__).parent / 'skills' / 'dnaspec-dapi-checker'
if str(skill_dir) not in sys.path:
    sys.path.insert(0, str(skill_dir))

# Import from scripts package
import scripts.executor as executor_module
DAPICheckerExecutor = executor_module.DAPICheckerExecutor

def test_basic_execution():
    """测试基本执行功能"""
    print("测试: test_basic_execution")
    executor = DAPICheckerExecutor()
    result = executor.execute("请检查模块级接口一致性")

    assert result["success"] == True, f"执行失败: {result}"
    assert "validation" in result, "缺少 validation 字段"
    assert "metrics" in result, "缺少 metrics 字段"
    assert "analysis" in result, "缺少 analysis 字段"
    assert "prompt_level" in result, "缺少 prompt_level 字段"
    assert "prompt_content" in result, "缺少 prompt_content 字段"
    assert result["validation"].is_valid == True, "验证应该通过"
    assert len(result["prompt_content"]) > 0, "Prompt 内容不应为空"

    print(f"  ✅ Prompt Level: {result['prompt_level']}")
    print(f"  ✅ Token Count: {result['metrics'].token_count}")
    print(f"  ✅ Check Level: {result['analysis'].check_level}")

def test_check_level_detection():
    """测试检查级别检测"""
    print("\n测试: test_check_level_detection")
    executor = DAPICheckerExecutor()

    test_cases = [
        ("模块级", "请检查模块内部接口一致性"),
        ("子系统级", "请验证子系统间接口对齐"),
        ("系统级", "请审查系统级API规范")
    ]

    for name, request in test_cases:
        result = executor.execute(request)
        assert result["success"] == True, f"{name} 执行失败: {result}"
        assert result["validation"].is_valid == True, f"{name} 验证应该通过"
        print(f"  ✅ {name}: Level={result['prompt_level']}, Check={result['analysis'].check_level}")

def test_validation():
    """测试输入验证"""
    print("\n测试: test_validation")
    executor = DAPICheckerExecutor()

    # 测试空请求
    result = executor.execute("")
    assert result["success"] == False, "空请求应该失败"
    assert result["validation"].is_valid == False, "空请求验证应该失败"
    print("  ✅ 空请求正确拒绝")

    # 测试过短请求
    result = executor.execute("太短")
    assert result["success"] == False, "过短请求应该失败"
    assert result["validation"].is_valid == False, "过短请求验证应该失败"
    print("  ✅ 过短请求正确拒绝")

def test_force_level():
    """测试强制级别"""
    print("\n测试: test_force_level")
    executor = DAPICheckerExecutor()

    levels = ["00", "01", "02", "03"]
    for level in levels:
        result = executor.execute("请检查API接口规范", force_level=level)
        assert result["success"] == True, f"级别 {level} 执行失败"
        assert result["prompt_level"] == level, f"期望级别 {level}, 实际 {result['prompt_level']}"
        print(f"  ✅ 强制级别 {level}: 成功")

if __name__ == "__main__":
    print("=" * 60)
    print("DNASPEC DAPI-Checker 技能测试")
    print("=" * 60)

    try:
        test_basic_execution()
        test_check_level_detection()
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
