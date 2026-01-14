"""
Qwen CLI适配器
为Qwen CLI工具提供DNASPEC技能集成支持
"""
import json
import os
from typing import Dict, Any, List
from pathlib import Path


class QwenCliAdapter:
    """
    Qwen CLI适配器
    将DNASPEC技能转换为Qwen CLI插件格式
    """
    
    def __init__(self, skills_directory: str = None):
        """
        初始化Qwen CLI适配器
        
        Args:
            skills_directory: 技能目录路径
        """
        self.skills_directory = skills_directory or str(Path.home() / '.qwen' / 'plugins')
        self.supported_skills = [
            'context-analysis',
            'context-optimization', 
            'cognitive-template',
            'system-architect',
            'simple-architect'
        ]
    
    def generate_qwen_plugin_manifest(self, skill_name: str, skill_description: str) -> Dict[str, Any]:
        """
        生成Qwen插件清单文件
        
        Args:
            skill_name: 技能名称
            skill_description: 技能描述
            
        Returns:
            Qwen插件清单字典
        """
        return {
            "type": "function",
            "function": {
                "name": f"dnaspec-{skill_name}",
                "description": skill_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "input": {
                            "type": "string",
                            "description": "The input content to process"
                        },
                        "detail_level": {
                            "type": "string",
                            "enum": ["basic", "standard", "detailed"],
                            "description": "Level of detail for the response",
                            "default": "standard"
                        }
                    },
                    "required": ["input"]
                }
            },
            "metadata": {
                "author": "DNASPEC Team",
                "version": "1.0.4",
                "tags": ["context-analysis", "ai-tools", "development"],
                "skill_name": skill_name
            }
        }
    
    def deploy_skill_to_qwen(self, skill_name: str, skill_description: str) -> Dict[str, Any]:
        """
        将技能部署到Qwen CLI
        
        Args:
            skill_name: 技能名称
            skill_description: 技能描述
            
        Returns:
            部署结果字典
        """
        try:
            # 确保插件目录存在
            plugins_dir = Path(self.skills_directory)
            plugins_dir.mkdir(parents=True, exist_ok=True)
            
            # 生成插件清单
            plugin_manifest = self.generate_qwen_plugin_manifest(skill_name, skill_description)
            
            # 保存插件清单文件
            plugin_file = plugins_dir / f"dnaspec-{skill_name}.json"
            with open(plugin_file, 'w', encoding='utf-8') as f:
                json.dump(plugin_manifest, f, ensure_ascii=False, indent=2)
            
            # 生成或更新Qwen CLI配置文件
            config_file = plugins_dir / 'dnaspec_config.json'
            self._update_qwen_config(config_file, skill_name, plugin_file)
            
            return {
                'success': True,
                'message': f'Successfully deployed {skill_name} to Qwen CLI',
                'plugin_file': str(plugin_file),
                'config_file': str(config_file)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _update_qwen_config(self, config_file: Path, skill_name: str, plugin_file: Path):
        """
        更新Qwen CLI配置文件
        
        Args:
            config_file: 配置文件路径
            skill_name: 技能名称
            plugin_file: 插件文件路径
        """
        # 如果配置文件不存在，创建新的
        if not config_file.exists():
            config = {
                "dnaspec_skills": {},
                "last_updated": self._get_timestamp()
            }
        else:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        
        # 更新技能配置
        config["dnaspec_skills"][skill_name] = {
            "plugin_file": str(plugin_file),
            "enabled": True,
            "registered_at": self._get_timestamp()
        }
        
        config["last_updated"] = self._get_timestamp()
        
        # 保存配置文件
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def deploy_all_skills(self) -> Dict[str, Any]:
        """
        部署所有支持的技能到Qwen CLI
        
        Returns:
            批量部署结果字典
        """
        skill_descriptions = {
            'context-analysis': 'Analyze context quality across 5 dimensions: clarity, relevance, completeness, consistency, efficiency',
            'context-optimization': 'Optimize context with specific goals like clarity, completeness, relevance',
            'cognitive-template': 'Apply cognitive templates like chain-of-thought, verification, few-shot learning',
            'system-architect': 'System architecture design expert for complex projects',
            'simple-architect': 'Simple architecture design for general applications'
        }
        
        results = {}
        successful_deployments = 0
        
        for skill_name in self.supported_skills:
            description = skill_descriptions.get(skill_name, f'{skill_name} skill from DNASPEC')
            result = self.deploy_skill_to_qwen(skill_name, description)
            results[skill_name] = result
            
            if result.get('success'):
                successful_deployments += 1
        
        return {
            'success': True,
            'deployment_results': results,
            'successful_deployments': successful_deployments,
            'total_skills': len(self.supported_skills)
        }
    
    def verify_deployment(self) -> Dict[str, Any]:
        """
        验证Qwen CLI技能部署状态
        
        Returns:
            验证结果字典
        """
        plugins_dir = Path(self.skills_directory)
        
        if not plugins_dir.exists():
            return {
                'success': False,
                'error': f'Qwen plugins directory does not exist: {self.skills_directory}'
            }
        
        # 检查插件文件
        deployed_skills = []
        missing_skills = []
        
        for skill_name in self.supported_skills:
            plugin_file = plugins_dir / f"dnaspec-{skill_name}.json"
            if plugin_file.exists():
                deployed_skills.append(skill_name)
            else:
                missing_skills.append(skill_name)
        
        return {
            'success': len(deployed_skills) > 0,
            'deployed_skills': deployed_skills,
            'missing_skills': missing_skills,
            'plugins_directory': str(plugins_dir),
            'total_deployed': len(deployed_skills),
            'total_expected': len(self.supported_skills)
        }
    
    def remove_skill_from_qwen(self, skill_name: str) -> Dict[str, Any]:
        """
        从Qwen CLI移除技能
        
        Args:
            skill_name: 技能名称
            
        Returns:
            移除结果字典
        """
        try:
            # 删除插件文件
            plugin_file = Path(self.skills_directory) / f"dnaspec-{skill_name}.json"
            if plugin_file.exists():
                plugin_file.unlink()
            
            # 更新配置文件
            config_file = Path(self.skills_directory) / 'dnaspec_config.json'
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                if skill_name in config.get("dnaspec_skills", {}):
                    del config["dnaspec_skills"][skill_name]
                    config["last_updated"] = self._get_timestamp()
                    
                    with open(config_file, 'w', encoding='utf-8') as f:
                        json.dump(config, f, ensure_ascii=False, indent=2)
            
            return {
                'success': True,
                'message': f'Successfully removed {skill_name} from Qwen CLI'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_qwen_cli_info(self) -> Dict[str, Any]:
        """
        获取Qwen CLI信息
        
        Returns:
            Qwen CLI信息字典
        """
        return {
            'plugins_directory': self.skills_directory,
            'supported_skills': self.supported_skills,
            'adapter_version': '1.0.4',
            'required_qwen_version': '>=2.0.0'
        }


def main():
    """主函数 - Qwen CLI适配器命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Qwen CLI Adapter for DNASPEC Skills')
    parser.add_argument('--action', choices=['deploy', 'deploy-all', 'verify', 'remove'], 
                       required=True, help='Action to perform')
    parser.add_argument('--skill', help='Skill name for deploy/remove actions')
    parser.add_argument('--description', help='Skill description for deploy action')
    parser.add_argument('--plugins-dir', help='Qwen plugins directory path')
    
    args = parser.parse_args()
    
    # 创建适配器实例
    adapter = QwenCliAdapter(args.plugins_dir)
    
    if args.action == 'deploy':
        if not args.skill:
            print("Error: --skill is required for deploy action")
            return
        
        description = args.description or f'{args.skill} skill from DNASPEC'
        result = adapter.deploy_skill_to_qwen(args.skill, description)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.action == 'deploy-all':
        result = adapter.deploy_all_skills()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.action == 'verify':
        result = adapter.verify_deployment()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.action == 'remove':
        if not args.skill:
            print("Error: --skill is required for remove action")
            return
        
        result = adapter.remove_skill_from_qwen(args.skill)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()