#!/usr/bin/env python3
"""
Debug script to identify the actual skill mappings in the DNASPEC system
"""
import os
import sys
import subprocess
import importlib


def debug_skills():
    """Debug the actual skill system"""
    print("🔍 DEBUGGING DNASPEC SKILL SYSTEM")
    print("="*60)
    
    # Import and check the skill executor
    try:
        print("\n1. Checking skill executor implementation...")
        sys.path.insert(0, 'src')
        from dna_spec_kit_integration.core.skill_executor import SkillExecutor
        executor = SkillExecutor()
        print(f"   ✅ SkillExecutor imported and instantiated: {type(executor)}")
        
        # Check what methods/attributes are available
        print(f"   Available methods: {[attr for attr in dir(executor) if not attr.startswith('_')]}")
        
    except Exception as e:
        print(f"   ❌ Error with SkillExecutor: {e}")
        import traceback
        traceback.print_exc()
    
    # Check the PythonBridge and SkillMapper
    try:
        print("\n2. Checking skill mapper...")
        from dna_spec_kit_integration.core.python_bridge import PythonBridge
        from dna_spec_kit_integration.core.skill_mapper import SkillMapper
        
        bridge = PythonBridge()
        mapper = SkillMapper()
        
        print(f"   ✅ PythonBridge: {type(bridge)}")
        print(f"   ✅ SkillMapper: {type(mapper)}")
        
        # Check what skills are mapped
        if hasattr(mapper, 'get_skill_function'):
            print("   SkillMapper has get_skill_function method")
        if hasattr(mapper, 'skill_map'):
            print(f"   SkillMapper skill_map: {type(getattr(mapper, 'skill_map', {}))}")
            print(f"   SkillMapper skill_map keys: {list(getattr(mapper, 'skill_map', {}).keys())}")
        
    except Exception as e:
        print(f"   ❌ Error with mappers: {e}")
        import traceback
        traceback.print_exc()
    
    # Try to call the handler with a simple command
    try:
        print("\n3. Testing command handler directly...")
        from dna_spec_kit_integration.core.command_handler import CommandHandler
        handler = CommandHandler()
        print(f"   ✅ CommandHandler: {type(handler)}")
        
        # Test a simple command
        result = handler.handle_command("/speckit.dnaspec.list")  # Try a potential command
        print(f"   Command result for /speckit.dnaspec.list: {result}")
        
    except Exception as e:
        print(f"   ❌ Error with CommandHandler: {e}")
        import traceback
        traceback.print_exc()
    
    # Check if there are actual skill files that might be called
    try:
        print("\n4. Checking available skill implementations...")
        # Look for skill implementations
        import os
        skill_dir = "src/dna_context_engineering"
        if os.path.exists(skill_dir):
            skill_files = [f for f in os.listdir(skill_dir) if f.endswith('.py')]
            print(f"   Skill files in {skill_dir}: {skill_files}")
        
        # Check for specific skill files
        core_skill_path = "src/dna_context_engineering/core_skill.py"
        if os.path.exists(core_skill_path):
            print("   ✅ core_skill.py exists")
            # Try to import and check skills
            from dna_context_engineering.core_skill import SkillsManager
            from dna_context_engineering.ai_client import GenericAPIClient
            from dna_context_engineering.instruction_template import TemplateRegistry
            
            client = GenericAPIClient()
            registry = TemplateRegistry()
            manager = SkillsManager(client, registry)
            
            available_skills = manager.list_skills()
            print(f"   Available skills in SkillsManager: {list(available_skills.keys())}")
        
    except Exception as e:
        print(f"   ❌ Error checking skill implementations: {e}")
        import traceback
        traceback.print_exc()

    # Check CLI extension handler again with better error handling
    try:
        print("\n5. Checking CLI extension handler...")
        from dna_spec_kit_integration.cli_extension_handler import get_available_skills
        skills_data = get_available_skills()
        print(f"   CLI Extension Handler skills data type: {type(skills_data)}")
        print(f"   CLI Extension Handler keys: {list(skills_data.keys()) if isinstance(skills_data, dict) else 'Not a dict'}")
        if isinstance(skills_data, dict) and 'skills' in skills_data:
            print(f"   Number of skills: {len(skills_data['skills'])}")
            for i, skill in enumerate(skills_data['skills'][:5]):  # Show first 5
                print(f"     {i+1}. Name: {skill.get('name', 'N/A')}, Command: {skill.get('command', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Error with CLI extension handler: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    debug_skills()