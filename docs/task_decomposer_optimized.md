# Task Decomposer Skill - Optimized Documentation

## Layer 1: Conceptual Overview
**Purpose**: Breaks complex tasks into smaller, atomic components with isolated workspaces
**Value**: Prevents context explosion in AI interactions by isolating task components
**Quick Start**: `/dnaspec.task-decompose "Build a website" max_depth=2`

---

## Layer 2: Core Usage

### Basic Command
```
/dnaspec.task-decompose <task_description>
```

### Common Parameters
- `max_depth`: Maximum decomposition depth (1-3)
- `workspace_base`: Base directory for isolated workspaces

### Examples
```
# Decompose a simple task
/dnaspec.task-decompose "Build a website" max_depth=2

# Decompose with custom workspace location
/dnaspec.task-decompose "Design API and implement" max_depth=2 workspace_base="./project_workspaces"
```

### Expected Output
- Hierarchical task breakdown
- Isolated workspace paths for each atomic task
- Validation metrics
- Depth and count information

### Error Handling
- Excessive task depth triggers warnings
- Malformed tasks return decomposition suggestions

---

## Layer 3: Advanced Features

### Configuration Options
- Subtask limits to prevent explosion
- Recursive depth controls
- Workspace isolation enforcement

### Integration Patterns
- Use with agent creator for task-specific AI agents
- Combine with constraint generator to set task boundaries

### Performance Considerations
- Decomposition time: <200ms for typical tasks
- File system operations for workspace creation

### Troubleshooting
- If decomposition seems incorrect: Check task description clarity
- If performance is slow: Reduce max_depth parameter
- If workspaces don't appear: Verify workspace_base permissions

---

## Layer 4: Implementation Details

### API Specification
```
Input: {
  task_description: string (required),
  max_depth?: number (default: 2, max: 3),
  workspace_base?: string (default: "./workspaces")
}
Output: {
  decomposition: {
    id: string,
    description: string,
    is_atomic: boolean,
    depth: number,
    subtasks: [...],
    workspace: string
  },
  validation: {
    is_valid: boolean,
    issues: string[],
    metrics: {
      total_tasks: number,
      max_depth: number
    }
  },
  success: boolean,
  timestamp: number
}
```

### Architecture
- Recursive decomposition algorithm
- File system workspace management
- Task explosion prevention mechanisms
- Validation and quality metrics

### Extension Points
- Custom splitting heuristics
- Advanced dependency tracking
- Integration with project management tools