"""
Claude兼容技能文件
映射到Claude Skills主实现
"""
import sys
import os
# 将当前包的路径添加到Python路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 从claude_skills包中的main模块导入
from main import lambda_handler as execute
from main import (
    _execute_architect_skill,
    _execute_context_analysis_skill,
    _execute_context_optimization_skill,
    _execute_cognitive_template_skill,
    _execute_agent_creator_skill,
    _execute_task_decomposer_skill,
    _execute_constraint_generator_skill
)

# 保持与原有接口的兼容性
__all__ = [
    'execute',
    'lambda_handler',
    '_execute_architect_skill',
    '_execute_context_analysis_skill',
    '_execute_context_optimization_skill',
    '_execute_cognitive_template_skill',
    '_execute_agent_creator_skill',
    '_execute_task_decomposer_skill',
    '_execute_constraint_generator_skill'
]


def execute_skill(skill_args):
    """
    标准执行接口 - 用于与DNASPEC系统兼容
    """
    # 模拟Claude Skills格式的事件
    event = {
        'inputs': [skill_args],
        'tool_name': skill_args.get('skill', 'architect')
    }
    context = None

    return execute(event, context)