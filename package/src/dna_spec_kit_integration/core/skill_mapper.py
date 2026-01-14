"""
技能映射器模块
负责将命令中的技能名称映射到实际的技能实现
"""
from typing import Dict, Optional


class SkillMapper:
    """
    DNASPEC技能映射器
    将命令中的技能名称映射到相应的DNASPEC技能实现
    """
    
    def __init__(self):
        # 定义技能映射关系
        # 格式：'skill_name_used_in_command': 'dnaspec-module_name'
        # PythonBridge会在多个路径中查找模块：
        # 1. 标准路径: dna_spec_kit_integration.skills.{module_name}
        # 2. Claude技能路径: claude_skills.{module_name}
        # 3. 上下文工程路径: dna_context_engineering.{module_name}
        # 4. 直接路径: {module_name}
        # 现在指向Claude兼容的统一技能实现
        self.skill_map = {
            # 核心技能 - 指向Claude兼容的统一技能实现
            'architect': 'dnaspec-claude_skill',  # Claude技能实现
            'agent-creator': 'dnaspec-claude_skill',  # Claude技能实现
            'task-decomposer': 'dnaspec-claude_skill',  # Claude技能实现
            'constraint-generator': 'dnaspec-claude_skill', # Claude技能实现
            'dapi-checker': 'dnaspec-claude_skill', # Claude技能实现
            'modulizer': 'dnaspec-claude_skill', # Claude技能实现

            # 宪法治理技能 - 指向Claude兼容的实现
            'constitutional-validator': 'dnaspec-claude_skill',  # Claude技能实现
            'constitutional-enforcer': 'dnaspec-claude_skill',  # Claude技能实现

            # 临时工作空间技能 - 指向Claude兼容的实现
            'temp-workspace': 'dnaspec-claude_skill',  # Claude技能实现
            'workspace-manager': 'dnaspec-claude_skill',  # Claude技能实现

            # Git操作和项目宪法技能 - 指向Claude兼容的实现
            'git-ops': 'dnaspec-claude_skill',  # Claude技能实现
            'project-constitution': 'dnaspec-claude_skill',  # Claude技能实现

            # 协调合同技能 - 指向Claude兼容的实现
            'contract-checker': 'dnaspec-claude_skill',  # Claude技能实现
            'contract-enforcer': 'dnaspec-claude_skill',  # Claude技能实现

            # 上下文工程技能
            'context-analysis': 'dnaspec-claude_skill',  # Claude技能实现
            'context-analyzer': 'dnaspec-claude_skill',  # Claude技能实现
            'context-optimization': 'dnaspec-claude_skill',  # Claude技能实现
            'context-optimizer': 'dnaspec-claude_skill',  # Claude技能实现
            'cognitive-template': 'dnaspec-claude_skill',  # Claude技能实现
            'cognitive-templater': 'dnaspec-claude_skill',  # Claude技能实现
            'simple-architect': 'dnaspec-claude_skill',  # Claude技能实现
            'system-architect': 'dnaspec-claude_skill',  # Claude技能实现
            'api-checker': 'dnaspec-claude_skill',  # Claude技能实现
            'git-operations': 'dnaspec-claude_skill',  # Claude技能实现
            'temp-workspace-skill': 'dnaspec-claude_skill',  # Claude技能实现
            'liveness': 'dnaspec-claude_skill',  # Claude技能实现
            'dnaspec-init': 'dnaspec-claude_skill',  # DNASPEC初始化技能实现
        }
    
    def map(self, skill_name: str) -> Optional[str]:
        """
        将命令中的技能名称映射到DNASPEC技能名称
        
        Args:
            skill_name: 命令中的技能名称（如 'architect'）
            
        Returns:
            对应的DNASPEC技能名称，如果不存在则返回None
        """
        return self.skill_map.get(skill_name)
    
    def register(self, custom_skill_name: str, dnaspec_skill_name: str) -> None:
        """
        注册自定义技能映射
        
        Args:
            custom_skill_name: 自定义的技能名称
            dnaspec_skill_name: 对应的DNASPEC技能名称
        """
        self.skill_map[custom_skill_name] = dnaspec_skill_name
    
    def get_available_skills(self) -> list:
        """
        获取所有可用的技能名称列表
        
        Returns:
            可用技能名称列表
        """
        return list(self.skill_map.keys())
    
    def get_available_dnaspec_skills(self) -> list:
        """
        获取所有可用的DNASPEC技能名称列表
        
        Returns:
            可用DNASPEC技能名称列表
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