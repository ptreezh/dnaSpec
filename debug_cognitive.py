import sys
import os
sys.path.insert(0, os.path.join('D:', 'DAIP', 'dnaSpec', 'src'))

try:
    from src.dna_context_engineering.skills_system_final import execute_cognitive_template
    result = execute_cognitive_template('Test context')
    print('Result:', repr(result))
except Exception as e:
    print('Error:', str(e))
    import traceback
    traceback.print_exc()