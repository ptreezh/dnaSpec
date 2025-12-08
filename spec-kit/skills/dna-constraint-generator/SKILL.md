---
name: dnaspec-constraint-generator
description: DNASPEC Constraint Generator sub-skill for generating system constraints, API specification constraints, data constraints, and quality constraints. Use when you need to generate constraints, API specifications, data validation rules, or quality constraints.
license: Apache 2.0
allowed-tools: 
  - Bash(python:scripts/constraint_generator.py)
metadata:
  speckit-version: 1.0
  speckit-category: constraints
---

# DNASPEC Constraint Generator

## Overview
DNASPEC Constraint Generator is a specialized sub-skill of the DNASPEC Intelligent Architect system. It focuses on generating comprehensive system constraints, API specification constraints, data constraints, and quality constraints based on project requirements and architectural design. This skill ensures that systems are designed with appropriate boundaries, rules, and quality measures from the start.

## Core Functions

### 1. System Constraint Generation
Generate system-level constraints:
- Performance and scalability limits
- Resource utilization boundaries
- Security and access constraints
- Integration and compatibility requirements
- Operational and deployment restrictions

### 2. API Specification Constraints
Define API constraints and interface specifications:
- Request/response format limitations
- Rate limiting and throttling rules
- Authentication and authorization requirements
- Error handling and response codes
- Versioning and backward compatibility constraints

### 3. Data Constraint Definition
Specify data constraints and validation rules:
- Schema and format requirements
- Business rule validations
- Data integrity constraints
- Privacy and security restrictions
- Quality and consistency measures

### 4. Quality Constraint Establishment
Create quality and performance standards:
- Performance benchmarks and SLAs
- Reliability and availability requirements
- Test coverage and quality gates
- Security and compliance standards
- Maintainability and observability requirements

### 5. Validation Mechanism Design
Design constraint validation and enforcement:
- Real-time validation approaches
- Batch validation procedures
- Monitoring and alerting systems
- Compliance checking mechanisms
- Enforcement and governance procedures

## Constraint Generation Process

### Phase 1: Requirements Analysis
- Analyze project requirements for constraint needs
- Identify regulatory and compliance requirements
- Assess performance and quality expectations
- Understand security and privacy requirements
- Determine integration and interoperability constraints

### Phase 2: System Constraint Definition
- Define performance and scalability constraints
- Specify resource utilization limits
- Establish security and access controls
- Plan for operational constraints
- Document architectural boundaries

### Phase 3: API Constraint Design
- Define API format and protocol constraints
- Specify rate limiting and throttling rules
- Plan authentication and authorization requirements
- Design error handling and response constraints
- Establish versioning and compatibility rules

### Phase 4: Data Constraint Specification
- Define data schema and format constraints
- Specify business rule validations
- Plan for data integrity constraints
- Establish privacy and security restrictions
- Design quality and consistency measures

### Phase 5: Quality Constraint Establishment
- Define performance benchmarks and standards
- Specify reliability and availability requirements
- Plan test coverage and quality measures
- Establish security and compliance standards
- Design maintainability and observability constraints

## Constraint Categories

### Performance Constraints
- Response time requirements
- Throughput and concurrency limits
- Resource utilization thresholds
- Scalability requirements
- Latency and bandwidth limitations

### Security Constraints
- Authentication and authorization rules
- Data encryption requirements
- Access control policies
- Audit and logging requirements
- Compliance and privacy restrictions

### Data Constraints
- Schema validation rules
- Business logic constraints
- Data integrity requirements
- Privacy and consent limitations
- Retention and deletion policies

### Quality Constraints
- Test coverage requirements
- Code quality standards
- Reliability and uptime targets
- Error rate and performance thresholds
- Maintainability and documentation standards

### Operational Constraints
- Deployment and infrastructure requirements
- Monitoring and alerting needs
- Backup and recovery procedures
- Maintenance and update windows
- Disaster recovery and business continuity

## Advanced Features

### Constraint Prioritization
- Critical vs. important vs. nice-to-have constraints
- Business impact assessment
- Technical feasibility evaluation
- Implementation priority setting
- Risk-based constraint ranking

### Constraint Validation Strategies
- Schema validation approaches
- Business rule enforcement
- Performance testing procedures
- Security scanning integration
- Compliance checking automation

### Dynamic Constraint Management
- Runtime constraint modification
- Adaptive constraint adjustment
- Constraint inheritance and overriding
- Constraint lifecycle management
- Versioning and evolution strategies

### Constraint Communication
- Clear constraint documentation
- Constraint violation reporting
- Impact analysis for constraint changes
- Constraint negotiation protocols
- Stakeholder constraint alignment

## Output Format

The constraint generation will provide:

1. **System Constraint Documentation**
   - Performance and scalability limits
   - Resource utilization boundaries
   - Security and access constraints
   - Operational restrictions

2. **API Constraint Specifications**
   - Request/response format rules
   - Rate limiting and throttling
   - Authentication requirements
   - Error handling guidelines

3. **Data Constraint Definitions**
   - Schema and format requirements
   - Business rule validations
   - Data integrity constraints
   - Privacy and security rules

4. **Quality Constraint Standards**
   - Performance benchmarks
   - Reliability requirements
   - Test coverage standards
   - Security and compliance measures

5. **Validation Mechanisms**
   - Validation approach and tools
   - Monitoring and alerting systems
   - Enforcement procedures
   - Compliance checking processes

## Examples
- "Generate constraints for this API design"
- "Define data validation rules for this system"
- "Create quality standards for this project"

## Guidelines
- Ensure constraints align with business objectives
- Balance constraint strictness with flexibility
- Make constraints measurable and testable
- Document constraint rationale and impact
- Plan for constraint evolution and changes
- Consider implementation feasibility