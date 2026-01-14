"""
配置生成器模块
根据检测结果生成DNASPEC配置文件
"""
import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigGenerator:
    """
    DNASPEC配置生成器
    根据检测到的CLI工具生成配置文件
    """
    
    def __init__(self):
        self.default_config = {
            'version': '1.0.0',
            'createdAt': None,
            'platforms': [],
            'skills': self._get_default_skills(),
            'settings': {
                'autoUpdate': True,
                'verboseLogging': False,
                'maxRetries': 3
            }
        }
    
    def generate(self, detected_tools: Dict[str, Any]) -> Dict[str, Any]:
        """
        根据检测到的工具生成配置
        
        Args:
            detected_tools: 检测到的工具字典
            
        Returns:
            生成的配置字典
        """
        import datetime
        config = self.default_config.copy()
        config['createdAt'] = datetime.datetime.now().isoformat()
        
        # 根据检测结果配置平台
        for platform_name, tool_info in detected_tools.items():
            if tool_info.get('installed', False):
                platform_config = {
                    'name': platform_name,
                    'enabled': True,
                    'version': tool_info.get('version', 'unknown'),
                    'installPath': tool_info.get('installPath'),
                    'configPath': tool_info.get('configPath'),
                    'skills': self._get_platform_skills(platform_name)
                }
                config['platforms'].append(platform_config)
        
        return config
    
    def save(self, config: Dict[str, Any], file_path: str) -> bool:
        """
        保存配置到文件
        
        Args:
            config: 配置字典
            file_path: 文件路径
            
        Returns:
            保存是否成功
        """
        try:
            # 确保目录存在
            directory = os.path.dirname(file_path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True, indent=2)
            
            return True
        except Exception as e:
            print(f'Failed to save config: {str(e)}')
            return False
    
    def load(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        从文件加载配置
        
        Args:
            file_path: 文件路径
            
        Returns:
            配置字典或None
        """
        try:
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f'Failed to load config: {str(e)}')
            return None
    
    def validate(self, config: Dict[str, Any]) -> bool:
        """
        验证配置结构
        
        Args:
            config: 配置字典
            
        Returns:
            配置是否有效
        """
        if not config:
            return False
        
        required_fields = ['version', 'platforms', 'skills']
        for field in required_fields:
            if field not in config:
                return False
        
        if not isinstance(config['platforms'], list):
            return False
        
        return True
    
    def _get_default_skills(self) -> Dict[str, Any]:
        """
        获取默认技能配置
        
        Returns:
            默认技能配置字典
        """
        return {
            'architect': {
                'command': '/speckit.dnaspec.architect',
                'description': '系统架构设计专家',
                'enabled': True
            },
            'agent-creator': {
                'command': '/speckit.dnaspec.agent-creator',
                'description': '智能体创建专家',
                'enabled': True
            },
            'task-decomposer': {
                'command': '/speckit.dnaspec.task-decomposer',
                'description': '任务分解专家',
                'enabled': True
            },
            'constraint-generator': {
                'command': '/speckit.dnaspec.constraint-generator',
                'description': '约束生成专家',
                'enabled': True
            },
            'dapi-checker': {
                'command': '/speckit.dnaspec.dapi-checker',
                'description': '接口检查专家',
                'enabled': True
            },
            'modulizer': {
                'command': '/speckit.dnaspec.modulizer',
                'description': '模块化专家',
                'enabled': True
            }
        }
    
    def _get_platform_skills(self, platform_name: str) -> Dict[str, Any]:
        """
        获取特定平台的技能配置
        
        Args:
            platform_name: 平台名称
            
        Returns:
            平台特定的技能配置
        """
        platform_skills = {
            'claude': {
                'skillPath': 'skills/',
                'template': 'claude-skill-template.json'
            },
            'gemini': {
                'skillPath': 'extensions/',
                'template': 'gemini-extension-template.yaml'
            },
            'qwen': {
                'skillPath': 'plugins/',
                'template': 'qwen-plugin-template.json'
            },
            'copilot': {
                'skillPath': 'copilot-skills/',
                'template': 'copilot-skill-template.json'
            },
            'cursor': {
                'skillPath': 'cursor-extensions/',
                'template': 'cursor-extension-template.json'
            }
        }
        
        return platform_skills.get(platform_name, {})