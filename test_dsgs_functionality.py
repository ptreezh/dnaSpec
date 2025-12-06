#!/usr/bin/env python3
"""
DSGS功能测试脚本
验证DSGS Context Engineering Skills是否正确安装和工作
"""
from src.dsgs_context_engineering.skills_system_final import execute

def test_context_analysis():
    """测试上下文分析功能"""
    print("测试上下文分析功能...")
    result = execute({
        'context': '设计一个用户管理系统',
        'skill': 'context-analysis'
    })
    print(result)
    print()

def test_context_optimization():
    """测试上下文优化功能"""
    print("测试上下文优化功能...")
    result = execute({
        'context': '创建一个电商网站',
        'skill': 'context-optimization'
    })
    print(result)
    print()

def test_cognitive_template():
    """测试认知模板功能"""
    print("测试认知模板功能...")
    result = execute({
        'context': '如何提高系统性能',
        'skill': 'cognitive-template'
    })
    print(result)
    print()

if __name__ == "__main__":
    print("DSGS功能测试")
    print("="*50)
    
    test_context_analysis()
    test_context_optimization()
    test_cognitive_template()
    
    print("测试完成！")