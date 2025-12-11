#!/usr/bin/env python3
"""
Test script for DNASPEC advanced skills
"""
import sys
import os
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from skills.skill_manager import SkillManager


def test_advanced_skills():
    """Test advanced DNASPEC skills"""
    print("Testing DNASPEC advanced skills...")
    print("=" * 50)
    
    # Create skill manager
    skill_manager = SkillManager()
    
    # Test system architect skill
    print("\n1. Testing System Architect Skill:")
    test_requirements = "构建一个电商平台，需要支持用户注册登录、商品浏览、购物车、订单处理、支付功能。要求系统具有高可用性和可扩展性。"
    result = skill_manager.execute_skill("system-architect", {
        "input": test_requirements,
        "detail_level": "standard"
    })
    if 'data' in result:
        print(f"   Architecture Type: {result['data'].get('architecture_type', 'N/A')}")
        print(f"   Recommended Tech Stack: {result['data'].get('recommended_tech_stack', 'N/A')}")
        if 'identified_modules' in result['data']:
            print(f"   Number of Modules: {len(result['data']['identified_modules'])}")
    
    # Test git operations skill
    print("\n2. Testing Git Operations Skill:")
    result = skill_manager.execute_skill("git-operations", {
        "input": "",
        "detail_level": "standard",
        "options": {
            "operation": "status"
        }
    })
    if 'data' in result:
        print(f"   Operation: {result['data'].get('operation', 'N/A')}")
        print(f"   Success: {result['data'].get('success', 'N/A')}")
    
    # Test temp workspace skill
    print("\n3. Testing Temp Workspace Skill:")
    result = skill_manager.execute_skill("temp-workspace", {
        "input": "",
        "detail_level": "standard",
        "options": {
            "operation": "get-workspace-path"
        }
    })
    if 'data' in result:
        print(f"   Operation: {result['data'].get('operation', 'N/A')}")
        print(f"   Result: {result['data'].get('result', 'N/A')[:50]}...")
    
    print("\n✅ Advanced skills test completed!")


if __name__ == "__main__":
    test_advanced_skills()