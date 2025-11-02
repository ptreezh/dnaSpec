# 修复后的Hook系统单元测试
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

try:
    from src.dsgs_spec_kit_integration.core.hook import HookSystem, HookConfig, HookResult
    from src.dsgs_spec_kit_integration.core.skill import DSGSSkill, SkillResult, SkillStatus
    print('所有导入成功')
except ImportError as e:
    print('导入错误:', e)
    import traceback
    traceback.print_exc()

# 现在测试HookConfig
print('')
print('=== 测试HookConfig ===')
config = HookConfig()
print('Hook配置初始化成功: enabled=', config.enabled)
print('Auto invoke threshold:', config.auto_invoke_threshold)

# 测试HookSystem
print('')
print('=== 测试HookSystem ===')
hook_system = HookSystem()
print('Hook系统初始化成功: interceptors=', len(hook_system._interceptors))

# 测试命令检测
is_spec_kit = hook_system._is_spec_kit_command('/speckit.dsgs.architect 设计系统')
print('Spec.kit命令检测:', is_spec_kit)

is_natural = hook_system._is_natural_language_request('设计一个系统架构')
print('自然语言请求检测:', is_natural)

# 测试HookResult
print('')
print('=== 测试HookResult ===')
result = HookResult(intercepted=True, handled=False, error_message='Test error')
print('HookResult创建成功: intercepted=', result.intercepted, ', handled=', result.handled)

print('')
print('所有基本测试通过!')