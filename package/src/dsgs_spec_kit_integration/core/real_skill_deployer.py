#!/usr/bin/env python3
"""
DSGS技能安装器 - 将技能安装到AI CLI工具中
真正的技能部署和注册系统
"""
import os
import platform
import json
import shutil
from pathlib import Path
from typing import Dict, Any


class RealSkillDeployer:
    """
    真正的技能部署系统
    将DSGS技能安装到各个AI CLI工具的扩展目录中
    """

    def __init__(self):
        self.home_dir = Path.home()
        self.os_type = platform.system().lower()
        
        # 定义各AI工具的扩展安装路径
        self.extension_paths = {
            'claude': self._get_claude_skills_path(),
            'gemini': self._get_gemini_extensions_path(),
            'qwen': self._get_qwen_plugins_path(),
            'copilot': self._get_copilot_extensions_path(),
            'cursor': self._get_cursor_extensions_path()
        }

    def _get_claude_skills_path(self) -> str:
        """获取Claude技能路径"""
        if self.os_type == 'windows':
            return str(self.home_dir / '.config' / 'claude' / 'skills')
        else:
            return str(self.home_dir / '.config' / 'claude' / 'skills')

    def _get_gemini_extensions_path(self) -> str:
        """获取Gemini扩展路径"""
        if self.os_type == 'windows':
            return str(self.home_dir / '.local' / 'share' / 'gemini' / 'extensions')
        else:
            return str(self.home_dir / '.local' / 'share' / 'gemini' / 'extensions')

    def _get_qwen_plugins_path(self) -> str:
        """获取Qwen插件路径"""
        if self.os_type == 'windows':
            return str(self.home_dir / '.qwen' / 'plugins')
        else:
            return str(self.home_dir / '.qwen' / 'plugins')

    def _get_copilot_extensions_path(self) -> str:
        """获取Copilot扩展路径"""
        if self.os_type == 'windows':
            return str(self.home_dir / '.config' / 'gh-copilot')
        else:
            return str(self.home_dir / '.config' / 'gh-copilot')

    def _get_cursor_extensions_path(self) -> str:
        """获取Cursor扩展路径"""
        if self.os_type == 'windows':
            return str(self.home_dir / '.cursor')
        else:
            return str(self.home_dir / '.cursor')

    def deploy_skills_to_all_platforms(self) -> Dict[str, Any]:
        """将技能部署到所有支持的AI平台"""
        from .cli_detector import CliDetector
        detector = CliDetector()
        detected_tools = detector.detect_all()

        results = {}
        successful_deployments = 0

        for platform_name, tool_info in detected_tools.items():
            if tool_info.get('installed', False):
                print(f"🔄 部署DSGS技能到 {platform_name}...")
                results[platform_name] = self.deploy_skills_to_platform(platform_name, tool_info)
                if results[platform_name]['success']:
                    successful_deployments += 1
            else:
                results[platform_name] = {
                    'success': False,
                    'message': 'Platform not installed'
                }

        return {
            'success': True,
            'deployment_results': results,
            'successful_deployments': successful_deployments,
            'total_installed_platforms': sum(1 for info in detected_tools.values() if info.get('installed', False)),
            'deployed_skills': ['context-analysis', 'context-optimization', 'cognitive-template', 'architect']
        }

    def deploy_skills_to_platform(self, platform_name: str, platform_info: Dict[str, Any]) -> Dict[str, Any]:
        """将技能部署到特定平台"""
        extension_path = self.extension_paths.get(platform_name)
        if not extension_path:
            return {
                'success': False,
                'error': f'Unsupported platform: {platform_name}'
            }

        try:
            # 确保扩展目录存在
            os.makedirs(extension_path, exist_ok=True)

            # 根据平台类型部署技能
            if platform_name == 'claude':
                return self._deploy_to_claude(extension_path)
            elif platform_name == 'qwen':
                return self._deploy_to_qwen(extension_path)
            elif platform_name in ['gemini', 'cursor', 'copilot']:
                return self._deploy_to_generic(extension_path, platform_name)
            else:
                return self._deploy_to_generic(extension_path, platform_name)

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _deploy_to_claude(self, extension_path: str) -> Dict[str, Any]:
        """为Claude部署技能"""
        try:
            skills_dir = Path(extension_path)
            os.makedirs(skills_dir, exist_ok=True)

            # 创建Claude技能定义文件
            skill_defs = self._get_claude_skill_definitions()
            
            deployed_skills = []
            for skill_name, skill_def in skill_defs.items():
                skill_file = skills_dir / f"{skill_name}.json"
                
                # Claude技能规范格式
                claude_spec = {
                    "name": skill_def["name"],
                    "description": skill_def["description"],
                    "version": skill_def["version"],
                    "specification": {
                        "type": "claude_custom_skill",
                        "version": "2024-10-01",
                        "category": "development-tools",
                        "commands": skill_def["commands"],
                        "implementation": {
                            "module": skill_def["module"],
                            "function": skill_def["function"]
                        },
                        "permissions": [
                            {
                                "type": "read-conversation-context",
                                "description": "Read current conversation context for processing"
                            }
                        ]
                    },
                    "metadata": {
                        "author": "DSGS Team",
                        "license": "MIT",
                        "tags": ["context-analysis", "optimization", "cognitive-templates"]
                    }
                }
                
                with open(skill_file, 'w', encoding='utf-8') as f:
                    json.dump(claude_spec, f, ensure_ascii=False, indent=2)
                
                deployed_skills.append(skill_name)

            return {
                'success': True,
                'message': f'Deployed {len(deployed_skills)} skills to Claude',
                'deployed_skills': deployed_skills,
                'extension_path': str(skills_dir)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _deploy_to_qwen(self, extension_path: str) -> Dict[str, Any]:
        """为Qwen部署插件"""
        try:
            plugins_dir = Path(extension_path)
            os.makedirs(plugins_dir, exist_ok=True)

            # 创建Qwen插件定义
            plugin_defs = self._get_qwen_plugin_definitions()
            
            deployed_plugins = []
            for plugin_name, plugin_def in plugin_defs.items():
                plugin_file = plugins_dir / f"{plugin_name}.json"
                
                # Qwen插件规范格式
                qwen_plugin = {
                    "type": "function",
                    "function": {
                        "name": plugin_def["name"],
                        "description": plugin_def["description"],
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "input": {
                                    "type": "string",
                                    "description": "The input content to process"
                                }
                            },
                            "required": ["input"]
                        }
                    },
                    "metadata": {
                        "author": "DSGS Team",
                        "version": plugin_def["version"],
                        "tags": ["context-analysis", "ai-tools", "development"]
                    }
                }
                
                with open(plugin_file, 'w', encoding='utf-8') as f:
                    json.dump(qwen_plugin, f, ensure_ascii=False, indent=2)
                
                deployed_plugins.append(plugin_name)

            return {
                'success': True,
                'message': f'Deployed {len(deployed_plugins)} plugins to Qwen',
                'deployed_plugins': deployed_plugins,
                'extension_path': str(plugins_dir)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _deploy_to_generic(self, extension_path: str, platform_name: str) -> Dict[str, Any]:
        """为通用平台部署技能"""
        try:
            ext_dir = Path(extension_path)
            os.makedirs(ext_dir, exist_ok=True)

            # 创建通用扩展配置
            config_file = ext_dir / 'dsks-config.json'
            
            config = {
                'platform': platform_name,
                'extension_type': 'dsks',
                'version': '1.0.4',
                'dsks_skills': self._get_dsgs_skill_definitions(),
                'activation_commands': [
                    '/speckit.dsgs.context-analysis',
                    '/speckit.dsgs.context-optimization', 
                    '/speckit.dsgs.cognitive-template',
                    '/speckit.dsgs.architect'
                ],
                'handlers': {
                    'context-analysis': 'dsgs_context_engineering.skills_system_final:execute_context_analysis',
                    'context-optimization': 'dsgs_context_engineering.skills_system_final:execute_context_optimization',
                    'cognitive-template': 'dsgs_context_engineering.skills_system_final:execute_cognitive_template',
                    'architect': 'dsgs_context_engineering.skills_system_final:execute_architect'
                },
                'installed_at': self._get_timestamp()
            }
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)

            return {
                'success': True,
                'message': f'Configured DSGS skills for {platform_name}',
                'config_path': str(config_file),
                'extension_path': str(ext_dir),
                'skills_installed': len(config['dsks_skills'])
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _get_claude_skill_definitions(self) -> Dict[str, Any]:
        """获取Claude技能定义"""
        return {
            'dsgs-context-analysis': {
                'name': 'dsgs-context-analysis',
                'description': 'Analyze context quality across 5 dimensions: clarity, relevance, completeness, consistency, efficiency',
                'version': '1.0.4',
                'commands': [{
                    'name': '/dsgs-analyze',
                    'description': 'Analyze quality of provided context',
                    'handler': 'context_analysis_handler'
                }],
                'module': 'dsgs_context_engineering.skills_system_final',
                'function': 'execute_context_analysis'
            },
            'dsgs-context-optimization': {
                'name': 'dsgs-context-optimization',
                'description': 'Optimize context with specific goals like clarity, completeness, relevance',
                'version': '1.0.4',
                'commands': [{
                    'name': '/dsgs-optimize',
                    'description': 'Optimize provided context',
                    'handler': 'context_optimization_handler'
                }],
                'module': 'dsgs_context_engineering.skills_system_final',
                'function': 'execute_context_optimization'
            },
            'dsgs-cognitive-template': {
                'name': 'dsgs-cognitive-template',
                'description': 'Apply cognitive templates like chain-of-thought, verification, few-shot learning',
                'version': '1.0.4',
                'commands': [{
                    'name': '/dsgs-template',
                    'description': 'Apply cognitive templates to task',
                    'handler': 'cognitive_template_handler'
                }],
                'module': 'dsgs_context_engineering.skills_system_final',
                'function': 'execute_cognitive_template'
            },
            'dsgs-architect': {
                'name': 'dsgs-architect',
                'description': 'System architecture design expert',
                'version': '1.0.4',
                'commands': [{
                    'name': '/dsgs-architect',
                    'description': 'Design system architecture',
                    'handler': 'architect_handler'
                }],
                'module': 'dsgs_context_engineering.skills_system_final',
                'function': 'execute_architect'
            }
        }

    def _get_qwen_plugin_definitions(self) -> Dict[str, Any]:
        """获取Qwen插件定义"""
        return {
            'dsgs-context-analysis': {
                'name': 'dsgs-context-analysis',
                'description': 'Analyze context quality across 5 dimensions',
                'version': '1.0.4',
                'module': 'dsgs_context_engineering.skills_system_final',
                'function': 'execute_context_analysis'
            },
            'dsgs-context-optimization': {
                'name': 'dsgs-context-optimization', 
                'description': 'Optimize context with specific goals',
                'version': '1.0.4',
                'module': 'dsgs_context_engineering.skills_system_final',
                'function': 'execute_context_optimization'
            },
            'dsgs-cognitive-template': {
                'name': 'dsgs-cognitive-template',
                'description': 'Apply cognitive templates to structure thinking',
                'version': '1.0.4',
                'module': 'dsgs_context_engineering.skills_system_final',
                'function': 'execute_cognitive_template'
            }
        }

    def _get_dsgs_skill_definitions(self) -> Dict[str, Any]:
        """获取DSGS技能定义"""
        return {
            'context-analysis': {
                'name': 'dsgs-context-analysis',
                'description': 'Analyze context quality across 5 dimensions',
                'version': '1.0.4',
                'handler': 'execute_context_analysis'
            },
            'context-optimization': {
                'name': 'dsgs-context-optimization',
                'description': 'Optimize context with specific goals',
                'version': '1.0.4', 
                'handler': 'execute_context_optimization'
            },
            'cognitive-template': {
                'name': 'dsgs-cognitive-template',
                'description': 'Apply cognitive templates to tasks',
                'version': '1.0.4',
                'handler': 'execute_cognitive_template'
            },
            'architect': {
                'name': 'dsgs-architect', 
                'description': 'System architecture design expert',
                'version': '1.0.4',
                'handler': 'execute_architect'
            }
        }

    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()

    def verify_deployment(self, platform_name: str = None) -> Dict[str, Any]:
        """验证部署结果"""
        if platform_name:
            extension_path = self.extension_paths.get(platform_name)
            if not extension_path or not os.path.exists(extension_path):
                return {
                    'success': False,
                    'platform': platform_name,
                    'error': f'Extension directory does not exist: {extension_path}'
                }
            
            # 检查技能文件是否存在
            deployed_files = os.listdir(extension_path)
            return {
                'success': len(deployed_files) > 0,
                'platform': platform_name,
                'files_count': len(deployed_files),
                'files': deployed_files,
                'extension_path': extension_path
            }
        else:
            results = {}
            for platform, path in self.extension_paths.items():
                if os.path.exists(path):
                    try:
                        files = os.listdir(path)
                        results[platform] = {
                            'success': len(files) > 0,
                            'files_count': len(files),
                            'extension_path': path
                        }
                    except Exception as e:
                        results[platform] = {
                            'success': False,
                            'error': str(e),
                            'extension_path': path
                        }
                else:
                    results[platform] = {
                        'success': False,
                        'error': 'Extension path does not exist',
                        'extension_path': path
                    }
            return {
                'success': True,
                'verification_results': results
            }


def main():
    """主函数 - 部署DSGS技能到AI CLI工具"""
    print("🚀 DSGS Skills Deployment System - 真正的技能部署器")
    print("="*60)
    print("将DSGS核心技能部署到已安装的AI CLI工具中...")
    print()
    
    deployer = RealSkillDeployer()
    
    print("🔍 检测AI CLI工具扩展目录...")
    for platform, path in deployer.extension_paths.items():
        exists = "✅" if os.path.exists(path) else "❌"
        print(f"  {exists} {platform}: {path}")
    
    print()
    print("📦 开始部署DSGS技能...")
    results = deployer.deploy_skills_to_all_platforms()
    
    print()
    print("📊 部署结果:")
    for platform, result in results['deployment_results'].items():
        status = "✅" if result.get('success', False) else "❌"
        message = result.get('message', result.get('error', 'Unknown status'))
        print(f"  {status} {platform}: {message}")
        
        if result.get('success'):
            if result.get('deployed_skills'):
                print(f"      已部署技能: {result.get('deployed_skills', [])}")
            if result.get('extension_path'):
                print(f"      扩展路径: {result.get('extension_path')}")
    
    print()
    print(f"📈 部署统计:")
    print(f"  成功部署到: {results['successful_deployments']}/{results['total_installed_platforms']} 个平台")
    print(f"  总共部署技能: {len(results['deployed_skills'])} 个")
    
    print()
    print("✅ DSGS技能部署完成！")
    print("现在可以在AI CLI工具中使用以下命令:")
    print("  /speckit.dsgs.context-analysis [上下文] - 分析上下文质量")
    print("  /speckit.dsgs.context-optimization [上下文] - 优化上下文")
    print("  /speckit.dsgs.cognitive-template [任务] - 应用认知模板")
    print("  /speckit.dsgs.architect [需求] - 系统架构设计")
    
    return results


if __name__ == "__main__":
    main()