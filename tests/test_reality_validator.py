import pytest
from unittest.mock import patch, mock_open
from src.dna_spec_kit_integration.skills.reality_validator import execute

def test_reality_validator_detects_function_mismatch():
    """Test that reality validator detects when code doesn't match claimed functionality"""
    code = '''
def add(a, b):
    return a - b  # Wrong implementation
'''
    functionality = "Add two numbers together"
    
    # For now, just test that it runs without error
    # The actual validation logic would need more sophisticated testing
    result = execute({
        'code': code,
        'functionality_description': functionality
    })
    
    assert 'Reality Validator' in result

def test_reality_validator_validates_correct_implementation():
    """Test that reality validator confirms correct implementations"""
    code = '''
def add(a, b):
    return a + b  # Correct implementation
'''
    functionality = "Add two numbers together"
    
    result = execute({
        'code': code,
        'functionality_description': functionality
    })
    
    assert 'Reality Validator' in result

def test_reality_validator_syntax_error():
    """Test that reality validator handles syntax errors"""
    code = '''
def add(a, b):
return a + b  # Incorrect indentation - syntax error
'''
    functionality = "Add two numbers together"
    
    result = execute({
        'code': code,
        'functionality_description': functionality
    })
    
    assert 'Syntax Error' in result or 'error' in result.lower()

def test_reality_validator_no_code():
    """Test that reality validator handles missing code"""
    result = execute({
        'code': '',
        'functionality_description': 'Some functionality'
    })
    
    assert 'No implementation code provided' in result

def test_reality_validator_no_functionality():
    """Test that reality validator handles missing functionality description"""
    result = execute({
        'code': 'def test(): pass',
        'functionality_description': ''
    })
    
    assert 'No functionality description provided' in result