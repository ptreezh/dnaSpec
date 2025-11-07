
import pytest
from dsgs_spec_kit_integration.core.skill_manager import SkillManager

def test_skill_manager_executes_existing_skill():
    """测试SkillManager能否成功执行一个存在的技能。"""
    manager = SkillManager()
    result = manager.execute_skill("liveness", {})
    assert result == "alive"

def test_skill_manager_handles_nonexistent_skill():
    """测试当技能不存在时，SkillManager是否会引发ValueError。"""
    manager = SkillManager()
    with pytest.raises(ValueError, match="Skill 'nonexistent_skill' not found."):
        manager.execute_skill("nonexistent_skill", {})

def test_skill_manager_handles_skill_without_execute_function(mocker):
    """测试当技能模块没有execute函数时，是否会引发ValueError。"""
    # 模拟一个没有execute函数的模块
    mocker.patch('importlib.import_module', return_value=object())
    
    manager = SkillManager()
    with pytest.raises(ValueError, match="Skill 'some_skill' does not have an 'execute' function."):
        manager.execute_skill("some_skill", {})
