import sys
import os
sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

from src.dna_spec_kit_integration.skills.architect import execute

print("Testing architect skill...")

# Test 1: Blog system
result1 = execute({'description': '设计一个博客系统'})
print(f'Blog system result: {repr(result1)}')

# Test 2: E-commerce system  
result2 = execute({'description': '设计一个电商系统'})
print(f'E-commerce system result: {repr(result2)}')

# Test 3: Other system
result3 = execute({'description': '设计一个用户认证系统'})
print(f'Authentication system result: {repr(result3)}')

print("Tests completed.")