#!/usr/bin/env python3
"""
DNASPEC Context Engineering Skills - 最终英文版验证
确认所有输出均为英文ANSI字符
"""
import subprocess
import sys
import os

def test_english_output():
    """
    测试英文输出是否正常
    """
    print("Testing English Output for DNASPEC Context Engineering Skills")
    print("="*60)
    
    # 测试list命令
    print("\\n1. Testing 'dnaspec list' command:")
    try:
        result = subprocess.run(['dnaspec', 'list'], capture_output=True, text=True, timeout=30)
        print("STDOUT:", result.stdout[:500])
        if result.stderr:
            print("STDERR:", result.stderr[:200])
        print(f"Return code: {result.returncode}")
    except Exception as e:
        print(f"Error: {e}")
    
    # 测试analyze命令
    print("\\n2. Testing 'dnaspec analyze' command:")
    try:
        # 直接调用Python模块测试
        from src.dnaspec_context_engineering.skills_system_final import execute
        result = execute({
            'skill': 'context-analysis',
            'context': 'Test context analysis functionality',
            'params': {}
        })
        print("Analysis result:", result[:500] if result else "None")
    except Exception as e:
        print(f"Error calling analysis skill: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_english_output()