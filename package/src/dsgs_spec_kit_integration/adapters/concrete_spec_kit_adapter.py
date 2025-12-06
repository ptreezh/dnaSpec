"""
spec.kit适配器具体实现示例
用于演示和测试完整功能
"""
from src.dsgs_spec_kit_integration.adapters.spec_kit_adapter import SpecKitAdapter
from typing import Dict, Any


class ConcreteSpecKitAdapter(SpecKitAdapter):
    """具体的SpecKitAdapter实现"""
    
    def __init__(self):
        super().__init__()
        # 预注册一些测试技能
        self._test_skills = {
            'dsgs-architect': self._architect_skill,
            'dsgs-agent-creator': self._agent_creator_skill,
            'dsgs-task-decomposer': self._task_decomposer_skill
        }
        
        # 注册测试技能
        for skill_name, skill_func in self._test_skills.items():
            self.register_skill(skill_name, skill_func)
    
    def execute_skill(self, skill_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行映射的DSGS技能"""
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