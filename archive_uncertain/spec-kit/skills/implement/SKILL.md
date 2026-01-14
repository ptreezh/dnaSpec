---
name: speckit-implement
description: Guide implementation of tasks based on specifications, plans, and task breakdowns. Use during the coding and development phase to ensure alignment with original goals.
license: Apache 2.0
metadata:
  speckit-version: 1.0
  speckit-category: implementation
---

# SpecKit - Implementation Guidance

## Overview
This skill provides guidance for implementing tasks based on established specifications, technical plans, and task breakdowns, ensuring alignment with original goals while maintaining code quality and best practices.

## Process

### 1. Prepare Implementation Environment
Before starting implementation:
- Set up development environment per project plan
- Configure required tools and dependencies
- Verify access to necessary services and APIs
- Set up version control and branching strategy

### 2. Review Requirements and Plan
Before implementation, review:
- Original specifications
- Technical plan and architecture decisions
- Specific task requirements and success criteria
- Dependencies on other tasks/components
- Quality standards and coding guidelines

### 3. Implementation Approach
Follow this structured approach to implementation:

#### 3.1 Code Structure
- Follow established project structure patterns
- Implement modular, reusable components
- Maintain consistent naming conventions
- Organize files logically according to project plan

#### 3.2 Development Best Practices
- Write clean, readable code
- Follow DRY (Don't Repeat Yourself) principles
- Implement proper error handling
- Add appropriate logging
- Write self-documenting code

#### 3.3 Testing Integration
- Write unit tests for new functionality
- Follow test-driven development where appropriate
- Ensure test coverage meets project standards
- Test edge cases and error conditions

#### 3.4 Documentation
- Add inline comments for complex logic
- Update documentation for public APIs
- Describe architectural decisions in code comments
- Ensure code remains maintainable

### 4. Quality Assurance
During implementation:
- Perform regular code reviews
- Run automated tests frequently
- Verify implementation against success criteria
- Check for performance considerations
- Validate security measures

### 5. Integration and Validation
After implementation:
- Integrate with existing components
- Test end-to-end functionality
- Verify performance against requirements
- Conduct peer review
- Update task status and documentation

## Examples
- When implementing a feature: "Implement the user dashboard according to specifications using React components, following the planned architecture and connecting to the backend API"
- When building an API endpoint: "Implement the user creation endpoint following the defined API specification, including validation, authentication, and proper error handling"
- When creating a data pipeline: "Implement the data transformation module according to the specified requirements and technical plan, ensuring proper error handling and monitoring"

## Guidelines
- Follow established coding standards and style guides
- Write modular, testable code
- Implement proper error handling and validation
- Maintain performance considerations
- Ensure security best practices throughout
- Document complex logic and architectural decisions
- Regularly synchronize with project specifications
- Validate implementation against success criteria
- Keep integration in mind throughout development