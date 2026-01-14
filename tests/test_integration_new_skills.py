import pytest
from src.dna_spec_kit_integration.core.skill_manager import SkillManager

def test_minimalist_architect_integration():
    """Test minimalist architect integration with skill manager"""
    manager = SkillManager()
    result = manager.execute_skill('minimalist-architect', {
        'requirement': 'Create a simple calculator',
        'architecture': 'Single class with basic operations'
    })
    
    assert result is not None
    assert 'minimalist' in result.lower() or 'architecture' in result.lower() or 'appropriate' in result.lower()

def test_reality_validator_integration():
    """Test reality validator integration with skill manager"""
    manager = SkillManager()
    code = '''
def add(a, b):
    return a + b
'''
    result = manager.execute_skill('reality-validator', {
        'code': code,
        'functionality_description': 'Add two numbers together'
    })
    
    assert result is not None
    assert 'Reality Validator' in result or 'validator' in result.lower()

def test_integration_with_existing_skills():
    """Test that new skills don't break existing functionality"""
    manager = SkillManager()
    
    # Test an existing skill still works
    result = manager.execute_skill('context-analysis', {
        'context': 'Simple test requirement'
    })
    
    assert result is not None
    assert 'context' in result.lower() or 'analysis' in result.lower()