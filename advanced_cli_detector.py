#!/usr/bin/env python3
"""
高级AI CLI工具检测器 - 基于第一性原理的多环境适配检测
从操作系统层面检测AI工具的各种可能安装位置
"""
import os
import platform
import subprocess
import shutil
from typing import Dict, Any, List, Optional


class AdvancedAICLIDetector:
    """
    高级AI CLI工具检测器
    采用多策略检测方法，适应不同环境和安装方式
    """
    
    def __init__(self):
        self.os_type = platform.system().lower()
        self.system_path = os.environ.get('PATH', '')
        
        # 定义各种AI工具的可能名称和路径模式
        self.ai_tools = {
            'claude': {
                'executables': ['claude', 'claude-cli'],
                'common_paths': self._get_common_paths('claude'),
                'version_command': ['--version']
            },
            'gemini': {
                'executables': ['gemini', 'google-gemini'],
                'common_paths': self._get_common_paths('gemini'),
                'version_command': ['--version']
            },
            'qwen': {
                'executables': ['qwen', 'tongyi'],
                'common_paths': self._get_common_paths('qwen'),
                'version_command': ['--version']
            },
            'copilot': {
                'executables': ['gh', 'copilot'],  # GitHub CLI with copilot extension
                'common_paths': self._get_common_paths('copilot'),
                'version_command': ['copilot', '--version']
            },
            'cursor': {
                'executables': ['cursor'],
                'common_paths': self._get_common_paths('cursor'),
                'version_command': ['--version']
            }
        }
    
    def _get_common_paths(self, tool_name: str) -> List[str]:
        """获取特定工具的常见安装路径"""
        if self.os_type == 'windows':
            return [
                # npm全局安装路径
                r'C:\npm_global',
                r'C:\Users\*\AppData\Roaming\npm',
                r'C:\Users\*\AppData\Local\Microsoft\WinGet\Packages',
                # 用户本地安装路径
                os.path.expanduser('~\\AppData\\Roaming\\npm'),
                os.path.expanduser('~\\AppData\\Local\\npm-cache'),
                # 全局程序路径
                r'C:\Program Files',
                r'C:\Program Files (x86)',
                # 自定义安装路径
                os.path.expanduser('~\\bin'),
                os.path.expanduser('~\\.local\\bin')
            ]
        elif self.os_type == 'darwin':  # macOS
            return [
                '/usr/local/bin',
                '/opt/homebrew/bin',
                os.path.expanduser('~/bin'),
                os.path.expanduser('~/.local/bin'),
                os.path.expanduser('/Applications'),
                '/Applications'
            ]
        else:  # Linux and others
            return [
                '/usr/local/bin',
                '/usr/bin',
                os.path.expanduser('~/bin'),
                os.path.expanduser('~/.local/bin'),
                '/opt/bin'
            ]
    
    def detect_tool_advanced(self, tool_name: str) -> Dict[str, Any]:
        """
        高级检测工具安装状态
        使用多策略方法检测工具是否存在
        """
        tool_config = self.ai_tools.get(tool_name)
        if not tool_config:
            return {'installed': False, 'error': f'Unknown tool: {tool_name}'}
        
        # 策略1: 使用shutil.which检测PATH中的可执行文件
        for exe_name in tool_config['executables']:
            exe_path = shutil.which(exe_name)
            if exe_path:
                try:
                    # 尝试执行版本命令
                    result = subprocess.run(
                        [exe_name] + tool_config['version_command'],
                        capture_output=True,
                        text=True,
                        timeout=15,
                        shell=(self.os_type == 'windows')
                    )
                    
                    if result.returncode == 0:
                        return {
                            'installed': True,
                            'version': result.stdout.strip(),
                            'installPath': exe_path,
                            'configPath': self._get_config_path(tool_name),
                            'method': 'which_detection'
                        }
                    else:
                        # 即使版本命令失败，也说明工具存在
                        return {
                            'installed': True,
                            'version': 'unknown',
                            'installPath': exe_path,
                            'configPath': self._get_config_path(tool_name),
                            'method': 'which_detection_no_version',
                            'stderr': result.stderr.strip() if result.stderr else ''
                        }
                except Exception as e:
                    # 工具存在但执行失败
                    return {
                        'installed': True,
                        'version': 'unknown',
                        'installPath': exe_path,
                        'configPath': self._get_config_path(tool_name),
                        'method': 'which_detection_exception',
                        'error': str(e)
                    }
        
        # 策略2: 搜索常见安装路径
        for path_pattern in tool_config['common_paths']:
            try:
                if '*' in path_pattern:
                    # 处理通配符路径
                    import glob
                    matching_paths = glob.glob(path_pattern)
                    for actual_path in matching_paths:
                        if self._check_path_for_tool(actual_path, tool_config):
                            return self._construct_result(True, tool_name, actual_path, 'glob_search')
                else:
                    if self._check_path_for_tool(path_pattern, tool_config):
                        return self._construct_result(True, tool_name, path_pattern, 'common_path')
            except Exception:
                continue  # 忽略无法访问的路径
        
        # 策略3: 系统特定的检测方法
        result = self._system_specific_detection(tool_name)
        if result and result.get('installed', False):
            return result
        
        # 所有策略都失败
        return {'installed': False, 'method': 'all_strategies_failed'}
    
    def _check_path_for_tool(self, directory: str, tool_config: Dict[str, Any]) -> bool:
        """检查目录中是否存在工具"""
        try:
            if os.path.exists(directory) and os.path.isdir(directory):
                for exe_name in tool_config['executables']:
                    exe_path = os.path.join(directory, exe_name)
                    exe_cmd_path = exe_path + '.cmd' if self.os_type == 'windows' else exe_path + '.exe'
                    
                    if os.path.isfile(exe_path) and os.access(exe_path, os.X_OK):
                        return True
                    elif os.path.isfile(exe_cmd_path) and os.access(exe_cmd_path, os.X_OK):
                        return True
        except Exception:
            pass
        return False
    
    def _construct_result(self, installed: bool, tool_name: str, path: str, method: str) -> Dict[str, Any]:
        """构建检测结果"""
        result = {
            'installed': installed,
            'installPath': path,
            'configPath': self._get_config_path(tool_name),
            'method': method
        }
        
        if installed:
            try:
                # 尝试获取版本 (使用检测到的路径)
                tool_exec = shutil.which(tool_name) or path
                if tool_exec:
                    # 尝试获取版本信息
                    tool_config = self.ai_tools[tool_name]
                    version_result = subprocess.run(
                        [tool_exec] + tool_config['version_command'],
                        capture_output=True,
                        text=True,
                        timeout=10,
                        shell=(self.os_type == 'windows')
                    )
                    if version_result.returncode == 0:
                        result['version'] = version_result.stdout.strip()
                        
            except Exception:
                result['version'] = 'unknown'
        
        return result
    
    def _system_specific_detection(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """系统特定的检测方法"""
        if tool_name == 'cursor' and self.os_type == 'windows':
            # Windows上的Cursor可能安装在特定位置
            cursor_paths = [
                r'C:\Users\*\AppData\Local\Programs\cursor\resources\app\bin\cursor',
                r'E:\cursor\resources\app\bin\cursor',  # 您的安装位置
                os.path.expanduser('~\\AppData\\Local\\Programs\\cursor\\resources\\app\\bin\\cursor')
            ]
            
            import glob
            for path_pattern in cursor_paths:
                matches = glob.glob(path_pattern)
                for match in matches:
                    if os.path.isfile(match + '.exe') or os.path.isfile(match + '.cmd'):
                        return self._construct_result(True, tool_name, match, 'cursor_windows_specific')
        
        elif tool_name == 'copilot':
            # Copilot通过GitHub CLI扩展安装
            gh_path = shutil.which('gh')
            if gh_path:
                try:
                    # 检查copilot扩展是否安装
                    result = subprocess.run(
                        ['gh', 'extension', 'list'],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if 'copilot' in result.stdout.lower():
                        return self._construct_result(True, tool_name, gh_path, 'copilot_extension')
                except:
                    pass
        
        return None
    
    def _get_config_path(self, tool_name: str) -> str:
        """获取工具配置路径"""
        home = os.path.expanduser("~")
        
        config_paths = {
            'claude': os.path.join(home, '.config', 'claude'),
            'gemini': os.path.join(home, '.config', 'google-gemini'),
            'qwen': os.path.join(home, '.qwen'),
            'copilot': os.path.join(home, '.config', 'github-copilot'),
            'cursor': os.path.join(home, '.cursor')
        }
        
        return config_paths.get(tool_name, os.path.join(home, f'.{tool_name}'))
    
    def detect_all(self) -> Dict[str, Any]:
        """检测所有AI工具"""
        results = {}
        
        for tool_name in self.ai_tools:
            print(f"🔍 检测 {tool_name}...")
            results[tool_name] = self.detect_tool_advanced(tool_name)
            
            status = "✅" if results[tool_name].get('installed', False) else "❌"
            version = results[tool_name].get('version', 'Unknown')
            method = results[tool_name].get('method', 'unknown')
            print(f"   {status} {tool_name}: {version} (检测方法: {method})")
        
        return results


def main():
    """主函数 - 命令行接口"""
    print("🚀 高级AI CLI工具检测器 - 多环境适配版")
    print("=" * 60)
    
    detector = AdvancedAICLIDetector()
    
    print(f"操作系统: {detector.os_type}")
    print(f"检测路径: {detector.system_path[:100]}...")
    print()
    
    results = detector.detect_all()
    
    print()
    print("📊 检测结果摘要:")
    installed_count = sum(1 for r in results.values() if r.get('installed', False))
    total_count = len(results)
    print(f"已安装: {installed_count}/{total_count}")
    
    print()
    print("🔧 详细检测信息:")
    for tool, result in results.items():
        installed = result.get('installed', False)
        if installed:
            print(f"  ✅ {tool}:")
            print(f"      版本: {result.get('version', 'Unknown')}")
            print(f"      路径: {result.get('installPath', 'Unknown')}")
            print(f"      配置: {result.get('configPath', 'Unknown')}")
            print(f"      检测方法: {result.get('method', 'Unknown')}")
        else:
            print(f"  ❌ {tool}: Not installed")
            method = result.get('method', 'Unknown')
            error = result.get('error', '')
            if error:
                print(f"      错误: {error}")
            print(f"      检测方法: {method}")
    
    return results


if __name__ == "__main__":
    results = main()