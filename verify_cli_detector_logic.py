#!/usr/bin/env python3
"""
验证CLI检测器的核心逻辑
"""
import subprocess
import shutil
import platform

print('🔍 测试CLI检测器的核心逻辑...')

# 测试系统PATH中是否存在AI工具
ai_tools = ['claude', 'qwen', 'gemini', 'cursor']

for tool in ai_tools:
    print(f'\n--- 测试 {tool} ---')
    
    # 1. 测试shutil.which方法
    tool_path = shutil.which(tool)
    print(f'shutil.which结果: {tool_path}')
    
    # 2. 测试subprocess运行
    try:
        result = subprocess.run(
            [tool, '--version'],
            capture_output=True,
            text=True,
            timeout=15,
            shell=(platform.system() == 'Windows')
        )
        print(f'subprocess.returncode: {result.returncode}')
        print(f'subprocess.stdout: {result.stdout.strip()}')
        if result.stderr.strip():
            print(f'subprocess.stderr: {result.stderr.strip()}')
        
        if result.returncode == 0:
            print(f'✅ {tool} 可检测到并正常运行')
        else:
            print(f'❌ {tool} 命令执行失败')
            
    except subprocess.TimeoutExpired:
        print(f'❌ {tool} 命令超时')
    except FileNotFoundError:
        print(f'❌ {tool} 未在系统PATH中找到')
    except Exception as e:
        print(f'❌ {tool} 检测异常: {e}')

print('\n📋 检测器实现逻辑总结:')
print('1. 使用shutil.which()确认工具在系统PATH中')
print('2. 使用subprocess.run()执行具体命令验证工具功能')
print('3. Windows环境下使用shell=True处理.cmd/.bat脚本')
print('4. 设置足够超时时间避免网络延迟影响')
print('5. 分级错误处理，返回详细错误信息')