# 完整端到端测试：验证所有技能的协调工作

def test_end_to_end():
    """测试所有技能的端到端集成"""
    print("开始端到端集成测试 - 所有技能协调工作...")
    
    # 直接导入并测试
    try:
        import sys
        sys.path.insert(0, 'src')
        
        # 导入所有技能
        from dnaspec_architect import DNASPECArchitect
        from dnaspec_system_architect import DNASPECSystemArchitect
        from dnaspec_task_decomposer import DNASPECTaskDecomposer
        from dnaspec_agent_creator import DNASPECAgentCreator
        from dnaspec_constraint_generator import DNASPECConstraintGenerator
        
        print("✓ 成功导入所有技能")
        
        # 创建技能实例
        main_skill = DNASPECArchitect()
        system_architect = DNASPECSystemArchitect()
        task_decomposer = DNASPECTaskDecomposer()
        agent_creator = DNASPECAgentCreator()
        constraint_generator = DNASPECConstraintGenerator()
        
        # 测试用例1：系统架构设计
        print("\n--- 测试用例1：系统架构设计 ---")
        request1 = "Design architecture for a web application with API services"
        result1 = main_skill.process_request(request1)
        if result1["status"] == "processed" and result1["skill_used"] == "dnaspec-system-architect":
            print("✓ 系统架构设计请求处理成功")
        else:
            print(f"✗ 系统架构设计请求处理失败: {result1}")
            return
        
        # 测试用例2：任务分解
        print("\n--- 测试用例2：任务分解 ---")
        request2 = "Decompose tasks for developing a mobile app with backend services"
        result2 = main_skill.process_request(request2)
        if result2["status"] == "processed" and result2["skill_used"] == "dnaspec-task-decomposer":
            print("✓ 任务分解请求处理成功")
        else:
            print(f"✗ 任务分解请求处理失败: {result2}")
            return
        
        # 测试用例3：智能体创建
        print("\n--- 测试用例3：智能体创建 ---")
        request3 = "Create agents for implementing a secure web platform"
        result3 = main_skill.process_request(request3)
        if result3["status"] == "processed" and result3["skill_used"] == "dnaspec-agent-creator":
            print("✓ 智能体创建请求处理成功")
        else:
            print(f"✗ 智能体创建请求处理失败: {result3}")
            return
        
        # 测试用例4：约束生成
        print("\n--- 测试用例4：约束生成 ---")
        request4 = "Generate constraints for API design and data security"
        result4 = main_skill.process_request(request4)
        if result4["status"] == "processed" and result4["skill_used"] == "dnaspec-constraint-generator":
            print("✓ 约束生成请求处理成功")
        else:
            print(f"✗ 约束生成请求处理失败: {result4}")
            return
        
        # 验证路由准确性
        print("\n--- 验证路由准确性 ---")
        routing_tests = [
            ("Design system architecture", "dnaspec-system-architect"),
            ("Decompose complex tasks", "dnaspec-task-decomposer"),
            ("Create intelligent agents", "dnaspec-agent-creator"),
            ("Generate system constraints", "dnaspec-constraint-generator")
        ]
        
        all_routing_correct = True
        for request, expected_skill in routing_tests:
            routed_skill = main_skill._route_request(request)
            if routed_skill == expected_skill:
                print(f"✓ '{request}' -> '{routed_skill}'")
            else:
                print(f"✗ '{request}' -> '{routed_skill}' (期望: '{expected_skill}')")
                all_routing_correct = False
        
        if all_routing_correct:
            print("✓ 所有路由测试通过")
        else:
            print("✗ 部分路由测试失败")
            return
        
        print("\n🎉 所有端到端集成测试通过！")
        print("DNASPEC智能架构师系统完整功能验证成功！")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_end_to_end()