#!/usr/bin/env python3
"""
Test script to verify agent creator functionality
"""

def test_agent_creator():
    try:
        from src.dna_spec_kit_integration.skills.agent_creator_independent import execute_agent_creator
        result = execute_agent_creator({'context': 'Create a test agent for data analysis'})
        print(f"Agent Creator skill result: {result}")
        return result
    except Exception as e:
        print(f"Agent Creator error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
        
def test_core_skills():
    try:
        from src.dna_context_engineering.skills_system_final import execute
        result1 = execute({'skill': 'context-analysis', 'context': 'Test analysis context'})
        print(f"Context Analysis result: {type(result1)} - {str(result1)[:100]}...")
        
        result2 = execute({'skill': 'context-optimization', 'context': 'Test optimization context'})
        print(f"Context Optimization result: {type(result2)} - {str(result2)[:100]}...")
        
        result3 = execute({'skill': 'cognitive-template', 'context': 'Test cognitive template', 'params': {'template': 'chain_of_thought'}})
        print(f"Cognitive Template result: {type(result3)} - {str(result3)[:100]}...")
        
        return [result1, result2, result3]
    except Exception as e:
        print(f"Core skills error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("Testing Agent Creator...")
    test_agent_creator()
    print("\nTesting Core Skills...")
    test_core_skills()