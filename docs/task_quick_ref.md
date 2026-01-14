# TASK DECOMPOSER - Quick Reference Card

## Purpose
Break complex tasks into atomic components with isolated workspaces to prevent context explosion in AI interactions.

## Core Command
```
/dnaspec.task-decompose <task_description>
```

## Parameters
- `max_depth` (optional): Maximum decomposition depth (default: 2, max: 3)
- `workspace_base` (optional): Base directory for isolated workspaces (default: "./workspaces")

## Examples
```
# Decompose with default settings
/dnaspec.task-decompose "Build a website" max_depth=2

# Decompose with custom workspace location  
/dnaspec.task-decompose "Develop API" max_depth=2 workspace_base="./api_workspaces"
```

## Output
```
{
  decomposition: {
    id: "task_unique_uuid",
    description: "original task",
    is_atomic: false,  // true for atomic tasks
    depth: 0,          // current depth in hierarchy
    subtasks: [...],   // array of child tasks if any
    workspace: "/path/to/isolated/workspace"
  },
  validation: {
    is_valid: true,
    metrics: {
      total_tasks: N,
      max_depth: N
    }
  }
}
```

## Key Benefits
- Prevents AI context explosion
- Creates isolated workspaces for atomic tasks
- Maintains clear boundaries between tasks

## Performance
- Decomposition time: <200ms
- Creates file system workspaces automatically
- Task explosion prevention built-in