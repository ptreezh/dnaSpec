import sys
sys.path.append('.')

# 看看是否有execute_with_ai方法
try:
    from src.dsgs_context_engineering.skills_system_real import ContextAnalysisSkill
    skill_class = ContextAnalysisSkill
    print("Class methods:", [m for m in dir(skill_class) if not m.startswith('_')])
    
    # 尝试实例化
    skill = skill_class()
    print("Instance methods:", [m for m in dir(skill) if not m.startswith('_')])
    print("Has execute_with_ai:", hasattr(skill, 'execute_with_ai'))
    print("Has process_request:", hasattr(skill, 'process_request'))
    print("Name:", getattr(skill, 'name', 'No name'))
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()