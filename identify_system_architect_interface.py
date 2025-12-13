"""
Test to identify correct System Architect skill interface
"""
import sys
import os
from pathlib import Path

# Add the skill path
skill_path = Path("D:/DAIP/dnaSpec/spec-kit/skills/dna-system-architect/scripts")
sys.path.insert(0, str(skill_path))

def identify_system_architect_interface():
    """Identify the correct interface for System Architect skill"""
    try:
        import system_architect_designer
        print("Available classes in system_architect_designer:")
        
        # Get all classes in the module
        for name in dir(system_architect_designer):
            if not name.startswith('_'):
                obj = getattr(system_architect_designer, name)
                if isinstance(obj, type):
                    print(f"  Class: {name}")
                    print(f"    Methods: {[method for method in dir(obj) if not method.startswith('_')]}")
        
        # Try to instantiate the actual class
        if hasattr(system_architect_designer, 'DNASPECSystemArchitect'):
            print(f"\nFound DNASPECSystemArchitect class - this is the real class name!")
            architect = system_architect_designer.DNASPECSystemArchitect()
            
            # Test the main method
            if hasattr(architect, 'generate_architecture_design'):
                print("  generate_architecture_design method exists")
                sample_reqs = "Design a simple web application"
                try:
                    result = architect.generate_architecture_design(sample_reqs)
                    print(f"  Method call successful, returned: {type(result)}")
                    print(f"  Result keys: {list(result.keys()) if isinstance(result, dict) else 'N/A'}")
                except Exception as e:
                    print(f"  Method call failed: {e}")
        
    except ImportError as e:
        print(f"Could not import system_architect_designer: {e}")

if __name__ == "__main__":
    identify_system_architect_interface()