"""测试 dnaspec-workspace 技能"""
import sys
from pathlib import Path

# Add skills to path
skill_dir = Path(__file__).parent / 'skills' / 'dnaspec-workspace'
if str(skill_dir) not in sys.path:
    sys.path.insert(0, str(skill_dir))

# Import from scripts package
import scripts.executor as executor_module
WorkspaceExecutor = executor_module.WorkspaceExecutor

def test_basic_execution():
    """测试基本执行功能"""
    print("测试: test_basic_execution")
    executor = WorkspaceExecutor()
    result = executor.execute("请创建一个新的工作区")

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
    print(f"  ✅ Primary Operation: {result['analysis'].primary_operation}")

def test_operation_detection():
    """测试操作类型检测"""
    print("\n测试: test_operation_detection")
    executor = WorkspaceExecutor()

    test_cases = [
        ("创建操作", "请创建一个新的任务工作区"),
        ("清理操作", "请清理已完成的工作区"),
        ("状态查询", "请查询所有工作区的状态"),
        ("隔离检查", "请检查工作区上下文隔离情况"),
    ]

    for name, request in test_cases:
        result = executor.execute(request)
        assert result["success"] == True, f"{name} 执行失败: {result}"
        assert result["validation"].is_valid == True, f"{name} 验证应该通过"
        print(f"  ✅ {name}: Level={result['prompt_level']}, Op={result['analysis'].primary_operation}")

def test_workspace_type_detection():
    """测试工作区类型检测"""
    print("\n测试: test_workspace_type_detection")
    executor = WorkspaceExecutor()

    test_cases = [
        ("普通任务", "请创建一个普通任务工作区"),
        ("智能体工作区", "请为代码审查智能体创建工作区"),
        ("子任务工作区", "请为主任务创建子任务工作区"),
    ]

    for name, request in test_cases:
        result = executor.execute(request)
        assert result["success"] == True, f"{name} 执行失败: {result}"
        print(f"  ✅ {name}: Type={result['analysis'].workspace_type}")

def test_validation():
    """测试输入验证"""
    print("\n测试: test_validation")
    executor = WorkspaceExecutor()

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
    executor = WorkspaceExecutor()

    levels = ["00", "01", "02", "03"]
    for level in levels:
        result = executor.execute("请创建一个新的工作区", force_level=level)
        assert result["success"] == True, f"级别 {level} 执行失败: {result}"
        assert result["prompt_level"] == level, f"期望级别 {level}, 实际 {result['prompt_level']}"
        print(f"  ✅ 强制级别 {level}: 成功")

def test_agent_workspace_promotion():
    """测试智能体工作区级别提升"""
    print("\n测试: test_agent_workspace_promotion")
    executor = WorkspaceExecutor()

    # 智能体工作区应该提升级别
    result = executor.execute("请为代码审查智能体创建独立工作区")
    assert result["success"] == True, "执行失败"
    assert result["analysis"].workspace_type == "agent_workspace", "应该检测到智能体工作区"
    print(f"  ✅ 智能体工作区级别: {result['prompt_level']}")
    print(f"  ✅ 工作区类型: {result['analysis'].workspace_type}")

if __name__ == "__main__":
    print("=" * 60)
    print("DNASPEC Workspace 技能测试")
    print("=" * 60)

    try:
        test_basic_execution()
        test_operation_detection()
        test_workspace_type_detection()
        test_validation()
        test_force_level()
        test_agent_workspace_promotion()

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
