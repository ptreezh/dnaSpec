"""
DNASPEC Context Engineering API Documentation
=============================================

This document describes the API for the DNASPEC Context Engineering System,
which provides AI-powered context analysis, optimization, and cognitive template
application for software development tasks.
"""

# Core Skills
## ContextAnalysisSkill
The `ContextAnalysisSkill` analyzes the quality of input context across five dimensions:

- **Clarity**: How clear and unambiguous the context is
- **Relevance**: How relevant the context is to the target task 
- **Completeness**: How complete the context is with respect to key information
- **Consistency**: How internally consistent the context is
- **Efficiency**: How efficiently information is conveyed

### Usage
```python
from dna_context_engineering.core_skill import ContextAnalysisSkill
from dna_context_engineering.ai_client import GenericAPIClient
from dna_context_engineering.instruction_template import TemplateRegistry

ai_client = GenericAPIClient()
template_registry = TemplateRegistry()
skill = ContextAnalysisSkill(ai_client, template_registry)

# Analyze context
context = "Design a user authentication system"
result = skill.execute(context, {})
if result.success:
    metrics = result.data['metrics']
    print(f"Clarity: {metrics['clarity']}")
    print(f"Relevance: {metrics['relevance']}")
```

### Parameters
- `context`: String containing the context to analyze
- `params`: Optional dictionary with additional parameters (currently unused)

### Returns
- `SkillResult` object with:
  - `success`: Boolean indicating success/failure
  - `data`: Dictionary containing:
    - `metrics`: Dict with scores for each dimension (0.0-1.0)
    - `suggestions`: List of improvement suggestions
    - `issues`: List of identified issues
  - `error`: Error message if unsuccessful
  - `execution_time`: Time taken for execution
  - `confidence`: Confidence score (0.0-1.0)

## ContextOptimizationSkill
The `ContextOptimizationSkill` optimizes context based on specified goals.

### Usage
```python
from dna_context_engineering.core_skill import ContextOptimizationSkill

skill = ContextOptimizationSkill(ai_client, template_registry)

context = "System needed. Need auth."
result = skill.execute(context, {'optimization_goals': ['clarity', 'completeness']})
if result.success:
    print(result.data['optimized_context'])
```

### Parameters
- `context`: String containing the context to optimize
- `params`: Dictionary with:
  - `optimization_goals`: List of goals to optimize for (default: ['clarity', 'completeness'])

### Returns
- `SkillResult` object with:
  - `success`: Boolean indicating success/failure
  - `data`: Dictionary containing:
    - `original_context`: Original input context
    - `optimized_context`: The optimized version
    - `applied_optimizations`: List of changes applied
    - `improvement_metrics`: Dict showing improvements made
  - `error`: Error message if unsuccessful
  - `execution_time`: Time taken for execution
  - `confidence`: Confidence score (0.0-1.0)

## CognitiveTemplateSkill
The `CognitiveTemplateSkill` applies cognitive templates to structure complex tasks.

### Usage
```python
from dna_context_engineering.core_skill import CognitiveTemplateSkill

skill = CognitiveTemplateSkill(ai_client, template_registry)

context = "How should I structure my microservices?"
result = skill.execute(context, {'template_type': 'chain-of-thought'})
if result.success:
    print(result.data['enhanced_context'])
```

### Parameters
- `context`: String containing the context to apply template to
- `params`: Dictionary with:
  - `template_type`: Type of template to apply ('chain-of-thought', 'few-shot', 'verification', 'role-playing', 'understanding')

### Returns
- `SkillResult` object with:
  - `success`: Boolean indicating success/failure
  - `data`: Dictionary containing:
    - `template_type`: Applied template type
    - `template_description`: Description of the template
    - `original_context`: Original input context
    - `enhanced_context`: Context with template applied
    - `template_structure`: Steps of the applied template
  - `error`: Error message if unsuccessful
  - `execution_time`: Time taken for execution
  - `confidence`: Confidence score (0.0-1.0)

# Skills Manager
## SkillsManager
The `SkillsManager` coordinates multiple skills and provides a unified interface.

### Usage
```python
from dna_context_engineering.core_skill import SkillsManager

manager = SkillsManager(ai_client, template_registry)

# Execute a skill
result = manager.execute_skill('context-analysis', 'My context')
if result.success:
    print("Success!")

# List available skills
available_skills = manager.list_skills()
print(available_skills)  # {'context-analysis': 'description...', ...}
```

### Methods
- `execute_skill(skill_name, context, params)`: Execute a specific skill
- `list_skills()`: Get dictionary of available skills and descriptions
- `get_skill_stats(skill_name)`: Get statistical information about skill performance
- `register_skill(skill_name, skill_instance)`: Register a new skill

# AI Client Interface
## AI Clients
The system supports different AI providers through a unified interface.

### Available Clients
- `GenericAPIClient`: For testing and simulation
- `AnthropicClient`: For Claude API
- `GoogleAIClient`: For Gemini API  
- `OpenAIClient`: For GPT API

### Usage
```python
from dna_context_engineering.ai_client import create_ai_client

# Create different clients
anthropic_client = create_ai_client('anthropic', 'your-api-key')
google_client = create_ai_client('google', 'your-api-key')
openai_client = create_ai_client('openai', 'your-api-key')
generic_client = create_ai_client('generic', '')  # For testing
```

# Template System
## Instruction Templates
The system uses standardized templates for consistent AI instruction formatting.

### Available Templates
- `ContextAnalysisTemplate`: For quality analysis
- `ContextOptimizationTemplate`: For content optimization
- `CognitiveTemplate`: For applying cognitive frameworks

# Standalone Execution Functions
## Direct Execution
The system provides functions for direct skill execution without needing to instantiate classes:

### Functions
- `execute_context_analysis(context, params=None)`: Execute context analysis
- `execute_context_optimization(context, params=None)`: Execute context optimization  
- `execute_cognitive_template(context, params=None)`: Execute cognitive template

### Usage
```python
from dna_context_engineering.skills_system_final import (
    execute_context_analysis,
    execute_context_optimization,
    execute_cognitive_template
)

analysis_result = execute_context_analysis("Design a system")
optimization_result = execute_context_optimization("Basic system")
template_result = execute_cognitive_template("How to approach?")
```

# Error Handling and Validation
## Validation
All skills validate input before processing:

- Context cannot be empty
- Context length is limited (default max 10,000 characters)
- Parameters are validated based on skill requirements

## Error Responses
Skills return structured error information:
- `success = False`
- `error` field with descriptive message
- Proper error propagation from underlying systems

# Performance Characteristics
## Timing
- Response time typically under 1 second for simulated AI client
- Performance depends on actual AI provider used
- Memory usage remains stable under load

## Limits
- Context length: 10,000 characters maximum
- Concurrent operations: System can handle multiple requests
- Rate limiting: Built-in delays to respect API limits

# Security Considerations
## Input Sanitization
- All inputs are validated
- Special characters are handled properly
- Path traversal and injection attempts are prevented

## Boundary Enforcement
- Context length limits prevent DoS
- Proper error handling prevents information leaks
- Input validation occurs at multiple levels

For more information about implementation, see the source code in `src/dna_context_engineering/`.