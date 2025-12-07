#!/usr/bin/env python3
"""
DSGS技能集成安装器
将DSGS技能安装到各种AI CLI工具的扩展目录中
"""
import os
import platform
import json
import shutil
from pathlib import Path
from typing import Dict, Any


class SkillIntegrator:
    """
    技能集成器
    将DSGS技能安装到AI CLI工具的扩展系统中
    """
    
    def __init__(self):
        self.home_dir = Path.home()
        self.os_type = platform.system().lower()
        
        # 定义各AI工具的扩展/插件目录路径
        self.extension_paths = {
            'claude': self._get_claude_extension_path(),
            'gemini': self._get_gemini_extension_path(), 
            'qwen': self._get_qwen_plugin_path(),
            'copilot': self._get_copilot_extension_path(),
            'cursor': self._get_cursor_extension_path()
        }
    
    def _get_claude_extension_path(self) -> str:
        """获取Claude扩展路径"""
        if self.os_type == 'windows':
            return str(self.home_dir / '.config' / 'claude' / 'skills')
        else:
            return str(self.home_dir / '.config' / 'claude' / 'skills')
    
    def _get_gemini_extension_path(self) -> str:
        """获取Gemini扩展路径"""  
        if self.os_type == 'windows':
            return str(self.home_dir / '.local' / 'share' / 'gemini' / 'extensions')
        else:
            return str(self.home_dir / '.local' / 'share' / 'gemini' / 'extensions')
    
    def _get_qwen_plugin_path(self) -> str:
        """获取Qwen插件路径"""
        if self.os_type == 'windows':
            return str(self.home_dir / '.qwen' / 'plugins')
        else:
            return str(self.home_dir / '.qwen' / 'plugins')
    
    def _get_copilot_extension_path(self) -> str:
        """获取Copilot扩展路径"""
        if self.os_type == 'windows':
            return str(self.home_dir / '.config' / 'gh-copilot')
        else:
            return str(self.home_dir / '.config' / 'gh-copilot')
    
    def _get_cursor_extension_path(self) -> str:
        """获取Cursor扩展路径"""
        if self.os_type == 'windows':
            return str(self.home_dir / '.cursor')
        else:
            return str(self.home_dir / '.cursor')
    
    def install_skills_to_all_platforms(self) -> Dict[str, Any]:
        """将技能安装到所有已检测到的AI CLI平台"""
        from src.dsgs_spec_kit_integration.core.cli_detector import CliDetector
        detector = CliDetector()
        detected_tools = detector.detect_all()
        
        results = {}
        
        for tool_name, tool_info in detected_tools.items():
            if tool_info.get('installed', False):
                print(f"🔧 安装DSGS技能到 {tool_name}...")
                results[tool_name] = self.install_skills_to_platform(tool_name, tool_info)
            else:
                results[tool_name] = {
                    'success': False,
                    'message': 'Tool not installed'
                }
        
        return {
            'success': True,
            'installation_results': results,
            'installed_count': sum(1 for r in results.values() if r.get('success', False)),
            'target_count': len([t for t, i in detected_tools.items() if i.get('installed')])
        }
    
    def install_skills_to_platform(self, platform_name: str, platform_info: Dict[str, Any]) -> Dict[str, Any]:
        """将技能安装到特定平台"""
        extension_path = self.extension_paths.get(platform_name)
        if not extension_path:
            return {
                'success': False,
                'error': f'Unsupported platform: {platform_name}'
            }
        
        # 确保扩展目录存在
        try:
            os.makedirs(extension_path, exist_ok=True)
        except Exception as e:
            return {
                'success': False,
                'error': f'Could not create extension directory: {e}'
            }
        
        # 创建DSGS技能定义
        dsgs_skills = self._get_dsgs_skill_definitions()
        
        # 根据平台类型安装技能
        if platform_name == 'claude':
            result = self._install_claude_skills(extension_path, dsgs_skills)
        elif platform_name == 'qwen':
            result = self._install_qwen_plugins(extension_path, dsgs_skills)  
        elif platform_name in ['gemini', 'copilot', 'cursor']:
            result = self._install_generic_skills(extension_path, platform_name, dsgs_skills)
        else:
            result = self._install_generic_skills(extension_path, platform_name, dsgs_skills)
        
        return result
    
    def _get_dsgs_skill_definitions(self) -> Dict[str, Any]:
        """获取DSGS技能定义"""
        return {
            'context-analysis': {
                'name': 'dsgs-context-analysis',
                'description': 'Analyze context quality across 5 dimensions',
                'command': '/speckit.dsgs.context-analysis',
                'category': 'context-engineering',
                'version': '1.0.4',
                'handler': 'dsgs_context_engineering.skills_system_final.execute'
            },
            'context-optimization': {
                'name': 'dsgs-context-optimization', 
                'description': 'Optimize context quality with specific goals',
                'command': '/speckit.dsgs.context-optimization',
                'category': 'context-engineering',
                'version': '1.0.4',
                'handler': 'dsgs_context_engineering.skills_system_final.execute'
            },
            'cognitive-template': {
                'name': 'dsgs-cognitive-template',
                'description': 'Apply cognitive templates to structure reasoning',
                'command': '/speckit.dsgs.cognitive-template',
                'category': 'cognitive-engineering',
                'version': '1.0.4', 
                'handler': 'dsgs_context_engineering.skills_system_final.execute'
            },
            'architect': {
                'name': 'dsgs-architect',
                'description': 'System architecture design expert',
                'command': '/speckit.dsgs.architect',
                'category': 'system-design',
                'version': '1.0.4',
                'handler': 'dsgs_context_engineering.skills_system_final.execute'
            }
        }
    
    def _install_claude_skills(self, extension_path: str, skills: Dict[str, Any]) -> Dict[str, Any]:
        """为Claude安装技能"""
        try:
            claude_skills_dir = Path(extension_path)
            os.makedirs(claude_skills_dir, exist_ok=True)
            
            # 创建Claude技能文件
            for skill_name, skill_def in skills.items():
                skill_file = claude_skills_dir / f"{skill_def['name']}.json"
                
                claude_skill_spec = {
                    'name': skill_def['name'],
                    'description': skill_def['description'],
                    'command': skill_def['command'],
                    'version': skill_def['version'],
                    'specification': {
                        'type': 'dsks',
                        'version': '1.0',
                        'implementation': {
                            'module': 'dsgs_context_engineering.skills_system_final',
                            'function': 'execute'
                        }
                    }
                }
                
                with open(skill_file, 'w', encoding='utf-8') as f:
                    json.dump(claude_skill_spec, f, ensure_ascii=False, indent=2)
            
            return {
                'success': True,
                'installed_skills': list(skills.keys()),
                'extension_path': str(claude_skills_dir),
                'message': f'Installed {len(skills)} skills to Claude'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _install_qwen_plugins(self, plugin_path: str, skills: Dict[str, Any]) -> Dict[str, Any]:
        """为Qwen安装插件"""
        try:
            qwen_plugins_dir = Path(plugin_path)
            os.makedirs(qwen_plugins_dir, exist_ok=True)
            
            # 创建Qwen插件定义
            for skill_name, skill_def in skills.items():
                plugin_file = qwen_plugins_dir / f"{skill_def['name']}.json"
                
                qwen_plugin_spec = {
                    'name': skill_def['name'],
                    'description': skill_def['description'],
                    'version': skill_def['version'],
                    'type': 'function_call',
                    'api': {
                        'name': skill_def['command'],
                        'arguments': {
                            'context': {
                                'type': 'string',
                                'description': 'The context to analyze/optimize/process'
                            }
                        }
                    },
                    'instructions': f"When user uses {skill_def['command']}, call the DSGS {skill_name} skill.",
                    'created_at': self._get_timestamp()
                }
                
                with open(plugin_file, 'w', encoding='utf-8') as f:
                    json.dump(qwen_plugin_spec, f, ensure_ascii=False, indent=2)
            
            return {
                'success': True,
                'installed_plugins': list(skills.keys()),
                'plugin_path': str(qwen_plugins_dir),
                'message': f'Installed {len(skills)} plugins to Qwen'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _install_generic_skills(self, extension_path: str, platform_name: str, skills: Dict[str, Any]) -> Dict[str, Any]:
        """为通用平台安装技能"""
        try:
            generic_ext_dir = Path(extension_path)
            os.makedirs(generic_ext_dir, exist_ok=True)
            
            # 创建通用扩展配置
            config_file = generic_ext_dir / 'dsks-config.json'
            
            config = {
                'platform': platform_name,
                'extension_type': 'dsks',
                'version': '1.0.4',
                'installed_skills': skills,
                'activation': {
                    'commands': [skill['command'] for skill in skills.values()],
                    'prefixes': ['/speckit.dsgs.']
                },
                'settings': {
                    'enable_context_analysis': True,
                    'enable_optimization': True,
                    'enable_templates': True
                },
                'installed_at': self._get_timestamp()
            }
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            return {
                'success': True,
                'installed_skills': list(skills.keys()),
                'config_path': str(config_file),
                'message': f'Configured {len(skills)} skills for {platform_name}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def verify_installation(self, platform_name: str = None) -> Dict[str, Any]:
        """验证安装结果"""
        if platform_name:
            extension_path = self.extension_paths.get(platform_name)
            if not extension_path or not os.path.exists(extension_path):
                return {
                    'success': False,
                    'platform': platform_name,
                    'error': f'Extension path does not exist: {extension_path}'
                }
            
            installed_files = os.listdir(extension_path)
            return {
                'success': len(installed_files) > 0,
                'platform': platform_name,
                'files_count': len(installed_files),
                'files': installed_files,
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
                    except:
                        results[platform] = {
                            'success': False,
                            'error': 'Could not access extension path',
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
    """主函数 - 安装DSGS技能到AI CLI工具"""
    print("🚀 DSGS Skills Integration Installer")
    print("="*50)
    print("Installing DSGS Context Engineering Skills to AI CLI platforms...")
    print()
    
    integrator = SkillIntegrator()
    
    # 检查各平台扩展路径
    print("🔍 Checking AI CLI platform extension directories:")
    for platform, path in integrator.extension_paths.items():
        exists = os.path.exists(path)
        status = "✅" if exists else "❌"
        print(f"  {status} {platform}: {path}")
    
    print()
    
    # 安装技能
    print("🔧 Installing DSGS skills to detected platforms...")
    results = integrator.install_skills_to_all_platforms()
    
    print()
    print("📊 Installation Results:")
    for platform, result in results['installation_results'].items():
        status = "✅" if result.get('success', False) else "❌"
        message = result.get('message', result.get('error', 'Unknown'))
        print(f"  {status} {platform}: {message}")
    
    print()
    print(f"✅ Successfully installed to {results['installed_count']}/{results['target_count']} platforms")
    
    # 验证安装
    print("\n🔍 Verifying installations...")
    verification = integrator.verify_installation()
    
    print("\nVerification Summary:")
    for platform, ver_result in verification['verification_results'].items():
        status = "✅" if ver_result.get('success', False) else "❌"
        path = ver_result.get('extension_path', 'Unknown')
        count = ver_result.get('files_count', 0)
        print(f"  {status} {platform}: {count} files in {path}")
    
    print("\n🎉 DSGS Skills installation completed!")
    print("The /speckit.dsgs.* commands should now be available in your AI CLI tools.")
    
    return results


if __name__ == "__main__":
    main()