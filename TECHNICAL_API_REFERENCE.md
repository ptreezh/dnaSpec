# DNASPEC Context Engineering API Reference

## Table of Contents
1. [Core Skill Classes](#core-skill-classes)
2. [AI Client Interface](#ai-client-interface) 
3. [Template System](#template-system)
4. [Skills Manager](#skills-manager)
5. [Execution Functions](#execution-functions)
6. [Data Structures](#data-structures)

## Core Skill Classes

### ContextEngineeringSkill (Abstract Base Class)
Base class for all context engineering skills.

#### Methods
- `__init__(name: str, description: str, ai_client: AIModelClient, template_registry: TemplateRegistry)`
  - Initializes the skill with name, description, and required components
- `execute(context: str, params: Dict[str, Any] = None) -> SkillResult`
  - Abstract method to execute the skill
- `_construct_instruction(template_name: str, context: str, params: Dict[str, Any] = None) -> str`
  - Helper method to construct AI instruction using templates
- `_send_to_ai_and_parse(instruction: str, template_name: str) -> SkillResult`
  - Helper method to send instruction to AI and parse response
- `get_stats() -> Dict[str, Any]`
  - Returns execution statistics
- `reset_stats()`
  - Resets execution statistics
- `validate_input(context: str, params: Dict[str, Any] = None) -> Optional[str]`
  - Validates input parameters, returns error message if invalid

### ContextAnalysisSkill
Analyzes context quality across five dimensions.

#### Methods
- `execute(context: str, params: Dict[str, Any] = None) -> SkillResult`

#### Expected Output Data
```python
{
    "context_length": int,
    "token_count_estimate": int, 
    "metrics": {
        "clarity": float,      # 0.0-1.0
        "relevance": float,    # 0.0-1.0
        "completeness": float, # 0.0-1.0
        "consistency": float,  # 0.0-1.0
        "efficiency": float    # 0.0-1.0
    },
    "suggestions": List[str],
    "issues": List[str],
    "confidence": float        # 0.0-1.0
}
```

### ContextOptimizationSkill
Optimizes context based on specific goals.

#### Methods
- `execute(context: str, params: Dict[str, Any] = None) -> SkillResult`

#### Parameters
- `optimization_goals`: List of goals to optimize for (default: ['clarity', 'completeness'])

#### Expected Output Data
```python
{
    "original_context": str,
    "optimized_context": str,
    "applied_optimizations": List[str],
    "improvement_metrics": {
        "clarity": float,      # Improvement value
        "relevance": float,    # Improvement value  
        "completeness": float, # Improvement value
        "conciseness": float   # Improvement value
    },
    "optimization_summary": str
}
```

### CognitiveTemplateSkill
Applies cognitive templates to structure complex tasks.

#### Methods
- `execute(context: str, params: Dict[str, Any] = None) -> SkillResult`

#### Parameters
- `template_type`: Type of template ('chain-of-thought', 'few-shot', 'verification', 'role-playing', 'understanding')

#### Expected Output Data
```python
{
    "success": bool,
    "template_type": str,
    "template_description": str,
    "original_context": str,
    "enhanced_context": str,
    "template_structure": List[str],
    "confidence": float        # 0.0-1.0
}
```

## AI Client Interface

### AIModelClient (Abstract Base Class)
Base class for AI model clients.

#### Methods
- `__init__(api_key: str, base_url: str = None, rate_limit_delay: float = 1.0)`
- `send_instruction(instruction: str) -> str`
  - Abstract method to send instruction to AI model
- `get_remaining_quota() -> int`
  - Abstract method to get remaining API quota
- `_ensure_rate_limit()`
  - Internal method to enforce rate limiting

### Concrete Client Classes

#### AnthropicClient
Client for Anthropic Claude API.

#### GoogleAIClient  
Client for Google Gemini API.

#### OpenAIClient
Client for OpenAI API.

#### GenericAPIClient
Simulated client for testing and development.

## Template System

### InstructionTemplate (Abstract Base Class)
Base class for instruction templates.

#### Methods
- `__init__(name: str, description: str)`
- `construct_prompt(context: str, params: Dict[str, Any] = None) -> str`
  - Construct prompt from context and parameters
- `parse_response(response: str) -> Dict[str, Any]`
  - Parse AI response into structured data
- `validate_params(params: Dict[str, Any]) -> List[str]`
  - Validate parameters, return errors

### Concrete Template Classes

#### ContextAnalysisTemplate
Template for context quality analysis.

#### ContextOptimizationTemplate
Template for context optimization.

#### CognitiveTemplate
Template for cognitive template application.

### TemplateRegistry
Manages all available templates.

#### Methods
- `register_template(template: InstructionTemplate)`
- `get_template(name: str) -> InstructionTemplate`
- `list_templates() -> List[str]`
- `create_prompt(template_name: str, context: str, params: Dict[str, Any] = None) -> str`
- `parse_response(template_name: str, response: str) -> Dict[str, Any]`

## Skills Manager

### SkillsManager
Coordinates multiple skills.

#### Methods
- `__init__(ai_client: AIModelClient, template_registry: TemplateRegistry)`
- `execute_skill(skill_name: str, context: str, params: Dict[str, Any] = None) -> SkillResult`
- `list_skills() -> Dict[str, str]`
- `get_skill_stats(skill_name: str) -> Dict[str, Any]`
- `register_skill(skill_name: str, skill_instance: ContextEngineeringSkill) -> bool`

## Execution Functions

### Standalone Execution Functions
These functions provide direct access to skills without requiring class instantiation.

#### execute_context_analysis
```python
def execute_context_analysis(context_input: str, params: Dict[str, Any] = None) -> str
```

#### execute_context_optimization  
```python
def execute_context_optimization(context_input: str, params: Dict[str, Any] = None) -> str
```

#### execute_cognitive_template
```python
def execute_cognitive_template(context_input: str, params: Dict[str, Any] = None) -> str
```

#### execute
```python
def execute(args: Dict[str, Any]) -> str
```
Universal execution function accepting:
- `skill`: Name of skill ('context-analysis', 'context-optimization', 'cognitive-template')
- `context` or `request`: Input context
- `params`: Additional parameters

## Data Structures

### SkillResult
Result object returned by all skills.

#### Attributes
- `success: bool` - Whether execution was successful
- `data: Dict[str, Any]` - The result data
- `error: str` - Error message if execution failed
- `execution_time: float` - Time taken to execute
- `confidence: float` - Confidence in the result (0.0-1.0)

#### Methods
- `to_dict() -> Dict[str, Any]` - Convert to dictionary

### SkillStats
Statistics tracking for skills.

#### Attributes
- `executions: int` - Total number of executions
- `successes: int` - Number of successful executions  
- `failures: int` - Number of failed executions
- `total_execution_time: float` - Total time spent executing
- `avg_execution_time: float` - Average execution time (computed)
- `success_rate: float` - Success rate percentage (computed)

## Configuration and Setup

### AI Client Initialization
```python
from dna_context_engineering.ai_client import create_ai_client

client = create_ai_client('anthropic', 'your-api-key')
```

### Full System Setup
```python
from dna_context_engineering.ai_client import GenericAPIClient  # For testing
from dna_context_engineering.instruction_template import TemplateRegistry
from dna_context_engineering.core_skill import (
    ContextAnalysisSkill,
    ContextOptimizationSkill, 
    CognitiveTemplateSkill
)

# Initialize components
ai_client = GenericAPIClient()  # Use appropriate client for production
template_registry = TemplateRegistry()

# Initialize skills
analysis_skill = ContextAnalysisSkill(ai_client, template_registry)
optimization_skill = ContextOptimizationSkill(ai_client, template_registry)
template_skill = CognitiveTemplateSkill(ai_client, template_registry)
```

## Common Use Cases

### 1. Complete Context Engineering Workflow
```python
# Analyze, optimize, then apply cognitive template
context = "Build an API for user management"

# Step 1: Analysis
analysis_result = analysis_skill.execute(context, {})
if analysis_result.success:
    print(f"Quality score: {sum(analysis_result.data['metrics'].values()) / 5}")

# Step 2: Optimization 
optimization_result = optimization_skill.execute(context, {'optimization_goals': ['clarity']})
if optimization_result.success:
    optimized = optimization_result.data['optimized_context']

# Step 3: Apply cognitive template
template_result = template_skill.execute(optimized, {'template_type': 'chain-of-thought'})
if template_result.success:
    final_result = template_result.data['enhanced_context']
```

### 2. Using Skills Manager
```python
from dna_context_engineering.core_skill import SkillsManager

manager = SkillsManager(ai_client, template_registry)

# Execute skill by name
result = manager.execute_skill('context-analysis', 'My context', {})
if result.success:
    print("Analysis successful")
```

### 3. Direct Function Usage
```python
from dna_context_engineering.skills_system_final import execute_context_analysis

result = execute_context_analysis("Analyze this requirement")
print(result)
```