"""
Simple Architect Skill - Refactored Version
Compliant with DNASPEC Standardized Skill Interface Specification
"""
from typing import Dict, Any
from ..skill_base import BaseSkill, DetailLevel


class SimpleArchitectSkill(BaseSkill):
    """Simple Architect Skill - Generates simple text architecture diagrams"""

    def __init__(self):
        super().__init__(
            name="simple-architect",
            description="Generates a simple text architecture diagram based on input requirement description"
        )

        # Architecture mapping table
        self.architecture_map = {
            "电商": "[WebApp] -> [API Server] -> [Database]",
            "博客": "[WebApp] -> [Database]",
        }
    
    def _execute_skill_logic(self, input_text: str, detail_level: DetailLevel,
                          options: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Execute Simple Architect skill logic"""
        description = input_text.lower()

        # Check keyword matching
        for keyword, architecture in self.architecture_map.items():
            if keyword in description:
                return architecture

        # Check broader matching
        if "电商" in description or "电子商务" in description:
            return "[WebApp] -> [API Server] -> [Database]"
        elif "博客" in description or "blog" in description:
            return "[WebApp] -> [Database]"

        # No matching architecture
        return ""

    def _format_output(self, result_data: str, detail_level: DetailLevel) -> str:
        """Format output result - For Simple Architect skill, all detail levels return the same result"""
        return result_data