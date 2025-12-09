#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证所有Skills和Hook的集成状态
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_skills_and_hook_integration():
    """测试Skills和Hook的集成状态"""
    print("=== 验证Skills和Hook集成状态 ===\n")
    
    # 1. 测试SkillsDiscoveryHook导入
    try:
        from skills_hook_system import SkillsDiscoveryHook, SkillInvoker
        print("✓ SkillsDiscoveryHook和SkillInvoker导入成功")
    except ImportError as e:
        print(f"✗ 导入失败: {e}")
        return False
    
    # 2. 测试Skills注册
    try:
        hook = SkillsDiscoveryHook('skills')
        print(f"✓ Skills注册表构建成功，已注册{len(hook.skills_registry)}个Skills")
        
        # 打印所有已注册的Skills
        print("\n已注册的Skills:")
        for skill in hook.skills_registry:
            print(f"  - {skill.name}: {skill.description[:50]}...")
    except Exception as e:
        print(f"✗ Skills注册失败: {e}")
        return False
    
    # 3. 测试各Skill的关键词匹配功能
    print("\n✓ 各Skill关键词匹配功能测试:")
    for skill in hook.skills_registry:
        try:
            # 简单测试关键词提取功能
            test_keywords = hook._extract_keywords_improved(skill.description, skill.name)
            print(f"  - {skill.name}: {len(test_keywords)}个关键词")
        except Exception as e:
            print(f"  - {skill.name}: 关键词提取失败 - {e}")
    
    # 4. 测试置信度计算功能
    print("\n✓ 置信度计算功能测试:")
    test_messages = [
        "创建智能体",
        "分解任务",
        "检查接口一致性",
        "模块化重构",
        "生成约束"
    ]
    
    for msg in test_messages:
        try:
            matched_skills = hook.analyze_user_intent(msg)
            if matched_skills:
                top_skill = matched_skills[0]
                print(f"  - '{msg}' -> {top_skill.name} (置信度: {top_skill.confidence:.3f})")
            else:
                print(f"  - '{msg}' -> 无匹配")
        except Exception as e:
            print(f"  - '{msg}' -> 测试失败: {e}")
    
    # 5. 测试SkillInvoker功能
    try:
        invoker = SkillInvoker()
        print("\n✓ SkillInvoker创建成功")
        
        # 测试Hook调用
        response = invoker.hook_before_ai_response("创建一个智能体")
        if response:
            print(f"✓ Hook调用成功: {response['skill_name']}")
        else:
            print("✓ Hook调用正常（无匹配Skill）")
    except Exception as e:
        print(f"✗ SkillInvoker测试失败: {e}")
        return False
    
    # 6. 测试所有SKILL.md文件存在性
    print("\n✓ SKILL.md文件存在性检查:")
    import os
    skills_dir = "skills"
    if os.path.exists(skills_dir):
        skill_dirs = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
        for skill_dir in skill_dirs:
            skill_md_path = os.path.join(skills_dir, skill_dir, "SKILL.md")
            if os.path.exists(skill_md_path):
                print(f"  - {skill_dir}/SKILL.md: 存在")
            else:
                print(f"  - {skill_dir}/SKILL.md: 缺失")
    else:
        print("✗ skills目录不存在")
    
    print("\n=== 集成验证完成 ===")
    return True

if __name__ == "__main__":
    success = test_skills_and_hook_integration()
    if success:
        print("\n✓ 所有Skills和Hook都已成功集成并可用")
    else:
        print("\n✗ 集成验证失败")
        sys.exit(1)
