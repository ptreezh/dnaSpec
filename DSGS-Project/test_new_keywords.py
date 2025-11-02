#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新增关键词的匹配效果
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from skills_hook_system import SkillsDiscoveryHook

def test_new_keywords():
    """测试新增关键词的匹配效果"""
    print("=== 测试新增关键词的匹配效果 ===\n")
    
    # 创建Skills发现Hook
    hook = SkillsDiscoveryHook('skills')
    
    # 找到dsgs-agent-creator技能
    dsgs_agent_creator = None
    for skill in hook.skills_registry:
        if skill.name == 'dsgs-agent-creator':
            dsgs_agent_creator = skill
            break
    
    if dsgs_agent_creator:
        print(f"dsgs-agent-creator 关键词: {dsgs_agent_creator.keywords}")
        print()
        
        # 测试新增的关键词
        test_messages = [
            '模块智能化',
            'agentic',
            '具身认知',
            '模块自主智能',
            '增加模块自主智能',
            '创建智能体',
            '设计模块化智能系统',
            '实现具身智能体'
        ]
        
        for msg in test_messages:
            confidence = hook._calculate_match_confidence_improved(msg, dsgs_agent_creator)
            matched_keywords = [k for k in dsgs_agent_creator.keywords if k in msg.lower()]
            print(f'消息: "{msg}"')
            print(f'  置信度: {confidence:.3f}')
            print(f'  匹配关键词: {matched_keywords}')
            print()
    else:
        print("未找到 dsgs-agent-creator 技能")

if __name__ == "__main__":
    test_new_keywords()