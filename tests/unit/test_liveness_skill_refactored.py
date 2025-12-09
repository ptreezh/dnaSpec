"""
Liveness技能重构测试
"""
import pytest
from src.dna_spec_kit_integration.skills.liveness_refactored import LivenessSkill


def test_liveness_skill_basic():
    """测试Liveness技能 - 基础级别"""
    skill = LivenessSkill()
    args = {
        "input": "test",
        "detail_level": "basic"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert result["data"] == "alive"
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "basic"


def test_liveness_skill_standard():
    """测试Liveness技能 - 标准级别"""
    skill = LivenessSkill()
    args = {
        "input": "test",
        "detail_level": "standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert result["data"] == "alive"
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "standard"


def test_liveness_skill_detailed():
    """测试Liveness技能 - 详细级别"""
    skill = LivenessSkill()
    args = {
        "input": "test",
        "detail_level": "detailed"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert result["data"] == "alive"
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "detailed"


def test_liveness_skill_default_detail_level():
    """测试Liveness技能使用默认详细级别"""
    skill = LivenessSkill()
    args = {
        "input": "test"
        # 没有指定detail_level，应该使用默认值"standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert result["metadata"]["detail_level"] == "standard"


def test_liveness_skill_missing_input():
    """测试Liveness技能处理缺失输入"""
    skill = LivenessSkill()
    args = {
        # 没有input参数
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "error"
    assert result["error"]["type"] == "VALIDATION_ERROR"
    assert "Input cannot be empty" in result["error"]["message"]


def test_liveness_skill_empty_input():
    """测试Liveness技能处理空输入"""
    skill = LivenessSkill()
    args = {
        "input": ""  # 空字符串
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "error"
    assert result["error"]["type"] == "VALIDATION_ERROR"
    assert "Input cannot be empty" in result["error"]["message"]