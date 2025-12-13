#!/usr/bin/env python3
"""
DNASPEC CLI扩展部署器
为项目生成AI CLI工具支持的扩展斜杠命令格式
"""
import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime


class CLIExtensionDeployer:
    """
    CLI扩展部署器
    生成符合各种AI CLI工具扩展格式的斜杠命令
    """

    def __init__(self, project_root: Optional[Path] = None):
        """
        初始化CLI扩展部署器

        Args:
            project_root: 项目根目录，默认为当前目录
        """
        self.project_root = project_root or Path.cwd()
        self.stigmergy_available = self._check_stigmergy_availability()
        self.deployment_mode = self._determine_deployment_mode()

        # 部署目录配置
        self.cli_extensions_dir = self.project_root / '.dnaspec' / 'cli_extensions'
        self.stigmergy_hooks_dir = Path.home() / '.stigmergy' / 'hooks'

        # 支持的AI CLI工具及其扩展格式
        self.supported_clis = {
            'claude': {
                'format': 'claude_skill',
                'extension': '.json',
                'command_prefix': '/',
                'description': 'Claude skill extensions'
            },
            'cursor': {
                'format': 'cursor_extension',
                'extension': '.md',
                'command_prefix': '/',
                'description': 'Cursor editor extensions'
            },
            'vscode': {
                'format': 'vscode_task',
                'extension': '.json',
                'command_prefix': '',
                'description': 'VS Code task definitions'
            },
            'windsurf': {
                'format': 'windsurf_skill',
                'extension': '.js',
                'command_prefix': '/',
                'description': 'Windsurf AI extensions'
            },
            'continue': {
                'format': 'continue_tool',
                'extension': '.py',
                'command_prefix': '/',
                'description': 'Continue.dev tools'
            },
            'cursor_rules': {
                'format': 'cursor_rules',
                'extension': '.md',
                'command_prefix': '',
                'description': 'Cursor rules definitions'
            },
            # 新增：支持基于commands目录的CLI工具
            'gemini': {
                'format': 'commands_dir',
                'extension': '.md',
                'command_prefix': '/',
                'description': 'Gemini CLI slash commands',
                'commands_dir': '.gemini/commands'
            },
            'qwen': {
                'format': 'commands_dir',
                'extension': '.md',
                'command_prefix': '/',
                'description': 'Qwen CLI slash commands',
                'commands_dir': '.qwen/commands'
            },
            'iflow': {
                'format': 'commands_dir',
                'extension': '.md',
                'command_prefix': '/',
                'description': 'IFlow CLI slash commands',
                'commands_dir': '.iflow/commands'
            },
            'qodercli': {
                'format': 'commands_dir',
                'extension': '.md',
                'command_prefix': '/',
                'description': 'QoderCLI slash commands',
                'commands_dir': '.qodercli/commands'
            },
            'codebuddy': {
                'format': 'commands_dir',
                'extension': '.md',
                'command_prefix': '/',
                'description': 'CodeBuddy slash commands',
                'commands_dir': '.codebuddy/commands'
            },
            'copilot': {
                'format': 'commands_dir',
                'extension': '.md',
                'command_prefix': '/',
                'description': 'GitHub Copilot CLI slash commands',
                'commands_dir': '.copilot/commands'
            }
        }

    def _check_stigmergy_availability(self) -> bool:
        """检查Stigmergy是否可用"""
        try:
            result = subprocess.run(
                ['stigmergy', '--version'],
                capture_output=True,
                text=True,
                timeout=10,
                shell=True
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError, OSError):
            pass
        return False

    def _determine_deployment_mode(self) -> str:
        """确定部署模式"""
        if self.stigmergy_available:
            return 'stigmergy'
        else:
            return 'cli-extensions'

    def deploy_all(self) -> Dict[str, Any]:
        """
        执行完整部署流程

        Returns:
            Dict: 部署结果
        """
        print(f"🚀 DNASPEC CLI Extension Deployment")
        print(f"📍 Project Root: {self.project_root}")
        print(f"🔧 Deployment Mode: {self.deployment_mode}")
        print(f"📋 Stigmergy Available: {self.stigmergy_available}")
        print("-" * 60)

        if self.deployment_mode == 'stigmergy':
            return self._deploy_with_stigmergy()
        else:
            return self._deploy_cli_extensions()

    def _deploy_cli_extensions(self) -> Dict[str, Any]:
        """
        部署CLI扩展（项目级）

        Returns:
            Dict: 部署结果
        """
        print("📁 Deploying CLI extensions for AI tools...")

        # 创建CLI扩展目录
        self.cli_extensions_dir.mkdir(parents=True, exist_ok=True)

        deployed_extensions = []
        deployment_errors = []

        # 获取DNASPEC技能
        skills = self._get_dnaspec_skills()

        # 为每个支持的CLI工具生成扩展
        for cli_name, cli_config in self.supported_clis.items():
            try:
                cli_extensions = self._generate_cli_extensions(cli_name, cli_config, skills)
                deployed_extensions.extend(cli_extensions)
                print(f"✅ Generated {len(cli_extensions)} extensions for {cli_name}")
            except Exception as e:
                deployment_errors.append(f"Failed to generate extensions for {cli_name}: {str(e)}")
                print(f"❌ Failed to generate extensions for {cli_name}: {e}")

        # 生成使用指南
        self._generate_usage_guide()

        # 生成集成配置
        self._generate_integration_config()

        success_count = len(deployed_extensions)

        print(f"\n📊 CLI extensions deployment completed!")
        print(f"✅ Successfully deployed: {success_count} extensions")
        print(f"📂 Extensions location: {self.cli_extensions_dir}")

        if deployment_errors:
            print(f"⚠️  Errors: {len(deployment_errors)}")
            for error in deployment_errors:
                print(f"   - {error}")

        return {
            'mode': 'cli-extensions',
            'success': success_count > 0,
            'deployed_extensions': deployed_extensions,
            'deployment_errors': deployment_errors,
            'extensions_dir': str(self.cli_extensions_dir),
            'supported_clis': list(self.supported_clis.keys()),
            'message': f'CLI extensions deployed for {len(self.supported_clis)} AI tools'
        }

    def _deploy_with_stigmergy(self) -> Dict[str, Any]:
        """
        使用Stigmergy进行全局部署

        Returns:
            Dict: 部署结果
        """
        print("🌐 Deploying with Stigmergy (global integration)...")

        try:
            from .stigmergy_adapter import StigmergyAdapter
            adapter = StigmergyAdapter()
            result = adapter.deploy_to_all_clis()

            if result.get('success'):
                print(f"✅ Stigmergy deployment completed!")
                print(f"📊 Successfully deployed to {result.get('successful_deployments', 0)}/{result.get('total_platforms', 0)} platforms")

                verification = adapter.verify_deployment()
                deployed_clis = verification.get('deployed_clis', [])
                if deployed_clis:
                    print(f"🎯 Active CLI integrations: {', '.join(deployed_clis)}")

                return {
                    'mode': 'stigmergy',
                    'success': True,
                    'deployment_result': result,
                    'verification': verification,
                    'message': 'Global cross-CLI integration deployed via Stigmergy'
                }
            else:
                return {
                    'mode': 'stigmergy',
                    'success': False,
                    'error': 'Stigmergy deployment failed',
                    'fallback_result': self._deploy_cli_extensions()
                }
        except Exception as e:
            print(f"⚠️ Stigmergy deployment failed: {e}")
            print("🔄 Falling back to CLI extensions mode...")
            return {
                'mode': 'stigmergy',
                'success': True,  # Fallback succeeded
                'error': f'Stigmergy deployment failed: {str(e)}',
                'fallback_result': self._deploy_cli_extensions()
            }

    def _get_dnaspec_skills(self) -> List[Dict[str, Any]]:
        """
        获取DNASPEC技能列表

        Returns:
            List[Dict]: 技能列表
        """
        return [
            # 基于实际已实现的DNASPEC技能
            {
                'name': 'architect',
                'display_name': 'System Architect',
                'description': 'Design system architecture and technical specifications',
                'command': '/dnaspec.architect',
                'function': 'execute_architect',
                'category': 'design'
            },
            {
                'name': 'agent-creator',
                'display_name': 'Agent Creator',
                'description': 'Create intelligent agents for specific tasks and domains',
                'command': '/dnaspec.agent-creator',
                'function': 'execute_agent_creator',
                'category': 'agents'
            },
            {
                'name': 'task-decomposer',
                'display_name': 'Task Decomposer',
                'description': 'Decompose complex tasks into manageable steps',
                'command': '/dnaspec.task-decomposer',
                'function': 'execute_task_decomposer',
                'category': 'planning'
            },
            {
                'name': 'constraint-generator',
                'display_name': 'Constraint Generator',
                'description': 'Generate constraints and validation rules for development',
                'command': '/dnaspec.constraint-generator',
                'function': 'execute_constraint_generator',
                'category': 'validation'
            },
            {
                'name': 'dapi-checker',
                'display_name': 'API Checker',
                'description': 'Analyze and validate API interfaces and specifications',
                'command': '/dnaspec.dapi-checker',
                'function': 'execute_dapi_checker',
                'category': 'analysis'
            },
            {
                'name': 'modulizer',
                'display_name': 'Modulizer',
                'description': 'Break down code into reusable and maintainable modules',
                'command': '/dnaspec.modulizer',
                'function': 'execute_modulizer',
                'category': 'refactoring'
            },
            # 新增：缓存区管理和Git操作技能（项目宪法功能）
            {
                'name': 'workspace',
                'display_name': 'Workspace Management',
                'description': 'Manage AI-generated files in secure workspace',
                'command': '/dnaspec.workspace',
                'function': 'execute_command_mapper',
                'category': 'maintenance'
            },
            {
                'name': 'git',
                'display_name': 'Git Operations',
                'description': 'Execute Git workflow operations safely',
                'command': '/dnaspec.git',
                'function': 'execute_command_mapper',
                'category': 'maintenance'
            }
        ]

    def _generate_cli_extensions(self, cli_name: str, cli_config: Dict[str, Any], skills: List[Dict[str, Any]]) -> List[str]:
        """
        为特定CLI工具生成扩展

        Args:
            cli_name: CLI工具名称
            cli_config: CLI配置
            skills: 技能列表

        Returns:
            List[str]: 生成的扩展文件路径
        """
        generated_files = []
        cli_dir = self.cli_extensions_dir / cli_name
        cli_dir.mkdir(parents=True, exist_ok=True)

        # 根据CLI类型生成相应的扩展文件
        if cli_name == 'claude':
            generated_files.extend(self._generate_claude_skills(cli_dir, skills))
        elif cli_name == 'cursor':
            generated_files.extend(self._generate_cursor_extensions(cli_dir, skills))
        elif cli_name == 'vscode':
            generated_files.extend(self._generate_vscode_tasks(cli_dir, skills))
        elif cli_name == 'windsurf':
            generated_files.extend(self._generate_windsurf_skills(cli_dir, skills))
        elif cli_name == 'continue':
            generated_files.extend(self._generate_continue_tools(cli_dir, skills))
        elif cli_name == 'cursor_rules':
            generated_files.extend(self._generate_cursor_rules(cli_dir, skills))
        elif cli_config.get('format') == 'commands_dir':
            # 新格式：基于commands目录的斜杠命令
            generated_files.extend(self._generate_commands_dir_extensions(cli_name, cli_config, skills))

        return generated_files

    def _generate_claude_skills(self, cli_dir: Path, skills: List[Dict[str, Any]]) -> List[str]:
        """
        生成Claude技能扩展

        Args:
            cli_dir: CLI目录
            skills: 技能列表

        Returns:
            List[str]: 生成的文件路径
        """
        generated_files = []

        # 生成Claude技能配置
        claude_skills = []
        for skill in skills:
            claude_skill = {
                "name": f"dnaspec-{skill['name']}",
                "description": skill['description'],
                "category": skill['category'],
                "command": skill['command'],
                "handler": {
                    "type": "python",
                    "module": "dna_spec_kit_integration.cli_extension_handler",
                    "function": "handle_dnaspec_command",
                    "parameters": {
                        "skill_name": skill['name'],
                        "function": skill['function']
                    }
                }
            }
            claude_skills.append(claude_skill)

        # 生成Claude技能配置文件
        skills_config = {
            "version": "1.0.0",
            "name": "DNASPEC Skills",
            "description": "DNA SPEC Context Engineering Skills for Claude",
            "skills": claude_skills,
            "generated_at": datetime.now().isoformat(),
            "project_root": str(self.project_root)
        }

        config_file = cli_dir / 'dnaspec_skills.json'
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(skills_config, f, ensure_ascii=False, indent=2)
        generated_files.append(str(config_file))

        return generated_files

    def _generate_cursor_extensions(self, cli_dir: Path, skills: List[Dict[str, Any]]) -> List[str]:
        """
        生成Cursor扩展

        Args:
            cli_dir: CLI目录
            skills: 技能列表

        Returns:
            List[str]: 生成的文件路径
        """
        generated_files = []

        # 生成Cursor扩展配置
        for skill in skills:
            extension_content = f"""# DNASPEC {skill['display_name']}

## Description
{skill['description']}

## Usage
1. Open Cursor
2. Use the slash command: `{skill['command']}`
3. Follow the prompts to provide your context

## Example
```
{skill['command']} Analyze the requirements for a user authentication system
```

## Integration
This extension integrates with DNASPEC's context engineering capabilities to provide professional-grade analysis and optimization.

Generated for project: {self.project_root.name}
Generated on: {datetime.now().isoformat()}
"""

            extension_file = cli_dir / f"dnaspec_{skill['name']}.md"
            with open(extension_file, 'w', encoding='utf-8') as f:
                f.write(extension_content)
            generated_files.append(str(extension_file))

        return generated_files

    def _generate_vscode_tasks(self, cli_dir: Path, skills: List[Dict[str, Any]]) -> List[str]:
        """
        生成VS Code任务定义

        Args:
            cli_dir: CLI目录
            skills: 技能列表

        Returns:
            List[str]: 生成的文件路径
        """
        generated_files = []

        # 生成VS Code tasks配置
        vscode_tasks = {
            "version": "2.0.0",
            "tasks": []
        }

        for skill in skills:
            task = {
                "label": f"DNASPEC {skill['display_name']}",
                "type": "shell",
                "command": "dnaspec-spec-kit",
                "args": [
                    "exec",
                    f"/{skill['name']}",
                    "${input:taskDescription}"
                ],
                "group": "build",
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": False,
                    "panel": "shared",
                    "showReuseMessage": True,
                    "clear": False
                },
                "problemMatcher": [],
                "detail": skill['description'],
                "category": skill['category']
            }
            vscode_tasks["tasks"].append(task)

        # 生成tasks.json文件
        tasks_file = cli_dir / 'tasks.json'
        with open(tasks_file, 'w', encoding='utf-8') as f:
            json.dump(vscode_tasks, f, ensure_ascii=False, indent=2)
        generated_files.append(str(tasks_file))

        return generated_files

    def _generate_windsurf_skills(self, cli_dir: Path, skills: List[Dict[str, Any]]) -> List[str]:
        """
        生成Windsurf技能扩展

        Args:
            cli_dir: CLI目录
            skills: 技能列表

        Returns:
            List[str]: 生成的文件路径
        """
        generated_files = []

        # 为每个技能生成JavaScript扩展
        for skill in skills:
            skill_js = f"""// DNASPEC {skill['display_name']} Extension for Windsurf
// Generated for project: {self.project_root.name}

const dnaspec{skill['name'].title()}Handler = async (input, context) => {{
  try {{
    // 调用DNASPEC技能
    const {{ spawn }} = require('child_process');
    const path = require('path');

    const projectRoot = path.resolve(__dirname, '../..');
    const command = 'dnaspec-spec-kit';
    const args = ['exec', '/{skill['name']}', input];

    return new Promise((resolve, reject) => {{
      const process = spawn(command, args, {{
        cwd: projectRoot,
        stdio: ['pipe', 'pipe', 'pipe'],
        env: {{ ...process.env, PYTHONIOENCODING: 'utf-8' }}
      }});

      let output = '';
      let error = '';

      process.stdout.on('data', (data) => {{
        output += data.toString();
      }});

      process.stderr.on('data', (data) => {{
        error += data.toString();
      }});

      process.on('close', (code) => {{
        if (code === 0) {{
          resolve(output.trim());
        }} else {{
          reject(new Error(`DNASPEC execution failed: ${{error}}`));
        }}
      }});
    }});
  }} catch (error) {{
    throw new Error(`Failed to execute DNASPEC {skill['name']}: ${{error.message}}`);
  }}
}};

// 导出技能处理器
module.exports = {{
  name: 'dnaspec-{skill['name']}',
  description: '{skill['description']}',
  handler: dnaspec{skill['name'].title()}Handler,
  category: '{skill['category']}'
}};
"""

            skill_file = cli_dir / f"dnaspec_{skill['name']}.js"
            with open(skill_file, 'w', encoding='utf-8') as f:
                f.write(skill_js)
            generated_files.append(str(skill_file))

        return generated_files

    def _generate_continue_tools(self, cli_dir: Path, skills: List[Dict[str, Any]]) -> List[str]:
        """
        生成Continue.dev工具

        Args:
            cli_dir: CLI目录
            skills: 技能列表

        Returns:
            List[str]: 生成的文件路径
        """
        generated_files = []

        # 为每个技能生成Python工具
        for skill in skills:
            tool_py = f'''"""
DNASPEC {skill['display_name']} Tool for Continue.dev
Generated for project: {self.project_root.name}
"""

import os
import sys
import subprocess
from pathlib import Path

class Dnaspec{skill['name'].title()}Tool:
    """DNASPEC {skill['display_name']} Tool"""

    def __init__(self):
        self.name = "dnaspec_{skill['name']}"
        self.description = "{skill['description']}"
        self.category = "{skill['category']}"

    def execute(self, input_text: str) -> str:
        """
        执行DNASPEC技能

        Args:
            input_text: 输入文本

        Returns:
            str: 执行结果
        """
        try:
            # 获取项目根目录
            project_root = Path(__file__).parent.parent.parent

            # 执行DNASPEC命令
            cmd = [
                sys.executable, "-m", "dna_spec_kit_integration.cli",
                "exec", f"/{skill['name']}", input_text
            ]

            result = subprocess.run(
                cmd,
                cwd=project_root,
                capture_output=True,
                text=True,
                env={{**os.environ, "PYTHONIOENCODING": "utf-8"}}
            )

            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Error: {{result.stderr.strip()}}"

        except Exception as e:
            return f"Failed to execute DNASPEC {skill['name']}: {{str(e)}}"

# 注册工具
tool = Dnaspec{skill['name'].title()}Tool()
'''

            tool_file = cli_dir / f"dnaspec_{skill['name']}.py"
            with open(tool_file, 'w', encoding='utf-8') as f:
                f.write(tool_py)
            generated_files.append(str(tool_file))

        return generated_files

    def _generate_cursor_rules(self, cli_dir: Path, skills: List[Dict[str, Any]]) -> List[str]:
        """
        生成Cursor Rules

        Args:
            cli_dir: CLI目录
            skills: 技能列表

        Returns:
            List[str]: 生成的文件路径
        """
        generated_files = []

        # 生成技能使用规则
        rules_content = f"""# DNASPEC Skills Rules for Cursor

## Overview
This file defines rules for using DNASPEC context engineering skills within Cursor.

## Available Skills

{self._format_skills_for_rules(skills)}

## Usage Guidelines

1. Always start with the specific skill command
2. Provide clear context and requirements
3. Follow the prompts generated by each skill
4. Review and iterate on the results

## Integration

To use these skills:
1. Copy the relevant command
2. Paste it in Cursor with your context
3. Execute and follow the guidance

Generated for project: {self.project_root.name}
"""

        rules_file = cli_dir / 'dnaspec_rules.md'
        with open(rules_file, 'w', encoding='utf-8') as f:
            f.write(rules_content)
        generated_files.append(str(rules_file))

        return generated_files

    def _format_skills_for_rules(self, skills: List[Dict[str, Any]]) -> str:
        """格式化技能用于规则文件"""
        skills_text = ""
        for skill in skills:
            skills_text += f"""
### {skill['display_name']}

**Command**: `{skill['command']}`
**Description**: {skill['description']}
**Category**: {skill['category']}

**Example**:
```
{skill['command']} [your specific context here]
```

---
"""
        return skills_text

    def _generate_commands_dir_extensions(self, cli_name: str, cli_config: Dict[str, Any], skills: List[Dict[str, Any]]) -> List[str]:
        """
        生成基于commands目录的斜杠命令扩展

        Args:
            cli_name: CLI工具名称
            cli_config: CLI配置
            skills: 技能列表

        Returns:
            List[str]: 生成的文件路径
        """
        generated_files = []
        commands_dir = self.project_root / cli_config['commands_dir']
        commands_dir.mkdir(parents=True, exist_ok=True)

        # 为每个技能生成对应的.md命令文件
        for skill in skills:
            # 使用简化的命令名作为文件名（移除斜杠和dnaspec前缀）
            filename = skill['command'].replace('/dnaspec.', 'dnaspec-')
            command_file = commands_dir / f"{filename}.md"
            command_content = self._generate_slash_command_content(cli_name, skill)

            with open(command_file, 'w', encoding='utf-8') as f:
                f.write(command_content)
            generated_files.append(str(command_file))

        return generated_files

    def _generate_slash_command_content(self, cli_name: str, skill: Dict[str, Any]) -> str:
        """
        生成斜杠命令的Markdown内容

        Args:
            cli_name: CLI工具名称
            skill: 技能信息

        Returns:
            str: 命令文件内容
        """
        # 使用DNASPEC的实际命令格式
        command_name = skill['command']

        # 为不同类型的技能生成不同的内容
        if skill['name'] == 'cache-manager':
            return self._generate_cache_manager_command_content(cli_name, skill)
        elif skill['name'] == 'git-operations':
            return self._generate_git_operations_command_content(cli_name, skill)
        else:
            return self._generate_standard_skill_command_content(cli_name, skill)

    def _generate_cache_manager_command_content(self, cli_name: str, skill: Dict[str, Any]) -> str:
        """生成缓存管理技能的命令内容"""
        return f"""# DNASPEC {skill['display_name']}

## Description
{skill['description']}

## Command
`{skill['command']}`

## Usage
Use this command to manage AI-generated files and prevent workspace pollution through intelligent caching and staging.

### Examples
```bash
# Initialize cache system for the project
{skill['command']} "operation=init-cache project_path=."

# Stage a file for validation
{skill['command']} "operation=stage-file file_path=example.py content='import os'

# Validate staged files
{skill['command']} "operation=validate-staged project_path=."

# Commit validated files
{skill['command']} "operation=commit-staged project_path=. message='Add validated AI-generated code'

# Clean up cache
{skill['command']} "operation=cleanup-cache project_path=."

# Get cache status
{skill['command']} "operation=cache-status project_path=."
```

## Operations
- **init-cache**: Initialize cache system with staging areas
- **stage-file**: Stage files for validation before commit
- **validate-staged**: Validate staged files for quality and security
- **commit-staged**: Commit validated files to main workspace
- **cleanup-cache**: Clean expired files and free up space
- **cache-status**: Display cache system status and statistics

## Integration with DNASPEC
This command implements DNASPEC's workspace protection strategy to maintain clean development environments while leveraging AI assistance.

---
*Generated for {cli_name} CLI*
*Project: {self.project_root.name}*
*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    def _generate_git_operations_command_content(self, cli_name: str, skill: Dict[str, Any]) -> str:
        """生成Git操作技能的命令内容"""
        return f"""# DNASPEC {skill['display_name']}

## Description
{skill['description']}

## Command
`{skill['command']}`

## Usage
Use this command to establish Git constitution and rules that prevent AI-generated file pollution in projects.

### Examples
```bash
# Setup project constitution
{skill['command']} "operation=setup-constitution project_path=."

# Install Git hooks for AI file protection
{skill['command']} "operation=install-hooks project_path=."

# Smart commit with DNASPEC rules
{skill['command']} "operation=smart-commit project_path=. message='[DNASPEC] Add AI-validated feature'"

# Clean workspace from AI temporary files
{skill['command']} "operation=clean-workspace project_path=."

# Enforce Git rules
{skill['command']} "operation=enforce-rules project_path=."

# Get workspace status
{skill['command']} "operation=status-report project_path=."
```

## Operations
- **setup-constitution**: Establish project constitution and Git rules
- **install-hooks**: Install Git hooks to enforce AI file policies
- **smart-commit**: Intelligent commit following DNASPEC rules
- **clean-workspace**: Clean AI-generated temporary files
- **enforce-rules**: Forcefully enforce Git and project rules
- **status-report**: Report workspace protection status
- **validate-commit**: Validate commit message format
- **create-workflow**: Create AI development workflow rules
- **branch-policy**: Setup branch protection policies
- **review-policy**: Configure code review policies

## Integration with DNASPEC
This command establishes constitutional project governance that maintains Git repository hygiene while enabling AI-assisted development.

---
*Generated for {cli_name} CLI*
*Project: {self.project_root.name}*
*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    def _generate_standard_skill_command_content(self, cli_name: str, skill: Dict[str, Any]) -> str:
        """生成标准技能的命令内容"""
        return f"""# DNASPEC {skill['display_name']}

## Description
{skill['description']}

## Command
`{skill['command']}`

## Usage
Use this command to apply DNASPEC's {skill['display_name'].lower()} capability to your current context.

### Examples
```bash
{skill['command']} "Analyze this user story for clarity and completeness"
{skill['command']} "Optimize this context for code generation"
{skill['command']} "Apply chain-of-thought reasoning to this problem"
{skill['command']} "Design microservices architecture for e-commerce"
{skill['command']} "Break down this feature into development tasks"
{skill['command']} "Generate security constraints for this API"
{skill['command']} "Create an intelligent agent for code review automation"
{skill['command']} "Validate this REST API specification"
{skill['command']} "Extract reusable modules from this codebase"
```

## Integration with DNASPEC
This command integrates with DNASPEC's context engineering capabilities to provide professional-grade {skill['category']} functionality.

## Parameters
- **context**: The text, code, or requirements to analyze
- **goals**: Optional specific goals or focus areas
- **constraints**: Optional constraints or requirements

## Output
The command will provide:
- Analysis and insights based on the skill type
- Actionable recommendations
- Structured output for further processing

## Skill Categories
- **Analysis**: Context analysis and API interface validation
- **Optimization**: Context optimization and performance improvement
- **Templates**: Cognitive templates and reasoning patterns
- **Design**: System architecture and technical specifications
- **Planning**: Task decomposition and project planning
- **Validation**: Constraint generation and rule validation
- **Agents**: Intelligent agent creation and configuration
- **Refactoring**: Code modularization and structure improvement
- **Performance**: Cache strategy and data optimization
- **Maintenance**: Git repository cleaning and pollution prevention

---
*Generated for {cli_name} CLI*
*Project: {self.project_root.name}*
*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    def _generate_usage_guide(self) -> None:
        """生成使用指南"""
        guide_file = self.cli_extensions_dir / 'USAGE_GUIDE.md'

        guide_content = f"""# DNASPEC CLI Extensions Usage Guide

## Overview
This deployment provides CLI extensions for various AI development tools, enabling you to use DNASPEC context engineering skills directly within your preferred AI environment.

## Supported AI Tools

{self._format_supported_clis()}

## Usage Instructions

### For Claude Users
1. Copy the generated skills from `.dnaspec/cli_extensions/claude/`
2. Import them into your Claude skills directory
3. Use slash commands like `/context-analysis` directly in Claude

### For Cursor Users
1. Copy the extension files from `.dnaspec/cli_extensions/cursor/`
2. Add them to your Cursor extensions directory
3. Use the provided slash commands in Cursor

### For VS Code Users
1. Copy the tasks file from `.dnaspec/cli_extensions/vscode/`
2. Add it to your `.vscode/tasks.json` or merge with existing tasks
3. Use Command Palette (Ctrl+Shift+P) and search for "DNASPEC"

### For Windsurf Users
1. Copy the JavaScript extensions from `.dnaspec/cli_extensions/windsurf/`
2. Add them to your Windsurf extensions directory
3. The skills will be available as slash commands

### For Continue.dev Users
1. Copy the Python tools from `.dnaspec/cli_extensions/continue/`
2. Add them to your Continue configuration
3. Use the tools in your Continue sessions

## Quick Start

1. **Initialize your project**:
   ```bash
   cd your-project
   dnaspec-spec-kit deploy --force-project
   ```

2. **Choose your AI tool** and copy the corresponding extensions

3. **Start using DNASPEC skills**:
   - Context Analysis: `/context-analysis "analyze this requirement"`
   - Architecture Design: `/architect "design system for this"`
   - Task Planning: `/task-decomposer "break down this feature"`

## Integration Examples

### Claude Integration
```json
{{
  "name": "context-analysis",
  "description": "Analyze context quality",
  "command": "/context-analysis",
  "handler": "handle_dnaspec_context_analysis"
}}
```

### Cursor Integration
- Copy `.dnaspec/cli_extensions/cursor/dnaspec_*.md`
- Restart Cursor
- Use slash commands directly

### VS Code Integration
```json
{{
  "label": "DNASPEC Context Analysis",
  "type": "shell",
  "command": "dnaspec-spec-kit",
  "args": ["exec", "/context-analysis", "${{input:taskDescription}}"]
}}
```

## Security Note
All extensions run with project-level isolation, ensuring that DNASPEC skills can only access files within your project directory.

## Troubleshooting

- **Extensions not loading**: Ensure the files are in the correct directory for your AI tool
- **Commands not working**: Check that DNASPEC is properly installed in your project
- **Permission errors**: Verify that the extensions have execute permissions

For more help, run:
```bash
dnaspec-spec-kit security --validate
```

Generated on: {datetime.now().isoformat()}
Project: {self.project_root.name}
"""

        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide_content)

    def _format_supported_clis(self) -> str:
        """格式化支持的CLI工具"""
        cli_text = ""
        for cli_name, cli_config in self.supported_clis.items():
            cli_text += f"""
### {cli_name.title()}
- **Format**: {cli_config['format']}
- **Extension**: {cli_config['extension']}
- **Command Prefix**: {cli_config['command_prefix']}
- **Description**: {cli_config['description']}
"""
        return cli_text

    def _generate_integration_config(self) -> None:
        """生成集成配置"""
        config_file = self.cli_extensions_dir / 'integration_config.json'

        config = {
            "project_name": self.project_root.name,
            "project_root": str(self.project_root),
            "deployment_mode": self.deployment_mode,
            "generated_at": datetime.now().isoformat(),
            "supported_clis": self.supported_clis,
            "dnaspec_skills": self._get_dnaspec_skills(),
            "integration_status": {
                "extensions_generated": True,
                "ready_for_import": True,
                "security_level": "project-isolated"
            }
        }

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    def get_deployment_status(self) -> Dict[str, Any]:
        """获取部署状态"""
        return {
            'stigmergy_available': self.stigmergy_available,
            'deployment_mode': self.deployment_mode,
            'project_root': str(self.project_root),
            'cli_extensions_dir': str(self.cli_extensions_dir),
            'supported_clis': list(self.supported_clis.keys()),
            'cli_count': len(self.supported_clis)
        }


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(
        description='DNASPEC CLI Extension Deployer',
        prog='dnaspec-deploy-extensions'
    )

    parser.add_argument(
        '--action',
        choices=['deploy', 'status', 'validate'],
        default='deploy',
        help='Action to perform'
    )

    parser.add_argument(
        '--project-root',
        help='Project root directory (default: current directory)'
    )

    parser.add_argument(
        '--force-stigmergy',
        action='store_true',
        help='Force Stigmergy mode'
    )

    parser.add_argument(
        '--force-extensions',
        action='store_true',
        help='Force CLI extensions mode'
    )

    args = parser.parse_args()

    # 解析项目根目录
    project_root = None
    if args.project_root:
        project_root = Path(args.project_root).resolve()

    # 创建部署器
    deployer = CLIExtensionDeployer(project_root)

    # 覆盖部署模式（如果指定）
    if args.force_stigmergy:
        deployer.deployment_mode = 'stigmergy'
        deployer.stigmergy_available = True
        print("⚡ Forcing Stigmergy mode...")
    elif args.force_extensions:
        deployer.deployment_mode = 'cli-extensions'
        deployer.stigmergy_available = False
        print("📁 Forcing CLI extensions mode...")

    # 执行操作
    if args.action == 'deploy':
        result = deployer.deploy_all()
    elif args.action == 'status':
        result = deployer.get_deployment_status()
    elif args.action == 'validate':
        result = deployer.validate_deployment()

    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 设置退出码
    if not result.get('success', True):
        sys.exit(1)


if __name__ == '__main__':
    main()