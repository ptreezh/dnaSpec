# 简单测试脚本：验证约束生成器功能

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, 'src')

def test_constraint_generator():
    """测试约束生成器功能"""
    print("开始测试约束生成器...")
    
    # 导入约束生成器子技能
    try:
        from dsgs_constraint_generator import DSGSConstraintGenerator
        print("✓ 成功导入约束生成器子技能")
    except Exception as e:
        print(f"✗ 导入约束生成器子技能失败: {e}")
        return
    
    # 创建技能实例
    constraint_generator = DSGSConstraintGenerator()
    
    # 测试请求
    test_request = "Generate constraints for developing a web application with API services and database"
    
    # 测试约束生成功能
    result = constraint_generator.process_request(test_request)
    
    if result["status"] == "completed" and result["skill"] == "dsgs-constraint-generator":
        print("✓ 约束生成功能测试通过")
        spec = result['constraint_specification']
        print(f"  生成了 {len(spec['system_constraints'])} 个系统约束")
        print(f"  生成了 {len(spec['api_constraints'])} 个API约束")
        print(f"  生成了 {len(spec['data_constraints'])} 个数据约束")
        print(f"  生成了 {len(spec['quality_constraints'])} 个质量约束")
    else:
        print(f"✗ 约束生成功能测试失败: 状态={result['status']}, 技能={result['skill']}")
        return
    
    # 测试关键点提取
    key_points = constraint_generator._extract_key_points(test_request)
    expected_points = ["web_application", "api_service", "data_processing"]
    all_found = all(point in key_points for point in expected_points)
    
    if all_found:
        print("✓ 关键点提取测试通过")
        print(f"  提取到的关键点: {key_points}")
    else:
        print(f"✗ 关键点提取测试失败: 期望包含{expected_points}, 实际提取到{key_points}")
        return
    
    print("约束生成器测试成功完成！")

if __name__ == "__main__":
    test_constraint_generator()