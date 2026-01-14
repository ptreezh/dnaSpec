"""
技能执行器模块
负责协调技能映射和Python桥接器来执行技能
"""
from .skill_mapper import SkillMapper
from .python_bridge import PythonBridge
from typing import Dict, Any


class SkillExecutor:
    """
    DNASPEC技能执行器
    协调技能映射和Python桥接来执行技能
    """
    
    def __init__(self, python_bridge: PythonBridge = None, skill_mapper: SkillMapper = None):
        """
        初始化技能执行器
        
        Args:
            python_bridge: Python桥接器实例
            skill_mapper: 技能映射器实例
        """
        self.python_bridge = python_bridge or PythonBridge()
        self.skill_mapper = skill_mapper or SkillMapper()
    
    def execute(self, skill_name: str, params: str) -> Dict[str, Any]:
        """
        执行技能
        
        Args:
            skill_name: 技能名称（如 'architect'）
            params: 技能参数
            
        Returns:
            执行结果字典
        """
        try:
            # 验证输入
            validation_result = self.validate_input(skill_name, params)
            if not validation_result['valid']:
                return {
                    'success': False,
                    'error': validation_result['error'],
                    'skill': skill_name
                }
            
            # 映射技能名称到DNASPEC技能
            dnaspec_skill_name = self.skill_mapper.map(skill_name)
            if not dnaspec_skill_name:
                return {
                    'success': False,
                    'error': f'Skill not found: {skill_name}',
                    'skill': skill_name
                }
            
            # 通过Python桥接器执行技能，传递原始技能名称用于正确映射工具名称
            result = self.python_bridge.execute_skill(dnaspec_skill_name, params, original_skill_name=skill_name)
            
            # 格式化输出
            formatted_result = {
                'success': result['success'],
                'skill': skill_name,
                'result': self.format_output(result),
                'rawResult': result
            }
            
            if not result['success']:
                formatted_result['error'] = result.get('error', 'Unknown error')
            
            return formatted_result
            
        except Exception as e:
            return {
                'success': False,
                'skill': skill_name,
                'error': str(e),
                'stack': str(e.__traceback__) if e.__traceback__ else None
            }
    
    def validate_input(self, skill_name: str, params: str) -> Dict[str, Any]:
        """
        验证输入参数
        
        Args:
            skill_name: 技能名称
            params: 参数
            
        Returns:
            验证结果字典
        """
        if not skill_name or not isinstance(skill_name, str) or len(skill_name) == 0:
            return {
                'valid': False,
                'error': 'Skill name is required and must be a non-empty string'
            }
        
        # 检查技能是否被支持
        if not self.skill_mapper.is_skill_supported(skill_name):
            return {
                'valid': False,
                'error': f'Unsupported skill: {skill_name}'
            }
        
        return {
            'valid': True,
            'error': None
        }
    
    def format_output(self, result: Dict[str, Any]) -> str:
        """
        格式化输出结果
        
        Args:
            result: 原始结果字典
            
        Returns:
            格式化的输出字符串
        """
        if result.get('success') and 'result' in result:
            raw_result = result['result']
            if isinstance(raw_result, str):
                return raw_result
            else:
                return str(raw_result)
        elif not result.get('success'):
            return f"Error: {result.get('error', 'Unknown error')}"
        else:
            return str(result)
    
    def get_available_skills(self) -> list:
        """
        获取可用技能列表
        
        Returns:
            可用技能名称列表
        """
        return self.skill_mapper.get_available_skills()
    
    def is_skill_available(self, skill_name: str) -> bool:
        """
        检查技能是否可用
        
        Args:
            skill_name: 技能名称
            
        Returns:
            技能是否可用
        """
        dnaspec_skill_name = self.skill_mapper.map(skill_name)
        if not dnaspec_skill_name:
            return False
        
        return self.python_bridge.is_skill_available(dnaspec_skill_name)