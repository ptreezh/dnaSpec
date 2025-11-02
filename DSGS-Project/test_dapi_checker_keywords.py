#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试dapi-checker新增关键词的匹配效果
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from skills_hook_system import SkillsDiscoveryHook

def test_dapi_checker_keywords():
    """测试dapi-checker新增关键词的匹配效果"""
    print("=== 测试dapi-checker新增关键词的匹配效果 ===\n")
    
    # 创建Skills发现Hook
    hook = SkillsDiscoveryHook('skills')
    
    # 找到dsgs-dapi-checker技能
    dsgs_dapi_checker = None
    for skill in hook.skills_registry:
        if skill.name == 'dsgs-dapi-checker':
            dsgs_dapi_checker = skill
            break
    
    if dsgs_dapi_checker:
        print(f"dsgs-dapi-checker 关键词: {dsgs_dapi_checker.keywords}")
        print()
        
        # 测试新增的关键词
        test_messages = [
            '接口不一致',
            '参数不一致',
            '定义不一致',
            '参数不匹配',
            '接口不匹配',
            '参数错误',
            '接口错误',
            '检查接口不一致',
            '验证参数不匹配',
            '验证接口一致性'
        ]
        
        for msg in test_messages:
            confidence = hook._calculate_match_confidence_improved(msg, dsgs_dapi_checker)
            matched_keywords = [k for k in dsgs_dapi_checker.keywords if k in msg.lower()]
            print(f'消息: "{msg}"')
            print(f'  置信度: {confidence:.3f}')
            print(f'  匹配关键词: {matched_keywords}')
            print()
    else:
        print("未找到 dsgs-dapi-checker 技能")

if __name__ == "__main__":
    test_dapi_checker_keywords()