---
name: dnaspec-system-architect
description: DNASPEC System Architect sub-skill for system architecture design, technology stack selection, module division, and interface definition. Use when you need to design system architectures, select technology stacks, divide modules, or define interfaces.
license: Apache 2.0
allowed-tools: 
  - Bash(python:scripts/system_architect_designer.py)
metadata:
  speckit-version: 1.0
  speckit-category: architecture
---

# DNASPEC System Architect

## Overview
DNASPEC System Architect is a specialized sub-skill of the DNASPEC Intelligent Architect system. It focuses on system architecture design, technology stack selection, module division, and interface definition for complex projects. This skill creates comprehensive architectural designs that balance functionality, performance, scalability, and maintainability.

## Core Functions

### 1. Requirements Analysis
Analyze project requirements and technical constraints to understand:
- Functional requirements and expected capabilities
- Non-functional requirements (performance, scalability, security)
- Technical constraints and limitations
- Integration requirements with existing systems
- Compliance and regulatory requirements

### 2. Architecture Design
Create comprehensive system architecture designs:
- High-level system architecture diagrams
- Component relationships and interactions
- Data flow and processing patterns
- Service boundaries and responsibilities
- Communication protocols and patterns

### 3. Technology Stack Selection
Select appropriate technology stack and frameworks:
- Evaluate technology options based on requirements
- Consider team expertise and maintainability
- Assess long-term viability and support
- Balance innovation with stability
- Plan for scalability and performance needs

### 4. Module Division
Define module structure and boundaries:
- Identify logical module boundaries
- Establish module responsibilities
- Define module interaction patterns
- Plan for module independence and cohesion
- Consider future extensibility

### 5. Interface Definition
Design interfaces between components:
- API specifications and contracts
- Data format and serialization standards
- Error handling and retry mechanisms
- Security and authentication patterns
- Monitoring and logging interfaces

## Architecture Design Process

### Phase 1: Requirements Understanding
- Analyze project requirements in detail
- Identify critical success factors
- Document technical and business constraints
- Clarify ambiguous requirements
- Establish priority and criticality

### Phase 2: High-Level Architecture Design
- Create system context diagrams
- Define major system components
- Establish component relationships
- Plan for data flow and processing
- Consider integration points

### Phase 3: Technology Selection
- Evaluate technology options against requirements
- Assess team capabilities and learning curve
- Consider ecosystem and integration factors
- Plan for deployment and operational needs
- Document selection rationale

### Phase 4: Detailed Design
- Design component interfaces and contracts
- Define module boundaries and responsibilities
- Specify data models and schemas
- Plan for error handling and fault tolerance
- Design for scalability and performance

### Phase 5: Architecture Validation
- Verify architecture against requirements
- Identify potential risks and mitigations
- Assess scalability and performance characteristics
- Plan for security and compliance
- Document design decisions and trade-offs

## Technology Considerations

### Architecture Patterns
- Microservices vs. monolithic considerations
- Event-driven vs. request-response patterns
- Layered architecture principles
- Domain-driven design concepts
- Service-oriented architecture patterns

### Scalability Planning
- Horizontal vs. vertical scaling strategies
- Load distribution and balancing
- Caching strategies and patterns
- Database scaling approaches
- CDN and content distribution

### Security Design
- Authentication and authorization mechanisms
- Data encryption and privacy considerations
- Network security and isolation
- API security and rate limiting
- Compliance with security standards

### Performance Optimization
- Response time and throughput requirements
- Database query optimization
- Resource utilization patterns
- Concurrency and parallelism design
- Monitoring and performance metrics

## Output Format

The architecture design will provide:

1. **System Architecture Diagrams**
   - High-level architecture overview
   - Component interaction diagrams
   - Data flow diagrams
   - Deployment architecture

2. **Technology Stack Specification**
   - Selected technologies and frameworks
   - Rationale for each selection
   - Version recommendations
   - Integration approach

3. **Module Division Plan**
   - Module boundaries and responsibilities
   - Module interaction patterns
   - Dependency relationships
   - Module cohesion principles

4. **Interface Definitions**
   - API specifications and contracts
   - Data schema definitions
   - Error handling protocols
   - Security implementation

5. **Architecture Documentation**
   - Design decisions and rationale
   - Risk assessments and mitigations
   - Future evolution considerations
   - Implementation guidelines

## Advanced Features

### Multi-Cloud Architecture Planning
- Cloud provider selection criteria
- Multi-cloud deployment strategies
- Vendor lock-in mitigation strategies
- Cost optimization across providers

### Resilience and Fault Tolerance
- Circuit breaker patterns
- Retry and timeout strategies
- Graceful degradation mechanisms
- Disaster recovery planning

### Observability Integration
- Logging and monitoring strategies
- Performance metrics definition
- Alerting and notification systems
- Tracing and debugging capabilities

## Examples
- "Design a system architecture for this web application"
- "Select a technology stack for this distributed system"
- "Define module boundaries for this enterprise application"

## Guidelines
- Balance functionality with scalability requirements
- Consider maintainability and operational needs
- Document design decisions and trade-offs
- Plan for future growth and changes
- Ensure security and compliance from the start
- Align architecture with business objectives