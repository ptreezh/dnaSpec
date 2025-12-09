---
name: dnaspec-task-decomposer
description: DNASPEC Task Decomposer sub-skill for breaking down complex project requirements into atomic tasks, generating task dependency graphs, and ensuring closure of task context documentation. Use when you need to decompose complex requirements, analyze dependencies, or create task plans.
license: Apache 2.0
allowed-tools: 
  - Bash(python:scripts/task_decomposer.py)
metadata:
  speckit-version: 1.0
  speckit-category: task-management
---

# DNASPEC Task Decomposer

## Overview
DNASPEC Task Decomposer is a specialized sub-skill for the DNASPEC Intelligent Architect system. It breaks down complex project requirements into atomic tasks, generates task dependency relationships, and ensures comprehensive task context documentation closure.

The decomposition utilizes specialized scripts for accurate analysis:
- `scripts/task_decomposer.py` - Core task decomposition engine with advanced dependency mapping and resource recommendations

## Core Functions

### 1. Requirements Analysis
Analyze complex project requirements to understand:
- Functional requirements and expected outcomes
- Non-functional requirements and constraints
- Success criteria and acceptance tests
- Resource and time constraints
- Risk factors and dependencies

### 2. Atomic Task Generation
Decompose requirements into atomic tasks that are:
- Indivisible and self-contained
- Clearly defined with specific outcomes
- Estimable in terms of effort and complexity
- Assignable to individual team members
- Testable with clear acceptance criteria

### 3. Dependency Mapping
Generate task dependency relationships:
- Identify prerequisite relationships between tasks
- Determine parallelizable task groups
- Recognize critical path tasks
- Map resource dependencies
- Identify potential bottlenecks

### 4. Context Documentation
Ensure comprehensive task context documentation:
- Task purpose and objectives
- Required inputs and expected outputs
- Success criteria and quality standards
- Potential risks and mitigation strategies
- Related tasks and dependencies

### 5. Execution Planning
Create actionable execution plans:
- Task priority and sequencing
- Resource allocation recommendations
- Time estimation and scheduling
- Quality assurance checkpoints
- Integration and validation steps

## Decomposition Process

### Phase 1: Requirements Understanding
- Analyze the provided project requirements
- Identify functional and non-functional components
- Clarify ambiguities and fill information gaps
- Establish success criteria and acceptance tests

### Phase 2: Task Identification
- Identify major deliverables and components
- Break down deliverables into sub-components
- Define atomic tasks for each component
- Ensure tasks are specific, measurable, and achievable

### Phase 3: Dependency Analysis
- Determine temporal dependencies between tasks
- Identify resource conflicts and constraints
- Group tasks that can be executed in parallel
- Map out critical path for project scheduling

### Phase 4: Documentation and Context
- Create comprehensive documentation for each task
- Define inputs, outputs, and acceptance criteria
- Identify required resources and skills
- Document potential risks and mitigation strategies

### Phase 5: Planning and Prioritization
- Prioritize tasks based on dependencies and importance
- Estimate effort and duration for each task
- Create execution sequences and milestones
- Plan for quality assurance and validation

## Output Format

The decomposition will provide:

1. **Atomic Task List**: Complete list of decomposed tasks
   - Task ID
   - Task description
   - Expected output/deliverable
   - Effort estimation
   - Priority level

2. **Dependency Graph**: Visual representation of task relationships and dependencies

3. **Execution Sequence**: Recommended order for task execution considering dependencies

4. **Resource Recommendations**: Suggested allocation of resources for efficient execution

5. **Quality Checkpoints**: Validation points to ensure task completion quality

## Advanced Features

### Multi-Dimensional Task Classification
- Categorize tasks by type (development, testing, documentation, etc.)
- Classify by complexity and risk level
- Group by required expertise or team

### Dynamic Dependency Resolution
- Handle complex interdependencies
- Identify and resolve circular dependencies
- Optimize for parallel execution where possible

### Risk-Aware Task Planning
- Identify high-risk tasks requiring special attention
- Plan contingency tasks for potential failures
- Create buffer tasks for unexpected issues

## Examples
- "Decompose this complex software development requirement into atomic tasks"
- "Analyze the dependencies for this multi-component system"
- "Create a task plan for implementing this feature"

## Guidelines
- Ensure all tasks are truly atomic and indivisible
- Accurately map all dependencies to avoid bottlenecks
- Provide realistic effort estimations
- Include comprehensive context documentation
- Consider resource constraints in planning
- Maintain traceability from requirements to tasks