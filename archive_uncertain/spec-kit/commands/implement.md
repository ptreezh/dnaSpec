---
allowed-tools: Bash(fs.createFile:*), Bash(fs.writeFile:*), Bash(fs.readFile:*)
argument-hint: [task-description]
description: Guide implementation of tasks based on specifications, plans, and task breakdowns
model: claude-3-5-sonnet-20241022
---

# Implementation Guidance Process

## Task
Provide guidance for implementing the following task based on specifications, plans, and task breakdowns: $ARGUMENTS

## Process to Follow
1. Prepare implementation environment:
   - Set up development environment per project plan
   - Configure required tools and dependencies
   - Verify access to necessary services and APIs
   - Set up version control and branching strategy

2. Review requirements and plan:
   - Original specifications
   - Technical plan and architecture decisions
   - Specific task requirements and success criteria
   - Dependencies on other tasks/components
   - Quality standards and coding guidelines

3. Follow structured implementation approach:
   - Code Structure: Follow established patterns, modular components, naming conventions
   - Development Best Practices: Clean code, DRY principles, error handling, logging
   - Testing Integration: Unit tests, test-driven development, coverage requirements
   - Documentation: Inline comments, API documentation, maintainability

4. Perform quality assurance:
   - Regular code reviews
   - Automated testing
   - Verification against success criteria
   - Performance considerations
   - Security validation

5. Complete integration and validation:
   - Integrate with existing components
   - Test end-to-end functionality
   - Verify performance against requirements
   - Conduct peer review
   - Update task status and documentation

## Output Requirements
- Follow established coding standards and style guides
- Write modular, testable code
- Implement proper error handling and validation
- Maintain performance considerations
- Ensure security best practices throughout
- Document complex logic and architectural decisions
- Regularly synchronize with project specifications
- Validate implementation against success criteria
- Keep integration in mind throughout development
- Provide clear implementation steps and code examples