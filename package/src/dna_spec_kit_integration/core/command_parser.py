"""
命令解析器模块
负责解析和验证DNASPEC命令格式
"""
import re
from typing import Dict, Optional, Any


class CommandParser:
    """
    DNASPEC命令解析器
    解析符合/speckit.dnaspec.*格式的命令
    """
    
    def __init__(self):
        # 定义命令格式的正则表达式
        # 匹配 /dnaspec.{skill_name} [params] 格式 (优先格式)
        # 以及 /speckit.dnaspec.{skill_name} [params] 格式 (兼容格式)
        self.primary_pattern = r'^/dnaspec\.([a-zA-Z0-9-]+)(?:\s+(.+))?$'
        self.compatibility_pattern = r'^/speckit\.dnaspec\.([a-zA-Z0-9-]+)(?:\s+(.+))?$'
    
    def parse(self, command_string: str) -> Dict[str, Any]:
        """
        解析命令字符串

        Args:
            command_string: 命令字符串，如 '/dnaspec.architect 设计电商系统' 或 '/speckit.dnaspec.architect 设计电商系统'

        Returns:
            解析结果字典，包含命令、技能名、参数和有效性信息
        """
        # 首先检查主格式 /dnaspec.*
        if command_string and command_string.startswith('/dnaspec.'):
            match = re.match(self.primary_pattern, command_string)
            if match:
                return {
                    'command': command_string,
                    'skill': match.group(1),  # 技能名称
                    'params': match.group(2) or '',  # 参数，如果没有则为空字符串
                    'isValid': True
                }

        # 如果不是主格式，检查兼容格式 /speckit.dnaspec.*
        elif command_string and command_string.startswith('/speckit.dnaspec.'):
            match = re.match(self.compatibility_pattern, command_string)
            if match:
                return {
                    'command': command_string,
                    'skill': match.group(1),  # 技能名称
                    'params': match.group(2) or '',  # 参数，如果没有则为空字符串
                    'isValid': True
                }

        # 两个格式都不匹配
        return {
            'isValid': False,
            'error': 'Invalid command prefix. Use /dnaspec.{skill} or /speckit.dnaspec.{skill}',
            'command': command_string,
            'skill': None,
            'params': None
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