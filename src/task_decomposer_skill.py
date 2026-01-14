"""
Task Decomposer Skill Implementation
Following the TDD plan with KISS, SOLID, and YAGNI principles
"""
from typing import Dict, Any, List
from src.dna_spec_kit_integration.core.skill import DNASpecSkill, SkillResult, SkillStatus
import uuid
import time
from pathlib import Path


class TaskDecomposerSkill(DNASpecSkill):
    """
    Task Decomposer Skill - Decomposes complex tasks into atomic tasks with isolated workspaces
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
            "timestamp": time.time()
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
        if " and " in task.lower():
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