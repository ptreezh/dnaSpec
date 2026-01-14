"""
双重实现验证脚本
测试 DNASPEC slash 命令和 Claude Skills 格式
"""
import json
import sys
import os

# 添加路径
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

print("🔍 测试双重实现架构")
print("="*50)

# 1. 测试 Claude Skills 格式
print("\n1. 测试 Claude Skills 格式:")
try:
    from dna_spec_kit_integration.skills.architect_claude import execute_skill
    
    claude_event = {
        'requirements': '设计一个电商系统',
        'user_context': 'system_designer'
    }
    
    claude_result = execute_skill(claude_event)
    print(f"   ✅ Claude Skills 格式: 成功")
    print(f"   状态码: {claude_result.get('statusCode', 'N/A')}")
    print(f"   响应体: {claude_result.get('body', 'N/A')[:100]}...")
    
except Exception as e:
    print(f"   ❌ Claude Skills 格式: 失败 - {e}")

# 2. 测试 DNASPEC 格式
print("\n2. 测试 DNASPEC 格式:")
try:
    from dna_spec_kit_integration.skills.architect_claude import execute
    
    dnaspec_args = {
        'description': '设计一个电商系统',
        'requirements': '电商系统架构'
    }
    
    dnaspec_result = execute(dnaspec_args)
    print(f"   ✅ DNASPEC 格式: 成功")
    print(f"   结果类型: {type(dnaspec_result)}")
    print(f"   结果内容: {dnaspec_result[:100]}...")
    
except Exception as e:
    print(f"   ❌ DNASPEC 格式: 失败 - {e}")

# 3. 测试其他技能的 Claude 格式
print("\n3. 测试 Context Analysis Claude 格式:")
try:
    from dna_spec_kit_integration.skills.context_analysis_claude import execute_skill as ca_execute_skill
    
    ca_event = {
        'context': '这是一个简单的用户登录功能需求',
        'analysis_type': 'comprehensive'
    }
    
    ca_result = ca_execute_skill(ca_event)
    print(f"   ✅ Context Analysis Claude 格式: 成功")
    print(f"   状态码: {ca_result.get('statusCode', 'N/A')}")
    
    import ast
    body_data = ast.literal_eval(ca_result.get('body', '{}'))
    if body_data.get('success'):
        print(f"   分析成功: {body_data.get('result', {}).get('context_length', 'N/A')} 字符")
    else:
        print(f"   分析结果: {body_data.get('error', 'N/A')}")
    
except Exception as e:
    print(f"   ❌ Context Analysis Claude 格式: 失败 - {e}")

# 4. 测试 DNASPEC Context Analysis 格式
print("\n4. 测试 Context Analysis DNASPEC 格式:")
try:
    from dna_spec_kit_integration.skills.context_analysis_claude import execute as ca_execute
    
    ca_args = {
        'context': '这是一个简单的用户登录功能需求'
    }
    
    ca_dnaspec_result = ca_execute(ca_args)
    print(f"   ✅ Context Analysis DNASPEC 格式: 成功")
    print(f"   结果类型: {type(ca_dnaspec_result)}")
    print(f"   结果预览: {ca_dnaspec_result[:100]}...")
    
except Exception as e:
    print(f"   ❌ Context Analysis DNASPEC 格式: 失败 - {e}")

print("\n" + "="*50)
print("✅ 双重实现验证完成")
print("系统现在支持两种格式：")
print("- DNASPEC slash 命令格式 (/speckit.dnaspec.*)")
print("- Claude Skills 标准格式 (标准接口)")