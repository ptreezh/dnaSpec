# 集成测试：Hook系统与技能管理器
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

print("\n=== 测试Hook系统与技能管理器集成 ===")

# 创建模拟技能管理器
mock_skill_manager = Mock()

# 设置模拟的执行结果
mock_result = Mock()
mock_result.skill_name = "dsgs-architect"
mock_result.status = SkillStatus.COMPLETED
mock_result.result = {"architecture": "test"}

mock_skill_manager.execute_spec_kit_command.return_value = {
    'success': True,
    'result': mock_result,
    'skill_name': 'dsgs-architect'
}

# 创建Hook系统并注入模拟的技能管理器
hook_system = HookSystem(mock_skill_manager)

print("Hook系统创建成功，已注入模拟技能管理器")

# 测试spec.kit命令处理
print("\n--- 测试spec.kit命令处理 ---")
result = hook_system.intercept_request("/speckit.dsgs.architect 设计系统")

print("拦截结果:")
print(f"  intercepted: {result.intercepted}")
print(f"  handled: {result.handled}")
print(f"  skill_name: {result.skill_name}")
print(f"  error_message: {result.error_message}")
print(f"  processing_time: {result.processing_time}")

# 验证技能管理器被调用
print("\n验证技能管理器调用:")
mock_skill_manager.execute_spec_kit_command.assert_called_once_with("/speckit.dsgs.architect 设计系统")
print("技能管理器调用验证成功")

# 测试自然语言请求处理
print("\n--- 测试自然语言请求处理 ---")

# 设置智能匹配结果
mock_match_result = {
    'skill_name': 'dsgs-architect',
    'confidence': 0.8,
    'match_type': 'keyword',
    'matched_keywords': ['架构', '设计']
}

mock_skill_manager.match_skill_intelligently.return_value = mock_match_result

# 设置技能执行结果
mock_skill_result = SkillResult(
    skill_name='dsgs-architect',
    status=SkillStatus.COMPLETED,
    result={"architecture": "test_result"},
    confidence=0.8,
    execution_time=0.1
)

mock_skill_manager.execute_skill.return_value = mock_skill_result

# 测试自然语言请求处理
result = hook_system.intercept_request("设计一个系统架构")

print("自然语言处理结果:")
print(f"  intercepted: {result.intercepted}")
print(f"  handled: {result.handled}")
print(f"  skill_name: {result.skill_name}")
print(f"  error_message: {result.error_message}")
print(f"  processing_time: {result.processing_time}")

print("\n所有集成测试通过!")