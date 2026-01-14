"""测试 dnaspec-cognitive-template 技能"""
import sys
from pathlib import Path

skill_dir = Path(__file__).parent / 'skills' / 'dnaspec-cognitive-template'
if str(skill_dir) not in sys.path:
    sys.path.insert(0, str(skill_dir))

import scripts.executor as executor_module
TemplateExecutor = executor_module.TemplateExecutor

def test_basic_execution():
    print("测试: test_basic_execution")
    executor = TemplateExecutor()
    result = executor.execute("请使用理解模板分析问题")

    assert result["success"] == True
    assert result["validation"].is_valid == True
    print(f"  ✅ Level: {result['prompt_level']}, Template: {result['analysis'].primary_template}")

def test_template_type_detection():
    print("\n测试: test_template_type_detection")
    executor = TemplateExecutor()

    test_cases = [
        ("理解模板", "请使用理解模板分析需求"),
        ("推理模板", "请应用推理模板推导结论"),
        ("验证模板", "请用验证模板检查质量"),
        ("设计模板", "请使用设计模板规划方案"),
    ]

    for name, request in test_cases:
        result = executor.execute(request)
        assert result["success"] == True
        print(f"  ✅ {name}: {result['analysis'].primary_template}")

def test_application_type_detection():
    print("\n测试: test_application_type_detection")
    executor = TemplateExecutor()

    test_cases = [
        ("模板应用", "请应用验证模板检查代码质量"),
        ("模板创建", "请创建新的问题解决模板"),
        ("模板组合", "请组合多个认知模板使用"),
    ]

    for name, request in test_cases:
        result = executor.execute(request)
        assert result["success"] == True
        print(f"  ✅ {name}: Type={result['analysis'].application_type}")

def test_validation():
    print("\n测试: test_validation")
    executor = TemplateExecutor()

    result = executor.execute("")
    assert result["success"] == False
    print("  ✅ 空请求正确拒绝")

def test_force_level():
    print("\n测试: test_force_level")
    executor = TemplateExecutor()

    for level in ["00", "01", "02", "03"]:
        result = executor.execute("请全面应用认知模板分析问题", force_level=level)
        assert result["success"] == True
        assert result["prompt_level"] == level
    print("  ✅ 所有强制级别测试通过")

if __name__ == "__main__":
    print("=" * 60)
    print("DNASPEC Cognitive-Template 技能测试")
    print("=" * 60)

    try:
        test_basic_execution()
        test_template_type_detection()
        test_application_type_detection()
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
