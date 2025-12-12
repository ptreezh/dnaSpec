"""
CLI Detection Module
Responsible for detecting installed AI CLI tools in the system
"""
import subprocess
import os
import shutil
from typing import Dict, Any, Optional
import platform


class CliDetector:
    """
    AI CLI Tool Detector
    Detects various AI CLI tools installed in the system
    """

    def __init__(self):
        self.detectors = {
            'claude': self.detect_claude,
            'gemini': self.detect_gemini,
            'qwen': self.detect_qwen,
            'copilot': self.detect_copilot,
            'cursor': self.detect_cursor,
            'iflow': self.detect_iflow,
            'qodercli': self.detect_qodercli,
            'codebuddy': self.detect_codebuddy
        }

    def detect_claude(self) -> Dict[str, Any]:
        """
        Detect if Claude CLI is installed

        Returns:
            Detection result dictionary
        """
        try:
            # Run command name directly, this handles .cmd scripts on Windows properly
            result = subprocess.run(
                ['claude', '--version'],
                capture_output=True,
                text=True,
                timeout=15,  # Increase timeout to avoid timeout issues
                shell=(platform.system() == 'Windows')  # Use shell on Windows to handle scripts
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                # If execution succeeds, get installation path with shutil.which
                install_path = shutil.which('claude')

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
        Detect if Gemini CLI is installed

        Returns:
            Detection result dictionary
        """
        try:
            # Run command name directly, this handles .cmd scripts on Windows properly
            result = subprocess.run(
                ['gemini', '--version'],
                capture_output=True,
                text=True,
                timeout=15,  # Increase timeout to avoid timeout issues
                shell=(platform.system() == 'Windows')  # Use shell on Windows to handle scripts
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                # If execution succeeds, get installation path with shutil.which
                install_path = shutil.which('gemini')

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
        Detect if Qwen CLI is installed

        Returns:
            Detection result dictionary
        """
        try:
            # Run command name directly, this handles .cmd scripts on Windows properly
            result = subprocess.run(
                ['qwen', '--version'],
                capture_output=True,
                text=True,
                timeout=15,  # Increase timeout to avoid timeout issues
                shell=(platform.system() == 'Windows')  # Use shell on Windows to handle scripts
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                # If execution succeeds, get installation path with shutil.which
                install_path = shutil.which('qwen')

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
        Detect if Copilot CLI is installed

        Returns:
            Detection result dictionary
        """
        try:
            # GitHub Copilot runs as an extension to GitHub CLI (gh)
            result = subprocess.run(
                ['gh', 'copilot', '--version'],
                capture_output=True,
                text=True,
                timeout=15,  # Increase timeout to avoid timeout issues
                shell=(platform.system() == 'Windows')  # Use shell on Windows to handle scripts
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                # If execution succeeds, get installation path with shutil.which
                install_path = shutil.which('gh')

                return {
                    'installed': True,
                    'version': version,
                    'installPath': install_path,
                    'configPath': self._get_copilot_config_path()
                }
            else:
                # Check if GitHub CLI is installed but Copilot extension isn't
                gh_result = subprocess.run(
                    ['gh', '--version'],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    shell=(platform.system() == 'Windows')
                )
                
                if gh_result.returncode == 0:
                    return {
                        'installed': False,
                        'error': 'GitHub CLI installed but Copilot extension not found'
                    }
                else:
                    return {
                        'installed': False,
                        'error': 'GitHub CLI with Copilot extension not found'
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
        Detect if Cursor is installed

        Returns:
            Detection result dictionary
        """
        try:
            # Cursor may not have command line version, check if related commands exist
            result = subprocess.run(
                ['cursor', '--version'],
                capture_output=True,
                text=True,
                timeout=15,  # Increase timeout to avoid timeout issues
                shell=(platform.system() == 'Windows')  # Use shell on Windows to handle scripts
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                install_path = shutil.which('cursor')

                return {
                    'installed': True,
                    'version': version,
                    'installPath': install_path,
                    'configPath': self._get_cursor_config_path()
                }
            else:
                # Try other possible commands
                for cmd in ['cursor', 'cursor-cli']:
                    try:
                        result = subprocess.run(
                            [cmd, '--help'],
                            capture_output=True,
                            text=True,
                            timeout=5,
                            shell=(platform.system() == 'Windows')
                        )
                        if result.returncode == 0:
                            install_path = shutil.which(cmd)
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
        Detect all supported CLI tools

        Returns:
            All detection results dictionary
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
        Get installation path of CLI tool

        Args:
            cli_name: Name of CLI tool

        Returns:
            Installation path or None
        """
        try:
            result = subprocess.run(
                ['where' if platform.system() == 'Windows' else 'which', cli_name],
                capture_output=True,
                text=True,
                timeout=5,
                shell=(platform.system() == 'Windows')  # Use shell on Windows to handle 'where' command
            )
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0]  # Take first path
            return None
        except:
            return None

    def _get_claude_config_path(self) -> str:
        """
        Get Claude configuration path

        Returns:
            Configuration path string
        """
        home = os.path.expanduser("~")
        if platform.system() == "Windows":
            return os.path.join(home, ".config", "claude", "skills")
        else:
            return os.path.join(home, ".config", "claude", "skills")

    def _get_gemini_config_path(self) -> str:
        """
        Get Gemini configuration path

        Returns:
            Configuration path string
        """
        home = os.path.expanduser("~")
        if platform.system() == "Windows":
            return os.path.join(home, ".local", "share", "gemini", "extensions")
        else:
            return os.path.join(home, ".local", "share", "gemini", "extensions")

    def _get_qwen_config_path(self) -> str:
        """
        Get Qwen configuration path

        Returns:
            Configuration path string
        """
        home = os.path.expanduser("~")
        if platform.system() == "Windows":
            return os.path.join(home, ".qwen", "plugins")
        else:
            return os.path.join(home, ".qwen", "plugins")

    def _get_copilot_config_path(self) -> str:
        """
        Get Copilot configuration path

        Returns:
            Configuration path string
        """
        home = os.path.expanduser("~")
        if platform.system() == "Windows":
            return os.path.join(home, ".config", "gh-copilot")
        else:
            return os.path.join(home, ".config", "gh-copilot")

    def _get_cursor_config_path(self) -> str:
        """
        Get Cursor configuration path

        Returns:
            Configuration path string
        """
        home = os.path.expanduser("~")
        if platform.system() == "Windows":
            return os.path.join(home, ".cursor")
        else:
            return os.path.join(home, ".cursor")

    def detect_iflow(self) -> Dict[str, Any]:
        """
        Detect if IFlow CLI is installed

        Returns:
            Detection result dictionary
        """
        try:
            # Run command name directly, this handles .cmd scripts on Windows properly
            result = subprocess.run(
                ['iflow', '--version'],
                capture_output=True,
                text=True,
                timeout=15,
                shell=(platform.system() == 'Windows')
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                # If execution succeeds, get installation path with shutil.which
                install_path = shutil.which('iflow')

                return {
                    'installed': True,
                    'version': version,
                    'installPath': install_path,
                    'configPath': self._get_iflow_config_path()
                }
            else:
                return {
                    'installed': False,
                    'error': result.stderr.strip() if result.stderr else 'Unknown error'
                }
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return {
                'installed': False,
                'error': 'IFlow CLI not found in system PATH'
            }
        except Exception as e:
            return {
                'installed': False,
                'error': str(e)
            }

    def detect_qodercli(self) -> Dict[str, Any]:
        """
        Detect if QoderCLI is installed

        Returns:
            Detection result dictionary
        """
        try:
            # Run command name directly, this handles .cmd scripts on Windows properly
            result = subprocess.run(
                ['qodercli', '--version'],
                capture_output=True,
                text=True,
                timeout=15,
                shell=(platform.system() == 'Windows')
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                # If execution succeeds, get installation path with shutil.which
                install_path = shutil.which('qodercli')

                return {
                    'installed': True,
                    'version': version,
                    'installPath': install_path,
                    'configPath': self._get_qodercli_config_path()
                }
            else:
                return {
                    'installed': False,
                    'error': result.stderr.strip() if result.stderr else 'Unknown error'
                }
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return {
                'installed': False,
                'error': 'QoderCLI not found in system PATH'
            }
        except Exception as e:
            return {
                'installed': False,
                'error': str(e)
            }

    def detect_codebuddy(self) -> Dict[str, Any]:
        """
        Detect if CodeBuddy CLI is installed

        Returns:
            Detection result dictionary
        """
        try:
            # Run command name directly, this handles .cmd scripts on Windows properly
            result = subprocess.run(
                ['codebuddy', '--version'],
                capture_output=True,
                text=True,
                timeout=15,
                shell=(platform.system() == 'Windows')
            )

            if result.returncode == 0:
                version = result.stdout.strip()
                # If execution succeeds, get installation path with shutil.which
                install_path = shutil.which('codebuddy')

                return {
                    'installed': True,
                    'version': version,
                    'installPath': install_path,
                    'configPath': self._get_codebuddy_config_path()
                }
            else:
                return {
                    'installed': False,
                    'error': result.stderr.strip() if result.stderr else 'Unknown error'
                }
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return {
                'installed': False,
                'error': 'CodeBuddy not found in system PATH'
            }
        except Exception as e:
            return {
                'installed': False,
                'error': str(e)
            }

    def _get_iflow_config_path(self) -> str:
        """
        Get IFlow configuration path

        Returns:
            Configuration path string
        """
        home = os.path.expanduser("~")
        if platform.system() == "Windows":
            return os.path.join(home, ".iflow", "commands")
        else:
            return os.path.join(home, ".iflow", "commands")

    def _get_qodercli_config_path(self) -> str:
        """
        Get QoderCLI configuration path

        Returns:
            Configuration path string
        """
        home = os.path.expanduser("~")
        if platform.system() == "Windows":
            return os.path.join(home, ".qodercli", "extensions")
        else:
            return os.path.join(home, ".qodercli", "extensions")

    def _get_codebuddy_config_path(self) -> str:
        """
        Get CodeBuddy configuration path

        Returns:
            Configuration path string
        """
        home = os.path.expanduser("~")
        if platform.system() == "Windows":
            return os.path.join(home, ".codebuddy", "skills")
        else:
            return os.path.join(home, ".codebuddy", "skills")