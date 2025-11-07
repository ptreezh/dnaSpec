"""
CLI检测器模块
负责检测系统中安装的AI CLI工具
"""
import subprocess
import os
from typing import Dict, Any, Optional
import platform


class CliDetector:
    """
    AI CLI工具检测器
    检测系统中安装的各种AI CLI工具
    """
    
    def __init__(self):
        self.detectors = {
            'claude': self.detect_claude,
            'gemini': self.detect_gemini,
            'qwen': self.detect_qwen,
            'copilot': self.detect_copilot,
            'cursor': self.detect_cursor
        }
    
    def detect_claude(self) -> Dict[str, Any]:
        """
        检测Claude CLI是否安装
        
        Returns:
            检测结果字典
        """
        try:
            result = subprocess.run(
                ['claude', '--version'], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                version = result.stdout.strip()
                install_path = self._get_install_path('claude')
                
                return {
                    'installed': True,
                    'version': version,
                    'installPath': install_path,
                    'configPath': self._get_claude_config_path()
                }
            else:
                return {
                    'installed': False,
                    'error': result.stderr.strip() if result.stderr else 'Unknown error'
                }
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return {
                'installed': False,
                'error': 'Claude CLI not found in system PATH'
            }
        except Exception as e:
            return {
                'installed': False,
                'error': str(e)
            }
    
    def detect_gemini(self) -> Dict[str, Any]:
        """
        检测Gemini CLI是否安装
        
        Returns:
            检测结果字典
        """
        try:
            result = subprocess.run(
                ['gemini', '--version'], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                version = result.stdout.strip()
                install_path = self._get_install_path('gemini')
                
                return {
                    'installed': True,
                    'version': version,
                    'installPath': install_path,
                    'configPath': self._get_gemini_config_path()
                }
            else:
                return {
                    'installed': False,
                    'error': result.stderr.strip() if result.stderr else 'Unknown error'
                }
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return {
                'installed': False,
                'error': 'Gemini CLI not found in system PATH'
            }
        except Exception as e:
            return {
                'installed': False,
                'error': str(e)
            }
    
    def detect_qwen(self) -> Dict[str, Any]:
        """
        检测Qwen CLI是否安装
        
        Returns:
            检测结果字典
        """
        try:
            result = subprocess.run(
                ['qwen', '--version'], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                version = result.stdout.strip()
                install_path = self._get_install_path('qwen')
                
                return {
                    'installed': True,
                    'version': version,
                    'installPath': install_path,
                    'configPath': self._get_qwen_config_path()
                }
            else:
                return {
                    'installed': False,
                    'error': result.stderr.strip() if result.stderr else 'Unknown error'
                }
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return {
                'installed': False,
                'error': 'Qwen CLI not found in system PATH'
            }
        except Exception as e:
            return {
                'installed': False,
                'error': str(e)
            }
    
    def detect_copilot(self) -> Dict[str, Any]:
        """
        检测Copilot CLI是否安装
        
        Returns:
            检测结果字典
        """
        try:
            result = subprocess.run(
                ['gh', 'copilot', '--version'], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                version = result.stdout.strip()
                install_path = self._get_install_path('gh')
                
                return {
                    'installed': True,
                    'version': version,
                    'installPath': install_path,
                    'configPath': self._get_copilot_config_path()
                }
            else:
                return {
                    'installed': False,
                    'error': result.stderr.strip() if result.stderr else 'Unknown error'
                }
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return {
                'installed': False,
                'error': 'GitHub CLI with Copilot extension not found'
            }
        except Exception as e:
            return {
                'installed': False,
                'error': str(e)
            }
    
    def detect_cursor(self) -> Dict[str, Any]:
        """
        检测Cursor CLI是否安装
        
        Returns:
            检测结果字典
        """
        try:
            # Cursor通常没有命令行版本，这里检查是否有相关命令
            result = subprocess.run(
                ['cursor', '--version'], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                version = result.stdout.strip()
                install_path = self._get_install_path('cursor')
                
                return {
                    'installed': True,
                    'version': version,
                    'installPath': install_path,
                    'configPath': self._get_cursor_config_path()
                }
            else:
                # 尝试其他可能的命令
                for cmd in ['cursor', 'cursor-cli']:
                    try:
                        result = subprocess.run(
                            [cmd, '--help'], 
                            capture_output=True, 
                            text=True, 
                            timeout=5
                        )
                        if result.returncode == 0:
                            install_path = self._get_install_path(cmd)
                            return {
                                'installed': True,
                                'version': 'Unknown',
                                'installPath': install_path,
                                'configPath': self._get_cursor_config_path()
                            }
                    except FileNotFoundError:
                        continue
                
                return {
                    'installed': False,
                    'error': result.stderr.strip() if result.stderr else 'Unknown error'
                }
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return {
                'installed': False,
                'error': 'Cursor CLI not found in system PATH'
            }
        except Exception as e:
            return {
                'installed': False,
                'error': str(e)
            }
    
    def detect_all(self) -> Dict[str, Any]:
        """
        检测所有支持的CLI工具
        
        Returns:
            所有检测结果字典
        """
        results = {}
        
        for name, detector in self.detectors.items():
            try:
                results[name] = detector()
            except Exception as e:
                results[name] = {
                    'installed': False,
                    'error': str(e)
                }
        
        return results
    
    def _get_install_path(self, cli_name: str) -> Optional[str]:
        """
        获取CLI工具的安装路径
        
        Args:
            cli_name: CLI工具名称
            
        Returns:
            安装路径或None
        """
        try:
            result = subprocess.run(
                ['where' if platform.system() == 'Windows' else 'which', cli_name], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0]  # 取第一个路径
            return None
        except:
            return None
    
    def _get_claude_config_path(self) -> str:
        """
        获取Claude配置路径
        
        Returns:
            配置路径字符串
        """
        home = os.path.expanduser("~")
        if platform.system() == "Windows":
            return os.path.join(home, ".config", "claude", "skills")
        else:
            return os.path.join(home, ".config", "claude", "skills")
    
    def _get_gemini_config_path(self) -> str:
        """
        获取Gemini配置路径
        
        Returns:
            配置路径字符串
        """
        home = os.path.expanduser("~")
        if platform.system() == "Windows":
            return os.path.join(home, ".local", "share", "gemini", "extensions")
        else:
            return os.path.join(home, ".local", "share", "gemini", "extensions")
    
    def _get_qwen_config_path(self) -> str:
        """
        获取Qwen配置路径
        
        Returns:
            配置路径字符串
        """
        home = os.path.expanduser("~")
        if platform.system() == "Windows":
            return os.path.join(home, ".qwen", "plugins")
        else:
            return os.path.join(home, ".qwen", "plugins")
    
    def _get_copilot_config_path(self) -> str:
        """
        获取Copilot配置路径
        
        Returns:
            配置路径字符串
        """
        home = os.path.expanduser("~")
        if platform.system() == "Windows":
            return os.path.join(home, ".config", "gh-copilot")
        else:
            return os.path.join(home, ".config", "gh-copilot")
    
    def _get_cursor_config_path(self) -> str:
        """
        获取Cursor配置路径
        
        Returns:
            配置路径字符串
        """
        home = os.path.expanduser("~")
        if platform.system() == "Windows":
            return os.path.join(home, ".cursor")
        else:
            return os.path.join(home, ".cursor")