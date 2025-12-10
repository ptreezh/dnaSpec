"""
上下文工程工作流技能
组合多个技能实现完整的上下文工程流程
"""
from typing import Dict, Any
from ..skill_base import BaseSkill, DetailLevel
from ..intermediate.context_analysis import ContextAnalysisSkill
from ..intermediate.context_optimization import ContextOptimizationSkill
from ..intermediate.cognitive_template import CognitiveTemplateSkill


class ContextEngineeringWorkflow(BaseSkill):
    """上下文工程工作流技能 - 组合多个技能实现完整的上下文工程流程"""
    
    def __init__(self):
        super().__init__(
            name="context-engineering-workflow",
            description="组合多个技能实现完整的上下文工程流程：分析->优化->模板应用"
        )
        
        # 初始化组成技能
        self.context_analysis = ContextAnalysisSkill()
        self.context_optimization = ContextOptimizationSkill()
        self.cognitive_template = CognitiveTemplateSkill()
    
    def _execute_skill_logic(self, input_text: str, detail_level: DetailLevel, 
                          options: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """执行上下文工程工作流逻辑"""
        # 第一步：分析上下文
        analysis_result = self.context_analysis.execute({
            "input": input_text,
            "detail_level": "detailed"
        })
        
        # 第二步：优化上下文
        optimization_result = self.context_optimization.execute({
            "input": input_text,
            "detail_level": "detailed",
            "options": {
                "optimization_goals": ["clarity", "completeness", "relevance"]
            }
        })
        
        # 第三步：应用认知模板
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
        """根据详细程度格式化输出结果"""
        if detail_level == DetailLevel.BASIC:
            # 基础级别只返回核心信息
            return {
                "workflow": result_data["workflow"],
                "final_output": result_data["final_output"]
            }
        elif detail_level == DetailLevel.STANDARD:
            # 标准级别返回主要步骤结果
            return {
                "workflow": result_data["workflow"],
                "steps_count": len(result_data["steps"]),
                "final_output": result_data["final_output"]
            }
        else:  # DETAILED
            # 详细级别返回完整信息
            return result_data