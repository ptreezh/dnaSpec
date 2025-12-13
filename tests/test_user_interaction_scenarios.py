"""
Comprehensive User Interaction Tests for DNASPEC
Tests user workflows and interaction scenarios
"""
import pytest
import os
import sys
import tempfile
import shutil
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch

# Add project path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.dna_context_engineering.skills_system_final import (
    execute, get_available_skills, execute_context_analysis, 
    execute_context_optimization, execute_cognitive_template
)
from src.dna_spec_kit_integration.core.cli_detector import CliDetector
from src.dna_spec_kit_integration.core.auto_configurator import AutoConfigurator


class TestUserInteractionScenarios:
    """Tests for user interaction scenarios"""

    def test_context_analysis_workflow(self):
        """Test complete context analysis workflow"""
        test_context = "Design an e-commerce system with user authentication and payment processing"
        
        # Test direct execution
        result = execute({
            'skill': 'context-analysis', 
            'context': test_context
        })
        
        assert isinstance(result, str)
        assert "Context Quality Analysis Results:" in result
        assert "Length:" in result
        assert "Five-Dimensional Quality Metrics" in result

    def test_context_optimization_workflow(self):
        """Test complete context optimization workflow"""
        test_context = "Create a simple system"
        
        # Test direct execution
        result = execute({
            'skill': 'context-optimization', 
            'context': test_context
        })
        
        assert isinstance(result, str)
        assert "Context Optimization Results:" in result
        assert "Applied Optimizations:" in result
        
    def test_cognitive_template_workflow(self):
        """Test cognitive template application workflow"""
        test_context = "How to design a secure API?"
        params = {'template': 'verification'}
        
        # Test direct execution
        result = execute({
            'skill': 'cognitive-template', 
            'context': test_context,
            'params': params
        })
        
        assert isinstance(result, str)
        assert "Cognitive Template Application" in result
        assert "Verification Check" in result

    def test_available_skills_list(self):
        """Test getting available skills"""
        skills = get_available_skills()
        
        assert isinstance(skills, dict)
        assert len(skills) > 0
        assert 'context-analysis' in skills
        assert 'context-optimization' in skills
        assert 'cognitive-template' in skills
        
        for skill_name, description in skills.items():
            assert isinstance(skill_name, str)
            assert isinstance(description, str)
            assert len(skill_name) > 0
            assert len(description) > 0

    def test_individual_skill_execution_functions(self):
        """Test individual skill execution functions"""
        test_input = "Test context for individual skills"
        
        # Test context analysis
        analysis_result = execute_context_analysis(test_input)
        assert isinstance(analysis_result, str)
        assert "Context Quality Analysis Results:" in analysis_result
        
        # Test context optimization
        optimization_result = execute_context_optimization(test_input)
        assert isinstance(optimization_result, str)
        assert "Context Optimization Results:" in optimization_result
        
        # Test cognitive template
        template_result = execute_cognitive_template(test_input)
        assert isinstance(template_result, str)
        assert "Cognitive Template Application" in template_result

    def test_error_handling_in_user_workflow(self):
        """Test error handling in user workflows"""
        # Test with empty context
        empty_result = execute({
            'skill': 'context-analysis', 
            'context': ''
        })
        
        assert isinstance(empty_result, str)
        assert "Error:" in empty_result or "Context" in empty_result
        
        # Test with invalid skill name
        invalid_result = execute({
            'skill': 'invalid-skill', 
            'context': 'Test context'
        })
        
        assert isinstance(invalid_result, str)
        assert "Error:" in invalid_result
        assert "Unknown skill" in invalid_result

    def test_cli_detector_functionality(self):
        """Test CLI tool detection functionality"""
        detector = CliDetector()
        results = detector.detect_all()
        
        # Check that results is a dictionary
        assert isinstance(results, dict)
        
        # Check that common tools are detected (or not, depending on system)
        expected_tools = ['claude', 'gemini', 'qwen', 'copilot', 'cursor', 'codebuddy']
        for tool in expected_tools:
            assert tool in results
            assert isinstance(results[tool], dict)
            assert 'installed' in results[tool]
            assert isinstance(results[tool]['installed'], bool)

    def test_auto_configurator_functionality(self):
        """Test auto configurator functionality"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            auto_config = AutoConfigurator()
            
            # Test quick configuration
            result = auto_config.quick_configure()
            
            assert isinstance(result, dict)
            assert 'success' in result
            assert 'detected_tools' in result
            assert 'config_path' in result

    def test_cognitive_template_variations(self):
        """Test different cognitive template types"""
        test_context = "Implement a user authentication system"
        
        templates = ['chain_of_thought', 'verification', 'few_shot', 'role_playing', 'understanding']
        
        for template in templates:
            result = execute({
                'skill': 'cognitive-template', 
                'context': test_context,
                'params': {'template': template}
            })
            
            assert isinstance(result, str)
            assert "Cognitive Template Application" in result
            assert template.replace('_', '-') in result or template in result

    def test_context_optimization_with_goals(self):
        """Test context optimization with specific goals"""
        test_context = "System design for a blog platform"
        params = {'optimization_goals': ['clarity', 'completeness']}
        
        result = execute({
            'skill': 'context-optimization', 
            'context': test_context,
            'params': params
        })
        
        assert isinstance(result, str)
        assert "Context Optimization Results:" in result
        assert "clarity" in result.lower() or "completeness" in result.lower()

    def test_complex_context_analysis(self):
        """Test analysis of complex, multi-faceted contexts"""
        complex_context = """
        Design a cloud-based SaaS platform with the following requirements:
        - Multi-tenant architecture supporting thousands of customers
        - Real-time data synchronization across multiple regions
        - GDPR and HIPAA compliance for data handling
        - Microservices architecture with API gateway
        - Containerized deployment with Kubernetes
        - Automated CI/CD pipeline with security scanning
        - Advanced analytics and reporting capabilities
        - Mobile and web application support
        """
        
        result = execute({
            'skill': 'context-analysis', 
            'context': complex_context
        })
        
        assert isinstance(result, str)
        assert "Context Quality Analysis Results:" in result
        # Complex context should have more details
        assert len(result) > 200  # Should be substantial output


class TestAdvancedUserWorkflows:
    """Tests for advanced user workflows and edge cases"""

    def test_multi_step_skill_execution(self):
        """Test executing multiple skills in sequence"""
        # Start with context analysis
        context = "Design a REST API for user management"
        
        analysis_result = execute({
            'skill': 'context-analysis', 
            'context': context
        })
        
        assert "Context Quality Analysis Results:" in analysis_result
        
        # Then optimize based on analysis
        optimization_result = execute({
            'skill': 'context-optimization', 
            'context': context
        })
        
        assert "Context Optimization Results:" in optimization_result
        
        # Finally apply a cognitive template
        template_result = execute({
            'skill': 'cognitive-template', 
            'context': context,
            'params': {'template': 'verification'}
        })
        
        assert "Cognitive Template Application" in template_result

    def test_long_context_handling(self):
        """Test handling of long context inputs"""
        long_context = "System design for an enterprise application. " * 100  # 100 repetitions
        
        result = execute({
            'skill': 'context-analysis', 
            'context': long_context
        })
        
        assert isinstance(result, str)
        assert "Context Quality Analysis Results:" in result
        # Should handle long contexts without errors

    def test_special_characters_handling(self):
        """Test handling of special characters and non-ASCII text"""
        special_context = "设计一个多语言支持的系统，包含中文、日本語、한국어等字符"
        
        result = execute({
            'skill': 'context-analysis', 
            'context': special_context
        })
        
        assert isinstance(result, str)
        # Should handle special characters without errors

    def test_skill_execution_with_context_variations(self):
        """Test skill execution with different context types"""
        contexts = [
            "Simple task: create a hello world program",
            "Complex system: design a distributed database system",
            "Technical specification: API design for microservices",
            "Business requirement: customer onboarding system",
            "Architecture design: cloud migration strategy"
        ]
        
        for context in contexts:
            result = execute({
                'skill': 'context-analysis', 
                'context': context
            })
            
            assert isinstance(result, str)
            assert "Context Quality Analysis Results:" in result
    
    def test_cognitive_template_with_complex_reasoning(self):
        """Test cognitive templates with complex reasoning tasks"""
        complex_task = """
        Design a system for real-time fraud detection in financial transactions.
        Consider multiple factors: transaction amount, location, time, user behavior,
        historical patterns, and risk scoring. Provide a comprehensive solution
        that includes data processing, machine learning models, alert systems,
        and response protocols.
        """
        
        result = execute({
            'skill': 'cognitive-template', 
            'context': complex_task,
            'params': {'template': 'chain_of_thought'}
        })
        
        assert isinstance(result, str)
        assert "Chain-of-Thought" in result or "chain-of-thought" in result