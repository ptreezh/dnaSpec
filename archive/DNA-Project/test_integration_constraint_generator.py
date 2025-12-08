# 简单集成测试：验证主技能与约束生成器的协调

def test_integration():
    """测试主技能与约束生成器子技能的集成"""
    print("开始集成测试 - 主技能与约束生成器...")
    
    # 直接导入并测试
    try:
        import sys
        sys.path.insert(0, 'src')
        sys.path.insert(0, 'src/dnaspec_architect')
        sys.path.insert(0, 'src/dnaspec_constraint_generator')
        
        # 导入主技能
        from dnaspec_architect import DNASPECArchitect
        print("✓ 成功导入主技能")
        
        # 导入约束生成器子技能
        from dnaspec_constraint_generator import DNASPECConstraintGenerator
        print("✓ 成功导入约束生成器子技能")
        
        # 创建技能实例
        main_skill = DNASPECArchitect()
        constraint_generator_skill = DNASPECConstraintGenerator()
        
        # 测试请求
        test_request = "Generate constraints for API design"
        
        # 1. 验证主技能能正确路由到约束生成器
        routed_skill = main_skill._route_request(test_request)
        if routed_skill == "dnaspec-constraint-generator":
            print("✓ 主技能路由测试通过")
        else:
            print(f"✗ 主技能路由测试失败: 期望'dnaspec-constraint-generator'，实际'{routed_skill}'")
            return
        
        # 2. 验证约束生成器子技能能正确处理请求
        result = constraint_generator_skill.process_request(test_request)
        if result["status"] == "completed" and result["skill"] == "dnaspec-constraint-generator":
            print("✓ 子技能处理测试通过")
            spec = result['constraint_specification']
            print(f"  生成了 {len(spec['system_constraints'])} 个系统约束")
            print(f"  生成了 {len(spec['api_constraints'])} 个API约束")
        else:
            print(f"✗ 子技能处理测试失败: 状态={result['status']}, 技能={result['skill']}")
            return
        
        # 3. 验证完整流程
        main_result = main_skill.process_request(test_request)
        if main_result["status"] == "processed" and main_result["skill_used"] == "dnaspec-constraint-generator":
            print("✓ 完整流程测试通过")
        else:
            print(f"✗ 完整流程测试失败: 状态={main_result['status']}, 使用技能={main_result['skill_used']}")
            return
        
        print("主技能与约束生成器集成测试通过！")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_integration()