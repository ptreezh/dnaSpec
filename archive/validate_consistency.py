import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from src.dsgs_spec_kit_integration.skills.architect import execute as architect_execute
from src.context_engineering_skills.context_analysis import execute as context_analysis_execute

# 测试两个技能的输出格式一致性
architect_result = architect_execute({'description': '电商系统'})
context_result = context_analysis_execute({'context': '电商系统设计要求明确'})

print('Architect Skill Output Type:', type(architect_result))
print('Context Analysis Skill Output Type:', type(context_result))
print('Both return strings:', isinstance(architect_result, str) and isinstance(context_result, str))
print()
print('Architect Output:', repr(architect_result))
print('Context Analysis Output (first 100 chars):', repr(context_result[:100]))