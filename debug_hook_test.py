# 调试Hook系统测试
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from src.dsgs_spec_kit_integration.core.hook import HookSystem, HookConfig, HookResult
    from src.dsgs_spec_kit_integration.core.skill import DSGSSkill, SkillResult, SkillStatus
    from src.dsgs_spec_kit_integration.core.manager import SkillManager
    from unittest.mock import Mock
    print("所有导入成功")
except ImportError as e:
    print("导入错误:", e)
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n=== 调试Hook系统测试 ===")

# 创建Hook系统
hook_system = HookSystem()

# 注册拦截器和处理器
def test_interceptor(request):
    return "设计" in request

def test_processor(request):
    return {"result": "intercepted_result", "skill_name": "intercepted_skill"}

hook_system.register_interceptor(test_interceptor)
hook_system.register_processor(test_processor)

print("拦截器和处理器注册完成")
print("拦截器数量:", len(hook_system._interceptors))
print("处理器数量:", len(hook_system._processors))

# 测试拦截器处理
print("\n测试拦截器处理:")
result = hook_system.intercept_request("设计一个新的系统")
print("结果:")
print(f"  intercepted: {result.intercepted}")
print(f"  handled: {result.handled}")
print(f"  skill_name: {result.skill_name}")
print(f"  error_message: '{result.error_message}'")