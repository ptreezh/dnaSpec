"""
Task Decomposer - Input Validator
验证输入参数的完整性和有效性
"""
import re
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """验证结果"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings
        }


class TaskDecomposerValidator:
    """任务分解器输入验证器"""

    # 常量定义
    MIN_INPUT_LENGTH = 10
    MAX_INPUT_LENGTH = 50000
    MIN_TOKENS = 50
    MAX_TOKENS = 100000

    def validate(self, request: str, context: Dict[str, Any]) -> ValidationResult:
        """
        验证输入请求和上下文

        Args:
            request: 用户的任务描述
            context: 额外的上下文信息

        Returns:
            ValidationResult: 验证结果
        """
        errors = []
        warnings = []

        # 1. 验证request不为空
        if not request or not request.strip():
            errors.append("请求不能为空")
            return ValidationResult(False, errors, warnings)

        # 2. 验证长度
        request_length = len(request)
        if request_length < self.MIN_INPUT_LENGTH:
            errors.append(f"请求太短（{request_length}字符），最小要求{self.MIN_INPUT_LENGTH}字符")
        elif request_length > self.MAX_INPUT_LENGTH:
            errors.append(f"请求太长（{request_length}字符），最大支持{self.MAX_INPUT_LENGTH}字符")
            warnings.append("考虑将大任务分解为多个子任务")

        # 3. 估算token数量
        estimated_tokens = self._estimate_tokens(request)
        if estimated_tokens < self.MIN_TOKENS:
            warnings.append(f"请求内容较少（约{estimated_tokens} tokens），可能信息不足")
        elif estimated_tokens > self.MAX_TOKENS:
            errors.append(f"请求token数过多（约{estimated_tokens} tokens），超过{self.MAX_TOKENS}限制")

        # 4. 检查是否包含任务分解关键词
        if not self._contains_decomposition_keywords(request):
            warnings.append("请求不包含明确的任务分解关键词，可能不是任务分解场景")

        # 5. 检查是否包含具体实现细节
        if self._contains_implementation_details(request):
            warnings.append("请求包含具体实现细节，建议先进行架构设计（使用system-architect技能）")

        # 6. 验证上下文参数
        if context:
            context_errors, context_warnings = self._validate_context(context)
            errors.extend(context_errors)
            warnings.extend(context_warnings)

        return ValidationResult(len(errors) == 0, errors, warnings)

    def _estimate_tokens(self, text: str) -> int:
        """
        估算文本的token数量

        使用启发式方法：英文约4字符/token，中文约1.5字符/token
        """
        # 统计中文字符
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        # 统计英文字符
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        # 其他字符（标点、数字等）
        other_chars = len(text) - chinese_chars - english_chars

        # 估算token数
        chinese_tokens = chinese_chars / 1.5
        english_tokens = english_chars / 4
        other_tokens = other_chars / 4

        return int(chinese_tokens + english_tokens + other_tokens)

    def _contains_decomposition_keywords(self, request: str) -> bool:
        """
        检查是否包含任务分解相关的关键词
        """
        keywords = [
            "分解", "拆分", "decompose", "break down",
            "任务", "task", "步骤", "step",
            "阶段", "phase", "模块", "module",
            "子任务", "subtask", "工作流", "workflow"
        ]

        request_lower = request.lower()
        return any(keyword in request_lower for keyword in keywords)

    def _contains_implementation_details(self, request: str) -> bool:
        """
        检查是否包含具体实现细节（代码、函数名等）
        """
        # 检查是否包含代码块
        if "```" in request or "def " in request or "function " in request:
            return True

        # 检查是否包含具体文件路径
        if re.search(r'\.(py|js|ts|java|go|rs)\b', request):
            return True

        # 检查是否包含具体技术栈细节
        implementation_keywords = [
            "import ", "from ", "require(",
            "class ", "interface ", "struct ",
            "数据库表", "API端点", "路由"
        ]

        return any(keyword in request for keyword in implementation_keywords)

    def _validate_context(self, context: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """
        验证上下文参数
        """
        errors = []
        warnings = []

        # 检查是否有指定的复杂度级别
        if "complexity_level" in context:
            level = context["complexity_level"]
            if level not in ["minimal", "basic", "intermediate", "advanced"]:
                warnings.append(f"未知的复杂度级别：{level}，将使用自动检测")

        # 检查是否有最大任务数限制
        if "max_tasks" in context:
            max_tasks = context["max_tasks"]
            if not isinstance(max_tasks, int) or max_tasks < 1:
                errors.append("max_tasks必须是正整数")
            elif max_tasks > 100:
                warnings.append(f"max_tasks({max_tasks})过大，可能导致性能问题")

        # 检查是否有时间约束
        if "time_limit_hours" in context:
            time_limit = context["time_limit_hours"]
            if not isinstance(time_limit, (int, float)) or time_limit <= 0:
                errors.append("time_limit_hours必须是正数")

        return errors, warnings


# 便捷函数
def validate_input(request: str, context: Dict[str, Any] = None) -> ValidationResult:
    """
    验证任务分解器的输入

    Args:
        request: 用户的任务描述
        context: 额外的上下文信息

    Returns:
        ValidationResult: 验证结果

    Example:
        >>> result = validate_input("设计一个用户认证系统")
        >>> print(result.is_valid)
        True
    """
    validator = TaskDecomposerValidator()
    return validator.validate(request, context or {})


if __name__ == "__main__":
    # 测试用例
    test_cases = [
        ("", {}),  # 空请求
        ("实现登录功能", {}),  # 简单请求
        ("设计一个用户认证系统，包括注册、登录、密码重置等功能，使用JWT认证", {}),
        ("def hello(): pass", {}),  # 代码实现
        ("A" * 60000, {}),  # 超长请求
    ]

    for i, (request, ctx) in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}:")
        print(f"请求: {request[:50]}...")
        result = validate_input(request, ctx)
        print(f"验证结果: {result}")
