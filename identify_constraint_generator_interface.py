"""
Test to identify correct Constraint Generator skill interface
"""
import sys
import os
from pathlib import Path

# Add the skill path
skill_path = Path("D:/DAIP/dnaSpec/spec-kit/skills/dna-constraint-generator/scripts")
sys.path.insert(0, str(skill_path))

def identify_constraint_generator_interface():
    """Identify the correct interface for Constraint Generator skill"""
    try:
        import constraint_generator
        print("Available classes in constraint_generator:")
        
        # Get all classes in the module
        for name in dir(constraint_generator):
            if not name.startswith('_'):
                obj = getattr(constraint_generator, name)
                if isinstance(obj, type):
                    print(f"  Class: {name}")
                    print(f"    Methods: {[method for method in dir(obj) if not method.startswith('_')]}")
        
        # Check for main constraint generator class
        classes = [name for name in dir(constraint_generator) if isinstance(getattr(constraint_generator, name), type) and not name.startswith('_')]
        print(f"\nFound classes: {classes}")
        
        for class_name in classes:
            if 'constraint' in class_name.lower() or 'generator' in class_name.lower():
                print(f"\nTrying {class_name}...")
                try:
                    cls = getattr(constraint_generator, class_name)
                    instance = cls()
                    print(f"  Successfully instantiated {class_name}")
                    
                    # Check for main method
                    methods = [method for method in dir(instance) if not method.startswith('_')]
                    print(f"  Available methods: {methods}")
                    
                    # Try to test the main functionality if available
                    if hasattr(instance, 'generate_constraints'):
                        print(f"  generate_constraints method exists")
                        sample_reqs = "System must handle 1000 concurrent users with 99.9% uptime"
                        try:
                            result = instance.generate_constraints(sample_reqs)
                            print(f"  Method call successful, returned: {type(result)}")
                            if isinstance(result, dict):
                                print(f"  Result keys: {list(result.keys())}")
                        except Exception as e:
                            print(f"  Method call failed: {e}")
                    elif hasattr(instance, 'generate'):
                        print(f"  generate method exists")
                        sample_reqs = "System must handle 1000 concurrent users"
                        try:
                            result = instance.generate(sample_reqs)
                            print(f"  Method call successful, returned: {type(result)}")
                        except Exception as e:
                            print(f"  Method call failed: {e}")
                            
                except Exception as e:
                    print(f"  Failed to instantiate {class_name}: {e}")
        
    except ImportError as e:
        print(f"Could not import constraint_generator: {e}")

if __name__ == "__main__":
    identify_constraint_generator_interface()