---
allowed-tools: Bash(fs.createFile:*), Bash(fs.writeFile:*), Bash(fs.readFile:*)
argument-hint: [template-name] [context]
description: Apply cognitive templates for structured thinking. Use chain of thought, few-shot learning, verification, role-playing, or understanding frameworks.
model: claude-3-5-sonnet-20241022
---

# Cognitive Template Application Process

## Task
Apply the specified cognitive template to the following context:

Template: $1 (options: chain_of_thought, few_shot, verification, role_playing, understanding)
Context: $2

## Available Templates

### 1. Chain of Thought
Use this template to break down complex problems into logical steps:
- Problem understanding: Clarify the core requirements and constraints
- Step decomposition: Break the task into executable sub-steps
- Intermediate reasoning: Provide detailed thinking process at each step
- Verification check: Check reasoning process for reasonableness and logic
- Final answer: Synthesize all steps into a final result

### 2. Few-Shot Learning
Use this template when examples can guide the solution:
- Provide clear examples of input-output pairs
- Identify patterns from the examples
- Apply the learned patterns to the new task
- Explain the reasoning based on the examples

### 3. Verification Framework
Use this template to validate content or solutions:
- Initial answer: Provide initial judgment or answer
- Logical consistency check: Verify internal logical consistency
- Factual accuracy check: Check statement accuracy
- Completeness check: Assess whether all necessary information is included
- Final confirmation: Synthesize checks into final confirmation

### 4. Role Playing
Use this template to analyze from a specific professional perspective:
- Role understanding: Define the professional capabilities of the role
- Professional analysis: How would this role understand the task?
- Professional advice: What suggestions would this role make?
- Professional decision: How would this role decide?

### 5. Understanding Framework
Use this template for deep comprehension:
- Core objective: What is the main purpose?
- Key elements: What are the important components?
- Constraint conditions: What are the limitations and requirements?
- Success criteria: How to judge completion quality?
- Potential risks: What challenges might exist?

## Process to Follow
1. Select the appropriate template based on the task nature
2. Apply the selected template structure to the context
3. Provide a well-organized response following the template structure
4. Ensure all aspects of the template are addressed
5. Maintain logical flow between template elements

## Output Requirements
Please provide a structured response following the selected template with clear sections and logical flow.