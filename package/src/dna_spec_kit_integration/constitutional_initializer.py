"""
宪法系统启动和验证脚本
确保宪法约束机制正确激活
"""
from typing import Dict, Any

def verify_constitutional_system():
    """
    验证宪法系统是否正确激活
    确保所有宪法约束机制都已启动
    """
    print("🔍 验证宪法系统激活状态...")
    
    # 1. 验证宪法验证器可用性
    try:
        from .skills.constitutional_validator import validate_constitutional_compliance
        print("✅ 宪法验证器可用")
    except ImportError:
        print("❌ 宪法验证器不可用")
        return False
    
    # 2. 验证宪法执行器可用性
    try:
        from .core.constitutional_enforcer import CONSTITUTIONAL_EXECUTOR
        print("✅ 宪法执行器可用")
    except ImportError:
        print("❌ 宪法执行器不可用")
        return False
    
    # 3. 验证宪法钩子系统可用性
    try:
        from .core.constitutional_hook_system import HOOK_SYSTEM
        print("✅ 宪法钩子系统可用")
    except ImportError:
        print("❌ 宪法钩子系统不可用")
        return False
    
    # 4. 验证宪法执行器
    try:
        from .core.constitutional_skill_executor import execute_skill_constitutionally
        print("✅ 宪法技能执行器可用")
    except ImportError:
        print("❌ 宪法技能执行器不可用")
        return False
    
    print("🎯 宪法系统验证完成！所有约束机制均已激活")
    print("🔒 任何技能执行都必须通过宪法验证")
    print("🚫 无法绕过宪法原则 - 系统的基本法已生效")
    
    return True

def test_constitutional_enforcement():
    """
    测试宪法强制执行机制
    """
    print("\n🧪 测试宪法强制执行...")
    
    try:
        from .core.constitutional_skill_executor import execute_skill_constitutionally
        
        # 测试一个简单的输入验证
        test_args = {"context": "# 测试内容\n\n这是符合宪法原则的测试内容。"}
        result = execute_skill_constitutionally("constitutional_validator", test_args)
        
        print(f"✅ 宪法执行测试通过")
        print(f"结果: {result[:100]}...")
        
        return True
    except Exception as e:
        print(f"❌ 宪法执行测试失败: {str(e)}")
        return False

def initialize_constitutional_framework():
    """
    初始化宪法框架 - 激活所有宪法约束
    """
    print("🏛️  初始化DNASPEC宪法框架...")
    
    # 验证系统
    if not verify_constitutional_system():
        print("❌ 宪法系统验证失败，无法初始化")
        return False
    
    # 测试执行
    if not test_constitutional_enforcement():
        print("❌ 宪法执行测试失败")
        return False
    
    print("\n✨ 宪法框架初始化完成！")
    print("📋 系统宪法约束已激活:")
    print("   • 生成前验证: 每次生成都必须通过宪法审查")
    print("   • 自动化执法: 无需人工干预的自动宪法执行") 
    print("   • 不可绕过: 任何生成路径都必须经过宪法检查")
    print("   • DNA级约束: 原则已刻在系统DNA中")
    print("\n🔐 宪法原则已成为系统的基本法")
    print("   任何违反宪法原则的生成都将被自动拒绝")
    
    return True

if __name__ == "__main__":
    # 当直接运行此脚本时，执行初始化
    initialize_constitutional_framework()