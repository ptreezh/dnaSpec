"""
DNASPEC技能模块初始化文件

包含DNASPEC核心技能和上下文工程增强技能
"""
# 只保留统一技能模块
from .unified_skill import execute

__all__ = [
    'execute',
]

# 为CLI命令提供统一访问接口
SKILL_FUNCTIONS = {
    'unified_skill': execute,
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