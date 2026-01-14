"""
测试 Agent-Creator 与记忆系统集成
验证非侵入式集成和向后兼容性
"""
import sys
from pathlib import Path

# 添加src到路径
src_dir = Path(__file__).parent / 'src'
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from dna_context_engineering.memory import (
    AgentWithMemory,
    AgentMemoryIntegrator,
    create_agent_from_creator,
    MemoryConfig
)


def test_backward_compatibility():
    """测试1: 向后兼容 - 不启用记忆时正常工作"""
    print("\n### 测试1: 向后兼容性 ###")

    # 模拟 agent-creator 生成的配置
    agent_config = {
        'id': 'test-agent-001',
        'role': '数据分析助手',
        'domain': 'analysis',
        'agent_type': 'task_specialist',
        'capabilities': ['Data analysis', 'Report generation'],
        'instructions': '你是数据分析专家',
        'personality': {'type': 'professional_precise', 'name': '专业精确型'},
        'interaction_guidelines': ['保持专业'],
        'scope_limitations': ['专注数据分析'],
        'success_metrics': ['准确率']
    }

    # 创建不带记忆的智能体（默认）
    agent = AgentWithMemory(agent_config, enable_memory=False)

    # 验证基本功能
    result = agent.execute_task('分析销售数据')
    assert result['status'] == 'completed', "任务应该完成"
    assert result['agent_id'] == 'test-agent-001', "智能体ID应该匹配"

    # 验证记忆未启用
    assert not agent.has_memory, "记忆应该未启用"
    history = agent.recall_relevant_history('销售')
    assert len(history) == 0, "未启用记忆时应该返回空列表"

    print("  ✅ 不启用记忆时智能体正常工作")
    print("  ✅ 记忆功能完全可选")
    print("✅ 向后兼容性测试通过")


def test_memory_enhanced_agent():
    """测试2: 启用记忆的智能体"""
    print("\n### 测试2: 记忆增强智能体 ###")

    agent_config = {
        'id': 'test-agent-002',
        'role': '代码审查专家',
        'domain': 'software_development',
        'agent_type': 'domain_expert',
        'capabilities': ['Code review', 'Security analysis', 'Best practices'],
        'instructions': '你是代码审查专家',
        'personality': {'type': 'analytical_critical', 'name': '分析批判型'},
        'interaction_guidelines': ['批判性思考'],
        'scope_limitations': ['专注代码质量'],
        'success_metrics': ['代码质量']
    }

    # 创建启用记忆的智能体
    agent = AgentWithMemory(agent_config, enable_memory=True)

    # 验证记忆已启用
    assert agent.has_memory, "记忆应该已启用"

    # 执行多个任务
    tasks = [
        '审查登录模块代码',
        '检查API安全性',
        '优化数据库查询'
    ]

    for task in tasks:
        result = agent.execute_task(task)
        assert result['status'] == 'completed', f"任务 '{task}' 应该完成"

    # 验证记忆存储
    stats = agent.memory_manager.get_stats('test-agent-002')
    assert stats is not None, "应该有记忆统计"
    assert stats['total_memories'] > 0, "应该有记忆记录"
    print(f"  记忆数量: {stats['total_memories']}")

    # 验证记忆检索
    history = agent.recall_relevant_history('审查')
    assert len(history) > 0, "应该能检索到相关记忆"
    print(f"  检索到 {len(history)} 条相关记忆")

    print("✅ 记忆增强智能体测试通过")


def test_integrator_workflow():
    """测试3: 集成器工作流"""
    print("\n### 测试3: 集成器工作流 ###")

    integrator = AgentMemoryIntegrator()

    # 创建多个智能体
    configs = [
        {
            'id': 'agent-a',
            'role': '测试助手',
            'capabilities': ['Unit testing']
        },
        {
            'id': 'agent-b',
            'role': '文档助手',
            'capabilities': ['Documentation']
        }
    ]

    # 创建不带记忆的智能体
    agent_a = integrator.create_agent_with_memory(configs[0], enable_memory=False)
    agent_b = integrator.create_agent_with_memory(configs[1], enable_memory=True)

    # 验证注册
    assert 'agent-a' in integrator.agents, "agent-a 应该已注册"
    assert 'agent-b' in integrator.agents, "agent-b 应该已注册"

    # 列出智能体
    agents_list = integrator.list_agents()
    assert len(agents_list) == 2, "应该有2个智能体"

    # 验证记忆差异
    info_a = agent_a.get_agent_info()
    info_b = agent_b.get_agent_info()

    assert not info_a['has_memory'], "agent-a 不应该有记忆"
    assert info_b['has_memory'], "agent-b 应该有记忆"

    print(f"  注册智能体: {len(agents_list)}")
    print(f"  agent-a 有记忆: {info_a['has_memory']}")
    print(f"  agent-b 有记忆: {info_b['has_memory']}")

    print("✅ 集成器工作流测试通过")


def test_creator_integration():
    """测试4: 与 agent-creator 集成"""
    print("\n### 测试4: Agent-Creator 集成 ###")

    # 模拟 agent-creator 的返回结果
    creator_result = {
        'agent_config': {
            'id': 'creator-agent-001',
            'role': '性能优化专家',
            'domain': 'technical',
            'agent_type': 'task_specialist',
            'capabilities': ['Performance analysis', 'Optimization'],
            'instructions': '优化系统性能',
            'personality': {'type': 'direct_efficient', 'name': '直接高效型'},
            'interaction_guidelines': ['直接高效'],
            'scope_limitations': ['专注性能'],
            'success_metrics': ['性能提升']
        },
        'creation_metadata': {
            'agent_type': 'task_specialist',
            'complexity': 'medium',
            'estimated_effectiveness': 0.9
        },
        'quality_metrics': {
            'overall_quality': 0.85
        }
    }

    # 使用便捷函数创建智能体（不启用记忆）
    agent_no_memory = create_agent_from_creator(
        creator_result,
        enable_memory=False
    )

    assert not agent_no_memory.has_memory, "默认不应该启用记忆"

    # 使用便捷函数创建智能体（启用记忆）
    agent_with_memory = create_agent_from_creator(
        creator_result,
        enable_memory=True
    )

    assert agent_with_memory.has_memory, "应该启用记忆"

    # 执行任务对比
    task = '优化数据库查询性能'

    result1 = agent_no_memory.execute_task(task)
    result2 = agent_with_memory.execute_task(task)

    # 核心功能应该相同
    assert result1['task'] == result2['task'], "任务应该相同"
    assert result1['status'] == result2['status'], "状态应该相同"

    # 但 agent_with_memory 应该有记忆
    stats = agent_with_memory.memory_manager.get_stats('creator-agent-001')
    assert stats['total_memories'] > 0, "应该有记忆记录"

    print(f"  不带记忆智能体完成任务: {result1['status']}")
    print(f"  带记忆智能体完成任务: {result2['status']}")
    print(f"  记忆数量: {stats['total_memories']}")

    print("✅ Agent-Creator 集成测试通过")


def test_memory_cleanup():
    """测试5: 记忆清理"""
    print("\n### 测试5: 记忆清理 ###")

    agent_config = {
        'id': 'cleanup-test-agent',
        'role': '临时助手',
        'capabilities': ['Temp work']
    }

    # 创建启用记忆的智能体
    memory_config = MemoryConfig(
        enabled=True,
        max_short_term=5,
        auto_cleanup=True
    )

    agent = AgentWithMemory(agent_config, enable_memory=True, memory_config=memory_config)

    # 执行多个任务
    for i in range(10):
        agent.execute_task(f'任务 {i}')

    # 检查记忆数量
    stats_before = agent.memory_manager.get_stats('cleanup-test-agent')
    memories_before = stats_before['total_memories'] if stats_before else 0
    print(f"  清理前记忆数: {memories_before}")

    # 执行清理
    remaining = agent.cleanup_memory()
    print(f"  清理后记忆数: {remaining}")

    # 应该限制在 max_short_term 以内
    assert remaining <= 5, "记忆数量应该限制在max_short_term以内"

    print("✅ 记忆清理测试通过")


def test_task_tracking_workflow():
    """测试6: 任务追踪工作流"""
    print("\n### 测试6: 任务追踪工作流 ###")

    agent_config = {
        'id': 'tracking-agent',
        'role': '项目追踪助手',
        'capabilities': ['Task tracking', 'Progress monitoring']
    }

    agent = AgentWithMemory(agent_config, enable_memory=True)

    # 使用追踪函数运行多个任务
    tasks = [
        '设计系统架构',
        '实现核心功能',
        '编写测试用例',
        '性能优化',
        '文档编写'
    ]

    from dna_context_engineering.memory import run_agent_with_memory_tracking
    from tempfile import NamedTemporaryFile
    import tempfile

    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        export_path = Path(f.name)

    try:
        results = run_agent_with_memory_tracking(agent, tasks, export_path)

        assert len(results) == 5, "应该完成5个任务"
        for result in results:
            assert result['status'] == 'completed', "每个任务都应该完成"

        # 验证导出文件存在
        assert export_path.exists(), "记忆导出文件应该存在"

        print(f"  完成任务数: {len(results)}")
        print(f"  记忆已导出: {export_path.name}")

    finally:
        # 清理临时文件
        if export_path.exists():
            export_path.unlink()

    print("✅ 任务追踪工作流测试通过")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("Agent-Creator 与记忆系统集成测试")
    print("=" * 60)

    try:
        test_backward_compatibility()
        test_memory_enhanced_agent()
        test_integrator_workflow()
        test_creator_integration()
        test_memory_cleanup()
        test_task_tracking_workflow()

        print("\n" + "=" * 60)
        print("✅ 所有集成测试通过！")
        print("=" * 60)

        print("\n集成验证:")
        print("  1. ✅ 向后兼容 - 不启用记忆时正常工作")
        print("  2. ✅ 非侵入式 - 包装器不影响基础智能体")
        print("  3. ✅ 可选启用 - 记忆功能完全可选")
        print("  4. ✅ 集成工作流 - 支持批量创建和管理")
        print("  5. ✅ 记忆清理 - 自动管理记忆数量")
        print("  6. ✅ 任务追踪 - 完整的任务-记忆生命周期")

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
