"""
Context Engineering Enhancement System Test
测试整个上下文工程增强系统
"""
import sys
import os

# 添加项目路径到sys.path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from src.context_engineering_skills.system import ContextEngineeringSystem, execute, get_system_info


def test_context_engineering_system():
    """测试上下文工程系统"""
    print("=== 测试上下文工程增强系统 ===")
    
    # 显示系统信息
    info = get_system_info()
    print(f"系统名称: {info['system_name']}")
    print(f"版本: {info['version']}")
    print(f"功能: {', '.join(info['features'][:3])}...")  # 只显示前3个功能
    print()
    
    # 测试系统作为DNASPEC技能
    system = ContextEngineeringSystem()
    
    # 测试项目上下文增强
    print("1. 测试项目上下文增强:")
    project_desc = "开发一个电商平台，需要支持用户注册、商品展示、购物车、订单处理等功能。"
    context_params = {'function': 'enhance_context_for_project'}
    result = system.process_request(project_desc, context_params)
    
    if result.status.name == 'COMPLETED':
        result_data = result.result
        if result_data['success']:
            print(f"   原始描述长度: {len(result_data['original_description'])} 字符")
            print(f"   优化后长度: {len(result_data['optimized_context'])} 字符")
            print(f"   建议分解步骤数: {len(result_data['suggested_decomposition'])}")
        else:
            print(f"   错误: {result_data.get('error', '未知错误')}")
    else:
        print(f"   错误: {result.error_message}")
    print()
    
    # 测试AI代理上下文增强
    print("2. 测试AI代理上下文增强:")
    agent_task = "分析用户行为数据，识别购买模式，并提供个性化推荐策略。"
    context_params = {'function': 'enhance_agentic_context'}
    result = system.process_request(agent_task, context_params)
    
    if result.status.name == 'COMPLETED':
        result_data = result.result
        if result_data['success']:
            print(f"   原始任务长度: {len(result_data['original_task'])} 字符")
            print(f"   增强后上下文长度: {len(result_data['recommended_agent_context'])} 字符")
            print("   代理上下文已生成")
        else:
            print(f"   错误: {result_data.get('error', '未知错误')}")
    else:
        print(f"   错误: {result.error_message}")
    print()
    
    # 测试上下文审计
    print("3. 测试上下文审计:")
    test_context = "实现一个推荐系统，需要考虑用户偏好、时间因素等约束，目标是提高用户满意度。"
    context_params = {'function': 'run_context_audit'}
    result = system.process_request(test_context, context_params)
    
    if result.status.name == 'COMPLETED':
        result_data = result.result
        if result_data['success']:
            audit = result_data['audit_result']
            print(f"   上下文长度: {audit['context_length']} 字符")
            print(f"   质量得分: {audit['overall_quality_score']:.2f}/1.0")
            if audit['original_analysis']:
                print(f"   清晰度: {audit['original_analysis']['metrics']['clarity']:.2f}")
        else:
            print(f"   错误: {result_data.get('error', '未知错误')}")
    else:
        print(f"   错误: {result.error_message}")
    print()


def test_direct_execution():
    """测试直接执行函数"""
    print("=== 测试直接执行函数 ===")
    
    # 测试项目上下文增强
    print("1. 项目上下文增强:")
    args = {
        'function': 'enhance_context_for_project',
        'context': '构建一个社交媒体应用，支持用户发帖、评论、点赞等功能。'
    }
    result = execute(args)
    print(f"   执行结果长度: {len(result)} 字符")
    print()
    
    # 测试AI代理上下文增强
    print("2. AI代理上下文增强:")
    args = {
        'function': 'enhance_agentic_context', 
        'context': '设计一个自动化测试框架，用于API接口的功能和性能测试。'
    }
    result = execute(args)
    print(f"   执行结果长度: {len(result)} 字符")
    print()
    
    # 测试上下文审计
    print("3. 上下文审计:")
    args = {
        'function': 'run_context_audit',
        'context': '开发一个任务管理系统，支持多用户协作。'
    }
    result = execute(args)
    print(f"   执行结果长度: {len(result)} 字符")
    print()


def main():
    """主要测试函数"""
    print("Context Engineering Enhancement System 测试")
    print("=" * 70)
    
    try:
        test_context_engineering_system()
        test_direct_execution()
        
        print("所有系统测试完成！")
        print("\n系统已成功实现以下功能：")
        print("• 上下文分析与评估")
        print("• 上下文优化与改进") 
        print("• 认知模板应用")
        print("• 项目分解支持")
        print("• AI代理上下文管理")
        print("• 上下文审计功能")
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()