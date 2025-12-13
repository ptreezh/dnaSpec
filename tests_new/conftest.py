"""
Test configuration and fixtures for DNASPEC tests
"""
import sys
import os
import pytest
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

# Test configuration
TEST_TIMEOUT = 30  # seconds


@pytest.fixture
def project_root():
    """Return the project root directory"""
    return Path(__file__).parent.parent


@pytest.fixture
def sample_context():
    """Provide a sample context for testing"""
    return "Implement a user authentication system with OAuth integration"


@pytest.fixture
def sample_requirements():
    """Provide sample requirements for testing"""
    return """
    Develop a complete e-commerce platform with the following features:
    - User registration and authentication
    - Product catalog with search capabilities
    - Shopping cart functionality
    - Secure payment processing
    - Order management system
    """


@pytest.fixture
def sample_api_spec():
    """Provide sample API specification for testing"""
    return """
    User Management API Specification:
    
    GET /users
    Description: Retrieve list of users
    Parameters: page (int), limit (int, max 100), sort (string)
    Response: 200 OK with JSON array of users

    POST /users
    Description: Create new user
    Body: { "name": "string", "email": "string", "password": "string" }
    Response: 201 Created with user object
    """


def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end tests"
    )