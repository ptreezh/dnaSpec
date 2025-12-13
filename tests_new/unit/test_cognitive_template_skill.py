"""
Unit tests for Cognitive Template Skill following TDD approach
"""
import pytest
from typing import Dict, Any

# Import the skill to be tested
from src.dna_context_engineering.skills_system_final import CognitiveTemplateSkill


class TestCognitiveTemplateSkill:
    """Test cases for CognitiveTemplateSkill"""

    def test_skill_initialization(self):
        """Test that CognitiveTemplateSkill initializes correctly"""
        skill = CognitiveTemplateSkill()
        
        assert skill.name == "dnaspec-cognitive-template"
        assert "Cognitive Template Skill" in skill.description
        assert "AI model native intelligence" in skill.description
        assert hasattr(skill, 'templates')
        assert isinstance(skill.templates, dict)

    def test_process_request_with_valid_context_default_template(self):
        """Test processing a valid context with default template"""
        skill = CognitiveTemplateSkill()
        test_context = "How to solve this problem?"
        
        result = skill.process_request(test_context, {})
        
        # Verify the result structure
        assert result.status.name == "COMPLETED"
        template_result = result.result if isinstance(result.result, dict) else result.result['result']
        
        # Check required fields in the result
        assert 'success' in template_result
        assert 'template_type' in template_result
        assert 'template_description' in template_result
        assert 'original_context' in template_result
        assert 'enhanced_context' in template_result
        assert 'template_structure' in template_result
        assert 'confidence' in template_result
        
        # Verify values
        assert template_result['success'] is True
        assert template_result['template_type'] == 'chain_of_thought'  # Default
        assert template_result['original_context'] == test_context
        assert isinstance(template_result['enhanced_context'], str)
        assert isinstance(template_result['template_structure'], list)
        assert 0.0 <= template_result['confidence'] <= 1.0

    def test_process_request_empty_context(self):
        """Test processing an empty context"""
        skill = CognitiveTemplateSkill()
        
        result = skill.process_request("", {})
        
        # Verify the result structure for empty context
        assert result.status.name == "COMPLETED"
        template_result = result.result if isinstance(result.result, dict) else result.result['result']
        
        assert template_result['success'] is False
        assert 'error' in template_result
        assert template_result['original_context'] == ""
        assert template_result['enhanced_context'] == ""

    def test_process_request_with_chain_of_thought_template(self):
        """Test processing with chain of thought template"""
        skill = CognitiveTemplateSkill()
        test_context = "How to improve system performance?"
        
        params = {'template': 'chain_of_thought'}
        
        result = skill.process_request(test_context, params)
        
        assert result.status.name == "COMPLETED"
        template_result = result.result if isinstance(result.result, dict) else result.result['result']
        
        assert template_result['success'] is True
        assert template_result['template_type'] == 'chain_of_thought'
        assert 'Chain-of-Thought' in template_result['template_description']
        assert test_context in template_result['original_context']
        assert isinstance(template_result['enhanced_context'], str)
        assert 'Chain-of-Thought Cognitive Template Application' in template_result['enhanced_context']

    def test_process_request_with_few_shot_template(self):
        """Test processing with few-shot template"""
        skill = CognitiveTemplateSkill()
        test_context = "How to implement user authentication?"
        
        params = {'template': 'few_shot'}
        
        result = skill.process_request(test_context, params)
        
        assert result.status.name == "COMPLETED"
        template_result = result.result if isinstance(result.result, dict) else result.result['result']
        
        assert template_result['success'] is True
        assert template_result['template_type'] == 'few_shot'
        assert 'Few-Shot' in template_result['template_description']
        assert test_context in template_result['original_context']
        assert isinstance(template_result['enhanced_context'], str)
        assert 'Few-Shot Learning Cognitive Template Application' in template_result['enhanced_context']

    def test_process_request_with_verification_template(self):
        """Test processing with verification template"""
        skill = CognitiveTemplateSkill()
        test_context = "Verify this implementation approach"
        
        params = {'template': 'verification'}
        
        result = skill.process_request(test_context, params)
        
        assert result.status.name == "COMPLETED"
        template_result = result.result if isinstance(result.result, dict) else result.result['result']
        
        assert template_result['success'] is True
        assert template_result['template_type'] == 'verification'
        assert 'Verification' in template_result['template_description']
        assert test_context in template_result['original_context']
        assert isinstance(template_result['enhanced_context'], str)
        assert 'Verification Check Cognitive Template Application' in template_result['enhanced_context']

    def test_process_request_with_invalid_template(self):
        """Test processing with an invalid template name"""
        skill = CognitiveTemplateSkill()
        test_context = "Test context"
        
        params = {'template': 'invalid_template'}
        
        result = skill.process_request(test_context, params)
        
        # Should fail gracefully with error message
        assert result.status.name == "COMPLETED"  # Still completed, but with error
        template_result = result.result if isinstance(result.result, dict) else result.result['result']
        
        assert template_result['success'] is False
        assert 'error' in template_result
        assert 'invalid_template' in template_result['error']
        assert test_context in template_result['original_context']

    def test_skill_execute_logic_direct_default(self):
        """Test the execute skill logic directly with default template"""
        skill = CognitiveTemplateSkill()
        test_context = "Problem to solve"
        
        # Call the internal method directly with default context
        result = skill._execute_skill_logic(test_context, {})
        
        # Should return a dict with the expected structure
        assert isinstance(result, dict)
        assert result['success'] is True
        assert result['template_type'] == 'chain_of_thought'

    def test_skill_execute_logic_direct_specific_template(self):
        """Test the execute skill logic directly with specific template"""
        skill = CognitiveTemplateSkill()
        test_context = "Design question"
        
        # Call the internal method directly with template context
        result = skill._execute_skill_logic(test_context, {'template': 'verification'})
        
        # Should return a dict with the expected structure
        assert isinstance(result, dict)
        assert result['success'] is True
        assert result['template_type'] == 'verification'

    def test_available_templates(self):
        """Test that all expected templates are available"""
        skill = CognitiveTemplateSkill()
        
        expected_templates = {
            'chain_of_thought', 'few_shot', 'verification', 'role_playing', 'understanding'
        }
        actual_templates = set(skill.templates.keys())
        
        assert expected_templates.issubset(actual_templates)

    def test_calculate_confidence_short_input(self):
        """Test confidence calculation for different input lengths"""
        skill = CognitiveTemplateSkill()
        
        # Short input
        short_result = skill.process_request("Hi", {})
        short_analysis = short_result.result if isinstance(short_result.result, dict) else short_result.result['result']
        
        # Longer input
        long_result = skill.process_request("This is a much longer context for cognitive template application", {})
        long_analysis = long_result.result if isinstance(long_result.result, dict) else long_result.result['result']
        
        # Both should return valid confidence values
        assert 0.0 <= short_analysis['confidence'] <= 1.0
        assert 0.0 <= long_analysis['confidence'] <= 1.0


if __name__ == "__main__":
    # Run the tests directly if this file is executed
    pytest.main([__file__, "-v"])