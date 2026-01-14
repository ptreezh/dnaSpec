"""
记忆管理器 - 可选的、非侵入式记忆功能
"""
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime

from .model import (
    MemoryItem,
    MemoryType,
    MemoryImportance,
    MemoryConfig,
    MemoryModel
)
from .store import MemoryStore


class MemoryManager:
    """
    记忆管理器

    这是一个可选的组件，用于为智能体添加记忆能力。
    默认禁用，需要显式启用。
    """

    def __init__(self, config: Optional[MemoryConfig] = None):
        """
        初始化记忆管理器

        Args:
            config: 记忆配置（如果为None，使用默认配置且禁用）
        """
        self.config = config or MemoryConfig(enabled=False)

        # 如果未启用，则不初始化存储
        if not self.config.enabled:
            self.store = None
            return

        # 初始化存储
        storage_path = self.config.storage_path
        self.store = MemoryStore(storage_path)

        # 内存缓存（短期记忆）
        self._short_term_cache: Dict[str, List[MemoryItem]] = {}

    @property
    def is_enabled(self) -> bool:
        """检查记忆功能是否启用"""
        return self.config.enabled and self.store is not None

    def add_memory(
        self,
        agent_id: str,
        content: str,
        memory_type: MemoryType = MemoryType.SHORT_TERM,
        importance: Optional[MemoryImportance] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        添加记忆

        Args:
            agent_id: 智能体ID
            content: 记忆内容
            memory_type: 记忆类型
            importance: 重要性（如果为None，自动评估）
            tags: 标签
            metadata: 元数据

        Returns:
            记忆ID（如果未启用则返回None）
        """
        if not self.is_enabled:
            return None

        # 自动评估重要性
        if importance is None:
            importance = MemoryModel.assess_importance(content)

        # 自动提取标签
        if tags is None:
            tags = MemoryModel.extract_tags(content)

        # 创建记忆项
        memory_id = MemoryModel.generate_memory_id(agent_id)
        memory = MemoryItem(
            memory_id=memory_id,
            agent_id=agent_id,
            memory_type=memory_type,
            content=content,
            importance=importance,
            tags=tags,
            metadata=metadata or {}
        )

        # 保存到存储
        self.store.save_memory(memory)

        # 添加到缓存
        if memory_type == MemoryType.SHORT_TERM:
            if agent_id not in self._short_term_cache:
                self._short_term_cache[agent_id] = []
            self._short_term_cache[agent_id].append(memory)

        return memory_id

    def recall_memories(
        self,
        agent_id: str,
        query: str,
        memory_type: Optional[MemoryType] = None,
        limit: int = 10
    ) -> List[MemoryItem]:
        """
        检索记忆

        Args:
            agent_id: 智能体ID
            query: 查询字符串
            memory_type: 记忆类型过滤
            limit: 返回数量限制

        Returns:
            相关记忆列表（如果未启用则返回空列表）
        """
        if not self.is_enabled:
            return []

        # 从存储加载所有记忆
        memories = self.store.load_agent_memories(agent_id, memory_type)

        # 简单的关键词匹配
        query_lower = query.lower()
        relevant_memories = []

        for memory in memories:
            # 检查内容是否包含查询词
            if query_lower in memory.content.lower():
                # 更新访问信息
                memory.accessed_at = datetime.now()
                memory.access_count += 1

                relevant_memories.append(memory)

                if len(relevant_memories) >= limit:
                    break

        return relevant_memories

    def get_recent_memories(
        self,
        agent_id: str,
        count: int = 10
    ) -> List[MemoryItem]:
        """获取最近的记忆"""
        if not self.is_enabled:
            return []

        memories = self.store.load_agent_memories(agent_id)
        return memories[:count]

    def promote_to_long_term(
        self,
        memory_id: str,
        agent_id: str
    ) -> bool:
        """将记忆提升到长期记忆"""
        if not self.is_enabled:
            return False

        memory = self.store.load_memory(memory_id, agent_id)
        if not memory:
            return False

        # 更新类型
        memory.memory_type = MemoryType.LONG_TERM

        # 保存
        self.store.save_memory(memory)

        return True

    def cleanup(self, agent_id: Optional[str] = None):
        """
        清理低价值记忆

        Args:
            agent_id: 智能体ID（如果为None，清理所有智能体）
        """
        if not self.is_enabled:
            return

        if agent_id:
            # 清理单个智能体的记忆
            max_short = self.config.max_short_term
            max_long = self.config.max_long_term

            # 清理短期记忆
            if self.config.auto_cleanup:
                self.store.cleanup_low_value(agent_id, max_short)
        else:
            # 清理所有智能体的记忆
            # （暂不实现，避免误删）
            pass

    def get_stats(self, agent_id: str) -> Optional[Dict]:
        """获取记忆统计"""
        if not self.is_enabled:
            return None

        stats = self.store.get_stats(agent_id)

        return {
            'total_memories': stats.total_memories,
            'short_term_count': stats.short_term_count,
            'long_term_count': stats.long_term_count,
            'total_size': stats.total_size,
            'oldest_memory': stats.oldest_memory.isoformat() if stats.oldest_memory else None,
            'newest_memory': stats.newest_memory.isoformat() if stats.newest_memory else None
        }

    def clear_all(self, agent_id: str) -> int:
        """清除所有记忆（慎用）"""
        if not self.is_enabled:
            return 0

        memories = self.store.load_agent_memories(agent_id)
        deleted_count = 0

        for memory in memories:
            if self.store.delete_memory(memory.memory_id, agent_id):
                deleted_count += 1

        # 清除缓存
        if agent_id in self._short_term_cache:
            del self._short_term_cache[agent_id]

        return deleted_count


class MemoryMixin:
    """
    记忆混入类

    这是一个可选的包装器，用于给智能体添加记忆能力。
    使用方式：通过包装而不是修改现有智能体代码
    """

    def __init__(self, agent_id: str, memory_manager: Optional[MemoryManager] = None):
        """
        初始化记忆混入

        Args:
            agent_id: 智能体ID
            memory_manager: 记忆管理器（如果为None，创建一个新的禁用的管理器）
        """
        self.agent_id = agent_id
        self.memory_manager = memory_manager or MemoryManager()

    def remember(
        self,
        content: str,
        importance: Optional[MemoryImportance] = None,
        as_long_term: bool = False
    ) -> Optional[str]:
        """
        记住信息

        Args:
            content: 要记住的内容
            importance: 重要性
            as_long_term: 是否作为长期记忆

        Returns:
            记忆ID
        """
        if not self.memory_manager.is_enabled:
            return None

        memory_type = MemoryType.LONG_TERM if as_long_term else MemoryType.SHORT_TERM
        return self.memory_manager.add_memory(
            agent_id=self.agent_id,
            content=content,
            memory_type=memory_type,
            importance=importance
        )

    def recall(self, query: str, limit: int = 10) -> List[str]:
        """
        回忆信息

        Args:
            query: 查询字符串
            limit: 返回数量限制

        Returns:
            相关记忆内容列表
        """
        if not self.memory_manager.is_enabled:
            return []

        memories = self.memory_manager.recall_memories(
            agent_id=self.agent_id,
            query=query,
            limit=limit
        )

        return [m.content for m in memories]

    def get_recent(self, count: int = 10) -> List[str]:
        """获取最近的记忆"""
        if not self.memory_manager.is_enabled:
            return []

        memories = self.memory_manager.get_recent_memories(
            agent_id=self.agent_id,
            count=count
        )

        return [m.content for m in memories]
