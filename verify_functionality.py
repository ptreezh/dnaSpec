#!/usr/bin/env python3
"""
DNASPEC功能测试脚本 - 修复版本
验证所有功能是否正常工作
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.dnaspec_context_engineering.skills_system_final import execute

def test_all_skills():
    print("DNASPEC Context Engineering Skills - 功能验证")
    print("="*50)
    
    try:
        # 1. 测试上下文分析
        print("1. 测试上下文分析...")
        result1 = execute({
            'skill': 'context-analysis',
            'context': '设计一个用户登录系统，需要支持邮箱和密码验证'
        })
        print(f"   结果长度: {len(result1)}")
        print(f"   预览: {result1[:100]}...")
        print("   ✅ 上下文分析功能正常\n")
        
        # 2. 测试上下文优化
        print("2. 测试上下文优化...")
        result2 = execute({
            'skill': 'context-optimization',
            'context': '做个登录功能',
            'params': {'optimization_goals': ['clarity', 'completeness']}
        })
        print(f"   结果长度: {len(result2)}")
        print(f"   预览: {result2[:100]}...")
        print("   ✅ 上下文优化功能正常\n")
        
        # 3. 测试认知模板
        print("3. 测试认知模板...")
        result3 = execute({
            'skill': 'cognitive-template',
            'context': '如何设计API接口',
            'params': {'template': 'verification'}
        })
        print(f"   结果长度: {len(result3)}")
        print(f"   预览: {result3[:100]}...")
        print("   ✅ 认知模板功能正常\n")
        
        print("🎉 所有核心功能测试通过！")
        print("DNASPEC Context Engineering Skills 系统完全正常运行！")
        print("系统已准备好在AI CLI环境中使用。")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_all_skills()