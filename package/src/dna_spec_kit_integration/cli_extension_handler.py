#!/usr/bin/env python3
"""
DNASPEC CLI扩展处理器
为AI CLI工具提供扩展接口
"""
import sys
import os
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


def handle_dnaspec_command(skill_name: str, input_text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    处理DNASPEC命令（供AI CLI工具调用）

    Args:
        skill_name: 技能名称
        input_text: 输入文本
        context: 上下文信息

    Returns:
        Dict: 处理结果
    """
    try:
        # 获取项目根目录（基于调用时的上下文）
        if context and 'project_root' in context:
            project_root = Path(context['project_root'])
        else:
            # 从当前工作目录推断项目根目录
            project_root = _detect_project_root()

        # 验证项目根目录
        if not _validate_project_access(project_root):
            return {
                'success': False,
                'error': 'Access denied: Cannot access project directory',
                'error_code': 'SECURITY_VIOLATION'
            }

        # 构建DNASPEC命令
        command = [
            sys.executable, '-m', 'dna_spec_kit_integration.cli',
            'exec', f'/{skill_name}', input_text
        ]

        # 执行DNASPEC命令
        result = subprocess.run(
            command,
            cwd=project_root,
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONIOENCODING": "utf-8", "LANG": "en_US.UTF-8"},
            timeout=120  # 2分钟超时
        )

        if result.returncode == 0:
            return {
                'success': True,
                'output': result.stdout.strip(),
                'skill_name': skill_name,
                'execution_time': datetime.now().isoformat(),
                'project_root': str(project_root)
            }
        else:
            return {
                'success': False,
                'error': result.stderr.strip(),
                'skill_name': skill_name,
                'error_code': 'EXECUTION_FAILED',
                'project_root': str(project_root)
            }

    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': 'DNASPEC execution timed out',
            'error_code': 'TIMEOUT'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}',
            'error_code': 'UNEXPECTED_ERROR'
        }


def _detect_project_root() -> Path:
    """
    检测项目根目录

    Returns:
        Path: 项目根目录
    """
    current_dir = Path.cwd()

    # 向上查找项目标识文件
    project_markers = [
        '.dnaspec',
        'package.json',
        'pyproject.toml',
        'requirements.txt',
        '.git'
    ]

    search_dir = current_dir
    while search_dir != search_dir.parent:
        for marker in project_markers:
            if (search_dir / marker).exists():
                return search_dir
        search_dir = search_dir.parent

    # 如果没找到，返回当前目录
    return current_dir


def _validate_project_access(project_root: Path) -> bool:
    """
    验证项目访问权限

    Args:
        project_root: 项目根目录

    Returns:
        bool: 是否有访问权限
    """
    try:
        # 检查目录是否存在
        if not project_root.exists():
            return False

        # 检查是否可读
        if not os.access(project_root, os.R_OK):
            return False

        # 检查是否可写（用于临时文件）
        temp_file = project_root / '.dnaspec_temp_test'
        try:
            temp_file.touch()
            temp_file.unlink()
            return True
        except (PermissionError, OSError):
            # 即使不能写，如果能读也认为可以访问（只读模式）
            return True

    except Exception:
        return False


def get_available_skills() -> Dict[str, Any]:
    """
    获取可用的DNASPEC技能列表

    Returns:
        Dict: 技能列表
    """
    skills = [
        {
            'name': 'context-analysis',
            'display_name': 'Context Analysis',
            'description': 'Analyze context quality across 5 dimensions (clarity, relevance, completeness, consistency, efficiency)',
            'command': '/dnaspec.context-analysis',
            'category': 'analysis',
            'examples': [
                '/dnaspec.context-analysis "Analyze this user story for clarity and completeness"',
                '/dnaspec.context-analysis "Review the technical specifications for consistency"'
            ]
        },
        {
            'name': 'context-optimization',
            'display_name': 'Context Optimization',
            'description': 'Optimize context based on specific goals and requirements',
            'command': '/dnaspec.context-optimization',
            'category': 'optimization',
            'examples': [
                '/dnaspec.context-optimization "Optimize this context for code generation"',
                '/dnaspec.context-optimization "Improve clarity for junior developers"'
            ]
        },
        {
            'name': 'cognitive-template',
            'display_name': 'Cognitive Template',
            'description': 'Apply cognitive templates (Chain-of-Thought, Verification, Few-shot Learning)',
            'command': '/dnaspec.cognitive-template',
            'category': 'templates',
            'examples': [
                '/dnaspec.cognitive-template "Apply verification template to this requirement"',
                '/dnaspec.cognitive-template "Use chain-of-thought for this problem"'
            ]
        },
        {
            'name': 'architect',
            'display_name': 'System Architect',
            'description': 'Design system architecture and technical specifications',
            'command': '/dnaspec.architect',
            'category': 'design',
            'examples': [
                '/dnaspec.architect "Design microservices architecture for e-commerce"',
                '/dnaspec.architect "Create technical specifications for user authentication"'
            ]
        },
        {
            'name': 'task-decomposer',
            'display_name': 'Task Decomposer',
            'description': 'Decompose complex tasks into manageable steps',
            'command': '/dnaspec.task-decomposer',
            'category': 'planning',
            'examples': [
                '/dnaspec.task-decomposer "Break down this feature into development tasks"',
                '/dnaspec.task-decomposer "Create project timeline with milestones"'
            ]
        },
        {
            'name': 'constraint-generator',
            'display_name': 'Constraint Generator',
            'description': 'Generate constraints and validation rules for development',
            'command': '/dnaspec.constraint-generator',
            'category': 'validation',
            'examples': [
                '/dnaspec.constraint-generator "Generate security constraints for this API"',
                '/dnaspec.constraint-generator "Create validation rules for user input"'
            ]
        },
        {
            'name': 'agent-creator',
            'display_name': 'Agent Creator',
            'description': 'Create intelligent agents for specific tasks and domains',
            'command': '/dnaspec.agent-creator',
            'category': 'agents',
            'examples': [
                '/dnaspec.agent-creator "Create an agent for code review automation"',
                '/dnaspec.agent-creator "Design a testing agent for API validation"'
            ]
        },
        {
            'name': 'dapi-checker',
            'display_name': 'API Checker',
            'description': 'Analyze and validate API interfaces and specifications',
            'command': '/dnaspec.dapi-checker',
            'category': 'analysis',
            'examples': [
                '/dnaspec.dapi-checker "Validate this REST API specification"',
                '/dnaspec.dapi-checker "Check GraphQL schema consistency"'
            ]
        },
        {
            'name': 'modulizer',
            'display_name': 'Modulizer',
            'description': 'Break down code into reusable and maintainable modules',
            'command': '/dnaspec.modulizer',
            'category': 'refactoring',
            'examples': [
                '/dnaspec.modulizer "Extract reusable modules from this codebase"',
                '/dnaspec.modulizer "Design modular architecture for this service"'
            ]
        },
        {
            'name': 'cache-manager',
            'display_name': 'Cache Manager',
            'description': 'Optimize cache strategy and manage data caching for improved performance',
            'command': '/dnaspec.cache-manager',
            'category': 'performance',
            'examples': [
                '/dnaspec.cache-manager "Optimize caching strategy for this API"',
                '/dnaspec.cache-manager "Design cache invalidation policy for this service"'
            ]
        },
        {
            'name': 'git-cleaner',
            'display_name': 'Git Cleaner',
            'description': 'Prevent project pollution and maintain clean Git repository structure',
            'command': '/dnaspec.git-cleaner',
            'category': 'maintenance',
            'examples': [
                '/dnaspec.git-cleaner "Clean up this Git repository and remove pollution"',
                '/dnaspec.git-cleaner "Setup Git hooks to prevent project pollution"'
            ]
        }
    ]

    return {
        'skills': skills,
        'total_count': len(skills),
        'categories': list(set(skill['category'] for skill in skills)),
        'updated_at': datetime.now().isoformat()
    }


def validate_skill_parameters(skill_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    验证技能参数

    Args:
        skill_name: 技能名称
        parameters: 参数字典

    Returns:
        Dict: 验证结果
    """
    available_skills = get_available_skills()
    skill_names = [skill['name'] for skill in available_skills['skills']]

    if skill_name not in skill_names:
        return {
            'valid': False,
            'error': f'Unknown skill: {skill_name}',
            'available_skills': skill_names
        }

    # 这里可以添加特定技能的参数验证逻辑
    # 目前所有技能都接受简单的文本输入
    return {
        'valid': True,
        'skill_name': skill_name,
        'parameters': parameters
    }


def get_skill_examples(skill_name: str) -> Dict[str, Any]:
    """
    获取技能使用示例

    Args:
        skill_name: 技能名称

    Returns:
        Dict: 示例信息
    """
    skills = get_available_skills()['skills']

    for skill in skills:
        if skill['name'] == skill_name:
            return {
                'skill_name': skill_name,
                'display_name': skill['display_name'],
                'description': skill['description'],
                'examples': skill['examples'],
                'category': skill['category']
            }

    return {
        'error': f'Skill not found: {skill_name}',
        'available_skills': [skill['name'] for skill in skills]
    }


# CLI入口点
def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description='DNASPEC CLI Extension Handler',
        prog='dnaspec-handler'
    )

    # 互斥参数组
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--list-skills', action='store_true', help='List available skills')
    group.add_argument('--examples', help='Get examples for a skill')
    group.add_argument('--context', help='Context JSON file')

    # 位置参数（仅在有操作时需要）
    parser.add_argument('skill_name', nargs='?', help='DNASPEC skill name')
    parser.add_argument('input_text', nargs='?', help='Input text for the skill')

    args = parser.parse_args()

    if args.list_skills:
        skills = get_available_skills()
        print(json.dumps(skills, ensure_ascii=False, indent=2))
        return

    if args.examples:
        examples = get_skill_examples(args.examples)
        print(json.dumps(examples, ensure_ascii=False, indent=2))
        return

    # 处理技能命令
    context = None
    if args.context:
        try:
            with open(args.context, 'r') as f:
                context = json.load(f)
        except Exception as e:
            print(f"Error reading context file: {e}", file=sys.stderr)
            sys.exit(1)

    result = handle_dnaspec_command(args.skill_name, args.input_text, context)

    if result['success']:
        print(result['output'])
    else:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()