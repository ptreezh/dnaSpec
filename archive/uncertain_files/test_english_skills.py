#!/usr/bin/env python3
"""
Test script for English versions of DNASPEC skills
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from skills.skill_manager_en import SkillManager


def test_english_skills():
    """Test English versions of skills"""
    print("Testing English versions of DNASPEC skills...")
    print("=" * 50)
    
    # Create skill manager with English language
    skill_manager = SkillManager()
    
    # Test liveness skill
    print("\n1. Testing Liveness Skill:")
    result = skill_manager.execute_skill("liveness", {"input": "test"})
    print(f"   Result: {result}")
    
    # Test context analysis skill
    print("\n2. Testing Context Analysis Skill:")
    test_context = "Design a user authentication system with login, registration, and password reset functionality."
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
    print("\n3. Testing Context Optimization Skill:")
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
    print("\n4. Testing Cognitive Template Skill:")
    result = skill_manager.execute_skill("cognitive-template", {
        "input": "How to optimize database queries?",
        "detail_level": "standard",
        "options": {
            "template": "chain-of-thought"
        }
    })
    if 'data' in result:
        print(f"   Template Type: {result['data'].get('template_type', 'N/A')}")
        print(f"   Template Name: {result['data'].get('template_name', 'N/A')}")
    
    # List all skills
    print("\n5. Available Skills:")
    skills = skill_manager.list_skills()
    for skill in skills:
        print(f"   - {skill}")
    
    print("\n✅ English skills test completed!")


if __name__ == "__main__":
    test_english_skills()