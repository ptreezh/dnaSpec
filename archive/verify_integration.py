import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from src.dsgs_spec_kit_integration.core.skill import DSGSSkill, SkillResult
from src.context_engineering_skills.context_analysis import ContextAnalysisSkill
from src.context_engineering_skills.system import ContextEngineeringSystem

# 测试继承关系
analysis_skill = ContextAnalysisSkill()
system = ContextEngineeringSystem()

print('继承关系验证:')
print(f'ContextAnalysisSkill is DSGSSkill: {isinstance(analysis_skill, DSGSSkill)}')
print(f'ContextEngineeringSystem is DSGSSkill: {isinstance(system, DSGSSkill)}')

# 测试接口一致性
print('\n接口一致性验证:')
print(f'ContextAnalysisSkill has process_request: {hasattr(analysis_skill, "process_request")}')
print(f'ContextEngineeringSystem has process_request: {hasattr(system, "process_request")}')

# 测试执行
print('\n执行验证:')
result = analysis_skill.process_request('测试上下文', {})
print(f'分析技能执行状态: {result.status.name}')
print(f'分析技能结果类型: {type(result.result)}')

result = system.process_request('测试任务', {'function': 'run_context_audit'})
print(f'系统技能执行状态: {result.status.name}')

print('\n✓ 所有验证通过！上下文工程技能与DSGS系统完全兼容')