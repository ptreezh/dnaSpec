"""
改进的CLI检测器模块
使用npm包管理器进行更可靠的检测
"""
import subprocess
import os
import json
from typing import Dict, Any, Optional
import platform


class ImprovedCliDetector:
    """
    改进的AI CLI工具检测器
    使用npm包管理器进行更可靠的检测
    """

    def __init__(self):
        # npm包名映射 - 使用在npm list中实际找到的包名
        self.npm_patterns = {
            'claude': '@anthropic-ai/claude-code',      # 在npm list中找到的确切包名
            'gemini': '@google/gemini-cli',             # 在npm list中找到的确切包名
            'qwen': '@qwen-code/qwen-code',             # 在npm list中找到的确切包名
            'copilot': '@github/copilot',               # 在npm list中找到的确切包名
            'cursor': 'cursor',                         # 需要单独处理
            'codebuddy': '@tencent-ai/codebuddy-code',  # 代码助手
            'qoder': '@qoder-ai/qodercli',              # Qoder CLI
            'kimi': '@jacksontian/kimi-cli',            # Kimi CLI
            'iflow': '@iflow-ai/iflow-cli',             # iFlow CLI
            'arxiv': 'arxiv-mcp-server'                 # Arxiv MCP服务器
        }

    def get_all_supported_tools(self):
        """获取所有支持的工具列表"""
        return list(self.npm_patterns.keys())

    def detect_with_npm(self, package_pattern: str) -> Dict[str, Any]:
        """
        使用npm检测包安装状态（文件重定向方式）

        Args:
            package_pattern: 要检测的包名模式

        Returns:
            检测结果字典
        """
        import tempfile
        import os

        # 使用临时文件来获取npm输出
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json', encoding='utf-8') as tmp_file:
            temp_filename = tmp_file.name

        try:
            # 使用shell重定向方式运行npm命令
            subprocess.run(f'npm list -g --depth=0 --json > "{temp_filename}"',
                         shell=True, capture_output=True, timeout=15)

            # 检查文件是否存在且有内容
            if os.path.exists(temp_filename):
                try:
                    with open(temp_filename, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        if content:
                            packages = json.loads(content)
                            if 'dependencies' in packages:
                                for pkg_name, pkg_info in packages['dependencies'].items():
                                    # 检查包名是否包含指定模式（部分匹配）
                                    if package_pattern.lower() in pkg_name.lower():
                                        version = pkg_info.get('version', 'unknown')
                                        # 如果version为unknown或不存在，尝试从其他字段获取
                                        if not version or version == 'unknown':
                                            version = pkg_info.get('resolved', 'unknown')

                                        return {
                                            'installed': True,
                                            'version': version,
                                            'packageName': pkg_name,
                                            'installPath': pkg_info.get('resolved', 'unknown')
                                        }

                                    # 也检查是否是完整的包名匹配
                                    if pkg_name.lower() == package_pattern.lower():
                                        version = pkg_info.get('version', 'unknown')
                                        if not version or version == 'unknown':
                                            version = pkg_info.get('resolved', 'unknown')

                                        return {
                                            'installed': True,
                                            'version': version,
                                            'packageName': pkg_name,
                                            'installPath': pkg_info.get('resolved', 'unknown')
                                        }
                except json.JSONDecodeError as e:
                    return {
                        'installed': False,
                        'error': f'JSON parse error: {str(e)}'
                    }
                except Exception as e:
                    return {
                        'installed': False,
                        'error': f'Reading file error: {str(e)}'
                    }
            else:
                return {
                    'installed': False,
                    'error': 'Could not create temporary file'
                }

            return {
                'installed': False,
                'error': 'Package not found in npm global list'
            }
        except subprocess.TimeoutExpired:
            return {
                'installed': False,
                'error': 'NPM command timed out'
            }
        except Exception as e:
            return {
                'installed': False,
                'error': str(e)
            }
        finally:
            # 清理临时文件
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

    def detect_with_which(self, command: str) -> Optional[str]:
        """
        使用which或where命令检测可执行文件

        Args:
            command: 命令名称

        Returns:
            可执行文件路径或None
        """
        try:
            if platform.system() == 'Windows':
                result = subprocess.run(
                    ['where', command],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
            else:
                result = subprocess.run(
                    ['which', command],
                    capture_output=True,
                    text=True,
                    timeout=5
                )

            if result.returncode == 0:
                path = result.stdout.strip().split('\n')[0]  # 取第一个路径
                return path
            return None
        except:
            return None

    def detect_claude(self) -> Dict[str, Any]:
        """检测Claude CLI - 使用npm和命令行双重检测"""
        # 首先使用npm检测 (使用精确的包名)
        npm_result = self.detect_with_npm('@anthropic-ai/claude-code')
        if npm_result['installed']:
            return npm_result

        # 如果npm检测失败，尝试命令行检测
        cmd_path = self.detect_with_which('claude')
        if cmd_path:
            try:
                version_result = subprocess.run(
                    ['claude', '--version'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if version_result.returncode == 0:
                    version = version_result.stdout.strip() or version_result.stderr.strip()
                    return {
                        'installed': True,
                        'version': version,
                        'installPath': cmd_path
                    }
            except:
                pass

        # 最后尝试Claude的其他可能命令
        for cmd in ['claude', 'anthropic']:
            cmd_path = self.detect_with_which(cmd)
            if cmd_path:
                try:
                    version_result = subprocess.run(
                        [cmd, '--version'],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if version_result.returncode == 0:
                        version = version_result.stdout.strip() or version_result.stderr.strip()
                        return {
                            'installed': True,
                            'version': version,
                            'installPath': cmd_path
                        }
                except:
                    continue

        return {'installed': False, 'error': 'Claude CLI not found'}

    def detect_gemini(self) -> Dict[str, Any]:
        """检测Gemini CLI - 使用npm和命令行双重检测"""
        # 首先使用npm检测 (使用精确的包名)
        npm_result = self.detect_with_npm('@google/gemini-cli')
        if npm_result['installed']:
            return npm_result

        # 如果npm检测失败，尝试命令行检测
        cmd_path = self.detect_with_which('gemini')
        if cmd_path:
            try:
                version_result = subprocess.run(
                    ['gemini', '--version'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if version_result.returncode == 0:
                    version = version_result.stdout.strip() or version_result.stderr.strip()
                    return {
                        'installed': True,
                        'version': version,
                        'installPath': cmd_path
                    }
            except:
                pass

        return {'installed': False, 'error': 'Gemini CLI not found'}

    def detect_qwen(self) -> Dict[str, Any]:
        """检测Qwen CLI - 使用npm和命令行双重检测"""
        # 首先使用npm检测 (使用精确的包名)
        npm_result = self.detect_with_npm('@qwen-code/qwen-code')
        if npm_result['installed']:
            return npm_result

        # 尝试检测其他Qwen相关的包
        for pattern in ['@qwen-code/qwen-code', 'qwen', 'qoder']:
            npm_result = self.detect_with_npm(pattern)
            if npm_result['installed']:
                return npm_result

        # 如果npm检测失败，尝试命令行检测
        cmd_path = self.detect_with_which('qwen')
        if cmd_path:
            try:
                version_result = subprocess.run(
                    ['qwen', '--version'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if version_result.returncode == 0:
                    version = version_result.stdout.strip() or version_result.stderr.strip()
                    return {
                        'installed': True,
                        'version': version,
                        'installPath': cmd_path
                    }
            except:
                pass

        # 尝试其他可能与Qwen相关的命令
        for cmd in ['qwen', 'qwen-code', 'qoder']:
            cmd_path = self.detect_with_which(cmd)
            if cmd_path:
                try:
                    version_result = subprocess.run(
                        [cmd, '--version'],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if version_result.returncode == 0:
                        version = version_result.stdout.strip() or version_result.stderr.strip()
                        return {
                            'installed': True,
                            'version': version,
                            'installPath': cmd_path
                        }
                except:
                    continue

        return {'installed': False, 'error': 'Qwen CLI not found'}

    def detect_copilot(self) -> Dict[str, Any]:
        """检测Copilot CLI - 使用npm和命令行双重检测"""
        # 首先使用npm检测 (使用精确的包名)
        npm_result = self.detect_with_npm('@github/copilot')
        if npm_result['installed']:
            return npm_result

        # 如果npm检测失败，尝试命令行检测
        cmd_path = self.detect_with_which('gh')
        if cmd_path:
            try:
                version_result = subprocess.run(
                    ['gh', 'copilot', '--version'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if version_result.returncode == 0:
                    version = version_result.stdout.strip() or version_result.stderr.strip()
                    return {
                        'installed': True,
                        'version': version,
                        'installPath': cmd_path
                    }
            except:
                pass

        return {'installed': False, 'error': 'GitHub Copilot not found'}

    def detect_codebuddy(self) -> Dict[str, Any]:
        """检测CodeBuddy CLI - 使用npm检测"""
        # 使用npm检测
        npm_result = self.detect_with_npm('@tencent-ai/codebuddy-code')
        if npm_result['installed']:
            return npm_result

        # 尝试命令行检测
        for cmd in ['codebuddy', 'codebuddy-code']:
            cmd_path = self.detect_with_which(cmd)
            if cmd_path:
                try:
                    version_result = subprocess.run(
                        [cmd, '--version'],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if version_result.returncode == 0:
                        version = version_result.stdout.strip() or version_result.stderr.strip()
                        return {
                            'installed': True,
                            'version': version,
                            'installPath': cmd_path
                        }
                except:
                    continue

        return {'installed': False, 'error': 'CodeBuddy CLI not found'}

    def detect_qoder(self) -> Dict[str, Any]:
        """检测Qoder CLI - 使用npm检测"""
        # 使用npm检测
        npm_result = self.detect_with_npm('@qoder-ai/qodercli')
        if npm_result['installed']:
            return npm_result

        # 尝试命令行检测
        cmd_path = self.detect_with_which('qoder')
        if cmd_path:
            try:
                version_result = subprocess.run(
                    ['qoder', '--version'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if version_result.returncode == 0:
                    version = version_result.stdout.strip() or version_result.stderr.strip()
                    return {
                        'installed': True,
                        'version': version,
                        'installPath': cmd_path
                    }
            except:
                pass

        return {'installed': False, 'error': 'Qoder CLI not found'}

    def detect_kimi(self) -> Dict[str, Any]:
        """检测Kimi CLI - 使用npm检测"""
        # 使用npm检测
        npm_result = self.detect_with_npm('@jacksontian/kimi-cli')
        if npm_result['installed']:
            return npm_result

        # 尝试命令行检测
        for cmd in ['kimi', 'kimi-cli']:
            cmd_path = self.detect_with_which(cmd)
            if cmd_path:
                try:
                    version_result = subprocess.run(
                        [cmd, '--version'],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    if version_result.returncode == 0:
                        version = version_result.stdout.strip() or version_result.stderr.strip()
                        return {
                            'installed': True,
                            'version': version,
                            'installPath': cmd_path
                        }
                except:
                    continue

        return {'installed': False, 'error': 'Kimi CLI not found'}

    def detect_iflow(self) -> Dict[str, Any]:
        """检测iFlow CLI - 使用npm检测"""
        # 使用npm检测
        npm_result = self.detect_with_npm('@iflow-ai/iflow-cli')
        if npm_result['installed']:
            return npm_result

        # 尝试命令行检测
        cmd_path = self.detect_with_which('iflow')
        if cmd_path:
            try:
                version_result = subprocess.run(
                    ['iflow', '--version'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if version_result.returncode == 0:
                    version = version_result.stdout.strip() or version_result.stderr.strip()
                    return {
                        'installed': True,
                        'version': version,
                        'installPath': cmd_path
                    }
            except:
                pass

        return {'installed': False, 'error': 'iFlow CLI not found'}

    def detect_cursor(self) -> Dict[str, Any]:
        """检测Cursor - 使用多种检测方法"""
        # 尝试npm检测
        npm_result = self.detect_with_npm('cursor')
        if npm_result['installed']:
            return npm_result

        # 尝试命令检测
        cmd_path = self.detect_with_which('cursor')
        if cmd_path:
            return {
                'installed': True,
                'version': 'unknown',
                'installPath': cmd_path
            }

        # 尝试在常见路径中查找Cursor
        common_paths = [
            '/usr/local/bin/cursor',
            '/opt/cursor/cursor',
            'C:\\Users\\*\\AppData\\Local\\Programs\\Cursor\\resources\\app\\out\\cli\\cursor.cmd',
            'C:\\Users\\*\\AppData\\Local\\Programs\\Cursor\\cursor.exe',
            '/Applications/Cursor.app/Contents/MacOS/Cursor'
        ]

        for path in common_paths:
            if os.path.exists(path):
                return {
                    'installed': True,
                    'version': 'unknown',
                    'installPath': path
                }

        return {'installed': False, 'error': 'Cursor not found'}

    def detect_all(self) -> Dict[str, Any]:
        """
        检测所有支持的CLI工具

        Returns:
            所有检测结果字典
        """
        results = {}

        detectors = {
            'claude': self.detect_claude,
            'gemini': self.detect_gemini,
            'qwen': self.detect_qwen,
            'copilot': self.detect_copilot,
            'cursor': self.detect_cursor,
            'codebuddy': self.detect_codebuddy,
            'qoder': self.detect_qoder,
            'kimi': self.detect_kimi,
            'iflow': self.detect_iflow
        }

        for name, detector in detectors.items():
            try:
                results[name] = detector()
            except Exception as e:
                results[name] = {
                    'installed': False,
                    'error': str(e)
                }

        return results

    def get_detailed_report(self) -> Dict[str, Any]:
        """
        获取详细的检测报告

        Returns:
            详细检测报告
        """
        results = self.detect_all()

        report = {
            'timestamp': self._get_timestamp(),
            'platform': platform.system(),
            'detectedTools': results,
            'summary': {
                'totalTools': len(results),
                'installedTools': sum(1 for r in results.values() if r.get('installed', False)),
                'detectedByNpm': [],
                'detectedByCommand': []
            }
        }

        return report

    def _get_timestamp(self) -> str:
        """
        获取当前时间戳

        Returns:
            ISO格式时间戳字符串
        """
        import datetime
        return datetime.datetime.now().isoformat()


def quick_detect_and_configure():
    """快速检测和配置函数"""
    print("🚀 开始改进的自动检测和配置...")
    
    detector = ImprovedCliDetector()
    report = detector.get_detailed_report()
    
    print("\n🔍 检测结果:")
    for tool, result in report['detectedTools'].items():
        status = "✅" if result.get('installed', False) else "❌"
        version = result.get('version', 'unknown')
        print(f"  {status} {tool}: {version}")
    
    print(f"\n📋 摘要: {report['summary']['installedTools']}/{report['summary']['totalTools']} 个工具已安装")
    
    # 这里可以继续执行配置逻辑...
    print("\n⚙️  检测完成，可以进行相应的配置...")
    
    return report


if __name__ == "__main__":
    quick_detect_and_configure()