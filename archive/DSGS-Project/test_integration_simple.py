# 简单集成测试脚本

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, 'src')

def test_integration():
    """测试主技能与系统架构师子技能的集成"""
    print("开始集成测试...")
    
    # 导入主技能
    try:
        from dsgs_architect import DSGSArchitect
        print("✓ 成功导入主技能")
    except Exception as e:
        print(f"✗ 导入主技能失败: {e}")
        return
    
    # 导入系统架构师子技能
    try:
        from dsgs_system_architect import DSGSSystemArchitect
        print("✓ 成功导入系统架构师子技能")
    except Exception as e:
        print(f"✗ 导入系统架构师子技能失败: {e}")
        return
    
    # 创建技能实例
    main_skill = DSGSArchitect()
    system_architect_skill = DSGSSystemArchitect()
    
    # 测试请求
    test_request = "Design architecture for a web application"
    
    # 1. 验证主技能能正确路由到系统架构师
    routed_skill = main_skill._route_request(test_request)
    if routed_skill == "dnaspec-system-architect":
        print("✓ 主技能路由测试通过")
    else:
        print(f"✗ 主技能路由测试失败: 期望'dnaspec-system-architect'，实际'{routed_skill}'")
        return
    
    # 2. 验证系统架构师子技能能正确处理请求
    result = system_architect_skill.process_request(test_request)
    if result["status"] == "completed" and result["skill"] == "dnaspec-system-architect":
        print("✓ 子技能处理测试通过")
    else:
        print(f"✗ 子技能处理测试失败: 状态={result['status']}, 技能={result['skill']}")
        return
    
    # 3. 验证完整流程
    main_result = main_skill.process_request(test_request)
    if main_result["status"] == "processed" and main_result["skill_used"] == "dnaspec-system-architect":
        print("✓ 完整流程测试通过")
    else:
        print(f"✗ 完整流程测试失败: 状态={main_result['status']}, 使用技能={main_result['skill_used']}")
        return
    
    print("所有集成测试通过！")

if __name__ == "__main__":
    test_integration()