"""
技能管理器
用于加载和管理所有技能
"""
import os
import sys
from typing import Dict, Any, List
from .skill_base import BaseSkill

# 导入所有技能
from .basic.liveness import LivenessSkill
from .basic.simple_architect import SimpleArchitectSkill
from .intermediate.context_analysis import ContextAnalysisSkill
from .intermediate.context_optimization import ContextOptimizationSkill
from .intermediate.cognitive_template import CognitiveTemplateSkill
from .advanced.system_architect import SystemArchitectSkill
from .advanced.git_operations import GitOperationsSkill
from .advanced.temp_workspace import TempWorkspaceSkill
from .advanced.progressive_disclosure import ProgressiveDisclosureSkill
from .workflows.context_engineering import ContextEngineeringWorkflow


class SkillManager:
    """技能管理器 - 加载和管理所有技能"""
    
    def __init__(self):
        self.skills = {}
        self._load_skills()
    
    def _load_skills(self):
        """加载所有技能"""
        # 基础技能
        self.skills["liveness"] = LivenessSkill()
        self.skills["simple-architect"] = SimpleArchitectSkill()
        
        # 中级技能
        self.skills["context-analysis"] = ContextAnalysisSkill()
        self.skills["context-optimization"] = ContextOptimizationSkill()
        self.skills["cognitive-template"] = CognitiveTemplateSkill()
        
        # 高级技能
        self.skills["system-architect"] = SystemArchitectSkill()
        self.skills["git-operations"] = GitOperationsSkill()
        self.skills["temp-workspace"] = TempWorkspaceSkill()
        self.skills["progressive-disclosure"] = ProgressiveDisclosureSkill()
        
        # 工作流技能
        self.skills["context-engineering-workflow"] = ContextEngineeringWorkflow()
    
    def get_skill(self, skill_name: str) -> BaseSkill:
        """获取指定名称的技能"""
        return self.skills.get(skill_name)
    
    def list_skills(self) -> List[str]:
        """列出所有可用技能"""
        return list(self.skills.keys())
    
    def execute_skill(self, skill_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """执行指定技能"""
        skill = self.get_skill(skill_name)
        if not skill:
            return {
                "status": "error",
                "error": {
                    "type": "SKILL_NOT_FOUND",
                    "message": f"技能 '{skill_name}' 未找到",
                    "code": "SKILL_NOT_FOUND"
                }
            }
        
        return skill.execute(args)