"""
Task Decomposer - Dependency Analyzer
分析任务间的依赖关系、检测循环依赖、计算关键路径
"""
from typing import Dict, Any, List, Set, Tuple
from dataclasses import dataclass
from collections import deque, defaultdict


@dataclass
class TaskNode:
    """任务节点"""
    id: str
    name: str
    description: str
    dependencies: List[str]  # 依赖的任务ID列表
    estimated_hours: float = 0.0

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, TaskNode):
            return False
        return self.id == other.id


@dataclass
class DependencyAnalysis:
    """依赖分析结果"""
    has_circular_deps: bool
    circular_paths: List[List[str]]  # 循环依赖路径

    max_depth: int  # 最大依赖深度
    total_tasks: int  # 总任务数
    parallelizable_tasks: int  # 可并行执行的任务数

    critical_path: List[str]  # 关键路径（任务ID列表）
    critical_path_duration: float  # 关键路径总时长

    topological_order: List[str]  # 拓扑排序结果

    levels: Dict[int, List[str]]  # 分层结果 {level: [task_ids]}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "circular_dependencies": {
                "has_cycles": self.has_circular_deps,
                "cycles": self.circular_paths
            },
            "depth_analysis": {
                "max_depth": self.max_depth,
                "levels": {k: v for k, v in self.levels.items()}
            },
            "parallelization": {
                "total_tasks": self.total_tasks,
                "parallelizable_count": self.parallelizable_tasks,
                "parallelizable_ratio": self.parallelizable_tasks / self.total_tasks if self.total_tasks > 0 else 0
            },
            "critical_path": {
                "tasks": self.critical_path,
                "duration_hours": self.critical_path_duration
            },
            "topological_order": self.topological_order
        }


class DependencyAnalyzer:
    """依赖关系分析器"""

    def analyze(self, tasks: List[TaskNode]) -> DependencyAnalysis:
        """
        分析任务依赖关系

        Args:
            tasks: 任务列表

        Returns:
            DependencyAnalysis: 分析结果
        """
        # 构建任务字典
        task_dict = {task.id: task for task in tasks}

        # 1. 检测循环依赖
        has_cycles, cycles = self._detect_circular_dependencies(tasks)

        # 2. 计算最大深度
        max_depth, levels = self._calculate_depths(tasks, task_dict)

        # 3. 计算可并行任务数
        parallelizable_count = self._count_parallelizable_tasks(tasks, levels)

        # 4. 计算关键路径
        critical_path, path_duration = self._calculate_critical_path(tasks, task_dict)

        # 5. 拓扑排序
        topological_order = self._topological_sort(tasks)

        return DependencyAnalysis(
            has_circular_deps=has_cycles,
            circular_paths=cycles,
            max_depth=max_depth,
            total_tasks=len(tasks),
            parallelizable_tasks=parallelizable_count,
            critical_path=critical_path,
            critical_path_duration=path_duration,
            topological_order=topological_order,
            levels=levels
        )

    def _detect_circular_dependencies(self, tasks: List[TaskNode]) -> Tuple[bool, List[List[str]]]:
        """
        使用深度优先搜索检测循环依赖

        Returns:
            (has_cycles, circular_paths)
        """
        # 构建邻接表
        graph = {task.id: task.dependencies for task in tasks}

        # DFS状态：0=未访问，1=访问中，2=已完成
        state = {task.id: 0 for task in tasks}
        cycles = []

        def dfs(node_id: str, path: List[str]) -> bool:
            state[node_id] = 1  # 标记为访问中
            path.append(node_id)

            for dep_id in graph.get(node_id, []):
                if dep_id not in state:
                    continue  # 依赖的任务不在列表中，跳过

                if state[dep_id] == 1:
                    # 发现环
                    cycle_start = path.index(dep_id)
                    cycle = path[cycle_start:] + [dep_id]
                    cycles.append(cycle)
                elif state[dep_id] == 0:
                    dfs(dep_id, path)

            path.pop()
            state[node_id] = 2  # 标记为已完成
            return False

        for task in tasks:
            if state[task.id] == 0:
                dfs(task.id, [])

        return len(cycles) > 0, cycles

    def _calculate_depths(self, tasks: List[TaskNode],
                         task_dict: Dict[str, TaskNode]) -> Tuple[int, Dict[int, List[str]]]:
        """
        计算任务的最大深度和分层

        Returns:
            (max_depth, levels) where levels is {level: [task_ids]}
        """
        # 计算每个任务的深度（最长依赖链）
        def get_depth(task_id: str, memo: Dict[str, int]) -> int:
            if task_id in memo:
                return memo[task_id]

            task = task_dict.get(task_id)
            if not task or not task.dependencies:
                memo[task_id] = 0
                return 0

            max_dep_depth = 0
            for dep_id in task.dependencies:
                if dep_id in task_dict:
                    dep_depth = get_depth(dep_id, memo)
                    max_dep_depth = max(max_dep_depth, dep_depth)

            memo[task_id] = max_dep_depth + 1
            return memo[task_id]

        # 计算所有任务的深度
        depth_memo = {}
        for task in tasks:
            get_depth(task.id, depth_memo)

        # 按深度分组
        levels = defaultdict(list)
        max_depth = 0
        for task_id, depth in depth_memo.items():
            levels[depth].append(task_id)
            max_depth = max(max_depth, depth)

        return max_depth, dict(levels)

    def _count_parallelizable_tasks(self, tasks: List[TaskNode],
                                   levels: Dict[int, List[str]]) -> int:
        """
        计算可并行执行的任务数

        策略：同一层的任务可以并行执行（假设无跨层依赖）
        """
        parallelizable = 0

        for level_tasks in levels.values():
            # 同层的任务数如果>1，说明可以并行
            if len(level_tasks) > 1:
                parallelizable += len(level_tasks)
            elif len(level_tasks) == 1:
                # 单个任务也算可并行（和其他层的任务并行）
                parallelizable += 1

        return min(parallelizable, len(tasks))  # 不超过总任务数

    def _calculate_critical_path(self, tasks: List[TaskNode],
                                task_dict: Dict[str, TaskNode]) -> Tuple[List[str], float]:
        """
        使用动态规划计算关键路径（最长路径）

        Returns:
            (critical_path_ids, total_duration)
        """
        # 构建邻接表和计算入度
        graph = {task.id: task.dependencies for task in tasks}
        in_degree = {task.id: 0 for task in tasks}
        for task in tasks:
            for dep_id in task.dependencies:
                if dep_id in in_degree:
                    in_degree[task.id] += 1

        # 拓扑排序
        queue = deque([task_id for task_id, degree in in_degree.items() if degree == 0])
        topo_order = []
        while queue:
            node_id = queue.popleft()
            topo_order.append(node_id)
            for task in tasks:
                if node_id in task.dependencies:
                    in_degree[task.id] -= 1
                    if in_degree[task.id] == 0:
                        queue.append(task.id)

        # 动态规划计算最长路径
        dist = {task.id: 0 for task in tasks}
        prev = {task.id: None for task in tasks}

        for task_id in topo_order:
            task = task_dict.get(task_id)
            if not task:
                continue

            # 尝试从所有依赖更新距离
            for dep_id in task.dependencies:
                if dep_id in dist and dep_id in task_dict:
                    dep_duration = task_dict[dep_id].estimated_hours
                    if dist[dep_id] + dep_duration > dist[task_id]:
                        dist[task_id] = dist[dep_id] + dep_duration
                        prev[task_id] = dep_id

            # 加上自己的时间
            dist[task_id] += task.estimated_hours

        # 找到最长路径的终点
        end_task_id = max(dist.keys(), key=lambda k: dist[k])

        # 回溯构建路径
        path = []
        current = end_task_id
        while current is not None:
            path.append(current)
            current = prev.get(current)

        path.reverse()
        return path, dist[end_task_id]

    def _topological_sort(self, tasks: List[TaskNode]) -> List[str]:
        """
        拓扑排序

        Returns:
            排序后的任务ID列表
        """
        # 构建邻接表和入度
        graph = {task.id: [] for task in tasks}
        in_degree = {task.id: 0 for task in tasks}

        for task in tasks:
            for dep_id in task.dependencies:
                if dep_id in graph:
                    graph[dep_id].append(task.id)
                    in_degree[task.id] += 1

        # Kahn算法
        queue = deque([task_id for task_id, degree in in_degree.items() if degree == 0])
        result = []

        while queue:
            node_id = queue.popleft()
            result.append(node_id)

            for neighbor_id in graph[node_id]:
                in_degree[neighbor_id] -= 1
                if in_degree[neighbor_id] == 0:
                    queue.append(neighbor_id)

        # 检查是否所有节点都被访问（检测环）
        if len(result) != len(tasks):
            # 有环，返回部分结果
            pass

        return result


# 便捷函数
def analyze_dependencies(tasks: List[Dict[str, Any]]) -> DependencyAnalysis:
    """
    分析任务依赖关系

    Args:
        tasks: 任务列表，每个任务是字典，包含id, name, dependencies等

    Returns:
        DependencyAnalysis: 分析结果

    Example:
        >>> tasks = [
        ...     {"id": "001", "name": "Task1", "dependencies": []},
        ...     {"id": "002", "name": "Task2", "dependencies": ["001"]},
        ...     {"id": "003", "name": "Task3", "dependencies": ["001", "002"]}
        ... ]
        >>> analysis = analyze_dependencies(tasks)
        >>> print(f"有环: {analysis.has_circular_deps}")
        >>> print(f"最大深度: {analysis.max_depth}")
        >>> print(f"关键路径: {analysis.critical_path}")
    """
    # 转换为TaskNode对象
    task_nodes = []
    for task in tasks:
        task_nodes.append(TaskNode(
            id=task["id"],
            name=task.get("name", ""),
            description=task.get("description", ""),
            dependencies=task.get("dependencies", []),
            estimated_hours=task.get("estimated_hours", 4.0)
        ))

    analyzer = DependencyAnalyzer()
    return analyzer.analyze(task_nodes)


if __name__ == "__main__":
    # 测试用例
    print("测试用例1：无依赖的并行任务")
    tasks1 = [
        {"id": "001", "name": "Task1", "dependencies": [], "estimated_hours": 2},
        {"id": "002", "name": "Task2", "dependencies": [], "estimated_hours": 3},
        {"id": "003", "name": "Task3", "dependencies": [], "estimated_hours": 1},
    ]
    analysis1 = analyze_dependencies(tasks1)
    print(f"分析结果: {analysis1.to_dict()}")

    print("\n测试用例2：有序依赖的任务")
    tasks2 = [
        {"id": "001", "name": "Task1", "dependencies": [], "estimated_hours": 2},
        {"id": "002", "name": "Task2", "dependencies": ["001"], "estimated_hours": 3},
        {"id": "003", "name": "Task3", "dependencies": ["002"], "estimated_hours": 1},
    ]
    analysis2 = analyze_dependencies(tasks2)
    print(f"分析结果: {analysis2.to_dict()}")

    print("\n测试用例3：有循环依赖的任务")
    tasks3 = [
        {"id": "001", "name": "Task1", "dependencies": ["003"], "estimated_hours": 2},
        {"id": "002", "name": "Task2", "dependencies": ["001"], "estimated_hours": 3},
        {"id": "003", "name": "Task3", "dependencies": ["002"], "estimated_hours": 1},
    ]
    analysis3 = analyze_dependencies(tasks3)
    print(f"分析结果: {analysis3.to_dict()}")
