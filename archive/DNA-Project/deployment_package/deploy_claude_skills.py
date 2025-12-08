#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Code Skills集成验证和部署脚本
"""

import os
import shutil
import sys
from pathlib import Path

def verify_claude_skills():
    """验证Claude Skills导出"""
    print("=== 验证Claude Code Skills导出 ===\n")
    
    export_path = "exports/claude_code_skills"
    if not os.path.exists(export_path):
        print("✗ Claude Skills导出目录不存在")
        return False
    
    # 检查所有技能目录
    skill_dirs = [d for d in os.listdir(export_path) if os.path.isdir(os.path.join(export_path, d))]
    expected_skills = [
        'dnaspec-agent-creator',
        'dnaspec-architect',
        'dnaspec-constraint-generator',
        'dnaspec-dapi-checker',
        'dnaspec-modulizer',
        'dnaspec-system-architect',
        'dnaspec-task-decomposer'
    ]
    
    print(f"发现 {len(skill_dirs)} 个Skills:")
    missing_skills = []
    for expected_skill in expected_skills:
        if expected_skill in skill_dirs:
            print(f"  ✓ {expected_skill}")
        else:
            print(f"  ✗ {expected_skill} (缺失)")
            missing_skills.append(expected_skill)
    
    if missing_skills:
        print(f"\n✗ 缺失 {len(missing_skills)} 个Skills: {missing_skills}")
        return False
    
    # 检查每个技能的SKILL.md文件
    print("\n验证SKILL.md文件:")
    for skill_dir in skill_dirs:
        skill_md_path = os.path.join(export_path, skill_dir, "SKILL.md")
        if os.path.exists(skill_md_path):
            # 检查文件内容
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if content.startswith('---') and 'name:' in content and 'description:' in content:
                print(f"  ✓ {skill_dir}/SKILL.md 格式正确")
            else:
                print(f"  ✗ {skill_dir}/SKILL.md 格式错误")
                return False
        else:
            print(f"  ✗ {skill_dir}/SKILL.md 文件缺失")
            return False
    
    print("\n✓ 所有Claude Skills验证通过")
    return True

def deploy_to_claude_code(target_path=None):
    """部署到Claude Code"""
    print("\n=== 部署到Claude Code ===\n")
    
    # 默认Claude Skills路径
    if target_path is None:
        # Windows路径
        if os.name == 'nt':
            target_path = os.path.expanduser("~/.config/claude/skills")
        else:
            # Unix/Linux/Mac路径
            target_path = os.path.expanduser("~/.config/claude/skills")
    
    print(f"目标路径: {target_path}")
    
    # 创建目标目录
    os.makedirs(target_path, exist_ok=True)
    print(f"✓ 确保目标目录存在: {target_path}")
    
    # 复制所有Skills
    source_path = "exports/claude_code_skills"
    skill_dirs = [d for d in os.listdir(source_path) if os.path.isdir(os.path.join(source_path, d))]
    
    print(f"\n开始部署 {len(skill_dirs)} 个Skills:")
    deployed_count = 0
    
    for skill_dir in skill_dirs:
        source_skill_path = os.path.join(source_path, skill_dir)
        target_skill_path = os.path.join(target_path, skill_dir)
        
        try:
            # 如果目标已存在，先删除
            if os.path.exists(target_skill_path):
                shutil.rmtree(target_skill_path)
                print(f"  更新 {skill_dir}")
            else:
                print(f"  部署 {skill_dir}")
            
            # 复制整个技能目录
            shutil.copytree(source_skill_path, target_skill_path)
            deployed_count += 1
            
        except Exception as e:
            print(f"  ✗ 部署 {skill_dir} 失败: {e}")
            return False
    
    print(f"\n✓ 成功部署 {deployed_count} 个Skills到 {target_path}")
    return True

def create_integration_test_script():
    """创建集成测试脚本"""
    print("\n=== 创建集成测试脚本 ===\n")
    
    test_script_content = '''#!/usr/bin/env python3
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
        'dnaspec-agent-creator',
        'dnaspec-architect',
        'dnaspec-constraint-generator',
        'dnaspec-dapi-checker',
        'dnaspec-modulizer',
        'dnaspec-system-architect',
        'dnaspec-task-decomposer'
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
        ("创建一个智能体", "dnaspec-agent-creator"),
        ("分解复杂任务", "dnaspec-task-decomposer"),
        ("生成系统约束", "dnaspec-constraint-generator"),
        ("检查接口一致性", "dnaspec-dapi-checker"),
        ("模块化重构", "dnaspec-modulizer")
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
'''
    
    with open("test_claude_integration.py", 'w', encoding='utf-8') as f:
        f.write(test_script_content)
    
    print("✓ 创建集成测试脚本: test_claude_integration.py")
    return True

def main():
    """主函数"""
    print("=== Claude Code Skills集成部署 ===\n")
    
    # 1. 验证Skills导出
    if not verify_claude_skills():
        print("\n✗ Skills验证失败，无法继续部署")
        return 1
    
    # 2. 部署到Claude Code
    if not deploy_to_claude_code():
        print("\n✗ Skills部署失败")
        return 1
    
    # 3. 创建测试脚本
    if not create_integration_test_script():
        print("\n✗ 测试脚本创建失败")
        return 1
    
    print("\n=== 部署完成 ===")
    print("✓ 所有DNASPEC Skills已成功部署到Claude Code")
    print("✓ 集成测试脚本已创建: test_claude_integration.py")
    print("\n下一步操作:")
    print("1. 在Claude Code中启用Skills功能")
    print("2. 运行 'python test_claude_integration.py' 进行验证")
    print("3. 手动测试Skill调用功能")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())