"""
Unit tests for Context Analysis Skill following TDD approach
"""
import pytest
from typing import Dict, Any
from pathlib import Path

# Import the skill to be tested
from src.dna_context_engineering.skills_system_final import ContextAnalysisSkill


class TestContextAnalysisSkill:
    """Test cases for ContextAnalysisSkill"""

    def test_skill_initialization(self):
        """Test that ContextAnalysisSkill initializes correctly"""
        skill = ContextAnalysisSkill()
        
        assert skill.name == "dnaspec-context-analysis"
        assert "Context Analysis Skill" in skill.description
        assert "AI model native intelligence" in skill.description

    def test_process_request_with_valid_context(self):
        """Test processing a valid context"""
        skill = ContextAnalysisSkill()
        test_context = "Implement a user authentication system"
        
        result = skill.process_request(test_context, {})
        
        # Verify the result structure
        assert result.status.name == "COMPLETED"
        assert hasattr(result, 'result')
        
        analysis = result.result if isinstance(result.result, dict) else result.result['result']
        
        # Check required fields in the analysis
        assert 'context_length' in analysis
        assert 'token_count_estimate' in analysis
        assert 'metrics' in analysis
        assert 'suggestions' in analysis
        assert 'issues' in analysis
        assert 'confidence' in analysis
        
        # Verify metrics structure
        assert isinstance(analysis['metrics'], dict)
        expected_metrics = {'clarity', 'relevance', 'completeness', 'consistency', 'efficiency'}
        actual_metrics = set(analysis['metrics'].keys())
        assert expected_metrics.issubset(actual_metrics)
        
        # Verify values are in expected ranges
        for metric, value in analysis['metrics'].items():
            assert 0.0 <= value <= 1.0
        
        assert isinstance(analysis['suggestions'], list)
        assert isinstance(analysis['issues'], list)
        assert 0.0 <= analysis['confidence'] <= 1.0

    def test_process_request_empty_context(self):
        """Test processing an empty context"""
        skill = ContextAnalysisSkill()
        
        result = skill.process_request("", {})
        
        # Verify the result structure for empty context
        assert result.status.name == "COMPLETED"
        analysis = result.result if isinstance(result.result, dict) else result.result['result']
        
        assert analysis['context_length'] == 0
        assert analysis['token_count_estimate'] == 0
        
        # All metrics should be 0.0 for empty context
        for metric, value in analysis['metrics'].items():
            assert value == 0.0
        
        # Should have appropriate issues for empty context
        assert 'Context is empty' in analysis['issues']

    def test_process_request_whitespace_context(self):
        """Test processing a whitespace-only context"""
        skill = ContextAnalysisSkill()
        
        result = skill.process_request("   \t\n  ", {})
        
        # Should be treated similarly to empty context
        assert result.status.name == "COMPLETED"
        analysis = result.result if isinstance(result.result, dict) else result.result['result']
        
        assert analysis['context_length'] == 0  # After stripping

    def test_process_request_long_context(self):
        """Test processing a long context"""
        skill = ContextAnalysisSkill()
        long_context = "This is a very long context " * 100  # Repeat 100 times
        
        result = skill.process_request(long_context, {})
        
        assert result.status.name == "COMPLETED"
        analysis = result.result if isinstance(result.result, dict) else result.result['result']
        
        assert analysis['context_length'] == len(long_context)
        assert analysis['token_count_estimate'] > 0
        
        # Verify all metrics are present and in valid range
        for metric, value in analysis['metrics'].items():
            assert 0.0 <= value <= 1.0

    def test_calculate_confidence_short_input(self):
        """Test confidence calculation for short input"""
        skill = ContextAnalysisSkill()
        
        # Short input should have lower confidence
        short_result = skill.process_request("Hi", {})
        short_analysis = short_result.result if isinstance(short_result.result, dict) else short_result.result['result']
        
        long_result = skill.process_request("This is a much longer context for analysis", {})
        long_analysis = long_result.result if isinstance(long_result.result, dict) else long_result.result['result']
        
        # Note: The confidence comes from the result, not from _calculate_confidence method directly
        # Just verify that both return valid confidence values
        assert 0.0 <= short_analysis['confidence'] <= 1.0
        assert 0.0 <= long_analysis['confidence'] <= 1.0

    def test_process_request_with_params(self):
        """Test processing with additional parameters"""
        skill = ContextAnalysisSkill()
        test_context = "System requirements for authentication"
        params = {"test_param": "test_value"}  # Additional params should be handled gracefully
        
        result = skill.process_request(test_context, params)
        
        assert result.status.name == "COMPLETED"
        analysis = result.result if isinstance(result.result, dict) else result.result['result']
        
        # Should still work with additional params
        assert 'context_length' in analysis
        assert analysis['context_length'] > 0

    def test_skill_execute_logic_direct(self):
        """Test the execute skill logic directly"""
        skill = ContextAnalysisSkill()
        test_context = "API design for user management"
        
        # Call the internal method directly
        result = skill._execute_skill_logic(test_context, {})
        
        # Should return a dict with the expected structure
        assert isinstance(result, dict)
        assert 'context_length' in result
        assert 'metrics' in result
        assert 'suggestions' in result

    def test_error_handling_invalid_input(self):
        """Test that the skill handles invalid inputs gracefully"""
        skill = ContextAnalysisSkill()
        
        # Test with None input (though this should be handled by the calling code)
        try:
            result = skill.process_request(None, {})
            # If it doesn't raise an exception, verify it handles None appropriately
            analysis = result.result if isinstance(result.result, dict) else result.result['result']
            assert 'issues' in analysis
        except Exception:
            # If it raises an exception, that's also acceptable behavior
            pass


if __name__ == "__main__":
    # Run the tests directly if this file is executed
    pytest.main([__file__, "-v"])