"""
认知模板技能重构测试
"""
import pytest
from src.dna_spec_kit_integration.skills.cognitive_template_refactored import CognitiveTemplateSkill


def test_cognitive_template_skill_basic():
    """测试认知模板技能 - 基础级别"""
    skill = CognitiveTemplateSkill()
    args = {
        "input": "请设计一个电商网站",
        "detail_level": "basic"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert "template_type" in result["data"]
    assert "enhanced_context" in result["data"]
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "basic"


def test_cognitive_template_skill_standard_chain_of_thought():
    """测试认知模板技能 - 标准级别思维链模板"""
    skill = CognitiveTemplateSkill()
    args = {
        "input": "请设计一个电商网站",
        "options": {
            "template": "chain_of_thought"
        },
        "detail_level": "standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert result["data"]["template_type"] == "chain_of_thought"
    assert "template_description" in result["data"]
    assert "enhanced_context" in result["data"]
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "standard"


def test_cognitive_template_skill_detailed_few_shot():
    """测试认知模板技能 - 详细级别少样本模板"""
    skill = CognitiveTemplateSkill()
    args = {
        "input": "请设计一个电商网站",
        "options": {
            "template": "few_shot"
        },
        "detail_level": "detailed"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert result["data"]["template_type"] == "few_shot"
    assert "template_description" in result["data"]
    assert "enhanced_context" in result["data"]
    assert "template_structure" in result["data"]
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "detailed"


def test_cognitive_template_skill_with_role():
    """测试认知模板技能 - 指定角色"""
    skill = CognitiveTemplateSkill()
    args = {
        "input": "请设计一个电商网站",
        "options": {
            "template": "role_playing",
            "role": "架构师"
        },
        "detail_level": "standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert result["data"]["template_type"] == "role_playing"
    assert "enhanced_context" in result["data"]


def test_cognitive_template_skill_invalid_template():
    """测试认知模板技能 - 无效模板类型"""
    skill = CognitiveTemplateSkill()
    args = {
        "input": "请设计一个电商网站",
        "options": {
            "template": "invalid_template"
        },
        "detail_level": "standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"  # 技能执行成功，但返回错误信息
    assert "data" in result
    assert result["data"]["success"] == False
    assert "error" in result["data"]


def test_cognitive_template_skill_default_detail_level():
    """测试认知模板技能使用默认详细级别"""
    skill = CognitiveTemplateSkill()
    args = {
        "input": "请设计一个电商网站"
        # 没有指定detail_level，应该使用默认值"standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert result["metadata"]["detail_level"] == "standard"


def test_cognitive_template_skill_missing_input():
    """测试认知模板技能处理缺失输入"""
    skill = CognitiveTemplateSkill()
    args = {
        # 没有input参数
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "error"
    assert result["error"]["type"] == "VALIDATION_ERROR"
    assert "Input cannot be empty" in result["error"]["message"]


def test_cognitive_template_skill_empty_input():
    """测试认知模板技能处理空输入"""
    skill = CognitiveTemplateSkill()
    args = {
        "input": ""  # 空字符串
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "error"
    assert result["error"]["type"] == "VALIDATION_ERROR"
    assert "Input cannot be empty" in result["error"]["message"]