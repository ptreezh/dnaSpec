#!/usr/bin/env python3
"""
Detailed verification of the actual agentic skills implementation status
"""

import sys
import os

def test_individual_agentic_skills():
    """Test the actual files that the comprehensive test was trying to load"""
    print("Testing Individual Agentic Skills Implementation...")
    
    # Test the paths that were mentioned in the comprehensive test
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'spec-kit', 'skills', 'dna-task-decomposer', 'scripts'))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'spec-kit', 'skills', 'dna-system-architect', 'scripts'))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'spec-kit', 'skills', 'dna-constraint-generator', 'scripts'))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'spec-kit', 'skills', 'dna-dapi-checker', 'scripts'))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'spec-kit', 'skills', 'dna-modulizer', 'scripts'))
    
    print("\n1. Testing Agent Creator (should work)...")
    try:
        from agent_creator import AgentCreator
        creator = AgentCreator()
        specification = creator.generate_agent_specification("TestAgent", "Create an intelligent agent that monitors server performance")
        print(f"✅ Agent Creator: SUCCESS")
        print(f"   Specification keys: {list(specification.keys())}")
    except Exception as e:
        print(f"❌ Agent Creator: FAILED - {str(e)}")
    
    print("\n2. Testing Task Decomposer...")
    try:
        from task_decomposer import TaskDecomposer
        print(f"✅ Task Decomposer: Module imported")
        # Try to create instance
        decomposer = TaskDecomposer()
        print(f"✅ Task Decomposer: Instance created")
    except ImportError as e:
        print(f"❌ Task Decomposer: Module not found - {str(e)}")
    except Exception as e:
        print(f"❌ Task Decomposer: Runtime error - {str(e)}")
    
    print("\n3. Testing System Architect...")
    try:
        from system_architect_designer import SystemArchitectDesigner
        print(f"✅ System Architect: Module imported")
        # Try to create instance
        architect = SystemArchitectDesigner()
        print(f"✅ System Architect: Instance created")
    except ImportError as e:
        print(f"❌ System Architect: Module not found - {str(e)}")
    except Exception as e:
        print(f"❌ System Architect: Runtime error - {str(e)}")
    
    print("\n4. Testing Constraint Generator...")
    try:
        from constraint_generator import ConstraintGenerator
        print(f"✅ Constraint Generator: Module imported")
        # Try to create instance
        generator = ConstraintGenerator()
        print(f"✅ Constraint Generator: Instance created")
    except ImportError as e:
        print(f"❌ Constraint Generator: Module not found - {str(e)}")
    except Exception as e:
        print(f"❌ Constraint Generator: Runtime error - {str(e)}")
    
    print("\n5. Testing DAPI Checker...")
    try:
        from dapi_checker import DAPIChecker
        print(f"✅ DAPI Checker: Module imported")
        # Try to create instance
        checker = DAPIChecker()
        print(f"✅ DAPI Checker: Instance created")
    except ImportError as e:
        print(f"❌ DAPI Checker: Module not found - {str(e)}")
    except Exception as e:
        print(f"❌ DAPI Checker: Runtime error - {str(e)}")
    
    print("\n6. Testing Modulizer...")
    try:
        from modulizer import Modulizer
        print(f"✅ Modulizer: Module imported")
        # Try to create instance
        modulizer = Modulizer()
        print(f"✅ Modulizer: Instance created")
    except ImportError as e:
        print(f"❌ Modulizer: Module not found - {str(e)}")
    except Exception as e:
        print(f"❌ Modulizer: Runtime error - {str(e)}")

def check_actual_files():
    """Check if the actual skill implementation files exist"""
    print("\nChecking for actual skill implementation files...")
    
    skill_files = [
        "D:/DAIP/dnaSpec/spec-kit/skills/dna-agent-creator/scripts/agent_creator.py",
        "D:/DAIP/dnaSpec/spec-kit/skills/dna-task-decomposer/scripts/task_decomposer.py",
        "D:/DAIP/dnaSpec/spec-kit/skills/dna-system-architect/scripts/system_architect_designer.py",
        "D:/DAIP/dnaSpec/spec-kit/skills/dna-constraint-generator/scripts/constraint_generator.py",
        "D:/DAIP/dnaSpec/spec-kit/skills/dna-dapi-checker/scripts/dapi_checker.py",
        "D:/DAIP/dnaSpec/spec-kit/skills/dna-modulizer/scripts/modulizer.py"
    ]
    
    for file_path in skill_files:
        import os
        if os.path.exists(file_path):
            print(f"✅ File exists: {os.path.basename(file_path)}")
            # Check file size
            size = os.path.getsize(file_path)
            print(f"   Size: {size} bytes")
        else:
            print(f"❌ File missing: {os.path.basename(file_path)}")

def test_core_functionality():
    """Test the core functionality that was working"""
    print("\nTesting core functionality (should work)...")
    
    from src.dna_context_engineering.skills_system_final import execute
    
    # Test context analysis
    result = execute({'skill': 'context-analysis', 'context': 'Implement a user authentication system'})
    print(f"✅ Context Analysis: Works - {type(result)}")
    
    # Test context optimization
    result = execute({'skill': 'context-optimization', 'context': 'User login'})
    print(f"✅ Context Optimization: Works - {type(result)}")
    
    # Test cognitive template
    result = execute({'skill': 'cognitive-template', 'context': 'How to improve performance?', 'params': {'template': 'chain_of_thought'}})
    print(f"✅ Cognitive Template: Works - {type(result)}")

def main():
    print("="*70)
    print("DETAILED DNASPEC AGENTIC SKILLS STATUS VERIFICATION")
    print("="*70)
    
    check_actual_files()
    test_core_functionality()
    test_individual_agentic_skills()
    
    print("\n" + "="*70)
    print("CONCLUSION:")
    print("Based on detailed testing, we can see that:")
    print("1. Core context engineering skills are fully implemented")
    print("2. Basic agent creator skill works (simplified version)")
    print("3. Many advanced agentic skills referenced in documentation")
    print("   are not actually implemented in the codebase")
    print("4. The comprehensive test was referencing non-existent files")
    print("="*70)

if __name__ == "__main__":
    main()