"""
平台工具模块
提供跨平台兼容性功能
"""
import os
import sys
import platform
from pathlib import Path
from typing import Dict, Any, Optional


class PlatformUtils:
    """
    跨平台工具类
    提供跨平台兼容性功能
    """
    
    @staticmethod
    def get_platform() -> str:
        """
        获取当前平台名称
        
        Returns:
            平台名称字符串
        """
        return platform.system().lower()
    
    @staticmethod
    def is_windows() -> bool:
        """
        检查是否为Windows平台
        
        Returns:
            是否为Windows平台
        """
        return PlatformUtils.get_platform() == 'windows'
    
    @staticmethod
    def is_mac() -> bool:
        """
        检查是否为macOS平台
        
        Returns:
            是否为macOS平台
        """
        return PlatformUtils.get_platform() == 'darwin'
    
    @staticmethod
    def is_linux() -> bool:
        """
        检查是否为Linux平台
        
        Returns:
            是否为Linux平台
        """
        return PlatformUtils.get_platform() == 'linux'
    
    @staticmethod
    def get_user_home() -> str:
        """
        获取用户主目录路径
        
        Returns:
            用户主目录路径字符串
        """
        return os.path.expanduser("~")
    
    @staticmethod
    def get_standard_paths() -> Dict[str, str]:
        """
        获取标准目录路径
        
        Returns:
            标准目录路径字典
        """
        home = PlatformUtils.get_user_home()
        
        if PlatformUtils.is_windows():
            return {
                'config': os.path.join(home, '.dnaspec'),
                'temp': os.environ.get('TEMP', os.environ.get('TMP', 'C:\\temp')),
                'data': os.path.join(home, 'AppData', 'Local', 'dnaspec')
            }
        else:
            return {
                'config': os.path.join(home, '.dnaspec'),
                'temp': '/tmp',
                'data': os.path.join(home, '.local', 'share', 'dnaspec')
            }
    
    @staticmethod
    def get_config_path(platform_name: str) -> str:
        """
        获取特定平台的配置路径
        
        Args:
            platform_name: 平台名称
            
        Returns:
            配置路径字符串
        """
        home = PlatformUtils.get_user_home()
        standard_paths = PlatformUtils.get_standard_paths()
        
        platform_paths = {
            'claude': os.path.join(home, '.config', 'claude', 'skills') if not PlatformUtils.is_windows()
                    else os.path.join(home, '.config', 'claude', 'skills'),
            'gemini': os.path.join(home, '.local', 'share', 'gemini', 'extensions') if not PlatformUtils.is_windows()
                    else os.path.join(home, '.local', 'share', 'gemini', 'extensions'),
            'qwen': os.path.join(home, '.qwen', 'plugins') if not PlatformUtils.is_windows()
                  else os.path.join(home, '.qwen', 'plugins'),
            'copilot': os.path.join(home, '.config', 'gh-copilot') if not PlatformUtils.is_windows()
                     else os.path.join(home, '.config', 'gh-copilot'),
            'cursor': os.path.join(home, '.cursor') if not PlatformUtils.is_windows()
                     else os.path.join(home, '.cursor')
        }
        
        return platform_paths.get(platform_name, standard_paths['config'])
    
    @staticmethod
    def check_permissions(file_path: str) -> Dict[str, bool]:
        """
        检查文件权限
        
        Args:
            file_path: 文件路径
            
        Returns:
            权限信息字典
        """
        try:
            path_obj = Path(file_path)
            return {
                'readable': os.access(file_path, os.R_OK),
                'writable': os.access(file_path, os.W_OK),
                'executable': os.access(file_path, os.X_OK),
                'exists': path_obj.exists()
            }
        except:
            return {
                'readable': False,
                'writable': False,
                'executable': False,
                'exists': False
            }
    
    @staticmethod
    def ensure_directory_exists(dir_path: str) -> bool:
        """
        确保目录存在，如果不存在则创建
        
        Args:
            dir_path: 目录路径
            
        Returns:
            创建是否成功
        """
        try:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f'Failed to create directory {dir_path}: {str(e)}')
            return False
    
    @staticmethod
    def copy_file_with_backup(source: str, destination: str) -> bool:
        """
        复制文件并在目标存在时创建备份
        
        Args:
            source: 源文件路径
            destination: 目标文件路径
            
        Returns:
            复制是否成功
        """
        import shutil
        import datetime
        
        try:
            dest_path = Path(destination)
            
            # 创建备份（如果目标文件存在）
            if dest_path.exists():
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"{destination}.backup.{timestamp}"
                shutil.copy2(destination, backup_path)
                print(f'Backup created: {backup_path}')
            
            # 复制文件
            shutil.copy2(source, destination)
            return True
        except Exception as e:
            print(f'Failed to copy file: {str(e)}')
            return False
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """
        检查文件是否存在
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件是否存在
        """
        return Path(file_path).exists()
    
    @staticmethod
    def ensure_path_separators(path: str) -> str:
        """
        确保路径分隔符正确（跨平台兼容）
        
        Args:
            path: 原始路径
            
        Returns:
            标准化路径
        """
        if PlatformUtils.is_windows():
            # Windows使用反斜杠，但Python会自动处理
            return os.path.normpath(path)
        else:
            return os.path.normpath(path)
    
    @staticmethod
    def get_executable_extension() -> str:
        """
        获取可执行文件扩展名
        
        Returns:
            可执行文件扩展名
        """
        if PlatformUtils.is_windows():
            return '.exe'
        else:
            return ''
    
    @staticmethod
    def get_path_separator() -> str:
        """
        获取路径分隔符
        
        Returns:
            路径分隔符
        """
        return os.sep
    
    @staticmethod
    def normalize_path(path: str) -> str:
        """
        标准化路径格式
        
        Args:
            path: 原始路径
            
        Returns:
            标准化路径
        """
        return os.path.normpath(path)
    
    @staticmethod
    def is_path_absolute(path: str) -> bool:
        """
        检查路径是否为绝对路径
        
        Args:
            path: 路径字符串
            
        Returns:
            路径是否为绝对路径
        """
        return os.path.isabs(path)