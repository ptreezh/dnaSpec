# task_discovery.py (完整实现)
import os
from pathlib import Path
import json

class TaskDiscovery:
    def __init__(self, start_directory=None):
        self.start_directory = Path(start_directory or os.getcwd()).resolve()
        self.project_root = self._find_project_root()
    
    def _find_project_root(self):
        current_path = self.start_directory
        while current_path != current_path.parent:
            if any((
                (current_path / "PROJECT_SPEC.json").exists(),
                (current_path / ".git").exists(),
                (current_path / "package.json").exists(),
                (current_path / "requirements.txt").exists(),
                (current_path / "setup.py").exists()
            )):
                return current_path
            current_path = current_path.parent
        return self.start_directory
    
    def discover_tasks(self):
        all_tasks = []
        current_path = self.start_directory
        
        while current_path != current_path.parent:
            tasks_in_dir = self._find_and_parse_tasks_in_directory(current_path)
            all_tasks.extend(tasks_in_dir)
            
            if current_path == self.project_root:
                break
            current_path = current_path.parent
        
        return all_tasks
    
    def _find_and_parse_tasks_in_directory(self, directory):
        tasks = []
        task_files_patterns = [
            directory / "PROJECT_SPEC.json",
            directory / "tasks.json",
            directory / "todo.md",
            directory / "task.md",
            directory / "TODO.md",  # 这容大小写
            directory / "TASK.md",  # 这容大小写
            directory / ".tasks.json",
            directory / "project_plan.md"
        ]

        # 跟踪已处理的文件，避免重复处理（在Windows上文件名不区分大小写）
        processed_files = set()

        for task_file_path in task_files_patterns:
            if task_file_path.exists():
                # 获取规范化的真实路径，以处理大小写不敏感的系统
                try:
                    real_path = os.path.realpath(task_file_path)
                except (OSError, ValueError):
                    # 如果无法获取真实路径，则使用字符串形式的规范化路径
                    real_path = os.path.normcase(str(task_file_path))

                if real_path in processed_files:
                    continue  # 跳过已处理的文件

                processed_files.add(real_path)

                parsed_tasks = self._parse_task_file(task_file_path)
                for task in parsed_tasks:
                    task['source_file'] = str(task_file_path)
                tasks.extend(parsed_tasks)

        return tasks
    
    def _parse_task_file(self, file_path):
        if file_path.suffix == '.json':
            return self._parse_json_file(file_path)
        elif file_path.suffix in ['.md', '.txt']:
            return self._parse_markdown_file(file_path)
        else:
            return []
    
    def _parse_json_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            tasks = []
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, str):
                        tasks.append({
                            'description': item,
                            'status': 'pending'
                        })
                    elif isinstance(item, dict):
                        tasks.append(item)
            elif isinstance(data, dict):
                possible_task_keys = ['tasks', 'todo', 'items', 'work_items']
                for key in possible_task_keys:
                    if key in data and isinstance(data[key], list):
                        for item in data[key]:
                            if isinstance(item, str):
                                tasks.append({
                                    'description': item,
                                    'status': 'pending'
                                })
                            elif isinstance(item, dict):
                                tasks.append(item)
            
            return tasks
        except Exception:
            return []
    
    def _parse_markdown_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tasks = []
            lines = content.split('\n')
            
            for line in lines:
                line = line.strip()
                # 只处理以任务标记开头的行
                if line.startswith('- [ ]'):
                    # 通用未完成任务处理
                    task_text = line.replace('- [ ]', '').strip()
                    if task_text:
                        tasks.append({
                            'description': task_text,
                            'status': 'pending'
                        })
                elif line.startswith('- [x]'):
                    # 通用完成任务处理
                    task_text = line.replace('- [x]', '').strip()
                    if task_text:
                        tasks.append({
                            'description': task_text,
                            'status': 'completed'
                        })
                elif line.startswith('TODO:'):
                    task_text = line.replace('TODO:', '').strip()
                    if task_text:
                        tasks.append({
                            'description': task_text,
                            'status': 'pending'
                        })
                elif line.startswith('TASK:'):
                    task_text = line.replace('TASK:', '').strip()
                    if task_text:
                        tasks.append({
                            'description': task_text,
                            'status': 'pending'
                        })
            
            return tasks
        except Exception:
            return []