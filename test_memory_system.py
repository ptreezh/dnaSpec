"""
测试智能体记忆系统 - 可选的、非侵入式记忆功能
"""
import sys
from pathlib import Path
from typing import List

# 添加src到路径
src_dir = Path(__file__).parent / 'src'
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from dna_context_engineering.memory import (
    MemoryManager,
    MemoryMixin,
    MemoryConfig,
    MemoryType,
    MemoryImportance
)


def test_memory_disabled_by_default():
    """测试1: 记忆默认禁用"""
    print("\n### 测试1: 记忆默认禁用 ###")

    # 创建默认配置的记忆管理器（应该禁用）
    manager = MemoryManager()

    print(f"记忆功能启用: {manager.is_enabled}")
    assert not manager.is_enabled, "记忆应该默认禁用"

    # 尝试添加记忆应该返回None
    memory_id = manager.add_memory("test-agent", "测试内容")
    assert memory_id is None, "禁用状态下add_memory应该返回None"

    print("✅ 记忆默认禁用测试通过")


def test_memory_optional_enable():
    """测试2: 可选启用记忆"""
    print("\n### 测试2: 可选启用记忆 ###")

    # 创建启用记忆的配置
    config = MemoryConfig(
        enabled=True,
        max_short_term=10,
        max_long_term=50
    )

    manager = MemoryManager(config)

    print(f"记忆功能启用: {manager.is_enabled}")
    assert manager.is_enabled, "记忆应该已启用"

    # 添加记忆
    memory_id = manager.add_memory(
        agent_id="agent-001",
        content="这是一个重要的bug修复",
        importance=MemoryImportance.HIGH
    )

    assert memory_id is not None, "启用状态下应该返回记忆ID"
    print(f"  创建记忆: {memory_id}")

    # 检索记忆
    memories = manager.recall_memories("agent-001", "bug")
    assert len(memories) > 0, "应该能检索到记忆"
    print(f"  检索到 {len(memories)} 条记忆")

    print("✅ 可选启用记忆测试通过")


def test_memory_mixin():
    """测试3: 记忆混入（非侵入式集成）"""
    print("\n### 测试3: 记忆混入 ###")

    # 模拟一个智能体
    class SimpleAgent:
        """简单智能体（无记忆功能）"""
        def __init__(self, agent_id: str):
            self.agent_id = agent_id

        def process(self, input_data: str) -> str:
            return f"处理: {input_data}"

    # 使用记忆混入包装智能体
    class AgentWithMemory:
        """带记忆的智能体（使用包装器）"""
        def __init__(self, base_agent: SimpleAgent, enable_memory: bool = False):
            self.base_agent = base_agent
            self.agent_id = base_agent.agent_id

            # 可选的记忆功能
            if enable_memory:
                config = MemoryConfig(enabled=True)
                memory_manager = MemoryManager(config)
                self.memory = MemoryMixin(base_agent.agent_id, memory_manager)
            else:
                memory_manager = MemoryManager()
                self.memory = MemoryMixin(base_agent.agent_id, memory_manager)

        def process(self, input_data: str) -> str:
            # 调用基础智能体
            result = self.base_agent.process(input_data)

            # 可选：记住处理结果
            if self.memory.memory_manager.is_enabled:
                self.memory.remember(f"处理: {input_data} -> {result}")

            return result

        def recall_history(self, query: str) -> List[str]:
            """回忆历史（可选功能）"""
            return self.memory.recall(query)

    # 测试1: 不启用记忆
    print("\n  测试A: 不启用记忆")
    base_agent = SimpleAgent("agent-test")
    agent_without_memory = AgentWithMemory(base_agent, enable_memory=False)

    result1 = agent_without_memory.process("测试输入")
    history1 = agent_without_memory.recall_history("测试")
    assert len(history1) == 0, "未启用记忆时应该返回空列表"
    print(f"    处理结果: {result1}")
    print(f"    历史记录: {len(history1)} 条（符合预期：无记忆）")

    # 测试2: 启用记忆
    print("\n  测试B: 启用记忆")
    base_agent2 = SimpleAgent("agent-test-2")
    agent_with_memory = AgentWithMemory(base_agent2, enable_memory=True)

    result2 = agent_with_memory.process("测试输入2")
    history2 = agent_with_memory.recall_history("测试输入2")
    print(f"    处理结果: {result2}")
    print(f"    历史记录: {len(history2)} 条")

    print("✅ 记忆混入测试通过")


def test_memory_isolation():
    """测试4: 记忆不影响基础技能"""
    print("\n### 测试4: 记忆不影响基础技能 ###")

    # 测试：启用记忆后，技能的核心功能不受影响
    manager_with_memory = MemoryManager(MemoryConfig(enabled=True))
    manager_without_memory = MemoryManager()  # 禁用

    # 两个智能体执行相同任务
    class TestAgent:
        def __init__(self, name: str, use_memory: bool = False):
            self.name = name
            self.memory_manager = MemoryManager(
                MemoryConfig(enabled=use_memory)
            ) if use_memory else MemoryManager()

        def execute_task(self, task: str) -> str:
            # 执行核心任务（不依赖记忆）
            result = f"任务 '{task}' 执行完成"

            # 可选：记录到记忆
            self.memory_manager.add_memory(
                agent_id=self.name,
                content=result,
                importance=MemoryImportance.MEDIUM
            )

            return result

    # 创建两个智能体
    agent1 = TestAgent("agent-no-memory", use_memory=False)
    agent2 = TestAgent("agent-with-memory", use_memory=True)

    # 执行相同任务
    task_result1 = agent1.execute_task("分析代码")
    task_result2 = agent2.execute_task("分析代码")

    # 核心功能应该相同
    assert task_result1 == task_result2, "记忆不应该影响核心功能"
    print(f"  无记忆智能体结果: {task_result1}")
    print(f"  有记忆智能体结果: {task_result2}")
    print(f"  结果一致: ✅")

    # 但agent2应该有记忆
    stats2 = agent2.memory_manager.get_stats("agent-with-memory")
    assert stats2 is not None, "有记忆的智能体应该有统计"
    assert stats2['total_memories'] > 0, "应该有记忆记录"
    print(f"  记忆数量: {stats2['total_memories']}")

    print("✅ 记忆不影响基础技能测试通过")


def test_memory_cleanup():
    """测试5: 记忆清理"""
    print("\n### 测试5: 记忆清理 ###")

    config = MemoryConfig(
        enabled=True,
        max_short_term=5,  # 限制为5条
        auto_cleanup=True
    )

    manager = MemoryManager(config)

    # 添加10条记忆（超过限制）
    agent_id = "cleanup-test-agent"
    for i in range(10):
        manager.add_memory(
            agent_id=agent_id,
            content=f"记忆内容 {i}",
            importance=MemoryImportance.LOW  # 低重要性
        )

    stats = manager.get_stats(agent_id)
    print(f"  添加前: {stats['total_memories']} 条记忆")

    # 执行清理
    manager.cleanup(agent_id)

    stats_after = manager.get_stats(agent_id)
    print(f"  清理后: {stats_after['total_memories']} 条记忆")

    # 应该保留重要记忆
    assert stats_after['total_memories'] <= 5, "应该限制在max_short_term以内"

    print("✅ 记忆清理测试通过")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("智能体记忆系统测试 - 可选的、非侵入式")
    print("=" * 60)

    try:
        test_memory_disabled_by_default()
        test_memory_optional_enable()
        test_memory_mixin()
        test_memory_isolation()
        test_memory_cleanup()

        print("\n" + "=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60)

        print("\n记忆系统特性:")
        print("  1. ✅ 默认禁用 - 不影响现有技能")
        print("  2. ✅ 可选启用 - 按需激活")
        print("  3. ✅ 完全独立 - 不修改核心代码")
        print("  4. ✅ 向后兼容 - 无记忆时正常工作")
        print("  5. ✅ 自动清理 - 防止记忆膨胀")

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
