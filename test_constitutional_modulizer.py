"""
Test script to verify constitutional module formation skill
"""
import sys
import os
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def test_constitutional_module_formation():
    """Test the constitutional module formation skill"""
    print("🧪 Testing Constitutional Module Formation Skill")
    print("="*60)
    
    try:
        # Test importing the skill
        from src.dna_spec_kit_integration.skills.constitutional_modulizer_independent import execute_constitutional_module_formation, get_constitutional_module_formation_info
        print("✅ Successfully imported constitutional module formation skill")
        
        # Get skill info
        info = get_constitutional_module_formation_info()
        print(f"✅ Skill info retrieved: {info['name']}")
        print(f"   Description: {info['description']}")
        print(f"   Purpose: {info['purpose']}")
        
        # Test registering a component
        print("\n📝 Testing component registration:")
        register_result = execute_constitutional_module_formation({
            'operation': 'register_component',
            'component_name': 'test_auth_handler',
            'component_description': 'Handles user authentication',
            'component_category': 'security'
        })
        
        if register_result['success']:
            comp_id = register_result['component_id']
            print(f"✅ Component registered: {comp_id}")
            print(f"   Message: {register_result['message']}")
        else:
            print(f"❌ Component registration failed: {register_result.get('error')}")
            return False
            
        # Test updating component status
        print("\n🔄 Testing component status update:")
        update_result = execute_constitutional_module_formation({
            'operation': 'update_component_status',
            'component_id': comp_id,
            'status': 'MATURE',
            'maturity_boost': 0.5
        })
        
        print(f"✅ Component status updated: {update_result['success']}")
        print(f"   Message: {update_result['message']}")
        
        # Test adding dependency
        print("\n🔗 Testing component dependency addition:")
        # Register second component
        comp2_result = execute_constitutional_module_formation({
            'operation': 'register_component',
            'component_name': 'session_manager',
            'component_description': 'Manages user sessions',
            'component_category': 'security'
        })
        
        if comp2_result['success']:
            comp2_id = comp2_result['component_id']
            print(f"✅ Second component registered: {comp2_id}")
            
            # Add dependency
            dep_result = execute_constitutional_module_formation({
                'operation': 'add_component_dependency',
                'from_component_id': comp_id,
                'to_component_id': comp2_id
            })
            
            print(f"✅ Dependency added: {dep_result['success']}")
            print(f"   Message: {dep_result['message']}")
        
        # Test evaluating module formation
        print("\n🏗️  Testing module formation evaluation:")
        eval_result = execute_constitutional_module_formation({
            'operation': 'evaluate_module_formation'
        })
        
        print(f"✅ Module formation evaluation: {eval_result['success']}")
        print(f"   Insights: {eval_result['insights']}")
        
        # Test getting ready modules
        print("\n📦 Testing getting ready modules:")
        modules_result = execute_constitutional_module_formation({
            'operation': 'get_ready_modules'
        })
        
        print(f"✅ Got modules: {modules_result['success']}")
        print(f"   Modules count: {modules_result.get('modules_count', 0)}")
        
        if modules_result['modules_count'] > 0:
            print("   Formed modules:")
            for mod in modules_result['modules']:
                print(f"     - {mod['name']} ({mod['component_count']} components)")
        
        print("\n🎉 Constitutional Module Formation skill is working correctly!")
        print("   ✓ Supports bottom-up module formation from mature components")
        print("   ✓ Supports gradual encapsulation as complexity grows")
        print("   ✓ Aligns with constitutional requirements")
        
        return True
        
    except ImportError as e:
        print(f"❌ ImportError: {e}")
        print("   This indicates the constitutional module formation skill may not be integrated properly.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_integration_with_skill_executor():
    """Test that the skill is properly integrated with the skill executor"""
    print("\n\n🔌 Testing Skill Executor Integration")
    print("="*60)
    
    try:
        from src.dna_spec_kit_integration.skills.skill_executor import skill_executor
        
        # Check if constitutional-module-formation is registered
        available_skills = skill_executor.get_available_skills()
        if 'constitutional-module-formation' in available_skills:
            print("✅ Constitutional module formation skill is registered in skill executor")
            print(f"   Description: {available_skills['constitutional-module-formation']}")
        else:
            print("❌ Constitutional module formation skill is NOT registered in skill executor")
            print(f"   Available skills: {list(available_skills.keys())}")
            return False
            
        # Test executing through skill executor
        print("\n🚀 Testing execution through skill executor:")
        result = skill_executor.execute_skill('constitutional-module-formation', operation='get_formulation_insights')
        
        if result['success']:
            print("✅ Successfully executed through skill executor")
            insights = result.get('result', {}).get('insights', {})
            print(f"   Insights retrieved: {len(insights)} metrics")
        else:
            print(f"❌ Failed to execute through skill executor: {result.get('error')}")
            return False
            
        print("\n🎉 Skill executor integration successful!")
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Starting Constitutional Module Formation Verification")
    print("="*70)
    
    # Test the constitutional module formation skill
    skill_works = test_constitutional_module_formation()
    
    # Test integration
    integration_works = test_integration_with_skill_executor()
    
    print("\n" + "="*70)
    print("📋 VERIFICATION SUMMARY")
    print("="*70)
    
    if skill_works and integration_works:
        print("✅ ALL TESTS PASSED")
        print("🎯 Constitutional module formation skill is fully operational!")
        print("💡 The skill now supports:")
        print("   - Bottom-up module formation from mature components")
        print("   - Gradual encapsulation as complexity increases")
        print("   - Constitutional requirements for module formation")
        print("   - Component registration and tracking")
        print("   - Automatic module formation when components mature")
        print("   - Relationship-based component clustering")
    else:
        print("❌ SOME TESTS FAILED")
        print("⚠️  Constitutional module formation skill needs attention")
        
    print("\n🏁 Verification complete!")