"""
Git操作技能 - 重构版本
符合DNASPEC标准化技能接口规范
"""
from typing import Dict, Any
import subprocess
import os
import tempfile
from src.dna_spec_kit_integration.core.skill_base import BaseSkill, DetailLevel


class GitOperationsSkill(BaseSkill):
    """Git操作技能 - 提供完整的Git操作支持"""
    
    def __init__(self):
        super().__init__(
            name="git-operations",
            description="提供完整的Git操作支持，包括分支管理、worktree、并发提交和CI/CD相关功能"
        )
    
    def _execute_skill_logic(self, input_text: str, detail_level: DetailLevel, 
                          options: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """执行Git操作技能逻辑"""
        operation = options.get("operation", "")
        repository_path = options.get("repository_path", ".")
        branch_name = options.get("branch", "main")
        message = options.get("message", "Auto-commit by AI")
        remote = options.get("remote", "origin")
        files = options.get("files", ".")
        
        # 如果没有指定操作，返回错误信息
        if not operation:
            return {
                "success": False,
                "error": "未指定Git操作",
                "operation": operation,
                "repository_path": repository_path,
                "result": "错误: 未指定Git操作"
            }
        
        try:
            # 改变到指定目录
            original_dir = os.getcwd()
            os.chdir(repository_path)
            
            command_executed = ""
            
            if operation == "status":
                result = self._git_status()
                command_executed = "git status"
            elif operation == "commit":
                result = self._git_commit(message, files)
                command_executed = f"git add {files} && git commit -m \"{message}\""
            elif operation == "push":
                result = self._git_push(remote, branch_name)
                command_executed = f"git push {remote} {branch_name}"
            elif operation == "pull":
                result = self._git_pull(remote, branch_name)
                command_executed = f"git pull {remote} {branch_name}"
            elif operation == "branch-create":
                result = self._git_create_branch(branch_name)
                command_executed = f"git checkout -b {branch_name}"
            elif operation == "branch-switch":
                result = self._git_switch_branch(branch_name)
                command_executed = f"git checkout {branch_name}"
            elif operation == "worktree-add":
                path = options.get("path", "")
                worktree_branch = options.get("worktree_branch", branch_name)
                result = self._git_worktree_add(path, worktree_branch)
                command_executed = f"git worktree add {path} {worktree_branch}"
            elif operation == "worktree-list":
                result = self._git_worktree_list()
                command_executed = "git worktree list"
            elif operation == "worktree-remove":
                worktree_path = options.get("worktree_path", "")
                result = self._git_worktree_remove(worktree_path)
                command_executed = f"git worktree remove {worktree_path}"
            elif operation == "merge":
                source_branch = options.get("source_branch", "feature")
                result = self._git_merge(source_branch, branch_name)
                command_executed = f"git checkout {branch_name} && git merge {source_branch}"
            elif operation == "stash":
                result = self._git_stash()
                command_executed = "git stash"
            elif operation == "stash-pop":
                result = self._git_stash_pop()
                command_executed = "git stash pop"
            elif operation == "diff":
                result = self._git_diff()
                command_executed = "git diff"
            elif operation == "log":
                count = options.get("count", 5)
                result = self._git_log(count)
                command_executed = f"git log --oneline -{count}"
            elif operation == "reset":
                commit = options.get("commit", "HEAD")
                result = self._git_reset(commit)
                command_executed = f"git reset --hard {commit}"
            else:
                result = f"未知的Git操作: {operation}"
                command_executed = f"unknown git operation: {operation}"
            
            os.chdir(original_dir)
            
            return {
                "success": True,
                "operation": operation,
                "repository_path": repository_path,
                "result": result,
                "command_executed": command_executed
            }
            
        except Exception as e:
            os.chdir(original_dir)
            return {
                "success": False,
                "operation": operation,
                "repository_path": repository_path,
                "result": f"Git操作失败: {str(e)}",
                "command_executed": f"git {operation}",
                "error": str(e)
            }
    
    def _format_output(self, result_data: Dict[str, Any], detail_level: DetailLevel) -> Dict[str, Any]:
        """根据详细程度格式化输出结果"""
        if detail_level == DetailLevel.BASIC:
            # 基础级别只返回核心信息
            return {
                "operation": result_data["operation"],
                "result": result_data["result"][:200] + "..." if len(result_data["result"]) > 200 else result_data["result"]
            }
        elif detail_level == DetailLevel.STANDARD:
            # 标准级别返回标准信息
            return {
                "operation": result_data["operation"],
                "repository_path": result_data["repository_path"],
                "result": result_data["result"]
            }
        else:  # DETAILED
            # 详细级别返回完整信息
            detailed_info = {
                "command_executed": result_data.get("command_executed", ""),
                "execution_details": {
                    "success": result_data.get("success", True),
                    "error_message": result_data.get("error", "")
                }
            }
            result_data.update(detailed_info)
            return result_data
    
    def _run_git_command(self, cmd: str) -> str:
        """
        执行Git命令
        """
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"错误: {result.stderr}"
    
    def _git_status(self) -> str:
        """
        获取Git状态
        """
        return self._run_git_command("git status")
    
    def _git_commit(self, message: str, files: str) -> str:
        """
        提交文件
        """
        add_cmd = f"git add {files}"
        commit_cmd = f'git commit -m "{message}"'
        return self._run_git_command(f"{add_cmd} && {commit_cmd}")
    
    def _git_push(self, remote: str, branch: str) -> str:
        """
        推送到远程仓库
        """
        return self._run_git_command(f"git push {remote} {branch}")
    
    def _git_pull(self, remote: str, branch: str) -> str:
        """
        从远程仓库拉取
        """
        return self._run_git_command(f"git pull {remote} {branch}")
    
    def _git_create_branch(self, branch_name: str) -> str:
        """
        创建分支
        """
        return self._run_git_command(f"git checkout -b {branch_name}")
    
    def _git_switch_branch(self, branch_name: str) -> str:
        """
        切换分支
        """
        return self._run_git_command(f"git checkout {branch_name}")
    
    def _git_worktree_add(self, path: str, branch: str) -> str:
        """
        添加工作树
        """
        if not path:
            path = tempfile.mkdtemp(prefix="git-worktree-")
        return self._run_git_command(f"git worktree add {path} {branch}")
    
    def _git_worktree_list(self) -> str:
        """
        列出工作树
        """
        return self._run_git_command("git worktree list")
    
    def _git_worktree_remove(self, path: str) -> str:
        """
        移除工作树
        """
        return self._run_git_command(f"git worktree remove {path}")
    
    def _git_merge(self, source_branch: str, target_branch: str) -> str:
        """
        合并分支
        """
        switch_cmd = f"git checkout {target_branch}"
        merge_cmd = f"git merge {source_branch}"
        return self._run_git_command(f"{switch_cmd} && {merge_cmd}")
    
    def _git_stash(self) -> str:
        """
        暂存更改
        """
        return self._run_git_command("git stash")
    
    def _git_stash_pop(self) -> str:
        """
        恢复暂存
        """
        return self._run_git_command("git stash pop")
    
    def _git_diff(self) -> str:
        """
        显示差异
        """
        return self._run_git_command("git diff")
    
    def _git_log(self, count: int) -> str:
        """
        显示提交历史
        """
        return self._run_git_command(f"git log --oneline -{count}")
    
    def _git_reset(self, commit: str) -> str:
        """
        重置到指定提交
        """
        return self._run_git_command(f"git reset --hard {commit}")