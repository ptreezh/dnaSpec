#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试task-decomposer新增关键词的匹配效果
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from skills_hook_system import SkillsDiscoveryHook

def test_task_decomposer_keywords():
    """测试task-decomposer新增关键词的匹配效果"""
    print("=== 测试task-decomposer新增关键词的匹配效果 ===\n")
    
    # 创建Skills发现Hook
    hook = SkillsDiscoveryHook('skills')
    
    # 找到dsgs-task-decomposer技能
    dsgs_task_decomposer = None
    for skill in hook.skills_registry:
        if skill.name == 'dsgs-task-decomposer':
            dsgs_task_decomposer = skill
            break
    
    if dsgs_task_decomposer:
        print(f"dsgs-task-decomposer 关键词: {dsgs_task_decomposer.keywords}")
        print()
        
        # 测试新增的关键词
        test_messages = [
            '复杂任务',
            '一步步拆解',
            '任务分析',
            '任务清单',
            '任务计划',
            '分解复杂任务',
            '一步步分析任务',
            '制定任务清单',
            '任务分解计划'
        ]
        
        for msg in test_messages:
            confidence = hook._calculate_match_confidence_improved(msg, dsgs_task_decomposer)
            matched_keywords = [k for k in dsgs_task_decomposer.keywords if k in msg.lower()]
            print(f'消息: "{msg}"')
            print(f'  置信度: {confidence:.3f}')
            print(f'  匹配关键词: {matched_keywords}')
            print()
    else:
        print("未找到 dsgs-task-decomposer 技能")

if __name__ == "__main__":
    test_task_decomposer_keywords()