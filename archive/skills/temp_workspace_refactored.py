"""
临时工作区技能 - 重构版本
符合DNASPEC标准化技能接口规范
"""
from typing import Dict, Any
import os
import tempfile
import shutil
from pathlib import Path
import subprocess
from src.dna_spec_kit_integration.core.skill_base import BaseSkill, DetailLevel


class WorkspaceSkill(BaseSkill):
    """工作区管理技能 - 用于管理AI生成的文件，提供安全的工作流"""

    def __init__(self):
        super().__init__(
            name="workspace",
            description="管理AI生成的文件，提供安全的工作流和隔离机制"
        )
        # 全局变量存储当前工作会话
        self.current_temp_workspace = None
        self.confirmed_area = None
        self.max_temp_files = 20  # 临时文件数量阈值
    
    def _execute_skill_logic(self, input_text: str, detail_level: DetailLevel, 
                          options: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """执行临时工作区技能逻辑"""
        operation = options.get("operation", "")
        file_content = options.get("file_content", "")
        file_path = options.get("file_path", "")
        confirm_file = options.get("confirm_file", "")
        
        result_data = {
            "operation": operation,
            "file_path": file_path
        }
        
        if operation == "create-workspace":
            result_data["result"] = self.create_temp_workspace()
            result_data["workspace_path"] = self.current_temp_workspace
        elif operation == "add-file":
            result_data["result"] = self.add_file_to_temp_workspace(file_path, file_content)
            result_data["workspace_path"] = self.current_temp_workspace
        elif operation == "list-files":
            files_list = self.list_files_in_temp_workspace()
            result_data["result"] = files_list
            result_data["files"] = files_list.split('\n')[2:] if '\n' in files_list else []  # 提取文件列表
            result_data["workspace_path"] = self.current_temp_workspace
            result_data["file_count"] = len([f for f in result_data["files"] if f.strip() and not f.strip().startswith("临时工作区中没有文件")])
        elif operation == "confirm-file":
            result_data["result"] = self.confirm_file_from_temp_workspace(confirm_file)
            result_data["confirmed_file"] = confirm_file
        elif operation == "confirm-all":
            result_data["result"] = self.confirm_all_files_from_temp_workspace()
        elif operation == "clean-workspace":
            result_data["result"] = self.clean_temp_workspace()
            result_data["workspace_path"] = self.current_temp_workspace
        elif operation == "get-workspace-path":
            result_data["result"] = self.get_temp_workspace_path()
            result_data["workspace_path"] = self.current_temp_workspace
        elif operation == "auto-manage":
            result_data["result"] = self.auto_manage_workspace()
        else:
            result_data["result"] = f"未知操作: {operation}"
        
        return result_data
    
    def _format_output(self, result_data: Dict[str, Any], detail_level: DetailLevel) -> Dict[str, Any]:
        """根据详细程度格式化输出结果"""
        if detail_level == DetailLevel.BASIC:
            # 基础级别只返回核心信息
            return {
                "operation": result_data["operation"],
                "result": result_data["result"][:200] + "..." if len(result_data["result"]) > 200 else result_data["result"],
                "workspace_path": result_data.get("workspace_path", "")
            }
        elif detail_level == DetailLevel.STANDARD:
            # 标准级别返回标准信息
            formatted_data = {
                "operation": result_data["operation"],
                "file_path": result_data["file_path"],
                "result": result_data["result"],
                "workspace_path": result_data.get("workspace_path", "")
            }
            
            # 添加特定操作的额外信息
            if "confirmed_file" in result_data:
                formatted_data["confirmed_file"] = result_data["confirmed_file"]
                
            return formatted_data
        else:  # DETAILED
            # 详细级别返回完整信息
            return result_data
    
    def create_temp_workspace(self) -> str:
        """
        创建临时工作区
        """
        # 创建临时目录
        self.current_temp_workspace = tempfile.mkdtemp(prefix="ai_temp_workspace_")
        
        # 创建确认区域
        self.confirmed_area = os.path.join(self.current_temp_workspace, "confirmed")
        os.makedirs(self.confirmed_area, exist_ok=True)
        
        return f"临时工作区已创建: {self.current_temp_workspace}"
    
    def add_file_to_temp_workspace(self, file_path: str, content: str) -> str:
        """
        添加文件到临时工作区
        """
        if not self.current_temp_workspace:
            return "错误: 未创建临时工作区，请先执行create-workspace操作"
        
        # 确保临时工作区路径存在
        temp_file_path = os.path.join(self.current_temp_workspace, file_path)
        os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
        
        # 写入文件内容
        with open(temp_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 检查是否需要整理清理
        result = self.auto_manage_workspace()
        
        return f"文件已添加到临时工作区: {temp_file_path}\n{result}"
    
    def list_files_in_temp_workspace(self) -> str:
        """
        列出临时工作区中的文件
        """
        if not self.current_temp_workspace:
            return "错误: 未创建临时工作区"
        
        files = []
        for root, dirs, filenames in os.walk(self.current_temp_workspace):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                if not file_path.startswith(os.path.join(self.current_temp_workspace, "confirmed")):
                    files.append(file_path)
        
        if not files:
            return "临时工作区中没有文件"
        
        result = f"临时工作区中的文件 ({len(files)} 个):\n"
        for file_path in files:
            result += f"  - {file_path}\n"
        
        return result
    
    def confirm_file_from_temp_workspace(self, file_path: str) -> str:
        """
        将文件从临时工作区确认到确认区域
        """
        if not self.current_temp_workspace:
            return "错误: 未创建临时工作区"
        
        temp_file_path = os.path.join(self.current_temp_workspace, file_path)
        confirmed_file_path = os.path.join(self.confirmed_area, file_path)
        
        if not os.path.exists(temp_file_path):
            return f"错误: 临时文件不存在: {temp_file_path}"
        
        # 确保目标目录存在
        os.makedirs(os.path.dirname(confirmed_file_path), exist_ok=True)
        
        # 复制文件到确认区域
        shutil.copy2(temp_file_path, confirmed_file_path)
        
        return f"文件已确认到确认区域: {confirmed_file_path}"
    
    def confirm_all_files_from_temp_workspace(self) -> str:
        """
        将临时工作区中的所有文件确认到确认区域
        """
        if not self.current_temp_workspace:
            return "错误: 未创建临时工作区"
        
        files = []
        for root, dirs, filenames in os.walk(self.current_temp_workspace):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                if not file_path.startswith(os.path.join(self.current_temp_workspace, "confirmed")):
                    files.append(os.path.relpath(file_path, self.current_temp_workspace))
        
        confirmed_count = 0
        for file_path in files:
            temp_file_path = os.path.join(self.current_temp_workspace, file_path)
            confirmed_file_path = os.path.join(self.confirmed_area, file_path)
            
            os.makedirs(os.path.dirname(confirmed_file_path), exist_ok=True)
            shutil.copy2(temp_file_path, confirmed_file_path)
            confirmed_count += 1
        
        return f"已确认 {confirmed_count} 个文件到确认区域"
    
    def clean_temp_workspace(self) -> str:
        """
        清理临时工作区
        """
        if not self.current_temp_workspace:
            return "错误: 未创建临时工作区"
        
        try:
            shutil.rmtree(self.current_temp_workspace)
            self.current_temp_workspace = None
            return "临时工作区已清理"
        except Exception as e:
            return f"清理临时工作区失败: {str(e)}"
    
    def get_temp_workspace_path(self) -> str:
        """
        获取临时工作区路径
        """
        if not self.current_temp_workspace:
            return "错误: 未创建临时工作区"
        
        return self.current_temp_workspace
    
    def auto_manage_workspace(self) -> str:
        """
        自动管理工作区：当临时文件数量超过阈值时进行整理
        """
        if not self.current_temp_workspace:
            return "错误: 未创建临时工作区"
        
        # 计算临时文件数量（排除confirmed目录）
        temp_file_count = 0
        for root, dirs, filenames in os.walk(self.current_temp_workspace):
            if not root.startswith(os.path.join(self.current_temp_workspace, "confirmed")):
                temp_file_count += len(filenames)
        
        if temp_file_count > self.max_temp_files:
            # 超过阈值，进行整理
            result = f"临时文件数量 ({temp_file_count}) 超过阈值 ({self.max_temp_files})，建议进行整理:\n"
            result += "1. 选择需要确认的文件: 使用 confirm-file 操作\n"
            result += "2. 或确认所有文件: 使用 confirm-all 操作\n"
            result += "3. 或清理临时工作区: 使用 clean-workspace 操作\n"
            result += self.list_files_in_temp_workspace()
            return result
        else:
            return f"临时文件数量正常 ({temp_file_count}/{self.max_temp_files})"