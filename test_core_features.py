#!/usr/bin/env python3
"""
测试DSGS核心功能
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.dnaspec_context_engineering.skills_system_final import execute

print("测试DSGS核心功能:")

# 测试上下文分析功能
print("\n1. 上下文分析功能测试:")
try:
    result = execute({
        'skill': 'context-analysis', 
        'context': '设计一个电商系统，包含用户管理、商品管理、订单处理功能'
    })
    print(f"结果长度: {len(result)}")
    print(f"预览: {result[:100]}...")
except Exception as e:
    print(f"错误: {e}")

# 测试上下文优化功能  
print("\n2. 上下文优化功能测试:")
try:
    result = execute({
        'skill': 'context-optimization', 
        'context': '构建一个电商平台'
    })
    print(f"结果长度: {len(result)}")
    print(f"预览: {result[:100]}...")
except Exception as e:
    print(f"错误: {e}")

# 测试认知模板功能
print("\n3. 认知模板功能测试:")
try:
    result = execute({
        'skill': 'cognitive-template', 
        'context': '如何设计数据库架构', 
        'params': {'template': 'verification'}
    })
    print(f"结果长度: {len(result)}")
    print(f"预览: {result[:100]}...")
except Exception as e:
    print(f"错误: {e}")

print("\n所有核心功能测试完成！")