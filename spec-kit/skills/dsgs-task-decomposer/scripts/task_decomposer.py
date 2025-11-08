"""
DSGS Task Decomposer Script
Implements the core functionality for breaking down complex requirements into atomic tasks
"""

import re
from typing import Dict, Any, List, Tuple
from enum import Enum


class TaskPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskType(Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    INFRASTRUCTURE = "infrastructure"
    ANALYSIS = "analysis"


class Task:
    def __init__(self, id: str, description: str, task_type: TaskType, 
                 priority: TaskPriority, dependencies: List[str] = None, 
                 estimated_hours: int = 1):
        self.id = id
        self.description = description
        self.type = task_type
        self.priority = priority
        self.dependencies = dependencies or []
        self.estimated_hours = estimated_hours
        self.subtasks = []
    
    def add_subtask(self, subtask: 'Task'):
        self.subtasks.append(subtask)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "description": self.description,
            "type": self.type.value,
            "priority": self.priority.value,
            "dependencies": self.dependencies,
            "estimated_hours": self.estimated_hours,
            "subtasks": [subtask.to_dict() for subtask in self.subtasks]
        }


class TaskDecomposer:
    def __init__(self):
        self.known_patterns = {
            # Development patterns
            r'implement|create|build|develop|design': TaskType.DEVELOPMENT,
            r'test|verify|validate|check|review': TaskType.TESTING,
            r'document|write|specify|describe|outline': TaskType.DOCUMENTATION,
            r'setup|configure|deploy|install|environment': TaskType.INFRASTRUCTURE,
            r'analyze|research|study|investigate|explore': TaskType.ANALYSIS
        }
    
    def identify_dependencies(self, tasks: List[Task]) -> Dict[str, List[str]]:
        """
        Identify dependencies between tasks
        """
        dependencies = {}
        task_map = {task.id: task for task in tasks}
        
        # Simple dependency analysis - in reality this would be more sophisticated
        for task in tasks:
            deps = []
            # Check if the task description references other tasks
            for other_task in tasks:
                if other_task.id != task.id:
                    # Simple heuristic: if the task description contains the other task's name or concept
                    if other_task.id.lower() in task.description.lower():
                        deps.append(other_task.id)
            dependencies[task.id] = deps
        
        return dependencies
    
    def estimate_complexity(self, description: str) -> Tuple[TaskPriority, int]:
        """
        Estimate the priority and time based on description
        """
        description_lower = description.lower()
        
        # Priority indicators
        critical_indicators = ['critical', 'must', 'required', 'essential', 'vital', 'security', 'safety']
        high_indicators = ['important', 'needed', 'significant', 'major', 'primary', 'core']
        low_indicators = ['optional', 'nice to have', 'improvement', 'enhancement']
        
        # Time estimation based on keywords
        time_indicators = {
            'simple': 2,
            'basic': 4,
            'moderate': 8,
            'complex': 16,
            'challenging': 20,
            'difficult': 24,
            'extensive': 40
        }
        
        # Determine priority
        priority = TaskPriority.MEDIUM
        for indicator in critical_indicators:
            if indicator in description_lower:
                priority = TaskPriority.CRITICAL
                break
        else:
            for indicator in high_indicators:
                if indicator in description_lower:
                    priority = TaskPriority.HIGH
                    break
            else:
                for indicator in low_indicators:
                    if indicator in description_lower:
                        priority = TaskPriority.LOW
                        break
        
        # Estimate time
        estimated_hours = 4  # default
        for indicator, hours in time_indicators.items():
            if indicator in description_lower:
                estimated_hours = hours
                break
        
        return priority, estimated_hours
    
    def identify_task_type(self, description: str) -> TaskType:
        """
        Identify the type of task based on keywords in description
        """
        description_lower = description.lower()
        
        for pattern, task_type in self.known_patterns.items():
            if re.search(pattern, description_lower):
                return task_type
        
        # Default to development if no pattern matches
        return TaskType.DEVELOPMENT
    
    def decompose_requirements(self, requirements: str) -> List[Task]:
        """
        Decompose complex requirements into atomic tasks
        """
        tasks = []
        
        # Extract potential tasks from the requirements using common task patterns
        potential_tasks = self._extract_potential_tasks(requirements)
        
        # Create tasks from identified potential tasks
        for i, task_desc in enumerate(potential_tasks):
            task_id = f"T{i+1:03d}"
            task_type = self.identify_task_type(task_desc)
            priority, hours = self.estimate_complexity(task_desc)
            
            task = Task(
                id=task_id,
                description=task_desc,
                task_type=task_type,
                priority=priority,
                estimated_hours=hours
            )
            
            tasks.append(task)
        
        # Identify dependencies after all tasks are created
        dependencies = self.identify_dependencies(tasks)
        for task in tasks:
            task.dependencies = dependencies.get(task.id, [])
        
        return tasks
    
    def _extract_potential_tasks(self, requirements: str) -> List[str]:
        """
        Extract potential tasks from requirements text
        This is a simplified version - a real implementation would be more sophisticated
        """
        # Look for common task-indicating phrases
        task_indicators = [
            r'should', r'need to', r'have to', r'must', r'require', 
            r'implement', r'develop', r'create', r'design', r'build',
            r'analyze', r'research', r'study', r'investigate',
            r'test', r'validate', r'verify', r'check',
            r'document', r'write', r'specify', r'outline'
        ]
        
        # Split requirements into sentences
        sentences = re.split(r'[.!?]+', requirements)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Identify sentences that likely represent tasks
        potential_tasks = []
        for sentence in sentences:
            for indicator in task_indicators:
                if re.search(r'\b' + indicator + r'\b', sentence, re.IGNORECASE):
                    potential_tasks.append(sentence.strip())
                    break
        
        # If no task-indicating sentences found, try to extract by other means
        if not potential_tasks:
            # Just return sentences that seem like they might be tasks
            for sentence in sentences:
                if len(sentence) > 20:  # Skip very short sentences
                    potential_tasks.append(sentence.strip())
        
        # Limit to 20 potential tasks to prevent overwhelming
        return potential_tasks[:20]
    
    def generate_task_breakdown(self, requirements: str) -> Dict[str, Any]:
        """
        Generate a complete task breakdown from requirements
        """
        # Decompose requirements into tasks
        tasks = self.decompose_requirements(requirements)
        
        # Create dependency graph
        dependency_graph = self._create_dependency_graph(tasks)
        
        # Identify critical path
        critical_path = self._identify_critical_path(tasks, dependency_graph)
        
        # Create the breakdown report
        breakdown = {
            "requirements_analyzed": requirements[:100] + "..." if len(requirements) > 100 else requirements,
            "total_tasks": len(tasks),
            "tasks": [task.to_dict() for task in tasks],
            "dependency_graph": dependency_graph,
            "critical_path": critical_path,
            "resource_recommendations": self._generate_resource_recommendations(tasks),
            "execution_sequence": self._generate_execution_sequence(tasks, dependency_graph)
        }
        
        return breakdown
    
    def _create_dependency_graph(self, tasks: List[Task]) -> Dict[str, List[str]]:
        """
        Create a dependency graph showing task relationships
        """
        graph = {}
        task_map = {task.id: task for task in tasks}
        
        for task in tasks:
            graph[task.id] = task.dependencies
        
        return graph
    
    def _identify_critical_path(self, tasks: List[Task], dependency_graph: Dict[str, List[str]]) -> List[str]:
        """
        Identify the critical path through the task graph
        This is a simplified approach - real implementation would be more sophisticated
        """
        # For now, return the longest sequence found through a simple traversal
        visited = set()
        path = []
        
        def dfs(task_id, current_path):
            if task_id in visited:
                return current_path
            
            visited.add(task_id)
            current_path.append(task_id)
            
            # Continue to dependent tasks
            dependents = [t.id for t in tasks if task_id in t.dependencies]
            longest_path = current_path[:]
            
            for dep in dependents:
                new_path = dfs(dep, current_path[:])
                if len(new_path) > len(longest_path):
                    longest_path = new_path
            
            return longest_path
        
        for task in tasks:
            if not task.dependencies:  # Start with tasks that have no dependencies
                candidate_path = dfs(task.id, [])
                if len(candidate_path) > len(path):
                    path = candidate_path
        
        return path
    
    def _generate_resource_recommendations(self, tasks: List[Task]) -> Dict[str, int]:
        """
        Generate resource recommendations based on task types
        """
        recommendations = {}
        
        for task in tasks:
            task_type = task.type.value
            if task_type not in recommendations:
                recommendations[task_type] = 0
            recommendations[task_type] += task.estimated_hours
        
        return recommendations
    
    def _generate_execution_sequence(self, tasks: List[Task], dependency_graph: Dict[str, List[str]]) -> List[str]:
        """
        Generate an execution sequence respecting dependencies
        """
        # Topological sort implementation
        in_degree = {task.id: 0 for task in tasks}
        
        for task_id, deps in dependency_graph.items():
            for dep in deps:
                in_degree[task_id] += 1
        
        queue = [task_id for task_id, degree in in_degree.items() if degree == 0]
        sequence = []
        
        while queue:
            current = queue.pop(0)
            sequence.append(current)
            
            # Find tasks that depend on current task
            for task_id, deps in dependency_graph.items():
                if current in deps:
                    in_degree[task_id] -= 1
                    if in_degree[task_id] == 0:
                        queue.append(task_id)
        
        return sequence


def main():
    """
    Example usage of the TaskDecomposer
    """
    requirements = """
    The system should allow users to register and login securely. 
    It must store user information in a database. 
    The application needs to provide a dashboard for users to view their information.
    There should be an admin panel to manage users.
    The system must be responsive and work on mobile devices.
    Security is critical - all passwords must be encrypted.
    We need to implement proper error handling and logging.
    The system should be documented with API specifications.
    """
    
    decomposer = TaskDecomposer()
    breakdown = decomposer.generate_task_breakdown(requirements)
    
    print("## Task Breakdown Report")
    print(f"Total Tasks: {breakdown['total_tasks']}")
    print(f"Critical Path: {' -> '.join(breakdown['critical_path'])}")
    print("\n### Tasks:")
    
    for task in breakdown['tasks']:
        print(f"- {task['id']}: {task['description']}")
        print(f"  Type: {task['type']}, Priority: {task['priority']}, Hours: {task['estimated_hours']}")
        if task['dependencies']:
            print(f"  Dependencies: {', '.join(task['dependencies'])}")
        print()


if __name__ == "__main__":
    main()