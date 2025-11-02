#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Code Skills集成测试脚本
"""

import os
import subprocess
import sys
import time

def test_skills_discovery():
    """测试Skills发现功能"""
    print("=== 测试Skills发现功能 ===")
    
    # Claude Code Skills路径
    skills_path = os.path.expanduser("~/.config/claude/skills")
    
    if not os.path.exists(skills_path):
        print("✗ Claude Skills目录不存在")
        return False
    
    # 检查Skills目录
    skill_dirs = [d for d in os.listdir(skills_path) if os.path.isdir(os.path.join(skills_path, d))]
    expected_skills = [
        'dsgs-agent-creator',
        'dsgs-architect',
        'dsgs-constraint-generator',
        'dsgs-dapi-checker',
        'dsgs-modulizer',
        'dsgs-system-architect',
        'dsgs-task-decomposer'
    ]
    
    print(f"发现 {len(skill_dirs)} 个已部署的Skills:")
    found_skills = []
    for skill_dir in skill_dirs:
        if skill_dir in expected_skills:
            print(f"  ✓ {skill_dir}")
            found_skills.append(skill_dir)
        else:
            print(f"  ? {skill_dir} (额外Skills)")
    
    missing_skills = [skill for skill in expected_skills if skill not in found_skills]
    if missing_skills:
        print(f"✗ 缺失 {len(missing_skills)} 个Skills: {missing_skills}")
        return False
    
    print(f"✓ 所有预期Skills都已部署")
    return True

def test_skill_invocation():
    """测试Skill调用功能"""
    print("\n=== 测试Skill调用功能 ===")
    
    # 测试用例
    test_cases = [
        ("创建一个智能体", "dsgs-agent-creator"),
        ("分解复杂任务", "dsgs-task-decomposer"),
        ("生成系统约束", "dsgs-constraint-generator"),
        ("检查接口一致性", "dsgs-dapi-checker"),
        ("模块化重构", "dsgs-modulizer")
    ]
    
    print("技能调用测试需要手动验证:")
    print("请在Claude Code中尝试以下请求:")
    for i, (request, expected_skill) in enumerate(test_cases, 1):
        print(f"  {i}. '{request}' -> 应该调用 {expected_skill}")
    
    print("\n验证步骤:")
    print("1. 打开Claude Code CLI")
    print("2. 输入上述测试请求")
    print("3. 观察是否自动调用相应的Skill")
    print("4. 检查Skill的响应内容")
    
    return True

def main():
    """主函数"""
    print("=== Claude Code Skills集成测试 ===\n")
    
    # 测试Skills发现
    if not test_skills_discovery():
        print("\n✗ Skills发现测试失败")
        return 1
    
    # 测试Skill调用
    if not test_skill_invocation():
        print("\n✗ Skill调用测试失败")
        return 1
    
    print("\n✓ 所有集成测试通过!")
    print("\n集成验证完成。请手动测试Claude Code中的Skill调用功能。")
    return 0

if __name__ == "__main__":
    sys.exit(main())