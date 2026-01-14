# DNASPEC - Context Engineering System

**For New AI Systems**: Start with [PROJECT_ENTRY_GUIDE.md](PROJECT_ENTRY_GUIDE.md) for rapid understanding of the project.

**Cognitive-Load-Optimized Overview**: Read [PROJECT_MEMORY_OPTIMIZED.md](PROJECT_MEMORY_OPTIMIZED.md) for reduced cognitive load.

**Mission**: Enhance AI interactions through specialized skills that manage context quality, prevent contamination, and enforce system constraints.

## Core Skills

| Skill | Purpose | Command | Key Benefit |
|-------|---------|---------|-------------|
| **Agent Creator** | Create specialized AI agents | `/dnaspec.agent-create` | Context isolation for focused tasks |
| **Task Decomposer** | Break complex tasks into atomic units | `/dnaspec.task-decompose` | Prevent context explosion |
| **Constraint Generator** | Generate and manage system constraints | `/dnaspec.constraint-gen` | Maintain requirements consistency |

## Quick Start
```bash
# Create specialized agents
/dnaspec.agent-create "Python code reviewer"

# Decompose complex tasks
/dnaspec.task-decompose "Build a web app" max_depth=2

# Generate constraints from requirements
/dnaspec.constraint-gen "System with security" change_request="Add feature"
```

## Architecture
- All skills inherit from `DNASpecSkill` base class
- Consistent interface: `request` string + `context` object
- Lightweight operations (<200ms each)
- Minimal dependencies

## Performance
- Agent Creation: <100ms
- Task Decomposition: <200ms
- Constraint Generation: <50ms