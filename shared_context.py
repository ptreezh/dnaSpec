# shared_context.py (完整实现)
import time
from typing import Dict, Any, List
from task_discovery import TaskDiscovery
from task_storage import TaskStorage

class Task:
    """任务类，表示单个任务"""
    def __init__(self, task_id: str, description: str, assigned_to=None, status="pending", source_file=None):
        self.id = task_id
        self.description = description
        self.assigned_to = assigned_to
        self.status = status
        self.source_file = source_file
        self.created_at = time.time()
        self.updated_at = time.time()

class SharedContextManager:
    """共享上下文管理器，完全符合宪法要求"""
    def __init__(self, working_directory: str = None):
        """
        初始化共享上下文管理器
        Args:
            working_directory: 工作目录，默认为当前目录
        """
        self.tasks = {}  # 任务ID到Task对象的映射
        self.agents = {}  # 智能体ID到智能体对象的映射
        self.context_state = {}  # 共享背景状态
        self.task_discovery = TaskDiscovery(working_directory)
        self.task_storage = TaskStorage(working_directory)
        
        # 初始化时从项目文档加载任务
        self._load_tasks_from_project_docs()
    
    def _load_tasks_from_project_docs(self):
        """从项目文档加载任务到内存"""
        discovered_tasks = self.task_discovery.discover_tasks()
        
        for i, task_data in enumerate(discovered_tasks):
            task_id = f"discovered_{i}_{int(time.time())}"
            
            if isinstance(task_data, dict):
                task = Task(
                    task_id=task_id,
                    description=task_data.get('description', f'Discovered task {i}'),
                    status=task_data.get('status', 'pending'),
                    source_file=task_data.get('source_file', 'discovered_from_docs')
                )
            else:
                task = Task(
                    task_id=task_id,
                    description=str(task_data),
                    status='pending',
                    source_file='discovered_from_docs'
                )
            
            self.tasks[task.id] = task
    
    def register_task(self, task: Task):
        """
        注册新任务到共享上下文，同时保存到文档
        Args:
            task: 要注册的任务对象
        """
        self.tasks[task.id] = task

        # 同步到文档
        task_doc_format = {
            'id': task.id,
            'description': task.description,
            'status': task.status,
            'assigned_to': task.assigned_to,
            'source_file': task.source_file
        }

        # 确保至少存储一次，不管源文档更新是否成功
        self.task_storage.store_tasks([task_doc_format])
    
    def update_task_status(self, task_id: str, status: str, agent_id: str = None):
        """
        更新任务状态到共享上下文，同时同步到文档
        Args:
            task_id: 任务ID
            status: 新状态
            agent_id: 认领任务的智能体ID
        """
        if task_id in self.tasks:
            task = self.tasks[task_id]
            
            # 更新内存中的任务状态
            old_status = task.status
            task.status = status
            task.assigned_to = agent_id
            task.updated_at = time.time()
            
            # 尝同步到源文档，如果失败则存储新任务
            if task.source_file and 'discovered_from_docs' not in task.source_file:
                success = self.task_storage.update_task_status(task.description, status)
                if not success:
                    # 如果更新源文档失败，保存到本地任务文件
                    self.task_storage.store_tasks([{
                        'id': task.id,
                        'description': task.description,
                        'status': task.status,
                        'assigned_to': task.assigned_to
                    }])
            else:
                # 对于新创建的任务，保存到本地文档
                self.task_storage.store_tasks([{
                    'id': task.id,
                    'description': task.description,
                    'status': task.status,
                    'assigned_to': task.assigned_to
                }])
    
    def get_available_tasks(self, agent_capabilities: List[str]) -> List[Task]:
        """
        获取智能体能力匹配的未分配任务
        Args:
            agent_capabilities: 智能体能力列表
        Returns:
            匹配的可用任务列表
        """
        available_tasks = []
        
        for task in self.tasks.values():
            if task.status == "pending" and task.assigned_to is None:
                # 检查任务描述是否包含智能体能力关键词
                task_description_lower = task.description.lower()
                if any(cap.lower() in task_description_lower for cap in agent_capabilities):
                    available_tasks.append(task)
        
        return available_tasks