#!/usr/bin/env python3
"""
修复DNASPEC与AI CLI工具的集成问题
实现真正可用的技能部署
"""
import os
import sys
import json
import shutil
from pathlib import Path
from typing import Dict, Any, List

# 确保模块路径正确
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir / 'src'))

from dna_spec_kit_integration.core.cli_detector import CliDetector


class DNASPECIntegrationFixer:
    """DNASPEC集成修复器"""

    def __init__(self):
        self.cli_detector = CliDetector()
        self.skills = [
            {
                'name': 'context-analysis',
                'display_name': 'Context Analysis',
                'description': 'Analyze context quality across 5 dimensions',
                'command': '/speckit.dnaspec.context-analysis'
            },
            {
                'name': 'context-optimization',
                'display_name': 'Context Optimization',
                'description': 'Optimize context quality with AI-driven improvements',
                'command': '/speckit.dnaspec.context-optimization'
            },
            {
                'name': 'cognitive-template',
                'display_name': 'Cognitive Template',
                'description': 'Apply cognitive frameworks to structure complex tasks',
                'command': '/speckit.dnaspec.cognitive-template'
            },
            {
                'name': 'architect',
                'display_name': 'System Architect',
                'description': 'Design system architecture and components',
                'command': '/speckit.dnaspec.architect'
            },
            {
                'name': 'git-operations',
                'display_name': 'Git Operations',
                'description': 'Execute Git workflow operations',
                'command': '/speckit.dnaspec.git-skill'
            },
            {
                'name': 'temp-workspace',
                'display_name': 'Temporary Workspace',
                'description': 'Manage AI-generated files safely',
                'command': '/speckit.dnaspec.temp-workspace'
            }
        ]

    def fix_integration(self):
        """修复所有检测到的平台的集成"""
        print("🔧 DNASPEC Integration Fixer")
        print("=" * 40)

        # 检测已安装的平台
        detected_tools = self.cli_detector.detect_all()
        available_platforms = [
            name for name, result in detected_tools.items()
            if result.get('installed', False)
        ]

        if not available_platforms:
            print("❌ No AI CLI tools detected")
            return False

        print(f"✅ Detected platforms: {', '.join(available_platforms)}")

        # 为每个平台生成真实可用的集成
        success_count = 0
        for platform in available_platforms:
            try:
                if platform == 'claude':
                    self._fix_claude_integration()
                    success_count += 1
                elif platform == 'qwen':
                    self._fix_qwen_integration()
                    success_count += 1
                elif platform in ['gemini', 'iflow', 'qodercli', 'codebuddy']:
                    self._fix_commands_dir_integration(platform)
                    success_count += 1
                else:
                    print(f"⚠️  Platform {platform} not yet supported for real integration")

            except Exception as e:
                print(f"❌ Failed to fix {platform}: {e}")

        # 生成统一的执行脚本
        self._generate_unified_executor()

        print(f"\n✅ Successfully fixed {success_count}/{len(available_platforms)} platforms")
        print("\n📖 Next steps:")
        print("1. Restart your AI CLI tools")
        print("2. Try commands like: /speckit.dnaspec.context-analysis 'your text'")
        print("3. Check logs in .dnaspec/logs/ if issues occur")

        return success_count > 0

    def _fix_claude_integration(self):
        """修复Claude CLI集成 - 生成真实可执行的技能"""
        print("🔧 Fixing Claude CLI integration...")

        claude_skills_dir = Path.home() / '.claude' / 'skills'
        claude_skills_dir.mkdir(parents=True, exist_ok=True)

        # 生成DNASPEC主技能
        main_skill_dir = claude_skills_dir / 'dnaspec-context-engineering'
        main_skill_dir.mkdir(exist_ok=True)

        skill_content = '''# DNASPEC Context Engineering Skills

Professional context analysis, optimization, and cognitive template application for AI-assisted development.

## Skills Available

### Context Analysis
Analyzes context quality across 5 dimensions: clarity, relevance, completeness, consistency, efficiency.

**Command**: `/speckit.dnaspec.context-analysis "your context here"`

### Context Optimization
Optimizes context quality based on specific goals (clarity, completeness, etc.).

**Command**: `/speckit.dnaspec.context-optimization "your context" goals=clarity,completeness`

### Cognitive Template
Applies professional cognitive frameworks (Chain-of-Thought, Verification, etc.).

**Command**: `/speckit.dnaspec.cognitive-template "your task" template=verification`

### System Architect
Designs system architecture and components.

**Command**: `/speckit.dnaspec.architect "design a system for X"`

### Git Operations
Manages Git workflow operations safely.

**Command**: `/speckit.dnaspec.git-skill operation=status`

### Temporary Workspace
Manages AI-generated files in isolated workspace.

**Command**: `/speckit.dnaspec.temp-workspace operation=create`

## Implementation

```python
import subprocess
import sys
import re
import json
from pathlib import Path

def execute_dnaspec_command(user_input: str) -> str:
    """Execute DNASPEC command and return results"""

    # 解析命令
    if not user_input.strip().startswith('/speckit.dnaspec.'):
        return "Please use a valid DNASPEC command starting with /speckit.dnaspec.*"

    # 提取技能名称和参数
    match = re.match(r'/speckit\.dnaspec\.(\w+)\s*(.*)', user_input.strip())
    if not match:
        return "Invalid DNASPEC command format"

    skill_name = match.group(1)
    args = match.group(2)

    try:
        # 执行DNASPEC技能
        result = subprocess.run([
            sys.executable, '-c', f'''
import sys
import os
sys.path.insert(0, "{Path(__file__).parent.parent.parent}")

from dna_context_engineering.skills_system_final import execute as execute_skill

# 准备参数
params = {{}}
if "template=" in "{args}":
    template = "{args}".split("template=")[1].split()[0]
    params["template"] = template

if "goals=" in "{args}":
    goals = "{args}".split("goals=")[1].split()[0]
    params["optimization_goals"] = goals.split(",")

if "operation=" in "{args}":
    operation = "{args}".split("operation=")[1].split()[0]
    params["operation"] = operation

# 执行技能
try:
    if "{skill_name}" == "context-analysis":
        result = execute_skill({{"skill": "context-analysis", "context": "{args}"}})
    elif "{skill_name}" == "context-optimization":
        result = execute_skill({{"skill": "context-optimization", "context": "{args}", "params": params}})
    elif "{skill_name}" == "cognitive-template":
        result = execute_skill({{"skill": "cognitive-template", "context": "{args}", "params": params}})
    elif "{skill_name}" == "architect":
        result = execute_skill({{"skill": "architect", "context": "{args}"}})
    elif "{skill_name}" == "git-operations":
        result = execute_skill({{"skill": "git-operations", "context": "{args}", "params": params}})
    elif "{skill_name}" == "temp-workspace":
        result = execute_skill({{"skill": "temp-workspace", "context": "{args}", "params": params}})
    else:
        result = f"Unknown skill: {skill_name}"

    print(result)
except Exception as e:
    print(f"Skill execution error: {{str(e)}}")
'''
        ], capture_output=True, text=True, timeout=30, cwd=Path.cwd())

        return result.stdout if result.returncode == 0 else result.stderr

    except subprocess.TimeoutExpired:
        return "DNASPEC skill execution timed out (30s)"
    except Exception as e:
        return f"Error executing DNASPEC skill: {str(e)}"

# 主要执行逻辑
user_input = """{{USER_INPUT}}"""
result = execute_dnaspec_command(user_input)
print(result)
```

## Examples

1. **Context Analysis**: `/speckit.dnaspec.context-analysis "Design a user authentication system with login, registration, and password recovery"`

2. **Architecture Design**: `/speckit.dnaspec.architect "Create a microservices architecture for an e-commerce platform"`

3. **Cognitive Template**: `/speckit.dnaspec.cognitive-template "Analyze this system design for potential issues" template=verification`

4. **Git Operations**: `/speckit.dnaspec.git-skill operation=commit message="feat: add authentication system"`

5. **Workspace Management**: `/speckit.dnaspec.temp-workspace operation=create`
'''

        with open(main_skill_dir / 'SKILL.md', 'w', encoding='utf-8') as f:
            f.write(skill_content)

        print("✅ Claude CLI skill installed to ~/.claude/skills/dnaspec-context-engineering/")

    def _fix_qwen_integration(self):
        """修复Qwen CLI集成 - 生成可安装的扩展"""
        print("🔧 Fixing Qwen CLI integration...")

        # 创建Qwen扩展目录结构
        qwen_ext_dir = Path.cwd() / '.dnaspec' / 'qwen-extension'
        qwen_ext_dir.mkdir(parents=True, exist_ok=True)

        # 生成package.json
        package_json = {
            "name": "dnaspec-context-engineering",
            "version": "1.0.0",
            "description": "DNASPEC Context Engineering Skills for Qwen CLI",
            "main": "index.js",
            "qwen": {
                "type": "extension",
                "commands": [
                    {
                        "name": "dnaspec-context-analysis",
                        "description": "Analyze context quality across 5 dimensions"
                    },
                    {
                        "name": "dnaspec-context-optimization",
                        "description": "Optimize context quality with AI-driven improvements"
                    },
                    {
                        "name": "dnaspec-cognitive-template",
                        "description": "Apply cognitive frameworks to structure tasks"
                    },
                    {
                        "name": "dnaspec-architect",
                        "description": "Design system architecture and components"
                    },
                    {
                        "name": "dnaspec-git-skill",
                        "description": "Execute Git workflow operations"
                    },
                    {
                        "name": "dnaspec-temp-workspace",
                        "description": "Manage AI-generated files safely"
                    }
                ]
            }
        }

        with open(qwen_ext_dir / 'package.json', 'w') as f:
            json.dump(package_json, f, indent=2)

        # 生成主执行文件
        index_js = '''const {{ spawn }} = require('child_process');
const path = require('path');

// DNASPEC技能执行器
class DNASPECExecutor {
    constructor() {{
        this.projectRoot = process.cwd();
    }}

    async executeCommand(command, args) {{
        return new Promise((resolve, reject) => {{
            const python = spawn('python', [
                '-c', `
import sys
import os
sys.path.insert(0, "${this.projectRoot}/src")

from dna_context_engineering.skills_system_final import execute as execute_skill

skill_map = {
    'context-analysis': 'context-analysis',
    'context-optimization': 'context-optimization',
    'cognitive-template': 'cognitive-template',
    'architect': 'architect',
    'git-skill': 'git-operations',
    'temp-workspace': 'temp-workspace'
}

skill_name = skill_map.get('${command}', '${command}')
input_text = "${args}"

try:
    result = execute_skill({
        'skill': skill_name,
        'context': input_text
    })
    print(result)
except Exception as e:
    print(f"Error: {str(e)}")
`
            ], {{
                cwd: this.projectRoot,
                stdio: ['pipe', 'pipe', 'pipe']
            }});

            let stdout = '';
            let stderr = '';

            python.stdout.on('data', (data) => {{
                stdout += data.toString();
            }});

            python.stderr.on('data', (data) => {{
                stderr += data.toString();
            }});

            python.on('close', (code) => {{
                if (code === 0) {{
                    resolve(stdout.trim());
                }} else {{
                    reject(new Error(stderr || 'Execution failed'));
                }}
            }});
        }});
    }}
}}

// Qwen扩展入口
module.exports = async function(input, context) {{
    const executor = new DNASPECExecutor();

    // 解析命令
    const commandPattern = /\\/dnaspec-(\\w+)(?:\\s+(.+))?/;
    const match = input.match(commandPattern);

    if (match) {{
        const [, command, args = ''] = match;
        try {{
            const result = await executor.executeCommand(command, args);
            return result;
        }} catch (error) {{
            return `DNASPEC Error: ${{error.message}}`;
        }}
    }}

    return input;
}};

// 导出命令处理器
module.exports.commands = {
    'dnaspec-context-analysis': async (args) => {{
        const executor = new DNASPECExecutor();
        return await executor.executeCommand('context-analysis', args.join(' '));
    }},
    'dnaspec-context-optimization': async (args) => {{
        const executor = new DNASPECExecutor();
        return await executor.executeCommand('context-optimization', args.join(' '));
    }},
    'dnaspec-cognitive-template': async (args) => {{
        const executor = new DNASPECExecutor();
        return await executor.executeCommand('cognitive-template', args.join(' '));
    }},
    'dnaspec-architect': async (args) => {{
        const executor = new DNASPECExecutor();
        return await executor.executeCommand('architect', args.join(' '));
    }},
    'dnaspec-git-skill': async (args) => {{
        const executor = new DNASPECExecutor();
        return await executor.executeCommand('git-skill', args.join(' '));
    }},
    'dnaspec-temp-workspace': async (args) => {{
        const executor = new DNASPECExecutor();
        return await executor.executeCommand('temp-workspace', args.join(' '));
    }}
};
'''

        with open(qwen_ext_dir / 'index.js', 'w') as f:
            f.write(index_js)

        print("✅ Qwen CLI extension created at .dnaspec/qwen-extension/")
        print("💡 Install with: qwen extensions install .dnaspec/qwen-extension")

    def _fix_commands_dir_integration(self, platform: str):
        """修复基于commands目录的工具集成（Gemini, IFlow等）"""
        print(f"🔧 Fixing {platform} integration...")

        commands_dir = Path.cwd() / f'.{platform}' / 'commands'
        commands_dir.mkdir(parents=True, exist_ok=True)

        # 生成可执行的命令脚本而不是文档
        for skill in self.skills:
            script_name = skill['command'].replace('/speckit.dnaspec.', 'dnaspec-')
            script_file = commands_dir / f'{script_name}.py'

            script_content = f'''#!/usr/bin/env python3
"""
DNASPEC {skill['display_name']} - {platform} Integration
Executable command script for {platform} CLI
"""

import sys
import os
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / 'src'))

def main():
    """主执行函数"""
    if len(sys.argv) < 2:
        print("Usage: {script_name} <input_text>")
        return 1

    input_text = ' '.join(sys.argv[1:])

    try:
        from dna_context_engineering.skills_system_final import execute as execute_skill

        # 准备执行参数
        skill_params = {{
            'skill': '{skill["name"]}',
            'context': input_text
        }}

        # 执行技能
        result = execute_skill(skill_params)
        print(result)
        return 0

    except Exception as e:
        print(f"Error executing {skill['name']}: {{str(e)}}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
'''

            with open(script_file, 'w', encoding='utf-8') as f:
                f.write(script_content)

            # 设置可执行权限
            script_file.chmod(0o755)

        print(f"✅ {platform} commands created in .{platform}/commands/")

    def _generate_unified_executor(self):
        """生成统一执行脚本"""
        print("🔧 Generating unified DNASPEC executor...")

        dnaspec_dir = Path.cwd() / '.dnaspec'
        dnaspec_dir.mkdir(exist_ok=True)

        executor_script = '''#!/usr/bin/env python3
"""
DNASPEC Unified Executor
统一的DNASPEC技能执行器
"""

import sys
import os
import re
import json
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

def execute_dnaspec_skill(skill_name: str, input_text: str, params: dict = None) -> str:
    """执行DNASPEC技能"""

    try:
        from dna_context_engineering.skills_system_final import execute as execute_skill

        skill_params = {
            'skill': skill_name,
            'context': input_text,
            'params': params or {}
        }

        result = execute_skill(skill_params)
        return result

    except Exception as e:
        return f"Error executing {skill_name}: {str(e)}"

def parse_command(command_line: str) -> tuple:
    """解析命令行"""
    # 支持多种命令格式
    patterns = [
        r'/speckit\\.dnaspec\\.(\\w+)\\s*(.*)',
        r'dnaspec-(\\w+)\\s*(.*)',
        r'(\\w+)-skill\\s*(.*)'
    ]

    for pattern in patterns:
        match = re.match(pattern, command_line.strip())
        if match:
            return match.group(1), match.group(2)

    return None, None

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Usage: dnaspec-exec <command>")
        return 1

    command_line = ' '.join(sys.argv[1:])
    skill_name, args = parse_command(command_line)

    if not skill_name:
        print("Invalid DNASPEC command format")
        print("Expected: /speckit.dnaspec.<skill> <args>")
        return 1

    # 解析参数
    params = {}
    if 'template=' in args:
        template = re.search(r'template=(\\w+)', args)
        if template:
            params['template'] = template.group(1)

    if 'goals=' in args:
        goals = re.search(r'goals=([^\\s]+)', args)
        if goals:
            params['optimization_goals'] = goals.group(1).split(',')

    if 'operation=' in args:
        operation = re.search(r'operation=(\\w+)', args)
        if operation:
            params['operation'] = operation.group(1)

    # 技能名称映射
    skill_map = {
        'context': 'context-analysis',
        'analysis': 'context-analysis',
        'optimization': 'context-optimization',
        'template': 'cognitive-template',
        'architect': 'architect',
        'git': 'git-operations',
        'workspace': 'temp-workspace',
        'temp': 'temp-workspace'
    }

    mapped_skill = skill_map.get(skill_name, skill_name)

    # 执行技能
    result = execute_dnaspec_skill(mapped_skill, args, params)
    print(result)

    return 0

if __name__ == "__main__":
    sys.exit(main())
'''

        executor_file = dnaspec_dir / 'dnaspec-exec.py'
        with open(executor_file, 'w', encoding='utf-8') as f:
            f.write(executor_script)

        executor_file.chmod(0o755)
        print("✅ Unified executor created at .dnaspec/dnaspec-exec.py")

def main():
    """主函数"""
    try:
        fixer = DNASPECIntegrationFixer()
        success = fixer.fix_integration()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\\n❌ Operation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()