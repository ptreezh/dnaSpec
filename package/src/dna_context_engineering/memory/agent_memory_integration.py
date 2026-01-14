"""
智能体记忆增强系统 - 非侵入式集成到 agent-creator

提供可选的记忆功能，不影响基础智能体创建和运行
"""
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
import json
from datetime import datetime

from .model import (
    MemoryConfig,
    MemoryType,
    MemoryImportance
)
from .manager import MemoryManager, MemoryMixin


class AgentWithMemory:
    """
    带记忆的智能体包装器

    非侵入式设计：包装 agent-creator 创建的智能体配置
    """

    def __init__(
        self,
        agent_config: Dict[str, Any],
        enable_memory: bool = False,
        memory_config: Optional[MemoryConfig] = None
    ):
        """
        初始化带记忆的智能体

        Args:
            agent_config: agent-creator 生成的智能体配置
            enable_memory: 是否启用记忆（默认禁用）
            memory_config: 记忆配置（可选）
        """
        self.agent_config = agent_config
        self.agent_id = agent_config.get('id', 'unknown')
        self.agent_role = agent_config.get('role', 'Assistant')

        # 可选的记忆功能
        if enable_memory:
            if memory_config is None:
                memory_config = MemoryConfig(
                    enabled=True,
                    max_short_term=50,
                    max_long_term=200,
                    auto_cleanup=True
                )
            self.memory_manager = MemoryManager(memory_config)
            self.memory = MemoryMixin(self.agent_id, self.memory_manager)
            self._has_memory = True
        else:
            # 创建禁用的记忆管理器（不影响功能）
            self.memory_manager = MemoryManager()
            self.memory = MemoryMixin(self.agent_id, self.memory_manager)
            self._has_memory = False

    @property
    def has_memory(self) -> bool:
        """检查是否启用了记忆"""
        return self._has_memory and self.memory_manager.is_enabled

    def execute_task(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None,
        remember_task: bool = True
    ) -> Dict[str, Any]:
        """
        执行任务（可选地记住）

        Args:
            task: 任务描述
            context: 上下文信息
            remember_task: 是否记住任务（默认True）

        Returns:
            执行结果
        """
        # 调用基础智能体逻辑
        result = self._execute_base_task(task, context)

        # 可选：记住任务和结果
        if self.has_memory and remember_task:
            self._remember_task_execution(task, context, result)

        return result

    def _execute_base_task(
        self,
        task: str,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        基础任务执行逻辑

        Args:
            task: 任务描述
            context: 上下文

        Returns:
            执行结果
        """
        # 模拟智能体执行
        capabilities = self.agent_config.get('capabilities', [])

        # 根据能力选择处理方式
        result = {
            'task': task,
            'agent_id': self.agent_id,
            'agent_role': self.agent_role,
            'capabilities_used': capabilities[:3],  # 使用前3个能力
            'status': 'completed',
            'result': f"任务 '{task}' 已由 {self.agent_role} 完成",
            'timestamp': datetime.now().isoformat()
        }

        if context:
            result['context_applied'] = True

        return result

    def _remember_task_execution(
        self,
        task: str,
        context: Optional[Dict[str, Any]],
        result: Dict[str, Any]
    ):
        """
        记住任务执行过程

        Args:
            task: 任务
            context: 上下文
            result: 结果
        """
        # 记忆任务
        task_memory = f"执行任务: {task}"
        if result.get('status') == 'completed':
            task_memory += " ✅"
        self.memory.remember(
            task_memory,
            importance=MemoryImportance.MEDIUM
        )

        # 记忆重要结果
        if result.get('status') == 'completed':
            result_memory = f"结果: {result.get('result', '无')}"
            self.memory.remember(
                result_memory,
                importance=MemoryImportance.LOW
            )

    def recall_relevant_history(
        self,
        query: str,
        limit: int = 5
    ) -> List[str]:
        """
        回顾相关历史

        Args:
            query: 查询字符串
            limit: 返回数量限制

        Returns:
            相关历史记录
        """
        if not self.has_memory:
            return []

        return self.memory.recall(query, limit=limit)

    def get_agent_info(self) -> Dict[str, Any]:
        """
        获取智能体信息（包含记忆统计）

        Returns:
            智能体信息字典
        """
        info = {
            'agent_config': self.agent_config,
            'has_memory': self.has_memory,
            'memory_enabled': self.memory_manager.is_enabled
        }

        # 如果启用记忆，添加统计
        if self.has_memory:
            stats = self.memory_manager.get_stats(self.agent_id)
            if stats:
                info['memory_stats'] = stats

        return info

    def cleanup_memory(self) -> int:
        """
        清理记忆

        Returns:
            清理的记忆数量
        """
        if not self.has_memory:
            return 0

        self.memory_manager.cleanup(self.agent_id)
        stats_after = self.memory_manager.get_stats(self.agent_id)
        return stats_after.get('total_memories', 0) if stats_after else 0


class AgentMemoryIntegrator:
    """
    智能体记忆集成器

    连接 agent-creator 和记忆系统
    """

    def __init__(self):
        """初始化集成器"""
        self.agents: Dict[str, AgentWithMemory] = {}

    def create_agent_with_memory(
        self,
        agent_config: Dict[str, Any],
        enable_memory: bool = False,
        memory_config: Optional[MemoryConfig] = None
    ) -> AgentWithMemory:
        """
        创建带记忆的智能体

        Args:
            agent_config: agent-creator 生成的配置
            enable_memory: 是否启用记忆
            memory_config: 记忆配置

        Returns:
            AgentWithMemory 实例
        """
        agent = AgentWithMemory(
            agent_config,
            enable_memory=enable_memory,
            memory_config=memory_config
        )

        # 注册智能体
        agent_id = agent.agent_id
        self.agents[agent_id] = agent

        return agent

    def get_agent(self, agent_id: str) -> Optional[AgentWithMemory]:
        """
        获取已注册的智能体

        Args:
            agent_id: 智能体ID

        Returns:
            AgentWithMemory 实例或None
        """
        return self.agents.get(agent_id)

    def list_agents(self) -> List[Dict[str, Any]]:
        """
        列出所有智能体

        Returns:
            智能体信息列表
        """
        agents_info = []
        for agent_id, agent in self.agents.items():
            info = agent.get_agent_info()
            agents_info.append(info)

        return agents_info

    def cleanup_agent_memory(self, agent_id: str) -> bool:
        """
        清理智能体记忆

        Args:
            agent_id: 智能体ID

        Returns:
            是否成功
        """
        agent = self.agents.get(agent_id)
        if agent:
            agent.cleanup_memory()
            return True
        return False

    def export_agent_memory(
        self,
        agent_id: str,
        output_path: Optional[Path] = None
    ) -> Optional[Dict[str, Any]]:
        """
        导出智能体记忆

        Args:
            agent_id: 智能体ID
            output_path: 输出路径（可选）

        Returns:
            记忆数据或None
        """
        agent = self.agents.get(agent_id)
        if not agent or not agent.has_memory:
            return None

        # 获取记忆统计
        stats = agent.memory_manager.get_stats(agent_id)
        if not stats:
            return None

        # 获取最近记忆
        recent_memories = agent.memory.get_recent(20)

        memory_data = {
            'agent_id': agent_id,
            'export_time': datetime.now().isoformat(),
            'stats': stats,
            'recent_memories': recent_memories
        }

        # 如果指定输出路径，保存到文件
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, indent=2, ensure_ascii=False)

        return memory_data


# 便捷函数

def create_agent_from_creator(
    agent_creator_result: Dict[str, Any],
    enable_memory: bool = False,
    memory_config: Optional[MemoryConfig] = None
) -> AgentWithMemory:
    """
    从 agent-creator 结果创建带记忆的智能体

    Args:
        agent_creator_result: agent-creator.execute_skill() 的返回值
        enable_memory: 是否启用记忆
        memory_config: 记忆配置

    Returns:
        AgentWithMemory 实例

    Example:
        >>> from skills.agent_creator.skill import agent_creator_skill
        >>>
        >>> # 使用 agent-creator 创建智能体
        >>> result = agent_creator_skill.execute_skill({
        ...     'agent_description': '数据分析专家'
        ... })
        >>>
        >>> # 创建带记忆的智能体
        >>> agent = create_agent_from_creator(
        ...     result['agent_config'],
        ...     enable_memory=True
        ... )
        >>>
        >>> # 执行任务
        >>> result = agent.execute_task('分析销售数据')
    """
    agent_config = agent_creator_result.get('agent_config')

    if not agent_config:
        raise ValueError("Invalid agent_creator_result: missing agent_config")

    return AgentWithMemory(
        agent_config,
        enable_memory=enable_memory,
        memory_config=memory_config
    )


def run_agent_with_memory_tracking(
    agent: AgentWithMemory,
    tasks: List[str],
    export_memory_path: Optional[Path] = None
) -> List[Dict[str, Any]]:
    """
    运行智能体并追踪记忆

    Args:
        agent: AgentWithMemory 实例
        tasks: 任务列表
        export_memory_path: 记忆导出路径（可选）

    Returns:
        执行结果列表
    """
    results = []

    for task in tasks:
        result = agent.execute_task(task)
        results.append(result)

        # 显示记忆增长
        if agent.has_memory:
            stats = agent.memory_manager.get_stats(agent.agent_id)
            if stats:
                print(f"任务 '{task}' 完成 - 当前记忆数: {stats['total_memories']}")

    # 导出记忆
    if export_memory_path and agent.has_memory:
        integrator = AgentMemoryIntegrator()
        integrator.agents[agent.agent_id] = agent
        integrator.export_agent_memory(agent.agent_id, export_memory_path)
        print(f"记忆已导出到: {export_memory_path}")

    return results
