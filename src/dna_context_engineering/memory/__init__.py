"""
智能体记忆系统 - 可选的、非侵入式记忆功能
"""
from .model import (
    MemoryItem,
    MemoryType,
    MemoryImportance,
    MemoryConfig,
    MemoryStats,
    MemoryModel
)
from .store import MemoryStore
from .manager import MemoryManager, MemoryMixin
from .agent_memory_integration import (
    AgentWithMemory,
    AgentMemoryIntegrator,
    create_agent_from_creator,
    run_agent_with_memory_tracking
)
from .skill_memory_integration import (
    SkillWithMemory,
    TaskDecomposerWithMemory,
    ArchitectWithMemory,
    ModulizerWithMemory,
    ConstraintGeneratorWithMemory,
    SkillsMemoryManager,
    create_task_decomposer_with_memory,
    create_architect_with_memory,
    create_modulizer_with_memory,
    create_constraint_generator_with_memory
)

__all__ = [
    # 基础记忆系统
    'MemoryItem',
    'MemoryType',
    'MemoryImportance',
    'MemoryConfig',
    'MemoryStats',
    'MemoryModel',
    'MemoryStore',
    'MemoryManager',
    'MemoryMixin',

    # 智能体记忆集成
    'AgentWithMemory',
    'AgentMemoryIntegrator',
    'create_agent_from_creator',
    'run_agent_with_memory_tracking',

    # 技能记忆集成
    'SkillWithMemory',
    'TaskDecomposerWithMemory',
    'ArchitectWithMemory',
    'ModulizerWithMemory',
    'ConstraintGeneratorWithMemory',
    'SkillsMemoryManager',
    'create_task_decomposer_with_memory',
    'create_architect_with_memory',
    'create_modulizer_with_memory',
    'create_constraint_generator_with_memory'
]
