#!/usr/bin/env python3
"""
诊断 uuid 错误问题
"""
import sys
sys.path.insert(0, 'D:/DAIP/dnaSpec')

print("="*60)
print("UUID 问题诊断")
print("="*60)

# 测试 1: 检查 uuid 模块
print("\n1. 测试 uuid 模块导入...")
try:
    import uuid
    print(f"   ✅ uuid 模块导入成功")
    print(f"   测试 uuid.uuid4(): {uuid.uuid4()}")
except Exception as e:
    print(f"   ❌ uuid 模块导入失败: {e}")

# 测试 2: 检查技能文件导入
print("\n2. 测试技能文件导入...")
skill_files = [
    'src.task_decomposer_skill',
    'src.agent_creator_skill',
    'src.constraint_generator_skill'
]

for skill_module in skill_files:
    try:
        module = __import__(skill_module, fromlist=[''])
        print(f"   ✅ {skill_module} 导入成功")
    except Exception as e:
        print(f"   ❌ {skill_module} 导入失败: {e}")

# 测试 3: 检查技能系统导入
print("\n3. 测试技能系统导入...")
try:
    from src.dna_context_engineering.skills_system_final import *
    print("   ✅ skills_system_final 导入成功")
except Exception as e:
    print(f"   ❌ skills_system_final 导入失败: {e}")

# 测试 4: 直接测试 SkillMapper
print("\n4. 测试 SkillMapper...")
try:
    from src.dna_spec_kit_integration.core.skill_mapper import SkillMapper
    mapper = SkillMapper()
    print(f"   ✅ SkillMapper 创建成功")

    # 测试映射
    skill_name = 'task-decomposer'
    mapped = mapper.map(skill_name)
    print(f"   映射 '{skill_name}' -> '{mapped}'")
except Exception as e:
    print(f"   ❌ SkillMapper 测试失败: {e}")

# 测试 5: 测试 PythonBridge
print("\n5. 测试 PythonBridge...")
try:
    from src.dna_spec_kit_integration.core.python_bridge import PythonBridge
    bridge = PythonBridge()
    print(f"   ✅ PythonBridge 创建成功")

    # 测试执行
    result = bridge.execute_skill('task_decomposer', '测试输入')
    print(f"   执行结果状态码: {result.get('statusCode')}")
    if result.get('statusCode') == 500:
        print(f"   错误信息: {result.get('body', '')[:200]}")
except Exception as e:
    print(f"   ❌ PythonBridge 测试失败: {e}")

# 测试 6: 检查实际使用的技能实现
print("\n6. 检查实际使用的技能实现...")
try:
    from src.dna_spec_kit_integration.core.skill_mapper import SkillMapper
    import os

    mapper = SkillMapper()

    # 检查技能文件路径
    skill_name = 'task_decomposer'
    dnaspec_skill_name = mapper.map(skill_name)
    print(f"   技能名称映射: {skill_name} -> {dnaspec_skill_name}")

    # 查找实际文件
    possible_paths = [
        f"src/{skill_name}_skill.py",
        f"claude_skills/{skill_name}_skill.py",
        f"skills/{skill_name}",
    ]

    for path in possible_paths:
        full_path = f"D:/DAIP/dnaSpec/{path}"
        if os.path.exists(full_path):
            print(f"   找到文件: {path}")
            # 检查是否有 uuid 导入
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                has_uuid_import = 'import uuid' in content
                has_uuid_usage = 'uuid.' in content
                print(f"     导入 uuid: {'是' if has_uuid_import else '否'}")
                print(f"     使用 uuid: {'是' if has_uuid_usage else '否'}")

except Exception as e:
    print(f"   ❌ 检查失败: {e}")

print("\n" + "="*60)
print("诊断完成")
print("="*60)
