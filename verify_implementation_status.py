#!/usr/bin/env python3
"""
Comprehensive verification of DNASPEC skills actual implementation status
"""

def test_agent_creator():
    """Test the agent creator skill"""
    print("Testing Agent Creator Skill...")
    try:
        from src.dna_spec_kit_integration.skills.agent_creator_independent import execute_agent_creator
        result = execute_agent_creator({'context': 'Create a test agent for data analysis'})
        print(f"✅ Agent Creator: SUCCESS - {result['success']}")
        print(f"   Result type: {type(result['result'])}")
        print(f"   Agent name: {result['result']['name']}")
        return True
    except Exception as e:
        print(f"❌ Agent Creator: FAILED - {str(e)}")
        return False

def test_core_context_skills():
    """Test the core context engineering skills"""
    print("\nTesting Core Context Engineering Skills...")
    success_count = 0
    
    try:
        from src.dna_context_engineering.skills_system_final import execute
        
        # Test context analysis
        try:
            result = execute({'skill': 'context-analysis', 'context': 'Test analysis context'})
            print(f"✅ Context Analysis: SUCCESS - Output type: {type(result)}")
            success_count += 1
        except Exception as e:
            print(f"❌ Context Analysis: FAILED - {str(e)}")
        
        # Test context optimization
        try:
            result = execute({'skill': 'context-optimization', 'context': 'Test optimization context'})
            print(f"✅ Context Optimization: SUCCESS - Output type: {type(result)}")
            success_count += 1
        except Exception as e:
            print(f"❌ Context Optimization: FAILED - {str(e)}")
        
        # Test cognitive template
        try:
            result = execute({'skill': 'cognitive-template', 'context': 'Test cognitive template', 'params': {'template': 'chain_of_thought'}})
            print(f"✅ Cognitive Template: SUCCESS - Output type: {type(result)}")
            success_count += 1
        except Exception as e:
            print(f"❌ Cognitive Template: FAILED - {str(e)}")
        
        return success_count
    except Exception as e:
        print(f"❌ Core Skills Module: FAILED to import - {str(e)}")
        return 0

def test_advanced_skills_via_executor():
    """Test advanced skills through the skill executor"""
    print("\nTesting Advanced Skills via Skill Executor...")
    success_count = 0
    
    try:
        from src.dna_spec_kit_integration.skills.skill_executor import skill_executor
        
        # Check available skills
        available_skills = skill_executor.get_available_skills()
        print(f"Available skills in executor: {list(available_skills.keys())}")
        
        # Test some skills if available
        if 'agent-creator' in available_skills:
            try:
                result = skill_executor.execute_skill('agent-creator', 'Create a test agent')
                print(f"✅ Agent Creator via Executor: SUCCESS")
                success_count += 1
            except Exception as e:
                print(f"❌ Agent Creator via Executor: FAILED - {str(e)}")
        
        if 'architect' in available_skills:
            try:
                result = skill_executor.execute_skill('architect', 'Design a simple system')
                print(f"✅ Architect via Executor: SUCCESS")
                success_count += 1
            except Exception as e:
                print(f"❌ Architect via Executor: FAILED - {str(e)}")
        
        if 'context-analysis' in available_skills:
            try:
                result = skill_executor.execute_skill('context-analysis', 'Test context')
                print(f"✅ Context Analysis via Executor: SUCCESS")
                success_count += 1
            except Exception as e:
                print(f"❌ Context Analysis via Executor: FAILED - {str(e)}")
        
        return success_count
    except Exception as e:
        print(f"❌ Skill Executor: FAILED - {str(e)}")
        return 0

def test_cli_integration():
    """Test CLI integration"""
    print("\nTesting CLI Integration...")
    try:
        from src.dna_spec_kit_integration.cli_extension_handler import get_available_skills
        skills_info = get_available_skills()
        print(f"✅ CLI Integration: SUCCESS - {skills_info['total_count']} skills available")
        print(f"   Categories: {skills_info['categories']}")
        return True
    except Exception as e:
        print(f"❌ CLI Integration: FAILED - {str(e)}")
        return False

def test_adapter_implementation():
    """Test adapter implementation"""
    print("\nTesting Adapter Implementation...")
    try:
        from src.dna_spec_kit_integration.adapters.concrete_spec_kit_adapter import ConcreteSpecKitAdapter
        adapter = ConcreteSpecKitAdapter()
        registered_skills = adapter.get_registered_skills() if hasattr(adapter, 'get_registered_skills') else 'Method not available'
        print(f"✅ Concrete Adapter: SUCCESS - {len(adapter._registered_skills)} registered skills")
        print(f"   Registered skills: {list(adapter._registered_skills.keys())}")
        return True
    except Exception as e:
        print(f"❌ Concrete Adapter: FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main verification function"""
    print("="*70)
    print("DNASPEC SKILLS IMPLEMENTATION STATUS VERIFICATION")
    print("="*70)
    
    results = {}
    
    # Test individual skills
    results['agent_creator'] = test_agent_creator()
    results['core_skills_count'] = test_core_context_skills()
    results['executor_skills_count'] = test_advanced_skills_via_executor()
    results['cli_integration'] = test_cli_integration()
    results['adapter_implementation'] = test_adapter_implementation()
    
    # Summary
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    
    print(f"✅ Agent Creator: {'PASS' if results['agent_creator'] else 'FAIL'}")
    print(f"✅ Core Context Skills: {results['core_skills_count']}/3 working")
    print(f"✅ Executor Skills: {results['executor_skills_count']}/3 tested successfully")
    print(f"✅ CLI Integration: {'PASS' if results['cli_integration'] else 'FAIL'}")
    print(f"✅ Adapter Implementation: {'PASS' if results['adapter_implementation'] else 'FAIL'}")
    
    total_possible = 1 + 3 + 3 + 1 + 1  # 9 total checks
    total_passed = (
        int(results['agent_creator']) + 
        results['core_skills_count'] + 
        results['executor_skills_count'] + 
        int(results['cli_integration']) + 
        int(results['adapter_implementation'])
    )
    
    print(f"\n📊 Overall Status: {total_passed}/{total_possible} checks passed")
    print(f"   Success Rate: {total_passed/total_possible*100:.1f}%")
    
    if total_passed == total_possible:
        print("🎉 ALL SYSTEMS OPERATIONAL - Full Implementation Verified!")
    elif total_passed/total_possible >= 0.8:
        print("✅ MOSTLY IMPLEMENTED - Core functionality working")
    elif total_passed/total_possible >= 0.5:
        print("⚠️  PARTIALLY IMPLEMENTED - Core skills available but some advanced features missing")
    else:
        print("❌ UNDER IMPLEMENTATION - Significant functionality missing")

if __name__ == "__main__":
    main()