import sys
import os
sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

print("Testing skills with execute functions...")

# Test architect skill
try:
    from src.dna_spec_kit_integration.skills.architect import execute as architect_execute
    result = architect_execute({'description': '设计一个电商系统'})
    print(f'Architect skill: SUCCESS - {repr(result)}')
except Exception as e:
    print(f'Architect skill: FAILED - {e}')

# Test cache_manager skill
try:
    from src.dna_spec_kit_integration.skills.cache_manager import execute as cache_execute
    result = cache_execute({'operation': 'status'})
    print(f'Cache Manager skill: SUCCESS - type: {type(result)}, length: {len(str(result)) if result else 0}')
except Exception as e:
    print(f'Cache Manager skill: FAILED - {e}')

# Test cognitive_template skill
try:
    from src.dna_spec_kit_integration.skills.cognitive_template import execute as cognitive_execute
    result = cognitive_execute({'context': 'How to improve performance?', 'template_type': 'chain_of_thought'})
    print(f'Cognitive Template skill: SUCCESS - type: {type(result)}, length: {len(str(result)) if result else 0}')
except Exception as e:
    print(f'Cognitive Template skill: FAILED - {e}')

# Test context_analysis skill
try:
    from src.dna_spec_kit_integration.skills.context_analysis import execute as context_analysis_execute
    result = context_analysis_execute({'context': 'A simple requirement'})
    print(f'Context Analysis skill: SUCCESS - type: {type(result)}, length: {len(str(result)) if result else 0}')
except Exception as e:
    print(f'Context Analysis skill: FAILED - {e}')

# Test system_architect skill
try:
    from src.dna_spec_kit_integration.skills.system_architect import execute as system_arch_execute
    result = system_arch_execute({'requirements': 'Build a web app'})
    print(f'System Architect skill: SUCCESS - type: {type(result)}, length: {len(str(result)) if result else 0}')
except Exception as e:
    print(f'System Architect skill: FAILED - {e}')

print("Testing completed.")