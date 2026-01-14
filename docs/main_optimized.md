# DNASPEC Documentation - Cognitive-Optimized Structure

## Layer 1: Quick Start & Overview

### What is DNASPEC?
DNASPEC is a Context Engineering System that enhances AI interactions through specialized skills. It prevents context contamination, manages complex tasks, and enforces system constraints.

### Core Value Propositions
- **Context Isolation**: Keep AI interactions focused and clean
- **Task Management**: Break complex work into manageable pieces  
- **Constraint Enforcement**: Maintain consistency and compliance

### Quick Commands
```
/dnaspec.agent-create "role description"     # Create specialized AI agents
/dnaspec.task-decompose "complex task"      # Break tasks into atomic units
/dnaspec.constraint-gen "requirements"      # Generate and check constraints
```

---

## Layer 2: Essential Skills Guide

### When to Use Each Skill

#### Use Agent Creator When:
- You need a specialized AI agent for a specific role
- To prevent context contamination between different AI tasks
- Working on multi-faceted projects requiring role isolation

#### Use Task Decomposer When:
- You have a complex task that's difficult to manage
- AI is getting confused by task complexity
- You need to break work into smaller, isolated components

#### Use Constraint Generator When:
- You have system requirements to enforce
- Evaluating change requests against existing requirements
- Need to maintain consistency across system evolution

---

## Layer 3: Advanced Usage Patterns

### Skill Combinations
- **Agent + Task**: Create specialized agents for each decomposed task
- **Task + Constraint**: Enforce constraints on each atomic task
- **Agent + Constraint**: Limit agent capabilities based on constraints

### Performance Guidelines
- Agent creation: <100ms
- Task decomposition: <200ms  
- Constraint generation: <50ms

### Common Workflows
1. **Project Setup**: Create agents → Decompose tasks → Apply constraints
2. **Change Evaluation**: Define changes → Check constraints → Create specialized agents
3. **Quality Assurance**: Decompose quality tasks → Apply constraint checking

---

## Layer 4: Technical Reference

### Architecture
- All skills inherit from DNASpecSkill base class
- Consistent interface: request string + context object
- Standardized response format across all skills
- File system integration for workspace management

### Extension Points
- Create custom skill classes inheriting from base
- Add new constraint types to generator
- Extend agent capabilities with new functions

### Troubleshooting Decision Tree
- **A**: Issue with agent creation?
  - **B**: Is role description clear? → Improve clarity
  - **C**: Are capabilities valid? → Check capability list
- **A**: Issue with task decomposition?
  - **B**: Is task too complex? → Reduce max_depth
  - **C**: Workspace errors? → Check directory permissions
- **A**: Issue with constraints?
  - **B**: Are requirements valid? → Add more specific requirements
  - **C**: Alignment issues? → Review change request clarity