"""
任务分解工作区集成 - 集成task-decomposer和workspace
"""
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field

# 添加src到路径
src_dir = Path(__file__).parent.parent.parent.parent / 'src'
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))


@dataclass
class SubTask:
    """子任务"""
    task_id: str
    parent_task_id: str
    name: str
    description: str
    workspace_id: str
    dependencies: List[str] = field(default_factory=list)


@dataclass
class TaskDecompositionResult:
    """任务分解结果"""
    success: bool
    main_task_id: str
    main_task_name: str
    sub_tasks: List[SubTask] = field(default_factory=list)
    workspaces_created: int = 0
    error: Optional[str] = None


class TaskWorkspaceIntegrator:
    """任务工作区集成器"""

    def __init__(self, dnaspec_root: Optional[Path] = None):
        if dnaspec_root is None:
            dnaspec_root = Path(__file__).parent.parent.parent.parent

        self.dnaspec_root = Path(dnaspec_root)
        self.workspaces_root = self.dnaspec_root / 'workspaces' / 'tasks'
        self.workspaces_root.mkdir(parents=True, exist_ok=True)

    def decompose_and_create_workspaces(
        self,
        task_name: str,
        task_description: str,
        max_subtasks: int = 5
    ) -> TaskDecompositionResult:
        """
        分解任务并创建子任务工作区

        流程:
        1. 使用task-decomposer分解任务
        2. 为每个子任务创建独立工作区
        3. 建立任务依赖关系
        4. 生成任务结构图

        Args:
            task_name: 主任务名称
            task_description: 任务描述
            max_subtasks: 最大子任务数量

        Returns:
            TaskDecompositionResult: 分解结果
        """
        print(f"\n{'='*60}")
        print(f"任务分解与工作区创建: {task_name}")
        print(f"{'='*60}")

        try:
            # 步骤1: 分解任务
            print("\n[1/4] 分解任务...")
            main_task_id = self._generate_task_id(task_name)
            sub_tasks = self._decompose_task(
                main_task_id, task_name, task_description, max_subtasks
            )

            print(f"  分解为 {len(sub_tasks)} 个子任务")

            # 步骤2: 创建主任务工作区
            print("\n[2/4] 创建主任务工作区...")
            main_workspace_id = f"{main_task_id}-main"
            main_workspace_path = self._create_task_workspace(
                main_workspace_id, task_name, task_description, is_main=True
            )

            # 步骤3: 为每个子任务创建工作区
            print(f"\n[3/4] 创建子任务工作区...")
            workspaces_created = 0

            for sub_task in sub_tasks:
                workspace_path = self._create_task_workspace(
                    sub_task.workspace_id,
                    sub_task.name,
                    sub_task.description,
                    parent_task_id=main_task_id
                )
                workspaces_created += 1
                print(f"  - {sub_task.name}: {sub_task.workspace_id}")

            # 步骤4: 保存任务结构
            print(f"\n[4/4] 保存任务结构...")
            self._save_task_structure(
                main_task_id, task_name, sub_tasks, main_workspace_id
            )

            print(f"\n✅ 任务分解与工作区创建完成！")
            print(f"   主任务ID: {main_task_id}")
            print(f"   子任务数: {len(sub_tasks)}")
            print(f"   工作区数: {workspaces_created + 1}")  # +1 for main

            return TaskDecompositionResult(
                success=True,
                main_task_id=main_task_id,
                main_task_name=task_name,
                sub_tasks=sub_tasks,
                workspaces_created=workspaces_created + 1
            )

        except Exception as e:
            print(f"\n❌ 分解失败: {e}")
            import traceback
            traceback.print_exc()

            return TaskDecompositionResult(
                success=False,
                main_task_id="",
                main_task_name=task_name,
                error=str(e)
            )

    def _generate_task_id(self, task_name: str) -> str:
        """生成任务ID"""
        # 简化名称
        simple_name = task_name.lower().replace(' ', '-').replace('_', '-')
        # 移除特殊字符
        simple_name = ''.join(c for c in simple_name if c.isalnum() or c == '-')
        return f"{simple_name}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    def _decompose_task(
        self,
        parent_id: str,
        task_name: str,
        task_description: str,
        max_subtasks: int
    ) -> List[SubTask]:
        """分解任务（简化版本）"""
        # 实际应用中会调用task-decomposer技能
        # 这里提供一个简化实现

        # 基于描述中的关键词识别子任务
        subtasks = []

        # 简单分解逻辑
        if '用户' in task_description and '认证' in task_description:
            subtasks.append(SubTask(
                task_id=f"{parent_id}-sub-1",
                parent_task_id=parent_id,
                name="用户注册功能",
                description="实现用户注册功能，包括表单验证、数据存储",
                workspace_id=f"{parent_id}-sub-1"
            ))

            subtasks.append(SubTask(
                task_id=f"{parent_id}-sub-2",
                parent_task_id=parent_id,
                name="用户登录功能",
                description="实现用户登录功能，支持多种认证方式",
                workspace_id=f"{parent_id}-sub-2"
            ))

            subtasks.append(SubTask(
                task_id=f"{parent_id}-sub-3",
                parent_task_id=parent_id,
                name="密码重置功能",
                description="实现密码重置功能，包括邮件验证",
                workspace_id=f"{parent_id}-sub-3",
                dependencies=[f"{parent_id}-sub-1"]
            ))

        else:
            # 通用分解：按阶段分解
            subtasks.append(SubTask(
                task_id=f"{parent_id}-sub-1",
                parent_task_id=parent_id,
                name="需求分析",
                description=f"分析{task_name}的需求",
                workspace_id=f"{parent_id}-sub-1"
            ))

            subtasks.append(SubTask(
                task_id=f"{parent_id}-sub-2",
                parent_task_id=parent_id,
                name="设计阶段",
                description=f"设计{task_name}的架构和接口",
                workspace_id=f"{parent_id}-sub-2",
                dependencies=[f"{parent_id}-sub-1"]
            ))

            subtasks.append(SubTask(
                task_id=f"{parent_id}-sub-3",
                parent_task_id=parent_id,
                name="实现阶段",
                description=f"实现{task_name}的核心功能",
                workspace_id=f"{parent_id}-sub-3",
                dependencies=[f"{parent_id}-sub-2"]
            ))

        return subtasks[:max_subtasks]

    def _create_task_workspace(
        self,
        workspace_id: str,
        task_name: str,
        task_description: str,
        parent_task_id: Optional[str] = None,
        is_main: bool = False
    ) -> Path:
        """创建任务工作区"""
        workspace_path = self.workspaces_root / workspace_id

        # 创建目录结构
        (workspace_path / 'context').mkdir(parents=True, exist_ok=True)
        (workspace_path / 'input').mkdir(parents=True, exist_ok=True)
        (workspace_path / 'output').mkdir(parents=True, exist_ok=True)
        (workspace_path / 'workspace').mkdir(parents=True, exist_ok=True)

        # 创建context.md
        context_file = workspace_path / 'context' / 'context.md'
        context_content = self._generate_task_context(
            workspace_id, task_name, task_description, parent_task_id, is_main
        )

        with open(context_file, 'w', encoding='utf-8') as f:
            f.write(context_content)

        return workspace_path

    def _generate_task_context(
        self,
        workspace_id: str,
        task_name: str,
        task_description: str,
        parent_task_id: Optional[str],
        is_main: bool
    ) -> str:
        """生成任务上下文"""
        task_type = "主任务" if is_main else "子任务"

        content = f"""# {task_name} - 任务上下文

## 任务信息
- **任务ID**: {workspace_id}
- **任务类型**: {task_type}
- **父任务ID**: {parent_task_id if parent_task_id else '无'}

## 任务描述
{task_description}

## 约束条件
- 上下文隔离：每个子任务有独立上下文
- 依赖管理：按依赖顺序执行
- 质量标准：满足DNASPEC质量要求

## 输入
- [ ] 需求文档
- [ ] 技术规范
- [ ] 设计文档

## 输出
- [ ] 实现代码
- [ ] 测试用例
- [ ] 文档

## 执行历史

---
*此上下文仅用于本任务，与其他任务隔离*
"""

        return content

    def _save_task_structure(
        self,
        main_task_id: str,
        task_name: str,
        sub_tasks: List[SubTask],
        main_workspace_id: str
    ):
        """保存任务结构"""
        structure = {
            'main_task_id': main_task_id,
            'main_task_name': task_name,
            'main_workspace_id': main_workspace_id,
            'created_at': datetime.now().isoformat(),
            'sub_tasks': [
                {
                    'task_id': st.task_id,
                    'name': st.name,
                    'description': st.description,
                    'workspace_id': st.workspace_id,
                    'dependencies': st.dependencies
                }
                for st in sub_tasks
            ],
            'dependency_graph': self._build_dependency_graph(sub_tasks)
        }

        structure_file = self.workspaces_root / f"{main_task_id}_structure.json"
        with open(structure_file, 'w', encoding='utf-8') as f:
            json.dump(structure, f, indent=2, ensure_ascii=False)

        print(f"  保存结构: {structure_file}")

    def _build_dependency_graph(self, sub_tasks: List[SubTask]) -> Dict:
        """构建依赖关系图"""
        graph = {}

        for sub_task in sub_tasks:
            graph[sub_task.task_id] = {
                'depends_on': sub_task.dependencies,
                'dependents': []
            }

        # 填充dependents
        for sub_task in sub_tasks:
            for dep in sub_task.dependencies:
                if dep in graph:
                    graph[dep]['dependents'].append(sub_task.task_id)

        return graph

    def list_task_workspaces(self) -> List[Dict]:
        """列出所有任务工作区"""
        workspaces = []

        if not self.workspaces_root.exists():
            return workspaces

        # 读取所有结构文件
        for structure_file in self.workspaces_root.glob('*_structure.json'):
            with open(structure_file, 'r', encoding='utf-8') as f:
                structure = json.load(f)
                workspaces.append(structure)

        return workspaces


def demo_task_workspace():
    """演示任务工作区集成"""
    print("="*60)
    print("任务工作区集成演示")
    print("="*60)

    integrator = TaskWorkspaceIntegrator()

    # 分解一个复杂任务
    result = integrator.decompose_and_create_workspaces(
        task_name="用户认证系统",
        task_description="""
        设计并实现一个完整的用户认证系统，包括：
        - 用户注册功能
        - 用户登录功能（支持多种方式）
        - 密码重置功能
        - 会话管理
        - 安全性要求高
        """,
        max_subtasks=5
    )

    if result.success:
        print(f"\n✅ 任务分解成功!")
        print(f"   主任务: {result.main_task_name}")
        print(f"   子任务数: {len(result.sub_tasks)}")
        print(f"   工作区数: {result.workspaces_created}")

        print(f"\n子任务列表:")
        for i, sub_task in enumerate(result.sub_tasks, 1):
            deps = f" (依赖: {', '.join(sub_task.dependencies)})" if sub_task.dependencies else ""
            print(f"  {i}. {sub_task.name}{deps}")
    else:
        print(f"\n❌ 分解失败: {result.error}")

    return result


if __name__ == '__main__':
    demo_task_workspace()
