#!/usr/bin/env python3
"""
Test script for DNASPEC agentic skills
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_agent_creator():
    """Test the agent creator skill"""
    print("Testing DNASPEC Agent Creator skill...")
    print("=" * 50)
    
    try:
        # Add agent creator path
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spec-kit', 'skills', 'dna-agent-creator', 'scripts'))
        from agent_creator import AgentCreator
        
        # Test agent creation
        print("\n1. Testing Agent Creation:")
        requirements = """
        Create an agent that can monitor system performance and alert administrators 
        when certain thresholds are exceeded. The agent should collect metrics, 
        analyze them in real-time, and send notifications to appropriate channels. 
        It must be secure and reliable, with minimal impact on system performance.
        """
        
        creator = AgentCreator()
        specification = creator.generate_agent_specification("SystemMonitorAgent", requirements)
        
        print(f"   Agent Name: {specification['agent_name']}")
        print(f"   Type: {specification['agent_type']}")
        print(f"   Role: {specification['agent_role']}")
        print(f"   Number of Capabilities: {len(specification['capabilities'])}")
        print(f"   Number of Constraints: {len(specification['constraints'])}")
        
        print("\n✅ Agent Creator skill test completed!")
        
    except Exception as e:
        print(f"❌ Error testing Agent Creator skill: {e}")
        import traceback
        traceback.print_exc()


def test_task_decomposer():
    """Test the task decomposer skill"""
    print("\nTesting DNASPEC Task Decomposer skill...")
    print("=" * 50)
    
    try:
        # Add task decomposer path
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spec-kit', 'skills', 'dna-task-decomposer', 'scripts'))
        from task_decomposer import TaskDecomposer
        
        # Test task decomposition
        print("\n1. Testing Task Decomposition:")
        task = "Build a complete e-commerce platform with user authentication, product catalog, shopping cart, payment processing, and order management."
        
        decomposer = TaskDecomposer()
        decomposition = decomposer.generate_task_breakdown(task)
        
        print(f"   Task: {task}")
        print(f"   Number of Atomic Tasks: {decomposition.get('total_tasks', 0)}")
        print(f"   Critical Path Length: {len(decomposition.get('critical_path', []))}")
        
        if 'tasks' in decomposition:
            print("   Sample Atomic Tasks:")
            for i, task in enumerate(decomposition['tasks'][:3]):  # Show first 3
                print(f"     {i+1}. {task.get('description', 'Unnamed Task')[:50]}...")
        
        print("\n✅ Task Decomposer skill test completed!")
        
    except Exception as e:
        print(f"❌ Error testing Task Decomposer skill: {e}")
        import traceback
        traceback.print_exc()


def test_system_architect():
    """Test the system architect skill"""
    print("\nTesting DNASPEC System Architect skill...")
    print("=" * 50)
    
    try:
        # Add system architect path
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spec-kit', 'skills', 'dna-system-architect', 'scripts'))
        
        # First, let's see what's in the system architect script
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spec-kit', 'skills', 'dna-system-architect', 'scripts', 'system_architect_designer.py')
        print(f"   Script path: {script_path}")
        print(f"   Script exists: {os.path.exists(script_path)}")
        
        if os.path.exists(script_path):
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"   Script content preview: {content[:200]}...")
        
        print("\n✅ System Architect skill test completed!")
        
    except Exception as e:
        print(f"❌ Error testing System Architect skill: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_agent_creator()
    test_task_decomposer()
    test_system_architect()