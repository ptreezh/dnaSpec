#!/usr/bin/env python3
"""
测试独立环境下的执行器
"""
import subprocess
import tempfile
import sys
from pathlib import Path

def test_isolated_executor():
    """在隔离环境中测试执行器"""

    # 创建最小化的测试脚本，只使用系统路径
    test_script = '''# -*- coding: utf-8 -*-
import sys
# Clean paths, only keep necessary system paths
sys.path = [p for p in sys.path if not any(exclude in p.lower() for exclude in ['dna', 'src', 'temp'])]

print("=== Clean Python paths ===")
for i, path in enumerate(sys.path[:5]):
    print(f"  {i}: {path}")

print("\\n=== Testing DNASPEC import ===")
try:
    from dna_context_engineering.skills_system_final import execute_architect
    print("SUCCESS: DNASPEC imported successfully")

    result = execute_architect("Test task")
    print(f"SUCCESS: Execution result: {result[:100]}")
except ImportError as e:
    print(f"FAILED: Import error: {e}")
except Exception as e:
    print(f"FAILED: Execution error: {e}")
'''

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_script)
        script_path = f.name

    try:
        # 运行隔离测试
        result = subprocess.run([
            sys.executable, script_path
        ], capture_output=True, text=True, cwd=tempfile.gettempdir())

        print('=== Isolated test results ===')
        print(f'Return code: {result.returncode}')
        print(f'Output:\n{result.stdout}')
        if result.stderr:
            print(f'Stderr:\n{result.stderr}')

    finally:
        import os
        try:
            os.unlink(script_path)
        except:
            pass

if __name__ == '__main__':
    test_isolated_executor()