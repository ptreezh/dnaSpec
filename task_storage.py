# task_storage.py (完整实现)
import os
from pathlib import Path
import json
from datetime import datetime

class TaskStorage:
    def __init__(self, working_directory=None):
        """
        初始化任务存储器
        Args:
            working_directory: 工作目录，默认为当前工作目录
        """
        self.working_directory = Path(working_directory or os.getcwd()).resolve()
    
    def store_tasks(self, tasks, filename=None):
        """
        将任务存储到doc目录
        Args:
            tasks: 任务列表
            filename: 存储文件名，如果为None则自动选择
        Returns:
            存储文件的路径
        """
        # 确保doc目录存在
        doc_path = self.working_directory / "doc"
        doc_path.mkdir(exist_ok=True)
        
        # 如果未指定文件名，根据任务状态确定文件名
        if not filename:
            filename = self._determine_filename_from_tasks(tasks)
        
        file_path = doc_path / filename
        
        # 根据文件扩展名选择存储格式
        if file_path.suffix.lower() == '.json':
            self._store_as_json(tasks, file_path)
        elif file_path.suffix.lower() == '.md':
            self._store_as_markdown(tasks, file_path)
        else:
            # 默认使用markdown格式
            markdown_path = doc_path / f"{file_path.stem}.md"
            self._store_as_markdown(tasks, markdown_path)
            file_path = markdown_path
        
        return str(file_path)
    
    def _determine_filename_from_tasks(self, tasks):
        """
        根据任务内容确定文件名
        默认使用task.md作为主要任务文件
        Args:
            tasks: 任务列表
        Returns:
            适合的文件名
        """
        # 默认使用task.md，除非特别指定其他情况
        return "task.md"
    
    def _store_as_markdown(self, tasks, file_path):
        """
        以Markdown格式存储任务
        Args:
            tasks: 任务列表
            file_path: 存储路径
        """
        content = f"# Task List\n\nGenerated at: {datetime.now().isoformat()}\n\n"
        
        for task in tasks:
            if isinstance(task, dict):
                description = task.get('description', 'Unnamed task')
                status = task.get('status', 'pending')
                # 转换状态为复选框
                status_marker = 'x' if status.lower() in ['completed', 'done', 'finished'] else ' '
                content += f"- [{status_marker}] {description}\n"
            else:
                # 对于非字典类型，视为描述文本
                content += f"- [ ] {str(task)}\n"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _store_as_json(self, tasks, file_path):
        """
        以JSON格式存储任务
        Args:
            tasks: 任务列表
            file_path: 存储路径
        """
        task_data = {
            "tasks": tasks,
            "generated_at": datetime.now().isoformat(),
            "format_version": "1.0.0"
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(task_data, f, indent=2, ensure_ascii=False)
    
    def update_task_status(self, task_description, new_status):
        """
        更新特定任务的状态
        Args:
            task_description: 任务描述（用作标识）
            new_status: 新状态
        Returns:
            更新成功返回True，否则返回False
        """
        task_lower = task_description.lower()
        
        # 查找doc目录下的任务文件
        doc_path = self.working_directory / "doc"
        if not doc_path.exists():
            return False
        
        # 尝试更新markdown文件中的任务状态
        for task_file in doc_path.glob("*.md"):
            if self._update_markdown_task_status(task_file, task_lower, new_status):
                return True
        
        # 尝试更新json文件中的任务状态
        for task_file in doc_path.glob("*.json"):
            if self._update_json_task_status(task_file, task_lower, new_status):
                return True
        
        return False
    
    def _update_markdown_task_status(self, file_path, task_description_lower, new_status):
        """
        更新Markdown文件中的任务状态
        Args:
            file_path: 文件路径
            task_description_lower: 任务描述（小写）
            new_status: 新状态
        Returns:
            更新成功返回True
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            updated_any = False
            updated_lines = []
            
            for line in lines:
                # 检查是否包含目标任务
                if task_description_lower in line.lower() and ('- [ ]' in line or '- [x]' in line):
                    # 更新状态标记
                    if new_status.lower() in ['completed', 'done', 'finished']:
                        updated_line = line.replace('- [ ]', '- [x]').replace('- [X]', '- [x]')
                    else:
                        updated_line = line.replace('- [x]', '- [ ]').replace('- [X]', '- [ ]')
                    updated_lines.append(updated_line)
                    updated_any = True
                else:
                    updated_lines.append(line)
            
            if updated_any:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(updated_lines)
            
            return updated_any
        except Exception:
            return False
    
    def _update_json_task_status(self, file_path, task_description_lower, new_status):
        """
        更新JSON文件中的任务状态
        Args:
            file_path: 文件路径
            task_description_lower: 任务描述（小写）
            new_status: 新状态
        Returns:
            更新成功返回True
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            updated_any = False
            
            # 查找tasks数组中的任务
            if 'tasks' in data and isinstance(data['tasks'], list):
                for task in data['tasks']:
                    if isinstance(task, dict) and 'description' in task:
                        if task_description_lower in task['description'].lower():
                            task['status'] = new_status
                            updated_any = True
                    elif isinstance(task, str) and task_description_lower in task.lower():
                        # 如果任务是字符串，转换为字典格式
                        idx = data['tasks'].index(task)
                        data['tasks'][idx] = {
                            'description': task,
                            'status': new_status
                        }
                        updated_any = True
            
            if updated_any:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            
            return updated_any
        except Exception:
            return False