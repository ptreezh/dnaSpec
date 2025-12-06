"""
命令解析器模块
负责解析和验证DSGS命令格式
"""
import re
from typing import Dict, Optional, Any


class CommandParser:
    """
    DSGS命令解析器
    解析符合/speckit.dsgs.*格式的命令
    """
    
    def __init__(self):
        # 定义命令格式的正则表达式
        # 匹配 /speckit.dsgs.{skill_name} [params] 格式
        self.pattern = r'^/speckit\.dsgs\.([a-zA-Z0-9-]+)(?:\s+(.+))?$'
    
    def parse(self, command_string: str) -> Dict[str, Any]:
        """
        解析命令字符串
        
        Args:
            command_string: 命令字符串，如 '/speckit.dsgs.architect 设计电商系统'
            
        Returns:
            解析结果字典，包含命令、技能名、参数和有效性信息
        """
        if not command_string or not command_string.startswith('/speckit.dsgs.'):
            return {
                'isValid': False,
                'error': 'Invalid command prefix',
                'command': command_string,
                'skill': None,
                'params': None
            }
        
        match = re.match(self.pattern, command_string)
        if not match:
            return {
                'isValid': False,
                'error': 'Invalid command format',
                'command': command_string,
                'skill': None,
                'params': None
            }
        
        return {
            'command': command_string,
            'skill': match.group(1),  # 技能名称
            'params': match.group(2) or '',  # 参数，如果没有则为空字符串
            'isValid': True
        }
    
    def validate(self, command_object: Dict[str, Any]) -> bool:
        """
        验证解析后的命令对象
        
        Args:
            command_object: 解析后的命令对象
            
        Returns:
            命令是否有效
        """
        return (
            command_object.get('isValid', False) and
            command_object.get('skill') is not None and
            len(command_object.get('skill', '')) > 0
        )