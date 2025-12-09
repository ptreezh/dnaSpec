"""
上下文优化技能重构测试
"""
import pytest
from src.dna_spec_kit_integration.skills.context_optimization_refactored import ContextOptimizationSkill


def test_context_optimization_skill_basic():
    """测试上下文优化技能 - 基础级别"""
    skill = ContextOptimizationSkill()
    args = {
        "input": "请设计一个电商网站",
        "detail_level": "basic"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert "optimized_context" in result["data"]
    assert "main_optimizations" in result["data"]
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "basic"


def test_context_optimization_skill_standard():
    """测试上下文优化技能 - 标准级别"""
    skill = ContextOptimizationSkill()
    args = {
        "input": "请设计一个电商网站",
        "detail_level": "standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert "optimized_context" in result["data"]
    assert "applied_optimizations" in result["data"]
    assert "improvement_metrics" in result["data"]
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "standard"


def test_context_optimization_skill_detailed():
    """测试上下文优化技能 - 详细级别"""
    skill = ContextOptimizationSkill()
    args = {
        "input": "请设计一个电商网站",
        "detail_level": "detailed"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert "original_context" in result["data"]
    assert "optimized_context" in result["data"]
    assert "applied_optimizations" in result["data"]
    assert "improvement_metrics" in result["data"]
    assert "optimization_summary" in result["data"]
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "detailed"


def test_context_optimization_skill_with_custom_goals():
    """测试上下文优化技能 - 自定义优化目标"""
    skill = ContextOptimizationSkill()
    args = {
        "input": "请设计一个电商网站",
        "options": {
            "optimization_goals": ["clarity", "conciseness"]
        },
        "detail_level": "standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert "optimized_context" in result["data"]
    assert "applied_optimizations" in result["data"]


def test_context_optimization_skill_default_detail_level():
    """测试上下文优化技能使用默认详细级别"""
    skill = ContextOptimizationSkill()
    args = {
        "input": "请设计一个电商网站"
        # 没有指定detail_level，应该使用默认值"standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert result["metadata"]["detail_level"] == "standard"


def test_context_optimization_skill_missing_input():
    """测试上下文优化技能处理缺失输入"""
    skill = ContextOptimizationSkill()
    args = {
        # 没有input参数
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "error"
    assert result["error"]["type"] == "VALIDATION_ERROR"
    assert "Input cannot be empty" in result["error"]["message"]


def test_context_optimization_skill_empty_input():
    """测试上下文优化技能处理空输入"""
    skill = ContextOptimizationSkill()
    args = {
        "input": ""  # 空字符串
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "error"
    assert result["error"]["type"] == "VALIDATION_ERROR"
    assert "Input cannot be empty" in result["error"]["message"]