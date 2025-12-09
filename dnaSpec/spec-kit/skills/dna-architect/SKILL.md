---
name: dnaspec-architect
description: DNASPEC Intelligent Architect main skill for complex project hierarchical architecture design, task decomposition, agent creation, and constraint generation. Use when you need to design complex system architectures, plan multi-layered systems, or create agent-based systems.
license: Apache 2.0
allowed-tools: 
  - Bash(python:scripts/architect_coordinator.py)
metadata:
  speckit-version: 1.0
  speckit-category: architecture
---

# DNASPEC Intelligent Architect

## Overview
DNASPEC Intelligent Architect is the core coordinating skill for the DNASPEC Intelligent Architect system. It handles complex project requirements by analyzing them and routing to appropriate sub-skills, coordinating workflows between components, and integrating outputs into comprehensive architecture design documentation.

## Core Functions

### 1. Requirements Analysis
Analyze complex project requirements to understand:
- Functional and non-functional requirements
- System scope and boundaries
- Performance and scalability needs
- Integration requirements
- Security and compliance needs

### 2. Architecture Design Coordination
Coordinate the design of multi-layered system architectures:
- High-level system architecture
- Component-level design
- Interface and API design
- Data flow architecture
- Integration patterns

### 3. Workflow Management
Manage the architecture design workflow:
- Route requirements to appropriate sub-skills
- Coordinate task decomposition processes
- Integrate constraint generation
- Oversee agent creation processes
- Ensure consistency across all components

### 4. Output Integration
Synthesize outputs from various sub-skills:
- System architecture diagrams
- Task decomposition structures
- Agent specifications
- Constraint definitions
- Implementation roadmaps

## Architecture Design Process

### Phase 1: Requirements Understanding
- Analyze the provided project requirements
- Identify system scope and constraints
- Clarify ambiguities and gather missing information
- Establish success criteria and quality standards

### Phase 2: System Architecture Planning
- Design high-level system architecture
- Identify key components and their relationships
- Define interfaces and communication patterns
- Plan for scalability and maintainability

### Phase 3: Task Decomposition Coordination
- Decompose architecture into executable tasks
- Identify dependencies and critical paths
- Plan for parallel development where possible
- Ensure traceability from architecture to tasks

### Phase 4: Agent System Design
- Design intelligent agents to implement components
- Specify agent behaviors and responsibilities
- Define agent communication protocols
- Plan for agent coordination mechanisms

### Phase 5: Constraint Definition
- Generate system constraints and requirements
- Define architectural constraints and guidelines
- Establish quality and performance constraints
- Document compliance and security requirements

## Sub-Skill Coordination

### dnaspec-system-architect
- Coordinates system architecture design
- Manages component-level planning
- Ensures architectural consistency

### dnaspec-task-decomposer
- Routes requirements for task decomposition
- Integrates task structures with architecture
- Ensures task-architecture alignment

### dnaspec-agent-creator
- Coordinates intelligent agent creation
- Ensures agents align with architectural design
- Manages agent interaction patterns

### dnaspec-constraint-generator
- Coordinates constraint generation
- Ensures constraints align with architecture
- Manages constraint validation

## Output Format

The architecture will provide:

1. **System Architecture Documentation**
   - High-level architecture diagram
   - Component specifications
   - Interface definitions
   - Data flow diagrams

2. **Implementation Roadmap**
   - Development phases and milestones
   - Task dependencies and sequencing
   - Resource allocation recommendations
   - Timeline estimates

3. **Agent System Design**
   - Agent specifications and responsibilities
   - Communication protocols
   - Coordination mechanisms
   - Behavior patterns

4. **Constraint Documentation**
   - Architectural constraints
   - Performance requirements
   - Security and compliance requirements
   - Quality standards

## Advanced Features

### Multi-Paradigm Architecture Support
- Support for various architectural paradigms (microservices, monolith, hybrid)
- Pattern-based architecture generation
- Domain-specific architecture templates
- Scalability and performance optimization

### Adaptive Architecture Design
- Design adjustments based on constraints
- Alternative architecture proposals
- Risk-mitigation architecture patterns
- Future-proofing considerations

### Integrated Design Validation
- Architecture consistency checks
- Constraint validation against design
- Scalability assessment
- Performance prediction

## Examples
- "Design an architecture for this complex distributed system"
- "Plan a multi-layered system architecture with intelligent agents"
- "Create a system architecture with comprehensive constraints"

## Guidelines
- Maintain architectural consistency across all components
- Ensure design aligns with requirements and constraints
- Provide clear, actionable specifications
- Consider scalability and maintainability from the start
- Coordinate effectively with sub-skills
- Document decisions and trade-offs clearly