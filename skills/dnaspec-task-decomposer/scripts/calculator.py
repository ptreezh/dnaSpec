"""
Task Decomposer - Metrics Calculator
计算任务分解相关的定量指标
"""
import re
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class DecompositionMetrics:
    """任务分解指标"""
    # 复杂度指标
    complexity_score: float  # 0.0-1.0，任务复杂度
    estimated_tasks: int  # 估计的任务数量
    estimated_hours: float  # 估计的总工时

    # 依赖关系指标
    max_depth: int  # 最大任务层级深度
    parallelizable_ratio: float  # 可并行任务比例（0.0-1.0）

    # 上下文指标
    estimated_token_count: int  # 估计的token数量
    context_per_task: int  # 每个任务的平均上下文大小

    # 风险指标
    risk_level: str  # low/medium/high
    risk_factors: List[str]

    # 推荐配置
    recommended_prompt_level: str  # minimal/basic/intermediate/advanced
    requires_decomposition: bool  # 是否需要进一步分解

    def to_dict(self) -> Dict[str, Any]:
        return {
            "complexity": {
                "score": self.complexity_score,
                "estimated_tasks": self.estimated_tasks,
                "estimated_hours": self.estimated_hours
            },
            "dependencies": {
                "max_depth": self.max_depth,
                "parallelizable_ratio": self.parallelizable_ratio
            },
            "context": {
                "estimated_tokens": self.estimated_token_count,
                "context_per_task": self.context_per_task
            },
            "risk": {
                "level": self.risk_level,
                "factors": self.risk_factors
            },
            "recommendations": {
                "prompt_level": self.recommended_prompt_level,
                "requires_decomposition": self.requires_decomposition
            }
        }


class TaskDecomposerCalculator:
    """任务分解指标计算器"""

    def calculate(self, request: str, context: Dict[str, Any] = None) -> DecompositionMetrics:
        """
        计算任务分解的各种指标

        Args:
            request: 用户的任务描述
            context: 额外的上下文信息

        Returns:
            DecompositionMetrics: 计算出的指标
        """
        context = context or {}

        # 1. 计算token数量
        token_count = self._estimate_tokens(request)

        # 2. 计算复杂度分数
        complexity_score = self._calculate_complexity_score(request, token_count)

        # 3. 估计任务数量
        estimated_tasks = self._estimate_task_count(request, complexity_score)

        # 4. 估计总工时
        estimated_hours = self._estimate_total_hours(request, estimated_tasks)

        # 5. 估计最大深度
        max_depth = self._estimate_max_depth(request)

        # 6. 计算可并行比例
        parallelizable_ratio = self._calculate_parallelizable_ratio(request)

        # 7. 计算每个任务的平均上下文
        context_per_task = self._calculate_context_per_task(token_count, estimated_tasks)

        # 8. 评估风险等级
        risk_level, risk_factors = self._assess_risk_level(
            complexity_score, estimated_tasks, token_count
        )

        # 9. 推荐提示词层次
        prompt_level = self._recommend_prompt_level(
            complexity_score, token_count, context
        )

        # 10. 判断是否需要进一步分解
        requires_decomposition = self._check_requires_decomposition(
            complexity_score, estimated_tasks
        )

        return DecompositionMetrics(
            complexity_score=complexity_score,
            estimated_tasks=estimated_tasks,
            estimated_hours=estimated_hours,
            max_depth=max_depth,
            parallelizable_ratio=parallelizable_ratio,
            estimated_token_count=token_count,
            context_per_task=context_per_task,
            risk_level=risk_level,
            risk_factors=risk_factors,
            recommended_prompt_level=prompt_level,
            requires_decomposition=requires_decomposition
        )

    def _estimate_tokens(self, text: str) -> int:
        """估算文本的token数量"""
        # 统计中文字符
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        # 统计英文字符
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        # 其他字符
        other_chars = len(text) - chinese_chars - english_chars

        # 估算
        chinese_tokens = chinese_chars / 1.5
        english_tokens = english_chars / 4
        other_tokens = other_chars / 4

        return int(chinese_tokens + english_tokens + other_tokens)

    def _calculate_complexity_score(self, request: str, token_count: int) -> float:
        """
        计算任务复杂度分数（0.0-1.0）

        考虑因素：
        - 文本长度（token数量）
        - 功能数量（提到多少个功能点）
        - 技术栈数量（提到多少种技术）
        - 集成点数量（外部系统集成）
        - 约束条件数量
        """
        score = 0.0

        # 因素1：token数量（权重0.3）
        if token_count < 100:
            token_score = 0.1
        elif token_count < 500:
            token_score = 0.3
        elif token_count < 2000:
            token_score = 0.5
        elif token_count < 5000:
            token_score = 0.7
        else:
            token_score = 0.9
        score += token_score * 0.3

        # 因素2：功能数量（权重0.3）
        function_patterns = [
            r'(功能|特性|function|feature)[：:]\s*([^\n。；;]+)',
            r'(包括|包含|including)\s*([^。；;\n]+)',
            r'(实现|implement|添加|add)\s*([^\n。；;]+)'
        ]
        function_count = 0
        for pattern in function_patterns:
            matches = re.findall(pattern, request)
            function_count += len(matches)

        if function_count <= 1:
            function_score = 0.1
        elif function_count <= 3:
            function_score = 0.3
        elif function_count <= 5:
            function_score = 0.5
        elif function_count <= 10:
            function_score = 0.7
        else:
            function_score = 0.9
        score += function_score * 0.3

        # 因素3：技术栈数量（权重0.2）
        tech_keywords = [
            'Python', 'Node.js', 'React', 'Vue', 'Angular', 'Java', 'Go',
            'PostgreSQL', 'MongoDB', 'Redis', 'MySQL', 'Kafka',
            'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP'
        ]
        tech_count = sum(1 for keyword in tech_keywords if keyword in request)

        if tech_count == 0:
            tech_score = 0.1
        elif tech_count <= 2:
            tech_score = 0.3
        elif tech_count <= 4:
            tech_score = 0.5
        elif tech_count <= 6:
            tech_score = 0.7
        else:
            tech_score = 0.9
        score += tech_score * 0.2

        # 因素4：约束条件数量（权重0.2）
        constraint_patterns = [
            r'(约束|限制|constraint|requirement)[：:]\s*([^\n。；;]+)',
            r'(必须|需要|must|should|require)\s*([^\n。；;]+)'
        ]
        constraint_count = 0
        for pattern in constraint_patterns:
            matches = re.findall(pattern, request, re.IGNORECASE)
            constraint_count += len(matches)

        if constraint_count == 0:
            constraint_score = 0.1
        elif constraint_count <= 2:
            constraint_score = 0.3
        elif constraint_count <= 4:
            constraint_score = 0.5
        elif constraint_count <= 6:
            constraint_score = 0.7
        else:
            constraint_score = 0.9
        score += constraint_score * 0.2

        return min(1.0, score)

    def _estimate_task_count(self, request: str, complexity_score: float) -> int:
        """
        估计任务数量

        基于复杂度分数和文本中提到的功能点
        """
        # 基础数量：根据复杂度
        if complexity_score < 0.2:
            base_count = 2
        elif complexity_score < 0.4:
            base_count = 3
        elif complexity_score < 0.6:
            base_count = 5
        elif complexity_score < 0.8:
            base_count = 8
        else:
            base_count = 12

        # 根据提到的功能点调整
        function_patterns = [
            r'(功能|特性|模块|module|feature)[：:]\s*([^\n。；;]+)',
            r'(实现|implement|添加|add)\s*([^\n。；;]+)'
        ]
        mentioned_functions = 0
        for pattern in function_patterns:
            matches = re.findall(pattern, request)
            mentioned_functions += len(matches)

        # 取较大值
        return max(base_count, mentioned_functions)

    def _estimate_total_hours(self, request: str, task_count: int) -> float:
        """
        估计总工时（小时）

        基于任务数量和平均复杂度
        """
        # 基础工时：每个任务平均4小时
        base_hours_per_task = 4.0

        # 根据关键词调整
        if any(keyword in request.lower() for keyword in
               ['简单', '快速', 'quick', 'simple', 'easy']):
            base_hours_per_task = 2.0
        elif any(keyword in request.lower() for keyword in
                 ['复杂', '困难', 'complex', 'difficult', 'challenging']):
            base_hours_per_task = 6.0

        total_hours = task_count * base_hours_per_task

        # 考虑集成和测试的额外时间（20%）
        total_hours *= 1.2

        return round(total_hours, 1)

    def _estimate_max_depth(self, request: str) -> int:
        """
        估计任务分解的最大深度

        深度定义：
        - 深度1：所有任务都是平行的原子任务
        - 深度2：有两层任务（主任务 + 子任务）
        - 深度3+：有多层嵌套任务
        """
        # 检查是否明确提到分层结构
        layer_keywords = ['阶段', 'phase', '层级', 'layer', '步骤', 'step']
        layer_count = sum(1 for keyword in layer_keywords if keyword in request)

        if layer_count >= 3:
            return 3
        elif layer_count >= 1:
            return 2

        # 根据复杂度判断
        if len(request) > 1000:
            return 2
        else:
            return 1

    def _calculate_parallelizable_ratio(self, request: str) -> float:
        """
        计算可并行任务的比例

        检查是否有明确的依赖关系描述
        """
        # 检查依赖关键词
        dependency_keywords = [
            '依赖', '前置', '先决', 'depend', 'prerequisite',
            '然后', '之后', 'after', 'then', 'next',
            '顺序', '次序', 'sequence', 'order'
        ]

        dependency_count = sum(1 for keyword in dependency_keywords
                              if keyword in request.lower())

        # 依赖越多，可并行比例越低
        if dependency_count == 0:
            return 0.8  # 大部分可并行
        elif dependency_count <= 2:
            return 0.6
        elif dependency_count <= 4:
            return 0.4
        else:
            return 0.2  # 大部分需要顺序执行

    def _calculate_context_per_task(self, total_tokens: int, task_count: int) -> int:
        """计算每个任务的平均上下文大小"""
        if task_count == 0:
            return 0
        return total_tokens // task_count

    def _assess_risk_level(self, complexity_score: float,
                          task_count: int, token_count: int) -> tuple:
        """
        评估风险等级和风险因素
        """
        risk_factors = []

        # 检查复杂度风险
        if complexity_score > 0.8:
            risk_factors.append("高复杂度：任务非常复杂，需要仔细规划")

        # 检查任务数量风险
        if task_count > 15:
            risk_factors.append("任务数量过多：可能导致管理困难")

        # 检查上下文风险
        if token_count > 10000:
            risk_factors.append("上下文过大：可能导致信息过载")

        # 检查token风险
        if token_count > 30000:
            risk_factors.append("Token数过多：可能超出处理能力")

        # 确定风险等级
        if len(risk_factors) == 0:
            risk_level = "low"
        elif len(risk_factors) <= 2:
            risk_level = "medium"
        else:
            risk_level = "high"

        return risk_level, risk_factors

    def _recommend_prompt_level(self, complexity_score: float,
                                token_count: int,
                                context: Dict[str, Any]) -> str:
        """
        推荐提示词层次

        - minimal: 最简单任务
        - basic: 一般任务
        - intermediate: 中等复杂度
        - advanced: 高复杂度
        """
        # 如果上下文明确指定了层次，使用指定的
        if "complexity_level" in context:
            specified = context["complexity_level"]
            if specified in ["minimal", "basic", "intermediate", "advanced"]:
                return specified

        # 根据复杂度和token数量自动选择
        if complexity_score < 0.3 and token_count < 500:
            return "minimal"
        elif complexity_score < 0.5 and token_count < 2000:
            return "basic"
        elif complexity_score < 0.7 and token_count < 5000:
            return "intermediate"
        else:
            return "advanced"

    def _check_requires_decomposition(self, complexity_score: float,
                                     task_count: int) -> bool:
        """
        判断是否需要进一步分解
        """
        # 如果估计的任务数量超过20，建议进一步分解
        if task_count > 20:
            return True

        # 如果复杂度很高，建议进一步分解
        if complexity_score > 0.8:
            return True

        return False


# 便捷函数
def calculate_metrics(request: str, context: Dict[str, Any] = None) -> DecompositionMetrics:
    """
    计算任务分解指标

    Args:
        request: 用户的任务描述
        context: 额外的上下文信息

    Returns:
        DecompositionMetrics: 计算出的指标

    Example:
        >>> metrics = calculate_metrics("设计一个用户认证系统")
        >>> print(f"复杂度: {metrics.complexity_score}")
        >>> print(f"估计任务数: {metrics.estimated_tasks}")
        >>> print(f"估计工时: {metrics.estimated_hours}小时")
    """
    calculator = TaskDecomposerCalculator()
    return calculator.calculate(request, context)


if __name__ == "__main__":
    # 测试用例
    test_cases = [
        "实现用户登录功能",
        "设计一个电商平台，包括用户、商品、订单、支付模块",
        "构建微服务架构的系统，支持10万并发，使用Node.js、PostgreSQL、Redis、Kafka",
    ]

    for i, request in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}:")
        print(f"请求: {request}")
        metrics = calculate_metrics(request)
        print(f"指标: {metrics.to_dict()}")
