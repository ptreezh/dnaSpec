"""
测试技能协同集成
"""
import sys
from pathlib import Path

# 添加src到路径
src_dir = Path(__file__).parent / 'src'
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from dna_context_engineering.integration import (
    ContextImprovementCycle,
    AgentWorkspaceIntegrator,
    TaskWorkspaceIntegrator
)


def test_improvement_cycle():
    """测试改进循环"""
    print("\n### 测试1: 上下文改进循环 ###")

    cycle = ContextImprovementCycle()

    # 模拟一个需要改进的上下文
    poor_context = """
    用户系统

    用户可以登录。账号可以登录。使用者可以登入。
    系统支持注册。系统支持注册。系统支持注册。
    待更新功能。
    TODO: 修复bug。
    """ * 10

    result = cycle.improve_context(
        context_id='test-improvement',
        context_content=poor_context,
        max_cycles=2,
        quality_threshold=0.85
    )

    assert result is not None
    assert result.cycles_completed > 0
    print(f"✅ 改进循环测试通过")
    print(f"   循环次数: {result.cycles_completed}")
    print(f"   质量提升: {result.improvement_percentage:.1f}%")


def test_agent_workspace():
    """测试智能体工作区"""
    print("\n### 测试2: 智能体工作区集成 ###")

    integrator = AgentWorkspaceIntegrator()

    result = integrator.create_agent_workspace(
        agent_name="Test Agent",
        agent_role="测试智能体",
        agent_capabilities=[
            "功能1",
            "功能2",
            "功能3"
        ]
    )

    assert result.success
    assert result.workspace_path.exists()

    # 验证工作区结构
    assert (result.workspace_path / 'context').exists()
    assert (result.workspace_path / 'input').exists()
    assert (result.workspace_path / 'output').exists()
    assert (result.workspace_path / 'workspace').exists()

    print(f"✅ 智能体工作区测试通过")
    print(f"   工作区ID: {result.workspace_id}")


def test_task_workspace():
    """测试任务工作区"""
    print("\n### 测试3: 任务工作区集成 ###")

    integrator = TaskWorkspaceIntegrator()

    result = integrator.decompose_and_create_workspaces(
        task_name="测试任务",
        task_description="""
        这是一个测试任务，需要：
        1. 需求分析
        2. 系统设计
        3. 功能实现
        """,
        max_subtasks=3
    )

    assert result.success
    assert len(result.sub_tasks) > 0
    assert result.workspaces_created > 0

    print(f"✅ 任务工作区测试通过")
    print(f"   子任务数: {len(result.sub_tasks)}")
    print(f"   工作区数: {result.workspaces_created}")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("技能协同集成测试")
    print("=" * 60)

    try:
        test_improvement_cycle()
        test_agent_workspace()
        test_task_workspace()

        print("\n" + "=" * 60)
        print("✅ 所有集成测试通过！")
        print("=" * 60)

        print("\n集成功能:")
        print("  1. ✅ context-analysis ↔ context-optimization 循环")
        print("  2. ✅ workspace + agent-creator 集成")
        print("  3. ✅ task-decomposer + workspace 集成")

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
