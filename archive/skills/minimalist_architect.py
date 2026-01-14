"""
Minimalist Architect Skill - Evaluates architectural solutions for optimal complexity
"""
from typing import Dict, Any
import re

def execute(args: Dict[str, Any]) -> str:
    """
    Evaluate architecture proposals for minimalism and optimal complexity
    """
    requirement = args.get("requirement", "")
    proposed_architecture = args.get("architecture", "")
    essential_elements = args.get("essential_elements", [])
    
    # Calculate complexity value ratio
    value_ratio = calculate_complexity_value_ratio(requirement, proposed_architecture)

    # Evaluate against minimalism principles
    minimalist_feedback = evaluate_minimalism(requirement, proposed_architecture, value_ratio)

    # Suggest simpler alternatives if needed
    simpler_alternatives = suggest_simpler_architectures(requirement, proposed_architecture)
    
    return format_minimalist_review(value_ratio, minimalist_feedback, simpler_alternatives)

def calculate_complexity_value_ratio(requirement: str, architecture: str) -> float:
    """Calculate the ratio of complexity to value delivered"""
    architecture_lower = architecture.lower()

    # More sophisticated component counting
    # Identify architectural elements based on keywords and context

    # Define architectural components and services
    architectural_elements = [
        'service', 'module', 'component', 'system', 'layer', 'microservice',
        'api', 'database', 'frontend', 'backend', 'gateway', 'cache', 'queue',
        'broker', 'application', 'program', 'platform', 'framework', 'engine',
        'user-service', 'auth-service', 'calculation-service', 'payment-service',
        'product-service', 'order-service', 'data-service', 'logging-service'
    ]

    # Count architectural components more accurately
    word_list = architecture_lower.split()
    keyword_matches = [word for word in word_list if word in architectural_elements]

    # Count comma-separated parts that contain architectural terms
    comma_parts = [part.strip() for part in architecture.split(',') if part.strip()]
    comma_arch_parts = []

    for part in comma_parts:
        part_lower = part.lower()
        # Look for architectural terms in each comma-separated part
        if any(element in part_lower for element in architectural_elements) or \
           any(word in part_lower.split() for word in architectural_elements):
            comma_arch_parts.append(part)

    # Use the more accurate count based on the description
    if len(comma_arch_parts) > 0:
        # Count each comma-separated architectural unit as one component
        total_components = len(comma_arch_parts)
    else:
        # If no comma separation, count distinct architectural elements
        total_components = max(1, len(set(keyword_matches)))

    # Special handling for common architectural phrases
    if 'single file' in architecture_lower or 'monolithic' in architecture_lower:
        total_components = 1
    elif 'multi-tier' in architecture_lower or 'n-tier' in architecture_lower:
        total_components = min(total_components, 3)  # Multi-tier usually refers to 3-4 layers

    # Determine requirement complexity based on content
    req_lower = requirement.lower()
    req_words = req_lower.split()

    # Adjust for requirement type - simple requirements should have fewer components
    simple_indicators = ['simple', 'basic', 'hello', 'calculator', 'file upload', 'todo']
    complex_indicators = ['complex', 'enterprise', 'scalable', 'distributed', 'e-commerce', 'platform']

    # Adjust the expected complexity based on requirement type more carefully
    if any(indicator in req_lower for indicator in simple_indicators):
        expected_components = 1  # Very simple requirements: expect minimal architecture
    elif any(indicator in req_lower for indicator in complex_indicators):
        # Complex requirements: allow more components, but based on requirement complexity
        expected_components = max(3, len(req_words) // 2)  # Complex reqs can have more components
    else:
        # For medium complexity requirements, use a balanced approach
        expected_components = max(1, len(req_words) / 3)  # Moderate expectations

    # Calculate ratio with better sensitivity for small differences
    if expected_components == 0:
        return 1.0

    raw_ratio = total_components / expected_components
    # Cap the ratio to prevent extreme values, but make the function more sensitive
    return min(2.0, raw_ratio)  # Allow up to 2x over expected, but make warnings more contextual

def evaluate_minimalism(requirement: str, architecture: str, value_ratio: float = None) -> str:
    """Evaluate architecture against minimalism principles"""
    feedback = []

    # Check for over-engineering indicators
    words_indicating_over_engineering = [
        'microservices', 'kubernetes', 'docker', 'container', 'load balancer',
        'service mesh', 'api gateway', 'enterprise', 'scalability', 'high availability',
        'cluster', 'orchestration', 'middleware', 'complexity', 'distributed'
    ]

    arch_lower = architecture.lower()
    over_engineering_indicators = [
        word for word in words_indicating_over_engineering
        if word in arch_lower
    ]

    if over_engineering_indicators:
        feedback.append(f"Potential over-engineering indicators found: {', '.join(over_engineering_indicators)}")

    # Use the provided value ratio if available, otherwise calculate it
    if value_ratio is None:
        value_ratio = calculate_complexity_value_ratio(requirement, architecture)

    # Check if the architecture is appropriate for the requirement
    # Adjust thresholds based on requirement complexity
    req_word_count = len(requirement.split())

    # Only apply stricter rules for simpler requirements
    if req_word_count < 10 and value_ratio > 1.2:
        feedback.append("Architecture may be more complex than requirement warrants")
    elif value_ratio > 1.5:
        feedback.append("Architecture is significantly more complex than requirement warrants")

    return '; '.join(feedback) if feedback else "Architecture appears appropriate for requirement complexity"

def suggest_simpler_architectures(requirement: str, architecture: str) -> list:
    """Suggest more minimalist architectural alternatives"""
    suggestions = []
    
    # Basic heuristic suggestions based on requirement
    req_lower = requirement.lower()
    
    if 'simple' in req_lower or 'basic' in req_lower:
        if any(overcomp in architecture.lower() for overcomp in ['microservices', 'kubernetes', 'docker']):
            suggestions.append("Consider a monolithic architecture with modular components")
    
    if 'calculator' in req_lower or 'file upload' in req_lower or 'todo' in req_lower:
        if 'microservice' in architecture.lower() or 'kubernetes' in architecture.lower():
            suggestions.append("A single application with clear modules would be more appropriate")
    
    return suggestions

def format_minimalist_review(value_ratio: float, feedback: str, alternatives: list) -> str:
    """Format the minimalist review for output"""
    review = "🧩 Minimalist Architect Review\n"
    review += "=" * 40 + "\n\n"
    
    review += f"Complexity-to-Value Ratio: {value_ratio:.2f}\n\n"
    
    if value_ratio > 1.5:
        review += "⚠️  WARNING: Architecture may be overly complex for the requirement\n\n"
    else:
        review += "✅ Architecture complexity appears appropriate\n\n"
    
    review += f"Analysis: {feedback}\n\n"
    
    if alternatives:
        review += "💡 Suggested Alternatives:\n"
        for alt in alternatives:
            review += f"  • {alt}\n"
    
    return review