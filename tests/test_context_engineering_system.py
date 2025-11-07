# tests/test_context_engineering_system.py
"""
System-level integration tests for the Context Engineering Skills System
"""
import pytest
from src.dsgs_spec_kit_integration.core.skill import SkillStatus
from tests.conftest import (
    context_analysis_skill, context_optimization_skill, 
    cognitive_template_skill, context_engineering_system, skills_manager
)


def test_system_overall_integration(
    context_analysis_skill, 
    context_optimization_skill, 
    cognitive_template_skill
):
    """Test that all context engineering skills work together"""
    
    # Test 1: Context Analysis
    analysis_result = context_analysis_skill.process_request(
        "Design a system for e-commerce that handles user authentication and payment processing.",
        {}
    )
    
    assert analysis_result.status == SkillStatus.COMPLETED
    assert analysis_result.result['context_length'] > 0
    assert 'metrics' in analysis_result.result
    assert len(analysis_result.result['metrics']) == 5  # clarity, relevance, completeness, consistency, efficiency
    
    # Test 2: Context Optimization
    optimization_result = context_optimization_skill.process_request(
        "System needed for e-commerce. Need authentication and payments.",
        {'optimization_goals': ['clarity', 'completeness']}
    )
    
    assert optimization_result.status == SkillStatus.COMPLETED
    assert optimization_result.result['original_context'] != optimization_result.result['optimized_context']
    assert 'applied_optimizations' in optimization_result.result
    
    # Test 3: Cognitive Template
    template_result = cognitive_template_skill.process_request(
        "How should we structure the e-commerce system?",
        {'template': 'chain_of_thought'}
    )
    
    assert template_result.status == SkillStatus.COMPLETED
    assert template_result.result['success'] is True
    assert 'enhanced_context' in template_result.result


def test_skills_manager_integration(skills_manager):
    """Test Skills Manager can coordinate different skills"""
    # The manager itself would coordinate skills, for now just test instantiation
    from src.context_engineering_skills.skills_manager import ContextEngineeringSkillsManager
    assert isinstance(skills_manager, ContextEngineeringSkillsManager)


def test_error_handling_consistency(
    context_analysis_skill, 
    context_optimization_skill, 
    cognitive_template_skill
):
    """Test that all skills handle errors consistently"""
    
    # All skills should handle empty context gracefully
    analysis_result = context_analysis_skill.process_request("", {})
    optimization_result = context_optimization_skill.process_request("", {})
    template_result = cognitive_template_skill.process_request("", {'template': 'chain_of_thought'})
    
    # All should complete without errors
    assert analysis_result.status == SkillStatus.COMPLETED
    assert optimization_result.status == SkillStatus.COMPLETED
    assert template_result.status == SkillStatus.COMPLETED


def test_performance_under_load(context_analysis_skill):
    """Test that skills perform well under typical loads"""
    import time
    
    # Test with moderately sized contexts
    test_context = "This is a test context for performance evaluation. " * 500  # ~30K chars
    
    start_time = time.time()
    result = context_analysis_skill.process_request(test_context, {})
    end_time = time.time()
    
    assert result.status == SkillStatus.COMPLETED
    assert (end_time - start_time) < 2.0  # Should complete in under 2 seconds


def test_metric_ranges_consistency(context_analysis_skill):
    """Test that all metrics return values in expected range [0.0, 1.0]"""
    test_context = "This is a reasonably well-formed context for testing metrics."
    
    result = context_analysis_skill.process_request(test_context, {})
    
    assert result.status == SkillStatus.COMPLETED
    metrics = result.result['metrics']
    
    for metric_name, score in metrics.items():
        assert 0.0 <= score <= 1.0, f"Metric {metric_name} score {score} not in range [0.0, 1.0]"