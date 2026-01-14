"""
Test to identify correct Task Decomposer skill interface
"""
import sys
import os
from pathlib import Path

# Add the skill path
skill_path = Path("D:/DAIP/dnaSpec/spec-kit/skills/dna-task-decomposer/scripts")
sys.path.insert(0, str(skill_path))

def identify_task_decomposer_interface():
    """Identify the correct interface for Task Decomposer skill"""
    try:
        import task_decomposer
        print("Available classes in task_decomposer:")
        
        # Get all classes in the module
        for name in dir(task_decomposer):
            if not name.startswith('_'):
                obj = getattr(task_decomposer, name)
                if isinstance(obj, type):
                    print(f"  Class: {name}")
                    print(f"    Methods: {[method for method in dir(obj) if not method.startswith('_')]}")
        
        # Check if there's a TaskDecomposer class
        if hasattr(task_decomposer, 'TaskDecomposer'):
            print(f"\nFound TaskDecomposer class!")
            decomposer = task_decomposer.TaskDecomposer()
            print("  Successfully instantiated TaskDecomposer")
            
            # Check for main method (likely to be generate_task_breakdown or similar)
            methods = [method for method in dir(decomposer) if not method.startswith('_')]
            print(f"  Available methods: {methods}")
            
            # Try to test the main functionality if available
            if hasattr(decomposer, 'generate_task_breakdown'):
                print("  generate_task_breakdown method exists")
                sample_reqs = "Develop a simple web application"
                try:
                    result = decomposer.generate_task_breakdown(sample_reqs)
                    print(f"  Method call successful, returned: {type(result)}")
                    print(f"  Result keys: {list(result.keys()) if isinstance(result, dict) else 'N/A'}")
                except Exception as e:
                    print(f"  Method call failed: {e}")
            elif hasattr(decomposer, 'decompose'):
                print("  decompose method exists")
                sample_reqs = "Develop a simple web application"
                try:
                    result = decomposer.decompose(sample_reqs)
                    print(f"  Method call successful, returned: {type(result)}")
                except Exception as e:
                    print(f"  Method call failed: {e}")
        
    except ImportError as e:
        print(f"Could not import task_decomposer: {e}")

if __name__ == "__main__":
    identify_task_decomposer_interface()