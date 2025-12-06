"""
命令处理器模块
负责处理完整的命令流程：解析 -> 映射 -> 执行
"""
from .command_parser import CommandParser
from .skill_executor import SkillExecutor
from typing import Dict, Any


class CommandHandler:
    """
    DSGS命令处理器
    处理完整的命令流程：解析 -> 映射 -> 执行
    """
    
    def __init__(self, command_parser: CommandParser = None, skill_executor: SkillExecutor = None):
        """
        初始化命令处理器
        
        Args:
            command_parser: 命令解析器实例
            skill_executor: 技能执行器实例
        """
        self.command_parser = command_parser or CommandParser()
        self.skill_executor = skill_executor or SkillExecutor()
    
    def handle_command(self, command_string: str) -> Dict[str, Any]:
        """
        处理命令字符串
        
        Args:
            command_string: 完整的命令字符串，如 '/speckit.dsgs.architect 设计电商系统'
            
        Returns:
            处理结果字典
        """
        # 解析命令
        parsed_command = self.command_parser.parse(command_string)
        if not parsed_command['isValid']:
            return {
                'success': False,
                'error': parsed_command.get('error', 'Invalid command'),
                'originalCommand': command_string
            }
        
        # 执行技能
        return self.skill_executor.execute(
            parsed_command['skill'],
            parsed_command['params']
        )
    
    def get_available_commands(self) -> list:
        """
        获取可用命令列表
        
        Returns:
            可用命令描述列表
        """
        skills = self.skill_executor.get_available_skills()
        commands = []
        
        for skill in skills:
            # 将技能名称转换为更友好的描述
            descriptions = {
                'architect': '系统架构设计',
                'agent-creator': '智能体创建',
                'task-decomposer': '任务分解',
                'constraint-generator': '约束生成',
                'dapi-checker': '接口检查',
                'modulizer': '模块化'
            }
            
            description = descriptions.get(skill, f'{skill}功能')
            commands.append(f'/speckit.dsgs.{skill} [参数] - {description}')
        
        return commands
    
    def is_command_valid(self, command_string: str) -> bool:
        """
        检查命令是否格式有效（不执行）
        
        Args:
            command_string: 命令字符串
            
        Returns:
            命令格式是否有效
        """
        parsed_command = self.command_parser.parse(command_string)
        return parsed_command['isValid']
    
    def parse_command_info(self, command_string: str) -> Dict[str, Any]:
        """
        解析命令并返回详细信息（不执行）
        
        Args:
            command_string: 命令字符串
            
        Returns:
            命令解析信息
        """
        parsed = self.command_parser.parse(command_string)
        if parsed['isValid']:
            # 检查技能是否可用
            is_available = self.skill_executor.is_skill_available(parsed['skill'])
            parsed['skillAvailable'] = is_available
        
        return parsed