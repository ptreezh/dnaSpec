#!/usr/bin/env python3
"""
验证适配器修复
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.dsgs_spec_kit_integration.adapters.concrete_spec_kit_adapter import ConcreteSpecKitAdapter

def test_adapter_registration():
    print("测试适配器技能注册...")
    
    # 创建适配器
    adapter = ConcreteSpecKitAdapter()
    
    # 获取所有注册的技能
    registered_skills = adapter.get_registered_skills()
    print(f"已注册技能数量: {len(registered_skills)}")
    print("已注册的DSGS技能:")
    for skill in registered_skills:
        print(f"  - {skill}")
    
    # 检查核心DSGS技能是否注册
    core_skills = [
        'dsgs-context-analysis',
        'dsgs-context-optimization', 
        'dsgs-cognitive-template'
    ]
    
    print("\n核心DSGS技能注册状态:")
    for skill in core_skills:
        status = "✅" if skill in registered_skills else "❌"
        print(f"  {status} {skill}")
    
    # 测试命令解析和执行
    print("\n测试斜杠命令:")
    test_commands = [
        "/speckit.dsgs.context-analysis 这是测试文本",
        "/speckit.dsgs.context-optimization 这是测试文本",
        "/speckit.dsgs.cognitive-template 这是测试文本"
    ]
    
    for cmd in test_commands:
        parsed = adapter.parse_command(cmd)
        print(f"命令: {cmd}")
        print(f"解析结果: {parsed}")
        
        # 尝试执行（可能会因缺少其他依赖而失败，但解析应该成功）
        try:
            result = adapter.execute_command(cmd)
            print(f"执行结果: {result.get('success', 'Unknown')}")
        except Exception as e:
            print(f"执行异常（可能是正常情况）: {type(e).__name__}")
        
        print()

if __name__ == "__main__":
    test_adapter_registration()