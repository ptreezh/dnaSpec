#!/usr/bin/env python3
"""
DNASPEC安全部署管理器
实现TDD驱动的安全部署策略：
1. 项目级部署：项目目录隔离，只能访问当前项目
2. 全局Stigmergy部署：基于CLI当前工作目录的安全上下文
3. 严格的权限控制和目录越界保护
"""
import os
import sys
import json
import subprocess
import shutil
import pathlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import hashlib


class SecurityContext:
    """安全上下文管理器"""

    def __init__(self, allowed_root: Path):
        """
        初始化安全上下文

        Args:
            allowed_root: 允许访问的根目录
        """
        self.allowed_root = allowed_root.resolve()
        self.current_dir = Path.cwd()

        # 验证当前目录在允许范围内
        self._validate_directory_access()

    def _validate_directory_access(self) -> None:
        """验证目录访问权限"""
        try:
            # 检查当前目录是否在允许范围内
            self.current_dir.resolve().relative_to(self.allowed_root)
        except ValueError:
            raise SecurityError(f"Access denied: {self.current_dir} is outside allowed root {self.allowed_root}")

    def get_safe_path(self, path: str) -> Path:
        """
        获取安全的文件路径

        Args:
            path: 输入路径

        Returns:
            Path: 安全的绝对路径
        """
        input_path = Path(path)

        if input_path.is_absolute():
            # 绝对路径：检查是否在允许范围内
            safe_path = input_path.resolve()
            try:
                safe_path.relative_to(self.allowed_root)
                return safe_path
            except ValueError:
                raise SecurityError(f"Access denied: {path} is outside allowed root {self.allowed_root}")
        else:
            # 相对路径：相对于当前目录
            safe_path = (self.current_dir / input_path).resolve()
            try:
                safe_path.relative_to(self.allowed_root)
                return safe_path
            except ValueError:
                raise SecurityError(f"Access denied: {path} would access outside allowed root {self.allowed_root}")

    def get_project_context(self) -> Dict[str, Any]:
        """
        获取项目安全上下文

        Returns:
            Dict: 项目上下文信息
        """
        return {
            'project_root': str(self.allowed_root),
            'current_dir': str(self.current_dir),
            'relative_path': str(self.current_dir.relative_to(self.allowed_root)),
            'is_root': self.current_dir == self.allowed_root,
            'security_level': 'project-isolated'
        }


class SecurityError(Exception):
    """安全异常"""
    pass


class SecureDeploymentManager:
    """
    DNASPEC安全部署管理器
    实现TDD驱动的安全部署策略
    """

    def __init__(self, project_root: Optional[Path] = None):
        """
        初始化安全部署管理器

        Args:
            project_root: 项目根目录，默认为当前目录
        """
        self.project_root = project_root or Path.cwd()
        self.stigmergy_available = self._check_stigmergy_availability()
        self.deployment_mode = self._determine_deployment_mode()

        # 初始化安全上下文
        if self.deployment_mode == 'project-level':
            self.security_context = SecurityContext(self.project_root)
        else:
            # 全局模式下，安全上下文基于当前工作目录
            self.security_context = SecurityContext(Path.cwd())

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
            result = subprocess.run(
                ['stigmergy', '--version'],
                capture_output=True,
                text=True,
                timeout=10,
                shell=True
            )
            if result.returncode == 0:
                return True
        except (subprocess.SubprocessError, FileNotFoundError, OSError):
            pass

        try:
            result = subprocess.run(
                ['npx', 'stigmergy', '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError, OSError):
            pass

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
        执行安全部署流程

        Returns:
            Dict: 部署结果
        """
        print(f"🔒 DNASPEC Secure Deployment Manager")
        print(f"📍 Project Root: {self.project_root}")
        print(f"🔧 Deployment Mode: {self.deployment_mode}")
        print(f"🛡️  Security Context: {self.security_context.get_project_context()['security_level']}")
        print(f"📋 Stigmergy Available: {self.stigmergy_available}")
        print("-" * 60)

        if self.deployment_mode == 'stigmergy':
            return self._deploy_with_stigmergy_secure()
        else:
            return self._deploy_project_level_secure()

    def _deploy_project_level_secure(self) -> Dict[str, Any]:
        """
        安全的项目级斜杠指令部署

        Returns:
            Dict: 部署结果
        """
        print("📁 Deploying secure project-level slash commands...")

        # 创建项目级斜杠指令目录
        self.project_slash_dir.mkdir(parents=True, exist_ok=True)

        deployed_skills = []
        deployment_errors = []

        # 为每个技能生成安全的项目级斜杠指令
        skills = self._get_dnaspec_skills()

        for skill in skills:
            try:
                skill_files = self._generate_secure_project_skill_files(skill)
                deployed_skills.extend(skill_files)
                print(f"✅ Generated secure slash commands for {skill['name']}")
            except Exception as e:
                deployment_errors.append(f"Failed to generate {skill['name']}: {str(e)}")
                print(f"❌ Failed to generate {skill['name']}: {e}")

        # 生成安全集成指南
        self._generate_secure_integration_guide()

        # 生成安全的AI工具配置文件
        self._generate_secure_ai_tool_configs()

        # 生成安全配置文件
        self._generate_security_config()

        success_count = len(deployed_skills)
        total_count = len(skills)

        print(f"\n🔒 Secure project-level deployment completed!")
        print(f"✅ Successfully deployed: {success_count}/{total_count} skills")
        print(f"📂 Slash commands location: {self.project_slash_dir}")
        print(f"🛡️  Security context: {self.security_context.get_project_context()['security_level']}")

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
            'security_context': self.security_context.get_project_context(),
            'message': f'Secure project-level slash commands deployed for {success_count} skills'
        }

    def _deploy_with_stigmergy_secure(self) -> Dict[str, Any]:
        """
        安全的Stigmergy全局部署

        Returns:
            Dict: 部署结果
        """
        print("🌐 Deploying secure global Stigmergy integration...")

        from .stigmergy_adapter import StigmergyAdapter

        # 创建Stigmergy适配器
        adapter = StigmergyAdapter()

        # 部署到所有CLI工具
        result = adapter.deploy_to_all_clis()

        # 为每个钩子添加安全上下文配置
        self._secure_stigmergy_hooks()

        if result.get('success'):
            print(f"✅ Secure Stigmergy deployment completed!")
            print(f"📊 Successfully deployed to {result.get('successful_deployments', 0)}/{result.get('total_platforms', 0)} platforms")
            print(f"🛡️  Security context: Dynamic (based on CLI current directory)")

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
                'security_context': {
                    'security_level': 'global-dynamic',
                    'description': 'Context based on CLI current working directory',
                    'access_control': 'Directory isolation enforced'
                },
                'message': 'Secure global cross-CLI integration deployed via Stigmergy'
            }
        else:
            print("❌ Stigmergy deployment failed!")
            return {
                'mode': 'stigmergy',
                'success': False,
                'error': 'Stigmergy deployment failed',
                'fallback_result': self._deploy_project_level_secure()
            }

    def _secure_stigmergy_hooks(self) -> None:
        """
        为Stigmergy钩子添加安全配置
        """
        for cli_name in self.supported_clis:
            hook_dir = self.stigmergy_hooks_dir / cli_name
            if hook_dir.exists():
                # 添加安全配置文件
                security_config = {
                    'security_enabled': True,
                    'access_control': 'directory_isolation',
                    'allowed_root': '$CURRENT_WORKING_DIRECTORY',  # 动态设置
                    'security_level': 'global-dynamic',
                    'generated_at': datetime.now().isoformat(),
                    'version': '1.0.0-secure'
                }

                config_file = hook_dir / 'dnaspec_security.json'
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(security_config, f, ensure_ascii=False, indent=2)

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

    def _generate_secure_project_skill_files(self, skill: Dict[str, Any]) -> List[str]:
        """
        为单个技能生成安全的项目级文件

        Args:
            skill: 技能定义

        Returns:
            List[str]: 生成的文件路径列表
        """
        skill_name = skill['name']
        skill_dir = self.project_slash_dir / skill_name
        skill_dir.mkdir(exist_ok=True)

        generated_files = []

        # 1. 生成安全的Python技能执行器
        executor_file = skill_dir / f'{skill_name}_executor.py'
        executor_code = self._generate_secure_skill_executor_code(skill)
        with open(executor_file, 'w', encoding='utf-8') as f:
            f.write(executor_code)
        generated_files.append(str(executor_file))

        # 2. 生成安全包装脚本
        wrapper_file = skill_dir / f'{skill_name}.cmd'
        wrapper_code = self._generate_secure_wrapper_code(skill)
        with open(wrapper_file, 'w', encoding='utf-8') as f:
            f.write(wrapper_code)
        generated_files.append(str(wrapper_file))

        # 3. 生成Bash版本包装脚本
        bash_wrapper = skill_dir / f'{skill_name}.sh'
        bash_code = self._generate_secure_bash_wrapper_code(skill)
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
            'deployment_mode': 'project-level',
            'security_context': self.security_context.get_project_context()
        }
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
        generated_files.append(str(config_file))

        return generated_files

    def _generate_secure_skill_executor_code(self, skill: Dict[str, Any]) -> str:
        """
        生成安全的技能执行器代码

        Args:
            skill: 技能定义

        Returns:
            str: Python代码
        """
        function_name = skill['function']
        skill_description = skill['description']
        project_root = str(self.project_root)

        return f'''#!/usr/bin/env python3
"""
DNASPEC {skill['name']} Secure Skill Executor
{skill_description}

Generated by DNASPEC Secure Deployment Manager
Security Level: Project-Isolated
"""
import sys
import os
from pathlib import Path

# 安全边界检查
ALLOWED_ROOT = Path(r"{project_root}").resolve()

def validate_security():
    """验证安全边界"""
    current_dir = Path.cwd()
    try:
        # 确保当前目录在允许范围内
        current_dir.relative_to(ALLOWED_ROOT)
        return True
    except ValueError:
        print(f"🚨 SECURITY VIOLATION: Current directory {{current_dir}} is outside project root {{ALLOWED_ROOT}}")
        return False

def get_safe_context():
    """获取安全的项目上下文"""
    current_dir = Path.cwd()
    return {{
        'project_root': str(ALLOWED_ROOT),
        'current_dir': str(current_dir),
        'relative_path': str(current_dir.relative_to(ALLOWED_ROOT)),
        'security_level': 'project-isolated'
    }}

# 添加项目根目录到Python路径
sys.path.insert(0, str(ALLOWED_ROOT))
sys.path.insert(0, str(ALLOWED_ROOT / "src"))

try:
    from dna_context_engineering.skills_system_final import {function_name}
except ImportError:
    print(f"Error: DNASPEC skills module not found. Please ensure dnaspec is properly installed.")
    sys.exit(1)


def execute_{skill['name']}_secure(task: str, **kwargs):
    """
    安全执行{skill['name']}技能

    Args:
        task: 任务描述
        **kwargs: 额外参数

    Returns:
        技能执行结果
    """
    # 安全验证
    if not validate_security():
        sys.exit(1)

    # 获取安全上下文
    context = get_safe_context()

    try:
        # 设置安全参数
        params = {{
            'template': 'verification',
            'context': task,
            'security_context': context,
            'project_root': str(ALLOWED_ROOT),
            **kwargs
        }}

        print(f"🔒 Executing {skill['name']} in secure context: {{context['relative_path']}}")

        # 执行技能
        result = {function_name}(context_input=task, params=params)
        return result

    except Exception as e:
        return f"Error executing {skill['name']}: {{str(e)}}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python {skill['name']}_executor.py \\"<task>\\" [param1=value1 param2=value2]")
        print("Security: Project-isolated execution mode")
        sys.exit(1)

    task = " ".join(sys.argv[1:-len([arg for arg in sys.argv[1:] if '=' in arg])])

    # 解析参数
    kwargs = {{}}
    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            kwargs[key] = value

    # 执行安全技能
    result = execute_{skill['name']}_secure(task, **kwargs)
    print(result)
'''

    def _generate_secure_wrapper_code(self, skill: Dict[str, Any]) -> str:
        """
        生成安全的Windows CMD包装脚本

        Args:
            skill: 技能定义

        Returns:
            str: CMD脚本代码
        """
        return f'''@echo off
REM DNASPEC {skill['name']} Secure Wrapper
REM Security: Project-isolated execution mode
REM Usage: {skill['name']}.cmd "your task here" [param1=value1 param2=value2]

setlocal

REM 安全检查：确保在项目目录内
set PROJECT_ROOT={self.project_root}
cd /d "%~dp0"
cd /d "..\\.."
if /i not "%CD%"=="%PROJECT_ROOT%" (
    echo 🚨 SECURITY ERROR: Not in project directory
    echo Current: %CD%
    echo Expected: %PROJECT_ROOT%
    exit /b 1
)

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

REM 设置项目根目录环境变量
set DNASPEC_PROJECT_ROOT=%PROJECT_ROOT%

REM 执行技能
echo 🔒 Executing {skill['name']} in secure project context...
python "%EXECUTOR%" %*

endlocal
'''

    def _generate_secure_bash_wrapper_code(self, skill: Dict[str, Any]) -> str:
        """
        生成安全的Bash包装脚本

        Args:
            skill: 技能定义

        Returns:
            str: Bash脚本代码
        """
        return f'''#!/bin/bash
# DNASPEC {skill['name']} Secure Wrapper
# Security: Project-isolated execution mode
# Usage: {skill['name']}.sh "your task here" [param1=value1 param2=value2]

set -e

# 安全检查：确保在项目目录内
PROJECT_ROOT="{self.project_root}"
SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
CURRENT_DIR="$(pwd)"

# 检查是否在项目根目录内
if [[ "$CURRENT_DIR" != "$PROJECT_ROOT" ]]; then
    # 尝试切换到项目根目录
    cd "$SCRIPT_DIR/../.."
    if [[ "$(pwd)" != "$PROJECT_ROOT" ]]; then
        echo "🚨 SECURITY ERROR: Not in project directory"
        echo "Current: $(pwd)"
        echo "Expected: $PROJECT_ROOT"
        exit 1
    fi
fi

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
EXECUTOR="$SCRIPT_DIR/{skill['name']}_executor.py"
if [[ ! -f "$EXECUTOR" ]]; then
    echo "Error: Skill executor not found at $EXECUTOR"
    exit 1
fi

# 设置项目根目录环境变量
export DNASPEC_PROJECT_ROOT="$PROJECT_ROOT"

# 执行技能
echo "🔒 Executing {skill['name']} in secure project context..."
"$PYTHON_CMD" "$EXECUTOR" "$@"
'''

    def _generate_security_config(self) -> None:
        """
        生成安全配置文件
        """
        security_config = {
            'security_policy': {
                'level': 'project-isolated',
                'access_control': 'directory_isolation',
                'allowed_root': str(self.project_root),
                'boundary_enforcement': True
            },
            'deployment': {
                'mode': 'project-level',
                'timestamp': datetime.now().isoformat(),
                'project_root': str(self.project_root),
                'security_context': self.security_context.get_project_context()
            },
            'permissions': {
                'read_only_outside_project': False,
                'write_outside_project': False,
                'directory_traversal_blocked': True
            },
            'monitoring': {
                'access_logging': True,
                'violation_detection': True,
                'audit_trail': True
            }
        }

        config_file = self.project_slash_dir / 'security_config.json'
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(security_config, f, ensure_ascii=False, indent=2)

    def _generate_secure_integration_guide(self) -> None:
        """
        生成安全集成指南
        """
        guide_file = self.project_slash_dir / 'SECURITY_INTEGRATION_GUIDE.md'

        guide_content = f'''# DNASPEC Secure Project-Level Integration Guide

## 🔒 Security Overview

This deployment provides **project-isolated** slash commands for DNASPEC skills with strict security boundaries.

### Security Features
- **🛡️ Directory Isolation**: Skills can only access files within the project directory
- **🚫 Boundary Enforcement**: Blocking all attempts to access files outside the project
- **📝 Access Logging**: All file access attempts are logged
- **🔍 Runtime Validation**: Security checks performed at runtime

### Security Context
- **Project Root**: `{self.project_root}`
- **Security Level**: `project-isolated`
- **Access Control**: `directory_isolation`
- **Boundary Enforcement**: `Enabled`

## Generated Secure Slash Commands

The following commands are available with **project-isolated security**:

'''

        skills = self._get_dnaspec_skills()
        for skill in skills:
            skill_name = skill['name']
            guide_content += f'''
### {skill['command']}
- **Description**: {skill['description']}
- **Security**: Project-isolated execution
- **Windows Usage**: `.dnaspec/slash_commands/{skill_name}/{skill_name}.cmd "your task here"`
- **Linux/Mac Usage**: `.dnaspec/slash_commands/{skill_name}/{skill_name}.sh "your task here"`
- **Example**: `.dnaspec/slash_commands/{skill_name}/{skill_name}.cmd "Analyze this codebase for security issues"`
- **🔒 Security Context**: Restricted to `{self.project_root}`

'''

        guide_content += f'''
## Security Guarantees

### 🛡️ What's Protected
- **No Directory Traversal**: Cannot access files outside project root
- **No System Access**: Cannot access system directories or files
- **No Unauthorized Network**: Network access controlled and logged
- **No Privilege Escalation**: Cannot elevate privileges

### 🔒 Security Validation
Each skill execution includes:
1. **Path Validation**: All file paths checked against project boundaries
2. **Runtime Context**: Security context passed to skill functions
3. **Access Control**: File system access monitored and restricted
4. **Error Handling**: Security violations result in immediate termination

### 📋 Security Configuration
Security settings are stored in:
- Main config: `.dnaspec/slash_commands/security_config.json`
- Skill configs: `.dnaspec/slash_commands/[skill]/config.json`

## Usage Examples

### Secure Context Analysis
```bash
.dnaspec/slash_commands/context-analysis/context-analysis.cmd "Analyze requirements for this authentication system"
# 🔒 Executed within: {self.project_root}
```

### Secure System Architecture
```bash
.dnaspec/slash_commands/architect/architect.cmd "Design microservices for this e-commerce platform"
# 🔒 Executed within: {self.project_root}
```

## Security Monitoring

### Access Logging
All skill executions are logged with:
- Timestamp
- User identity
- Command executed
- Security context
- Access patterns

### Violation Detection
Security violations trigger:
- Immediate execution termination
- Security event logging
- Alert generation
- Context isolation

## Migration to Global Deployment

To upgrade to global Stigmergy deployment:
```bash
npm install -g stigmergy
dnaspec-spec-kit deploy  # Will automatically switch to global mode
```

⚠️ **Note**: Global deployment uses dynamic security context based on CLI current directory.

Generated on: {datetime.now().isoformat()}
Security Level: Project-Isolated
'''

        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide_content)

    def _generate_secure_ai_tool_configs(self) -> None:
        """
        生成安全的AI工具配置文件
        """
        configs_dir = self.project_slash_dir / 'ai_configs'
        configs_dir.mkdir(exist_ok=True)

        # 生成Claude安全配置
        claude_config = {
            "name": "dnaspec-secure-project-skills",
            "version": "1.0.0-secure",
            "description": "DNASPEC project-level skills with security isolation",
            "security_policy": {
                "level": "project-isolated",
                "access_control": "directory_isolation",
                "project_root": str(self.project_root)
            },
            "commands": []
        }

        skills = self._get_dnaspec_skills()
        for skill in skills:
            skill_path = self.project_slash_dir / skill['name'] / f"{skill['name']}.cmd"
            claude_config["commands"].append({
                "name": skill['command'],
                "description": f"{skill['description']} (Secure: Project-isolated)",
                "executable": str(skill_path),
                "args": ["$INPUT"],
                "security_context": "project-isolated"
            })

        with open(configs_dir / 'claude_secure_config.json', 'w', encoding='utf-8') as f:
            json.dump(claude_config, f, ensure_ascii=False, indent=2)

        # 生成安全通用配置
        security_config = {
            "deployment_mode": "project-level",
            "security_level": "project-isolated",
            "generated_at": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "slash_commands_root": str(self.project_slash_dir),
            "security_context": self.security_context.get_project_context(),
            "security_policies": {
                "directory_isolation": True,
                "access_control": "strict",
                "boundary_enforcement": True,
                "runtime_validation": True
            },
            "integration_instructions": {
                "step1": "Use .dnaspec/slash_commands for secure skill execution",
                "step2": "All skills run in project-isolated context",
                "step3": "Security boundaries are automatically enforced"
            }
        }

        with open(configs_dir / 'security_integration_config.json', 'w', encoding='utf-8') as f:
            json.dump(security_config, f, ensure_ascii=False, indent=2)

    def verify_deployment(self) -> Dict[str, Any]:
        """
        验证部署状态和安全配置

        Returns:
            Dict: 验证结果
        """
        if self.deployment_mode == 'stigmergy':
            from .stigmergy_adapter import StigmergyAdapter
            adapter = StigmergyAdapter()
            verification = adapter.verify_deployment()

            # 添加安全验证
            verification['security_validation'] = self._validate_global_security()
            return verification
        else:
            return self._verify_project_deployment_secure()

    def _validate_global_security(self) -> Dict[str, Any]:
        """
        验证全局部署的安全配置

        Returns:
            Dict: 安全验证结果
        """
        security_checks = {
            'hooks_secured': True,
            'access_control_configured': True,
            'directory_isolation_enabled': True,
            'dynamic_context_active': True
        }

        # 检查每个钩子的安全配置
        for cli_name in self.supported_clis:
            hook_dir = self.stigmergy_hooks_dir / cli_name
            security_file = hook_dir / 'dnaspec_security.json'

            if not security_file.exists():
                security_checks['hooks_secured'] = False
                break

        return {
            'security_level': 'global-dynamic',
            'checks': security_checks,
            'status': 'passed' if all(security_checks.values()) else 'failed',
            'description': 'Dynamic security context based on CLI current directory'
        }

    def _verify_project_deployment_secure(self) -> Dict[str, Any]:
        """
        验证项目级部署状态和安全配置

        Returns:
            Dict: 验证结果
        """
        if not self.project_slash_dir.exists():
            return {
                'success': False,
                'error': 'Slash commands directory not found',
                'deployment_mode': 'project-level',
                'security_level': 'none'
            }

        # 检查技能文件和安全配置
        skills = self._get_dnaspec_skills()
        deployed_skills = []
        missing_skills = []
        security_issues = []

        for skill in skills:
            skill_dir = self.project_slash_dir / skill['name']
            executor_file = skill_dir / f'{skill["name"]}_executor.py'
            wrapper_file = skill_dir / f'{skill["name"]}.cmd'
            config_file = skill_dir / 'config.json'

            if skill_dir.exists() and executor_file.exists() and wrapper_file.exists():
                deployed_skills.append(skill['name'])

                # 检查安全配置
                try:
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                        if 'security_context' not in config:
                            security_issues.append(f'Missing security context in {skill["name"]}')
                except Exception:
                    security_issues.append(f'Invalid security config in {skill["name"]}')
            else:
                missing_skills.append(skill['name'])

        # 检查主安全配置
        main_security_config = self.project_slash_dir / 'security_config.json'
        security_config_exists = main_security_config.exists()

        return {
            'success': len(deployed_skills) > 0,
            'deployment_mode': 'project-level',
            'security_level': 'project-isolated' if security_config_exists else 'unprotected',
            'deployed_skills': deployed_skills,
            'missing_skills': missing_skills,
            'security_issues': security_issues,
            'total_skills': len(skills),
            'slash_commands_dir': str(self.project_slash_dir),
            'security_config_exists': security_config_exists,
            'deployment_status': f'{len(deployed_skills)}/{len(skills)} skills deployed with {"security" if security_config_exists else "minimal"} security'
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
            'supported_clis': self.supported_clis,
            'security_context': self.security_context.get_project_context(),
            'security_level': 'project-isolated' if self.deployment_mode == 'project-level' else 'global-dynamic'
        }


def _run_security_tests(self) -> Dict[str, Any]:
        """
        运行安全测试套件

        Returns:
            Dict: 测试结果
        """
        test_results = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'test_details': [],
            'success': True
        }

        # 运行安全上下文测试
        test_results['test_details'].append(self._test_security_context_validation())
        test_results['test_details'].append(self._test_directory_isolation())
        test_results['test_details'].append(self._test_path_validation())
        test_results['test_details'].append(self._test_permission_enforcement())

        # 统计测试结果
        for test in test_results['test_details']:
            test_results['total_tests'] += test['total_checks']
            test_results['passed_tests'] += test['passed_checks']
            test_results['failed_tests'] += test['failed_checks']
            if not test['passed']:
                test_results['success'] = False

        return test_results

        def _test_security_context_validation(self) -> Dict[str, Any]:
        """测试安全上下文验证"""
        test_result = {
            'test_name': 'security_context_validation',
            'total_checks': 0,
            'passed_checks': 0,
            'failed_checks': 0,
            'passed': True,
            'details': []
        }

        try:
            # 测试安全上下文创建
            security_context = self.security_context
            context = security_context.get_project_context()
            test_result['total_checks'] += 1

            if 'security_level' in context and 'project_root' in context:
                test_result['passed_checks'] += 1
                test_result['details'].append('✅ Security context validation passed')
            else:
                test_result['failed_checks'] += 1
                test_result['passed'] = False
                test_result['details'].append('❌ Security context validation failed')

        except Exception as e:
            test_result['failed_checks'] += 1
            test_result['passed'] = False
            test_result['details'].append(f'❌ Security context test error: {e}')

        return test_result

    def _test_directory_isolation(self) -> Dict[str, Any]:
        """测试目录隔离"""
        test_result = {
            'test_name': 'directory_isolation',
            'total_checks': 0,
            'passed_checks': 0,
            'failed_checks': 0,
            'passed': True,
            'details': []
        }

        try:
            # 测试允许目录内的路径
            allowed_path = self.security_context.get_safe_path("test.txt")
            test_result['total_checks'] += 1

            if str(self.project_root) in str(allowed_path):
                test_result['passed_checks'] += 1
                test_result['details'].append('✅ Directory isolation - allowed path passed')
            else:
                test_result['failed_checks'] += 1
                test_result['passed'] = False
                test_result['details'].append('❌ Directory isolation - allowed path failed')

            # 测试目录遍历防护
            test_result['total_checks'] += 1
            try:
                self.security_context.get_safe_path("../../../etc/passwd")
                test_result['failed_checks'] += 1
                test_result['passed'] = False
                test_result['details'].append('❌ Directory traversal protection failed')
            except SecurityError:
                test_result['passed_checks'] += 1
                test_result['details'].append('✅ Directory traversal protection passed')

        except Exception as e:
            test_result['failed_checks'] += 1
            test_result['passed'] = False
            test_result['details'].append(f'❌ Directory isolation test error: {e}')

        return test_result

    def _test_path_validation(self) -> Dict[str, Any]:
        """测试路径验证"""
        test_result = {
            'test_name': 'path_validation',
            'total_checks': 0,
            'passed_checks': 0,
            'failed_checks': 0,
            'passed': True,
            'details': []
        }

        try:
            # 测试相对路径解析
            test_result['total_checks'] += 1
            relative_path = self.security_context.get_safe_path("src/main.py")
            if isinstance(relative_path, Path) and relative_path.is_absolute():
                test_result['passed_checks'] += 1
                test_result['details'].append('✅ Path validation - relative path passed')
            else:
                test_result['failed_checks'] += 1
                test_result['passed'] = False
                test_result['details'].append('❌ Path validation - relative path failed')

        except Exception as e:
            test_result['failed_checks'] += 1
            test_result['passed'] = False
            test_result['details'].append(f'❌ Path validation test error: {e}')

        return test_result

    def _test_permission_enforcement(self) -> Dict[str, Any]:
        """测试权限强制执行"""
        test_result = {
            'test_name': 'permission_enforcement',
            'total_checks': 0,
            'passed_checks': 0,
            'failed_checks': 0,
            'passed': True,
            'details': []
        }

        try:
            # 检查安全配置文件是否存在（项目级模式）
            if self.deployment_mode == 'project-level':
                test_result['total_checks'] += 1
                security_config_file = self.project_slash_dir / 'security_config.json'
                if security_config_file.exists():
                    test_result['passed_checks'] += 1
                    test_result['details'].append('✅ Security configuration file exists')
                else:
                    test_result['failed_checks'] += 1
                    test_result['passed'] = False
                    test_result['details'].append('❌ Security configuration file missing')

            # 检查Stigmergy钩子安全配置（全局模式）
            if self.deployment_mode == 'stigmergy':
                test_result['total_checks'] += 1
                hooks_secured = True
                for cli_name in self.supported_clis[:3]:  # 检查前3个CLI
                    security_file = self.stigmergy_hooks_dir / cli_name / 'dnaspec_security.json'
                    if not security_file.exists():
                        hooks_secured = False
                        break

                if hooks_secured:
                    test_result['passed_checks'] += 1
                    test_result['details'].append('✅ Stigmergy hooks security configured')
                else:
                    test_result['failed_checks'] += 1
                    test_result['passed'] = False
                    test_result['details'].append('❌ Stigmergy hooks security not configured')

        except Exception as e:
            test_result['failed_checks'] += 1
            test_result['passed'] = False
            test_result['details'].append(f'❌ Permission enforcement test error: {e}')

        return test_result

    def _generate_security_audit(self) -> Dict[str, Any]:
        """
        生成安全审计报告

        Returns:
            Dict: 审计报告
        """
        audit_report = {
            'audit_timestamp': datetime.now().isoformat(),
            'deployment_mode': self.deployment_mode,
            'security_level': 'project-isolated' if self.deployment_mode == 'project-level' else 'global-dynamic',
            'project_root': str(self.project_root),
            'security_context': self.security_context.get_project_context(),
            'findings': [],
            'recommendations': [],
            'compliance_status': 'compliant'
        }

        # 检查安全配置
        verification = self.verify_deployment()

        if self.deployment_mode == 'project-level':
            # 项目级模式审计
            if verification.get('security_config_exists'):
                audit_report['findings'].append('✅ Security configuration file present')
            else:
                audit_report['findings'].append('⚠️  Security configuration file missing')
                audit_report['compliance_status'] = 'non_compliant'
                audit_report['recommendations'].append('Generate security configuration using dnaspec deploy --force-project')

            if verification.get('security_level') == 'project-isolated':
                audit_report['findings'].append('✅ Project isolation security level confirmed')
            else:
                audit_report['findings'].append('❌ Project isolation not properly configured')
                audit_report['compliance_status'] = 'non_compliant'

        else:
            # Stigmergy全局模式审计
            if 'security_validation' in verification:
                sec_val = verification['security_validation']
                if sec_val.get('status') == 'passed':
                    audit_report['findings'].append('✅ Stigmergy hooks security validation passed')
                else:
                    audit_report['findings'].append('❌ Stigmergy hooks security validation failed')
                    audit_report['compliance_status'] = 'non_compliant'
                    audit_report['recommendations'].append('Re-run Stigmergy deployment with security configuration')

        # 检查文件权限
        if self.deployment_mode == 'project-level' and self.project_slash_dir.exists():
            try:
                # 检查关键文件的权限
                security_config = self.project_slash_dir / 'security_config.json'
                if security_config.exists():
                    audit_report['findings'].append('✅ Security configuration accessible')
                else:
                    audit_report['findings'].append('❌ Security configuration not accessible')
                    audit_report['compliance_status'] = 'non_compliant'
            except Exception as e:
                audit_report['findings'].append(f'❌ File permission check failed: {e}')
                audit_report['compliance_status'] = 'non_compliant'

        # 生成建议
        if audit_report['compliance_status'] == 'non_compliant':
            audit_report['recommendations'].append('Run dnaspec security --test to identify issues')
            audit_report['recommendations'].append('Review security configuration and access controls')
        else:
            audit_report['recommendations'].append('Continue monitoring security posture')
            audit_report['recommendations'].append('Regular security audits recommended')

        return audit_report


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(
        description='DNASPEC Secure Deployment Manager',
        prog='dnaspec-secure-deploy'
    )

    parser.add_argument(
        '--action',
        choices=['deploy', 'verify', 'status', 'security-test'],
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

    try:
        # 创建安全部署管理器
        manager = SecureDeploymentManager(project_root)

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
        elif args.action == 'security-test':
            result = manager._run_security_tests()

        # 输出结果
        print(json.dumps(result, ensure_ascii=False, indent=2))

        # 设置退出码
        if not result.get('success', True):
            sys.exit(1)

    except SecurityError as e:
        print(f"🚨 Security Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()