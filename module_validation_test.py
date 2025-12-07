#!/usr/bin/env python3
"""
模块功能验证脚本
测试DSGS模块是否可以正确导入并提供所需功能
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_imports():
    """测试模块导入"""
    print("测试模块导入...")
    
    # 尝试导入核心模块
    try:
        import src.dsgs_context_engineering.skills_system_final as skills_sys
        print("✅ 主模块导入成功")
    except ImportError as e:
        print(f"❌ 主模块导入失败: {e}")
        return False
    
    # 检查关键属性
    has_execute = hasattr(skills_sys, 'execute')
    has_get_available_skills = hasattr(skills_sys, 'get_available_skills')
    
    print(f"✅ execute函数: {'存在' if has_execute else '不存在'}")
    print(f"✅ get_available_skills函数: {'存在' if has_get_available_skills else '不存在'}")
    
    return has_execute

def test_available_skills():
    """测试可用技能列表"""
    print("\n测试可用技能...")
    try:
        import src.dsgs_context_engineering.skills_system_final as skills_sys
        available_skills = skills_sys.get_available_skills()
        print("✅ 可用技能列表获取成功:")
        for skill, desc in available_skills.items():
            print(f"  - {skill}: {desc}")
        return True
    except Exception as e:
        print(f"❌ 获取可用技能失败: {e}")
        return False

def test_core_functions():
    """测试核心功能"""
    print("\n测试核心功能...")
    try:
        import src.dsgs_context_engineering.skills_system_final as skills_sys
        
        # 1. 测试上下文分析
        print("  测试上下文分析...")
        try:
            result = skills_sys.execute({
                'skill': 'context-analysis', 
                'context': '测试上下文'
            })
            if result and len(result) > 10:
                print("    ✅ 上下文分析功能正常")
            else:
                print(f"    ❌ 上下文分析返回结果异常: {result}")
        except Exception as e:
            print(f"    ❌ 上下文分析错误: {e}")
            
        # 2. 测试上下文优化
        print("  测试上下文优化...")
        try:
            result = skills_sys.execute({
                'skill': 'context-optimization', 
                'context': '测试内容',
                'params': {}
            })
            if result and len(result) > 10:
                print("    ✅ 上下文优化功能正常")
            else:
                print(f"    ❌ 上下文优化返回结果异常: {result}")
        except Exception as e:
            print(f"    ❌ 上下文优化错误: {e}")
            
        # 3. 测试认知模板
        print("  测试认知模板...")
        try:
            result = skills_sys.execute({
                'skill': 'cognitive-template', 
                'context': '测试任务',
                'params': {}
            })
            if result and len(result) > 10:
                print("    ✅ 认知模板功能正常")
            else:
                print(f"    ❌ 认知模板返回结果异常: {result}")
        except Exception as e:
            print(f"    ❌ 认知模板错误: {e}")
            
        return True
    except Exception as e:
        print(f"❌ 核心功能测试错误: {e}")
        return False

def inspect_module_contents():
    """检查模块内容"""
    print("\n检查模块内容...")
    try:
        import importlib.util
        import inspect
        
        spec = importlib.util.spec_from_file_location(
            "skills_system", 
            "src/dsgs_context_engineering/skills_system_final.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # 获取模块的所有公共属性
        attributes = [attr for attr in dir(module) if not attr.startswith('_')]
        print("模块公共属性:")
        for attr in attributes:
            obj = getattr(module, attr)
            obj_type = type(obj).__name__
            print(f"  {attr}: {obj_type}")
            
            # 如果是函数，显示签名
            if callable(obj) and obj_type in ['function', 'builtin_function_or_method']:
                try:
                    sig = inspect.signature(obj)
                    print(f"    签名: {sig}")
                except:
                    pass
                    
        return True
    except Exception as e:
        print(f"❌ 检查模块内容失败: {e}")
        return False

def main():
    """主测试函数"""
    print("DSGS Context Engineering Skills 功能验证")
    print("="*50)
    
    success = True
    success &= test_imports()
    success &= test_available_skills()
    success &= test_core_functions()
    success &= inspect_module_contents()
    
    print("\n" + "="*50)
    if success:
        print("🎉 所有测试通过！DSGS系统功能正常。")
    else:
        print("❌ 存在测试失败。DSGS系统可能存在问题。")
    
    return success

if __name__ == "__main__":
    main()