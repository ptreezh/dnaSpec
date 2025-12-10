"""
Liveness技能 - 重构版本
符合DNASPEC标准化技能接口规范
"""
from typing import Dict, Any
from ..skill_base import BaseSkill, DetailLevel


class LivenessSkill(BaseSkill):
    """Liveness技能 - 简单的存活检查技能"""
    
    def __init__(self):
        super().__init__(
            name="liveness",
            description="简单的存活检查技能，返回'alive'"
        )
    
    def _execute_skill_logic(self, input_text: str, detail_level: DetailLevel, 
                          options: Dict[str, Any], context: Dict[str, Any]) -> str:
        """执行Liveness技能逻辑"""
        return "alive"
    
    def _format_output(self, result_data: str, detail_level: DetailLevel) -> str:
        """格式化输出结果 - 对于Liveness技能，所有详细级别都返回相同结果"""
        return result_data