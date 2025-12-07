#!/usr/bin/env python3
"""
真实环境CLI工具检测测试
用于验证检测逻辑是否真实有效
"""
import subprocess
import platform
import shutil
import os

def test_detection_methods():
    """测试不同的检测方法"""
    print("真实环境CLI工具检测测试")
    print("="*50)
    
    tools = ['claude', 'qwen', 'gemini', 'cursor', 'gh']
    
    for tool in tools:
        print(f"\n测试工具: {tool}")
        print("-" * 30)
        
        # 方法1: shutil.which
        print("方法1 - shutil.which:")
        path_result = shutil.which(tool)
        print(f"  路径: {path_result}")
        
        if path_result:
            # 方法2: 直接执行
            print("方法2 - 直接执行version命令:")
            try:
                result = subprocess.run(
                    [tool, '--version'],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    shell=(platform.system() == 'Windows'),
                    env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}
                )
                print(f"  执行结果: 退出码={result.returncode}")
                print(f"  标准输出: {result.stdout.strip()}")
                if result.stderr.strip():
                    print(f"  标准错误: {result.stderr.strip()}")
            except subprocess.TimeoutExpired:
                print("  执行结果: 超时")
            except Exception as e:
                print(f"  执行结果: 异常 - {e}")
            
            # 方法3: 使用完整路径执行
            print("方法3 - 使用完整路径执行:")
            try:
                result = subprocess.run(
                    [path_result, '--version'],
                    capture_output=True,
                    text=True,
                    timeout=15,  # 较长超时
                    env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}
                )
                print(f"  执行结果: 退出码={result.returncode}")
                print(f"  标准输出: {result.stdout.strip()}")
                if result.stderr.strip():
                    print(f"  标准错误: {result.stderr.strip()}")
            except subprocess.TimeoutExpired:
                print("  执行结果: 超时")
            except Exception as e:
                print(f"  执行结果: 异常 - {e}")
        else:
            print("  工具未找到，跳过执行测试")

def test_windows_specific():
    """测试Windows特定情况"""
    print("\n" + "="*50)
    print("Windows特定测试")
    print("="*50)
    
    # 测试Windows命令
    try:
        result = subprocess.run(
            ['where', 'claude'],
            capture_output=True,
            text=True,
            shell=True  # Windows必需
        )
        print(f"Windows where命令测试:")
        print(f"  返回码: {result.returncode}")
        print(f"  输出: {result.stdout.strip()}")
    except Exception as e:
        print(f"Windows where命令测试失败: {e}")

def test_alternative_commands():
    """测试可能的替代命令"""
    print("\n" + "="*50)
    print("替代命令测试")
    print("="*50)
    
    # 为可能的不同命名方式测试
    possible_names = {
        'cursor': ['cursor', 'cursor.exe', 'cursor.cmd'],
        'qwen': ['qwen', 'tongyi', 'qwen.exe', 'qwen.cmd'],
        'claude': ['claude', 'claude.exe', 'claude.cmd', 'claude-cli']
    }
    
    for main_name, alt_names in possible_names.items():
        print(f"\n测试 {main_name} 的可能变体:")
        for alt_name in alt_names:
            path = shutil.which(alt_name)
            if path:
                print(f"  ✅ 找到: {alt_name} -> {path}")
                # 尝试执行
                try:
                    result = subprocess.run(
                        [alt_name, '--version'],
                        capture_output=True,
                        text=True,
                        timeout=10,
                        shell=(platform.system() == 'Windows')
                    )
                    if result.returncode == 0:
                        print(f"    版本: {result.stdout.strip()[:50]}")
                    else:
                        print(f"    版本命令失败，但文件存在")
                except:
                    print(f"    版本命令执行失败")
            else:
                print(f"  ❌ 未找到: {alt_name}")

if __name__ == "__main__":
    test_detection_methods()
    test_windows_specific()
    test_alternative_commands()
    
    print("\n" + "="*50)
    print("检测逻辑验证完成")
    print("="*50)