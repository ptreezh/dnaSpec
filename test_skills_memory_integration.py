"""
测试 DNASPEC 技能与记忆系统集成
验证 task-decomposer、architect 等技能的记忆增强
"""
import sys
from pathlib import Path

# 添加src到路径
src_dir = Path(__file__).parent / 'src'
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from dna_context_engineering.memory import (
    TaskDecomposerWithMemory,
    ArchitectWithMemory,
    ModulizerWithMemory,
    ConstraintGeneratorWithMemory,
    SkillsMemoryManager,
    create_task_decomposer_with_memory,
    create_architect_with_memory
)


def test_task_decomposer_memory():
    """测试1: 任务分解技能记忆集成"""
    print("\n### 测试1: Task-Decomposer 记忆集成 ###")

    # 模拟 task-decomposer 技能
    class MockTaskDecomposer:
        def execute_skill(self, input_data):
            task = input_data.get('input', '')
            method = input_data.get('decomposition_method', 'hierarchical')

            # 模拟分解结果
            return {
                'task': task,
                'decomposition_method': method,
                'subtasks': [
                    {'id': '1', 'name': '需求分析', 'status': 'pending'},
                    {'id': '2', 'name': '技术选型', 'status': 'pending'},
                    {'id': '3', 'name': '原型设计', 'status': 'pending'},
                    {'id': '4', 'name': '核心开发', 'status': 'pending'}
                ],
                'complexity_analysis': {
                    'overall_complexity': 'medium',
                    'estimated_hours': 40
                }
            }

    mock_skill = MockTaskDecomposer()

    # 测试1A: 不启用记忆
    print("\n  测试A: 不启用记忆")
    decomposer_no_memory = create_task_decomposer_with_memory(
        mock_skill,
        enable_memory=False
    )

    result1 = decomposer_no_memory.execute({
        'input': '实现用户认证系统',
        'decomposition_method': 'sequential'
    })

    assert result1['task'] == '实现用户认证系统'
    assert len(result1['subtasks']) == 4
    assert not decomposer_no_memory.has_memory

    history = decomposer_no_memory.recall_similar_decompositions('认证')
    assert len(history) == 0

    print(f"    ✅ 分解完成: {len(result1['subtasks'])} 个子任务")
    print(f"    ✅ 记忆未启用")

    # 测试1B: 启用记忆
    print("\n  测试B: 启用记忆")
    decomposer_with_memory = create_task_decomposer_with_memory(
        mock_skill,
        enable_memory=True
    )

    # 执行多个分解
    tasks = [
        {'input': '实现用户认证系统', 'decomposition_method': 'sequential'},
        {'input': '设计数据库架构', 'decomposition_method': 'hierarchical'},
        {'input': '开发API接口', 'decomposition_method': 'parallel'}
    ]

    for task_input in tasks:
        result = decomposer_with_memory.execute(task_input)
        print(f"    分解: {task_input['input'][:20]}... → {len(result['subtasks'])} 个子任务")

    # 验证记忆存储
    stats = decomposer_with_memory.memory_manager.get_stats(decomposer_with_memory.skill_id)
    assert stats is not None
    assert stats['total_memories'] > 0
    print(f"    记忆数量: {stats['total_memories']}")

    # 验证记忆检索
    auth_history = decomposer_with_memory.recall_similar_decompositions('认证')
    assert len(auth_history) > 0
    print(f"    检索 '认证': {len(auth_history)} 条相关记忆")

    db_history = decomposer_with_memory.recall_similar_decompositions('数据库')
    assert len(db_history) > 0
    print(f"    检索 '数据库': {len(db_history)} 条相关记忆")

    print("✅ Task-Decomposer 记忆集成测试通过")


def test_architect_memory():
    """测试2: 架构师技能记忆集成"""
    print("\n### 测试2: Architect 记忆集成 ###")

    # 模拟 architect 技能
    class MockArchitect:
        def execute_skill(self, input_data):
            requirement = input_data.get('input', '')
            style = input_data.get('architecture_style', 'microservices')

            # 模拟架构设计
            return {
                'requirement': requirement,
                'architecture_style': style,
                'architecture_design': {
                    'style': style,
                    'components': [
                        {'name': 'API Gateway', 'type': 'gateway'},
                        {'name': 'Auth Service', 'type': 'service'},
                        {'name': 'User Service', 'type': 'service'},
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

    mock_skill = MockArchitect()

    # 创建带记忆的架构师
    architect = create_architect_with_memory(mock_skill, enable_memory=True)

    # 设计多个架构
    designs = [
        {'input': '电商平台微服务架构', 'architecture_style': 'microservices'},
        {'input': '内容管理系统', 'architecture_style': 'layered'},
        {'input': '实时数据处理系统', 'architecture_style': 'event-driven'}
    ]

    print("\n  设计架构:")
    for design_input in designs:
        result = architect.execute(design_input)
        style = result['architecture_style']
        components = result['architecture_design']['components']
        quality = result['quality_metrics']['overall_quality']
        print(f"    {design_input['input'][:25]}... {style} ({len(components)} 组件, 质量: {quality:.2f})")

    # 验证记忆
    stats = architect.memory_manager.get_stats(architect.skill_id)
    assert stats is not None
    print(f"\n  记忆统计:")
    print(f"    总记忆数: {stats['total_memories']}")

    # 回顾相似设计
    ecommerce_history = architect.recall_similar_designs('电商')
    assert len(ecommerce_history) > 0
    print(f"    检索 '电商': {len(ecommerce_history)} 条相关记忆")

    print("✅ Architect 记忆集成测试通过")


def test_modulizer_memory():
    """测试3: 模块化技能记忆集成"""
    print("\n### 测试3: Modulizer 记忆集成 ###")

    # 模拟 modulizer 技能
    class MockModulizer:
        def execute_skill(self, input_data):
            desc = input_data.get('codebase_description', '')

            return {
                'codebase': desc,
                'modules': [
                    {'name': 'auth', 'responsibility': '用户认证'},
                    {'name': 'user', 'responsibility': '用户管理'},
                    {'name': 'content', 'responsibility': '内容管理'}
                ],
                'modularity_score': 0.82
            }

    mock_skill = MockModulizer()

    # 创建带记忆的模块化技能
    from dna_context_engineering.memory import create_modulizer_with_memory
    modulizer = create_modulizer_with_memory(mock_skill, enable_memory=True)

    # 执行模块化
    result = modulizer.execute({
        'codebase_description': '大型博客系统需要模块化重构'
    })

    assert len(result['modules']) == 3
    assert modulizer.has_memory

    stats = modulizer.memory_manager.get_stats(modulizer.skill_id)
    assert stats['total_memories'] > 0

    print(f"  模块化完成: {len(result['modules'])} 个模块")
    print(f"  记忆数量: {stats['total_memories']}")
    print("✅ Modulizer 记忆集成测试通过")


def test_constraint_generator_memory():
    """测试4: 约束生成技能记忆集成"""
    print("\n### 测试4: Constraint-Generator 记忆集成 ###")

    # 模拟 constraint-generator 技能
    class MockConstraintGenerator:
        def execute_skill(self, input_data):
            req = input_data.get('requirement_description', '')

            return {
                'requirement': req,
                'constraints': [
                    {'type': 'performance', 'description': '响应时间 < 200ms'},
                    {'type': 'security', 'description': '必须使用HTTPS'},
                    {'type': 'scalability', 'description': '支持10万并发'}
                ],
                'constraint_count': 3
            }

    mock_skill = MockConstraintGenerator()

    # 创建带记忆的约束生成技能
    from dna_context_engineering.memory import create_constraint_generator_with_memory
    generator = create_constraint_generator_with_memory(mock_skill, enable_memory=True)

    # 生成约束
    result = generator.execute({
        'requirement_description': '高性能API系统需要设计约束'
    })

    assert len(result['constraints']) == 3
    assert generator.has_memory

    stats = generator.memory_manager.get_stats(generator.skill_id)
    assert stats['total_memories'] > 0

    print(f"  约束生成完成: {len(result['constraints'])} 个约束")
    print(f"  记忆数量: {stats['total_memories']}")
    print("✅ Constraint-Generator 记忆集成测试通过")


def test_skills_manager():
    """测试5: 技能记忆管理器"""
    print("\n### 测试5: Skills Memory Manager ###")

    manager = SkillsMemoryManager()

    # 创建多个带记忆的技能
    class MockSkill:
        def __init__(self, name):
            self.name = name

        def execute_skill(self, input_data):
            return {'result': f'{self.name} executed', 'data': input_data}

    # 注册技能
    task_decomposer = create_task_decomposer_with_memory(MockSkill('task-decomposer'), enable_memory=True)
    architect = create_architect_with_memory(MockSkill('architect'), enable_memory=True)

    manager.register_skill(task_decomposer)
    manager.register_skill(architect)

    # 列出技能
    skills = manager.list_skills()
    print(f"  注册技能数: {len(skills)}")

    for skill_info in skills:
        has_memory = "✅" if skill_info['has_memory'] else "❌"
        print(f"    {has_memory} {skill_info['skill_name']}")

    assert len(skills) == 2

    # 清理所有记忆
    cleanup_results = manager.cleanup_all_skills()
    print(f"\n  清理结果:")
    for skill_id, remaining in cleanup_results.items():
        print(f"    {skill_id}: {remaining} 条记忆保留")

    print("✅ Skills Memory Manager 测试通过")


def test_backward_compatibility():
    """测试6: 向后兼容性"""
    print("\n### 测试6: 向后兼容性 ###")

    class MockSkill:
        def __init__(self, name):
            self.name = name

        def execute_skill(self, input_data):
            return {'result': 'success', 'data': input_data}

    # 创建不启用记忆的技能
    skill = create_task_decomposer_with_memory(MockSkill('test'), enable_memory=False)

    # 执行任务
    result = skill.execute({'input': '测试任务'})

    # 验证基本功能正常
    assert result['result'] == 'success'
    assert not skill.has_memory

    # 验证记忆操作返回空
    history = skill.recall_similar_decompositions('测试')
    assert len(history) == 0

    print("  ✅ 不启用记忆时功能正常")
    print("  ✅ 记忆操作安全返回空列表")
    print("✅ 向后兼容性测试通过")


def test_memory_persistence():
    """测试7: 记忆持久化"""
    print("\n### 测试7: 记忆持久化 ###")

    class MockSkill:
        def __init__(self, name):
            self.name = name

        def execute_skill(self, input_data):
            return {
                'result': 'success',
                'subtasks': [{'id': '1'}, {'id': '2'}],
                'architecture_design': {'components': [{'name': 'Service1'}]},
                'quality_metrics': {'overall_quality': 0.9}
            }

    # 创建带记忆的技能
    task_decomposer = create_task_decomposer_with_memory(MockSkill('task'), enable_memory=True)
    architect = create_architect_with_memory(MockSkill('arch'), enable_memory=True)

    # 执行任务
    task_decomposer.execute({'input': '任务1'})
    task_decomposer.execute({'input': '任务2'})
    architect.execute({'input': '设计1'})

    # 导出所有记忆
    from tempfile import TemporaryDirectory
    import json

    with TemporaryDirectory() as tmpdir:
        manager = SkillsMemoryManager()
        manager.register_skill(task_decomposer)
        manager.register_skill(architect)

        all_memories = manager.export_all_memories(Path(tmpdir))

        print(f"  导出技能数: {len(all_memories)}")

        for skill_id, memory_data in all_memories.items():
            skill_name = memory_data['skill_name']
            stats = memory_data['stats']
            print(f"    {skill_name}: {stats['total_memories']} 条记忆")

            # 验证文件已创建
            export_file = Path(tmpdir) / f"{skill_name}_memory.json"
            assert export_file.exists()

            # 验证数据格式
            with open(export_file, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                assert 'skill_name' in loaded_data
                assert 'recent_memories' in loaded_data

    print("✅ 记忆持久化测试通过")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("DNASPEC 技能与记忆系统集成测试")
    print("=" * 60)

    try:
        test_task_decomposer_memory()
        test_architect_memory()
        test_modulizer_memory()
        test_constraint_generator_memory()
        test_skills_manager()
        test_backward_compatibility()
        test_memory_persistence()

        print("\n" + "=" * 60)
        print("✅ 所有技能记忆集成测试通过！")
        print("=" * 60)

        print("\n集成验证:")
        print("  1. ✅ Task-Decomposer 记忆集成")
        print("  2. ✅ Architect 记忆集成")
        print("  3. ✅ Modulizer 记忆集成")
        print("  4. ✅ Constraint-Generator 记忆集成")
        print("  5. ✅ Skills Memory Manager 统一管理")
        print("  6. ✅ 向后兼容 - 不启用记忆时正常工作")
        print("  7. ✅ 记忆持久化和导出")

        print("\n记忆增强特性:")
        print("  • 记住任务分解模式和复杂度")
        print("  • 记住架构设计风格和组件")
        print("  • 记住模块化策略")
        print("  • 记住约束生成模式")
        print("  • 支持检索历史经验")
        print("  • 统一管理多个技能记忆")

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
