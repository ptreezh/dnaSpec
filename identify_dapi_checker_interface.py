"""
Test to identify correct DAPI Checker skill interface
"""
import sys
import os
from pathlib import Path

# Add the skill path
skill_path = Path("D:/DAIP/dnaSpec/spec-kit/skills/dna-dapi-checker/scripts")
sys.path.insert(0, str(skill_path))

def identify_dapi_checker_interface():
    """Identify the correct interface for DAPI Checker skill"""
    try:
        import dapi_checker
        print("Available classes in dapi_checker:")
        
        # Get all classes in the module
        for name in dir(dapi_checker):
            if not name.startswith('_'):
                obj = getattr(dapi_checker, name)
                if isinstance(obj, type):
                    print(f"  Class: {name}")
                    print(f"    Methods: {[method for method in dir(obj) if not method.startswith('_')]}")
        
        # Check for main DAPI checker class
        classes = [name for name in dir(dapi_checker) if isinstance(getattr(dapi_checker, name), type) and not name.startswith('_')]
        print(f"\nFound classes: {classes}")
        
        for class_name in classes:
            if 'checker' in class_name.lower() or 'dapi' in class_name.lower() or 'api' in class_name.lower():
                print(f"\nTrying {class_name}...")
                try:
                    cls = getattr(dapi_checker, class_name)
                    instance = cls()
                    print(f"  Successfully instantiated {class_name}")
                    
                    # Check for main method
                    methods = [method for method in dir(instance) if not method.startswith('_')]
                    print(f"  Available methods: {methods}")
                    
                    # Try to test the main functionality if available
                    if hasattr(instance, 'analyze_api_specification'):
                        print(f"  analyze_api_specification method exists")
                        sample_spec = """
                        GET /users
                        Description: Retrieve list of users
                        Response: 200 OK with JSON array of users
                        """
                        try:
                            result = instance.analyze_api_specification(sample_spec)
                            print(f"  Method call successful, returned: {type(result)}")
                            if isinstance(result, dict):
                                print(f"  Result keys: {list(result.keys())}")
                        except Exception as e:
                            print(f"  Method call failed: {e}")
                    elif hasattr(instance, 'check_api'):
                        print(f"  check_api method exists")
                        sample_spec = "GET /users"
                        try:
                            result = instance.check_api(sample_spec)
                            print(f"  Method call successful, returned: {type(result)}")
                        except Exception as e:
                            print(f"  Method call failed: {e}")
                            
                except Exception as e:
                    print(f"  Failed to instantiate {class_name}: {e}")
        
    except ImportError as e:
        print(f"Could not import dapi_checker: {e}")

if __name__ == "__main__":
    identify_dapi_checker_interface()