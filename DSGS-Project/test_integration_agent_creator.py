# 简单集成测试：验证主技能与智能体创建器的协调

def test_integration():
    """测试主技能与智能体创建器子技能的集成"""
    print("开始集成测试 - 主技能与智能体创建器...")
    
    # 直接导入并测试
    try:
        import sys
        sys.path.insert(0, 'src')
        sys.path.insert(0, 'src/dsgs_architect')
        sys.path.insert(0, 'src/dsgs_agent_creator')
        
        # 导入主技能
        from dsgs_architect import DSGSArchitect
        print("✓ 成功导入主技能")
        
        # 导入智能体创建器子技能
        from dsgs_agent_creator import DSGSAgentCreator
        print("✓ 成功导入智能体创建器子技能")
        
        # 创建技能实例
        main_skill = DSGSArchitect()
        agent_creator_skill = DSGSAgentCreator()
        
        # 测试请求
        test_request = "Create agents for developing a web application"
        
        # 1. 验证主技能能正确路由到智能体创建器
        routed_skill = main_skill._route_request(test_request)
        if routed_skill == "dsgs-agent-creator":
            print("✓ 主技能路由测试通过")
        else:
            print(f"✗ 主技能路由测试失败: 期望'dsgs-agent-creator'，实际'{routed_skill}'")
            return
        
        # 2. 验证智能体创建器子技能能正确处理请求
        result = agent_creator_skill.process_request(test_request)
        if result["status"] == "completed" and result["skill"] == "dsgs-agent-creator":
            print("✓ 子技能处理测试通过")
            print(f"  创建了 {len(result['agent_configuration']['agents'])} 个智能体")
        else:
            print(f"✗ 子技能处理测试失败: 状态={result['status']}, 技能={result['skill']}")
            return
        
        # 3. 验证完整流程
        main_result = main_skill.process_request(test_request)
        if main_result["status"] == "processed" and main_result["skill_used"] == "dsgs-agent-creator":
            print("✓ 完整流程测试通过")
        else:
            print(f"✗ 完整流程测试失败: 状态={main_result['status']}, 使用技能={main_result['skill_used']}")
            return
        
        print("主技能与智能体创建器集成测试通过！")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_integration()