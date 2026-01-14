"""
CI/CD 项目助手 - 使用记忆系统学习项目历史
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


class MockTaskDecomposer:
    """模拟任务分解技能"""
    def execute_skill(self, input_data):
        task = input_data.get('input', '')
        return {
            'task': task,
            'decomposition_method': input_data.get('decomposition_method', 'hierarchical'),
            'subtasks': [
                {'id': '1', 'name': '需求分析', 'status': 'pending'},
                {'id': '2', 'name': '技术选型', 'status': 'pending'},
                {'id': '3', 'name': '原型设计', 'status': 'pending'},
                {'id': '4', 'name': '核心开发', 'status': 'pending'},
                {'id': '5', 'name': '测试部署', 'status': 'pending'}
            ],
            'complexity_analysis': {
                'overall_complexity': 'medium',
                'estimated_hours': 40
            }
        }


class MockArchitect:
    """模拟架构师技能"""
    def execute_skill(self, input_data):
        requirement = input_data.get('input', '')
        style = input_data.get('architecture_style', 'microservices')

        return {
            'requirement': requirement,
            'architecture_style': style,
            'architecture_design': {
                'style': style,
                'components': [
                    {'name': 'API Gateway', 'type': 'gateway'},
                    {'name': 'Auth Service', 'type': 'service'},
                    {'name': 'Business Service', 'type': 'service'},
                    {'name': 'Database', 'type': 'database'},
                    {'name': 'Cache', 'type': 'cache'}
                ]
            },
            'quality_metrics': {
                'scalability': 0.9,
                'maintainability': 0.85,
                'reliability': 0.88,
                'overall_quality': 0.88
            }
        }


class CIProjectHelper:
    """CI/CD 项目助手"""

    def __init__(self, config_path: str = "config/memory_config.json"):
        # 加载配置
        try:
            from scripts.memory_config_loader import MemoryConfigLoader
            self.config_loader = MemoryConfigLoader(config_path)
        except Exception as e:
            print(f"⚠️  无法加载配置: {e}")
            print("使用默认配置")
            self.config_loader = None

        # 导入记忆组件
        from dna_context_engineering.memory import (
            create_task_decomposer_with_memory,
            create_architect_with_memory,
            SkillsMemoryManager,
            MemoryConfig
        )

        # 创建带记忆的技能
        task_decomposer_skill = MockTaskDecomposer()
        architect_skill = MockArchitect()

        # 检查是否启用
        task_enabled = self._is_skill_enabled('task-decomposer')
        arch_enabled = self._is_skill_enabled('architect')

        self.task_decomposer = create_task_decomposer_with_memory(
            task_decomposer_skill,
            enable_memory=task_enabled
        )

        self.architect = create_architect_with_memory(
            architect_skill,
            enable_memory=arch_enabled
        )

        # 统一管理
        self.manager = SkillsMemoryManager()
        if self.task_decomposer.has_memory:
            self.manager.register_skill(self.task_decomposer)
        if self.architect.has_memory:
            self.manager.register_skill(self.architect)

    def _is_skill_enabled(self, skill_name: str) -> bool:
        """检查技能是否启用记忆"""
        if self.config_loader:
            return self.config_loader.is_skill_enabled(skill_name)
        return False  # 默认禁用

    def plan_project(self, project_description: str) -> dict:
        """
        规划新项目（利用历史经验）

        Args:
            project_description: 项目描述

        Returns:
            项目规划
        """
        print(f"\n📋 规划项目: {project_description}")

        # 1. 回顾类似项目
        if self.task_decomposer.has_memory:
            similar = self.task_decomposer.recall_similar_decompositions(project_description[:20])
            if similar:
                print(f"\n💡 找到 {len(similar)} 条类似项目经验:")
                for memory in similar[:3]:
                    print(f"  - {memory}")

        # 2. 分解任务
        print("\n🔨 分解项目任务...")
        tasks = self.task_decomposer.execute({
            'input': project_description,
            'decomposition_method': 'hierarchical'
        })

        subtasks = tasks.get('subtasks', [])
        print(f"  生成 {len(subtasks)} 个子任务:")
        for task in subtasks[:3]:
            print(f"    - {task.get('name', 'Unknown')}")
        if len(subtasks) > 3:
            print(f"    ... 还有 {len(subtasks) - 3} 个任务")

        # 3. 设计架构
        print("\n🏗️  设计项目架构...")
        architecture = self.architect.execute({
            'input': project_description,
            'architecture_style': 'auto'
        })

        style = architecture.get('architecture_style', 'unknown')
        components = architecture.get('architecture_design', {}).get('components', [])
        quality = architecture.get('quality_metrics', {}).get('overall_quality', 0)

        print(f"  架构风格: {style}")
        print(f"  核心组件: {len(components)} 个")
        print(f"  质量评分: {quality:.2f}")

        return {
            'tasks': tasks,
            'architecture': architecture
        }

    def show_memory_stats(self):
        """显示记忆统计"""
        print("\n📊 记忆统计:")
        print("-" * 60)

        skills = self.manager.list_skills()
        for skill_info in skills:
            skill_name = skill_info['skill_name']
            has_memory = "✅" if skill_info['has_memory'] else "❌"
            stats = skill_info.get('memory_stats', {})
            total = stats.get('total_memories', 0)

            print(f"  {has_memory} {skill_name}: {total} 条记忆")

            if total > 0:
                short = stats.get('short_term_count', 0)
                long = stats.get('long_term_count', 0)
                print(f"      短期: {short}, 长期: {long}")


def main():
    """主函数"""
    print("=" * 70)
    print("CI/CD 项目助手 - 智能项目规划和经验积累")
    print("=" * 70)

    # 初始化助手
    helper = CIProjectHelper()

    # 规划多个项目（第二个项目会利用第一个的经验）
    projects = [
        "构建微服务架构的电商平台",
        "开发内容管理系统",
        "创建实时数据分析平台"
    ]

    for i, project in enumerate(projects, 1):
        print(f"\n{'=' * 70}")
        print(f"项目 {i}: {project}")
        print('=' * 70)

        result = helper.plan_project(project)

        # 显示记忆增长
        if helper.task_decomposer.has_memory or helper.architect.has_memory:
            print("\n当前记忆状态:")
            helper.show_memory_stats()

    # 最终统计
    print(f"\n{'=' * 70}")
    print("最终记忆统计")
    print('=' * 70)
    helper.show_memory_stats()

    print("\n" + "=" * 70)
    print("✅ 所有项目规划完成！")
    print("=" * 70)

    if helper.task_decomposer.has_memory or helper.architect.has_memory:
        print("\n💡 记忆系统已启用:")
        print("   - 技能已记住所有项目的规划经验")
        print("   - 后续项目可以利用这些经验")
        print("   - 定期备份: python scripts/backup_memory.py")


if __name__ == '__main__':
    main()
