---
allowed-tools: Bash(fs.createFile:*), Bash(fs.writeFile:*), Bash(fs.readFile:*)
argument-hint: [project-description]
description: Create project specifications focusing on "what" and "why" rather than implementation details
model: claude-3-5-sonnet-20241022
---

# Specification Creation Process

## Task
Create a comprehensive project specification based on the following description: $ARGUMENTS

## Process to Follow
1. Analyze the core requirements:
   - What problem is being solved?
   - Who are the stakeholders?
   - What are the functional requirements?
   - What are the non-functional requirements?

2. Create a specification document structure that includes:
   - Problem Statement: Clear description of the problem, context and background
   - Requirements: Functional and non-functional requirements
   - Scope: In scope items, out of scope items, dependencies
   - Success Metrics: How to measure success, key performance indicators

3. Validate against best practices:
   - Ensure clarity and unambiguity
   - Check completeness against requirements
   - Verify feasibility within constraints

## Output Requirements
- Focus on what needs to be built, not how it will be built
- Use clear, unambiguous language
- Include measurable success criteria
- Consider all stakeholders' needs
- Specify constraints and limitations upfront
- Document dependencies and assumptions
- Structure the specification in a clear, organized format