"""
DNASPEC统一技能执行器
支持所有DNASPEC技能的执行
"""
from typing import Dict, Any, List, Optional
import sys
from pathlib import Path

# 导入所有独立技能执行函数
try:
    from .context_analysis_independent import execute_context_analysis
    from .simple_architect_independent import execute_simple_architect
    from .system_architect_independent import execute_system_architect
except ImportError as e:
    print(f"Warning: Could not import some independent skills: {e}")

# 导入基础技能类
try:
    from dna_context_engineering.skills_system_final import (
        execute as execute_context_engineering
    )
except ImportError as e:
    print(f"Warning: Could not import context engineering skills: {e}")

# 导入命令映射器
from .command_mapper import command_mapper


class DNASPECSkillExecutor:
    """DNASPEC统一技能执行器"""

    def __init__(self):
        self.skill_registry = {
            # 上下文工程技能（通过独立函数）
            'context-analysis': execute_context_analysis,

            # 系统设计技能
            'architect': execute_system_architect,
            'simple-architect': execute_simple_architect,

            # 使用命令映射器（Git和Workspace）
            'git': lambda args: command_mapper.execute_command(f"git {args.get('command', 'status')}"),
            'workspace': lambda args: command_mapper.execute_command(f"workspace {args.get('command', 'status')}"),
        }

        # 从context engineering系统获取更多技能
        try:
            self.skill_registry.update({
                'context-optimization': lambda args: execute_context_engineering({
                    'skill': 'context-optimization',
                    'context': args.get('context', ''),
                    'params': args.get('params', {})
                }),
                'cognitive-template': lambda args: execute_context_engineering({
                    'skill': 'cognitive-template',
                    'context': args.get('context', ''),
                    'params': args.get('params', {})
                }),
            })
        except:
            pass

    def execute_skill(self, skill_name: str, context: str = "", **kwargs) -> Dict[str, Any]:
        """
        执行指定的DNASPEC技能

        Args:
            skill_name: 技能名称
            context: 上下文内容
            **kwargs: 其他参数

        Returns:
            执行结果
        """
        if skill_name not in self.skill_registry:
            return {
                'success': False,
                'error': f'Unknown skill: {skill_name}',
                'available_skills': list(self.skill_registry.keys())
            }

        try:
            skill_func = self.skill_registry[skill_name]

            # 准备参数
            args = {
                'context': context,
                **kwargs
            }

            # 执行技能
            if callable(skill_func):
                result = skill_func(args)

                # 确保返回格式一致
                if isinstance(result, dict):
                    return result
                else:
                    return {
                        'success': True,
                        'result': str(result)
                    }
            else:
                return {
                    'success': False,
                    'error': f'Skill {skill_name} is not callable'
                }

        except Exception as e:
            return {
                'success': False,
                'error': f'Error executing skill {skill_name}: {str(e)}'
            }

    def get_available_skills(self) -> Dict[str, str]:
        """获取可用技能列表"""
        descriptions = {
            'context-analysis': 'Analyze context quality across 5 dimensions',
            'context-optimization': 'Optimize context quality with AI-driven improvements',
            'cognitive-template': 'Apply cognitive frameworks to structure tasks',
            'architect': 'Design system architecture and components',
            'simple-architect': 'Simple architecture design for basic projects',
            'system-architect': 'Advanced system architecture with detailed design',
            'git': 'Execute Git workflow operations safely',
            'workspace': 'Manage AI-generated files in secure workspace'
        }

        skills = {}
        for skill_name in self.skill_registry.keys():
            skills[skill_name] = descriptions.get(skill_name, 'No description available')

        return skills

    def get_skill_help(self, skill_name: str) -> str:
        """获取特定技能的帮助信息"""
        help_texts = {
            'context-analysis': """
Context Analysis (/dnaspec.context-analysis):
Usage: /dnaspec.context-analysis "context to analyze"

Examples:
  /dnaspec.context-analysis "Design a user authentication system"
  /dnaspec.context-analysis "API design documentation" --mode enhanced
""",
            'context-optimization': """
Context Optimization (/dnaspec.context-optimization):
Usage: /dnaspec.context-optimization "context to optimize" --goals <goals>

Examples:
  /dnaspec.context-optimization "Write clean code" --goals clarity,completeness
  /dnaspec.context-optimization "System requirements" --goals relevance,consistency
""",
            'cognitive-template': """
Cognitive Template (/dnaspec.cognitive-template):
Usage: /dnaspec.cognitive-template "task description" --template <type>

Template Types:
  chain_of_thought - Step-by-step reasoning
  few_shot - Learning from examples
  verification - Double-checking results
  role_playing - Acting as a specific role

Examples:
  /dnaspec.cognitive-template "How to improve performance" --template chain_of_thought
  /dnaspec.cognitive-template "Review this design" --template verification
""",
            'architect': """
System Architect (/dnaspec.architect):
Usage: /dnaspec.architect "system requirements" [options]

Options:
  --style <type> - Architecture style (microservices, monolithic, etc.)
  --constraints <list> - Constraints (performance, security, etc.)

Examples:
  /dnaspec.architect "E-commerce platform" --style microservices
  /dnaspec.architect "Real-time system" --constraints high_performance
""",
            'git': """
Git Operations (/dnaspec.git):
Usage: /dnaspec.git <subcommand> [arguments]

Subcommands:
  status - Show repository status
  add <files> - Add files to staging
  commit <message> - Commit changes
  push - Push to remote
  pull - Pull from remote
  branch <name> - Create branch
  log --limit <n> - Show history

Examples:
  /dnaspec.git status
  /dnaspec.git commit "Fix authentication bug"
  /dnaspec.git branch feature/new-feature
""",
            'workspace': """
Workspace Management (/dnaspec.workspace):
Usage: /dnaspec.workspace <subcommand> [arguments]

Subcommands:
  create - Create new workspace
  add <file> <content> - Add file to workspace
  list - List workspace files
  clean - Clean workspace
  stage <file> - Move file to staging area
  verify <file> - Verify staged file
  promote <file> - Promote verified file

Examples:
  /dnaspec.workspace create
  /dnaspec.workspace add "auth.py" "import hashlib..."
  /dnaspec.workspace stage "auth.py"
"""
        }

        return help_texts.get(skill_name, f"No help available for skill: {skill_name}")

# 创建全局技能执行器实例
skill_executor = DNASPECSkillExecutor()


def execute_skill(skill_name: str, args: Dict[str, Any]) -> str:
    """
    全局技能执行入口函数

    Args:
        skill_name: 技能名称
        args: 参数字典

    Returns:
        执行结果字符串
    """
    result = skill_executor.execute_skill(skill_name, **args)

    if result.get('success'):
        return str(result.get('result', 'Skill executed successfully'))
    else:
        return f"Error: {result.get('error', 'Unknown error')}"


# 向后兼容的执行函数
def execute_architect(args: Dict[str, Any]) -> str:
    """向后兼容的架构师执行函数"""
    return execute_skill('architect', args)

def execute_agent_creator(args: Dict[str, Any]) -> str:
    """向后兼容的智能体创建执行函数"""
    return execute_skill('agent-creator', args)

def execute_task_decomposer(args: Dict[str, Any]) -> str:
    """向后兼容的任务分解执行函数"""
    return execute_skill('task-decomposer', args)

def execute_constraint_generator(args: Dict[str, Any]) -> str:
    """向后兼容的约束生成执行函数"""
    return execute_skill('constraint-generator', args)

def execute_dapi_checker(args: Dict[str, Any]) -> str:
    """向后兼容的API检查执行函数"""
    return execute_skill('dapi-checker', args)

def execute_modulizer(args: Dict[str, Any]) -> str:
    """向后兼容的模块化执行函数"""
    return execute_skill('modulizer', args)