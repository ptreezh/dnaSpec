#!/usr/bin/env python3
"""
测试CLI检测器功能
"""
import sys
import os
# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.dsgs_spec_kit_integration.core.cli_detector import CliDetector

def test_detection():
    print("开始测试CLI检测器...")
    
    detector = CliDetector()
    
    # 测试Claude检测
    print("\n1. 测试Claude检测:")
    try:
        claude_result = detector.detect_claude()
        print(f"   Claude检测结果: {claude_result}")
    except Exception as e:
        print(f"   Claude检测异常: {e}")
    
    # 测试所有检测
    print("\n2. 测试所有CLI检测:")
    try:
        all_results = detector.detect_all()
        for tool, result in all_results.items():
            status = "✅ 已安装" if result.get('installed') else "❌ 未安装"
            print(f"   {tool}: {status}")
            if result.get('installed'):
                print(f"     版本: {result.get('version', 'Unknown')}")
                print(f"     路径: {result.get('installPath', 'Unknown')}")
    except Exception as e:
        print(f"   所有检测异常: {e}")
    
    # 直接测试subprocess命令
    print("\n3. 直接测试subprocess命令:")
    import subprocess
    try:
        result = subprocess.run(['claude', '--version'], capture_output=True, text=True, timeout=10)
        print(f"   返回码: {result.returncode}")
        print(f"   输出: {result.stdout.strip()}")
        print(f"   错误: {result.stderr.strip() if result.stderr.strip() else '无错误'}")
    except subprocess.TimeoutExpired:
        print("   命令超时")
    except FileNotFoundError:
        print("   找不到命令")
    except Exception as e:
        print(f"   异常: {e}")

if __name__ == "__main__":
    test_detection()