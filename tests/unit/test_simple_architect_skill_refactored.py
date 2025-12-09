"""
Simple Architect技能重构测试
"""
import pytest
from src.dna_spec_kit_integration.skills.simple_architect_refactored import SimpleArchitectSkill


def test_simple_architect_skill_basic_ecommerce():
    """测试Simple Architect技能 - 电商网站基础级别"""
    skill = SimpleArchitectSkill()
    args = {
        "input": "我想要一个简单的电商网站",
        "detail_level": "basic"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert result["data"] == "[WebApp] -> [API Server] -> [Database]"
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "basic"


def test_simple_architect_skill_standard_blog():
    """测试Simple Architect技能 - 博客系统标准级别"""
    skill = SimpleArchitectSkill()
    args = {
        "input": "一个个人博客",
        "detail_level": "standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert result["data"] == "[WebApp] -> [Database]"
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "standard"


def test_simple_architect_skill_detailed_unknown():
    """测试Simple Architect技能 - 未知需求详细级别"""
    skill = SimpleArchitectSkill()
    args = {
        "input": "一个游戏应用",
        "detail_level": "detailed"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert result["data"] == ""
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "detailed"


def test_simple_architect_skill_default_detail_level():
    """测试Simple Architect技能使用默认详细级别"""
    skill = SimpleArchitectSkill()
    args = {
        "input": "电商网站"
        # 没有指定detail_level，应该使用默认值"standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert result["metadata"]["detail_level"] == "standard"


def test_simple_architect_skill_missing_input():
    """测试Simple Architect技能处理缺失输入"""
    skill = SimpleArchitectSkill()
    args = {
        # 没有input参数
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "error"
    assert result["error"]["type"] == "VALIDATION_ERROR"
    assert "Input cannot be empty" in result["error"]["message"]


def test_simple_architect_skill_empty_input():
    """测试Simple Architect技能处理空输入"""
    skill = SimpleArchitectSkill()
    args = {
        "input": ""  # 空字符串
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "error"
    assert result["error"]["type"] == "VALIDATION_ERROR"
    assert "Input cannot be empty" in result["error"]["message"]


def test_simple_architect_skill_case_insensitive():
    """测试Simple Architect技能大小写不敏感"""
    skill = SimpleArchitectSkill()
    args = {
        "input": "电子商务平台"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert result["data"] == "[WebApp] -> [API Server] -> [Database]"