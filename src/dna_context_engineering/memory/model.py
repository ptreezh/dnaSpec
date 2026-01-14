"""
智能体记忆系统 - 可选的、非侵入式记忆功能
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
from pathlib import Path
import json


class MemoryType(Enum):
    """记忆类型"""
    SHORT_TERM = "short_term"  # 短期记忆（当前会话）
    LONG_TERM = "long_term"    # 长期记忆（持久化）
    WORKING = "working"        # 工作记忆（临时信息）


class MemoryImportance(Enum):
    """记忆重要性"""
    CRITICAL = "critical"  # 关键（必须保留）
    HIGH = "high"         # 高（优先保留）
    MEDIUM = "medium"     # 中（常规保留）
    LOW = "low"          # 低（可清理）


@dataclass
class MemoryItem:
    """记忆项"""
    memory_id: str
    agent_id: str
    memory_type: MemoryType
    content: str
    importance: MemoryImportance
    created_at: datetime = field(default_factory=datetime.now)
    accessed_at: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'memory_id': self.memory_id,
            'agent_id': self.agent_id,
            'memory_type': self.memory_type.value,
            'content': self.content,
            'importance': self.importance.value,
            'created_at': self.created_at.isoformat(),
            'accessed_at': self.accessed_at.isoformat(),
            'access_count': self.access_count,
            'tags': self.tags,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'MemoryItem':
        """从字典创建"""
        return cls(
            memory_id=data['memory_id'],
            agent_id=data['agent_id'],
            memory_type=MemoryType(data['memory_type']),
            content=data['content'],
            importance=MemoryImportance(data['importance']),
            created_at=datetime.fromisoformat(data['created_at']),
            accessed_at=datetime.fromisoformat(data['accessed_at']),
            access_count=data['access_count'],
            tags=data.get('tags', []),
            metadata=data.get('metadata', {})
        )


@dataclass
class MemoryStats:
    """记忆统计"""
    total_memories: int = 0
    short_term_count: int = 0
    long_term_count: int = 0
    total_size: int = 0  # 字节
    oldest_memory: Optional[datetime] = None
    newest_memory: Optional[datetime] = None


@dataclass
class MemoryConfig:
    """记忆配置"""
    enabled: bool = False  # 是否启用记忆（默认关闭）
    max_short_term: int = 50  # 短期记忆最大数量
    max_long_term: int = 200  # 长期记忆最大数量
    auto_cleanup: bool = True  # 自动清理低价值记忆
    persistence_enabled: bool = True  # 是否持久化
    storage_path: Optional[Path] = None  # 存储路径


class MemoryModel:
    """记忆数据模型"""

    @staticmethod
    def generate_memory_id(agent_id: str) -> str:
        """生成记忆ID"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        return f"mem-{agent_id}-{timestamp}-{unique_id}"

    @staticmethod
    def assess_importance(content: str, context: Optional[Dict] = None) -> MemoryImportance:
        """评估记忆重要性"""
        # 简单的重要性评估逻辑
        content_lower = content.lower()

        # 关键词检测
        critical_keywords = ['critical', 'critical', 'error', 'bug', 'fail']
        high_keywords = ['重要', 'important', 'fix', '修复', '安全问题']
        low_keywords = ['临时', 'temp', '调试', 'debug', 'test']

        if any(kw in content_lower for kw in critical_keywords):
            return MemoryImportance.CRITICAL
        elif any(kw in content_lower for kw in high_keywords):
            return MemoryImportance.HIGH
        elif any(kw in content_lower for kw in low_keywords):
            return MemoryImportance.LOW
        else:
            return MemoryImportance.MEDIUM

    @staticmethod
    def extract_tags(content: str) -> List[str]:
        """从内容提取标签"""
        tags = []

        # 简单的标签提取
        if 'error' in content.lower() or '错误' in content:
            tags.append('error')
        if 'fix' in content.lower() or '修复' in content:
            tags.append('fix')
        if 'feature' in content.lower() or '功能' in content:
            tags.append('feature')
        if 'bug' in content.lower():
            tags.append('bug')

        return tags

    @staticmethod
    def calculate_decay_score(memory: MemoryItem) -> float:
        """计算记忆衰减分数（用于清理决策）

        分数越高，越应该保留

        考虑因素：
        - 重要性（40%）
        - 访问频率（30%）
        - 时间新近（20%）
        - 标签相关性（10%）
        """
        importance_score = {
            MemoryImportance.CRITICAL: 1.0,
            MemoryImportance.HIGH: 0.8,
            MemoryImportance.MEDIUM: 0.5,
            MemoryImportance.LOW: 0.2
        }[memory.importance]

        # 访问频率得分（限制在0-1）
        access_score = min(memory.access_count / 10.0, 1.0)

        # 时间新近得分（越新越好）
        days_old = (datetime.now() - memory.created_at).days
        recency_score = max(0.0, 1.0 - days_old / 30.0)  # 30天以上衰减为0

        # 综合得分
        decay_score = (
            importance_score * 0.4 +
            access_score * 0.3 +
            recency_score * 0.2 +
            0.1  # 基础分
        )

        return decay_score
