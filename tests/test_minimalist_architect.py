import pytest
from src.dna_spec_kit_integration.skills.minimalist_architect import execute

def test_minimalist_architect_identifies_over_engineering():
    """Test that minimalist architect identifies over-engineered solutions"""
    result = execute({
        'requirement': 'Create a simple calculator',
        'architecture': 'Microservices architecture with 10 separate services: user-service, calculation-service, data-service, auth-service, logging-service, monitoring-service, caching-service, api-gateway-service, load-balancer-service, security-service'
    })
    assert 'over-engineering' in result.lower() or 'simpler alternative' in result.lower()

def test_minimalist_architect_approves_suitable_architecture():
    """Test that minimalist architect approves appropriately complex solutions"""
    result = execute({
        'requirement': 'Create a complex e-commerce platform',
        'architecture': 'Frontend, Backend API, Database with User, Product, Order, Payment modules'
    })
    # Should not flag as over-engineered for complex requirements
    assert 'appropriate' in result.lower() or 'well-suited' in result.lower()

def test_minimalist_architect_suggests_simpler_alternatives():
    """Test that minimalist architect suggests simpler alternatives when appropriate"""
    result = execute({
        'requirement': 'Create a simple file upload service',
        'architecture': 'Kubernetes cluster with 50 microservices, multiple load balancers, complex CI/CD pipelines'
    })
    assert 'simpler alternative' in result.lower() or 'monolithic' in result.lower()

def test_minimalist_architect_simple_case():
    """Test minimalist architect with very simple case"""
    result = execute({
        'requirement': 'Create a hello world program',
        'architecture': 'Single file application'
    })
    assert 'appropriate' in result.lower() or 'simple' in result.lower()