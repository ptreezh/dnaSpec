#!/usr/bin/env python3
import subprocess
import os

# 测试不同的方式来运行claude命令
print("测试各种运行方式:")

# 方式1：直接运行（当前失败的方式）
try:
    result = subprocess.run(['claude', '--version'], capture_output=True, text=True, timeout=10)
    print(f"1. 直接运行: 返回码={result.returncode}, 输出='{result.stdout.strip()}'")
except Exception as e:
    print(f"1. 直接运行异常: {e}")

# 方式2：使用shell=True
try:
    result = subprocess.run(['claude', '--version'], capture_output=True, text=True, timeout=10, shell=True)
    print(f"2. 使用shell=True: 返回码={result.returncode}, 输出='{result.stdout.strip()}'")
except Exception as e:
    print(f"2. 使用shell=True异常: {e}")

# 方式3：使用cmd /c
try:
    result = subprocess.run('cmd /c claude --version', capture_output=True, text=True, timeout=10)
    print(f"3. 使用cmd /c: 返回码={result.returncode}, 输出='{result.stdout.strip()}'")
except Exception as e:
    print(f"3. 使用cmd /c异常: {e}")

# 方式4：使用完整路径
try:
    result = subprocess.run(['C:\\npm_global\\claude.cmd', '--version'], capture_output=True, text=True, timeout=10)
    print(f"4. 使用完整路径: 返回码={result.returncode}, 输出='{result.stdout.strip()}'")
except Exception as e:
    print(f"4. 使用完整路径异常: {e}")

# 方式5：使用完整路径并带shell=True
try:
    result = subprocess.run(['C:\\npm_global\\claude.cmd', '--version'], capture_output=True, text=True, timeout=10, shell=True)
    print(f"5. 完整路径+shell=True: 返回码={result.returncode}, 输出='{result.stdout.strip()}'")
except Exception as e:
    print(f"5. 完整路径+shell=True异常: {e}")