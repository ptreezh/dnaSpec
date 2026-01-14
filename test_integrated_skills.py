# 测试三个新技能是否已正确集成到系统中
import sys
import os
import json

# 添加项目路径到Python模块搜索路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_skills_availability():
    """测试技能可用性"""
    from src.dna_spec_kit_integration.skills.skill_executor import skill_executor
    
    print("=== 测试技能注册情况 ===")
    
    # 检查技能注册表
    available_skills = skill_executor.get_available_skills()
    
    print("所有可用技能:")
    for skill_name, description in available_skills.items():
        print(f"  - {skill_name}: {description}")
    
    print("\n=== 测试三个核心技能是否已注册 ===")
    
    core_skills = [
        ('task-decomposer', '任务分解技能'),
        ('constraint-generator', '约束生成技能'), 
        ('api-checker', 'API检查技能')
    ]
    
    for skill_name, description in core_skills:
        if skill_name in skill_executor.skill_registry:
            print(f"✅ {description} ({skill_name}) 已注册")
        else:
            print(f"❌ {description} ({skill_name}) 未注册")
    
    print("\n=== 测试技能帮助信息 ===")
    for skill_name, description in core_skills:
        help_text = skill_executor.get_skill_help(skill_name)
        if "No help available" not in help_text:
            print(f"✅ {description} 帮助信息可用")
        else:
            print(f"❌ {description} 帮助信息不可用")
    
    print("\n=== 测试技能执行示例 ===")
    try:
        # 测试任务分解技能
        task_args = {
            "input": "创建一个简单的用户注册系统，包含用户名验证、邮箱验证、密码强度检查功能",
            "max_depth": 2
        }
        result = skill_executor.execute_skill('task-decomposer', **task_args)
        print("✅ 任务分解技能测试执行结果:", result.get('success', False))
    except Exception as e:
        print(f"❌ 任务分解技能执行失败: {e}")
    
    try:
        # 测试约束生成技能
        constraint_args = {
            "input": "用户验证系统应包含用户名验证、邮箱验证和密码检查功能",
            "options": {}
        }
        result = skill_executor.execute_skill('constraint-generator', **constraint_args)
        print("✅ 约束生成技能测试执行结果:", result.get('success', False))
    except Exception as e:
        print(f"❌ 约束生成技能执行失败: {e}")
    
    try:
        # 测试API检查技能
        api_args = {
            "input": {
                "apis": [
                    {
                        "name": "user-service",
                        "version": "1.0",
                        "endpoints": [
                            {"path": "/api/users", "method": "GET", "description": "Get user list"}
                        ],
                        "level": "module",
                        "dependencies": []
                    }
                ]
            },
            "detail_level": "standard"
        }
        result = skill_executor.execute_skill('api-checker', **api_args)
        print("✅ API检查技能测试执行结果:", result.get('success', False))
    except Exception as e:
        print(f"❌ API检查技能执行失败: {e}")

if __name__ == "__main__":
    test_skills_availability()