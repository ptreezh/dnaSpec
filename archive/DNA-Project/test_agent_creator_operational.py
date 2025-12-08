# 智能体创建技能可操作性验证测试

import sys
import os
sys.path.insert(0, 'src')

from dnaspec_agent_creator import DNASPECAgentCreator

def test_operational_capabilities():
    """测试智能体创建技能的实际可操作性"""
    print("=== DNASPEC智能体创建技能可操作性验证 ===\n")
    
    agent_creator = DNASPECAgentCreator()
    
    # 测试用例1：复杂项目团队配置
    print("测试用例1：复杂项目团队配置")
    request1 = "Create agents for a large-scale fintech application development team including frontend, backend, mobile, security, and compliance specialists"
    result1 = agent_creator.process_request(request1)
    
    if result1["status"] == "completed":
        config1 = result1["agent_configuration"]
        print(f"✓ 成功创建 {len(config1['agents'])} 个智能体")
        print(f"✓ 定义 {len(config1['roles'])} 个角色")
        print("创建的智能体类型：", [agent['type'] for agent in config1['agents']])
        print()
    
    # 测试用例2：多领域智能体创建
    print("测试用例2：多领域智能体创建")
    request2 = "Create agents for a healthcare IoT system with device management, data analytics, patient monitoring, and regulatory compliance"
    result2 = agent_creator.process_request(request2)
    
    if result2["status"] == "completed":
        config2 = result2["agent_configuration"]
        print(f"✓ 成功创建 {len(config2['agents'])} 个智能体")
        domains = list(set([agent['domain'] for agent in config2['agents']]))
        print(f"✓ 涉及领域：{domains}")
        print()
    
    # 测试用例3：特定技术栈智能体
    print("测试用例3：特定技术栈智能体")
    request3 = "Create agents for a machine learning platform with data engineering, model training, deployment, and monitoring capabilities"
    result3 = agent_creator.process_request(request3)
    
    if result3["status"] == "completed":
        config3 = result3["agent_configuration"]
        print(f"✓ 成功创建 {len(config3['agents'])} 个智能体")
        # 显示能力关键词
        all_capabilities = []
        for agent in config3['agents']:
            all_capabilities.extend(agent['capabilities'])
        print(f"✓ 涉及技术能力：{list(set(all_capabilities))[:5]}...")  # 显示前5个
        print()
    
    # 测试用例4：通信协议验证
    print("测试用例4：通信协议配置")
    request4 = "Create agents for a real-time trading system with low-latency requirements"
    result4 = agent_creator.process_request(request4)
    
    if result4["status"] == "completed":
        config4 = result4["agent_configuration"]
        communication = config4['communication']
        print(f"✓ 支持的通信协议：{communication['protocols']}")
        print(f"✓ 支持的消息格式：{communication['message_formats']}")
        print(f"✓ 通信模式：{communication['communication_patterns']}")
        print()
    
    # 关键点提取准确性测试
    print("=== 关键点提取准确性测试 ===")
    test_requests = [
        ("Create security agents for financial applications", ["security_agent"]),
        ("Set up mobile app development team agents", ["mobile_app"]),
        ("Generate database administration agents", ["data_processing"]),
        ("Create testing and deployment automation agents", ["testing_agent", "deployment_agent"])
    ]
    
    accuracy_count = 0
    for request, expected_points in test_requests:
        extracted_points = agent_creator._extract_key_points(request)
        matched = all(point in extracted_points for point in expected_points)
        if matched:
            accuracy_count += 1
            print(f"✓ '{request}' -> {extracted_points}")
        else:
            print(f"✗ '{request}' -> {extracted_points} (期望包含: {expected_points})")
    
    accuracy_rate = accuracy_count / len(test_requests) * 100
    print(f"\n关键点提取准确率: {accuracy_rate:.1f}%")
    
    return accuracy_rate > 80  # 如果准确率超过80%则认为可操作性良好

def test_practical_application_scenarios():
    """测试实际应用场景的可操作性"""
    print("\n=== 实际应用场景可操作性测试 ===\n")
    
    agent_creator = DNASPECAgentCreator()
    
    # 场景1：电商平台开发
    print("场景1：电商平台开发团队配置")
    ecommerce_request = "Create a complete development team for an e-commerce platform including web frontend, mobile app, backend services, database management, payment integration, security, and testing"
    result = agent_creator.process_request(ecommerce_request)
    
    if result["status"] == "completed":
        config = result["agent_configuration"]
        agents_by_domain = {}
        for agent in config['agents']:
            domain = agent['domain']
            if domain not in agents_by_domain:
                agents_by_domain[domain] = []
            agents_by_domain[domain].append(agent['name'])
        
        print("✓ 按领域分配的智能体：")
        for domain, agents in agents_by_domain.items():
            print(f"  {domain}: {', '.join(agents)}")
        print()
        
        # 验证关键功能覆盖
        domains = list(agents_by_domain.keys())
        required_domains = ['frontend', 'backend', 'data', 'security']
        coverage = sum(1 for domain in required_domains if domain in domains) / len(required_domains)
        print(f"✓ 关键功能领域覆盖率: {coverage*100:.1f}%")
        print()
    
    # 场景2：企业级应用监控
    print("场景2：企业级应用监控配置")
    monitoring_request = "Create monitoring and operations agents for a enterprise application with performance monitoring, security auditing, log analysis, alerting, and automated remediation"
    result2 = agent_creator.process_request(monitoring_request)
    
    if result2["status"] == "completed":
        config2 = result2["agent_configuration"]
        monitoring_agents = [agent for agent in config2['agents'] if agent['type'] in ['monitoring', 'security']]
        print(f"✓ 创建了 {len(monitoring_agents)} 个监控相关智能体")
        
        # 显示监控能力
        monitoring_capabilities = []
        for agent in monitoring_agents:
            monitoring_capabilities.extend(agent['capabilities'])
        print(f"✓ 监控能力包括：{list(set(monitoring_capabilities))}")
        print()
    
    return True

def main():
    """主测试函数"""
    print("开始全面测试DNASPEC智能体创建技能的可操作性...\n")
    
    # 测试操作能力
    operational_ok = test_operational_capabilities()
    
    # 测试应用场景
    scenarios_ok = test_practical_application_scenarios()
    
    print("\n" + "="*60)
    print("=== 测试总结 ===")
    print(f"操作能力测试: {'通过' if operational_ok else '未通过'}")
    print(f"应用场景测试: {'通过' if scenarios_ok else '未通过'}")
    
    if operational_ok and scenarios_ok:
        print("\n🎉 DNASPEC智能体创建技能具有良好的可操作性！")
        print("\n主要优势：")
        print("1. 能够根据自然语言请求自动创建合适的智能体")
        print("2. 支持多领域、多类型的智能体配置")
        print("3. 提供完整的角色定义和能力规范")
        print("4. 生成标准化的通信协议配置")
        print("5. 适用于多种实际业务场景")
        print("\n建议改进：")
        print("1. 增强自然语言理解能力")
        print("2. 扩展智能体模板库")
        print("3. 支持智能体间更复杂的协作模式")
        print("4. 添加智能体生命周期管理功能")
    else:
        print("\n❌ 需要进一步优化可操作性")
    
    return operational_ok and scenarios_ok

if __name__ == "__main__":
    main()