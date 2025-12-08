# 集成测试：验证主技能与系统架构师子技能的协调

import sys
import os

# 添加src目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_dir)

def test_integration():
    """测试主技能与系统架构师子技能的集成"""
    # 导入主技能
    from dnaspec_architect import DNASPECArchitect
    # 导入系统架构师子技能
    from dnaspec_system_architect import DNASPECSystemArchitect
    
    # 创建技能实例
    main_skill = DNASPECArchitect()
    system_architect_skill = DNASPECSystemArchitect()
    
    # 测试请求
    test_request = "Design architecture for a web application"
    
    # 1. 验证主技能能正确路由到系统架构师
    routed_skill = main_skill._route_request(test_request)
    assert routed_skill == "dnaspec-system-architect", f"请求应该路由到dna-system-architect，但实际路由到{routed_skill}"
    print("✓ 主技能路由测试通过")
    
    # 2. 验证系统架构师子技能能正确处理请求
    result = system_architect_skill.process_request(test_request)
    assert result["status"] == "completed", "子技能处理状态应该为completed"
    assert result["skill"] == "dnaspec-system-architect", "处理技能应该是dna-system-architect"
    assert "architecture_design" in result, "结果应该包含架构设计"
    print("✓ 子技能处理测试通过")
    
    # 3. 验证完整流程
    main_result = main_skill.process_request(test_request)
    assert main_result["status"] == "processed", "主技能处理状态应该为processed"
    assert main_result["skill_used"] == "dnaspec-system-architect", "使用的技能应该是dna-system-architect"
    print("✓ 完整流程测试通过")
    
    print("所有集成测试通过！")

if __name__ == "__main__":
    test_integration()