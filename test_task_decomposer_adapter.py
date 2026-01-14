#!/usr/bin/env python3
"""
Test script for Task Decomposer Skill adapter
"""
import sys
import os

# Add the adapter path to sys.path
sys.path.insert(0, 'spec-kit/skills/dna-task-decomposer/scripts')

try:
    from task_decomposer import TaskDecomposer
    
    print("Testing Task Decomposer Skill Adapter...")
    
    # Test instantiation
    decomposer = TaskDecomposer()
    print("✅ TaskDecomposer instantiation successful")
    
    # Test main method
    breakdown = decomposer.generate_task_breakdown("Build a simple e-commerce website")
    print(f"✅ generate_task_breakdown:")
    print(f"   Total Tasks: {breakdown.get('total_tasks')}")
    print(f"   Critical Path Length: {len(breakdown.get('critical_path', []))}")
    print(f"   First Task: {breakdown.get('tasks', [{}])[0].get('description', 'None')}")
    
    # Test resource recommendations
    resources = breakdown.get('resource_recommendations', {})
    print(f"   Resource Recommendations: {len(resources)} categories")
    
    print("\n🎉 Task Decomposer Skill Adapter working correctly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()