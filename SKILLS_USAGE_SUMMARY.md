# DNASPEC Skills Usage Summary

## Overview

This document summarizes the various skills available in the DNASPEC system and their usage methods and scenarios. DNASPEC (Dynamic Specification Growth System) provides a comprehensive suite of context engineering skills designed to enhance AI-assisted development workflows.

## Core Context Engineering Skills

### 1. Context Analysis Skill

**Purpose**: Analyzes input context across five dimensions of quality: clarity, relevance, completeness, consistency, and efficiency.

**Usage Methods**:
- AI CLI command: `/dnaspec.context-analysis "content to analyze"`
- Python API: `execute({'skill': 'context-analysis', 'context': 'your content'})`
- Direct function: `execute_context_analysis('your content')`

**Scenarios**:
- Analyzing user stories for clarity and completeness
- Reviewing technical specifications for consistency
- Evaluating requirements documents for quality
- Preparing content for AI processing

**Example**:
```
/dnaspec.context-analysis "Design a user authentication system with OAuth integration"
```

### 2. Context Optimization Skill

**Purpose**: Optimizes context based on specific goals like clarity, completeness, relevance, and conciseness.

**Usage Methods**:
- AI CLI command: `/dnaspec.context-optimization "content to optimize" --goals clarity,completeness`
- Python API: `execute({'skill': 'context-optimization', 'context': 'content', 'params': {'optimization_goals': ['clarity', 'completeness']}})`
- Direct function: `execute_context_optimization('content', {'optimization_goals': ['clarity']})`

**Scenarios**:
- Improving code generation prompts
- Optimizing documentation for clarity
- Enhancing requirement specifications
- Preparing inputs for other AI tools

**Example**:
```
/dnaspec.context-optimization "Write clean code" --goals clarity,completeness
```

### 3. Cognitive Template Skill

**Purpose**: Applies cognitive frameworks to structure complex tasks using templates like chain-of-thought reasoning, verification, few-shot learning, and role-playing.

**Usage Methods**:
- AI CLI command: `/dnaspec.cognitive-template "task" template=chain_of_thought`
- Python API: `execute({'skill': 'cognitive-template', 'context': 'task', 'params': {'template': 'verification'}})`
- Direct function: `execute_cognitive_template('task', {'template': 'few_shot'})`

**Scenarios**:
- Breaking down complex problems systematically
- Applying verification checks to solutions
- Using few-shot learning patterns
- Role-playing for domain expertise

**Example**:
```
/dnaspec.cognitive-template "How to design API interfaces" --template verification
```

## Advanced Agentic Skills

### 4. Agent Creator Skill

**Purpose**: Creates specialized AI agents with defined roles, capabilities, and configurations based on requirements.

**Usage Methods**:
- AI CLI command: `/dnaspec.agent-creator "agent requirements"`
- Python API: `execute_skill('agent-creator', {'context': 'requirements'})`
- Direct function: `execute_agent_creator({'context': 'requirements'})`

**Agent Types**:
- Reactive: Fast response, rule-based decision making
- Deliberative: Analytical, strategic planning
- Learning: Adaptive, predictive capabilities
- Hybrid: Combines multiple approaches

**Agent Roles**:
- Task Executor: Performs specific tasks
- Communication: Handles inter-agent communication
- Monitoring: Tracks system performance
- Decision Maker: Makes strategic decisions
- Learning: Adapts and improves over time

**Scenarios**:
- Building multi-agent systems for complex projects
- Creating domain-specific specialists
- Designing autonomous monitoring systems
- Implementing task-specific assistants

**Example**:
```
/dnaspec.agent-creator "Create an intelligent agent that monitors server performance metrics"
```

### 5. System Architect Skill

**Purpose**: Designs system architecture and technical specifications with technology stacks and module definitions.

**Usage Methods**:
- AI CLI command: `/dnaspec.architect "system requirements"`
- Python API: `execute_architect({'context': 'requirements'})`
- Direct function: `execute_architect({'context': 'requirements'})`

**Scenarios**:
- Designing new system architectures
- Migrating legacy systems
- Planning scalability solutions
- Defining technology stacks

**Example**:
```
/dnaspec.architect "Design microservices architecture for e-commerce"
```

### 6. Task Decomposer Skill

**Purpose**: Breaks down complex projects into atomic, manageable tasks with dependencies and resource estimates.

**Usage Methods**:
- AI CLI command: `/dnaspec.task-decomposer "project requirements"`
- Python API: `execute_task_decomposer({'context': 'requirements'})`
- Direct function: `execute_task_decomposer({'context': 'requirements'})`

**Scenarios**:
- Project planning and sprint breakdown
- Resource allocation and timeline estimation
- Creating work breakdown structures
- Identifying critical path activities

**Example**:
```
/dnaspec.task-decomposer "Break down this feature into development tasks"
```

### 7. Constraint Generator Skill

**Purpose**: Identifies and formalizes system constraints and validation rules for development.

**Usage Methods**:
- AI CLI command: `/dnaspec.constraint-generator "system requirements"`
- Python API: `execute_constraint_generator({'context': 'requirements'})`
- Direct function: `execute_constraint_generator({'context': 'requirements'})`

**Constraint Categories**:
- Performance: Response times, throughput, latency
- Security: Authentication, authorization, encryption
- Data: Integrity, privacy, compliance
- Quality: Reliability, availability, maintainability

**Scenarios**:
- Generating compliance requirements
- Defining performance benchmarks
- Creating security mandates
- Establishing resource limits

**Example**:
```
/dnaspec.constraint-generator "Generate security constraints for this API"
```

### 8. DAPI Checker Skill

**Purpose**: Analyzes and validates API interfaces and specifications for correctness and best practices.

**Usage Methods**:
- AI CLI command: `/dnaspec.dapi-checker "API specification"`
- Python API: `execute_dapi_checker({'context': 'spec'})`
- Direct function: `execute_dapi_checker({'context': 'spec'})`

**Scenarios**:
- API design review and validation
- Contract validation for microservices
- Interface compliance checking
- Quality assurance for APIs

**Example**:
```
/dnaspec.dapi-checker "Validate this REST API specification"
```

### 9. Modulizer Skill

**Purpose**: Breaks down systems into reusable and maintainable modules with clear boundaries and interfaces.

**Usage Methods**:
- AI CLI command: `/dnaspec.modulizer "system architecture"`
- Python API: `execute_modulizer({'context': 'architecture'})`
- Direct function: `execute_modulizer({'context': 'architecture'})`

**Scenarios**:
- System refactoring into microservices
- Creating modular architecture designs
- Defining component boundaries
- Architectural modernization

**Example**:
```
/dnaspec.modulizer "Extract reusable modules from this codebase"
```

## Support and Infrastructure Skills

### 10. Workspace Management Skill

**Purpose**: Manages AI-generated files in secure workspace, preventing project pollution.

**Usage Methods**:
- AI CLI command: `/dnaspec.workspace create`, `/dnaspec.workspace add file content`, etc.

**Operations**:
- Create: Initialize secure workspace
- Add: Add files to workspace with isolation
- List: List workspace files
- Stage: Move files to staging area for validation
- Verify: Validate staged files
- Promote: Promote verified files to main project

**Scenarios**:
- Isolating AI-generated code for review
- Managing temporary AI output files
- Preventing unwanted changes to the project
- Maintaining clean project structure

**Example**:
```
/dnaspec.workspace create
/dnaspec.workspace add "auth.py" "import hashlib..."
/dnaspec.workspace stage "auth.py"
```

### 11. Git Operations Skill

**Purpose**: Executes Git workflow operations safely with AI-assisted development workflows.

**Usage Methods**:
- AI CLI command: `/dnaspec.git status`, `/dnaspec.git commit "message"`, etc.

**Operations**:
- Status: Show repository status
- Add: Add files to staging
- Commit: Commit changes with proper messages
- Push/Pull: Manage remote synchronization
- Branch: Create and manage branches
- Log: Show commit history

**Scenarios**:
- Managing AI-assisted development commits
- Safely integrating AI-generated code
- Following Git best practices
- Maintaining version control integrity

**Example**:
```
/dnaspec.git status
/dnaspec.git commit "Fix authentication bug"
/dnaspec.git branch feature/new-feature
```

## Integration with AI CLI Platforms

### Supported Platforms
- Claude Desktop
- Cursor
- VS Code
- Windsurf
- Continue.dev
- Qwen CLI
- Gemini CLI
- GitHub Copilot

### Integration Process
1. Install DNASPEC CLI extension
2. Deploy skills for specific AI platform
3. Use slash commands directly in AI chat
4. Leverage skills through Python API for automation

### Command Format
- `/dnaspec.[skill-name] "context or requirements"`
- Optional parameters: `--parameter value`
- Examples provided for each skill

## Security and Safety Features

### Project Constitution
- Establishes rules for AI-assisted development
- Prevents project pollution through staged work
- Maintains Git repository hygiene
- Ensures code quality standards

### Isolation Mechanisms
- Temporary workspaces for AI-generated content
- Validation before integration
- Review processes for AI output
- Clean workspace maintenance

## Best Practices

1. **Start with Analysis**: Use context analysis to understand quality before optimization
2. **Apply Templates**: Use cognitive templates for complex problems
3. **Create Specialized Agents**: Use agent creator for recurring tasks
4. **Maintain Isolation**: Always use workspace management for AI-generated files
5. **Follow Process**: Use skills in sequence for comprehensive results
6. **Validate Results**: Always verify AI-generated outputs before integration

## Workflow Integration

### Development Workflow
1. Analyze requirements with context analysis
2. Optimize with cognitive templates
3. Design architecture with system architect
4. Decompose tasks with task decomposer
5. Generate constraints and validation rules
6. Create specialized agents for specific tasks
7. Validate APIs with DAPI checker
8. Modularize with modulizer
9. Manage workspace and Git operations safely

### AI-Assisted Development
- Use skills to enhance AI conversations
- Prepare high-quality prompts
- Verify AI outputs systematically
- Maintain project quality standards
- Follow secure integration practices