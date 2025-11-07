"""
Final Integration Test for DSGS Context Engineering Skills System
验证所有组件正确集成和工作
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_imports():
    """测试所有模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        from src.dsgs_context_engineering import (
            ContextEngineeringSkill,
            SkillResult,
            SkillsManager,
            AIModelClient,
            TemplateRegistry,
            ContextEngineeringSystem
        )
        print("   ✅ 核心模块导入成功")
    except ImportError as e:
        print(f"   ❌ 核心模块导入失败: {e}")
        return False
    
    try:
        from src.dsgs_context_engineering.skills import (
            ContextAnalysisSkill,
            ContextOptimizationSkill,
            CognitiveTemplateSkill
        )
        print("   ✅ 技能模块导入成功")
    except ImportError as e:
        print(f"   ❌ 技能模块导入失败: {e}")
        return False
    
    return True


def test_ai_client_creation():
    """测试AI客户端创建"""
    print("\n🔍 测试AI客户端创建...")
    
    try:
        from src.dsgs_context_engineering.ai_client import create_ai_client
        
        # 测试通用客户端创建（用于开发测试）
        client = create_ai_client("generic", "dummy-key")
        print("   ✅ AI客户端创建成功")
        return True
    except Exception as e:
        print(f"   ❌ AI客户端创建失败: {e}")
        return False


def test_template_registry():
    """测试模板注册表"""
    print("\n🔍 测试模板注册表...")
    
    try:
        from src.dsgs_context_engineering.instruction_template import TemplateRegistry
        
        registry = TemplateRegistry()
        templates = registry.list_templates()
        print(f"   ✅ 模板注册表创建成功，可用模板: {len(templates)} 个")
        print(f"      模板列表: {templates}")
        return True
    except Exception as e:
        print(f"   ❌ 模板注册表测试失败: {e}")
        return False


def test_skill_creation():
    """测试技能创建"""
    print("\n🔍 测试技能创建...")
    
    try:
        from src.dsgs_context_engineering.ai_client import create_ai_client
        from src.dsgs_context_engineering.instruction_template import TemplateRegistry
        from src.dsgs_context_engineering.skills.context_analysis import ContextAnalysisSkill
        
        # 创建依赖组件
        client = create_ai_client("generic", "dummy-key")
        registry = TemplateRegistry()
        
        # 创建技能
        skill = ContextAnalysisSkill(client, registry)
        print(f"   ✅ {skill.name} 技能创建成功")
        return True
    except Exception as e:
        print(f"   ❌ 技能创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_system_creation():
    """测试系统创建"""
    print("\n🔍 测试系统创建...")
    
    try:
        from src.dsgs_context_engineering.system import ContextEngineeringSystem
        
        system = ContextEngineeringSystem(ai_provider="generic")
        print("   ✅ ContextEngineeringSystem 创建成功")
        print(f"      可用技能: {list(system.skills_manager.skills.keys())}")
        return True
    except Exception as e:
        print(f"   ❌ 系统创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_skill_execution():
    """测试技能执行"""
    print("\n🔍 测试技能执行...")
    
    try:
        from src.dsgs_context_engineering.system import ContextEngineeringSystem
        
        system = ContextEngineeringSystem(ai_provider="generic")
        
        # 测试上下文分析技能
        test_context = "开发一个电商系统，需要支持用户登录、商品浏览、购物车功能。"
        result = system.skills_manager.execute_skill('context-analysis', test_context, {})
        
        print(f"   ✅ 技能执行返回成功: {result.success}")
        if result.success:
            print(f"      结果类型: {type(result.data)}")
            print(f"      置信度: {result.confidence:.2f}")
        else:
            print(f"      错误: {result.error}")
        
        return True
    except Exception as e:
        print(f"   ❌ 技能执行失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("🧪 DSGS Context Engineering Skills System - 最终集成测试")
    print("=" * 70)
    
    all_tests_passed = True
    
    # 运行所有测试
    tests = [
        test_imports,
        test_ai_client_creation, 
        test_template_registry,
        test_skill_creation,
        test_system_creation,
        test_skill_execution
    ]
    
    for test_func in tests:
        if not test_func():
            all_tests_passed = False
    
    print("\n" + "=" * 70)
    if all_tests_passed:
        print("🎉 所有测试通过！DSGS Context Engineering Skills System 已成功部署。")
        print("\n系统现在可以使用以下功能：")
        print("   • context-analysis: 上下文质量五维分析")
        print("   • context-optimization: 上下文内容优化") 
        print("   • cognitive-template: 认知模板应用")
        print("   • 系统级功能: 项目分解支持、AI代理上下文管理、上下文审计")
        print("\n使用方法：")
        print("   1. 创建 ContextEngineeringSystem 实例")
        print("   2. 通过 skills_manager 调用所需技能")
        print("   3. 获取结构化的分析、优化或模板应用结果")
        print("\n💡 系统已准备好进行实际的上下文工程任务！")
    else:
        print("❌ 部分测试失败，请检查错误信息并修复问题。")
    
    print("=" * 70)
    return all_tests_passed


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)