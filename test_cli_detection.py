#!/usr/bin/env python3
"""
验证CLI检测器功能
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.dsgs_spec_kit_integration.core.cli_detector import CliDetector

def test_cli_detection():
    print("测试AI CLI工具检测功能...")
    
    detector = CliDetector()
    results = detector.detect_all()
    
    print("\n检测结果:")
    print("-" * 40)
    for tool, result in results.items():
        installed = result.get('installed', False)
        if installed:
            print(f"✅ {tool}: {result.get('version', 'Unknown')}")
            print(f"   路径: {result.get('installPath', 'Unknown')}")
        else:
            print(f"❌ {tool}: Not installed")
            error = result.get('error')
            if error:
                print(f"   错误: {error}")
    
    return results

if __name__ == "__main__":
    results = test_cli_detection()
    
    # 检查是否检测到已知工具
    detected_count = sum(1 for r in results.values() if r.get('installed', False))
    total_count = len(results)
    
    print(f"\n总结: 检测到 {detected_count}/{total_count} 个工具")
    
    if detected_count == 0:
        print("⚠️  没有检测到任何AI CLI工具")
        print("请确认:")
        print("- 工具是否已正确安装")
        print("- 是否已添加到系统PATH")
        print("- 是否可以从命令行直接运行 (如: claude --version)")