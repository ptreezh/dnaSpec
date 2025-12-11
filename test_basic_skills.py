#!/usr/bin/env python3
"""
Test script for DNASPEC skills
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from skills.skill_manager import SkillManager


def test_basic_skills():
    """Test basic DNASPEC skills"""
    print("Testing DNASPEC skills...")
    print("=" * 50)
    
    # Create skill manager
    skill_manager = SkillManager()
    
    # List all skills
    print("\n1. Available Skills:")
    skills = skill_manager.list_skills()
    for skill in skills:
        print(f"   - {skill}")
    
    # Test liveness skill
    print("\n2. Testing Liveness Skill:")
    result = skill_manager.execute_skill("liveness", {"input": "test"})
    print(f"   Result: {result}")
    
    # Test simple architect skill
    print("\n3. Testing Simple Architect Skill:")
    result = skill_manager.execute_skill("simple-architect", {"input": "电商系统"})
    print(f"   Result: {result}")
    
    print("\n✅ Basic skills test completed!")


if __name__ == "__main__":
    test_basic_skills()