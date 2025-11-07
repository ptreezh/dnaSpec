# tests/test_cognitive_template_skill.py
import pytest
from src.dsgs_spec_kit_integration.core.skill import SkillStatus


def test_cognitive_template_skill_inheritance():
    """RED: Test CognitiveTemplateSkill inherits from DSGSSkill"""
    from src.context_engineering_skills.cognitive_template import CognitiveTemplateSkill
    from src.dsgs_spec_kit_integration.core.skill import DSGSSkill
    
    skill = CognitiveTemplateSkill()
    assert isinstance(skill, DSGSSkill)


def test_cognitive_template_basic_functionality():
    """RED: Test basic template functionality"""
    from src.context_engineering_skills.cognitive_template import CognitiveTemplateSkill
    
    skill = CognitiveTemplateSkill()
    context = "How to improve system performance?"
    result = skill.process_request(context, {'template': 'chain_of_thought'})
    
    assert result.status == SkillStatus.COMPLETED
    assert 'enhanced_context' in result.result
    assert 'structure' in result.result
    assert result.result['success'] is True


def test_cognitive_template_chain_of_thought():
    """RED: Test chain of thought template"""
    from src.context_engineering_skills.cognitive_template import CognitiveTemplateSkill
    
    skill = CognitiveTemplateSkill()
    context = "Solve this problem."
    result = skill.process_request(context, {'template': 'chain_of_thought'})
    
    assert result.status == SkillStatus.COMPLETED
    enhanced = result.result['enhanced_context']
    assert "问题理解" in enhanced or "Problem Understanding" in enhanced  # or English equivalent


def test_cognitive_template_few_shot():
    """RED: Test few shot template"""
    from src.context_engineering_skills.cognitive_template import CognitiveTemplateSkill
    
    skill = CognitiveTemplateSkill()
    context = "Classify this."
    result = skill.process_request(context, {'template': 'few_shot'})
    
    assert result.status == SkillStatus.COMPLETED
    enhanced = result.result['enhanced_context']
    assert "示例" in enhanced or "Example" in enhanced


def test_cognitive_template_verification():
    """RED: Test verification template"""
    from src.context_engineering_skills.cognitive_template import CognitiveTemplateSkill
    
    skill = CognitiveTemplateSkill()
    context = "Validate this claim."
    result = skill.process_request(context, {'template': 'verification'})
    
    assert result.status == SkillStatus.COMPLETED
    enhanced = result.result['enhanced_context']
    assert "验证" in enhanced or "Verification" in enhanced


def test_cognitive_template_unknown_template():
    """RED: Test unknown template handling"""
    from src.context_engineering_skills.cognitive_template import CognitiveTemplateSkill
    
    skill = CognitiveTemplateSkill()
    context = "Test context"
    result = skill.process_request(context, {'template': 'unknown_template'})
    
    assert result.status == SkillStatus.COMPLETED
    assert result.result['success'] is False
    assert 'available_templates' in result.result


def test_cognitive_template_empty_context():
    """RED: Test template with empty context"""
    from src.context_engineering_skills.cognitive_template import CognitiveTemplateSkill
    
    skill = CognitiveTemplateSkill()
    result = skill.process_request("", {'template': 'chain_of_thought'})
    
    assert result.status == SkillStatus.COMPLETED
    # Should handle empty context gracefully