"""
spec.kit适配器具体实现
集成DNASPEC Context Engineering Skills
"""
from src.dnaspec_spec_kit_integration.adapters.spec_kit_adapter import SpecKitAdapter
from typing import Dict, Any
from src.dnaspec_context_engineering.skills_system_final import (
    ContextAnalysisSkill,
    ContextOptimizationSkill,
    CognitiveTemplateSkill
)


class ConcreteSpecKitAdapter(SpecKitAdapter):
    """具体的SpecKitAdapter实现"""

    def __init__(self):
        super().__init__()

        # 注册DNASPEC核心技能
        self._register_dnaspec_skills()

        # 保留原有的测试技能
        self._register_legacy_skills()

    def _register_dnaspec_skills(self):
        """注册DNASPEC核心上下文工程技能"""
        # 创建技能实例
        self._context_analysis_skill = ContextAnalysisSkill()
        self._context_optimization_skill = ContextOptimizationSkill()
        self._cognitive_template_skill = CognitiveTemplateSkill()

        # 注册核心DNASPEC技能
        self.register_skill('dnaspec-context-analysis', self._context_analysis_wrapper)
        self.register_skill('dnaspec-context-optimization', self._context_optimization_wrapper)
        self.register_skill('dnaspec-cognitive-template', self._cognitive_template_wrapper)

    def _register_legacy_skills(self):
        """注册原有的测试技能"""
        self.register_skill('dnaspec-architect', self._architect_skill)
        self.register_skill('dnaspec-agent-creator', self._agent_creator_skill)
        self.register_skill('dnaspec-task-decomposer', self._task_decomposer_skill)

    def _context_analysis_wrapper(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """上下文分析技能包装器"""
        try:
            result = self._context_analysis_skill.process_request(
                params.get("params", ""),
                params
            )
            return {
                'skill': 'context-analysis',
                'result': result,
                'success': result.status.name == 'COMPLETED'
            }
        except Exception as e:
            return {
                'skill': 'context-analysis',
                'error': str(e),
                'success': False
            }

    def _context_optimization_wrapper(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """上下文优化技能包装器"""
        try:
            result = self._context_optimization_skill.process_request(
                params.get("params", ""),
                params
            )
            return {
                'skill': 'context-optimization',
                'result': result,
                'success': result.status.name == 'COMPLETED'
            }
        except Exception as e:
            return {
                'skill': 'context-optimization',
                'error': str(e),
                'success': False
            }

    def _cognitive_template_wrapper(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """认知模板技能包装器"""
        try:
            result = self._cognitive_template_skill.process_request(
                params.get("params", ""),
                params
            )
            return {
                'skill': 'cognitive-template',
                'result': result,
                'success': result.status.name == 'COMPLETED'
            }
        except Exception as e:
            return {
                'skill': 'cognitive-template',
                'error': str(e),
                'success': False
            }
    
    def execute_skill(self, skill_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行映射的DNASPEC技能"""
        if skill_name in self._registered_skills:
            skill_func = self._registered_skills[skill_name]
            return skill_func(params)
        else:
            raise ValueError(f"Skill not found: {skill_name}")
    
    def _architect_skill(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """架构师技能实现"""
        return {
            'skill': 'architect',
            'result': f'设计了系统架构: {params.get("params", "")}',
            'confidence': 0.95
        }
    
    def _agent_creator_skill(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """智能体创建技能实现"""
        return {
            'skill': 'agent-creator',
            'result': f'创建了智能体: {params.get("params", "")}',
            'confidence': 0.90
        }
    
    def _task_decomposer_skill(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """任务分解技能实现"""
        return {
            'skill': 'task-decomposer',
            'result': f'分解了任务: {params.get("params", "")}',
            'confidence': 0.85
        }