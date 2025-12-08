#!/usr/bin/env python3
"""
验证新集成命令功能的工作脚本
"""
import subprocess
import os
import sys

def test_new_integrate_command():
    print("Testing new integrate command functionality...")
    print("="*60)
    
    # 测试列表功能
    print("1. Testing 'dnaspec integrate --list':")
    result = subprocess.run([
        sys.executable, '-c', 
        '''
from src.dnaspec_spec_kit_integration.cli import main
import sys
sys.argv = ['dnaspec', 'integrate', '--list']
main()
        '''
    ], cwd=os.getcwd(), capture_output=True, text=True, timeout=30)
    
    print(f"Return code: {result.returncode}")
    if result.stdout:
        print(f"Stdout: {result.stdout[:500]}...")
    if result.stderr:
        print(f"Stderr: {result.stderr[:200]}...")
    
    print()
    
    # 测试不带参数的integrate（应该运行完整集成流程）
    print("2. Testing 'dnaspec integrate' (full integration):")
    result = subprocess.run([
        sys.executable, '-c', 
        '''
from src.dnaspec_spec_kit_integration.cli import main
import sys
sys.argv = ['dnaspec', 'integrate']
main()
        '''
    ], cwd=os.getcwd(), capture_output=True, text=True, timeout=45)
    
    print(f"Return code: {result.returncode}")
    if result.stdout:
        print("Stdout:", result.stdout[:500], "..." if len(result.stdout) > 500 else "")
    if result.stderr:
        print("Stderr:", result.stderr[:200], "..." if len(result.stderr) > 200 else "")

if __name__ == "__main__":
    test_new_integrate_command()