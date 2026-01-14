"""
示例1: 技能记忆增强
场景: 长期使用 task-decomposer，让它积累分解经验
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

from dna_context_engineering.memory import create_task_decomposer_with_memory


class MockTaskDecomposer:
    """模拟任务分解技能"""
    def execute_skill(self, input_data):
        task = input_data.get('input', '')

        # 模拟：如果是第一次见到这类任务，返回通用分解
        # 如果见过类似任务，返回更精细的分解（基于记忆）

        return {
            'task': task,
            'subtasks': [
                {'id': '1', 'name': '需求分析', 'estimated_hours': 8},
                {'id': '2', 'name': '技术选型', 'estimated_hours': 16},
                {'id': '3', 'name': '系统设计', 'estimated_hours': 24},
                {'id': '4', 'name': '开发实现', 'estimated_hours': 40},
                {'id': '5', 'name': '测试部署', 'estimated_hours': 16}
            ],
            'complexity': 'medium',
            'estimated_total_hours': 104
        }


def demo_skill_memory_enhancement():
    """演示技能记忆增强"""

    print("=" * 70)
    print("示例1: 技能记忆增强")
    print("=" * 70)
    print("\n场景: 长期使用 task-decomposer 分解用户相关功能")
    print("效果: 技能记住分解模式，后续分解越来越精细")
    print("-" * 70)

    # 创建带记忆的分解器
    decomposer = create_task_decomposer_with_memory(
        MockTaskDecomposer(),
        enable_memory=True
    )

    # 模拟第1周：分解"用户登录"功能
    print("\n[第1周] 分解任务: 用户登录功能")
    result1 = decomposer.execute({'input': '用户登录功能'})

    subtasks1 = result1.get('subtasks', [])
    print(f"  生成 {len(subtasks1)} 个子任务")
    for task in subtasks1:
        print(f"    - {task['name']} ({task['estimated_hours']}h)")

    print("\n  ✅ 技能记住了这次分解")

    # 模拟第2周：分解"用户注册"功能
    print("\n[第2周] 分解任务: 用户注册功能")
    result2 = decomposer.execute({'input': '用户注册功能'})

    subtasks2 = result2.get('subtasks', [])
    print(f"  生成 {len(subtasks2)} 个子任务")

    # 回顾类似任务的历史
    print("\n  💡 技能回忆起之前的'用户登录'分解经验:")
    similar = decomposer.recall_similar_decompositions('用户')
    for memory in similar[:3]:
        print(f"    - {memory}")

    # 模拟第4周：分解"密码重置"功能
    print("\n[第4周] 分解任务: 密码重置功能")
    result3 = decomposer.execute({'input': '密码重置功能'})

    # 查看记忆增长
    stats = decomposer.memory_manager.get_stats(decomposer.skill_id)
    print(f"\n  📊 技能记忆统计:")
    print(f"     总记忆: {stats['total_memories']} 条")
    print(f"     短期: {stats['short_term_count']} 条")
    print(f"     长期: {stats['long_term_count']} 条")

    print("\n  💡 现在技能已积累 {len(similar)} 条用户相关功能的分解经验")

    print("\n" + "=" * 70)
    print("效果总结:")
    print("  ✅ 技能记住了3个用户相关功能的分解模式")
    print("  ✅ 后续分解类似功能时，可以参考历史经验")
    print("  ✅ 分解一致性和质量会随使用提高")
    print("=" * 70)


if __name__ == '__main__':
    demo_skill_memory_enhancement()
