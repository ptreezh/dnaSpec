import sys
print('Python paths:')
for i, path in enumerate(sys.path[:5]):
    print(f'  {i}: {path}')

print('\nTrying to import DNASPEC...')
try:
    from dna_context_engineering.skills_system_final import execute_architect
    print('SUCCESS: DNASPEC imported successfully')
except ImportError as e:
    print(f'FAILED: DNASPEC import failed: {e}')

print('\nTesting execution...')
try:
    result = execute_architect('Test task')
    print(f'SUCCESS: Execution completed: {result[:100]}')
except Exception as e:
    print(f'FAILED: Execution failed: {e}')