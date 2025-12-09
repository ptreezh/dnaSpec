# 模块内智能体生成示例

import sys
sys.path.insert(0, 'src')

from dnaspec_agent_creator import DNASPECAgentCreator

def create_module_agents(module_name, requirements):
    """为特定模块创建智能体"""
    print(f"=== 为模块 '{module_name}' 创建智能体 ===")
    
    agent_creator = DNASPECAgentCreator()
    
    # 根据模块需求创建智能体
    result = agent_creator.process_request(requirements)
    
    if result["status"] == "completed":
        config = result["agent_configuration"]
        
        print(f"✓ 成功为模块 '{module_name}' 创建了 {len(config['agents'])} 个智能体")
        print("\n创建的智能体详情:")
        
        for i, agent in enumerate(config['agents'], 1):
            print(f"\n  智能体 {i}:")
            print(f"    名称: {agent['name']}")
            print(f"    ID: {agent['id']}")
            print(f"    类型: {agent['type']}")
            print(f"    领域: {agent['domain']}")
            print(f"    能力: {', '.join(agent['capabilities'])}")
        
        # 显示通信协议
        print(f"\n通信协议: {', '.join(config['communication']['protocols'])}")
        print(f"消息格式: {', '.join(config['communication']['message_formats'])}")
        
        return config
    else:
        print(f"✗ 创建智能体失败: {result.get('error', '未知错误')}")
        return None

# 示例：为不同模块创建智能体
if __name__ == "__main__":
    # 示例1：用户认证模块
    auth_config = create_module_agents(
        "用户认证模块", 
        "Create agents for implementing user authentication and authorization system with security monitoring"
    )
    
    print("\n" + "="*60 + "\n")
    
    # 示例2：订单处理模块
    order_config = create_module_agents(
        "订单处理模块",
        "Create agents for handling e-commerce order processing with database operations and payment integration"
    )
    
    print("\n" + "="*60 + "\n")
    
    # 示例3：数据分析模块
    analytics_config = create_module_agents(
        "数据分析模块",
        "Create agents for data analytics and reporting with machine learning capabilities"
    )
    
    print("\n=== 总结 ===")
    print("通过DNASPEC智能体创建技能，我们可以:")
    print("1. 根据模块的具体需求自动生成合适的智能体")
    print("2. 为每个智能体定义明确的角色和能力")
    print("3. 提供智能体间的通信和协作规范")
    print("4. 生成可执行的智能体配置文档")
    print("\n这种机制使得复杂系统的模块化开发变得更加智能化和自动化。")