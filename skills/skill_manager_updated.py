"""
Skill Manager
Used to load and manage all skills
Supports both Chinese and English versions
"""
import os
import sys
from typing import Dict, Any, List
from .skill_base import BaseSkill
from .skill_base_en import BaseSkill as BaseSkillEn

# Import all Chinese skills
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

# Import all English skills
from .basic.liveness_en import LivenessSkill as LivenessSkillEn
from .basic.simple_architect_en import SimpleArchitectSkill as SimpleArchitectSkillEn
from .intermediate.context_analysis_en import ContextAnalysisSkill as ContextAnalysisSkillEn
from .intermediate.context_optimization_en import ContextOptimizationSkill as ContextOptimizationSkillEn
from .intermediate.cognitive_template_en import CognitiveTemplateSkill as CognitiveTemplateSkillEn
from .advanced.system_architect_en import SystemArchitectSkill as SystemArchitectSkillEn
from .advanced.git_operations_en import GitOperationsSkill as GitOperationsSkillEn
from .advanced.temp_workspace_en import TempWorkspaceSkill as TempWorkspaceSkillEn
from .advanced.progressive_disclosure_en import ProgressiveDisclosureSkill as ProgressiveDisclosureSkillEn
from .workflows.context_engineering_en import ContextEngineeringWorkflow as ContextEngineeringWorkflowEn


class SkillManager:
    """Skill Manager - Load and manage all skills"""
    
    def __init__(self, language: str = "zh"):
        self.language = language  # "zh" for Chinese, "en" for English
        self.skills = {}
        self._load_skills()
    
    def _load_skills(self):
        """Load all skills based on language preference"""
        if self.language == "en":
            # Load English skills
            self.skills["liveness"] = LivenessSkillEn()
            self.skills["simple-architect"] = SimpleArchitectSkillEn()
            self.skills["context-analysis"] = ContextAnalysisSkillEn()
            self.skills["context-optimization"] = ContextOptimizationSkillEn()
            self.skills["cognitive-template"] = CognitiveTemplateSkillEn()
            self.skills["system-architect"] = SystemArchitectSkillEn()
            self.skills["git-operations"] = GitOperationsSkillEn()
            self.skills["temp-workspace"] = TempWorkspaceSkillEn()
            self.skills["progressive-disclosure"] = ProgressiveDisclosureSkillEn()
            self.skills["context-engineering-workflow"] = ContextEngineeringWorkflowEn()
        else:
            # Load Chinese skills (default)
            self.skills["liveness"] = LivenessSkill()
            self.skills["simple-architect"] = SimpleArchitectSkill()
            self.skills["context-analysis"] = ContextAnalysisSkill()
            self.skills["context-optimization"] = ContextOptimizationSkill()
            self.skills["cognitive-template"] = CognitiveTemplateSkill()
            self.skills["system-architect"] = SystemArchitectSkill()
            self.skills["git-operations"] = GitOperationsSkill()
            self.skills["temp-workspace"] = TempWorkspaceSkill()
            self.skills["progressive-disclosure"] = ProgressiveDisclosureSkill()
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
            error_msg = f"Skill '{skill_name}' not found"

            return {
                "status": "error",
                "error": {
                    "type": "SKILL_NOT_FOUND",
                    "message": error_msg,
                    "code": "SKILL_NOT_FOUND"
                }
            }

        return skill.execute(args)
    
    def set_language(self, language: str):
        """Set language and reload skills"""
        self.language = language
        self._load_skills()