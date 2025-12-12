#!/usr/bin/env python3
"""
DNASPEC Initialization Script
项目级别的初始化命令，用于检测和配置AI CLI工具
"""
import sys
import os
from pathlib import Path
from typing import Dict, Any, List

# 确保模块路径正确
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir / 'src'))

from dna_spec_kit_integration.core.cli_detector import CliDetector
from dna_spec_kit_integration.core.cli_extension_deployer import CLIExtensionDeployer
from dna_spec_kit_integration.core.config_generator import ConfigGenerator
from dna_spec_kit_integration.core.integration_validator import IntegrationValidator


class DNASPECInitializer:
    """DNASPEC项目初始化器"""

    def __init__(self):
        self.cli_detector = CliDetector()
        self.deployer = CLIExtensionDeployer()
        self.config_generator = ConfigGenerator()
        self.validator = IntegrationValidator()

    def run_initialization(self):
        """执行完整的初始化流程"""
        self._print_welcome()

        # 1. 检测已安装的AI CLI工具
        print("\n🔍 Scanning for AI CLI tools...")
        detected_tools = self.cli_detector.detect_all()

        # 2. 筛选已安装的平台
        available_platforms = self._get_available_platforms(detected_tools)

        if not available_platforms:
            self._show_no_platforms_help()
            return False

        # 3. 显示检测结果并让用户选择
        selected_platforms = self._prompt_platform_selection(available_platforms)

        if not selected_platforms:
            print("\n❌ No platforms selected. Initialization cancelled.")
            return False

        # 4. 执行部署配置
        success = self._deploy_to_platforms(selected_platforms)

        if success:
            self._show_success_message(selected_platforms)
            return True
        else:
            print("\n❌ Initialization failed!")
            return False

    def _print_welcome(self):
        """显示欢迎信息"""
        print("🚀 DNASPEC Project Initialization")
        print("=" * 50)
        print("Welcome to DNA SPEC Context System!")
        print("This wizard will help you configure DNASPEC skills for your AI CLI tools.")

    def _get_available_platforms(self, detected_tools: Dict[str, Any]) -> List[Dict[str, Any]]:
        """获取可用的平台列表"""
        available = []

        for platform_name, result in detected_tools.items():
            if result.get('installed', False):
                available.append({
                    'name': platform_name,
                    'version': result.get('version', 'Unknown'),
                    'path': result.get('installPath', 'Unknown'),
                    'config_path': result.get('configPath', 'Unknown')
                })

        return available

    def _show_no_platforms_help(self):
        """显示没有找到平台时的帮助信息"""
        print("\n❌ No supported AI CLI tools detected.")
        print("\nPlease install at least one of the following AI CLI tools:")
        print("\n🛠️  Recommended AI CLI Tools:")

        tools_info = [
            ("Claude CLI", "https://claude.ai/cli", "claude --version"),
            ("Gemini CLI", "https://ai.google.dev/cli", "gemini --version"),
            ("Qwen CLI", "https://qwen.readthedocs.io/", "qwen --version"),
            ("IFlow CLI", "https://iflow.dev/docs/cli", "iflow --version"),
            ("QoderCLI", "https://qodercli.dev/", "qodercli --version"),
            ("CodeBuddy", "https://codebuddy.dev/", "codebuddy --version"),
            ("Cursor", "https://cursor.sh/", "cursor --version"),
            ("GitHub Copilot CLI", "https://github.com/cli/cli#installation", "gh copilot --version")
        ]

        for name, url, check_cmd in tools_info:
            print(f"  • {name}")
            print(f"    Install: {url}")
            print(f"    Verify: {check_cmd}")
            print("")

        print("\nAfter installing, run 'dnaspec init' again to continue setup.")

    def _prompt_platform_selection(self, available_platforms: List[Dict[str, Any]]) -> List[str]:
        """提示用户选择平台"""
        print(f"\n✅ Found {len(available_platforms)} AI CLI tool(s):")

        for i, platform in enumerate(available_platforms, 1):
            print(f"  {i}. {platform['name'].title()}")
            print(f"     Version: {platform['version']}")
            print(f"     Path: {platform['path']}")
            print("")

        print("Select deployment target:")
        print("  0. Deploy to all detected platforms")
        print("  1-{}. Deploy to specific platform".format(len(available_platforms)))
        print("  s. Skip deployment (generate configs only)")
        print("  q. Quit")

        while True:
            try:
                choice = input("\nEnter your choice: ").strip().lower()

                if choice == 'q':
                    return []
                elif choice == 's':
                    return self._select_platforms_interactive(available_platforms)
                elif choice == '0':
                    return [p['name'] for p in available_platforms]
                elif choice.isdigit() and 1 <= int(choice) <= len(available_platforms):
                    return [available_platforms[int(choice) - 1]['name']]
                else:
                    print("❌ Invalid choice. Please try again.")

            except (ValueError, KeyboardInterrupt):
                print("\n❌ Invalid input or cancelled.")
                return []

    def _select_platforms_interactive(self, available_platforms: List[Dict[str, Any]]) -> List[str]:
        """交互式选择多个平台"""
        print("\nSelect platforms (comma-separated numbers, e.g., 1,3,5):")

        while True:
            try:
                selection = input("Enter numbers: ").strip()
                if not selection:
                    return []

                indices = [int(x.strip()) for x in selection.split(',')]
                selected = []

                for idx in indices:
                    if 1 <= idx <= len(available_platforms):
                        selected.append(available_platforms[idx - 1]['name'])
                    else:
                        print(f"❌ Invalid number: {idx}")
                        raise ValueError

                return selected

            except (ValueError, KeyboardInterrupt):
                print("❌ Invalid input. Please enter comma-separated numbers.")
                continue

    def _deploy_to_platforms(self, selected_platforms: List[str]) -> bool:
        """部署到选定平台"""
        print(f"\n🚀 Deploying DNASPEC skills to {len(selected_platforms)} platform(s)...")

        try:
            # 1. 生成配置文件
            print("⚙️  Generating configuration files...")
            config = self._generate_config(selected_platforms)

            # 2. 部署技能到各平台
            deployment_results = {}

            for platform in selected_platforms:
                print(f"\n📦 Deploying to {platform.title()}...")

                try:
                    # 生成平台特定的技能文件
                    result = self.deployer.deploy_skills_for_platform(
                        platform,
                        self.project_root
                    )

                    deployment_results[platform] = {
                        'success': True,
                        'result': result
                    }

                    print(f"✅ {platform.title()} deployment completed")

                except Exception as e:
                    deployment_results[platform] = {
                        'success': False,
                        'error': str(e)
                    }
                    print(f"❌ {platform.title()} deployment failed: {e}")

            # 3. 验证部署结果
            successful_deployments = sum(1 for r in deployment_results.values() if r['success'])

            if successful_deployments > 0:
                print(f"\n✅ Successfully deployed to {successful_deployments}/{len(selected_platforms)} platforms")

                # 保存部署配置
                self._save_deployment_config(selected_platforms, deployment_results)

                return True
            else:
                print("\n❌ All deployments failed")
                return False

        except Exception as e:
            print(f"\n❌ Deployment process failed: {e}")
            return False

    def _generate_config(self, selected_platforms: List[str]) -> Dict[str, Any]:
        """生成配置"""
        return {
            'project_name': Path.cwd().name,
            'deployment_time': self._get_timestamp(),
            'selected_platforms': selected_platforms,
            'skills_enabled': [
                'context-analysis',
                'context-optimization',
                'cognitive-template',
                'architect',
                'git-operations',
                'temp-workspace'
            ],
            'version': '1.0.0'
        }

    def _save_deployment_config(self, platforms: List[str], results: Dict[str, Any]):
        """保存部署配置"""
        dnaspec_dir = Path.cwd() / '.dnaspec'
        dnaspec_dir.mkdir(exist_ok=True)

        config = {
            'initialized': True,
            'deployment_time': self._get_timestamp(),
            'platforms': platforms,
            'deployment_results': results,
            'project_root': str(Path.cwd())
        }

        config_file = dnaspec_dir / 'deployment.json'
        import json
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    def _show_success_message(self, deployed_platforms: List[str]):
        """显示成功消息"""
        print("\n" + "="*50)
        print("🎉 DNASPEC Initialization Complete!")
        print("="*50)

        print(f"\n✅ Successfully configured {len(deployed_platforms)} platform(s):")
        for platform in deployed_platforms:
            print(f"  • {platform.title()}")

        print("\n📖 Usage Examples:")
        print("\nYou can now use DNASPEC skills in your configured AI CLI tools:")

        examples = [
            ("Context Analysis", "/speckit.dnaspec.context-analysis \"Analyze this requirement\""),
            ("Context Optimization", "/speckit.dnaspec.context-optimization \"Optimize this prompt\""),
            ("System Architecture", "/speckit.dnaspec.architect \"Design a user authentication system\""),
            ("Cognitive Template", "/speckit.dnaspec.cognitive-template \"Apply verification template\" template=verification"),
            ("Git Operations", "/speckit.dnaspec.git-skill operation=status"),
            ("Temp Workspace", "/speckit.dnaspec.temp-workspace operation=create")
        ]

        for skill_name, command in examples:
            print(f"\n  {skill_name}:")
            print(f"    {command}")

        print(f"\n📁 Configuration saved to: {Path.cwd()}/.dnaspec/")
        print("🔧 To reconfigure, run: dnaspec init")
        print("📋 To check status, run: dnaspec status")

        print("\nHappy coding with DNASPEC! 🚀")

    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()

    @property
    def project_root(self) -> Path:
        """项目根目录"""
        return Path.cwd()


def main():
    """主函数"""
    try:
        initializer = DNASPECInitializer()
        success = initializer.run_initialization()
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\n❌ Initialization cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()