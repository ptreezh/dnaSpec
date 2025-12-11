"""
Skill Manager
Used to load and manage all skills
"""
import os
import sys
from typing import Dict, Any, List
from .skill_base_en import BaseSkill

# Import all English skills
from .basic.liveness_en import LivenessSkill
from .basic.simple_architect_en import SimpleArchitectSkill
from .intermediate.context_analysis_en import ContextAnalysisSkill
from .intermediate.context_optimization_en import ContextOptimizationSkill
from .intermediate.cognitive_template_en import CognitiveTemplateSkill
from .advanced.system_architect_en import SystemArchitectSkill
from .advanced.git_operations_en import GitOperationsSkill
from .advanced.temp_workspace_en import TempWorkspaceSkill
from .advanced.progressive_disclosure_en import ProgressiveDisclosureSkill
from .workflows.context_engineering_en import ContextEngineeringWorkflow


class SkillManager:
    """Skill Manager - Load and manage all skills"""
    
    def __init__(self):
        self.skills = {}
        self._load_skills()
    
    def _load_skills(self):
        """Load all skills"""
        # Basic skills
        self.skills["liveness"] = LivenessSkill()
        self.skills["simple-architect"] = SimpleArchitectSkill()
        
        # Intermediate skills
        self.skills["context-analysis"] = ContextAnalysisSkill()
        self.skills["context-optimization"] = ContextOptimizationSkill()
        self.skills["cognitive-template"] = CognitiveTemplateSkill()
        
        # Advanced skills
        self.skills["system-architect"] = SystemArchitectSkill()
        self.skills["git-operations"] = GitOperationsSkill()
        self.skills["temp-workspace"] = TempWorkspaceSkill()
        self.skills["progressive-disclosure"] = ProgressiveDisclosureSkill()
        
        # Workflow skills
        self.skills["context-engineering-workflow"] = ContextEngineeringWorkflow()
    
    def get_skill(self, skill_name: str) -> BaseSkill:
        """Get skill by specified name"""
        return self.skills.get(skill_name)
    
    def list_skills(self) -> List[str]:
        """List all available skills"""
        return list(self.skills.keys())
    
    def execute_skill(self, skill_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute specified skill"""
        skill = self.get_skill(skill_name)
        if not skill:
            return {
                "status": "error",
                "error": {
                    "type": "SKILL_NOT_FOUND",
                    "message": f"Skill '{skill_name}' not found",
                    "code": "SKILL_NOT_FOUND"
                }
            }
        
        return skill.execute(args)