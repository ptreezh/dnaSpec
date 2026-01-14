import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Any, Dict, List
from dataclasses import dataclass
from .hooks.hook_system import hook_manager, HookContext, HookType

@dataclass
class TaskInfo:
    """任务信息"""
    task_id: str
    task_func: Callable
    args: tuple
    kwargs: dict
    status: str = 'pending'
    result: Any = None
    error: Exception = None

class BackgroundTaskManager:
    """后台任务管理器，处理并发控制"""
    
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.task_queue: List[TaskInfo] = []
        self.max_concurrent_tasks = 5
        self.current_running_count = 0
        self.initialized = False
    
    def initialize(self):
        """初始化后台任务管理器"""
        self.initialized = True
        print("BackgroundTaskManager initialized")
    
    def shutdown(self):
        """关闭后台任务管理器"""
        # 取消所有正在运行的任务
        for task in self.running_tasks.values():
            task.cancel()
        
        self.executor.shutdown(wait=True)
        self.initialized = False
        print("BackgroundTaskManager shutdown")
    
    async def submit_task(self, task_id: str, task_func: Callable, *args, **kwargs) -> asyncio.Task:
        """提交后台任务"""
        # 触发工具注册hook
        context = HookContext(
            hook_name='tool_registered',
            hook_type=HookType.TOOL,
            data={
                'task_id': task_id,
                'task_func': task_func,
                'args': args,
                'kwargs': kwargs
            }
        )
        await hook_manager.trigger_hook('tool_registered', context)
        
        # 创建任务信息
        task_info = TaskInfo(task_id, task_func, args, kwargs)
        
        # 如果当前运行任务数少于最大并发数，直接运行
        if self.current_running_count < self.max_concurrent_tasks:
            return await self._execute_task(task_info)
        else:
            # 否则加入队列等待
            self.task_queue.append(task_info)
            return None
    
    async def _execute_task(self, task_info: TaskInfo) -> asyncio.Task:
        """执行任务"""
        self.current_running_count += 1
        task_info.status = 'running'
        
        # 触发工具执行前hook
        context = HookContext(
            hook_name='tool_before_execute',
            hook_type=HookType.TOOL,
            data={'task_info': task_info}
        )
        await hook_manager.trigger_hook('tool_before_execute', context)
        
        async def run_task():
            try:
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    self.executor,
                    lambda: task_info.task_func(*task_info.args, **task_info.kwargs)
                )
                
                task_info.result = result
                task_info.status = 'completed'
                
                # 触发工具执行后hook
                context = HookContext(
                    hook_name='tool_after_execute',
                    hook_type=HookType.TOOL,
                    data={'task_info': task_info, 'result': result}
                )
                await hook_manager.trigger_hook('tool_after_execute', context)
                
            except Exception as e:
                task_info.error = e
                task_info.status = 'failed'
                
                # 触发工具错误hook
                context = HookContext(
                    hook_name='tool_error',
                    hook_type=HookType.TOOL,
                    data={'task_info': task_info, 'error': e}
                )
                await hook_manager.trigger_hook('tool_error', context)
            
            finally:
                self.current_running_count -= 1
                # 从运行列表中移除
                if task_info.task_id in self.running_tasks:
                    del self.running_tasks[task_info.task_id]
                
                # 尝试执行队列中的下一个任务
                await self._process_next_queued_task()
        
        # 添加到运行任务列表
        task = asyncio.create_task(run_task())
        self.running_tasks[task_info.task_id] = task
        
        return task
    
    async def _process_next_queued_task(self):
        """处理队列中的下一个任务"""
        if self.task_queue and self.current_running_count < self.max_concurrent_tasks:
            next_task = self.task_queue.pop(0)
            await self._execute_task(next_task)
    
    def get_task_status(self, task_id: str) -> str:
        """获取任务状态"""
        if task_id in self.running_tasks:
            return 'running'
        # 检查已完成的任务
        for task_info in self.task_queue:
            if task_info.task_id == task_id:
                return task_info.status
        return 'not_found'
    
    def get_all_tasks(self) -> List[TaskInfo]:
        """获取所有任务信息"""
        return list(self.running_tasks.values()) + self.task_queue