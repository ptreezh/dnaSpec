# 简单测试脚本：验证智能体创建器功能

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, 'src')

def test_agent_creator():
    """测试智能体创建器功能"""
    print("开始测试智能体创建器...")
    
    # 导入智能体创建器子技能
    try:
        from dsgs_agent_creator import DSGSAgentCreator
        print("✓ 成功导入智能体创建器子技能")
    except Exception as e:
        print(f"✗ 导入智能体创建器子技能失败: {e}")
        return
    
    # 创建技能实例
    agent_creator = DSGSAgentCreator()
    
    # 测试请求
    test_request = "Create agents for developing a web application with API services and database"
    
    # 测试智能体创建功能
    result = agent_creator.process_request(test_request)
    
    if result["status"] == "completed" and result["skill"] == "dsgs-agent-creator":
        print("✓ 智能体创建功能测试通过")
        print(f"  创建了 {len(result['agent_configuration']['agents'])} 个智能体")
        print(f"  定义了 {len(result['agent_configuration']['roles'])} 个角色")
    else:
        print(f"✗ 智能体创建功能测试失败: 状态={result['status']}, 技能={result['skill']}")
        return
    
    # 测试关键点提取
    key_points = agent_creator._extract_key_points(test_request)
    expected_points = ["web_application", "api_service", "data_processing"]
    all_found = all(point in key_points for point in expected_points)
    
    if all_found:
        print("✓ 关键点提取测试通过")
        print(f"  提取到的关键点: {key_points}")
    else:
        print(f"✗ 关键点提取测试失败: 期望包含{expected_points}, 实际提取到{key_points}")
        return
    
    print("智能体创建器测试成功完成！")

if __name__ == "__main__":
    test_agent_creator()