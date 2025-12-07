#!/usr/bin/env python3
"""
对比测试原版检测器和高级检测器
"""
import subprocess
import shutil
import platform

def test_original_detector(tool_name):
    """测试原版检测器逻辑"""
    print(f"=== 测试原版检测器: {tool_name} ===")
    
    try:
        # 原版检测器使用的逻辑
        result = subprocess.run(
            [tool_name, '--version'],
            capture_output=True,
            text=True,
            timeout=10,
            shell=(platform.system() == 'Windows')
        )
        
        print(f"  返回码: {result.returncode}")
        print(f"  标准输出: {result.stdout.strip()}")
        print(f"  标准错误: {result.stderr.strip()}")
        print(f"  成功: {result.returncode == 0}")
        
        if result.returncode == 0:
            print(f"  版本: {result.stdout.strip()}")
        else:
            print(f"  原版检测器失败")
            
    except Exception as e:
        print(f"  异常: {e}")

def test_advanced_detector(tool_name):
    """测试高级检测器逻辑"""
    print(f"\n=== 测试高级检测器: {tool_name} ===")
    
    # 先用shutil.which找到工具路径
    exe_path = shutil.which(tool_name)
    print(f"  shutil.which结果: {exe_path}")
    
    if exe_path:
        try:
            # 使用完整路径执行
            result = subprocess.run(
                [exe_path, '--version'],
                capture_output=True,
                text=True,
                timeout=10,
                shell=(platform.system() == 'Windows')
            )
            
            print(f"  使用完整路径执行结果:")
            print(f"    返回码: {result.returncode}")
            print(f"    标准输出: {result.stdout.strip()}")
            print(f"    标准错误: {result.stderr.strip()}")
            print(f"    成功: {result.returncode == 0}")
            
        except Exception as e:
            print(f"  使用完整路径执行异常: {e}")
    else:
        print(f"  无法找到 {tool_name} 的完整路径")

def test_both_ways(tool_name):
    """测试两种方式"""
    test_original_detector(tool_name)
    test_advanced_detector(tool_name)

def main():
    tools = ['claude', 'qwen', 'gemini', 'cursor']
    
    for tool in tools:
        print(f"\n{'-'*50}")
        test_both_ways(tool)
    
    print(f"\n{'-'*50}")
    print("=== 问题诊断 ===")
    print("如果原版检测器失败但高级检测器成功，说明问题是:")
    print("1. subprocess.run使用工具名而非完整路径")
    print("2. Windows shell环境的特殊性")
    print("3. PATH解析问题")

if __name__ == "__main__":
    main()