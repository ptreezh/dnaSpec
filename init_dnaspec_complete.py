#!/usr/bin/env python3
"""
DNASPEC Complete Initialization Script
实现完整的项目初始化，包括：
1. AI CLI工具检测和部署
2. 渐进式披露目录结构创建
3. 安全工作流（缓冲区->核验->工作区->Git）
"""
import sys
import os
import json
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# 确保模块路径正确
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir / 'src'))

from dna_spec_kit_integration.core.cli_detector import CliDetector
from dna_spec_kit_integration.core.cli_extension_deployer import CLIExtensionDeployer


class DNASPECCompleteInitializer:
    """DNASPEC完整初始化器 - 实现安全工作流和渐进式披露"""

    def __init__(self):
        self.cli_detector = CliDetector()
        self.deployer = CLIExtensionDeployer()
        self.project_root = Path.cwd()

        # DNASPEC安全目录结构
        self.dnaspec_dir = self.project_root / '.dnaspec'
        self.temp_workspace_dir = self.dnaspec_dir / 'temp_workspace'
        self.staging_area_dir = self.dnaspec_dir / 'staging_area'
        self.workspace_dir = self.dnaspec_dir / 'workspace'
        self.docs_dir = self.dnaspec_dir / 'docs'
        self.logs_dir = self.dnaspec_dir / 'logs'
        self.config_dir = self.dnaspec_dir / 'config'

        # 渐进式披露级别
        self.disclosure_levels = {
            'basic': {
                'description': '基础级别 - 核心文档和结构',
                'directories': ['README.md', 'src/', 'docs/overview/'],
                'access_level': 'public'
            },
            'intermediate': {
                'description': '中级 - 技术细节和实现文档',
                'directories': ['docs/api/', 'docs/guides/', 'tests/', 'config/'],
                'access_level': 'team'
            },
            'advanced': {
                'description': '高级 - 内部架构和运维文档',
                'directories': ['docs/internal/', 'ops/', 'scripts/', '.dnaspec/internal/'],
                'access_level': 'internal'
            }
        }

    def run_complete_initialization(self):
        """执行完整的初始化流程"""
        self._print_banner()

        # 1. 创建DNASPEC安全目录结构
        print("\n🏗️  Creating DNASPEC secure directory structure...")
        self._create_dnaspec_directory_structure()

        # 2. 配置渐进式披露
        print("📋 Setting up progressive disclosure system...")
        self._setup_progressive_disclosure()

        # 3. 配置安全工作流
        print("🔒 Configuring secure workflow system...")
        self._setup_secure_workflow()

        # 4. 检测AI CLI工具
        print("\n🔍 Detecting AI CLI tools...")
        detected_tools = self.cli_detector.detect_all()
        available_platforms = self._get_available_platforms(detected_tools)

        if not available_platforms:
            self._show_no_platforms_help()
            return False

        # 5. 平台选择和部署
        selected_platforms = self._prompt_platform_selection(available_platforms)

        if not selected_platforms:
            print("\n❌ No platforms selected. Initialization cancelled.")
            return False

        # 6. 部署技能到选定平台
        success = self._deploy_to_platforms(selected_platforms)

        if success:
            self._show_completion_message(selected_platforms)
            return True
        else:
            print("\n❌ Initialization failed!")
            return False

    def _print_banner(self):
        """显示欢迎横幅"""
        print("🚀 DNASPEC Complete Project Initialization")
        print("=" * 60)
        print("🧬 DNA SPEC Context System - 安全工作流 + 渐进式披露")
        print("=" * 60)
        print("\nThis will create a secure AI-assisted development environment with:")
        print("  • Progressive disclosure directory structure")
        print("  • Secure workflow: Temp → Staging → Workspace → Git")
        print("  • AI CLI tool integration")
        print("  • Safety buffers and verification system")

    def _create_dnaspec_directory_structure(self):
        """创建DNASPEC安全目录结构"""
        print("📁 Creating secure directory structure...")

        # 创建主要目录
        directories = [
            self.dnaspec_dir,
            self.temp_workspace_dir,
            self.staging_area_dir,
            self.workspace_dir,
            self.docs_dir,
            self.logs_dir,
            self.config_dir
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Created: {directory.relative_to(self.project_root)}")

        # 创建缓冲区子目录
        buffer_dirs = [
            self.temp_workspace_dir / 'ai_generated',
            self.temp_workspace_dir / 'experiments',
            self.staging_area_dir / 'pending_review',
            self.staging_area_dir / 'verified',
            self.workspace_dir / 'src',
            self.workspace_dir / 'docs',
            self.workspace_dir / 'tests'
        ]

        for directory in buffer_dirs:
            directory.mkdir(parents=True, exist_ok=True)

        # 创建.gitignore确保安全隔离
        gitignore_content = """# DNASPEC Security - Never commit temp or staging files
temp_workspace/
staging_area/
logs/
*.tmp
*.temp
.DS_Store
.vscode/settings.json

# Only workspace files should be committed
!workspace/
"""

        gitignore_file = self.dnaspec_dir / '.gitignore'
        with open(gitignore_file, 'w') as f:
            f.write(gitignore_content)

        print("  ✅ Created .gitignore for security isolation")

    def _setup_progressive_disclosure(self):
        """设置渐进式披露系统"""
        print("📋 Setting up progressive disclosure levels...")

        # 创建渐进式披露配置
        disclosure_config = {
            'project_name': self.project_root.name,
            'created_at': datetime.now().isoformat(),
            'disclosure_levels': self.disclosure_levels,
            'current_level': 'basic',
            'access_control': {
                'public': ['README.md', 'docs/overview/'],
                'team': ['docs/api/', 'docs/guides/', 'tests/', 'config/'],
                'internal': ['docs/internal/', 'ops/', 'scripts/', '.dnaspec/internal/']
            }
        }

        config_file = self.config_dir / 'progressive_disclosure.json'
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(disclosure_config, f, ensure_ascii=False, indent=2)

        # 创建各披露级别的README文件
        for level, config in self.disclosure_levels.items():
            level_readme = self.docs_dir / f'{level}_README.md'
            with open(level_readme, 'w', encoding='utf-8') as f:
                f.write(f"""# {level.title()} Documentation Level

## Access Level: {config['access_level']}

## Description
{config['description']}

## Available Directories
{chr(10).join(f"- {dir}" for dir in config['directories'])}

## Access Guidelines
- Only share documentation at or below this level
- Respect access control restrictions
- Use judgment when sharing with external parties

---
*Generated by DNASPEC Progressive Disclosure System*
""")

        print("  ✅ Progressive disclosure system configured")

    def _setup_secure_workflow(self):
        """设置安全工作流系统"""
        print("🔒 Configuring secure workflow...")

        # 创建工作流配置
        workflow_config = {
            'project_name': self.project_root.name,
            'created_at': datetime.now().isoformat(),
            'workflow_stages': [
                {
                    'name': 'temp_workspace',
                    'description': 'AI生成内容暂存区',
                    'max_files': 20,
                    'auto_cleanup': True,
                    'path': str(self.temp_workspace_dir.relative_to(self.project_root))
                },
                {
                    'name': 'staging_area',
                    'description': '待核验内容缓冲区',
                    'verification_required': True,
                    'path': str(self.staging_area_dir.relative_to(self.project_root))
                },
                {
                    'name': 'workspace',
                    'description': '已核验工作区（可提交到Git）',
                    'git_tracked': True,
                    'path': str(self.workspace_dir.relative_to(self.project_root))
                }
            ],
            'safety_rules': [
                'Never commit directly from temp_workspace',
                'All files must pass verification before staging',
                'Manual confirmation required for workspace promotion',
                'Automatic cleanup of temp files > 7 days old'
            ]
        }

        workflow_file = self.config_dir / 'secure_workflow.json'
        with open(workflow_file, 'w', encoding='utf-8') as f:
            json.dump(workflow_config, f, ensure_ascii=False, indent=2)

        # 创建工作流脚本
        self._create_workflow_scripts()

        print("  ✅ Secure workflow system configured")

    def _create_workflow_scripts(self):
        """创建工作流管理脚本"""
        scripts_dir = self.dnaspec_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)

        # 验证脚本
        verify_script = scripts_dir / 'verify_and_stage.py'
        with open(verify_script, 'w', encoding='utf-8') as f:
            f.write('''#!/usr/bin/env python3
"""
DNASPEC文件验证和暂存脚本
将temp_workspace中的文件验证后移至staging_area
"""
import sys
import os
import json
import shutil
from pathlib import Path

def verify_file(file_path: Path) -> dict:
    """验证文件内容"""
    result = {
        'valid': True,
        'issues': [],
        'suggestions': []
    }

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 基本验证规则
        if len(content.strip()) == 0:
            result['valid'] = False
            result['issues'].append('File is empty')

        if 'TODO' in content or 'FIXME' in content:
            result['issues'].append('File contains TODO or FIXME markers')
            result['suggestions'].append('Consider completing todos before staging')

        # 安全检查
        dangerous_patterns = ['password', 'secret', 'key', 'token']
        for pattern in dangerous_patterns:
            if pattern.lower() in content.lower() and len(content) < 10000:
                result['issues'].append(f'File may contain sensitive information: {pattern}')
                result['valid'] = False

    except Exception as e:
        result['valid'] = False
        result['issues'].append(f'Error reading file: {str(e)}')

    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: verify_and_stage.py <file_path>")
        return 1

    file_path = Path(sys.argv[1])
    project_root = Path(__file__).parent.parent

    temp_dir = project_root / 'temp_workspace'
    staging_dir = project_root / 'staging_area' / 'pending_review'

    if not file_path.exists():
        print(f"Error: File {file_path} not found")
        return 1

    # 验证文件
    verification = verify_file(file_path)

    print(f"📋 Verifying: {file_path.name}")
    print(f"✅ Valid: {verification['valid']}")

    if verification['issues']:
        print("⚠️  Issues:")
        for issue in verification['issues']:
            print(f"  - {issue}")

    if verification['suggestions']:
        print("💡 Suggestions:")
        for suggestion in verification['suggestions']:
            print(f"  - {suggestion}")

    if verification['valid'] and input("\\nStage this file? (y/n): ").lower() == 'y':
        staging_dir.mkdir(parents=True, exist_ok=True)
        staging_path = staging_dir / file_path.name
        shutil.copy2(file_path, staging_path)
        print(f"✅ Staged to: {staging_path}")

        # 可选：删除原文件
        if input("Remove original from temp_workspace? (y/n): ").lower() == 'y':
            file_path.unlink()
            print("🗑️  Removed from temp_workspace")

    return 0

if __name__ == "__main__":
    sys.exit(main())
''')

        verify_script.chmod(0o755)

        # 提升脚本
        promote_script = scripts_dir / 'promote_to_workspace.py'
        with open(promote_script, 'w', encoding='utf-8') as f:
            f.write('''#!/usr/bin/env python3
"""
DNASPEC文件提升脚本
将staging_area中的已验证文件移至workspace
"""
import sys
import os
import shutil
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: promote_to_workspace.py <file_path>")
        return 1

    file_path = Path(sys.argv[1])
    project_root = Path(__file__).parent.parent

    verified_dir = project_root / 'staging_area' / 'verified'
    workspace_dir = project_root / 'workspace'

    if not file_path.exists():
        print(f"Error: File {file_path} not found")
        return 1

    print(f"📋 Promoting: {file_path.name}")

    # 确认提升
    if input("Promote to workspace (Git-tracked)? (y/n): ").lower() == 'y':
        workspace_dir.mkdir(parents=True, exist_ok=True)

        # 保持相对路径结构
        relative_path = file_path.relative_to(verified_dir)
        target_path = workspace_dir / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(file_path, target_path)
        print(f"✅ Promoted to: {target_path}")

        print("💡 File is now ready for Git commit")
        print("   Run: git add workspace/ && git commit -m 'Add verified AI-generated content'")

    return 0

if __name__ == "__main__":
    sys.exit(main())
''')

        promote_script.chmod(0o755)
        print("  ✅ Workflow management scripts created")

    def _get_available_platforms(self, detected_tools: Dict[str, Any]) -> List[Dict[str, Any]]:
        """获取可用的平台列表"""
        available = []

        for platform_name, result in detected_tools.items():
            if result.get('installed', False):
                available.append({
                    'name': platform_name,
                    'version': result.get('version', 'Unknown'),
                    'path': result.get('installPath', 'Unknown')
                })

        return available

    def _show_no_platforms_help(self):
        """显示没有找到平台时的帮助信息"""
        print("\n❌ No supported AI CLI tools detected.")
        print("\\nPlease install at least one AI CLI tool:")
        print("  • Claude CLI: npm install -g @anthropic-ai/claude-cli")
        print("  • Qwen CLI: npm install -g qwen-code")
        print("  • IFlow CLI: npm install -g iflow-cli")
        print("  • And others...")
        print("\\nAfter installation, run 'dnaspec init' again.")

    def _prompt_platform_selection(self, available_platforms: List[Dict[str, Any]]) -> List[str]:
        """提示用户选择平台"""
        print(f"\\n✅ Found {len(available_platforms)} AI CLI tool(s):")

        for i, platform in enumerate(available_platforms, 1):
            print(f"  {i}. {platform['name'].title()}")
            print(f"     Version: {platform['version']}")

        print("\\nSelect deployment target:")
        print("  0. Deploy to all detected platforms")
        print("  1-{}. Deploy to specific platform".format(len(available_platforms)))
        print("  s. Skip AI CLI integration (directories only)")
        print("  q. Quit")

        while True:
            try:
                choice = input("\\nEnter your choice: ").strip().lower()

                if choice == 'q':
                    return []
                elif choice == 's':
                    return []  # 跳过AI CLI集成
                elif choice == '0':
                    return [p['name'] for p in available_platforms]
                elif choice.isdigit() and 1 <= int(choice) <= len(available_platforms):
                    return [available_platforms[int(choice) - 1]['name']]
                else:
                    print("❌ Invalid choice. Please try again.")

            except (ValueError, KeyboardInterrupt):
                print("\\n❌ Invalid input or cancelled.")
                return []

    def _deploy_to_platforms(self, selected_platforms: List[str]) -> bool:
        """部署到选定平台"""
        if not selected_platforms:
            print("\\n⏭️  Skipping AI CLI tool integration")
            print("📁 DNASPEC directory structure created successfully")
            print("\\n🔧 To add AI CLI tools later, run:")
            print("   dnaspec deploy")
            return True

        print(f"\\n🚀 Deploying DNASPEC skills to {len(selected_platforms)} platform(s)...")

        try:
            # 生成CLI扩展
            self.dnaspec_dir.mkdir(exist_ok=True)
            result = self.deployer.deploy_cli_extensions()

            if result.get('success', False):
                print(f"✅ Successfully deployed CLI extensions")
                return True
            else:
                print(f"❌ CLI deployment failed")
                return False

        except Exception as e:
            print(f"\\n❌ Deployment error: {e}")
            return False

    def _show_completion_message(self, deployed_platforms: List[str]):
        """显示完成消息"""
        print("\\n" + "="*60)
        print("🎉 DNASPEC Complete Initialization Successful!")
        print("="*60)

        print(f"\\n✅ Created secure directory structure:")
        print(f"  📁 .dnaspec/")
        print(f"    🔒 temp_workspace/     - AI生成内容暂存区")
        print(f"    ⏳ staging_area/       - 待核验内容缓冲区")
        print(f"    ✅ workspace/          - 已核验工作区（Git可提交）")
        print(f"    📚 docs/               - 渐进式披露文档")
        print(f"    ⚙️  config/             - 配置文件")
        print(f"    📝 logs/               - 系统日志")

        if deployed_platforms:
            print(f"\\n✅ Deployed AI CLI skills to: {', '.join(deployed_platforms)}")

        print(f"\\n🔐 Security Workflow:")
        print(f"  1️⃣  AI生成 → temp_workspace (安全隔离)")
        print(f"  2️⃣  验证 → staging_area (缓冲区)")
        print(f"  3️⃣  确认 → workspace (工作区)")
        print(f"  4️⃣  Git提交 (仅工作区)")

        print(f"\\n📋 Usage Examples:")
        print(f"  🏗️  Create temp workspace:")
        print(f"     /dnaspec.workspace create")

        print(f"  📝 Add AI-generated file:")
        print(f"     /dnaspec.workspace add example.py '代码内容'")

        print(f"  ✅ Verify and stage file:")
        print(f"     python .dnaspec/scripts/verify_and_stage.py temp_workspace/example.py")

        print(f"  🚀 Promote to workspace:")
        print(f"     python .dnaspec/scripts/promote_to_workspace.py staging_area/verified/example.py")

        print(f"  🔧 Git operations:")
        print(f"     /dnaspec.git status")
        print(f"     /dnaspec.git commit 'Add verified AI-generated content'")

        print(f"\\n📚 Progressive Disclosure:")
        print(f"  🔒 Basic: README.md, docs/overview/")
        print(f"  👥 Team: docs/api/, docs/guides/, tests/")
        print(f"  🏢 Internal: docs/internal/, ops/, scripts/")

        print(f"\\n💡 Pro Tips:")
        print(f"  • Never commit temp_workspace/ or staging_area/ to Git")
        print(f"  • Always verify files before promoting to workspace")
        print(f"  • Use progressive disclosure to control information access")
        print(f"  • Check .dnaspec/logs/ for system activity")

        print(f"\\n🔧 Management Commands:")
        print(f"  dnaspec status     - Check system status")
        print(f"  dnaspec validate    - Verify integrations")
        print(f"  dnaspec clean       - Cleanup temporary files")

        print(f"\\n🎯 Ready for secure AI-assisted development!")


def main():
    """主函数"""
    try:
        initializer = DNASPECCompleteInitializer()
        success = initializer.run_complete_initialization()
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\\n\\n❌ Initialization cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()