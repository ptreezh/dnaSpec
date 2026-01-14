"""
Test to identify correct Modulizer skill interface
"""
import sys
import os
from pathlib import Path

# Add the skill path
skill_path = Path("D:/DAIP/dnaSpec/spec-kit/skills/dna-modulizer/scripts")
sys.path.insert(0, str(skill_path))

def identify_modulizer_interface():
    """Identify the correct interface for Modulizer skill"""
    try:
        import modulizer
        print("Available classes in modulizer:")
        
        # Get all classes in the module
        for name in dir(modulizer):
            if not name.startswith('_'):
                obj = getattr(modulizer, name)
                if isinstance(obj, type):
                    print(f"  Class: {name}")
                    print(f"    Methods: {[method for method in dir(obj) if not method.startswith('_')]}")
        
        # Check what classes exist
        classes = [name for name in dir(modulizer) if isinstance(getattr(modulizer, name), type) and not name.startswith('_')]
        print(f"\nFound classes: {classes}")
        
        # Check all possible class names that might be used
        for class_name in classes:
            if 'modulizer' in class_name.lower() or 'module' in class_name.lower() or 'designer' in class_name.lower():
                print(f"Trying {class_name}...")
                try:
                    cls = getattr(modulizer, class_name)
                    instance = cls()
                    print(f"  Successfully instantiated {class_name}")
                    
                    # Check for main method
                    methods = [method for method in dir(instance) if not method.startswith('_')]
                    print(f"  Available methods: {methods}")
                    
                    # Try to test the main functionality if available
                    if hasattr(instance, 'create_modular_design'):
                        print(f"  create_modular_design method exists")
                        sample_reqs = "Monolithic application to be modularized"
                        try:
                            result = instance.create_modular_design(sample_reqs)
                            print(f"  Method call successful, returned: {type(result)}")
                            if isinstance(result, dict):
                                print(f"  Result keys: {list(result.keys())}")
                        except Exception as e:
                            print(f"  Method call failed: {e}")
                    elif hasattr(instance, 'modulize'):
                        print(f"  modulize method exists")
                        sample_reqs = "Monolithic application to be modularized"
                        try:
                            result = instance.modulize(sample_reqs)
                            print(f"  Method call successful, returned: {type(result)}")
                        except Exception as e:
                            print(f"  Method call failed: {e}")
                    elif hasattr(instance, 'design_modular_architecture'):
                        print(f"  design_modular_architecture method exists")
                        sample_reqs = "Monolithic application to be modularized"
                        try:
                            result = instance.design_modular_architecture(sample_reqs)
                            print(f"  Method call successful, returned: {type(result)}")
                        except Exception as e:
                            print(f"  Method call failed: {e}")
                            
                except Exception as e:
                    print(f"  Failed to instantiate {class_name}: {e}")
        
    except ImportError as e:
        print(f"Could not import modulizer: {e}")

if __name__ == "__main__":
    identify_modulizer_interface()