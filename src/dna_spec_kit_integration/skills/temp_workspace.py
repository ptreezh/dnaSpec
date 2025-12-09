"""
Temporary Workspace Skill - 临时工作区管理技能
用于管理AI生成的临时文件，避免项目混乱
"""
from typing import Dict, Any
import os
import tempfile
import shutil
from pathlib import Path
import subprocess


# 全局变量存储当前工作会话
_current_temp_workspace = None
_confirmed_area = None
_max_temp_files = 20  # 临时文件数量阈值


def execute(args: Dict[str, Any]) -> str:
    """
    执行临时工作区管理技能
    """
    operation = args.get("operation", "")
    file_content = args.get("file_content", "")
    file_path = args.get("file_path", "")
    confirm_file = args.get("confirm_file", "")
    
    if operation == "create-workspace":
        return create_temp_workspace()
    elif operation == "add-file":
        return add_file_to_temp_workspace(file_path, file_content)
    elif operation == "list-files":
        return list_files_in_temp_workspace()
    elif operation == "confirm-file":
        return confirm_file_from_temp_workspace(confirm_file)
    elif operation == "confirm-all":
        return confirm_all_files_from_temp_workspace()
    elif operation == "clean-workspace":
        return clean_temp_workspace()
    elif operation == "get-workspace-path":
        return get_temp_workspace_path()
    elif operation == "auto-manage":
        return auto_manage_workspace()
    else:
        return f"未知操作: {operation}"


def create_temp_workspace() -> str:
    """
    创建临时工作区
    """
    global _current_temp_workspace, _confirmed_area
    
    # 创建临时目录
    _current_temp_workspace = tempfile.mkdtemp(prefix="ai_temp_workspace_")
    
    # 创建确认区域
    _confirmed_area = os.path.join(_current_temp_workspace, "confirmed")
    os.makedirs(_confirmed_area, exist_ok=True)
    
    return f"临时工作区已创建: {_current_temp_workspace}"


def add_file_to_temp_workspace(file_path: str, content: str) -> str:
    """
    添加文件到临时工作区
    """
    global _current_temp_workspace
    
    if not _current_temp_workspace:
        return "错误: 未创建临时工作区，请先执行create-workspace操作"
    
    # 确保临时工作区路径存在
    temp_file_path = os.path.join(_current_temp_workspace, file_path)
    os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
    
    # 写入文件内容
    with open(temp_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # 检查是否需要整理清理
    result = auto_manage_workspace()
    
    return f"文件已添加到临时工作区: {temp_file_path}\n{result}"


def list_files_in_temp_workspace() -> str:
    """
    列出临时工作区中的文件
    """
    global _current_temp_workspace
    
    if not _current_temp_workspace:
        return "错误: 未创建临时工作区"
    
    files = []
    for root, dirs, filenames in os.walk(_current_temp_workspace):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if not file_path.startswith(os.path.join(_current_temp_workspace, "confirmed")):
                files.append(file_path)
    
    if not files:
        return "临时工作区中没有文件"
    
    result = f"临时工作区中的文件 ({len(files)} 个):\n"
    for file_path in files:
        result += f"  - {file_path}\n"
    
    return result


def confirm_file_from_temp_workspace(file_path: str) -> str:
    """
    将文件从临时工作区确认到确认区域
    """
    global _current_temp_workspace, _confirmed_area
    
    if not _current_temp_workspace:
        return "错误: 未创建临时工作区"
    
    temp_file_path = os.path.join(_current_temp_workspace, file_path)
    confirmed_file_path = os.path.join(_confirmed_area, file_path)
    
    if not os.path.exists(temp_file_path):
        return f"错误: 临时文件不存在: {temp_file_path}"
    
    # 确保目标目录存在
    os.makedirs(os.path.dirname(confirmed_file_path), exist_ok=True)
    
    # 复制文件到确认区域
    shutil.copy2(temp_file_path, confirmed_file_path)
    
    return f"文件已确认到确认区域: {confirmed_file_path}"


def confirm_all_files_from_temp_workspace() -> str:
    """
    将临时工作区中的所有文件确认到确认区域
    """
    global _current_temp_workspace, _confirmed_area
    
    if not _current_temp_workspace:
        return "错误: 未创建临时工作区"
    
    files = []
    for root, dirs, filenames in os.walk(_current_temp_workspace):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if not file_path.startswith(os.path.join(_current_temp_workspace, "confirmed")):
                files.append(os.path.relpath(file_path, _current_temp_workspace))
    
    confirmed_count = 0
    for file_path in files:
        temp_file_path = os.path.join(_current_temp_workspace, file_path)
        confirmed_file_path = os.path.join(_confirmed_area, file_path)
        
        os.makedirs(os.path.dirname(confirmed_file_path), exist_ok=True)
        shutil.copy2(temp_file_path, confirmed_file_path)
        confirmed_count += 1
    
    return f"已确认 {confirmed_count} 个文件到确认区域"


def clean_temp_workspace() -> str:
    """
    清理临时工作区
    """
    global _current_temp_workspace
    
    if not _current_temp_workspace:
        return "错误: 未创建临时工作区"
    
    try:
        shutil.rmtree(_current_temp_workspace)
        _current_temp_workspace = None
        return "临时工作区已清理"
    except Exception as e:
        return f"清理临时工作区失败: {str(e)}"


def get_temp_workspace_path() -> str:
    """
    获取临时工作区路径
    """
    global _current_temp_workspace
    
    if not _current_temp_workspace:
        return "错误: 未创建临时工作区"
    
    return _current_temp_workspace


def auto_manage_workspace() -> str:
    """
    自动管理工作区：当临时文件数量超过阈值时进行整理
    """
    global _current_temp_workspace, _max_temp_files
    
    if not _current_temp_workspace:
        return "错误: 未创建临时工作区"
    
    # 计算临时文件数量（排除confirmed目录）
    temp_file_count = 0
    for root, dirs, filenames in os.walk(_current_temp_workspace):
        if not root.startswith(os.path.join(_current_temp_workspace, "confirmed")):
            temp_file_count += len(filenames)
    
    if temp_file_count > _max_temp_files:
        # 超过阈值，进行整理
        result = f"临时文件数量 ({temp_file_count}) 超过阈值 ({_max_temp_files})，建议进行整理:\n"
        result += "1. 选择需要确认的文件: 使用 confirm-file 操作\n"
        result += "2. 或确认所有文件: 使用 confirm-all 操作\n"
        result += "3. 或清理临时工作区: 使用 clean-workspace 操作\n"
        result += list_files_in_temp_workspace()
        return result
    else:
        return f"临时文件数量正常 ({temp_file_count}/{_max_temp_files})"


def integrate_with_git(confirm_to_repo: str = ".", git_operation: str = "add-commit") -> str:
    """
    与Git集成：将确认区域的文件提交到Git仓库
    """
    global _confirmed_area
    
    if not _confirmed_area:
        return "错误: 未创建临时工作区或确认区域"
    
    if not os.path.exists(_confirmed_area):
        return "错误: 确认区域不存在"
    
    try:
        # 切换到目标仓库目录
        original_dir = os.getcwd()
        os.chdir(confirm_to_repo)
        
        # 获取确认区域所有文件
        files_to_add = []
        for root, dirs, filenames in os.walk(_confirmed_area):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                rel_path = os.path.relpath(file_path, _confirmed_area)
                files_to_add.append(rel_path)
        
        if not files_to_add:
            return "确认区域中没有文件需要提交"
        
        # 使用Git命令添加文件
        git_add_cmd = ["git", "add"] + files_to_add
        result = subprocess.run(git_add_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return f"Git添加文件失败: {result.stderr}"
        
        # 提交更改
        commit_msg = f"AI generated files from temp workspace: {', '.join(files_to_add[:5])}{'...' if len(files_to_add) > 5 else ''}"
        git_commit_cmd = ["git", "commit", "-m", commit_msg]
        result = subprocess.run(git_commit_cmd, capture_output=True, text=True)
        
        os.chdir(original_dir)
        
        if result.returncode != 0:
            return f"Git提交失败: {result.stderr}"
        
        return f"成功将 {len(files_to_add)} 个文件提交到Git仓库"
        
    except Exception as e:
        os.chdir(original_dir)
        return f"Git集成操作失败: {str(e)}"