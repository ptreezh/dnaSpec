"""
DNASPEC技能模块初始化文件

包含DNASPEC核心技能和上下文工程增强技能
"""
from . import architect
from . import liveness  
from . import examples

# 导入上下文工程技能（作为独立函数）
from .context_analysis import execute as context_analysis_execute
from .context_optimization import execute as context_optimization_execute
from .cognitive_template import execute as cognitive_template_execute

__all__ = [
    'architect',
    'liveness', 
    'examples',
    # 上下文工程技能函数接口
    'context_analysis_execute',
    'context_optimization_execute',
    'cognitive_template_execute'
]

# 为CLI命令提供统一访问接口
SKILL_FUNCTIONS = {
    'architect': architect.execute,
    'liveness': liveness.execute,
    'context-analysis': context_analysis_execute,
    'context-optimization': context_optimization_execute,
    'cognitive-template': cognitive_template_execute
}


def run_skill(skill_name: str, args: dict) -> str:
    """
    统一技能执行接口
    """
    if skill_name not in SKILL_FUNCTIONS:
        available_skills = list(SKILL_FUNCTIONS.keys())
        return f"错误: 未知技能 '{skill_name}'. 可用技能: {', '.join(available_skills)}"
    
    try:
        skill_func = SKILL_FUNCTIONS[skill_name]
        return skill_func(args)
    except Exception as e:
        return f"技能执行错误: {e}"