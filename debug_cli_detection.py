#!/usr/bin/env python3
import subprocess
import os
import shutil

print('当前系统PATH的部分内容:')
path_parts = os.environ.get('PATH', '').split(';')
for i, part in enumerate(path_parts[:10]):  # 只显示前10个路径
    print(f'  {i+1}. {part}')

print()
print('查找claude命令:')
full_path = shutil.which('claude')
print(f'完整路径: {full_path}')

print()
print('测试运行claude命令:')
try:
    # 直接运行claude --version
    result = subprocess.run(['claude', '--version'], capture_output=True, text=True, timeout=15)
    print(f'返回码: {result.returncode}')
    print(f'标准输出: {repr(result.stdout)}')
    print(f'标准错误: {repr(result.stderr)}')
    
    if result.returncode == 0:
        print("命令执行成功！")
    else:
        print("命令执行失败")
except subprocess.TimeoutExpired:
    print("命令超时")
except FileNotFoundError as e:
    print(f"文件未找到错误: {e}")
except Exception as e:
    print(f"其他异常: {e}")

print()
print('测试使用完整路径:')
if full_path:
    try:
        result = subprocess.run([full_path, '--version'], capture_output=True, text=True, timeout=15)
        print(f'返回码: {result.returncode}')
        print(f'输出: {repr(result.stdout)}')
        print(f'错误: {repr(result.stderr)}')
    except Exception as e:
        print(f'完整路径执行异常: {e}')