#!/usr/bin/env python3
"""
直接测试当前安装的CLI检测器
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.dsgs_spec_kit_integration.core.cli_detector import CliDetector

def test_detector():
    print("直接测试CLI检测器...")
    
    detector = CliDetector()
    
    # 单独测试每个工具
    print("\n1. 测试Claude检测:")
    try:
        claude_result = detector.detect_claude()
        print(f"   Claude检测结果: {claude_result}")
    except Exception as e:
        print(f"   Claude检测异常: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n2. 测试Qwen检测:")
    try:
        qwen_result = detector.detect_qwen()
        print(f"   Qwen检测结果: {qwen_result}")
    except Exception as e:
        print(f"   Qwen检测异常: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n3. 测试所有检测:")
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
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_detector()