
from dnaspec_spec_kit_integration.core.skill_manager import SkillManager

def test_liveness_skill_end_to_end():
    """
    测试从技能管理器调用liveness技能的完整流程。
    """
    # 1. 初始化技能管理器
    skill_manager = SkillManager()
    
    # 2. 模拟执行'liveness'技能
    result = skill_manager.execute_skill("liveness", {})
    
    # 3. 验证结果
    assert result == "alive"
