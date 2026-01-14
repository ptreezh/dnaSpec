"""
认知协同增强器 - 为技能添加自动协同能力
让技能能够根据自己的产出自动触发协同机制
"""
from typing import Dict, Any, Callable, Optional
from .cognitive_coordination_center import COORDINATION_CENTER, CoordinationType, CoordinationLevel
import functools

class CognitiveCoordinationEnhancer:
    """认知协同增强器 - 为技能添加自动协同能力"""
    
    def __init__(self):
        self.enhanced_functions = {}
    
    def enhance_skill_with_coordination(self, skill_function: Callable, 
                                      skill_name: str,
                                      coordination_level: CoordinationLevel = CoordinationLevel.LOCAL,
                                      auto_trigger_cycle: bool = True) -> Callable:
        """
        增强技能以支持自动协同
        
        Args:
            skill_function: 原始技能函数
            skill_name: 技能名称
            coordination_level: 协同层级
            auto_trigger_cycle: 是否自动触发协周期
        """
        @functools.wraps(skill_function)
        def enhanced_wrapper(args: Dict[str, Any]) -> str:
            # 1. 执行原始技能
            result = skill_function(args)
            
            # 2. 从结果中提取上下文信息
            context_data = self._extract_context_from_result(result, skill_name)
            
            # 3. 注册上下文对齐协
            COORDINATION_CENTER.register_coordination_point(
                skill_name=skill_name,
                coordination_type=CoordinationType.CONTEXT_ALIGNMENT,
                data=context_data,
                level=coordination_level
            )
            
            # 4. 提取目标信息
            goal_data = self._extract_goal_from_args(args, skill_name)
            if goal_data:
                COORDINATION_CENTER.register_coordination_point(
                    skill_name=skill_name,
                    coordination_type=CoordinationType.GOAL_ALIGNMENT,
                    data=goal_data,
                    level=coordination_level
                )
            
            # 5. 提取质量相关信息
            quality_data = {
                "skill_name": skill_name,
                "result": result,
                "args": args
            }
            COORDINATION_CENTER.register_coordination_point(
                skill_name=skill_name,
                coordination_type=CoordinationType.QUALITY_ASSURANCE,
                data=quality_data,
                level=coordination_level
            )
            
            # 6. 一致性检查
            consistency_data = {
                "skill_name": skill_name,
                "result": result,
                "timestamp": args.get("timestamp", ""),
                "context": args.get("context", "")
            }
            COORDINATION_CENTER.register_coordination_point(
                skill_name=skill_name,
                coordination_type=CoordinationType.CONSISTENCY_MAINTENANCE,
                data=consistency_data,
                level=coordination_level
            )
            
            # 7. 根据需要触发协周期
            if auto_trigger_cycle:
                COORDINATION_CENTER.trigger_coordination_cycle()
            
            return result
        
        # 存储增强后的函数
        self.enhanced_functions[skill_name] = enhanced_wrapper
        
        return enhanced_wrapper
    
    def _extract_context_from_result(self, result: str, skill_name: str) -> Dict[str, Any]:
        """从结果中提取上下文信息"""
        return {
            "context_key": f"{skill_name}_output",
            "context": result,
            "skill_name": skill_name
        }
    
    def _extract_goal_from_args(self, args: Dict[str, Any], skill_name: str) -> Optional[Dict[str, Any]]:
        """从参数中提取目标信息"""
        goal_keywords = ["goal", "target", "objective", "purpose", "intent", "desired"]
        
        for keyword in goal_keywords:
            if keyword in args:
                return {
                    "goal_key": f"{skill_name}_goal",
                    "goal": str(args[keyword]),
                    "skill_name": skill_name
                }
        
        return None
    
    def sync_contexts_between_skills(self, skill1_name: str, skill2_name: str) -> Dict[str, Any]:
        """同步两个技能之间的上下文"""
        return {
            "status": "sync_completed",
            "skills_synced": [skill1_name, skill2_name]
        }
    
    def trigger_inter_skill_coordination(self, triggering_skill: str, affected_skills: List[str]) -> Dict[str, Any]:
        """触发跨技能协"""
        coordination_data = {
            "triggering_skill": triggering_skill,
            "affected_skills": affected_skills,
            "action": "inter_skill_coordination",
            "timestamp": "now"
        }
        
        # 对每个受影响的技能触发协
        for skill in affected_skills:
            COORDINATION_CENTER.register_coordination_point(
                skill_name=skill,
                coordination_type=CoordinationType.CONTEXT_ALIGNMENT,
                data=coordination_data,
                level=CoordinationLevel.INTER
            )
        
        COORDINATION_CENTER.trigger_coordination_cycle()
        
        return {
            "status": "inter_skill_coordination_triggered",
            "triggering_skill": triggering_skill,
            "affected_skills": affected_skills
        }

# 全局认知协同增强器实例
COGNITIVE_ENHANCER = CognitiveCoordinationEnhancer()