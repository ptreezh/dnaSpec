"""
记忆配置加载器
"""
import json
from pathlib import Path
from typing import Dict, Any


class MemoryConfigLoader:
    """加载和管理记忆配置"""

    def __init__(self, config_path: str = "config/memory_config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")

        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_skill_config(self, skill_name: str):
        """
        获取技能的配置

        Args:
            skill_name: 技能名称 (如 'task-decomposer')

        Returns:
            配置字典
        """
        skill_settings = self.config.get('skills', {}).get(skill_name, {})

        return {
            'enabled': skill_settings.get('enabled', False),
            'max_short_term': skill_settings.get('max_short_term', 50),
            'max_long_term': skill_settings.get('max_long_term', 200),
            'auto_cleanup': skill_settings.get('auto_cleanup', True),
            'storage_path': Path(self.config['storage']['path'])
        }

    def get_storage_path(self) -> Path:
        """获取存储路径"""
        return Path(self.config['storage']['path'])

    def get_backup_path(self) -> Path:
        """获取备份路径"""
        return Path(self.config['storage']['backup_path'])

    def is_skill_enabled(self, skill_name: str) -> bool:
        """检查技能是否启用记忆"""
        return self.config.get('skills', {}).get(skill_name, {}).get('enabled', False)

    def list_enabled_skills(self) -> list:
        """列出启用记忆的技能"""
        enabled = []
        for skill_name, settings in self.config.get('skills', {}).items():
            if settings.get('enabled', False):
                enabled.append(skill_name)
        return enabled

    def get_global_settings(self) -> Dict[str, Any]:
        """获取全局设置"""
        return self.config.get('global_settings', {})
