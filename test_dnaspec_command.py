#!/usr/bin/env python3
"""
测试dnaspec命令执行的自动配置过程
"""
import subprocess
import os
from pathlib import Path

def test_dnaspec_command():
    print("测试 dnaspec 命令执行情况...")
    
    # 运行 dnaspec 命令
    try:
        # 在当前项目目录运行dnaspec命令，这将触发自动配置
        print("执行: dnaspec")
        result = subprocess.run(
            ['dnaspec'], 
            capture_output=True, 
            text=True,
            timeout=60  # 设置超时时间
        )
        
        print(f"返回码: {result.returncode}")
        print(f"标准输出:\n{result.stdout}")
        if result.stderr:
            print(f"标准错误:\n{result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("dnaspec命令执行超时")
    except FileNotFoundError:
        print("dnaspec命令未找到，请确保已全局安装")
    except Exception as e:
        print(f"执行dnaspec命令时出错: {str(e)}")

def test_run_auto_config():
    print("\n测试直接运行自动配置...")
    
    # 直接运行自动配置脚本
    try:
        result = subprocess.run(
            ['python', 'run_auto_config.py'],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        print(f"返回码: {result.returncode}")
        print(f"标准输出:\n{result.stdout}")
        if result.stderr:
            print(f"标准错误:\n{result.stderr}")
            
    except Exception as e:
        print(f"执行run_auto_config.py时出错: {str(e)}")

if __name__ == "__main__":
    test_dnaspec_command()
    test_run_auto_config()