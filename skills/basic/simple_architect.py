"""
Simple Architect技能 - 重构版本
符合DNASPEC标准化技能接口规范
"""
from typing import Dict, Any
from ..skill_base import BaseSkill, DetailLevel


class SimpleArchitectSkill(BaseSkill):
    """Simple Architect技能 - 生成简单的文本架构图"""
    
    def __init__(self):
        super().__init__(
            name="simple-architect",
            description="根据输入的需求描述，生成一个简单的文本架构图"
        )
        
        # 架构映射表
        self.architecture_map = {
            "电商": "[WebApp] -> [API Server] -> [Database]",
            "博客": "[WebApp] -> [Database]",
        }
    
    def _execute_skill_logic(self, input_text: str, detail_level: DetailLevel, 
                          options: Dict[str, Any], context: Dict[str, Any]) -> str:
        """执行Simple Architect技能逻辑"""
        description = input_text.lower()
        
        # 检查关键字匹配
        for keyword, architecture in self.architecture_map.items():
            if keyword in description:
                return architecture
        
        # 检查更广泛的匹配
        if "电商" in description or "电子商务" in description:
            return "[WebApp] -> [API Server] -> [Database]"
        elif "博客" in description or "blog" in description:
            return "[WebApp] -> [Database]"
        
        # 没有匹配的架构
        return ""
    
    def _format_output(self, result_data: str, detail_level: DetailLevel) -> str:
        """格式化输出结果 - 对于Simple Architect技能，所有详细级别都返回相同结果"""
        return result_data