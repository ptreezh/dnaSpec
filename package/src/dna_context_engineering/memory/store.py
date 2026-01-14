"""
记忆存储 - 持久化后端
"""
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from .model import MemoryItem, MemoryType, MemoryStats, MemoryConfig


class MemoryStore:
    """记忆存储"""

    def __init__(self, storage_path: Optional[Path] = None):
        if storage_path is None:
            storage_path = Path(__file__).parent.parent.parent.parent.parent / 'memory_storage'

        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # 按agent分组存储
        self.agents_dir = self.storage_path / 'agents'
        self.agents_dir.mkdir(exist_ok=True)

    def save_memory(self, memory: MemoryItem):
        """保存记忆"""
        agent_dir = self.agents_dir / memory.agent_id
        agent_dir.mkdir(exist_ok=True)

        memory_file = agent_dir / f"{memory.memory_id}.json"

        with open(memory_file, 'w', encoding='utf-8') as f:
            json.dump(memory.to_dict(), f, indent=2, ensure_ascii=False)

    def load_memory(self, memory_id: str, agent_id: str) -> Optional[MemoryItem]:
        """加载记忆"""
        memory_file = self.agents_dir / agent_id / f"{memory_id}.json"

        if not memory_file.exists():
            return None

        with open(memory_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return MemoryItem.from_dict(data)

    def load_agent_memories(
        self,
        agent_id: str,
        memory_type: Optional[MemoryType] = None
    ) -> List[MemoryItem]:
        """加载智能体的所有记忆"""
        agent_dir = self.agents_dir / agent_id

        if not agent_dir.exists():
            return []

        memories = []
        for memory_file in agent_dir.glob('*.json'):
            try:
                with open(memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    memory = MemoryItem.from_dict(data)

                    # 过滤类型
                    if memory_type is None or memory.memory_type == memory_type:
                        memories.append(memory)
            except Exception as e:
                # 跳过损坏的记忆文件
                continue

        # 按访问时间排序（最新在前）
        memories.sort(key=lambda m: m.accessed_at, reverse=True)

        return memories

    def delete_memory(self, memory_id: str, agent_id: str) -> bool:
        """删除记忆"""
        memory_file = self.agents_dir / agent_id / f"{memory_id}.json"

        if memory_file.exists():
            memory_file.unlink()
            return True
        return False

    def get_stats(self, agent_id: str) -> MemoryStats:
        """获取记忆统计"""
        memories = self.load_agent_memories(agent_id)

        stats = MemoryStats(
            total_memories=len(memories),
            short_term_count=sum(1 for m in memories if m.memory_type == MemoryType.SHORT_TERM),
            long_term_count=sum(1 for m in memories if m.memory_type == MemoryType.LONG_TERM),
            total_size=sum(len(m.content) for m in memories)
        )

        if memories:
            stats.oldest_memory = min(m.created_at for m in memories)
            stats.newest_memory = max(m.created_at for m in memories)

        return stats

    def cleanup_low_value(self, agent_id: str, keep_count: int = 100):
        """清理低价值记忆"""
        memories = self.load_agent_memories(agent_id)

        if len(memories) <= keep_count:
            return 0  # 无需清理

        # 计算衰减分数
        from .model import MemoryModel
        scored_memories = [
            (m, MemoryModel.calculate_decay_score(m))
            for m in memories
        ]

        # 按分数排序（低分在前）
        scored_memories.sort(key=lambda x: x[1])

        # 删除最低分的记忆
        to_delete = scored_memories[:len(memories) - keep_count]
        deleted_count = 0

        for memory, _ in to_delete:
            if self.delete_memory(memory.memory_id, agent_id):
                deleted_count += 1

        return deleted_count
