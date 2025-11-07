"""
DSGS Context Engineering Skills Package Initialization
"""
from typing import Dict, Any, List
from .core_skill import ContextEngineeringSkill, SkillResult, SkillsManager
from .ai_client import AIModelClient, create_ai_client
from .instruction_template import TemplateRegistry
from .system import ContextEngineeringSystem
from .skills.context_analysis import ContextAnalysisSkill, execute as context_analysis_execute
from .skills.context_optimization import ContextOptimizationSkill, execute as context_optimization_execute  
from .skills.cognitive_template import CognitiveTemplateSkill, execute as cognitive_template_execute


__version__ = "1.0.0"
__author__ = "DSGS Context Engineering Team"
__description__ = "AI CLI平台的上下文工程增强工具集"


def get_system_info() -> Dict[str, Any]:
    """获取系统信息"""
    return {
        'name': 'DSGS Context Engineering Skills System',
        'version': __version__,
        'description': __description__,
        'modules': [
            'context_analysis', 
            'context_optimization', 
            'cognitive_template'
        ],
        'features': [
            '5维上下文质量分析',
            '多目标上下文优化', 
            '5种认知模板应用',
            'AI平台适配器集成',
            '结构化结果输出'
        ]
    }


def create_context_engineering_system(ai_provider: str = "generic", api_key: str = "") -> ContextEngineeringSystem:
    """创建上下文工程系统实例"""
    return ContextEngineeringSystem(ai_provider, api_key)


# 快速访问接口
def analyze_context(context: str, api_key: str = "", provider: str = "generic") -> Dict[str, Any]:
    """快速分析上下文质量"""
    system = create_context_engineering_system(provider, api_key)
    return system.skills_manager.execute_skill('context-analysis', context, {})


def optimize_context(context: str, goals: List[str] = None, api_key: str = "", provider: str = "generic") -> Dict[str, Any]:
    """快速优化上下文质量"""
    if goals is None:
        goals = ['clarity', 'completeness']
    
    system = create_context_engineering_system(provider, api_key)
    return system.skills_manager.execute_skill('context-optimization', context, {'optimization_goals': goals})


def apply_cognitive_template(context: str, template: str = 'chain_of_thought', api_key: str = "", provider: str = "generic") -> Dict[str, Any]:
    """快速应用认知模板"""
    system = create_context_engineering_system(provider, api_key)
    return system.skills_manager.execute_skill('cognitive-template', context, {'template': template})


__all__ = [
    'ContextEngineeringSkill',
    'SkillResult', 
    'SkillsManager',
    'ContextEngineeringSystem',
    'ContextAnalysisSkill',
    'ContextOptimizationSkill', 
    'CognitiveTemplateSkill',
    'TemplateRegistry',
    'AIModelClient',
    'create_ai_client',
    'get_system_info',
    'create_context_engineering_system',
    'analyze_context',
    'optimize_context', 
    'apply_cognitive_template',
    'context_analysis_execute',
    'context_optimization_execute',
    'cognitive_template_execute'
]