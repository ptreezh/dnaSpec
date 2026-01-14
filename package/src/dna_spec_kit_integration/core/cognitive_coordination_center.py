"""
认知协同中心 - 实现技能间的间接协同机制
确保各技能产出能够自动协调，保持层级对齐和上下文可控
"""
from typing import Dict, Any, List, Optional
import json
import threading
from datetime import datetime
from enum import Enum
import re

class CoordinationLevel(Enum):
    """协同层级"""
    LOCAL = "local"           # 同一技能组内的协同
    INTER = "inter"           # 技能间的协同
    SYSTEM = "system"         # 系统级协同

class CoordinationType(Enum):
    """协同类型"""
    CONTEXT_ALIGNMENT = "context_alignment"      # 上下文对齐
    GOAL_ALIGNMENT = "goal_alignment"            # 目标对齐
    QUALITY_ASSURANCE = "quality_assurance"      # 质量保证
    CONSISTENCY_MAINTENANCE = "consistency_maintenance"  # 一致性维护
    FEEDBACK_LOOP = "feedback_loop"              # 反馈循环

class CognitiveCoordinationCenter:
    """认知协同中心 - 实现技能间的间接协同"""
    
    def __init__(self):
        self.coordination_registry = {}  # 协同注册表
        self.context_state = {}  # 上下文状态
        self.goal_alignment = {}  # 目标对齐
        self.quality_metrics = {}  # 质量指标
        self.lock = threading.Lock()
        
        # 初始化协同规则
        self.coordination_rules = {
            CoordinationType.CONTEXT_ALIGNMENT: self._align_contexts,
            CoordinationType.GOAL_ALIGNMENT: self._align_goals,
            CoordinationType.QUALITY_ASSURANCE: self._assure_quality,
            CoordinationType.CONSISTENCY_MAINTENANCE: self._maintain_consistency,
            CoordinationType.FEEDBACK_LOOP: self._process_feedback
        }
        
    def register_coordination_point(self, skill_name: str, coordination_type: CoordinationType, 
                                  data: Dict[str, Any], level: CoordinationLevel = CoordinationLevel.LOCAL):
        """注册协 точки"""
        with self.lock:
            coord_id = f"{skill_name}_{coordination_type.value}_{datetime.now().timestamp()}"
            
            coordination_entry = {
                "skill_name": skill_name,
                "coordination_type": coordination_type.value,
                "data": data,
                "level": level.value,
                "timestamp": datetime.now().isoformat(),
                "processed": False
            }
            
            if skill_name not in self.coordination_registry:
                self.coordination_registry[skill_name] = []
            
            self.coordination_registry[skill_name].append(coordination_entry)
            
            return coord_id
    
    def trigger_coordination_cycle(self):
        """触发协周期"""
        with self.lock:
            for skill_name, coordinations in self.coordination_registry.items():
                for coord_entry in coordinations:
                    if not coord_entry["processed"]:
                        coord_type = CoordinationType(coord_entry["coordination_type"])
                        rule_func = self.coordination_rules.get(coord_type)
                        
                        if rule_func:
                            # 运行协规则
                            result = rule_func(coord_entry["data"], coord_entry["level"])
                            
                            # 更新处理状态
                            coord_entry["processed"] = True
                            coord_entry["result"] = result
                            
    def _align_contexts(self, data: Dict[str, Any], level: str) -> Dict[str, Any]:
        """上下文对齐协规则"""
        context_key = data.get("context_key", "default")
        new_context = data.get("context", "")
        
        # 检查是否已经有相似上下文
        if context_key in self.context_state:
            prev_context = self.context_state[context_key]
            # 确保新上下文与现有上下文一致
            alignment_score = self._calculate_context_alignment(prev_context, new_context)
            
            if alignment_score < 0.7:  # 低于阈值需要对齐
                aligned_context = self._align_context_with_existing(prev_context, new_context)
                self.context_state[context_key] = aligned_context
                return {
                    "status": "aligned",
                    "alignment_score": alignment_score,
                    "aligned_context": aligned_context
                }
        
        # 如果没有现有上下文，存储新上下文
        self.context_state[context_key] = new_context
        return {
            "status": "stored",
            "context_key": context_key,
            "alignment_score": 1.0
        }
    
    def _align_goals(self, data: Dict[str, Any], level: str) -> Dict[str, Any]:
        """目标对齐协规则"""
        goal_key = data.get("goal_key", "default")
        new_goal = data.get("goal", "")
        
        if goal_key in self.goal_alignment:
            prev_goal = self.goal_alignment[goal_key]
            # 确保新目标与现有目标一致
            alignment_score = self._calculate_goal_alignment(prev_goal, new_goal)
            
            if alignment_score < 0.75:  # 目标对齐阈值
                aligned_goal = self._align_goal_with_existing(prev_goal, new_goal)
                self.goal_alignment[goal_key] = aligned_goal
                return {
                    "status": "goal_aligned",
                    "alignment_score": alignment_score,
                    "aligned_goal": aligned_goal
                }
        
        self.goal_alignment[goal_key] = new_goal
        return {
            "status": "goal_stored",
            "goal_key": goal_key,
            "alignment_score": 1.0
        }
    
    def _assure_quality(self, data: Dict[str, Any], level: str) -> Dict[str, Any]:
        """质量保证协规则"""
        skill_name = data.get("skill_name", "")
        result_data = data.get("result", {})
        
        # 存储质量指标
        metrics = self._extract_quality_metrics(result_data)
        self.quality_metrics[skill_name] = {
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        }
        
        # 检查是否需要质量改进
        if self._needs_quality_improvement(metrics):
            return {
                "status": "quality_monitored",
                "metrics": metrics,
                "needs_improvement": True
            }
        
        return {
            "status": "quality_assured",
            "metrics": metrics
        }
    
    def _maintain_consistency(self, data: Dict[str, Any], level: str) -> Dict[str, Any]:
        """一致性维护协规则"""
        # 检查跨技能的一致性
        consistency_check = self._check_consistency_across_skills(data)
        
        return {
            "status": "consistency_checked",
            "consistent": consistency_check["consistent"],
            "inconsistencies": consistency_check["inconsistencies"]
        }
    
    def _process_feedback(self, data: Dict[str, Any], level: str) -> Dict[str, Any]:
        """反馈处理协规则"""
        feedback_data = data.get("feedback", {})
        
        # 处理反馈并更新相关状态
        processed_feedback = self._process_skill_feedback(feedback_data)
        
        return {
            "status": "feedback_processed",
            "processed_data": processed_feedback
        }
    
    def _calculate_context_alignment(self, ctx1: str, ctx2: str) -> float:
        """计算上下文对齐度"""
        if not ctx1 or not ctx2:
            return 0.0
        
        # 简单的关键词匹配算法
        words1 = set(re.findall(r'\w+', ctx1.lower()))
        words2 = set(re.findall(r'\w+', ctx2.lower()))
        
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _align_context_with_existing(self, existing_ctx: str, new_ctx: str) -> str:
        """将新上下文与现有上下文对齐"""
        # 合并现有上下文和新上下文
        if existing_ctx in new_ctx:
            return new_ctx
        if new_ctx in existing_ctx:
            return existing_ctx
        
        # 找到共同点并合并
        common_elements = self._find_common_elements(existing_ctx, new_ctx)
        if common_elements:
            return f"{common_elements}\n\n{existing_ctx}\n\n{new_ctx}"
        else:
            return f"{existing_ctx}\n\n{new_ctx}"
    
    def _calculate_goal_alignment(self, goal1: str, goal2: str) -> float:
        """计算目标对齐度"""
        # 使用简单的字符串相似度
        from difflib import SequenceMatcher
        return SequenceMatcher(None, goal1.lower(), goal2.lower()).ratio()
    
    def _align_goal_with_existing(self, existing_goal: str, new_goal: str) -> str:
        """将新目标与现有目标对齐"""
        # 检查新目标是否是现有目标的细化
        if new_goal.lower() in existing_goal.lower():
            return existing_goal
        if existing_goal.lower() in new_goal.lower():
            return new_goal
        
        # 合并目标
        return f"{existing_goal}; {new_goal}"
    
    def _extract_quality_metrics(self, result_data: Dict[str, Any]) -> Dict[str, float]:
        """提取质量指标"""
        # 从结果数据中提取质量指标
        metrics = {}
        
        # 如果结果包含质量相关字段
        if isinstance(result_data, dict):
            for key, value in result_data.items():
                if 'metric' in key.lower() or 'score' in key.lower():
                    metrics[key] = float(value) if isinstance(value, (int, float)) else 0.0
        
        return metrics
    
    def _needs_quality_improvement(self, metrics: Dict[str, float]) -> bool:
        """检查是否需要质量改进"""
        # 简单检查：如果有任何指标低于0.5
        low_metrics = [key for key, value in metrics.items() if value < 0.5]
        return len(low_metrics) > 0
    
    def _check_consistency_across_skills(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """检查跨技能的一致性"""
        inconsistencies = []
        
        # 检查数据中的关键字段是否与其他技能的输出一致
        key_fields = ['type', 'format', 'structure', 'context_key']
        
        for field in key_fields:
            if field in data:
                # 检查与其他技能输出的一致性
                pass  # 简化实现
        
        return {
            "consistent": len(inconsistencies) == 0,
            "inconsistencies": inconsistencies
        }
    
    def _find_common_elements(self, ctx1: str, ctx2: str) -> str:
        """找共同元素"""
        # 简化的共同元素识别
        lines1 = set(ctx1.split('\n'))
        lines2 = set(ctx2.split('\n'))
        
        common_lines = lines1.intersection(lines2)
        return '\n'.join(common_lines) if common_lines else ""
    
    def _process_skill_feedback(self, feedback_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理技能反馈"""
        processed = {}
        
        # 根据反馈更新相关状态
        for key, value in feedback_data.items():
            processed[f"processed_{key}"] = value
        
        return processed

# 全局认知协同中心实例
COORDINATION_CENTER = CognitiveCoordinationCenter()