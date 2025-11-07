"""
基本功能测试脚本
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(__file__))

def test_basic_functionality():
    try:
        # 导入核心模块
        from src.dsgs_spec_kit_integration.core.manager import SkillManager
        from src.dsgs_spec_kit_integration.skills.examples import ArchitectSkill
        
        # 创建技能管理器
        manager = SkillManager()
        print("✓ SkillManager创建成功")
        
        # 创建技能
        skill = ArchitectSkill()
        print("✓ ArchitectSkill创建成功")
        
        # 注册技能
        result = manager.register_skill(skill)
        if result:
            print("✓ 技能注册成功")
        else:
            print("✗ 技能注册失败")
            return False
        
        # 执行技能
        skill_result = manager.execute_skill("dsgs-architect", "电商系统")
        if skill_result.status.name == "COMPLETED":
            print("✓ 技能执行成功")
            print(f"  结果: {skill_result.result}")
        else:
            print("✗ 技能执行失败")
            return False
            
        # 获取管理器信息
        info = manager.get_manager_info()
        print(f"✓ 管理器信息获取成功: {info['registered_skills_count']}个已注册技能")
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("开始基本功能测试...")
    success = test_basic_functionality()
    if success:
        print("\n🎉 所有基本功能测试通过!")
    else:
        print("\n❌ 基本功能测试失败!")
        sys.exit(1)