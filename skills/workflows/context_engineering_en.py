"""
Context Engineering Workflow Skill
Combines multiple skills to implement a complete context engineering process
"""
from typing import Dict, Any
from ..skill_base_en import BaseSkill, DetailLevel
from ..intermediate.context_analysis_en import ContextAnalysisSkill
from ..intermediate.context_optimization_en import ContextOptimizationSkill
from ..intermediate.cognitive_template_en import CognitiveTemplateSkill


class ContextEngineeringWorkflow(BaseSkill):
    """Context Engineering Workflow Skill - Combines multiple skills to implement a complete context engineering process"""
    
    def __init__(self):
        super().__init__(
            name="context-engineering-workflow",
            description="Combines multiple skills to implement a complete context engineering process: analysis->optimization->template application"
        )
        
        # Initialize component skills
        self.context_analysis = ContextAnalysisSkill()
        self.context_optimization = ContextOptimizationSkill()
        self.cognitive_template = CognitiveTemplateSkill()
    
    def _execute_skill_logic(self, input_text: str, detail_level: DetailLevel, 
                          options: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute context engineering workflow logic"""
        # Step 1: Analyze context
        analysis_result = self.context_analysis.execute({
            "input": input_text,
            "detail_level": "detailed"
        })
        
        # Step 2: Optimize context
        optimization_result = self.context_optimization.execute({
            "input": input_text,
            "detail_level": "detailed",
            "options": {
                "optimization_goals": ["clarity", "completeness", "relevance"]
            }
        })
        
        # Step 3: Apply cognitive template
        template_result = self.cognitive_template.execute({
            "input": input_text,
            "detail_level": "detailed",
            "options": {
                "template": "chain_of_thought"
            }
        })
        
        return {
            "workflow": "context-engineering",
            "steps": [
                {
                    "step": 1,
                    "name": "context-analysis",
                    "result": analysis_result
                },
                {
                    "step": 2,
                    "name": "context-optimization",
                    "result": optimization_result
                },
                {
                    "step": 3,
                    "name": "cognitive-template",
                    "result": template_result
                }
            ],
            "final_output": {
                "original_context": input_text,
                "analyzed_metrics": analysis_result.get("data", {}).get("metrics", {}),
                "optimized_context": optimization_result.get("data", {}).get("optimized_context", ""),
                "template_applied": template_result.get("data", {}).get("template_type", "")
            }
        }
    
    def _format_output(self, result_data: Dict[str, Any], detail_level: DetailLevel) -> Dict[str, Any]:
        """Format output result based on detail level"""
        if detail_level == DetailLevel.BASIC:
            # Basic level returns core information only
            return {
                "workflow": result_data["workflow"],
                "final_output": result_data["final_output"]
            }
        elif detail_level == DetailLevel.STANDARD:
            # Standard level returns main step results
            return {
                "workflow": result_data["workflow"],
                "steps_count": len(result_data["steps"]),
                "final_output": result_data["final_output"]
            }
        else:  # DETAILED
            # Detailed level returns complete information
            return result_data