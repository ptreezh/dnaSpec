"""
Python桥接器模块
负责调用Python实现的DSGS技能
"""
import importlib
import sys
from typing import Dict, Any, Optional
from pathlib import Path


class PythonBridge:
    """
    Python桥接器
    负责调用Python实现的DSGS技能
    """
    
    def __init__(self, skills_base_path: Optional[str] = None):
        """
        初始化Python桥接器
        
        Args:
            skills_base_path: 技能模块的基础路径
        """
        self.skills_base_path = skills_base_path or "src.dsgs_spec_kit_integration.skills"
        self._imported_modules = {}
    
    def execute_skill(self, skill_name: str, params: str) -> Dict[str, Any]:
        """
        执行Python技能
        
        Args:
            skill_name: 技能名称（如 'dsgs-architect'）
            params: 技能参数
            
        Returns:
            执行结果字典
        """
        try:
            # 将技能名称规范化为模块名称
            # 例如 'dsgs-architect' -> 'architect'
            module_name = skill_name.replace('dsgs-', '')
            
            # 构建完整的模块路径
            full_module_path = f"{self.skills_base_path}.{module_name}"
            
            # 动态导入技能模块
            if full_module_path not in self._imported_modules:
                try:
                    module = importlib.import_module(full_module_path)
                    self._imported_modules[full_module_path] = module
                except ImportError as e:
                    return {
                        'success': False,
                        'error': f'Failed to import skill module {full_module_path}: {str(e)}',
                        'skill': skill_name
                    }
            
            module = self._imported_modules[full_module_path]
            
            # 验证模块是否包含execute函数
            if not hasattr(module, 'execute'):
                return {
                    'success': False,
                    'error': f'Skill module {full_module_path} does not have execute function',
                    'skill': skill_name
                }
            
            # 准备参数字典
            args = {'description': params} if params else {}
            
            # 执行技能
            result = module.execute(args)
            
            return {
                'success': True,
                'result': result,
                'skill': skill_name,
                'raw_result': result
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'skill': skill_name,
                'stack': str(e.__traceback__) if e.__traceback__ else None
            }
    
    def execute_skill_with_json_params(self, skill_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        使用JSON参数执行Python技能
        
        Args:
            skill_name: 技能名称
            params: JSON参数字典
            
        Returns:
            执行结果字典
        """
        try:
            # 将参数转换为字符串（如果需要）
            params_str = params.get('description', '') if isinstance(params, dict) else str(params)
            
            return self.execute_skill(skill_name, params_str)
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'skill': skill_name,
                'stack': str(e.__traceback__) if e.__traceback__ else None
            }
    
    def is_skill_available(self, skill_name: str) -> bool:
        """
        检查技能是否可用
        
        Args:
            skill_name: 技能名称
            
        Returns:
            技能是否可用
        """
        try:
            module_name = skill_name.replace('dsgs-', '')
            full_module_path = f"{self.skills_base_path}.{module_name}"
            
            # 尝试导入模块
            spec = importlib.util.find_spec(full_module_path)
            return spec is not None
        except:
            return False