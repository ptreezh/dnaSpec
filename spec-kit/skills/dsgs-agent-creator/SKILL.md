---
name: dsgs-agent-creator
description: DSGS Agent Creator sub-skill for creating and configuring intelligent agents, defining agent roles and behaviors, and generating agent specification documents. Use when you need to create agents, configure agent systems, design multi-agent systems, or define agent roles and behaviors.
license: Apache 2.0
allowed-tools: 
  - Bash(python:scripts/agent_creator.py)
metadata:
  speckit-version: 1.0
  speckit-category: agents
---

# DSGS Agent Creator

## Overview
DSGS Agent Creator is a specialized sub-skill of the DSGS Intelligent Architect system. It focuses on creating and configuring intelligent agents, defining agent roles and behaviors, and generating comprehensive agent specification documents. This skill designs agents that can operate autonomously or in coordination to achieve project objectives.

## Core Functions

### 1. Agent Type Selection
Analyze project requirements to select appropriate agent types:
- Task-specific agents for specialized operations
- Communication agents for coordination
- Monitoring agents for observation and reporting
- Decision-making agents for complex logic
- Learning agents for adaptive behavior

### 2. Role and Behavior Definition
Define agent roles and behavior patterns:
- Agent responsibilities and scope
- Decision-making authority and boundaries
- Interaction patterns with other components
- Goal-oriented behaviors and objectives
- Ethical and safety constraints

### 3. Agent Specification Generation
Create comprehensive agent specifications:
- Technical requirements and capabilities
- Input/output interfaces and protocols
- State management and memory systems
- Performance characteristics
- Integration touchpoints

### 4. Communication Protocol Design
Configure agent communication mechanisms:
- Internal communication patterns
- External interface protocols
- Message formats and serialization
- Coordination and synchronization methods
- Error handling and recovery procedures

### 5. Monitoring and Management
Define agent oversight mechanisms:
- Performance monitoring strategies
- Behavioral compliance checking
- Configuration management procedures
- Debugging and troubleshooting approaches
- Lifecycle management protocols

## Agent Creation Process

### Phase 1: Requirements Analysis
- Analyze project requirements for agent needs
- Identify tasks suitable for agent implementation
- Determine agent interaction patterns required
- Assess complexity and autonomy requirements
- Define success criteria for agent behavior

### Phase 2: Agent Design
- Select appropriate agent architectures
- Define agent capabilities and limitations
- Plan for agent autonomy and decision-making
- Design agent learning and adaptation mechanisms
- Establish safety and ethical boundaries

### Phase 3: Role Definition
- Specify agent responsibilities and duties
- Define agent authority boundaries
- Establish goal hierarchies and priorities
- Design conflict resolution mechanisms
- Plan for agent cooperation and coordination

### Phase 4: Technical Specification
- Define agent interfaces and protocols
- Specify data formats and communication methods
- Plan for state management and memory
- Design error handling and recovery
- Establish security and privacy measures

### Phase 5: Implementation Guidance
- Provide configuration recommendations
- Define deployment strategies
- Plan for testing and validation
- Establish monitoring and management procedures
- Document operational guidelines

## Agent Types

### Reactive Agents
- Respond to environmental stimuli
- Simple condition-action rules
- Fast response times
- Predictable behavior patterns
- Suitable for simple tasks

### Deliberative Agents
- Maintain internal models of the world
- Plan actions before executing
- Consider multiple alternatives
- Better for complex decision-making
- Higher computational requirements

### Learning Agents
- Adapt behavior based on experience
- Improve performance over time
- Handle uncertain environments
- Require training and evaluation
- Suitable for dynamic scenarios

### Hybrid Agents
- Combine multiple architectures
- Balance different capability requirements
- Offer flexibility in approach
- More complex to design and maintain
- Optimal for sophisticated tasks

## Advanced Features

### Multi-Agent Coordination
- Coordination protocol design
- Resource allocation mechanisms
- Task distribution strategies
- Conflict resolution procedures
- Consensus and negotiation mechanisms

### Agent Communication
- Message passing patterns
- Shared memory systems
- Blackboard architectures
- Publish-subscribe systems
- Direct communication channels

### Cognitive Architectures
- Memory systems and management
- Reasoning and decision-making frameworks
- Learning and adaptation mechanisms
- Attention and focus systems
- Meta-cognitive capabilities

### Emergent Behavior Design
- Design for emergence rather than programming
- Create interaction patterns that lead to desired outcomes
- Plan for unexpected behaviors
- Ensure robustness in complex systems
- Balance emergence with control

## Output Format

The agent creation will provide:

1. **Agent Specification Documents**
   - Agent type and architecture
   - Capabilities and limitations
   - Interface definitions
   - Performance characteristics

2. **Role and Behavior Definitions**
   - Agent responsibilities and duties
   - Decision-making authority
   - Interaction patterns
   - Goal structures

3. **Configuration Files**
   - Agent settings and parameters
   - Communication protocols
   - Security configurations
   - Performance tuning options

4. **Communication Protocols**
   - Message formats and structures
   - Communication patterns
   - Coordination mechanisms
   - Error handling procedures

5. **Management Strategies**
   - Monitoring approaches
   - Configuration management
   - Lifecycle procedures
   - Troubleshooting guidelines

## Examples
- "Create an agent for automated testing"
- "Design a multi-agent system for resource allocation"
- "Define an agent role for data processing"

## Guidelines
- Design agents with appropriate level of autonomy
- Ensure clear boundaries and responsibilities
- Plan for coordination and communication
- Consider safety and ethical constraints
- Document agent behavior thoroughly
- Design for maintainability and debugging