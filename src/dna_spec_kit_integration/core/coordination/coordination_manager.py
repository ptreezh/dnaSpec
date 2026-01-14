"""
协调管理器模块
负责技能间的协调、工作流编排和数据传递
"""
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio
from concurrent.futures import ThreadPoolExecutor

from .constitution_detector import ConstitutionDetector, ConstitutionInfo


class CoordinationMode(Enum):
    """协调模式枚举"""
    SEQUENTIAL = "sequential"      # 顺序执行
    PARALLEL = "parallel"          # 并行执行
    PIPELINE = "pipeline"          # 流水线执行
    ADAPTIVE = "adaptive"          # 自适应执行


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"            # 等待执行
    RUNNING = "running"            # 正在执行
    COMPLETED = "completed"        # 执行完成
    FAILED = "failed"              # 执行失败
    SKIPPED = "skipped"            # 跳过执行


@dataclass
class CoordinationTask:
    """协调任务数据类"""
    task_id: str
    skill_name: str
    input_data: Dict[str, Any]
    dependencies: List[str]
    status: TaskStatus
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if not self.task_id:
            self.task_id = str(uuid.uuid4())


@dataclass
class CoordinationWorkflow:
    """协调工作流数据类"""
    workflow_id: str
    name: str
    tasks: List[CoordinationTask]
    mode: CoordinationMode
    context: Dict[str, Any]
    status: TaskStatus
    created_at: datetime
    completed_at: Optional[datetime] = None
    results: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.workflow_id is None:
            self.workflow_id = str(uuid.uuid4())
        if self.results is None:
            self.results = {}


class CoordinationManager:
    """
    协调管理器
    负责技能间的协调、工作流编排和数据传递
    """
    
    def __init__(self, constitution_detector: ConstitutionDetector = None):
        """
        初始化协调管理器
        
        Args:
            constitution_detector: 宪法检测器实例
        """
        self.constitution_detector = constitution_detector or ConstitutionDetector()
        self.active_workflows: Dict[str, CoordinationWorkflow] = {}
        self.skill_registry: Dict[str, Any] = {}
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # 加载技能注册表
        self._load_skill_registry()
    
    def _load_skill_registry(self):
        """加载技能注册表"""
        # 预定义的技能映射
        self.skill_registry = {
            "architect": "dnaspec-system-architect",
            "simple-architect": "dnaspec-simple-architect", 
            "system-architect": "dnaspec-system-architect",
            "task-decomposer": "dnaspec-task-decomposer",
            "constraint-generator": "dnaspec-constraint-generator",
            "api-checker": "dnaspec-api-checker",
            "modulizer": "dnaspec-modulizer",
            "context-analyzer": "dnaspec-context-analyzer",
            "context-optimizer": "dnaspec-context-optimizer",
            "cognitive-templater": "dnaspec-cognitive-templater",
            "agent-creator": "dnaspec-agent-creator",
            "cache-manager": "dnaspec-cache-manager",
            "git-operations": "dnaspec-git-operations"
        }
    
    def detect_and_adapt(self) -> bool:
        """
        检测协调机制并自适应调整
        
        Returns:
            bool: 是否应该使用协调模式
        """
        constitution_info = self.constitution_detector.detect_constitution()
        return self.constitution_detector.should_use_coordination()
    
    def create_workflow(self, 
                       name: str,
                       tasks: List[Dict[str, Any]],
                       mode: CoordinationMode = CoordinationMode.SEQUENTIAL,
                       context: Dict[str, Any] = None) -> str:
        """
        创建协调工作流
        
        Args:
            name: 工作流名称
            tasks: 任务列表，每个任务包含 skill_name, input_data, dependencies
            mode: 协调模式
            context: 上下文信息
            
        Returns:
            str: 工作流ID
        """
        if context is None:
            context = {}
        
        # 创建任务对象
        coordination_tasks = []
        for task_config in tasks:
            task = CoordinationTask(
                task_id=task_config.get('task_id', str(uuid.uuid4())),
                skill_name=task_config['skill_name'],
                input_data=task_config.get('input_data', {}),
                dependencies=task_config.get('dependencies', []),
                status=TaskStatus.PENDING
            )
            coordination_tasks.append(task)
        
        # 创建工作流
        workflow = CoordinationWorkflow(
            workflow_id=str(uuid.uuid4()),
            name=name,
            tasks=coordination_tasks,
            mode=mode,
            context=context,
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        )
        
        # 注册工作流
        self.active_workflows[workflow.workflow_id] = workflow
        
        return workflow.workflow_id
    
    def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        执行协调工作流
        
        Args:
            workflow_id: 工作流ID
            
        Returns:
            Dict[str, Any]: 执行结果
        """
        if workflow_id not in self.active_workflows:
            return {
                "success": False,
                "error": f"Workflow not found: {workflow_id}"
            }
        
        workflow = self.active_workflows[workflow_id]
        workflow.status = TaskStatus.RUNNING
        
        try:
            if workflow.mode == CoordinationMode.SEQUENTIAL:
                result = self._execute_sequential_workflow(workflow)
            elif workflow.mode == CoordinationMode.PARALLEL:
                result = self._execute_parallel_workflow(workflow)
            elif workflow.mode == CoordinationMode.PIPELINE:
                result = self._execute_pipeline_workflow(workflow)
            else:  # ADAPTIVE
                result = self._execute_adaptive_workflow(workflow)
            
            workflow.status = TaskStatus.COMPLETED
            workflow.completed_at = datetime.now()
            workflow.results = result
            
            return {
                "success": True,
                "workflow_id": workflow_id,
                "results": result,
                "execution_time": (workflow.completed_at - workflow.created_at).total_seconds()
            }
            
        except Exception as e:
            workflow.status = TaskStatus.FAILED
            workflow.results = {"error": str(e)}
            return {
                "success": False,
                "workflow_id": workflow_id,
                "error": str(e)
            }
    
    def _execute_sequential_workflow(self, workflow: CoordinationWorkflow) -> Dict[str, Any]:
        """顺序执行工作流"""
        results = {}
        
        for task in workflow.tasks:
            task.status = TaskStatus.RUNNING
            task.start_time = datetime.now()
            
            try:
                # 检查依赖
                if not self._check_dependencies(task, results):
                    task.status = TaskStatus.SKIPPED
                    continue
                
                # 执行任务
                task_result = self._execute_single_task(task, results)
                
                if task_result["success"]:
                    task.status = TaskStatus.COMPLETED
                    task.result = task_result["result"]
                    results[task.task_id] = task_result["result"]
                else:
                    task.status = TaskStatus.FAILED
                    task.error = task_result["error"]
                    # 在顺序模式下，失败会终止整个工作流
                    break
                    
            except Exception as e:
                task.status = TaskStatus.FAILED
                task.error = str(e)
                break
            
            task.end_time = datetime.now()
        
        return results
    
    def _execute_parallel_workflow(self, workflow: CoordinationWorkflow) -> Dict[str, Any]:
        """并行执行工作流"""
        # 并行执行没有依赖的任务
        results = {}
        completed_tasks = set()
        
        # 获取可以并行执行的任务组
        task_groups = self._group_parallel_tasks(workflow.tasks)
        
        for group in task_groups:
            # 并行执行组内任务
            group_results = self._execute_task_group_parallel(group, results)
            results.update(group_results)
            completed_tasks.update([task.task_id for task in group])
            
            # 检查是否有依赖完成的任务可以执行
            remaining_tasks = [task for task in workflow.tasks 
                             if task.task_id not in completed_tasks and task.status == TaskStatus.PENDING]
            
            if remaining_tasks:
                # 检查新完成的任务是否解除了某些任务的依赖
                newly_ready = self._get_ready_tasks(remaining_tasks, results)
                for task in newly_ready:
                    task_result = self._execute_single_task(task, results)
                    if task_result["success"]:
                        results[task.task_id] = task_result["result"]
                        completed_tasks.add(task.task_id)
        
        return results
    
    def _execute_pipeline_workflow(self, workflow: CoordinationWorkflow) -> Dict[str, Any]:
        """流水线执行工作流"""
        # 流水线模式：前一任务的输出作为后一任务的输入
        pipeline_data = {}
        
        for task in workflow.tasks:
            task.status = TaskStatus.RUNNING
            task.start_time = datetime.now()
            
            # 准备输入数据（包含流水线数据）
            input_data = task.input_data.copy()
            if pipeline_data:
                input_data["pipeline_data"] = pipeline_data
            
            try:
                task_result = self._execute_task_with_input(task.skill_name, input_data)
                
                if task_result["success"]:
                    task.status = TaskStatus.COMPLETED
                    task.result = task_result["result"]
                    # 更新流水线数据
                    pipeline_data[task.task_id] = task_result["result"]
                else:
                    task.status = TaskStatus.FAILED
                    task.error = task_result["error"]
                    break
                    
            except Exception as e:
                task.status = TaskStatus.FAILED
                task.error = str(e)
                break
            
            task.end_time = datetime.now()
        
        return pipeline_data
    
    def _execute_adaptive_workflow(self, workflow: CoordinationWorkflow) -> Dict[str, Any]:
        """自适应执行工作流"""
        # 根据任务复杂度和依赖关系自动选择执行策略
        results = {}
        
        # 分析任务图
        task_graph = self._analyze_task_graph(workflow.tasks)
        
        # 选择执行策略
        if self._is_dag_with_long_chain(task_graph):
            # 长链依赖，使用流水线模式
            return self._execute_pipeline_workflow(workflow)
        elif self._has_large_parallel_groups(task_graph):
            # 有大量并行任务，使用并行模式
            return self._execute_parallel_workflow(workflow)
        else:
            # 简单依赖图，使用顺序模式
            return self._execute_sequential_workflow(workflow)
    
    def _execute_single_task(self, task: CoordinationTask, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行单个任务"""
        # 准备输入数据
        input_data = task.input_data.copy()
        
        # 添加上下文数据
        if context:
            input_data["context"] = context
        
        # 执行任务
        return self._execute_task_with_input(task.skill_name, input_data)
    
    def _execute_task_with_input(self, skill_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """使用输入数据执行任务"""
        try:
            # 获取技能实现
            skill_impl = self._get_skill_implementation(skill_name)
            
            if skill_impl is None:
                return {
                    "success": False,
                    "error": f"Skill not found: {skill_name}"
                }
            
            # 执行技能
            if hasattr(skill_impl, 'execute'):
                result = skill_impl.execute(**input_data)
            elif hasattr(skill_impl, '_execute_skill_logic'):
                result = skill_impl._execute_skill_logic(**input_data)
            else:
                # 尝试直接调用
                result = skill_impl(**input_data)
            
            return {
                "success": True,
                "result": result
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _check_dependencies(self, task: CoordinationTask, results: Dict[str, Any]) -> bool:
        """检查任务依赖是否满足"""
        for dep_id in task.dependencies:
            if dep_id not in results:
                return False
        return True
    
    def _group_parallel_tasks(self, tasks: List[CoordinationTask]) -> List[List[CoordinationTask]]:
        """将任务分组为可以并行执行的组"""
        groups = []
        remaining_tasks = tasks.copy()
        
        while remaining_tasks:
            # 找到当前可以执行的任务（依赖已满足或无依赖）
            ready_tasks = []
            for task in remaining_tasks:
                if self._check_dependencies(task, {}):  # 在开始时，context为空
                    ready_tasks.append(task)
            
            if not ready_tasks:
                # 如果没有可执行的任务，选择依赖最少的一个
                ready_tasks = [min(remaining_tasks, key=lambda t: len(t.dependencies))]
            
            groups.append(ready_tasks)
            # 移除已分组的任务
            for task in ready_tasks:
                remaining_tasks.remove(task)
        
        return groups
    
    def _execute_task_group_parallel(self, task_group: List[CoordinationTask], 
                                   context: Dict[str, Any]) -> Dict[str, Any]:
        """并行执行任务组"""
        results = {}
        
        # 使用线程池并行执行任务
        futures = []
        for task in task_group:
            future = self.executor.submit(self._execute_single_task, task, context)
            futures.append((task, future))
        
        # 收集结果
        for task, future in futures:
            try:
                result = future.result(timeout=300)  # 5分钟超时
                if result["success"]:
                    results[task.task_id] = result["result"]
                    task.status = TaskStatus.COMPLETED
                    task.result = result["result"]
                else:
                    task.status = TaskStatus.FAILED
                    task.error = result["error"]
            except Exception as e:
                task.status = TaskStatus.FAILED
                task.error = str(e)
        
        return results
    
    def _get_ready_tasks(self, tasks: List[CoordinationTask], 
                        completed_results: Dict[str, Any]) -> List[CoordinationTask]:
        """获取准备好的任务"""
        ready_tasks = []
        for task in tasks:
            if self._check_dependencies(task, completed_results):
                ready_tasks.append(task)
        return ready_tasks
    
    def _analyze_task_graph(self, tasks: List[CoordinationTask]) -> Dict[str, Any]:
        """分析任务依赖图"""
        graph = {}
        for task in tasks:
            graph[task.task_id] = {
                "dependencies": task.dependencies,
                "dependents": []
            }
        
        # 计算依赖关系
        for task_id, task_info in graph.items():
            for dep_id in task_info["dependencies"]:
                if dep_id in graph:
                    graph[dep_id]["dependents"].append(task_id)
        
        return graph
    
    def _is_dag_with_long_chain(self, graph: Dict[str, Any]) -> bool:
        """判断是否为有长链的有向无环图"""
        # 简化的长链检测
        max_depth = 0
        visited = set()
        
        def dfs(node, depth):
            nonlocal max_depth
            if node in visited:
                return depth
            visited.add(node)
            max_depth = max(max_depth, depth)
            
            for dependent in graph.get(node, {}).get("dependents", []):
                dfs(dependent, depth + 1)
        
        # 从根节点开始（无依赖的节点）
        roots = [node for node, info in graph.items() if not info["dependencies"]]
        for root in roots:
            dfs(root, 1)
        
        return max_depth >= 5  # 深度大于等于5认为是长链
    
    def _has_large_parallel_groups(self, graph: Dict[str, Any]) -> bool:
        """判断是否有大量并行任务"""
        max_parallel = 0
        for node, info in graph.items():
            if not info["dependencies"]:  # 根节点
                parallel_count = len(info["dependents"])
                max_parallel = max(max_parallel, parallel_count)
        
        return max_parallel >= 3  # 并行度大于等于3认为是大并行
    
    def _get_skill_implementation(self, skill_name: str):
        """获取技能实现"""
        # 从注册表获取技能名称
        dnaspec_skill_name = self.skill_registry.get(skill_name, skill_name)
        
        # 尝试动态导入技能实现
        try:
            if dnaspec_skill_name == "dnaspec-system-architect":
                import importlib.util
                spec = importlib.util.spec_from_file_location("system_architect", 
                    os.path.join(os.path.dirname(__file__), "..", "..", "..", "spec-kit", "skills", "dna-system-architect", "scripts", "system_architect_designer.py"))
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    return module.DNASPECSystemArchitect()
            elif dnaspec_skill_name == "dnaspec-task-decomposer":
                import importlib.util
                spec = importlib.util.spec_from_file_location("task_decomposer", 
                    os.path.join(os.path.dirname(__file__), "..", "..", "..", "spec-kit", "skills", "dna-task-decomposer", "scripts", "task_decomposer.py"))
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    return module.TaskDecomposer()
        except (ImportError, AttributeError, FileNotFoundError):
            pass
        
        return None
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """获取工作流状态"""
        if workflow_id not in self.active_workflows:
            return {"error": "Workflow not found"}
        
        workflow = self.active_workflows[workflow_id]
        
        return {
            "workflow_id": workflow_id,
            "name": workflow.name,
            "status": workflow.status.value,
            "mode": workflow.mode.value,
            "task_count": len(workflow.tasks),
            "completed_tasks": len([t for t in workflow.tasks if t.status == TaskStatus.COMPLETED]),
            "failed_tasks": len([t for t in workflow.tasks if t.status == TaskStatus.FAILED]),
            "created_at": workflow.created_at.isoformat(),
            "completed_at": workflow.completed_at.isoformat() if workflow.completed_at else None
        }
    
    def get_workflow(self, workflow_id: str) -> Optional[CoordinationWorkflow]:
        """获取工作流"""
        return self.active_workflows.get(workflow_id)
    
    def create_workflow_from_request(self, skill_request, workflow_id: str) -> CoordinationWorkflow:
        """从单个技能请求创建工作流"""
        tasks = [{
            'skill_name': skill_request.skill_name,
            'input_data': skill_request.params,
            'dependencies': []
        }]
        
        workflow_id = self.create_workflow(
            name=f"single_skill_{workflow_id}",
            tasks=tasks,
            mode=CoordinationMode.SEQUENTIAL
        )
        
        return self.get_workflow(workflow_id)
    
    def create_workflow_from_requests(self, skill_requests, workflow_id: str) -> CoordinationWorkflow:
        """从技能请求列表创建工作流"""
        tasks = []
        for i, request in enumerate(skill_requests):
            tasks.append({
                'skill_name': request.skill_name,
                'input_data': request.params,
                'dependencies': []
            })
        
        workflow_id = self.create_workflow(
            name=f"multi_skill_{workflow_id}",
            tasks=tasks,
            mode=CoordinationMode.SEQUENTIAL
        )
        
        return self.get_workflow(workflow_id)
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """列出所有工作流"""
        return [
            self.get_workflow_status(workflow_id) 
            for workflow_id in self.active_workflows.keys()
        ]
    
    def cleanup_workflow(self, workflow_id: str) -> bool:
        """清理已完成的工作流"""
        if workflow_id in self.active_workflows:
            workflow = self.active_workflows[workflow_id]
            if workflow.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
                del self.active_workflows[workflow_id]
                return True
        return False