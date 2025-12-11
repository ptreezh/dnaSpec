"""
Liveness Skill - Refactored Version
Compliant with DNASPEC Standardized Skill Interface Specification
"""
from typing import Dict, Any
from ..skill_base_en import BaseSkill, DetailLevel


class LivenessSkill(BaseSkill):
    """Liveness Skill - Simple alive check skill"""
    
    def __init__(self):
        super().__init__(
            name="liveness",
            description="Simple alive check skill, returns 'alive'"
        )
    
    def _execute_skill_logic(self, input_text: str, detail_level: DetailLevel, 
                          options: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Execute Liveness skill logic"""
        return "alive"
    
    def _format_output(self, result_data: str, detail_level: DetailLevel) -> str:
        """Format output result - For Liveness skill, all detail levels return the same result"""
        return result_data