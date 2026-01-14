"""
示例3: 混合使用 - 技能记忆 + 项目记忆
场景: 智能项目管理系统
"""
import sys
from pathlib import Path

# 添加src到路径
script_dir = Path(__file__).parent
src_dir = script_dir.parent / 'src'
project_root = script_dir.parent

if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from dna_context_engineering.memory import (
    create_task_decomposer_with_memory,
    MemoryManager,
    MemoryConfig,
    MemoryImportance
)


class MockTaskDecomposer:
    """模拟任务分解技能"""
    def execute_skill(self, input_data):
        task = input_data.get('input', '')

        return {
            'task': task,
            'subtasks': [
                {'id': '1', 'name': '需求确认', 'status': 'pending'},
                {'id': '2', 'name': '方案设计', 'status': 'pending'},
                {'id': '3', 'name': '开发实施', 'status': 'pending'},
                {'id': '4', 'name': '测试验证', 'status': 'pending'},
                {'id': '5', 'name': '部署上线', 'status': 'pending'}
            ],
            'estimated_hours': 80,
            'complexity': 'medium'
        }


class IntelligentProjectManager:
    """智能项目管理系统"""

    def __init__(self, project_name: str):
        self.project_name = project_name

        # 1. 技能记忆：让规划技能记住经验
        self.planner = create_task_decomposer_with_memory(
            MockTaskDecomposer(),
            enable_memory=True
        )

        # 2. 项目记忆：记住项目的所有历史
        config = MemoryConfig(
            enabled=True,
            max_short_term=200,
            max_long_term=1000
        )
        self.project_memory = MemoryManager(config)

    def plan_project_phase(self, phase_description: str):
        """规划项目阶段"""
        print(f"\n📋 规划阶段: {phase_description}")
        print("-" * 60)

        # 技能层：规划任务（技能会记住规划模式）
        plan = self.planner.execute({
            'input': phase_description,
            'decomposition_method': 'hierarchical'
        })

        subtasks = plan.get('subtasks', [])
        print(f"  生成 {len(subtasks)} 个任务:")
        for task in subtasks:
            print(f"    - {task['name']}")

        # 项目层：记住这个规划决策
        self.project_memory.add_memory(
            agent_id=self.project_name,
            content=f"规划决策: {phase_description} → {len(subtasks)}个任务",
            importance=MemoryImportance.HIGH
        )

        # 检查技能是否有类似规划的经验
        similar_plans = self.planner.recall_similar_decompositions(phase_description[:10])
        if similar_plans:
            print(f"\n  💡 规划技能回忆起 {len(similar_plans)} 条类似经验")
            print(f"     规划质量会基于历史经验优化")

        return plan

    def make_architecture_decision(self, decision: str, rationale: str):
        """记录架构决策"""
        self.project_memory.add_memory(
            agent_id=self.project_name,
            content=f"架构决策: {decision}",
            importance=MemoryImportance.CRITICAL
        )

        self.project_memory.add_memory(
            agent_id=self.project_name,
            content=f"决策理由: {rationale}",
            importance=MemoryImportance.HIGH
        )

        print(f"\n🏗️  架构决策: {decision}")
        print(f"   理由: {rationale}")
        print("   ✅ 已记录到项目记忆")

    def record_team_insight(self, insight: str):
        """记录团队洞察"""
        self.project_memory.add_memory(
            agent_id=self.project_name,
            content=f"团队洞察: {insight}",
            importance=MemoryImportance.MEDIUM
        )

        print(f"\n💡 团队洞察: {insight}")
        print("   ✅ 已记录到项目知识库")

    def review_project_history(self):
        """回顾项目历史"""
        print(f"\n📊 项目历史回顾: {self.project_name}")
        print("=" * 60)

        # 获取所有决策
        decisions = self.project_memory.recall_memories(
            self.project_name,
            "决策"
        )

        # 获取所有洞察
        insights = self.project_memory.recall_memories(
            self.project_name,
            "洞察"
        )

        # 获取统计
        stats = self.project_memory.get_stats(self.project_name)

        print(f"\n  总记忆条目: {stats['total_memories'] if stats else 0}")
        print(f"\n  🏗️  架构决策 ({len(decisions)} 条):")
        for d in decisions[-5:]:
            print(f"     - {d.content}")

        print(f"\n  💡 团队洞察 ({len(insights)} 条):")
        for i in insights[-5:]:
            print(f"     - {i.content}")

        # 检查技能学习情况
        skill_stats = self.planner.memory_manager.get_stats(self.planner.skill_id)
        if skill_stats:
            print(f"\n  🔧 规划技能学习:")
            print(f"     经验积累: {skill_stats['total_memories']} 次规划")
            print(f"     技能正在优化规划质量...")

    def get_project_recommendations(self):
        """基于历史获取建议"""
        print(f"\n🎯 智能建议: {self.project_name}")
        print("-" * 60)

        # 检查项目记忆
        history = self.project_memory.recall_memories(self.project_name, "", limit=10)

        if len(history) > 5:
            print("  ✅ 项目已积累足够的历史经验")
            print("  💡 建议:")
            print("     - 可以分析决策模式")
            print("     - 可以提取最佳实践")
            print("     - 可以预测潜在风险")
        else:
            print("  ⚡ 项目处于早期阶段")
            print("  💡 建议:")
            print("     - 继续记录决策和洞察")
            print("     - 建立知识库")
            print("     - 定期回顾历史")


def demo_hybrid_memory():
    """演示混合使用"""

    print("=" * 70)
    print("示例3: 技能记忆 + 项目记忆（混合使用）")
    print("=" * 70)
    print("\n场景: 智能项目管理系统")
    print("  - 技能记忆: 规划技能学习经验")
    print("  - 项目记忆: 记住项目决策历史")
    print("-" * 70)

    # 创建项目管理系统
    pm_system = IntelligentProjectManager("电商平台重构")

    # 项目第1周：初始规划
    print("\n" + "=" * 70)
    print("【第1周】项目启动")
    print("=" * 70)

    pm_system.plan_project_phase("用户服务重构")
    pm_system.make_architecture_decision(
        "采用微服务架构",
        "提高可扩展性和独立部署能力"
    )
    pm_system.record_team_insight(
        "建议使用容器化部署以简化环境配置"
    )

    # 项目第3周：第二个阶段
    print("\n" + "=" * 70)
    print("【第3周】订单服务重构")
    print("=" * 70)

    plan = pm_system.plan_project_phase("订单服务重构")

    print("\n  💡 规划技能已积累经验:")
    print(f"     之前规划过类似任务，可以参考")

    pm_system.make_architecture_decision(
        "采用事件驱动架构",
        "解耦订单处理流程，提高吞吐量"
    )

    # 项目第6周：回顾和决策
    print("\n" + "=" * 70)
    print("【第6周】项目回顾")
    print("=" * 70)

    pm_system.record_team_insight(
        "微服务间通信延迟需要优化"
    )
    pm_system.make_architecture_decision(
        "引入API网关",
        "统一管理服务调用和安全认证"
    )

    # 项目总结
    print("\n" + "=" * 70)
    print("【项目总结】")
    print("=" * 70)

    pm_system.review_project_history()
    pm_system.get_project_recommendations()

    print("\n" + "=" * 70)
    print("效果总结:")
    print("\n  ✅ 技能层面:")
    print("     - 规划技能记住了3次规划经验")
    print("     - 后续规划会参考历史模式")
    print("     - 规划质量和一致性提高")
    print("\n  ✅ 项目层面:")
    print("     - 记住所有架构决策和理由")
    print("     - 记住团队洞察和经验")
    print("     - 跨时间保持项目连贯性")
    print("\n  💡 混合优势:")
    print("     - 技能越来越聪明（经验积累）")
    print("     - 项目有完整历史（决策可追溯）")
    print("     - 新成员可以快速了解历史")
    print("=" * 70)


if __name__ == '__main__':
    demo_hybrid_memory()
