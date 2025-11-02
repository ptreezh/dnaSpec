# 调试特定测试用例
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

print("\n=== 调试技能禁用测试 ===")

# 创建模拟技能管理器
mock_skill_manager = Mock()

# 创建Hook系统并注入模拟的技能管理器
hook_system_with_manager = HookSystem(mock_skill_manager)

# 启用技能并设置正常匹配结果
hook_system_with_manager.config.enable_skill("dsgs-architect")
mock_skill_manager.match_skill_intelligently.return_value = {
    'skill_name': 'dsgs-architect',
    'confidence': 0.8,
    'match_type': 'keyword'
}

# 禁用技能
hook_system_with_manager.config.disable_skill("dsgs-architect")

print("启用的技能:", hook_system_with_manager.config.enabled_skills)
print("技能是否启用:", hook_system_with_manager.config.is_skill_enabled("dsgs-architect"))

# 测试请求处理
result = hook_system_with_manager.intercept_request("分解任务")
print("结果:")
print(f"  intercepted: {result.intercepted}")
print(f"  handled: {result.handled}")
print(f"  skill_name: {result.skill_name}")
print(f"  error_message: '{result.error_message}'")

# 检查是否调用了match_skill_intelligently
print("是否调用了match_skill_intelligently:", mock_skill_manager.match_skill_intelligently.called)