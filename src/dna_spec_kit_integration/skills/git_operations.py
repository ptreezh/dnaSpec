"""
Git Operations Skill - Git操作技能
提供完整的Git操作支持，包括分支管理、worktree、并发提交和CI/CD相关功能
"""
from typing import Dict, Any
import subprocess
import os
import tempfile


def execute(args: Dict[str, Any]) -> str:
    """
    执行Git操作技能
    """
    operation = args.get("operation", "")
    repository_path = args.get("repository_path", ".")
    branch_name = args.get("branch", "main")
    message = args.get("message", "Auto-commit by AI")
    remote = args.get("remote", "origin")
    files = args.get("files", ".")
    
    if not operation:
        return "错误: 未指定Git操作"
    
    try:
        # 改变到指定目录
        original_dir = os.getcwd()
        os.chdir(repository_path)
        
        if operation == "status":
            result = _git_status()
        elif operation == "commit":
            result = _git_commit(message, files)
        elif operation == "push":
            result = _git_push(remote, branch_name)
        elif operation == "pull":
            result = _git_pull(remote, branch_name)
        elif operation == "branch-create":
            result = _git_create_branch(branch_name)
        elif operation == "branch-switch":
            result = _git_switch_branch(branch_name)
        elif operation == "worktree-add":
            path = args.get("path", "")
            worktree_branch = args.get("worktree_branch", branch_name)
            result = _git_worktree_add(path, worktree_branch)
        elif operation == "worktree-list":
            result = _git_worktree_list()
        elif operation == "worktree-remove":
            worktree_path = args.get("worktree_path", "")
            result = _git_worktree_remove(worktree_path)
        elif operation == "merge":
            source_branch = args.get("source_branch", "feature")
            result = _git_merge(source_branch, branch_name)
        elif operation == "stash":
            result = _git_stash()
        elif operation == "stash-pop":
            result = _git_stash_pop()
        elif operation == "diff":
            result = _git_diff()
        elif operation == "log":
            count = args.get("count", 5)
            result = _git_log(count)
        elif operation == "reset":
            commit = args.get("commit", "HEAD")
            result = _git_reset(commit)
        else:
            result = f"未知的Git操作: {operation}"
        
        os.chdir(original_dir)
        return result
        
    except Exception as e:
        os.chdir(original_dir)
        return f"Git操作失败: {str(e)}"


def _run_git_command(cmd: str) -> str:
    """
    执行Git命令
    """
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout
    else:
        return f"错误: {result.stderr}"


def _git_status() -> str:
    """
    获取Git状态
    """
    return _run_git_command("git status")


def _git_commit(message: str, files: str) -> str:
    """
    提交文件
    """
    add_cmd = f"git add {files}"
    commit_cmd = f'git commit -m "{message}"'
    return _run_git_command(f"{add_cmd} && {commit_cmd}")


def _git_push(remote: str, branch: str) -> str:
    """
    推送到远程仓库
    """
    return _run_git_command(f"git push {remote} {branch}")


def _git_pull(remote: str, branch: str) -> str:
    """
    从远程仓库拉取
    """
    return _run_git_command(f"git pull {remote} {branch}")


def _git_create_branch(branch_name: str) -> str:
    """
    创建分支
    """
    return _run_git_command(f"git checkout -b {branch_name}")


def _git_switch_branch(branch_name: str) -> str:
    """
    切换分支
    """
    return _run_git_command(f"git checkout {branch_name}")


def _git_worktree_add(path: str, branch: str) -> str:
    """
    添加工作树
    """
    if not path:
        path = tempfile.mkdtemp(prefix="git-worktree-")
    return _run_git_command(f"git worktree add {path} {branch}")


def _git_worktree_list() -> str:
    """
    列出工作树
    """
    return _run_git_command("git worktree list")


def _git_worktree_remove(path: str) -> str:
    """
    移除工作树
    """
    return _run_git_command(f"git worktree remove {path}")


def _git_merge(source_branch: str, target_branch: str) -> str:
    """
    合并分支
    """
    switch_cmd = f"git checkout {target_branch}"
    merge_cmd = f"git merge {source_branch}"
    return _run_git_command(f"{switch_cmd} && {merge_cmd}")


def _git_stash() -> str:
    """
    暂存更改
    """
    return _run_git_command("git stash")


def _git_stash_pop() -> str:
    """
    恢复暂存
    """
    return _run_git_command("git stash pop")


def _git_diff() -> str:
    """
    显示差异
    """
    return _run_git_command("git diff")


def _git_log(count: int) -> str:
    """
    显示提交历史
    """
    return _run_git_command(f"git log --oneline -{count}")


def _git_reset(commit: str) -> str:
    """
    重置到指定提交
    """
    return _run_git_command(f"git reset --hard {commit}")