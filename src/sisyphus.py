import asyncio
from typing import Dict, Any, Callable, List
from dataclasses import dataclass
from .hooks.hook_system import hook_manager, HookContext, HookType
from .agents.agent_manager import AgentManager

@dataclass
class TaskSpec:
    """任务规格"""
    name: str
    agent_type: str
    params: Dict[str, Any]
    dependencies: List[str] = None
    priority: int = 0

class SisyphusOrchestrator:
    """Sisyphus 主编排器（默认）"""
    
    def __init__(self):
        self.task_queue: List[TaskSpec] = []
        self.completed_tasks: List[str] = []
        self.agent_manager: AgentManager = None
        self.initialized = False
    
    def initialize(self):
        """初始化编排器"""
        self.initialized = True
        print("SisyphusOrchestrator initialized")
    
    def shutdown(self):
        """关闭编排器"""
        self.initialized = False
        print("SisyphusOrchestrator shutdown")
    
    def set_agent_manager(self, agent_manager: AgentManager):
        """设置代理管理器"""
        self.agent_manager = agent_manager
    
    def add_task(self, task_spec: TaskSpec):
        """添加任务到队列"""
        self.task_queue.append(task_spec)
        self.task_queue.sort(key=lambda x: x.priority, reverse=True)
    
    async def execute_tasks(self):
        """执行所有任务"""
        while self.task_queue:
            # 查找没有未完成依赖的任务
            executable_tasks = []
            for task in self.task_queue[:]:  # 创建副本以避免修改时的问题
                if self._can_execute_task(task):
                    executable_tasks.append(task)
            
            if not executable_tasks:
                print("No executable tasks found, dependencies not met")
                break
            
            # 并行执行可执行任务
            tasks_to_run = []
            for task in executable_tasks:
                task_coro = self._execute_single_task(task)
                tasks_to_run.append(task_coro)
            
            if tasks_to_run:
                await asyncio.gather(*tasks_to_run, return_exceptions=True)
    
    def _can_execute_task(self, task: TaskSpec) -> bool:
        """检查任务是否可以执行（依赖是否都已完成）"""
        if not task.dependencies:
            return True
        
        for dep in task.dependencies:
            if dep not in self.completed_tasks:
                return False
        return True
    
    async def _execute_single_task(self, task: TaskSpec):
        """执行单个任务"""
        try:
            # 触发代理处理前hook
            context = HookContext(
                hook_name='agent_before_process',
                hook_type=HookType.AGENT,
                data={'task': task}
            )
            await hook_manager.trigger_hook('agent_before_process', context)
            
            # 获取指定类型的代理并执行任务
            agent = self.agent_manager.get_agent(task.agent_type)
            if agent:
                result = await agent.process(task.params)
                
                # 触发代理处理后hook
                context = HookContext(
                    hook_name='agent_after_process',
                    hook_type=HookType.AGENT,
                    data={'task': task, 'result': result}
                )
                await hook_manager.trigger_hook('agent_after_process', context)
                
                # 标记任务为已完成
                self.completed_tasks.append(task.name)
                self.task_queue.remove(task)
                
                return result
            else:
                raise ValueError(f"No agent found for type: {task.agent_type}")
        
        except Exception as e:
            print(f"Error executing task {task.name}: {e}")
            # 触发代理错误hook
            context = HookContext(
                hook_name='agent_error',
                hook_type=HookType.AGENT,
                data={'task': task, 'error': e}
            )
            await hook_manager.trigger_hook('agent_error', context)