"""
CLI检测器模块
负责检测系统中安装的AI CLI工具
"""
import subprocess
import os
import shutil
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
            # 首先使用shutil.which找到完整路径，避免PATH解析问题
            exe_path = shutil.which('claude')
            if not exe_path:
                return {
                    'installed': False,
                    'error': 'Claude CLI not found in system PATH'
                }

            # 使用完整路径执行命令
            result = subprocess.run(
                [exe_path, '--version'],
                capture_output=True,
                text=True,
                timeout=15,  # 增加超时时间以防万一
                shell=(platform.system() == 'Windows')
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                install_path = exe_path

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
            # 首先使用shutil.which找到完整路径，避免PATH解析问题
            exe_path = shutil.which('gemini')
            if not exe_path:
                return {
                    'installed': False,
                    'error': 'Gemini CLI not found in system PATH'
                }

            # 使用完整路径执行命令
            result = subprocess.run(
                [exe_path, '--version'],
                capture_output=True,
                text=True,
                timeout=15,  # 增加超时时间以防万一
                shell=(platform.system() == 'Windows')
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                install_path = exe_path

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
            # 首先使用shutil.which找到完整路径，避免PATH解析问题
            exe_path = shutil.which('qwen')
            if not exe_path:
                return {
                    'installed': False,
                    'error': 'Qwen CLI not found in system PATH'
                }

            # 使用完整路径执行命令
            result = subprocess.run(
                [exe_path, '--version'],
                capture_output=True,
                text=True,
                timeout=15,  # 增加超时时间以防万一
                shell=(platform.system() == 'Windows')
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                install_path = exe_path

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
            # 首先使用shutil.which找到完整路径，避免PATH解析问题
            exe_path = shutil.which('gh')
            if not exe_path:
                return {
                    'installed': False,
                    'error': 'GitHub CLI with Copilot extension not found'
                }

            # 使用完整路径执行命令，检查copilot扩展
            result = subprocess.run(
                [exe_path, 'copilot', '--version'],
                capture_output=True,
                text=True,
                timeout=15,  # 增加超时时间以防万一
                shell=(platform.system() == 'Windows')
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                install_path = exe_path

                return {
                    'installed': True,
                    'version': version,
                    'installPath': install_path,
                    'configPath': self._get_copilot_config_path()
                }
            else:
                # 检查copilot扩展是否已安装
                check_result = subprocess.run(
                    [exe_path, 'extension', 'list'],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    shell=(platform.system() == 'Windows')
                )

                if 'copilot' in check_result.stdout.lower():
                    # copilot扩展已安装但版本命令可能不工作
                    return {
                        'installed': True,
                        'version': 'copilot extension detected',
                        'installPath': exe_path,
                        'configPath': self._get_copilot_config_path()
                    }
                else:
                    return {
                        'installed': False,
                        'error': 'Copilot extension not installed for GitHub CLI'
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
            # 首先使用shutil.which找到完整路径，避免PATH解析问题
            # Cursor可能在不同路径下，需要尝试多个可能的名称
            exe_path = None
            for cmd_name in ['cursor', 'cursor-cli', 'cursor.exe']:
                exe_path = shutil.which(cmd_name)
                if exe_path:
                    break

            if not exe_path:
                return {
                    'installed': False,
                    'error': 'Cursor CLI not found in system PATH'
                }

            # 尝试执行版本命令或帮助命令
            result = subprocess.run(
                [exe_path, '--version'],
                capture_output=True,
                text=True,
                timeout=15,  # 增加超时时间以防万一
                shell=(platform.system() == 'Windows')
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                install_path = exe_path

                return {
                    'installed': True,
                    'version': version,
                    'installPath': install_path,
                    'configPath': self._get_cursor_config_path()
                }
            else:
                # 尝试--help命令作为备选
                help_result = subprocess.run(
                    [exe_path, '--help'],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    shell=(platform.system() == 'Windows')
                )
                if help_result.returncode == 0:
                    return {
                        'installed': True,
                        'version': 'available (version check failed)',
                        'installPath': exe_path,
                        'configPath': self._get_cursor_config_path()
                    }
                else:
                    return {
                        'installed': True,  # 可执行文件存在，但版本命令可能不支持
                        'version': 'executable found but no version info',
                        'installPath': exe_path,
                        'configPath': self._get_cursor_config_path(),
                        'note': 'Cursor executable exists but may not support --version flag'
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