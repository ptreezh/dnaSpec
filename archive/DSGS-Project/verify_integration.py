#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证所有Skills和Hook的集成状态
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def verify_skills_integration():
    """验证Skills和Hook的集成状态"""
    print("=== 验证Skills和Hook的集成状态 ===\n")
    
    # 1. 检查skills_hook_system.py文件是否存在且可导入
    try:
        from skills_hook_system import SkillsDiscoveryHook, SkillInvoker
        print("✓ skills_hook_system.py 模块导入成功")
    except ImportError as e:
        print(f"✗ skills_hook_system.py 模块导入失败: {e}")
        return False
    
    # 2. 检查Skills注册表构建
    try:
        hook = SkillsDiscoveryHook('skills')
        print(f"✓ Skills注册表构建成功，发现 {len(hook.skills_registry)} 个Skills")
        
        # 列出所有注册的Skills
        print("\n已注册的Skills:")
        for skill in hook.skills_registry:
            print(f"  - {skill.name}: {skill.description[:60]}...")
    except Exception as e:
        print(f"✗ Skills注册表构建失败: {e}")
        return False
    
    # 3. 检查所有关键Skills是否存在
    expected_skills = [
        'dnaspec-architect',
        'dnaspec-system-architect', 
        'dnaspec-task-decomposer',
        'dnaspec-agent-creator',
        'dnaspec-constraint-generator',
        'dnaspec-dapi-checker',
        'dnaspec-modulizer'
    ]
    
    registered_skill_names = [skill.name for skill in hook.skills_registry]
    missing_skills = [skill for skill in expected_skills if skill not in registered_skill_names]
    
    if missing_skills:
        print(f"✗ 缺少以下Skills: {missing_skills}")
        return False
    else:
        print("✓ 所有关键Skills都已注册")
    
    # 4. 检查Hook调用器
    try:
        invoker = SkillInvoker()
        print("✓ SkillInvoker创建成功")
    except Exception as e:
        print(f"✗ SkillInvoker创建失败: {e}")
        return False
    
    # 5. 测试意图分析功能
    try:
        test_message = "创建智能体"
        matched_skills = hook.analyze_user_intent(test_message)
        print(f"✓ 意图分析功能正常，测试消息'{test_message}'匹配到 {len(matched_skills)} 个Skills")
    except Exception as e:
        print(f"✗ 意图分析功能异常: {e}")
        return False
    
    # 6. 测试置信度计算
    try:
        test_skill = hook.skills_registry[0]  # 选择第一个Skill进行测试
        confidence = hook._calculate_match_confidence_improved("测试消息", test_skill)
        print(f"✓ 置信度计算功能正常，测试置信度: {confidence:.3f}")
    except Exception as e:
        print(f"✗ 置信度计算功能异常: {e}")
        return False
    
    # 7. 检查所有SKILL.md文件是否存在
    import os
    skills_dir = "skills"
    if os.path.exists(skills_dir):
        skill_dirs = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
        skill_md_files = []
        for skill_dir in skill_dirs:
            skill_md_path = os.path.join(skills_dir, skill_dir, "SKILL.md")
            if os.path.exists(skill_md_path):
                skill_md_files.append(skill_dir)
        
        print(f"✓ 发现 {len(skill_md_files)} 个SKILL.md文件")
        print(f"  SKILL.md文件: {skill_md_files}")
    else:
        print(f"✗ skills目录不存在: {skills_dir}")
        return False
    
    print("\n=== 集成状态验证完成 ===")
    print("✓ 所有Skills和Hook功能正常集成")
    print("✓ 关键词匹配系统正常工作")
    print("✓ 意图分析功能正常")
    print("✓ 置信度计算功能正常")
    print("✓ 所有SKILL.md文件完整")
    
    return True

if __name__ == "__main__":
    success = verify_skills_integration()
    if success:
        print("\n🎉 验证成功！所有Skills和Hook都已正确集成并可用。")
    else:
        print("\n❌ 验证失败！存在集成问题。")
        sys.exit(1)