# test_actual_skills.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

print("Testing actual skill classes...")

try:
    from src.dnaspec_context_engineering.skills_system_real import ContextAnalysisSkill
    print("✅ ContextAnalysisSkill imported")
    
    analysis_skill = ContextAnalysisSkill()
    print("✅ ContextAnalysisSkill instantiated")
    
    result = analysis_skill.execute_with_ai("测试上下文内容", {})
    print(f"✅ ContextAnalysisSkill.execute_with_ai works: {type(result)}")
    print(f"   Result success: {result.get('success', False)}")
except Exception as e:
    print(f"❌ Error in ContextAnalysisSkill: {e}")
    import traceback
    traceback.print_exc()

try:
    from src.dnaspec_context_engineering.skills_system_real import ContextOptimizationSkill
    print("✅ ContextOptimizationSkill imported")
    
    optimization_skill = ContextOptimizationSkill()
    print("✅ ContextOptimizationSkill instantiated")
    
    result = optimization_skill.execute_with_ai("简单上下文", {})
    print(f"✅ ContextOptimizationSkill.execute_with_ai works: {type(result)}")
    print(f"   Result success: {result.get('success', False)}")
except Exception as e:
    print(f"❌ Error in ContextOptimizationSkill: {e}")
    import traceback
    traceback.print_exc()

try:
    from src.dnaspec_context_engineering.skills_system_real import CognitiveTemplateSkill
    print("✅ CognitiveTemplateSkill imported")
    
    template_skill = CognitiveTemplateSkill()
    print("✅ CognitiveTemplateSkill instantiated")
    
    result = template_skill.execute_with_ai("测试任务", {})
    print(f"✅ CognitiveTemplateSkill.execute_with_ai works: {type(result)}")
    print(f"   Result success: {result.get('success', False) and result['result'].get('success', True)}")
except Exception as e:
    print(f"❌ Error in CognitiveTemplateSkill: {e}")
    import traceback
    traceback.print_exc()