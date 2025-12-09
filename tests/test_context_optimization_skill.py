# tests/test_context_optimization_skill.py
import pytest
from src.dna_spec_kit_integration.core.skill import SkillStatus


def test_context_optimization_skill_inheritance():
    """RED: Test ContextOptimizationSkill inherits from DNASpecSkill"""
    from src.dna_context_engineering.skills_system_final import ContextOptimizationSkill
    from src.dna_spec_kit_integration.core.skill import DNASpecSkill
    
    skill = ContextOptimizationSkill()
    assert isinstance(skill, DNASpecSkill)


def test_context_optimization_basic_functionality():
    """RED: Test basic optimization functionality"""
    from src.dna_context_engineering.skills_system_final import ContextOptimizationSkill
    
    skill = ContextOptimizationSkill()
    context = "Design a system. Maybe it should work well."
    result = skill.process_request(context, {})
    
    assert result.status == SkillStatus.COMPLETED
    assert 'original_context' in result.result
    assert 'optimized_context' in result.result
    assert 'applied_optimizations' in result.result
    assert 'improvement_metrics' in result.result


def test_context_optimization_clarity_goal():
    """RED: Test optimization with clarity goal"""
    from src.dna_context_engineering.skills_system_final import ContextOptimizationSkill
    
    skill = ContextOptimizationSkill()
    context = "Needs to do things in a way that might work."
    result = skill.process_request(context, {'optimization_goals': ['clarity']})
    
    assert result.status == SkillStatus.COMPLETED
    # Should have applied optimizations for clarity


def test_context_optimization_completeness_goal():
    """RED: Test optimization with completeness goal"""
    from src.dna_context_engineering.skills_system_final import ContextOptimizationSkill
    
    skill = ContextOptimizationSkill()
    context = "System required."
    result = skill.process_request(context, {'optimization_goals': ['completeness']})
    
    assert result.status == SkillStatus.COMPLETED
    # Should have added missing elements


def test_context_optimization_multiple_goals():
    """RED: Test optimization with multiple goals"""
    from src.dna_context_engineering.skills_system_final import ContextOptimizationSkill
    
    skill = ContextOptimizationSkill()
    context = "System."
    goals = ['clarity', 'completeness', 'relevance']
    result = skill.process_request(context, {'optimization_goals': goals})
    
    assert result.status == SkillStatus.COMPLETED
    assert len(result.result['applied_optimizations']) > 0


def test_context_optimization_empty_context():
    """RED: Test optimization with empty context"""
    from src.dna_context_engineering.skills_system_final import ContextOptimizationSkill
    
    skill = ContextOptimizationSkill()
    result = skill.process_request("", {})
    
    assert result.status == SkillStatus.COMPLETED
    assert result.result['original_context'] == ""
    # For empty context, the optimization may add default content, which is acceptable
    # The important thing is that it doesn't crash and produces a result
    assert 'optimized_context' in result.result
    assert 'applied_optimizations' in result.result
    assert 'improvement_metrics' in result.result