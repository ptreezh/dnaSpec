"""
Cognitive Template Skill - Refactored Version
Compliant with DNASPEC Standardized Skill Interface Specification
"""
from typing import Dict, Any
from ..skill_base_en import BaseSkill, DetailLevel


class CognitiveTemplateSkill(BaseSkill):
    """Cognitive Template Skill"""
    
    def __init__(self):
        super().__init__(
            name="cognitive-template",
            description="Apply cognitive templates to context engineering tasks, providing frameworks like chain-of-thought, few-shot learning, and verification checks"
        )
        self.templates = {
            "chain-of-thought": {
                "name": "Chain of Thought",
                "description": "Break down complex problems into sequential reasoning steps",
                "template": """Problem: {problem}

Thought Process:
1. Understand the problem requirements
2. Identify key constraints and assumptions
3. Break down into sub-problems
4. Solve each sub-problem step-by-step
5. Verify solution consistency
6. Present final answer

Solution:"""
            },
            "few-shot": {
                "name": "Few-Shot Learning",
                "description": "Provide examples to guide problem solving",
                "template": """Examples:
{examples}

New Problem: {problem}

Solution:"""
            },
            "verification": {
                "name": "Verification Checklist",
                "description": "Systematic verification approach for solution quality",
                "template": """Solution: {solution}

Verification Checklist:
□ Requirements fully addressed
□ Technical feasibility confirmed
□ Edge cases considered
□ Security implications evaluated
□ Performance requirements met
□ Maintainability ensured
□ Documentation complete

Verified Items:"""
            }
        }
    
    def _execute_skill_logic(self, input_text: str, detail_level: DetailLevel, 
                          options: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute cognitive template logic"""
        # Get template type
        template_type = options.get("template", "chain-of-thought")
        if template_type not in self.templates:
            template_type = "chain-of-thought"
        
        # Get template
        template = self.templates[template_type]
        
        # Apply template
        if template_type == "few-shot":
            # For few-shot, we need examples
            examples = options.get("examples", "Example 1: Problem A -> Solution A\nExample 2: Problem B -> Solution B")
            applied_template = template["template"].format(
                problem=input_text,
                examples=examples
            )
        elif template_type == "verification":
            # For verification, we need a solution to verify
            solution = options.get("solution", "Proposed solution goes here")
            applied_template = template["template"].format(
                solution=solution
            )
        else:
            # For chain-of-thought and others
            applied_template = template["template"].format(
                problem=input_text
            )
        
        return {
            "template_type": template_type,
            "template_name": template["name"],
            "template_description": template["description"],
            "applied_template": applied_template,
            "available_templates": list(self.templates.keys())
        }
    
    def _format_output(self, result_data: Dict[str, Any], detail_level: DetailLevel) -> Dict[str, Any]:
        """Format output result based on detail level"""
        if detail_level == DetailLevel.BASIC:
            # Basic level returns core information only
            return {
                "applied_template": result_data["applied_template"],
                "template_type": result_data["template_type"]
            }
        elif detail_level == DetailLevel.STANDARD:
            # Standard level returns standard information
            return {
                "template_name": result_data["template_name"],
                "template_description": result_data["template_description"],
                "applied_template": result_data["applied_template"]
            }
        else:  # DETAILED
            # Detailed level returns complete information
            return {
                "template_type": result_data["template_type"],
                "template_name": result_data["template_name"],
                "template_description": result_data["template_description"],
                "applied_template": result_data["applied_template"],
                "available_templates": result_data["available_templates"]
            }