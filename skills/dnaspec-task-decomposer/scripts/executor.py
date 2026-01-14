"""
Task Decomposer - Smart Executor
智能执行器：根据任务复杂度选择合适的提示词层次，协调定量和定性分析
"""
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

# 导入定量脚本
from .validator import validate_input, ValidationResult
from .calculator import calculate_metrics, DecompositionMetrics
from .analyzer import analyze_dependencies, DependencyAnalysis, TaskNode


class TaskDecomposerExecutor:
    """
    任务分解器智能执行器

    职责：
    1. 验证输入（validator）
    2. 计算指标（calculator）
    3. 选择提示词层次
    4. 加载合适的提示词
    5. 调用AI执行定性分析
    6. 合并定量和定性结果
    """

    def __init__(self, prompts_dir: Optional[str] = None):
        """
        初始化执行器

        Args:
            prompts_dir: 提示词目录路径
        """
        if prompts_dir is None:
            # 默认使用技能目录下的prompts文件夹
            current_dir = Path(__file__).parent
            prompts_dir = current_dir.parent / "prompts"

        self.prompts_dir = Path(prompts_dir)

        # 提示词层次映射
        self.prompt_levels = {
            "minimal": "00_context.md",
            "basic": "01_basic.md",
            "intermediate": "02_intermediate.md",
            "advanced": "03_advanced.md"
        }

    def execute(self, request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行任务分解

        流程：
        1. 验证输入
        2. 计算指标
        3. 选择提示词层次
        4. 加载提示词
        5. 调用AI（模拟）
        6. 合并结果

        Args:
            request: 用户的任务描述
            context: 额外的上下文信息

        Returns:
            Dict: 任务分解结果
        """
        context = context or {}
        result = {
            "request": request,
            "success": False,
            "steps": []
        }

        try:
            # 步骤1：验证输入
            result["steps"].append({"step": "validation", "status": "running"})
            validation = self._validate_request(request, context)
            result["validation"] = validation.to_dict()

            if not validation.is_valid:
                result["steps"][-1]["status"] = "failed"
                result["error"] = "输入验证失败"
                return result

            result["steps"][-1]["status"] = "completed"

            # 步骤2：计算定量指标
            result["steps"].append({"step": "calculation", "status": "running"})
            metrics = self._calculate_metrics(request, context)
            result["metrics"] = metrics.to_dict()
            result["steps"][-1]["status"] = "completed"

            # 步骤3：选择提示词层次
            result["steps"].append({"step": "prompt_selection", "status": "running"})
            prompt_level = metrics.recommended_prompt_level
            result["selected_prompt_level"] = prompt_level
            result["steps"][-1]["status"] = "completed"

            # 步骤4：加载提示词
            result["steps"].append({"step": "load_prompt", "status": "running"})
            prompt_content = self._load_prompt(prompt_level)
            if not prompt_content:
                result["steps"][-1]["status"] = "failed"
                result["error"] = f"无法加载提示词文件：{prompt_level}"
                return result
            result["steps"][-1]["status"] = "completed"

            # 步骤5：调用AI执行定性分析
            result["steps"].append({"step": "ai_analysis", "status": "running"})
            qualitative_result = self._call_ai_analysis(request, prompt_content, metrics)
            result["steps"][-1]["status"] = "completed"

            # 步骤6：合并结果
            result["steps"].append({"step": "merge_results", "status": "running"})
            final_result = self._merge_results(
                validation,
                metrics,
                qualitative_result
            )
            result["steps"][-1]["status"] = "completed"

            # 成功
            result["success"] = True
            result["decomposition"] = final_result

            return result

        except Exception as e:
            result["error"] = str(e)
            result["steps"][-1]["status"] = "failed"
            return result

    def _validate_request(self, request: str, context: Dict[str, Any]) -> ValidationResult:
        """验证请求"""
        return validate_input(request, context)

    def _calculate_metrics(self, request: str, context: Dict[str, Any]) -> DecompositionMetrics:
        """计算指标"""
        return calculate_metrics(request, context)

    def _load_prompt(self, level: str) -> Optional[str]:
        """
        加载指定层次的提示词

        Args:
            level: minimal/basic/intermediate/advanced

        Returns:
            提示词内容，失败返回None
        """
        prompt_file = self.prompt_levels.get(level)
        if not prompt_file:
            return None

        prompt_path = self.prompts_dir / prompt_file
        if not prompt_path.exists():
            return None

        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"加载提示词失败：{e}")
            return None

    def _call_ai_analysis(self, request: str, prompt: str,
                         metrics: DecompositionMetrics) -> Dict[str, Any]:
        """
        调用AI执行定性分析

        注意：这是模拟实现，实际应该调用真实的AI模型

        Args:
            request: 用户请求
            prompt: 提示词内容
            metrics: 计算出的指标

        Returns:
            AI分析结果
        """
        # 实际实现中，这里应该调用AI API
        # 例如：response = openai.ChatCompletion.create(...)

        # 模拟AI响应
        # 根据request生成模拟的任务分解结果
        mock_decomposition = self._generate_mock_decomposition(request, metrics)

        return {
            "prompt_level": metrics.recommended_prompt_level,
            "prompt_tokens": len(prompt.split()),
            "analysis": mock_decomposition,
            "confidence": 0.85
        }

    def _generate_mock_decomposition(self, request: str,
                                   metrics: DecompositionMetrics) -> Dict[str, Any]:
        """
        生成模拟的任务分解结果

        实际实现中，这个步骤应该由AI完成
        """
        # 提取关键信息
        task_count = metrics.estimated_tasks

        # 生成模拟任务
        tasks = []
        for i in range(task_count):
            task_id = f"{i+1:03d}"
            tasks.append({
                "id": task_id,
                "name": f"Task {i+1}",
                "description": f"任务{i+1}的描述",
                "type": "atomic",
                "workspace": f"task-{task_id}-task-{i+1}/",
                "context": {
                    "input": ["需求文档.md"],
                    "output": ["设计文档.md"]
                },
                "estimated_hours": metrics.estimated_hours / task_count,
                "dependencies": []
            })

        return {
            "root_task": {
                "id": "000",
                "name": "主任务",
                "type": "compound"
            },
            "tasks": tasks,
            "execution_plan": {
                "total_tasks": task_count,
                "estimated_total_hours": metrics.estimated_hours,
                "parallelizable_tasks": int(task_count * metrics.parallelizable_ratio)
            }
        }

    def _merge_results(self, validation: ValidationResult,
                      metrics: DecompositionMetrics,
                      qualitative: Dict[str, Any]) -> Dict[str, Any]:
        """
        合并定量和定性结果

        Args:
            validation: 验证结果
            metrics: 定量指标
            qualitative: 定性分析结果

        Returns:
            合并后的结果
        """
        decomposition = qualitative.get("analysis", {})

        # 添加定量指标到分解结果
        decomposition["quantitative_metrics"] = {
            "complexity_score": metrics.complexity_score,
            "estimated_tokens": metrics.estimated_token_count,
            "context_per_task": metrics.context_per_task,
            "risk_level": metrics.risk_level,
            "risk_factors": metrics.risk_factors
        }

        # 如果有任务列表，分析依赖关系
        if "tasks" in decomposition:
            tasks = decomposition["tasks"]
            # 转换为TaskNode
            task_nodes = []
            for task in tasks:
                task_nodes.append(TaskNode(
                    id=task["id"],
                    name=task.get("name", ""),
                    description=task.get("description", ""),
                    dependencies=task.get("dependencies", []),
                    estimated_hours=task.get("estimated_hours", 4.0)
                ))

            # 分析依赖
            dep_analysis = analyze_dependencies([
                {
                    "id": t.id,
                    "name": t.name,
                    "dependencies": t.dependencies,
                    "estimated_hours": t.estimated_hours
                }
                for t in task_nodes
            ])

            decomposition["dependency_analysis"] = dep_analysis.to_dict()

        return decomposition


# 便捷函数
def decompose_task(request: str, context: Dict[str, Any] = None,
                  prompts_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    执行任务分解

    Args:
        request: 用户的任务描述
        context: 额外的上下文信息
        prompts_dir: 提示词目录路径

    Returns:
        任务分解结果

    Example:
        >>> result = decompose_task("设计一个用户认证系统")
        >>> if result["success"]:
        ...     print(f"分解成 {len(result['decomposition']['tasks'])} 个任务")
        ... else:
        ...     print(f"错误：{result['error']}")
    """
    executor = TaskDecomposerExecutor(prompts_dir)
    return executor.execute(request, context)


if __name__ == "__main__":
    # 测试用例
    test_requests = [
        "实现用户登录功能",
        "设计一个电商平台，包括用户、商品、订单、支付模块",
        "构建微服务架构的系统，支持10万并发"
    ]

    for i, request in enumerate(test_requests, 1):
        print(f"\n{'='*60}")
        print(f"测试用例 {i}")
        print(f"{'='*60}")
        print(f"请求: {request}\n")

        result = decompose_task(request)

        if result["success"]:
            print("✅ 成功")
            print(f"\n步骤:")
            for step in result["steps"]:
                print(f"  - {step['step']}: {step['status']}")

            print(f"\n选择的提示词层次: {result['selected_prompt_level']}")
            print(f"\n指标:")
            metrics = result["metrics"]
            print(f"  - 复杂度: {metrics['complexity']['score']:.2f}")
            print(f"  - 估计任务数: {metrics['complexity']['estimated_tasks']}")
            print(f"  - 估计工时: {metrics['complexity']['estimated_hours']}小时")

            if "decomposition" in result:
                decomp = result["decomposition"]
                if "tasks" in decomp:
                    print(f"\n任务数量: {len(decomp['tasks'])}")
        else:
            print("❌ 失败")
            print(f"错误: {result.get('error', 'Unknown error')}")
            if "validation" in result:
                print(f"验证错误: {result['validation']['errors']}")
