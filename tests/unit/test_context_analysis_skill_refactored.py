"""
上下文分析技能重构测试
"""
import pytest
from src.dna_spec_kit_integration.skills.context_analysis_refactored import ContextAnalysisSkill


def test_context_analysis_skill_basic():
    """测试上下文分析技能 - 基础级别"""
    skill = ContextAnalysisSkill()
    args = {
        "input": "请设计一个电商网站",
        "detail_level": "basic"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert "overall_score" in result["data"]
    assert "main_issues" in result["data"]
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "basic"


def test_context_analysis_skill_standard():
    """测试上下文分析技能 - 标准级别"""
    skill = ContextAnalysisSkill()
    args = {
        "input": "请设计一个电商网站",
        "detail_level": "standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert "overall_score" in result["data"]
    assert "metrics" in result["data"]
    assert "issues" in result["data"]
    assert "suggestions" in result["data"]
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "standard"


def test_context_analysis_skill_detailed():
    """测试上下文分析技能 - 详细级别"""
    skill = ContextAnalysisSkill()
    args = {
        "input": "请设计一个电商网站",
        "detail_level": "detailed"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert "overall_score" in result["data"]
    assert "metrics" in result["data"]
    assert "issues" in result["data"]
    assert "suggestions" in result["data"]
    assert "detailed_analysis" in result["data"]
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "detailed"


def test_context_analysis_skill_default_detail_level():
    """测试上下文分析技能使用默认详细级别"""
    skill = ContextAnalysisSkill()
    args = {
        "input": "请设计一个电商网站"
        # 没有指定detail_level，应该使用默认值"standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert result["metadata"]["detail_level"] == "standard"


def test_context_analysis_skill_missing_input():
    """测试上下文分析技能处理缺失输入"""
    skill = ContextAnalysisSkill()
    args = {
        # 没有input参数
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "error"
    assert result["error"]["type"] == "VALIDATION_ERROR"
    assert "Input cannot be empty" in result["error"]["message"]


def test_context_analysis_skill_empty_input():
    """测试上下文分析技能处理空输入"""
    skill = ContextAnalysisSkill()
    args = {
        "input": ""  # 空字符串
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "error"
    assert result["error"]["type"] == "VALIDATION_ERROR"
    assert "Input cannot be empty" in result["error"]["message"]


def test_context_analysis_skill_confidence_calculation():
    """测试上下文分析技能置信度计算"""
    skill = ContextAnalysisSkill()
    
    # 短输入应该有较低置信度
    args_short = {"input": "hi"}
    result_short = skill.execute(args_short)
    
    # 长输入应该有较高置信度
    args_long = {"input": "这是一个很长的输入文本，应该会有更高的置信度"}
    result_long = skill.execute(args_long)
    
    assert result_short["status"] == "success"
    assert result_long["status"] == "success"
    # 长输入的置信度应该高于短输入
    assert result_long["metadata"]["confidence"] >= result_short["metadata"]["confidence"]