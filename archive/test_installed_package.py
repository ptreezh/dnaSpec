"""
Test installed package functionality
"""
from dsgs_spec_kit_integration.core.manager import SkillManager
from dsgs_spec_kit_integration.skills.examples import ArchitectSkill

def test_installed_package():
    print("Testing installed package...")
    
    # Create skill manager
    manager = SkillManager()
    print("✓ SkillManager created")
    
    # Create skill
    skill = ArchitectSkill()
    print("✓ ArchitectSkill created")
    
    # Register skill
    result = manager.register_skill(skill)
    if result:
        print("✓ Skill registered successfully")
    else:
        print("✗ Skill registration failed")
        return False
    
    # Execute skill
    skill_result = manager.execute_skill("dsgs-architect", "test system")
    if skill_result.status.name == "COMPLETED":
        print("✓ Skill executed successfully")
        print(f"  Result: {skill_result.result}")
    else:
        print("✗ Skill execution failed")
        return False
    
    print("✓ All tests passed! Package is working correctly.")
    return True

if __name__ == "__main__":
    success = test_installed_package()
    if success:
        print("\n🎉 Package verification successful!")
    else:
        print("\n❌ Package verification failed!")
        exit(1)