"""
spec.kit适配器基类
提供与GitHub spec.kit工具包集成的基础功能
"""
import shutil
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod


class SpecKitAdapter(ABC):
    """spec.kit适配器基类"""
    
    SUPPORTED_AGENTS = [
        'claude', 'gemini', 'qwen', 'copilot',
        'cursor', 'windsurf', 'opencode', 'codex'
    ]
    
    REQUIRED_DEPENDENCIES = ['git', 'python']
    
    def __init__(self):
        self.supported_agents = self.SUPPORTED_AGENTS.copy()
        self.command_prefix = "/speckit.dnaspec."
        self.is_initialized = False
        self._registered_skills = {}  # 注册的技能存储
    
    def check_dependencies(self) -> Dict[str, bool]:
        """检查系统依赖"""
        results = {}
        
        for dep in self.REQUIRED_DEPENDENCIES:
            results[dep] = self._check_dependency(dep)
        
        return results
    
    def _check_dependency(self, dependency: str) -> bool:
        """检查单个依赖"""
        return shutil.which(dependency) is not None
    
    def is_agent_supported(self, agent_name: str) -> bool:
        """检查指定代理是否被支持"""
        return agent_name.lower() in [agent.lower() for agent in self.supported_agents]
    
    def get_supported_agents(self) -> List[str]:
        """获取支持的AI代理列表"""
        return self.supported_agents.copy()
    
    def parse_command(self, command: str) -> Optional[Dict[str, Any]]:
        """解析spec.kit命令并提取技能信息"""
        if not command or not command.startswith(self.command_prefix):
            return None
        
        # 提取技能名称和参数
        remaining = command[len(self.command_prefix):].strip()
        if ' ' in remaining:
            skill_name, params = remaining.split(' ', 1)
            params = params.strip()
        else:
            skill_name = remaining
            params = ""
        
        return {
            'skill_name': f"dnaspec-{skill_name}",
            'params': params,
            'original_command': command
        }
    
    def map_command_to_skill(self, command: str) -> Optional[str]:
        """将命令映射到DNASPEC技能名称"""
        parsed = self.parse_command(command)
        if parsed:
            return parsed['skill_name']
        return None
    
    def register_skill(self, skill_name: str, skill_callable: callable) -> bool:
        """注册技能到适配器"""
        if not skill_name or not callable(skill_callable):
            return False
        
        self._registered_skills[skill_name] = skill_callable
        return True
    
    def is_skill_registered(self, skill_name: str) -> bool:
        """检查技能是否已注册"""
        return skill_name in self._registered_skills
    
    def get_registered_skills(self) -> List[str]:
        """获取已注册的技能列表"""
        return list(self._registered_skills.keys())
    
    @abstractmethod
    def execute_skill(self, skill_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行映射的DNASPEC技能 - 子类必须实现"""
        pass
    
    def execute_command(self, command: str) -> Dict[str, Any]:
        """执行完整的命令（解析+映射+执行）"""
        # 解析命令
        parsed = self.parse_command(command)
        if not parsed:
            return {
                'success': False,
                'error': 'Invalid command format',
                'original_command': command
            }
        
        # 获取技能名称和参数
        skill_name = parsed['skill_name']
        params = parsed['params']
        
        # 检查技能是否注册
        if not self.is_skill_registered(skill_name):
            return {
                'success': False,
                'error': f'Skill not registered: {skill_name}',
                'skill_name': skill_name,
                'params': params
            }
        
        # 执行技能
        try:
            result = self.execute_skill(skill_name, {'params': params})
            return {
                'success': True,
                'result': result,
                'skill_name': skill_name,
                'original_command': command
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'skill_name': skill_name,
                'params': params
            }
    
    def initialize(self) -> bool:
        """初始化适配器"""
        dependencies_ok = all(self.check_dependencies().values())
        if dependencies_ok:
            self.is_initialized = True
        return self.is_initialized
    
    def get_adapter_info(self) -> Dict[str, Any]:
        """获取适配器信息"""
        return {
            'name': self.__class__.__name__,
            'supported_agents': self.get_supported_agents(),
            'command_prefix': self.command_prefix,
            'is_initialized': self.is_initialized,
            'dependencies': self.check_dependencies(),
            'registered_skills_count': len(self._registered_skills),
            'registered_skills': self.get_registered_skills()
        }