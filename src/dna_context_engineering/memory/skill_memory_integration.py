"""
DNASPEC 技能记忆增强框架 - 统一的记忆集成系统

为所有 DNASPEC 技能提供可选的、非侵入式记忆功能
"""
from typing import Dict, Any, List, Optional, Type
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime

from .model import (
    MemoryConfig,
    MemoryType,
    MemoryImportance
)
from .manager import MemoryManager, MemoryMixin


class SkillWithMemory(ABC):
    """
    带记忆的技能基类

    提供统一的记忆集成接口
    """

    def __init__(
        self,
        skill_name: str,
        skill_instance: Any,
        enable_memory: bool = False,
        memory_config: Optional[MemoryConfig] = None
    ):
        """
        初始化带记忆的技能

        Args:
            skill_name: 技能名称
            skill_instance: 技能实例
            enable_memory: 是否启用记忆
            memory_config: 记忆配置
        """
        self.skill_name = skill_name
        self.skill = skill_instance
        self.skill_id = f"{skill_name}_{self._generate_id()}"

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
            self.memory = MemoryMixin(self.skill_id, self.memory_manager)
            self._has_memory = True
        else:
            self.memory_manager = MemoryManager()
            self.memory = MemoryMixin(self.skill_id, self.memory_manager)
            self._has_memory = False

    def _generate_id(self) -> str:
        """生成唯一ID"""
        import uuid
        return str(uuid.uuid4())[:8]

    @property
    def has_memory(self) -> bool:
        """检查是否启用了记忆"""
        return self._has_memory and self.memory_manager.is_enabled

    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行技能（子类实现）

        Args:
            input_data: 输入数据

        Returns:
            执行结果
        """
        pass

    def _remember_execution(
        self,
        input_data: Dict[str, Any],
        result: Dict[str, Any],
        importance: MemoryImportance = MemoryImportance.MEDIUM
    ):
        """
        记住执行过程

        Args:
            input_data: 输入数据
            result: 执行结果
            importance: 重要性
        """
        if not self.has_memory:
            return

        # 记忆输入
        input_summary = self._summarize_input(input_data)
        self.memory.remember(
            f"输入: {input_summary}",
            importance=importance
        )

        # 记忆结果
        result_summary = self._summarize_result(result)
        self.memory.remember(
            f"结果: {result_summary}",
            importance=importance
        )

    @abstractmethod
    def _summarize_input(self, input_data: Dict[str, Any]) -> str:
        """总结输入（子类实现）"""
        pass

    @abstractmethod
    def _summarize_result(self, result: Dict[str, Any]) -> str:
        """总结结果（子类实现）"""
        pass

    def recall_relevant_history(
        self,
        query: str,
        limit: int = 5
    ) -> List[str]:
        """回顾相关历史"""
        if not self.has_memory:
            return []
        return self.memory.recall(query, limit=limit)

    def get_skill_info(self) -> Dict[str, Any]:
        """获取技能信息"""
        info = {
            'skill_name': self.skill_name,
            'skill_id': self.skill_id,
            'has_memory': self.has_memory,
            'memory_enabled': self.memory_manager.is_enabled
        }

        if self.has_memory:
            stats = self.memory_manager.get_stats(self.skill_id)
            if stats:
                info['memory_stats'] = stats

        return info


class TaskDecomposerWithMemory(SkillWithMemory):
    """
    带记忆的任务分解技能
    """

    def __init__(
        self,
        task_decomposer_skill: Any,
        enable_memory: bool = False,
        memory_config: Optional[MemoryConfig] = None
    ):
        super().__init__(
            skill_name="task-decomposer",
            skill_instance=task_decomposer_skill,
            enable_memory=enable_memory,
            memory_config=memory_config
        )

    def execute(
        self,
        input_data: Dict[str, Any],
        remember_decomposition: bool = True
    ) -> Dict[str, Any]:
        """
        执行任务分解

        Args:
            input_data: 包含要分解的任务
            remember_decomposition: 是否记住分解结果

        Returns:
            分解结果
        """
        # 执行基础技能
        result = self.skill.execute_skill(input_data)

        # 可选：记住分解
        if remember_decomposition:
            self._remember_decomposition(input_data, result)

        return result

    def _remember_decomposition(
        self,
        input_data: Dict[str, Any],
        result: Dict[str, Any]
    ):
        """记住任务分解"""
        if not self.has_memory:
            return

        task = input_data.get('input', '')
        method = input_data.get('decomposition_method', 'auto')

        # 记忆任务分解
        self.memory.remember(
            f"分解任务: {task} (方法: {method})",
            importance=MemoryImportance.HIGH
        )

        # 记忆子任务数量
        if 'subtasks' in result:
            subtask_count = len(result['subtasks'])
            self.memory.remember(
                f"生成 {subtask_count} 个子任务",
                importance=MemoryImportance.MEDIUM
            )

        # 记忆复杂度
        if 'complexity_analysis' in result:
            complexity = result['complexity_analysis'].get('overall_complexity', 'unknown')
            self.memory.remember(
                f"任务复杂度: {complexity}",
                importance=MemoryImportance.MEDIUM
            )

    def _summarize_input(self, input_data: Dict[str, Any]) -> str:
        task = input_data.get('input', '')[:50]
        method = input_data.get('decomposition_method', 'auto')
        return f"任务分解: {task}... (方法: {method})"

    def _summarize_result(self, result: Dict[str, Any]) -> str:
        if 'subtasks' in result:
            count = len(result['subtasks'])
            return f"生成 {count} 个子任务"
        return "任务分解完成"

    def recall_similar_decompositions(
        self,
        task_query: str,
        limit: int = 3
    ) -> List[str]:
        """回顾相似的任务分解"""
        return self.recall_relevant_history(task_query, limit)


class ArchitectWithMemory(SkillWithMemory):
    """
    带记忆的架构师技能
    """

    def __init__(
        self,
        architect_skill: Any,
        enable_memory: bool = False,
        memory_config: Optional[MemoryConfig] = None
    ):
        super().__init__(
            skill_name="architect",
            skill_instance=architect_skill,
            enable_memory=enable_memory,
            memory_config=memory_config
        )

    def execute(
        self,
        input_data: Dict[str, Any],
        remember_design: bool = True
    ) -> Dict[str, Any]:
        """
        执行架构设计

        Args:
            input_data: 包含系统需求
            remember_design: 是否记住设计方案

        Returns:
            架构设计结果
        """
        # 执行基础技能
        result = self.skill.execute_skill(input_data)

        # 可选：记住设计
        if remember_design:
            self._remember_architecture_design(input_data, result)

        return result

    def _remember_architecture_design(
        self,
        input_data: Dict[str, Any],
        result: Dict[str, Any]
    ):
        """记住架构设计"""
        if not self.has_memory:
            return

        requirement = input_data.get('input', '')[:50]
        style = result.get('architecture_style', 'unknown')

        # 记忆架构设计
        self.memory.remember(
            f"架构设计: {requirement}... (风格: {style})",
            importance=MemoryImportance.HIGH
        )

        # 记忆组件
        if 'architecture_design' in result:
            components = result['architecture_design'].get('components', [])
            if components:
                component_names = [c.get('name', 'Unknown') for c in components[:5]]
                self.memory.remember(
                    f"核心组件: {', '.join(component_names)}",
                    importance=MemoryImportance.MEDIUM
                )

        # 记忆质量指标
        if 'quality_metrics' in result:
            quality = result['quality_metrics']
            overall_quality = quality.get('overall_quality', 0)
            self.memory.remember(
                f"架构质量评分: {overall_quality:.2f}",
                importance=MemoryImportance.LOW
            )

    def _summarize_input(self, input_data: Dict[str, Any]) -> str:
        requirement = input_data.get('input', '')[:50]
        style = input_data.get('architecture_style', 'auto')
        return f"架构设计: {requirement}... (风格: {style})"

    def _summarize_result(self, result: Dict[str, Any]) -> str:
        style = result.get('architecture_style', 'unknown')
        if 'architecture_design' in result:
            components = result['architecture_design'].get('components', [])
            return f"{style} 架构, {len(components)} 个组件"
        return f"{style} 架构设计"

    def recall_similar_designs(
        self,
        requirement_query: str,
        limit: int = 3
    ) -> List[str]:
        """回顾相似的架构设计"""
        return self.recall_relevant_history(requirement_query, limit)


class ModulizerWithMemory(SkillWithMemory):
    """
    带记忆的模块化技能
    """

    def __init__(
        self,
        modulizer_skill: Any,
        enable_memory: bool = False,
        memory_config: Optional[MemoryConfig] = None
    ):
        super().__init__(
            skill_name="modulizer",
            skill_instance=modulizer_skill,
            enable_memory=enable_memory,
            memory_config=memory_config
        )

    def execute(
        self,
        input_data: Dict[str, Any],
        remember_modularization: bool = True
    ) -> Dict[str, Any]:
        """执行模块化"""
        result = self.skill.execute_skill(input_data)

        if remember_modularization:
            self._remember_modularization(input_data, result)

        return result

    def _remember_modularization(
        self,
        input_data: Dict[str, Any],
        result: Dict[str, Any]
    ):
        """记住模块化"""
        if not self.has_memory:
            return

        codebase = input_data.get('codebase_description', '')[:50]
        self.memory.remember(
            f"模块化: {codebase}...",
            importance=MemoryImportance.HIGH
        )

        if 'modules' in result:
            module_count = len(result['modules'])
            self.memory.remember(
                f"生成 {module_count} 个模块",
                importance=MemoryImportance.MEDIUM
            )

    def _summarize_input(self, input_data: Dict[str, Any]) -> str:
        desc = input_data.get('codebase_description', '')[:50]
        return f"模块化: {desc}..."

    def _summarize_result(self, result: Dict[str, Any]) -> str:
        if 'modules' in result:
            return f"生成 {len(result['modules'])} 个模块"
        return "模块化完成"


class ConstraintGeneratorWithMemory(SkillWithMemory):
    """
    带记忆的约束生成技能
    """

    def __init__(
        self,
        constraint_generator_skill: Any,
        enable_memory: bool = False,
        memory_config: Optional[MemoryConfig] = None
    ):
        super().__init__(
            skill_name="constraint-generator",
            skill_instance=constraint_generator_skill,
            enable_memory=enable_memory,
            memory_config=memory_config
        )

    def execute(
        self,
        input_data: Dict[str, Any],
        remember_constraints: bool = True
    ) -> Dict[str, Any]:
        """执行约束生成"""
        result = self.skill.execute_skill(input_data)

        if remember_constraints:
            self._remember_constraint_generation(input_data, result)

        return result

    def _remember_constraint_generation(
        self,
        input_data: Dict[str, Any],
        result: Dict[str, Any]
    ):
        """记住约束生成"""
        if not self.has_memory:
            return

        requirement = input_data.get('requirement_description', '')[:50]
        self.memory.remember(
            f"约束生成: {requirement}...",
            importance=MemoryImportance.HIGH
        )

        if 'constraints' in result:
            constraint_count = len(result['constraints'])
            self.memory.remember(
                f"生成 {constraint_count} 个约束",
                importance=MemoryImportance.MEDIUM
            )

    def _summarize_input(self, input_data: Dict[str, Any]) -> str:
        desc = input_data.get('requirement_description', '')[:50]
        return f"约束生成: {desc}..."

    def _summarize_result(self, result: Dict[str, Any]) -> str:
        if 'constraints' in result:
            return f"生成 {len(result['constraints'])} 个约束"
        return "约束生成完成"


class SkillsMemoryManager:
    """
    技能记忆管理器

    统一管理多个技能的记忆
    """

    def __init__(self):
        """初始化管理器"""
        self.skills: Dict[str, SkillWithMemory] = {}

    def register_skill(self, skill: SkillWithMemory):
        """
        注册技能

        Args:
            skill: 带记忆的技能实例
        """
        self.skills[skill.skill_id] = skill

    def get_skill(self, skill_id: str) -> Optional[SkillWithMemory]:
        """获取技能"""
        return self.skills.get(skill_id)

    def list_skills(self) -> List[Dict[str, Any]]:
        """列出所有技能"""
        return [skill.get_skill_info() for skill in self.skills.values()]

    def cleanup_all_skills(self) -> Dict[str, int]:
        """
        清理所有技能的记忆

        Returns:
            清理结果字典 {skill_id: remaining_count}
        """
        results = {}
        for skill_id, skill in self.skills.items():
            if skill.has_memory:
                remaining = skill.memory_manager.cleanup(skill.skill_id)
                stats = skill.memory_manager.get_stats(skill.skill_id)
                results[skill_id] = stats['total_memories'] if stats else 0
        return results

    def export_all_memories(
        self,
        output_dir: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        导出所有技能的记忆

        Args:
            output_dir: 输出目录

        Returns:
            导出的记忆数据
        """
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

        all_memories = {}

        for skill_id, skill in self.skills.items():
            if skill.has_memory:
                stats = skill.memory_manager.get_stats(skill.skill_id)
                recent = skill.memory.get_recent(20)

                memory_data = {
                    'skill_name': skill.skill_name,
                    'skill_id': skill_id,
                    'export_time': datetime.now().isoformat(),
                    'stats': stats,
                    'recent_memories': recent
                }

                all_memories[skill_id] = memory_data

                # 保存到文件
                if output_dir:
                    output_file = output_dir / f"{skill.skill_name}_memory.json"
                    import json
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(memory_data, f, indent=2, ensure_ascii=False)

        return all_memories


# 便捷函数

def create_task_decomposer_with_memory(
    skill_instance: Any,
    enable_memory: bool = False
) -> TaskDecomposerWithMemory:
    """
    创建带记忆的任务分解技能

    Example:
        >>> from skills.task_decomposer.skill import task_decomposer_skill
        >>>
        >>> decomposer = create_task_decomposer_with_memory(
        ...     task_decomposer_skill,
        ...     enable_memory=True
        ... )
        >>>
        >>> result = decomposer.execute({
        ...     'input': '实现用户认证系统'
        ... })
    """
    return TaskDecomposerWithMemory(skill_instance, enable_memory=enable_memory)


def create_architect_with_memory(
    skill_instance: Any,
    enable_memory: bool = False
) -> ArchitectWithMemory:
    """
    创建带记忆的架构师技能

    Example:
        >>> from skills.architect.skill import architect_skill
        >>>
        >>> architect = create_architect_with_memory(
        ...     architect_skill,
        ...     enable_memory=True
        ... )
        >>>
        >>> result = architect.execute({
        ...     'input': '设计微服务架构的电商平台'
        ... })
    """
    return ArchitectWithMemory(skill_instance, enable_memory=enable_memory)


def create_modulizer_with_memory(
    skill_instance: Any,
    enable_memory: bool = False
) -> ModulizerWithMemory:
    """创建带记忆的模块化技能"""
    return ModulizerWithMemory(skill_instance, enable_memory=enable_memory)


def create_constraint_generator_with_memory(
    skill_instance: Any,
    enable_memory: bool = False
) -> ConstraintGeneratorWithMemory:
    """创建带记忆的约束生成技能"""
    return ConstraintGeneratorWithMemory(skill_instance, enable_memory=enable_memory)
