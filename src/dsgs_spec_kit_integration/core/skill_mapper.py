"""
技能映射器模块
负责将命令中的技能名称映射到实际的技能实现
"""
from typing import Dict, Optional


class SkillMapper:
    """
    DSGS技能映射器
    将命令中的技能名称映射到相应的DSGS技能实现
    """
    
    def __init__(self):
        # 定义技能映射关系
        self.skill_map = {
            'architect': 'dnaspec-architect',
            'agent-creator': 'dnaspec-agent-creator',
            'task-decomposer': 'dnaspec-task-decomposer',
            'constraint-generator': 'dnaspec-constraint-generator',
            'dapi-checker': 'dnaspec-dapi-checker',
            'modulizer': 'dnaspec-modulizer'
        }
    
    def map(self, skill_name: str) -> Optional[str]:
        """
        将命令中的技能名称映射到DSGS技能名称
        
        Args:
            skill_name: 命令中的技能名称（如 'architect'）
            
        Returns:
            对应的DSGS技能名称，如果不存在则返回None
        """
        return self.skill_map.get(skill_name)
    
    def register(self, custom_skill_name: str, dsgs_skill_name: str) -> None:
        """
        注册自定义技能映射
        
        Args:
            custom_skill_name: 自定义的技能名称
            dsgs_skill_name: 对应的DSGS技能名称
        """
        self.skill_map[custom_skill_name] = dsgs_skill_name
    
    def get_available_skills(self) -> list:
        """
        获取所有可用的技能名称列表
        
        Returns:
            可用技能名称列表
        """
        return list(self.skill_map.keys())
    
    def get_available_dsgs_skills(self) -> list:
        """
        获取所有可用的DSGS技能名称列表
        
        Returns:
            可用DSGS技能名称列表
        """
        return list(self.skill_map.values())
    
    def is_skill_supported(self, skill_name: str) -> bool:
        """
        检查某个技能是否被支持
        
        Args:
            skill_name: 要检查的技能名称
            
        Returns:
            技能是否被支持
        """
        return skill_name in self.skill_map