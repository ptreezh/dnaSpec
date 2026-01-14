#!/usr/bin/env python3
"""
Verification test for Task Decomposer Skill adapter
"""
import sys
import os

# Add the adapter path to sys.path
sys.path.insert(0, 'spec-kit/skills/dna-task-decomposer/scripts')

try:
    from task_decomposer import TaskDecomposer
    
    print("Verifying Task Decomposer Skill Adapter...")
    
    # Test 1: Instantiation
    decomposer = TaskDecomposer()
    print("✅ TaskDecomposer instantiation successful")
    
    # Test 2: generate_task_breakdown method exists
    assert hasattr(decomposer, 'generate_task_breakdown'), "generate_task_breakdown method missing"
    print("✅ generate_task_breakdown method exists")
    
    # Test 3: Method returns expected structure
    result = decomposer.generate_task_breakdown("Build a simple e-commerce website")
    assert isinstance(result, dict), "Result should be a dictionary"
    assert "tasks" in result, "Result should contain 'tasks' key"
    assert "total_tasks" in result, "Result should contain 'total_tasks' key"
    assert "critical_path" in result, "Result should contain 'critical_path' key"
    print("✅ Method returns expected structure")
    
    # Test 4: Result structure validation
    assert isinstance(result["tasks"], list), "Tasks should be a list"
    assert isinstance(result["total_tasks"], int), "Total tasks should be an integer"
    assert isinstance(result["critical_path"], list), "Critical path should be a list"
    print("✅ Result structure validation passed")
    
    # Test 5: Task properties validation
    if result["tasks"]:
        first_task = result["tasks"][0]
        required_keys = ["id", "description", "type", "priority", "estimated_hours", "dependencies"]
        for key in required_keys:
            assert key in first_task, f"Task missing required key: {key}"
    print("✅ Task properties validation passed")
    
    print("\n🎉 Task Decomposer Skill Adapter verification successful!")
    print(f"Generated {result['total_tasks']} tasks")
    print(f"Critical path length: {len(result['critical_path'])}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()