"""
DNASPEC命令映射器
将精简的命令格式映射到实际的技能执行函数
"""
from typing import Dict, Any, Optional
import sys
from pathlib import Path

# 导入实际技能类
from .git_operations_refactored import GitSkill
from .temp_workspace_refactored import WorkspaceSkill


class CommandMapper:
    """命令映射器 - 将精简命令映射到技能执行"""

    def __init__(self):
        self.git_skill = GitSkill()
        self.workspace_skill = WorkspaceSkill()

        # 命令映射表
        self.command_map = {
            'git': self.git_skill,
            'workspace': self.workspace_skill,
        }

    def execute_command(self, command: str, args: list) -> Dict[str, Any]:
        """
        执行精简格式的命令

        Args:
            command: 命令名称（如 'git', 'workspace'）
            args: 命令参数列表

        Returns:
            执行结果
        """
        if command not in self.command_map:
            return {
                'success': False,
                'error': f'Unknown command: {command}',
                'available_commands': list(self.command_map.keys())
            }

        skill = self.command_map[command]

        # 根据命令类型解析参数
        if command == 'git':
            return self._execute_git_command(args)
        elif command == 'workspace':
            return self._execute_workspace_command(args)

        return {
            'success': False,
            'error': f'Command {command} not implemented'
        }

    def _execute_git_command(self, args: list) -> Dict[str, Any]:
        """执行Git命令"""
        if not args:
            return self.git_skill.execute({"input": "git status", "options": {"operation": "status"}})

        # 解析Git命令
        subcommand = args[0].lower()

        if subcommand == 'status':
            return self.git_skill.execute({"input": "git status", "options": {"operation": "status"}})
        elif subcommand == 'add':
            files = ' '.join(args[1:]) if len(args) > 1 else "."
            return self.git_skill.execute({"input": f"git add {files}", "options": {"operation": "commit", "files": files}})
        elif subcommand == 'commit':
            message = ' '.join(args[1:]) if len(args) > 1 else "Auto commit"
            return self.git_skill.execute({"input": f"git commit -m '{message}'", "options": {"operation": "commit", "message": message}})
        elif subcommand == 'push':
            return self.git_skill.execute({"input": "git push", "options": {"operation": "push"}})
        elif subcommand == 'pull':
            return self.git_skill.execute({"input": "git pull", "options": {"operation": "pull"}})
        elif subcommand == 'branch':
            branch_name = args[1] if len(args) > 1 else None
            return self.git_skill.execute({"input": f"git branch {branch_name}", "options": {"operation": "branch-create", "branch": branch_name}})
        elif subcommand == 'log':
            limit = 10
            if '--limit' in args:
                limit_idx = args.index('--limit')
                if len(args) > limit_idx + 1:
                    limit = int(args[limit_idx + 1])
            return self.git_skill.execute({"input": f"git log --oneline -{limit}", "options": {"operation": "log", "count": limit}})
        else:
            return {
                'success': False,
                'error': f'Unknown git subcommand: {subcommand}',
                'available_subcommands': ['status', 'add', 'commit', 'push', 'pull', 'branch', 'log']
            }

    def _execute_workspace_command(self, args: list) -> Dict[str, Any]:
        """执行工作区命令"""
        if not args:
            return self.workspace_skill.execute({"input": "workspace status", "options": {"operation": "get-workspace-path"}})

        # 解析工作区命令
        subcommand = args[0].lower()

        if subcommand == 'create':
            return self.workspace_skill.execute({"input": "workspace create", "options": {"operation": "create-workspace"}})
        elif subcommand == 'add':
            if len(args) < 2:
                return {
                    'success': False,
                    'error': 'Usage: /dnaspec.workspace add <file_path> <content>'
                }
            file_path = args[1]
            content = ' '.join(args[2:]) if len(args) > 2 else ""
            return self.workspace_skill.execute({"input": f"workspace add {file_path}", "options": {"operation": "add-file", "file_path": file_path, "file_content": content}})
        elif subcommand == 'list':
            return self.workspace_skill.execute({"input": "workspace list", "options": {"operation": "list-files"}})
        elif subcommand == 'clean':
            return self.workspace_skill.execute({"input": "workspace clean", "options": {"operation": "clean-workspace"}})
        elif subcommand == 'stage':
            confirm_file = args[1] if len(args) > 1 else None
            return self.workspace_skill.execute({"input": f"workspace stage {confirm_file}", "options": {"operation": "confirm-file", "confirm_file": confirm_file}})
        elif subcommand == 'verify':
            confirm_file = args[1] if len(args) > 1 else None
            return self.workspace_skill.execute({"input": f"workspace verify {confirm_file}", "options": {"operation": "confirm-file", "confirm_file": confirm_file}})
        elif subcommand == 'promote':
            confirm_file = args[1] if len(args) > 1 else None
            return self.workspace_skill.execute({"input": f"workspace promote {confirm_file}", "options": {"operation": "confirm-file", "confirm_file": confirm_file}})
        else:
            return {
                'success': False,
                'error': f'Unknown workspace subcommand: {subcommand}',
                'available_subcommands': ['create', 'add', 'list', 'clean', 'stage', 'verify', 'promote']
            }

    def get_available_commands(self) -> Dict[str, str]:
        """获取可用命令列表"""
        return {
            'git': 'Git operations (status, add, commit, push, pull, branch, log)',
            'workspace': 'Workspace management (create, add, list, clean, stage, verify, promote)'
        }

    def get_command_help(self, command: str) -> str:
        """获取特定命令的帮助信息"""
        if command == 'git':
            return """
Git Operations:
  /dnaspec.git status                          - Show repository status
  /dnaspec.git add <files>                      - Add files to staging area
  /dnaspec.git commit "message"               - Commit changes
  /dnaspec.git push                          - Push to remote repository
  /dnaspec.git pull                          - Pull from remote repository
  /dnaspec.git branch <name>                  - Create new branch
  /dnaspec.git log --limit <n>                - Show commit history
"""
        elif command == 'workspace':
            return """
Workspace Management:
  /dnaspec.workspace create                   - Create new workspace
  /dnaspec.workspace add <file> <content>     - Add file to workspace
  /dnaspec.workspace list                    - List workspace files
  /dnaspec.workspace clean                   - Clean workspace
  /dnaspec.workspace stage <file>             - Move file to staging area
  /dnaspec.workspace verify <file>            - Verify staged file
  /dnaspec.workspace promote <file>           - Promote verified file
"""
        else:
            return f"Unknown command: {command}. Available: git, workspace"


# 创建全局命令映射器实例
command_mapper = CommandMapper()


def execute_command(command_string: str) -> Dict[str, Any]:
    """
    执行命令字符串（全局入口函数）

    Args:
        command_string: 完整的命令字符串，如 "git status" 或 "workspace create"

    Returns:
        执行结果
    """
    # 解析命令字符串
    parts = command_string.strip().split()
    if not parts:
        return {
            'success': False,
            'error': 'Empty command'
        }

    command = parts[0]
    args = parts[1:] if len(parts) > 1 else []

    return command_mapper.execute_command(command, args)


# 向后兼容的函数
def execute_git(args: Dict[str, Any]) -> str:
    """向后兼容的Git执行函数"""
    if 'command' in args:
        result = execute_command(f"git {args['command']}")
        if result.get('success'):
            return str(result.get('result', 'Git command executed'))
        else:
            return f"Error: {result.get('error', 'Unknown error')}"
    return "Error: No command specified"


def execute_workspace(args: Dict[str, Any]) -> str:
    """向后兼容的工作区执行函数"""
    if 'command' in args:
        result = execute_command(f"workspace {args['command']}")
        if result.get('success'):
            return str(result.get('result', 'Workspace command executed'))
        else:
            return f"Error: {result.get('error', 'Unknown error')}"
    return "Error: No command specified"