import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

print("🔍 真实系统验证测试")

try:
    # 直接测试具体实现
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "skills_system_final_clean", 
        "D:/DAIP/dnaSpec/src/dnaspec_context_engineering/skills_system_final_clean.py"
    )
    skills_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(skills_module)
    
    print("✅ 模块成功加载")
    
    # 检查是否有ContextAnalysisSkill类
    skill_class = getattr(skills_module, 'ContextAnalysisSkill', None)
    if skill_class:
        print("✅ ContextAnalysisSkill类存在")
        
        # 创建实例并测试
        skill = skill_class()
        print(f"✅ 技能实例化成功: {skill.name}")
        
        # 调用方法
        result = skill.process_request("测试上下文分析", {})
        print(f"✅ 技能执行完成: {result.status.name}")
        
        if result.status.name == 'COMPLETED':
            print("✅ 系统功能完全正常！")
            print("🎯 现在系统已按AI原生架构正确实现，准备就绪")
        else:
            print(f"❌ 执行状态异常: {result.error_message}")
    else:
        print("❌ ContextAnalysisSkill类不存在")
        print("可用属性:", [attr for attr in dir(skills_module) if not attr.startswith('_')])

except Exception as e:
    print(f"❌ 验证失败: {e}")
    import traceback
    traceback.print_exc()