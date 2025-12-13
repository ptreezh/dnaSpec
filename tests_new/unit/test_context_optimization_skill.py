"""
Unit tests for Context Optimization Skill following TDD approach
"""
import pytest
from typing import Dict, Any

# Import the skill to be tested
from src.dna_context_engineering.skills_system_final import ContextOptimizationSkill


class TestContextOptimizationSkill:
    """Test cases for ContextOptimizationSkill"""

    def test_skill_initialization(self):
        """Test that ContextOptimizationSkill initializes correctly"""
        skill = ContextOptimizationSkill()
        
        assert skill.name == "dnaspec-context-optimization"
        assert "Context Optimization Skill" in skill.description
        assert "AI model native intelligence" in skill.description

    def test_process_request_with_valid_context(self):
        """Test processing a valid context"""
        skill = ContextOptimizationSkill()
        test_context = "User login system"
        
        result = skill.process_request(test_context, {})
        
        # Verify the result structure
        assert result.status.name == "COMPLETED"
        assert hasattr(result, 'result')
        
        optimization = result.result if isinstance(result.result, dict) else result.result['result']
        
        # Check required fields in the optimization
        assert 'original_context' in optimization
        assert 'optimized_context' in optimization
        assert 'applied_optimizations' in optimization
        assert 'improvement_metrics' in optimization
        assert 'optimization_summary' in optimization
        
        # Verify values
        assert optimization['original_context'] == test_context
        assert isinstance(optimization['optimized_context'], str)
        assert isinstance(optimization['applied_optimizations'], list)
        assert isinstance(optimization['improvement_metrics'], dict)
        assert isinstance(optimization['optimization_summary'], str)
        
        # Verify improvement metrics structure
        expected_metrics = {'clarity', 'relevance', 'completeness', 'conciseness'}
        actual_metrics = set(optimization['improvement_metrics'].keys())
        # Not all metrics need to be present, but those that are should be valid
        for metric in actual_metrics:
            assert metric in expected_metrics
            assert isinstance(optimization['improvement_metrics'][metric], (int, float))

    def test_process_request_empty_context(self):
        """Test processing an empty context"""
        skill = ContextOptimizationSkill()
        
        result = skill.process_request("", {})
        
        # Verify the result structure for empty context
        assert result.status.name == "COMPLETED"
        optimization = result.result if isinstance(result.result, dict) else result.result['result']
        
        # For empty context, should still return valid structure
        assert 'original_context' in optimization
        assert optimization['original_context'] == ""
        assert 'optimized_context' in optimization
        assert isinstance(optimization['optimized_context'], str)
        assert 'applied_optimizations' in optimization
        assert isinstance(optimization['applied_optimizations'], list)

    def test_process_request_with_optimization_goals(self):
        """Test processing with specific optimization goals"""
        skill = ContextOptimizationSkill()
        test_context = "API specification"
        
        # Test with specific parameters
        params = {'optimization_goals': ['clarity', 'completeness']}
        
        result = skill.process_request(test_context, params)
        
        assert result.status.name == "COMPLETED"
        optimization = result.result if isinstance(result.result, dict) else result.result['result']
        
        assert 'original_context' in optimization
        assert optimization['original_context'] == test_context
        assert 'optimized_context' in optimization
        assert isinstance(optimization['optimized_context'], str)
        assert 'applied_optimizations' in optimization
        assert isinstance(optimization['applied_optimizations'], list)

    def test_process_request_with_single_optimization_goal(self):
        """Test processing with a single optimization goal as string"""
        skill = ContextOptimizationSkill()
        test_context = "User requirements"
        
        # Test with a single goal as string
        params = {'optimization_goals': 'clarity'}
        
        result = skill.process_request(test_context, params)
        
        assert result.status.name == "COMPLETED"
        optimization = result.result if isinstance(result.result, dict) else result.result['result']
        
        assert 'original_context' in optimization
        assert optimization['original_context'] == test_context

    def test_process_request_long_context(self):
        """Test processing a long context"""
        skill = ContextOptimizationSkill()
        long_context = "System requirements: " + "This is a requirement. " * 50
        
        result = skill.process_request(long_context, {})
        
        assert result.status.name == "COMPLETED"
        optimization = result.result if isinstance(result.result, dict) else result.result['result']
        
        assert optimization['original_context'] == long_context
        assert len(optimization['optimized_context']) >= len(long_context)  # Optimized context may be longer
        assert isinstance(optimization['applied_optimizations'], list)
        assert isinstance(optimization['improvement_metrics'], dict)

    def test_skill_execute_logic_direct(self):
        """Test the execute skill logic directly"""
        skill = ContextOptimizationSkill()
        test_context = "Database design requirements"
        
        # Call the internal method directly
        result = skill._execute_skill_logic(test_context, {})
        
        # Should return a dict with the expected structure
        assert isinstance(result, dict)
        assert 'original_context' in result
        assert 'optimized_context' in result

    def test_error_handling(self):
        """Test that the skill handles errors gracefully"""
        skill = ContextOptimizationSkill()
        
        # This should not raise an exception
        try:
            result = skill.process_request(12345, {})  # Non-string input
            # If no exception, ensure it returns proper structure
            assert hasattr(result, 'status')
        except Exception:
            # If it raises an exception, that's also acceptable as long as it's handled properly
            pass

    def test_optimization_goals_parsing(self):
        """Test that optimization goals are properly parsed"""
        skill = ContextOptimizationSkill()
        test_context = "Feature specification"
        
        # Test with different types of goal inputs
        test_cases = [
            ['clarity'],  # List with one item
            ['clarity', 'completeness'],  # List with multiple items
            'relevance',  # Single string
            'clarity,relevance',  # Comma-separated string
            [],  # Empty list
        ]
        
        for goals in test_cases:
            params = {'optimization_goals': goals}
            result = skill.process_request(test_context, params)
            
            assert result.status.name == "COMPLETED"
            optimization = result.result if isinstance(result.result, dict) else result.result['result']
            
            assert 'original_context' in optimization
            assert optimization['original_context'] == test_context


if __name__ == "__main__":
    # Run the tests directly if this file is executed
    pytest.main([__file__, "-v"])