"""
Temporary Workspace Skill - Refactored Version
Compliant with DNASPEC Standardized Skill Interface Specification
"""
from typing import Dict, Any
import os
import tempfile
import shutil
from pathlib import Path
import subprocess
from ..skill_base_en import BaseSkill, DetailLevel


class TempWorkspaceSkill(BaseSkill):
    """Temporary Workspace Skill - Used to manage AI-generated temporary files to avoid project clutter"""
    
    def __init__(self):
        super().__init__(
            name="temp-workspace",
            description="Used to manage AI-generated temporary files to avoid project clutter"
        )
        # Global variables to store current session
        self.current_temp_workspace = None
        self.confirmed_area = None
        self.max_temp_files = 20  # Temporary file count threshold
    
    def _execute_skill_logic(self, input_text: str, detail_level: DetailLevel, 
                          options: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute temporary workspace skill logic"""
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
            result_data["files"] = files_list.split('\n')[2:] if '\n' in files_list else []  # Extract file list
            result_data["workspace_path"] = self.current_temp_workspace
            result_data["file_count"] = len([f for f in result_data["files"] if f.strip() and not f.strip().startswith("No files in temporary workspace")])
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
            result_data["result"] = f"Unknown operation: {operation}"
        
        return result_data
    
    def _format_output(self, result_data: Dict[str, Any], detail_level: DetailLevel) -> Dict[str, Any]:
        """Format output result based on detail level"""
        if detail_level == DetailLevel.BASIC:
            # Basic level returns core information only
            return {
                "operation": result_data["operation"],
                "result": result_data["result"][:200] + "..." if len(result_data["result"]) > 200 else result_data["result"],
                "workspace_path": result_data.get("workspace_path", "")
            }
        elif detail_level == DetailLevel.STANDARD:
            # Standard level returns standard information
            formatted_data = {
                "operation": result_data["operation"],
                "file_path": result_data["file_path"],
                "result": result_data["result"],
                "workspace_path": result_data.get("workspace_path", "")
            }
            
            # Add specific operation extra information
            if "confirmed_file" in result_data:
                formatted_data["confirmed_file"] = result_data["confirmed_file"]
                
            return formatted_data
        else:  # DETAILED
            # Detailed level returns complete information
            return result_data
    
    def create_temp_workspace(self) -> str:
        """
        Create temporary workspace
        """
        # Create temporary directory
        self.current_temp_workspace = tempfile.mkdtemp(prefix="ai_temp_workspace_")
        
        # Create confirmation area
        self.confirmed_area = os.path.join(self.current_temp_workspace, "confirmed")
        os.makedirs(self.confirmed_area, exist_ok=True)
        
        return f"Temporary workspace created: {self.current_temp_workspace}"
    
    def add_file_to_temp_workspace(self, file_path: str, content: str) -> str:
        """
        Add file to temporary workspace
        """
        if not self.current_temp_workspace:
            return "Error: Temporary workspace not created, please execute create-workspace operation first"
        
        # Ensure temporary workspace path exists
        temp_file_path = os.path.join(self.current_temp_workspace, file_path)
        os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
        
        # Write file content
        with open(temp_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Check if cleanup is needed
        result = self.auto_manage_workspace()
        
        return f"File added to temporary workspace: {temp_file_path}\n{result}"
    
    def list_files_in_temp_workspace(self) -> str:
        """
        List files in temporary workspace
        """
        if not self.current_temp_workspace:
            return "Error: Temporary workspace not created"
        
        files = []
        for root, dirs, filenames in os.walk(self.current_temp_workspace):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                if not file_path.startswith(os.path.join(self.current_temp_workspace, "confirmed")):
                    files.append(file_path)
        
        if not files:
            return "No files in temporary workspace"
        
        result = f"Files in temporary workspace ({len(files)} files):\n"
        for file_path in files:
            result += f"  - {file_path}\n"
        
        return result
    
    def confirm_file_from_temp_workspace(self, file_path: str) -> str:
        """
        Confirm file from temporary workspace to confirmation area
        """
        if not self.current_temp_workspace:
            return "Error: Temporary workspace not created"
        
        temp_file_path = os.path.join(self.current_temp_workspace, file_path)
        confirmed_file_path = os.path.join(self.confirmed_area, file_path)
        
        if not os.path.exists(temp_file_path):
            return f"Error: Temporary file does not exist: {temp_file_path}"
        
        # Ensure target directory exists
        os.makedirs(os.path.dirname(confirmed_file_path), exist_ok=True)
        
        # Copy file to confirmation area
        shutil.copy2(temp_file_path, confirmed_file_path)
        
        return f"File confirmed to confirmation area: {confirmed_file_path}"
    
    def confirm_all_files_from_temp_workspace(self) -> str:
        """
        Confirm all files from temporary workspace to confirmation area
        """
        if not self.current_temp_workspace:
            return "Error: Temporary workspace not created"
        
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
        
        return f"Confirmed {confirmed_count} files to confirmation area"
    
    def clean_temp_workspace(self) -> str:
        """
        Clean temporary workspace
        """
        if not self.current_temp_workspace:
            return "Error: Temporary workspace not created"
        
        try:
            shutil.rmtree(self.current_temp_workspace)
            self.current_temp_workspace = None
            return "Temporary workspace cleaned"
        except Exception as e:
            return f"Failed to clean temporary workspace: {str(e)}"
    
    def get_temp_workspace_path(self) -> str:
        """
        Get temporary workspace path
        """
        if not self.current_temp_workspace:
            return "Error: Temporary workspace not created"
        
        return self.current_temp_workspace
    
    def auto_manage_workspace(self) -> str:
        """
        Auto-manage workspace: Organize when temporary file count exceeds threshold
        """
        if not self.current_temp_workspace:
            return "Error: Temporary workspace not created"
        
        # Count temporary files (excluding confirmed directory)
        temp_file_count = 0
        for root, dirs, filenames in os.walk(self.current_temp_workspace):
            if not root.startswith(os.path.join(self.current_temp_workspace, "confirmed")):
                temp_file_count += len(filenames)
        
        if temp_file_count > self.max_temp_files:
            # Exceeds threshold, organize
            result = f"Temporary file count ({temp_file_count}) exceeds threshold ({self.max_temp_files}), suggesting organization:\n"
            result += "1. Select files to confirm: Use confirm-file operation\n"
            result += "2. Or confirm all files: Use confirm-all operation\n"
            result += "3. Or clean temporary workspace: Use clean-workspace operation\n"
            result += self.list_files_in_temp_workspace()
            return result
        else:
            return f"Temporary file count normal ({temp_file_count}/{self.max_temp_files})"