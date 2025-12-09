# tests/test_context_analysis_skill.py
import pytest
from src.dnaspec_spec_kit_integration.core.skill import SkillStatus
from tests.conftest import context_analysis_skill, sample_context


def test_context_analysis_skill_inheritance(context_analysis_skill):
    """RED: Test that ContextAnalysisSkill properly inherits from DNASpecSkill"""
    # Should initially fail until we verify inheritance
    from src.context_engineering_skills.context_analysis import ContextAnalysisSkill
    from src.dnaspec_spec_kit_integration.core.skill import DNASpecSkill
    
    assert isinstance(context_analysis_skill, DNASpecSkill)


def test_context_analysis_skill_basic_functionality(context_analysis_skill, sample_context):
    """RED: Test basic analysis functionality"""
    # Should initially fail until implementation is complete
    result = context_analysis_skill.process_request(sample_context, {})
    
    assert result.status == SkillStatus.COMPLETED
    assert 'context_length' in result.result
    assert 'metrics' in result.result
    assert 'suggestions' in result.result
    assert 'issues' in result.result


def test_context_analysis_metrics_completeness(context_analysis_skill, sample_context):
    """RED: Test that all 5 metrics are present"""
    result = context_analysis_skill.process_request(sample_context, {})
    
    metrics = result.result['metrics']
    expected_metrics = ['clarity', 'relevance', 'completeness', 'consistency', 'efficiency']
    
    for metric in expected_metrics:
        assert metric in metrics
        assert 0.0 <= metrics[metric] <= 1.0


def test_context_analysis_empty_context(context_analysis_skill):
    """RED: Test empty context handling"""
    result = context_analysis_skill.process_request("", {})
    
    assert result.status == SkillStatus.COMPLETED
    assert result.result['context_length'] == 0
    assert all(result.result['metrics'][metric] == 0.0 for metric in result.result['metrics'])


def test_context_analysis_short_context(context_analysis_skill):
    """RED: Test very short context"""
    short_context = "Hi"
    result = context_analysis_skill.process_request(short_context, {})
    
    assert result.status == SkillStatus.COMPLETED
    assert result.result['context_length'] == 2
    # Should have appropriate metrics for short context


def test_context_analysis_long_context(context_analysis_skill):
    """RED: Test very long context (within limits)"""
    long_context = "Test. " * 1000  # 6000 chars
    result = context_analysis_skill.process_request(long_context, {})
    
    assert result.status == SkillStatus.COMPLETED
    assert result.result['context_length'] == 6000
    # Should handle long context without issues