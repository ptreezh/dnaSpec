#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNASPEC Gemini CLI Extensions 主入口
"""

import sys
import os
import json
from typing import Optional

# 添加项目路径到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gemini_skills_core import get_skill_manager
from gemini_intelligent_matcher import get_intelligent_matcher
from gemini_hook_handler import get_hook_handler

def main():
    """主函数"""
    print("=== DNASPEC Gemini CLI Extensions ===")
    print("DSGS智能架构师系统已加载")
    print()
    
    # 显示可用技能
    skill_manager = get_skill_manager()
    skills = skill_manager.list_skills()
    
    print(f"可用技能 ({len(skills)} 个):")
    for skill in skills:
        print(f"  • {skill.name} - {skill.description}")
    print()
    
    # 显示使用说明
    print("使用说明:")
    print("1. 在Gemini CLI中直接输入自然语言请求")
    print("2. 系统将自动匹配并执行相应的DSGS技能")
    print("3. 支持的技能包括:")
    print("   - 智能体创建 (dnaspec-agent-creator)")
    print("   - 任务分解 (dnaspec-task-decomposer)")
    print("   - 接口检查 (dnaspec-dapi-checker)")
    print("   - 模块化 (dnaspec-modulizer)")
    print("   - 架构设计 (dnaspec-architect)")
    print()
    
    # 测试模式
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    elif len(sys.argv) > 1:
        # 处理命令行输入
        user_input = " ".join(sys.argv[1:])
        process_input(user_input)

def process_input(user_input: str):
    """处理用户输入"""
    print(f"处理输入: {user_input}")
    
    # 使用Hook处理器处理
    hook_handler = get_hook_handler()
    result = hook_handler.process_hook(user_input)
    
    if result:
        print("处理结果:")
        print(result)
    else:
        print("未匹配到合适的技能，将由原始Gemini CLI处理")

def run_tests():
    """运行测试"""
    print("运行DSGS技能匹配测试...")
    
    test_cases = [
        "创建一个项目管理智能体",
        "分解复杂的软件开发任务",
        "检查API接口一致性",
        "对系统进行模块化重构",
        "设计系统架构",
        "生成智能体角色定义",
        "验证接口参数不一致问题",
        "执行模块成熟度检查",
        "分析复杂任务的依赖关系"
    ]
    
    hook_handler = get_hook_handler()
    hook_handler.enable_debug()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {test_case}")
        result = hook_handler.process_hook(test_case)
        if result:
            print(f"结果: {result[:200]}..." if len(result) > 200 else f"结果: {result}")
        else:
            print("未匹配到技能")

if __name__ == "__main__":
    main()