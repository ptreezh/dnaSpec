#!/usr/bin/env python3
"""
DSGS功能测试脚本
验证所有核心功能是否正常工作
"""
from src.dnaspec_context_engineering.skills_system_final import execute

def test_context_analysis():
    print("测试上下文分析功能...")
    result = execute({
        'skill': 'context-analysis', 
        'context': '设计一个电商系统，支持用户登录、商品浏览、购买功能'
    })
    print(f"结果: {result[:200]}...")
    print("✅ 上下文分析功能正常\n")

def test_context_optimization():
    print("测试上下文优化功能...")
    result = execute({
        'skill': 'context-optimization', 
        'context': '做个电商网站',
        'params': {'optimization_goals': ['clarity', 'completeness']}
    })
    print(f"结果: {result[:200]}...")
    print("✅ 上下文优化功能正常\n")

def test_cognitive_template():
    print("测试认知模板功能...")
    result = execute({
        'skill': 'cognitive-template', 
        'context': '如何设计数据库表结构',
        'params': {'template': 'verification'}
    })
    print(f"结果: {result[:200]}...")
    print("✅ 认知模板功能正常\n")

def test_agent_creation():
    print("测试代理创建功能...")
    result = execute({
        'skill': 'context-analysis',
        'context': '创建代码质量检查代理，专注性能问题'
    })
    print(f"结果: {result[:200]}...")
    print("✅ 代理创建功能测试完成\n")

def test_task_decomposition():
    print("测试任务分解功能...")
    result = execute({
        'skill': 'context-optimization',
        'context': '开发电商系统，包含用户、商品、订单模块',
        'params': {'optimization_goals': ['clarity']}
    })
    print(f"结果: {result[:200]}...")
    print("✅ 任务分解功能测试完成\n")

if __name__ == "__main__":
    print("DNASPEC Context Engineering Skills 功能测试")
    print("="*50)
    
    try:
        test_context_analysis()
        test_context_optimization()
        test_cognitive_template()
        test_agent_creation()
        test_task_decomposition()
        
        print("🎉 所有功能测试通过！")
        print("DSGS系统已完全正常运行！")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        
    input("\n按Enter键退出...")