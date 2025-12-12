#!/usr/bin/env python3
"""
DNASPEC智能部署管理器
根据Stigmergy安装状态自动选择部署策略：
1. 无Stigmergy：项目级斜杠指令部署
2. 有Stigmergy：完整跨CLI插件部署
"""
import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime


class DeploymentManager:
    """
    DNASPEC智能部署管理器
    自动检测环境并选择最优部署策略
    """

    def __init__(self, project_root: Optional[Path] = None):
        """
        初始化部署管理器

        Args:
            project_root: 项目根目录，默认为当前目录
        """
        self.project_root = project_root or Path.cwd()
        self.stigmergy_available = self._check_stigmergy_availability()
        self.deployment_mode = self._determine_deployment_mode()

        # 部署目录配置
        self.project_slash_dir = self.project_root / '.dnaspec' / 'slash_commands'
        self.stigmergy_hooks_dir = Path.home() / '.stigmergy' / 'hooks'

        # 支持的CLI工具
        self.supported_clis = [
            'claude', 'gemini', 'qwen', 'iflow', 'qodercli',
            'codebuddy', 'copilot', 'codex', 'cursor'
        ]

    def _check_stigmergy_availability(self) -> bool:
        """
        检查Stigmergy是否可用

        Returns:
            bool: Stigmergy是否可用
        """
        try:
            # 方法1：直接调用stigmergy命令
            result = subprocess.run(
                ['stigmergy', '--version'],
                capture_output=True,
                text=True,
                timeout=10,
                shell=True
            )
            if result.returncode == 0:
                print(f"✅ Stigmergy detected: {result.stdout.strip()}")
                return True
        except (subprocess.SubprocessError, FileNotFoundError, OSError):
            pass

        try:
            # 方法2：通过npx调用stigmergy
            result = subprocess.run(
                ['npx', 'stigmergy', '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print(f"✅ Stigmergy detected via npx: {result.stdout.strip()}")
                return True
        except (subprocess.SubprocessError, FileNotFoundError, OSError):
            pass

        # 方法3：检查全局包安装
        try:
            result = subprocess.run(
                ['npm', 'list', '-g', 'stigmergy'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print("✅ Stigmergy detected in global npm packages")
                return True
        except (subprocess.SubprocessError, FileNotFoundError, OSError):
            pass

        print("ℹ️  Stigmergy not detected - will use project-level slash commands")
        return False

    def _determine_deployment_mode(self) -> str:
        """
        确定部署模式

        Returns:
            str: 部署模式 ('stigmergy' 或 'project-level')
        """
        if self.stigmergy_available:
            return 'stigmergy'
        else:
            return 'project-level'

    def deploy_all(self) -> Dict[str, Any]:
        """
        执行完整部署流程

        Returns:
            Dict: 部署结果
        """
        print(f"🚀 DNASPEC Deployment Manager")
        print(f"📍 Project Root: {self.project_root}")
        print(f"🔧 Deployment Mode: {self.deployment_mode}")
        print(f"📋 Stigmergy Available: {self.stigmergy_available}")
        print("-" * 60)

        if self.deployment_mode == 'stigmergy':
            return self._deploy_with_stigmergy()
        else:
            return self._deploy_project_level()

    def _deploy_with_stigmergy(self) -> Dict[str, Any]:
        """
        使用Stigmergy进行完整部署

        Returns:
            Dict: 部署结果
        """
        print("🔌 Deploying with Stigmergy (full cross-CLI integration)...")

        from .stigmergy_adapter import StigmergyAdapter

        # 创建Stigmergy适配器
        adapter = StigmergyAdapter()

        # 部署到所有CLI工具
        result = adapter.deploy_to_all_clis()

        if result.get('success'):
            print(f"✅ Stigmergy deployment completed!")
            print(f"📊 Successfully deployed to {result.get('successful_deployments', 0)}/{result.get('total_platforms', 0)} platforms")

            # 验证部署
            verification = adapter.verify_deployment()
            deployed_clis = verification.get('deployed_clis', [])
            if deployed_clis:
                print(f"🎯 Active CLI integrations: {', '.join(deployed_clis)}")

            return {
                'mode': 'stigmergy',
                'success': True,
                'deployment_result': result,
                'verification': verification,
                'message': 'Full cross-CLI integration deployed via Stigmergy'
            }
        else:
            print("❌ Stigmergy deployment failed!")
            return {
                'mode': 'stigmergy',
                'success': False,
                'error': 'Stigmergy deployment failed',
                'fallback_result': self._deploy_project_level()
            }

    def _deploy_project_level(self) -> Dict[str, Any]:
        """
        项目级斜杠指令部署

        Returns:
            Dict: 部署结果
        """
        print("📁 Deploying project-level slash commands...")

        # 创建项目级斜杠指令目录
        self.project_slash_dir.mkdir(parents=True, exist_ok=True)

        deployed_skills = []
        deployment_errors = []

        # 为每个技能生成项目级斜杠指令
        skills = self._get_dnaspec_skills()

        for skill in skills:
            try:
                skill_files = self._generate_project_skill_files(skill)
                deployed_skills.extend(skill_files)
                print(f"✅ Generated slash commands for {skill['name']}")
            except Exception as e:
                deployment_errors.append(f"Failed to generate {skill['name']}: {str(e)}")
                print(f"❌ Failed to generate {skill['name']}: {e}")

        # 生成CLI集成指南
        self._generate_integration_guide()

        # 生成AI工具配置文件
        self._generate_ai_tool_configs()

        success_count = len(deployed_skills)
        total_count = len(skills)

        print(f"\n📊 Project-level deployment completed!")
        print(f"✅ Successfully deployed: {success_count}/{total_count} skills")
        print(f"📂 Slash commands location: {self.project_slash_dir}")

        if deployment_errors:
            print(f"⚠️  Errors: {len(deployment_errors)}")
            for error in deployment_errors:
                print(f"   - {error}")

        return {
            'mode': 'project-level',
            'success': success_count > 0,
            'deployed_skills': deployed_skills,
            'deployment_errors': deployment_errors,
            'slash_commands_dir': str(self.project_slash_dir),
            'message': f'Project-level slash commands deployed for {success_count} skills'
        }

    def _get_dnaspec_skills(self) -> List[Dict[str, Any]]:
        """
        获取DNASPEC技能列表

        Returns:
            List[Dict]: 技能列表
        """
        return [
            {
                'name': 'context-analysis',
                'description': 'Analyze context quality across 5 dimensions',
                'command': '/speckit.dnaspec.context-analysis',
                'function': 'execute_context_analysis'
            },
            {
                'name': 'context-optimization',
                'description': 'Optimize context based on specific goals',
                'command': '/speckit.dnaspec.context-optimization',
                'function': 'execute_context_optimization'
            },
            {
                'name': 'cognitive-template',
                'description': 'Apply cognitive templates (CoT, verification, etc.)',
                'command': '/speckit.dnaspec.cognitive-template',
                'function': 'execute_cognitive_template'
            },
            {
                'name': 'architect',
                'description': 'Design system architecture and specifications',
                'command': '/speckit.dnaspec.architect',
                'function': 'execute_architect'
            },
            {
                'name': 'task-decomposer',
                'description': 'Decompose complex tasks into manageable steps',
                'command': '/speckit.dnaspec.task-decomposer',
                'function': 'execute_task_decomposer'
            },
            {
                'name': 'constraint-generator',
                'description': 'Generate constraints and validation rules',
                'command': '/speckit.dnaspec.constraint-generator',
                'function': 'execute_constraint_generator'
            }
        ]

    def _generate_project_skill_files(self, skill: Dict[str, Any]) -> List[str]:
        """
        为单个技能生成项目级文件

        Args:
            skill: 技能定义

        Returns:
            List[str]: 生成的文件路径列表
        """
        skill_name = skill['name']
        skill_dir = self.project_slash_dir / skill_name
        skill_dir.mkdir(exist_ok=True)

        generated_files = []

        # 1. 生成Python技能执行器
        executor_file = skill_dir / f'{skill_name}_executor.py'
        executor_code = self._generate_skill_executor_code(skill)
        with open(executor_file, 'w', encoding='utf-8') as f:
            f.write(executor_code)
        generated_files.append(str(executor_file))

        # 2. 生成CLI包装脚本
        wrapper_file = skill_dir / f'{skill_name}.cmd'
        wrapper_code = self._generate_wrapper_code(skill)
        with open(wrapper_file, 'w', encoding='utf-8') as f:
            f.write(wrapper_code)
        generated_files.append(str(wrapper_file))

        # 3. 生成Bash版本包装脚本（Linux/Mac兼容）
        bash_wrapper = skill_dir / f'{skill_name}.sh'
        bash_code = self._generate_bash_wrapper_code(skill)
        with open(bash_wrapper, 'w', encoding='utf-8') as f:
            f.write(bash_code)
        os.chmod(bash_wrapper, 0o755)
        generated_files.append(str(bash_wrapper))

        # 4. 生成技能配置文件
        config_file = skill_dir / 'config.json'
        config_data = {
            'skill': skill,
            'generated_at': datetime.now().isoformat(),
            'project_root': str(self.project_root),
            'deployment_mode': 'project-level'
        }
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
        generated_files.append(str(config_file))

        return generated_files

    def _generate_skill_executor_code(self, skill: Dict[str, Any]) -> str:
        """
        生成技能执行器代码

        Args:
            skill: 技能定义

        Returns:
            str: Python代码
        """
        function_name = skill['function']
        skill_description = skill['description']

        return f'''#!/usr/bin/env python3
"""
DNASPEC {skill['name']} Skill Executor
{skill_description}

Generated by DNASPEC Deployment Manager
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

try:
    from dna_context_engineering.skills_system_final import {function_name}
except ImportError:
    print(f"Error: DNASPEC skills module not found. Please ensure dnaspec is properly installed.")
    sys.exit(1)


def execute_{skill['name']}(task: str, **kwargs):
    """
    执行{skill['name']}技能

    Args:
        task: 任务描述
        **kwargs: 额外参数

    Returns:
        技能执行结果
    """
    try:
        # 设置默认参数
        params = {{
            'template': 'verification',
            'context': task,
            **kwargs
        }}

        # 执行技能
        result = {function_name}(task)
        return result

    except Exception as e:
        return f"Error executing {skill['name']}: {{str(e)}}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python {skill['name']}_executor.py \\"<task>\\" [param1=value1 param2=value2]")
        sys.exit(1)

    task = " ".join(sys.argv[1:-len([arg for arg in sys.argv[1:] if '=' in arg])])

    # 解析参数
    kwargs = {{}}
    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            kwargs[key] = value

    # 执行技能
    result = execute_{skill['name']}(task, **kwargs)
    print(result)
'''

    def _generate_wrapper_code(self, skill: Dict[str, Any]) -> str:
        """
        生成Windows CMD包装脚本

        Args:
            skill: 技能定义

        Returns:
            str: CMD脚本代码
        """
        return f'''@echo off
REM DNASPEC {skill['name']} Wrapper
REM Usage: {skill['name']}.cmd "your task here" [param1=value1 param2=value2]

setlocal

REM 获取脚本所在目录
set SCRIPT_DIR=%~dp0
set EXECUTOR=%SCRIPT_DIR%{skill['name']}_executor.py

REM 检查Python是否可用
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.8+
    exit /b 1
)

REM 检查执行器文件是否存在
if not exist "%EXECUTOR%" (
    echo Error: Skill executor not found at %EXECUTOR%
    exit /b 1
)

REM 执行技能
python "%EXECUTOR%" %*

endlocal
'''

    def _generate_bash_wrapper_code(self, skill: Dict[str, Any]) -> str:
        """
        生成Bash包装脚本

        Args:
            skill: 技能定义

        Returns:
            str: Bash脚本代码
        """
        return f'''#!/bin/bash
# DNASPEC {skill['name']} Wrapper
# Usage: {skill['name']}.sh "your task here" [param1=value1 param2=value2]

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
EXECUTOR="$SCRIPT_DIR/{skill['name']}_executor.py"

# 检查Python是否可用
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python not found. Please install Python 3.8+"
    exit 1
fi

# 选择Python命令
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

# 检查执行器文件是否存在
if [[ ! -f "$EXECUTOR" ]]; then
    echo "Error: Skill executor not found at $EXECUTOR"
    exit 1
fi

# 执行技能
"$PYTHON_CMD" "$EXECUTOR" "$@"
'''

    def _generate_integration_guide(self) -> None:
        """
        生成集成指南
        """
        guide_file = self.project_slash_dir / 'INTEGRATION_GUIDE.md'

        guide_content = f'''# DNASPEC Project-Level Integration Guide

## Overview
This deployment provides project-level slash commands for DNASPEC skills. These can be used with any AI CLI tool that supports custom commands or external tool integration.

## Generated Slash Commands

The following commands are available in the `.dnaspec/slash_commands/` directory:

'''

        skills = self._get_dnaspec_skills()
        for skill in skills:
            skill_name = skill['name']
            guide_content += f'''
### {skill['command']}
- **Description**: {skill['description']}
- **Windows Usage**: `.dnaspec/slash_commands/{skill_name}/{skill_name}.cmd "your task here"`
- **Linux/Mac Usage**: `.dnaspec/slash_commands/{skill_name}/{skill_name}.sh "your task here"`
- **Example**: `.dnaspec/slash_commands/{skill_name}/{skill_name}.cmd "Analyze this codebase for security issues"`

'''

        guide_content += f'''
## Integration with AI CLI Tools

### Claude/Cursor
Add these commands to your AI tool's command palette or create custom shortcuts:
- Command: `{skill['command']}`
- Action: Execute `.dnaspec/slash_commands/{skill_name}/{skill_name}.cmd "$INPUT"`
- Description: {skill['description']}

### VS Code Extensions
Create VS Code tasks in `.vscode/tasks.json`:
```json
{{
    "version": "2.0.0",
    "tasks": [
{', '.join([f'''
        {{
            "label": "DNASPEC {s['name']}",
            "type": "shell",
            "command": "{self.project_slash_dir.relative_to(self.project_root) / s['name'] / (s['name'] + '.cmd')}",
            "args": ["${{input:taskDescription}}"],
            "group": "build"
        }}''' for s in skills[:3]])}
    ]
}}
```

### Shell Aliases
Add to your `.bashrc` or `.zshrc`:
```bash
# DNASPEC aliases
{chr(10).join([f'alias dnaspec-{s["name"]}="{self.project_slash_dir / s["name"] / (s["name"] + ".sh")}"' for s in skills[:3]])}
```

## Configuration

The configuration files are located in:
- Skill configs: `.dnaspec/slash_commands/*/config.json`
- Project settings: `.dnaspec/slash_commands/project_settings.json`

## Example Usage

1. **Context Analysis**:
   ```bash
   .dnaspec/slash_commands/context-analysis/context-analysis.cmd "Analyze the requirements for this user authentication system"
   ```

2. **System Architecture**:
   ```bash
   .dnaspec/slash_commands/architect/architect.cmd "Design a microservices architecture for an e-commerce platform"
   ```

3. **Task Decomposition**:
   ```bash
   .dnaspec/slash_commands/task-decomposer/task-decomposer.cmd "Break down this project into manageable development tasks"
   ```

## Full Stigmergy Integration

If you want full cross-CLI integration with automatic skill recognition, install Stigmergy:
```bash
npm install -g stigmergy
dnaspec deploy  # Will automatically switch to Stigmergy mode
```

Generated on: {datetime.now().isoformat()}
Deployment mode: {self.deployment_mode}
'''

        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide_content)

    def _generate_ai_tool_configs(self) -> None:
        """
        生成AI工具配置文件
        """
        configs_dir = self.project_slash_dir / 'ai_configs'
        configs_dir.mkdir(exist_ok=True)

        # 生成Claude配置
        claude_config = {
            "name": "dnaspec-project-skills",
            "version": "1.0.0",
            "description": "DNASPEC project-level skills",
            "commands": []
        }

        skills = self._get_dnaspec_skills()
        for skill in skills:
            skill_path = self.project_slash_dir / skill['name'] / f"{skill['name']}.cmd"
            claude_config["commands"].append({
                "name": skill['command'],
                "description": skill['description'],
                "executable": str(skill_path),
                "args": ["$INPUT"]
            })

        with open(configs_dir / 'claude_config.json', 'w', encoding='utf-8') as f:
            json.dump(claude_config, f, ensure_ascii=False, indent=2)

        # 生成通用配置模板
        generic_config = {
            "skills": skills,
            "deployment_mode": "project-level",
            "generated_at": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "slash_commands_root": str(self.project_slash_dir),
            "integration_instructions": {
                "step1": "Add .dnaspec/slash_commands to your PATH",
                "step2": "Use skill commands directly: context-analysis.cmd 'your task'",
                "step3": "Integrate with AI tools using the generated configs"
            }
        }

        with open(configs_dir / 'integration_config.json', 'w', encoding='utf-8') as f:
            json.dump(generic_config, f, ensure_ascii=False, indent=2)

    def verify_deployment(self) -> Dict[str, Any]:
        """
        验证部署状态

        Returns:
            Dict: 验证结果
        """
        if self.deployment_mode == 'stigmergy':
            from .stigmergy_adapter import StigmergyAdapter
            adapter = StigmergyAdapter()
            return adapter.verify_deployment()
        else:
            return self._verify_project_deployment()

    def _verify_project_deployment(self) -> Dict[str, Any]:
        """
        验证项目级部署状态

        Returns:
            Dict: 验证结果
        """
        if not self.project_slash_dir.exists():
            return {
                'success': False,
                'error': 'Slash commands directory not found',
                'deployment_mode': 'project-level'
            }

        # 检查技能文件
        skills = self._get_dnaspec_skills()
        deployed_skills = []
        missing_skills = []

        for skill in skills:
            skill_dir = self.project_slash_dir / skill['name']
            executor_file = skill_dir / f'{skill["name"]}_executor.py'
            wrapper_file = skill_dir / f'{skill["name"]}.cmd'

            if skill_dir.exists() and executor_file.exists() and wrapper_file.exists():
                deployed_skills.append(skill['name'])
            else:
                missing_skills.append(skill['name'])

        return {
            'success': len(deployed_skills) > 0,
            'deployment_mode': 'project-level',
            'deployed_skills': deployed_skills,
            'missing_skills': missing_skills,
            'total_skills': len(skills),
            'slash_commands_dir': str(self.project_slash_dir),
            'deployment_status': f'{len(deployed_skills)}/{len(skills)} skills deployed'
        }

    def get_deployment_status(self) -> Dict[str, Any]:
        """
        获取部署状态信息

        Returns:
            Dict: 部署状态
        """
        return {
            'stigmergy_available': self.stigmergy_available,
            'deployment_mode': self.deployment_mode,
            'project_root': str(self.project_root),
            'stigmergy_hooks_dir': str(self.stigmergy_hooks_dir),
            'project_slash_dir': str(self.project_slash_dir),
            'supported_clis': self.supported_clis
        }


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(
        description='DNASPEC Intelligent Deployment Manager',
        prog='dnaspec-deploy'
    )

    parser.add_argument(
        '--action',
        choices=['deploy', 'verify', 'status'],
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
        help='Force Stigmergy mode even if not detected'
    )

    parser.add_argument(
        '--force-project',
        action='store_true',
        help='Force project-level mode even if Stigmergy is available'
    )

    args = parser.parse_args()

    # 解析项目根目录
    project_root = None
    if args.project_root:
        project_root = Path(args.project_root).resolve()

    # 创建部署管理器
    manager = DeploymentManager(project_root)

    # 覆盖部署模式（如果指定）
    if args.force_stigmergy:
        manager.deployment_mode = 'stigmergy'
        manager.stigmergy_available = True
        print("⚡ Forcing Stigmergy mode...")
    elif args.force_project:
        manager.deployment_mode = 'project-level'
        manager.stigmergy_available = False
        print("📁 Forcing project-level mode...")

    # 执行操作
    if args.action == 'deploy':
        result = manager.deploy_all()
    elif args.action == 'verify':
        result = manager.verify_deployment()
    elif args.action == 'status':
        result = manager.get_deployment_status()

    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 设置退出码
    if not result.get('success', True):
        sys.exit(1)


if __name__ == '__main__':
    main()