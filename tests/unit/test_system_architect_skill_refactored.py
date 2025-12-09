"""
系统架构师技能重构测试
"""
import pytest
from src.dna_spec_kit_integration.skills.system_architect_refactored import SystemArchitectSkill


def test_system_architect_skill_basic():
    """测试系统架构师技能 - 基础级别"""
    skill = SystemArchitectSkill()
    args = {
        "input": "设计一个电商网站",
        "detail_level": "basic"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert "architecture_type" in result["data"]
    assert "recommended_tech_stack" in result["data"]
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "basic"


def test_system_architect_skill_standard():
    """测试系统架构师技能 - 标准级别"""
    skill = SystemArchitectSkill()
    args = {
        "input": "设计一个电商网站",
        "detail_level": "standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert "architecture_type" in result["data"]
    assert "recommended_tech_stack" in result["data"]
    assert "identified_modules" in result["data"]
    assert "defined_interfaces" in result["data"]
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "standard"


def test_system_architect_skill_detailed():
    """测试系统架构师技能 - 详细级别"""
    skill = SystemArchitectSkill()
    args = {
        "input": "设计一个电商网站",
        "detail_level": "detailed"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert "input_requirements" in result["data"]
    assert "architecture_type" in result["data"]
    assert "recommended_tech_stack" in result["data"]
    assert "identified_modules" in result["data"]
    assert "defined_interfaces" in result["data"]
    assert "architecture_recommendations" in result["data"]
    assert "potential_issues" in result["data"]
    assert "implementation_guidance" in result["data"]
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "detailed"


def test_system_architect_skill_microservices():
    """测试系统架构师技能 - 微服务架构"""
    skill = SystemArchitectSkill()
    args = {
        "input": "为一个大型电商平台设计微服务架构，包含用户服务、产品服务、订单服务，需要服务拆分和独立部署",
        "detail_level": "standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert result["data"]["architecture_type"] == "microservices"


def test_system_architect_skill_high_availability():
    """测试系统架构师技能 - 高可用性系统"""
    skill = SystemArchitectSkill()
    args = {
        "input": "设计一个金融交易系统，要求99.99%可用性，高安全性，需要容错和灾备",
        "detail_level": "standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert "architecture_recommendations" in result["data"]
    # 应该包含高可用性相关的建议
    recommendations = result["data"]["architecture_recommendations"]
    # 检查是否包含"redundancy"关键词
    assert any("redundancy" in rec.lower() for rec in recommendations)


def test_system_architect_skill_default_detail_level():
    """测试系统架构师技能使用默认详细级别"""
    skill = SystemArchitectSkill()
    args = {
        "input": "设计一个电商网站"
        # 没有指定detail_level，应该使用默认值"standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert result["metadata"]["detail_level"] == "standard"


def test_system_architect_skill_missing_input():
    """测试系统架构师技能处理缺失输入"""
    skill = SystemArchitectSkill()
    args = {
        # 没有input参数
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "error"
    assert result["error"]["type"] == "VALIDATION_ERROR"
    assert "Input cannot be empty" in result["error"]["message"]


def test_system_architect_skill_empty_input():
    """测试系统架构师技能处理空输入"""
    skill = SystemArchitectSkill()
    args = {
        "input": ""  # 空字符串
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "error"
    assert result["error"]["type"] == "VALIDATION_ERROR"
    assert "Input cannot be empty" in result["error"]["message"]