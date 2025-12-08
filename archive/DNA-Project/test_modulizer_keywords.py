#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试modulizer新增关键词的匹配效果
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from skills_hook_system import SkillsDiscoveryHook

def test_modulizer_keywords():
    """测试modulizer新增关键词的匹配效果"""
    print("=== 测试modulizer新增关键词的匹配效果 ===\n")
    
    # 创建Skills发现Hook
    hook = SkillsDiscoveryHook('skills')
    
    # 找到dna-modulizer技能
    dnaspec_modulizer = None
    for skill in hook.skills_registry:
        if skill.name == 'dnaspec-modulizer':
            dnaspec_modulizer = skill
            break
    
    if dnaspec_modulizer:
        print(f"dnaspec-modulizer 关键词: {dnaspec_modulizer.keywords}")
        print()
        
        # 测试新增的关键词
        test_messages = [
            '隔离测试',
            '分区测试',
            '系统重构',
            '降低系统复杂度',
            '模块化测试',
            '组件隔离测试',
            '系统复杂度优化'
        ]
        
        for msg in test_messages:
            confidence = hook._calculate_match_confidence_improved(msg, dnaspec_modulizer)
            matched_keywords = [k for k in dnaspec_modulizer.keywords if k in msg.lower()]
            print(f'消息: "{msg}"')
            print(f'  置信度: {confidence:.3f}')
            print(f'  匹配关键词: {matched_keywords}')
            print()
    else:
        print("未找到 dnaspec-modulizer 技能")

if __name__ == "__main__":
    test_modulizer_keywords()