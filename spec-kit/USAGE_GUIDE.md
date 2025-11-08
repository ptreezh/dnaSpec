# spec.kit Usage Guide

## Overview

spec.kit is a comprehensive toolkit for "Spec-Driven Development" that makes specifications the primary driver of development rather than code. This guide explains how to use spec.kit in different AI environments.

## Installation

### For Claude Code:
1. Install the skills according to Claude's skill installation instructions
2. The skills will be available as tools within Claude Code

### For Other AI CLIs:
1. Copy the commands from the `commands/` directory to `.claude/commands/` in your project
2. The slash commands will be available in your AI agent

## Usage Process

The recommended development process follows 5 steps:

### 1. Establish Project Constitution
```
/speckit.constitution [project-type]
```
This command establishes project principles, coding standards, and development practices that guide the entire development process.

### 2. Create Specifications
```
/speckit.specify [project-description]
```
This command helps create comprehensive project specifications focusing on "what" and "why" rather than implementation details.

### 3. Plan Implementation
```
/speckit.plan [project-description]
```
This command creates technical implementation plans including technology stack choices, architecture decisions, and development approach.

### 4. Break Down Tasks
```
/speckit.tasks [project-description]
```
This command breaks down project specifications and plans into executable tasks with clear responsibilities, dependencies, and success criteria.

### 5. Guide Implementation
```
/speckit.implement [task-description]
```
This command provides guidance for implementing tasks based on specifications, plans, and task breakdowns.

## Claude Skills Usage

When using Claude Skills, the commands are available as tools within the Claude interface. Simply describe what you want to do, and Claude will automatically select the appropriate skill from the spec.kit collection.

For example:
- "Help me create a specification for a user dashboard" - Claude will use the speckit-specify skill
- "Plan the technical implementation for this REST API" - Claude will use the speckit-plan skill

## Other AI CLI Usage

When using slash commands in other AI CLIs, use the commands as shown in the examples above. The commands will generate appropriate content based on the templates and guidelines defined in the spec.kit.

## Templates

spec.kit includes several templates that are used by the commands:

- `specification-template.md` - For creating project specifications
- `project-plan-template.md` - For creating technical implementation plans
- `task-list-template.md` - For breaking down work into executable tasks
- `implementation-template.md` - For guiding task implementation
- `constitution-template.md` - For establishing project governance

## Best Practices

1. Start with `/speckit.constitution` to establish project guidelines
2. Follow the sequence: constitution → specify → plan → tasks → implement
3. Use clear, descriptive arguments with your commands
4. Review and refine outputs from each step before proceeding
5. Keep specifications focused on requirements rather than implementation
6. Ensure plans align with both requirements and available resources
7. Break tasks into manageable, testable units
8. Validate implementation against original specifications

## Troubleshooting

If commands are not working:
1. Ensure the commands directory is correctly placed in `.claude/commands/`
2. Verify your AI agent supports slash commands
3. Check that the command file names match the expected slash command names
4. Confirm proper file permissions on the command files

For Claude Skills:
1. Ensure skills are properly installed and enabled
2. Verify Claude Code or Claude.ai is properly configured to use skills
3. Check that skill permissions are properly set