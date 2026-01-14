"""
temp_workspace.py
临时工作区管理技能 - 符合Claude Skills规范
"""
from typing import Dict, Any, List
import os
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import json

# 临时工作区状态（内存中的状态管理）
_current_workspace = None
_active_session = None
_temp_files = []
_confirmed_files = []
_session_start_time = None

def execute(args: Dict[str, Any]) -> str:
    """
    Claude Skills标准执行入口
    """
    operation = args.get("operation", "status")
    global _current_workspace, _active_session, _temp_files, _confirmed_files, _session_start_time
    
    if operation == "create-workspace":
        # 创建临时工作区
        _current_workspace = tempfile.mkdtemp(prefix="dnaspec_ai_temp_workspace_")
        _active_session = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        _session_start_time = datetime.now().isoformat()
        
        # 创建确认区域
        confirmed_area = os.path.join(_current_workspace, "confirmed")
        os.makedirs(confirmed_area, exist_ok=True)
        
        return f"📁 临时工作区已创建: {_current_workspace}\n会话: {_active_session}\n启动时间: {_session_start_time}"

    elif operation == "add-file":
        file_path = args.get("file_path", "")
        content = args.get("content", "")
        target_dir = args.get("target_dir", "")

        if not _current_workspace:
            return "❌ 错误: 未创建临时工作区"
        
        # 构造完整文件路径
        full_file_path = os.path.join(_current_workspace, target_dir, file_path) if target_dir else os.path.join(_current_workspace, file_path)
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
        
        # 写入内容
        with open(full_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 添加到临时文件列表
        if full_file_path not in _temp_files:
            _temp_files.append(full_file_path)
        
        # 文件统计信息
        file_size = len(content.encode('utf-8'))
        return f"📄 文件已添加到临时工作区\n文件: {full_file_path}\n大小: {file_size} 字节\n临时文件总数: {len(_temp_files)}"

    elif operation == "list-files":
        if not _current_workspace:
            return "❌ 错误: 未创建临时工作区"
        
        lines = ["📋 临时工作区文件状态:"]
        lines.append(f"临时文件: {len(_temp_files)} 个")
        lines.append(f"确认文件: {len(_confirmed_files)} 个")
        lines.append(f"活跃会话: {_active_session}")
        
        detailed = args.get("detailed", False)
        if detailed:
            lines.append("\n临时文件列表:")
            for i, file_path in enumerate(_temp_files[:10]):  # 只显示前10个
                try:
                    size = os.path.getsize(file_path)
                    lines.append(f"  [{i+1}] {os.path.basename(file_path)} ({size} bytes)")
                except:
                    lines.append(f"  [{i+1}] {os.path.basename(file_path)} (大小未知)")
            
            if len(_temp_files) > 10:
                lines.append(f"  ... 还有 {len(_temp_files) - 10} 个文件")
            
            lines.append("\n确认文件列表:")
            for i, file_path in enumerate(_confirmed_files[:5]):
                try:
                    size = os.path.getsize(file_path)
                    lines.append(f"  ✅ [{i+1}] {os.path.basename(file_path)} ({size} bytes)")
                except:
                    lines.append(f"  ✅ [{i+1}] {os.path.basename(file_path)} (大小未知)")
            
            if len(_confirmed_files) > 5:
                lines.append(f"  ... 还有 {len(_confirmed_files) - 5} 个确认文件")
        
        return "\n".join(lines)

    elif operation == "confirm-file":
        confirm_file = args.get("confirm_file", "")
        
        if not _current_workspace:
            return "❌ 错误: 未创建临时工作区"
        
        temp_file_path = os.path.join(_current_workspace, confirm_file)
        
        if not os.path.exists(temp_file_path):
            return f"❌ 错误: 临时文件不存在: {temp_file_path}"
        
        # 移动到确认区域
        confirmed_area = os.path.join(_current_workspace, "confirmed")
        confirmed_file_path = os.path.join(confirmed_area, confirm_file)
        
        os.makedirs(os.path.dirname(confirmed_file_path), exist_ok=True)
        shutil.move(temp_file_path, confirmed_file_path)
        
        # 更新状态
        if temp_file_path in _temp_files:
            _temp_files.remove(temp_file_path)
        if confirmed_file_path not in _confirmed_files:
            _confirmed_files.append(confirmed_file_path)
        
        return f"✅ 文件已确认到确认区域: {confirmed_file_path}\n临时文件: {len(_temp_files)} 个 -> {len(_temp_files)} 个\n确认文件: {len(_confirmed_files)-1} 个 -> {len(_confirmed_files)} 个"

    elif operation == "confirm-all":
        if not _current_workspace:
            return "❌ 错误: 未创建临时工作区"
        
        confirmed_count = 0
        for temp_file in _temp_files[:]:  # 复制列表以防止在迭代时修改
            relative_path = os.path.relpath(temp_file, _current_workspace)
            confirmed_area = os.path.join(_current_workspace, "confirmed")
            confirmed_file_path = os.path.join(confirmed_area, relative_path)
            
            os.makedirs(os.path.dirname(confirmed_file_path), exist_ok=True)
            shutil.move(temp_file, confirmed_file_path)
            
            _temp_files.remove(temp_file)
            _confirmed_files.append(confirmed_file_path)
            confirmed_count += 1
        
        return f"✅ 已确认所有 {confirmed_count} 个临时文件到确认区域\n已确认文件: {len(_confirmed_files)} 个"

    elif operation == "clean-workspace":
        if not _current_workspace:
            return "❌ 错误: 未创建临时工作区"
        
        # 清理临时文件
        for temp_file in _temp_files[:]:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                _temp_files.remove(temp_file)
            except Exception as e:
                return f"❌ 清理临时文件失败: {str(e)}"
        
        # 记录清理信息
        cleaned_count = confirmed_count - len(_temp_files)  # 实际清理的文件数
        return f"🧹 临时工作区清理完成\n清理临时文件: {cleaned_count} 个\n剩余确认文件: {len(_confirmed_files)} 个\n当前会话: {_active_session}"

    elif operation == "get-workspace-path":
        if not _current_workspace:
            return "❌ 错误: 未创建临时工作区"
        return f"📍 临时工作区路径: {_current_workspace}"

    elif operation == "auto-manage":
        if not _current_workspace:
            return "❌ 错误: 未创建临时工作区"
        
        temp_count = len(_temp_files)
        confirmed_count = len(_confirmed_files)
        
        if temp_count > 10:  # 假设阈值为10个临时文件
            return f"⚠️  临时文件数量 ({temp_count}) 达到阈值，建议确认或清理:\n1. 使用 confirm-all 操作确认所有文件\n2. 使用 confirm-file 操作选择性确认\n3. 使用 clean-workspace 清理临时文件\n\n当前文件:\n{chr(10).join(_temp_files[:5])}\n...{chr(10) if temp_count > 5 else ''}"
        else:
            return f"✅ 临时工作区状态正常\n临时文件: {temp_count}\n确认文件: {confirmed_count}\n阈值: 10\n状态: 正常运行"

    elif operation == "integrate-with-git":
        if not _current_workspace:
            return "❌ 错误: 未创建临时工作区"
        
        repo_path = args.get("repo_path", ".")
        confirm_to_git = args.get("confirm_to_git", True)
        
        if confirm_to_git:
            # 将确认区域的文件复制到Git仓库
            confirmed_area = os.path.join(_current_workspace, "confirmed")
            if os.path.exists(confirmed_area):
                import subprocess
                try:
                    # 获取确认区域的所有文件
                    git_add_cmd = ["git", "add"]
                    files_added = 0
                    for root, dirs, filenames in os.walk(confirmed_area):
                        for filename in filenames:
                            file_path = os.path.join(root, filename)
                            rel_path = os.path.relpath(file_path, confirmed_area)
                            target_path = os.path.join(repo_path, rel_path)
                            
                            # 确保目标目录存在
                            os.makedirs(os.path.dirname(target_path), exist_ok=True)
                            
                            # 复制文件到目标位置
                            import shutil
                            shutil.copy2(file_path, target_path)
                            git_add_cmd.append(rel_path)
                            files_added += 1
                    
                    # 添加到Git暂存区
                    if files_added > 0:
                        subprocess.run(["git", "add"] + [os.path.join(repo_path, rel_path) 
                                                        for root, dirs, filenames in os.walk(confirmed_area)
                                                        for filename in filenames
                                                        for rel_path in [os.path.relpath(os.path.join(root, filename), confirmed_area)]],
                                      cwd=repo_path, capture_output=True)
                    
                    return f"✅ 成功将 {files_added} 个确认文件集成到Git仓库: {repo_path}"
                    
                except Exception as e:
                    return f"❌ Git集成失败: {str(e)}"
            else:
                return "❌ 确认区域不存在或为空"
        else:
            return f"📊 临时工作区状态:\n  会话: {_active_session}\n  临时文件: {len(_temp_files)}\n  确认文件: {len(_confirmed_files)}\n  路径: {_current_workspace}"

    else:
        return f"❌ 未知操作: {operation}\n可用操作: create-workspace, add-file, list-files, confirm-file, confirm-all, clean-workspace, get-workspace-path, auto-manage, integrate-with-git"


def get_manifest() -> Dict[str, Any]:
    """
    Claude Skills标准技能清单
    """
    return {
        "name": "dnaspec-temp-workspace",
        "description": "管理AI生成临时文件的安全工作区技能，防止项目污染",
        "version": "1.0.0",
        "created_at": datetime.now().isoformat(),
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "description": "操作类型",
                    "enum": ["create-workspace", "add-file", "list-files", "confirm-file", 
                            "confirm-all", "clean-workspace", "get-workspace-path", 
                            "auto-manage", "integrate-with-git"],
                    "default": "status"
                },
                "file_path": {
                    "type": "string",
                    "description": "文件路径（add-file, confirm-file操作需要）"
                },
                "content": {
                    "type": "string",
                    "description": "文件内容（add-file操作需要）"
                },
                "confirm_file": {
                    "type": "string",
                    "description": "要确认的文件（confirm-file操作需要）"
                },
                "target_dir": {
                    "type": "string",
                    "description": "目标目录（add-file操作可选）",
                    "default": ""
                },
                "detailed": {
                    "type": "boolean",
                    "description": "是否返回详细信息",
                    "default": False
                },
                "repo_path": {
                    "type": "string",
                    "description": "Git仓库路径（integrate-with-git操作需要）",
                    "default": "."
                },
                "confirm_to_git": {
                    "type": "boolean",
                    "description": "是否将确认文件提交到Git（integrate-with-git操作需要）",
                    "default": True
                }
            },
            "required": ["operation"]
        }
    }