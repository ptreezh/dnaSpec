# 简单测试脚本：验证任务分解器功能

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, 'src')

def test_task_decomposer():
    """测试任务分解器功能"""
    print("开始测试任务分解器...")
    
    # 导入任务分解器子技能
    try:
        from dsgs_task_decomposer import DSGSTaskDecomposer
        print("✓ 成功导入任务分解器子技能")
    except Exception as e:
        print(f"✗ 导入任务分解器子技能失败: {e}")
        return
    
    # 创建技能实例
    task_decomposer = DSGSTaskDecomposer()
    
    # 测试请求
    test_request = "Decompose tasks for developing a web application with API services and database"
    
    # 测试任务分解功能
    result = task_decomposer.process_request(test_request)
    
    if result["status"] == "completed" and result["skill"] == "dsgs-task-decomposer":
        print("✓ 任务分解功能测试通过")
        print(f"  生成了 {len(result['task_decomposition']['atomic_tasks'])} 个原子任务")
        print(f"  识别了 {len(result['task_decomposition']['dependencies'])} 个任务依赖")
    else:
        print(f"✗ 任务分解功能测试失败: 状态={result['status']}, 技能={result['skill']}")
        return
    
    # 测试关键点提取
    key_points = task_decomposer._extract_key_points(test_request)
    expected_points = ["web_development", "api_development", "data_management"]
    all_found = all(point in key_points for point in expected_points)
    
    if all_found:
        print("✓ 关键点提取测试通过")
        print(f"  提取到的关键点: {key_points}")
    else:
        print(f"✗ 关键点提取测试失败: 期望包含{expected_points}, 实际提取到{key_points}")
        return
    
    print("任务分解器测试成功完成！")

if __name__ == "__main__":
    test_task_decomposer()