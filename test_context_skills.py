#!/usr/bin/env python3
"""
Test script for DNASPEC context engineering skills
"""
import sys
import os
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from skills.skill_manager import SkillManager


def test_context_engineering_skills():
    """Test context engineering DNASPEC skills"""
    print("Testing DNASPEC context engineering skills...")
    print("=" * 50)
    
    # Create skill manager
    skill_manager = SkillManager()
    
    # Test context analysis skill
    print("\n1. Testing Context Analysis Skill:")
    test_context = "设计一个用户认证系统，需要支持用户名密码登录、邮箱验证、密码找回功能。系统需要保证安全性，防止暴力破解和SQL注入攻击。"
    result = skill_manager.execute_skill("context-analysis", {
        "input": test_context,
        "detail_level": "standard"
    })
    print(f"   Overall Score: {result.get('data', {}).get('overall_score', 'N/A')}")
    if 'data' in result and 'metrics' in result['data']:
        print("   Metrics:")
        for metric, score in result['data']['metrics'].items():
            print(f"     {metric}: {score}")
    
    # Test context optimization skill
    print("\n2. Testing Context Optimization Skill:")
    result = skill_manager.execute_skill("context-optimization", {
        "input": test_context,
        "detail_level": "standard",
        "options": {
            "optimization_goals": ["clarity", "completeness"]
        }
    })
    if 'data' in result:
        print(f"   Original Length: {result['data'].get('original_length', 'N/A')} characters")
        print(f"   Optimized Length: {result['data'].get('optimized_length', 'N/A')} characters")
        if result['data'].get('applied_optimizations'):
            print("   Applied Optimizations:")
            for opt in result['data']['applied_optimizations'][:3]:  # Show first 3
                print(f"     - {opt}")
    
    # Test cognitive template skill
    print("\n3. Testing Cognitive Template Skill:")
    result = skill_manager.execute_skill("cognitive-template", {
        "input": "如何设计安全的用户认证系统？",
        "detail_level": "standard",
        "options": {
            "template": "chain-of-thought"
        }
    })
    if 'data' in result:
        print(f"   Template Type: {result['data'].get('template_type', 'N/A')}")
        print(f"   Template Name: {result['data'].get('template_name', 'N/A')}")
        if 'applied_template' in result['data']:
            print("   Applied Template Preview:")
            template_preview = result['data']['applied_template'][:200] + "..." if len(result['data']['applied_template']) > 200 else result['data']['applied_template']
            print(f"     {template_preview}")
    
    print("\n✅ Context engineering skills test completed!")


if __name__ == "__main__":
    test_context_engineering_skills()