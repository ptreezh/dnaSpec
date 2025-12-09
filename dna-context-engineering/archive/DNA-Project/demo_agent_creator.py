# 智能体创建技能使用演示

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, 'src')

def demo_agent_creator():
    """演示智能体创建技能的使用方法"""
    print("=== DNASPEC智能体创建技能使用演示 ===\n")
    
    # 导入智能体创建技能
    from dnaspec_agent_creator import DNASPECAgentCreator
    
    # 创建技能实例
    agent_creator = DNASPECAgentCreator()
    
    print("✓ 智能体创建技能加载成功")
    print(f"技能名称: {agent_creator.name}")
    print(f"技能描述: {agent_creator.description}")
    print(f"技能能力: {agent_creator.capabilities}")
    print("\n" + "="*60 + "\n")
    
    # 演示不同类型的智能体创建请求
    demo_requests = [
        {
            "request": "Create agents for developing a web application with API services",
            "description": "Web应用开发智能体"
        },
        {
            "request": "Create agents for implementing security monitoring and testing",
            "description": "安全和测试智能体"
        },
        {
            "request": "Create agents for a mobile e-commerce platform with database",
            "description": "移动电商智能体"
        }
    ]
    
    for i, demo in enumerate(demo_requests, 1):
        print(f"演示 {i}: {demo['description']}")
        print(f"请求: {demo['request']}")
        
        # 处理请求
        result = agent_creator.process_request(demo['request'])
        
        # 显示结果
        print(f"处理状态: {result['status']}")
        
        # 显示智能体配置
        config = result['agent_configuration']
        print(f"创建智能体数量: {len(config['agents'])}")
        print(f"定义角色数量: {len(config['roles'])}")
        print(f"行为规范数量: {len(config['behaviors'])}")
        
        # 显示创建的智能体
        print("创建的智能体:")
        for agent in config['agents'][:3]:  # 只显示前3个
            print(f"  - {agent['name']} (ID: {agent['id']})")
            print(f"    类型: {agent['type']}, 领域: {agent['domain']}")
            print(f"    能力: {', '.join(agent['capabilities'][:3])}")  # 只显示前3个能力
        
        # 显示定义的角色
        if config['roles']:
            print("定义的角色:")
            for role in config['roles'][:2]:  # 只显示前2个
                print(f"  - {role['name']}")
                print(f"    职责: {', '.join(role['responsibilities'][:3])}")
        
        print("-" * 40 + "\n")
    
    # 演示关键点提取功能
    print("=== 关键点提取功能演示 ===")
    test_requests = [
        "Create agents for web application development",
        "Set up security and monitoring agents",
        "Generate testing agents for API services"
    ]
    
    for request in test_requests:
        key_points = agent_creator._extract_key_points(request)
        print(f"请求: {request}")
        print(f"提取的关键点: {key_points}")
        print()
    
    print("=== 智能体创建技能工作原理解释 ===")
    print("1. 智能体创建技能通过分析自然语言请求来识别项目需求")
    print("2. 根据识别的关键点（如web_application, api_service等）创建相应类型的智能体")
    print("3. 为每个智能体定义明确的角色、职责和能力")
    print("4. 生成智能体间通信和协作的规范")
    print("5. 提供监控和管理建议")
    print("\n智能体创建技能可以帮助:")
    print("- 自动化项目团队配置")
    print("- 标准化角色定义和职责分配")
    print("- 生成可执行的智能体规范文档")
    print("- 提供智能体间协作的最佳实践")

if __name__ == "__main__":
    demo_agent_creator()