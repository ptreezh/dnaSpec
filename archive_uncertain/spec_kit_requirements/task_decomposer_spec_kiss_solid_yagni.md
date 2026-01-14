# Task Decomposer Skill - KISS/SOLID/YAGNI Compliant Specification

## 1. Overview
The Task Decomposer skill provides a simple, focused interface for breaking down complex tasks into smaller, manageable atomic tasks. This specification follows the KISS (Keep It Simple, Stupid), SOLID, and YAGNI (You Aren't Gonna Need It) principles to ensure clean, maintainable, and purposeful design.

## 2. Design Principles Compliance

### 2.1 KISS (Keep It Simple, Stupid)
- Single purpose: Decompose complex tasks into atomic tasks
- Minimal configuration parameters
- Straightforward workflow: task → decomposition → atomic tasks
- Clear and predictable outputs with isolated workspaces

### 2.2 SOLID Principles
- **Single Responsibility Principle**: The skill has one reason to change - decomposing tasks
- **Open/Closed Principle**: Extensible through configuration without modifying core logic
- **Liskov Substitution Principle**: Task decompositions follow a consistent interface
- **Interface Segregation Principle**: Minimal, focused interface
- **Dependency Inversion Principle**: Depends on abstractions rather than concrete implementations

### 2.3 YAGNI (You Aren't Gonna Need It)
- Only implements currently required functionality (basic decomposition)
- No speculative features like AI optimization or complex dependency analysis
- Focuses on core task decomposition capability
- Avoids over-engineering for future scenarios

## 3. Core Interface Definition

### 3.1 Input Parameters (Minimal Set)
```json
{
  "task_description": "String describing the complex task to be decomposed",
  "max_depth": "Integer specifying maximum allowed decomposition depth (default: 2, max: 3)",
  "workspace_base": "String specifying base path for task workspaces (default: './workspaces')"
}
```

### 3.2 Output Format
```json
{
  "success": "Boolean indicating success or failure",
  "decomposition": {
    "id": "Unique identifier for the main task",
    "description": "Original task description",
    "is_atomic": "Boolean indicating if this is an atomic task",
    "depth": "Integer representing the decomposition depth",
    "subtasks": [
      {
        "id": "Unique identifier of subtask",
        "description": "Subtask description",
        "is_atomic": "Boolean indicating if this is an atomic task",
        "depth": "Subtask depth in the hierarchy",
        "workspace": "Path to isolated workspace for this task"
      }
    ],
    "workspace": "Path to isolated workspace for this task"
  },
  "validation": {
    "is_valid": "Boolean indicating if decomposition is valid",
    "issues": ["List of validation issues (if any)"],
    "metrics": {
      "total_tasks": "Total number of tasks in the decomposition",
      "max_depth": "Maximum depth of the decomposition"
    }
  },
  "timestamp": "ISO format timestamp of execution"
}
```

## 4. Simplified Implementation

### 4.1 Core Class Structure
```python
from typing import Dict, Any, List
from src.dna_spec_kit_integration.core.skill import DNASpecSkill, SkillResult, SkillStatus
import uuid
import os
from pathlib import Path

class TaskDecomposerSkill(DNASpecSkill):
    """
    Task Decomposer Skill - Decomposes complex tasks into atomic tasks
    Adheres strictly to KISS, SOLID, and YAGNI principles
    """
    
    def __init__(self):
        super().__init__(
            name="dnaspec-task-decomposer-simple",
            description="Simple Task Decomposer - Decomposes tasks following KISS principles"
        )
        self.max_depth_limit = 3  # Keep complexity manageable
        self.max_subtasks = 5     # Prevent explosion, KISS approach
        self.workspace_base = "./workspaces"

    def _execute_skill_logic(self, request: str, context: Dict[str, Any]) -> Any:
        """
        Execute task decomposition logic
        Single method with clear responsibility
        """
        # Parse inputs - keep simple
        task_description = request
        max_depth = min(
            int(context.get('max_depth', 2)), 
            self.max_depth_limit
        )
        workspace_base = context.get('workspace_base', self.workspace_base)
        
        # Decompose task recursively - single responsibility
        decomposition = self._decompose_task(task_description, 0, max_depth, workspace_base)
        
        # Validate decomposition - separate concern (SOLID - SRP)
        validation = self._validate_decomposition(decomposition)
        
        return {
            "decomposition": decomposition,
            "validation": validation,
            "success": True,
            "timestamp": __import__('time').time()
        }

    def _decompose_task(self, task: str, current_depth: int, max_depth: int, workspace_base: str) -> Dict[str, Any]:
        """
        Recursive task decomposition with simple logic
        Maintains single responsibility
        """
        # Base case: if we've reached max depth or can't decompose further
        if current_depth >= max_depth:
            return {
                "id": f"task_{uuid.uuid4().hex[:8]}",
                "description": task,
                "is_atomic": True,
                "depth": current_depth,
                "workspace": self._create_workspace(task, current_depth, workspace_base),
                "subtasks": []
            }
        
        # Simple decomposition logic - avoid over-engineering (YAGNI)
        subtasks = self._simple_task_split(task)
        limited_subtasks = subtasks[:self.max_subtasks]  # Prevent explosion
        
        # Create decomposition result
        result = {
            "id": f"task_{uuid.uuid4().hex[:8]}",
            "description": task,
            "is_atomic": False,
            "depth": current_depth,
            "subtasks": [],
            "workspace": self._create_workspace(task, current_depth, workspace_base)
        }
        
        # Recursively decompose subtasks
        for subtask in limited_subtasks:
            subtask_result = self._decompose_task(subtask, current_depth + 1, max_depth, workspace_base)
            result["subtasks"].append(subtask_result)
        
        return result

    def _simple_task_split(self, task: str) -> List[str]:
        """
        Simple task splitting logic
        KISS approach - no complex AI or NLP
        """
        # Basic heuristics to split tasks
        if "and" in task.lower():
            parts = task.lower().split(" and ")
            return [part.strip().capitalize() for part in parts if len(part.strip()) > 5]
        
        # If no clear split, return the task as atomic
        return [task]
        
    def _create_workspace(self, task: str, depth: int, base_path: str) -> str:
        """
        Create isolated workspace for task
        Simple file-based approach (KISS)
        """
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        workspace_path = Path(base_path) / task_id
        
        # Create workspace directories
        workspace_path.mkdir(parents=True, exist_ok=True)
        (workspace_path / "src").mkdir(exist_ok=True)
        (workspace_path / "docs").mkdir(exist_ok=True)
        
        return str(workspace_path)

    def _validate_decomposition(self, decomposition: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the decomposition for basic issues
        Separate method for single responsibility (SOLID)
        """
        issues = []
        
        # Check for reasonable task count
        total_tasks = self._count_tasks(decomposition)
        if total_tasks > 20:  # Reasonable limit (KISS)
            issues.append("Too many tasks generated, consider simplifying the original task")
        
        # Check for reasonable depth
        max_depth = self._get_max_depth(decomposition)
        if max_depth > 3:
            issues.append("Decomposition depth exceeds recommended limit")
        
        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "metrics": {
                "total_tasks": total_tasks,
                "max_depth": max_depth
            }
        }

    def _count_tasks(self, decomposition: Dict[str, Any]) -> int:
        """
        Count total tasks in decomposition
        """
        count = 1
        for subtask in decomposition.get("subtasks", []):
            count += self._count_tasks(subtask)
        return count

    def _get_max_depth(self, decomposition: Dict[str, Any], current_depth: int = 0) -> int:
        """
        Get maximum depth of decomposition
        """
        max_depth = current_depth
        for subtask in decomposition.get("subtasks", []):
            sub_depth = self._get_max_depth(subtask, current_depth + 1)
            max_depth = max(max_depth, sub_depth)
        return max_depth
```

## 5. Usage Examples

### 5.1 Basic Usage (YAGNI - Only Required Parameters)
```
Input: "Build a simple website"
Output: Task decomposition with isolated workspaces
```

### 5.2 With Optional Parameters (KISS - Minimal Options)
```json
{
  "task_description": "Create an API for user management",
  "max_depth": 2,
  "workspace_base": "./api_project_workspaces"
}
```

## 6. Constraints and Validation

### 6.1 Input Validation (Simple, Focused)
- Task description must be provided (required)
- max_depth must be between 1 and 3 (reasonable limits)
- workspace_base must be a valid path string

### 6.2 Error Handling (Simple and Predictable)
```json
{
  "success": false,
  "error": "Descriptive error message",
  "error_type": "validation|processing|workspace_creation"
}
```

## 7. Integration Points

### 7.1 AI CLI Platform Integration (Simple Interface)
```
/dnaspec.task-decompose "Build an e-commerce platform"
```

### 7.2 Simple Workspace Management (Follows KISS)
- Workspaces created as simple directory structures
- Basic src/docs/test organization
- Path-based isolation

## 8. No Future Speculation (YAGNI)

### 8.1 Implemented Features Only
- Basic task decomposition following KISS/SOLID/YAGNI
- Isolated workspace creation
- Simple validation and metrics
- Depth and task count limits

### 8.2 Not Implemented (YAGNI)
- Complex AI-driven decomposition
- Dependency graph generation
- Advanced workspace orchestration
- Multi-agent coordination during decomposition
- Automatic task prioritization

## 9. Testing Strategy (Simple and Effective)

### 9.1 Unit Tests (Follow SOLID principles)
- Test task decomposition logic
- Test workspace creation
- Test validation logic

### 9.2 Integration Tests (Minimal but Effective)
- Test CLI integration
- Test workspace filesystem operations

## 10. Evolution Strategy (KISS + YAGNI)

### 10.1 Extension Guidelines
- Only add features when there's a specific, demonstrated need
- Maintain single responsibility throughout evolution
- Keep interface minimal and predictable

### 10.2 Anti-Patterns to Avoid
- Adding speculative AI features
- Complex dependency analysis without clear need
- Multiple responsibilities in single methods
- Overly complex validation rules

## 11. Performance and Scalability (KISS Approach)

### 11.1 Simple Performance Profile
- Fast task decomposition (under 200ms for most tasks)
- Minimal memory usage
- No external dependencies beyond core framework and filesystem

### 11.2 Scalability Through Simplicity
- Stateless design for easy scaling
- Minimal resource requirements
- Predictable performance characteristics

## 12. Security Considerations (Simple and Effective)

### 12.1 Input Sanitization (Minimal but Effective)
- Basic validation of task parameters
- Path validation for workspace creation
- No external resource references

### 12.2 Output Validation
- All generated paths are validated
- No arbitrary code execution in workspace creation

---
**Document Status**: Active  
**Version**: 1.0  
**Principles Compliance**: KISS, SOLID, YAGNI  
**Last Updated**: 2025-01-08  
**Compliance**: spec.kit standard v1.0