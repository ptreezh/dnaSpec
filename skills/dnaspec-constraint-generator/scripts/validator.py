"""
Constraint Generator Validator
负责验证约束生成请求
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class ValidationSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationIssue:
    severity: ValidationSeverity
    category: str
    message: str
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    is_valid: bool
    issues: List[ValidationIssue]

    def has_errors(self) -> bool:
        return any(
            issue.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL]
            for issue in self.issues
        )


class ConstraintValidator:
    """约束验证器"""

    MIN_REQUEST_LENGTH = 10
    MAX_REQUEST_LENGTH = 10000

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}

    def validate(self, request: str, context: Optional[Dict] = None) -> ValidationResult:
        """验证请求"""
        issues = []

        # 1. 验证不为空
        if not request or not request.strip():
            issues.append(ValidationIssue(
                severity=ValidationSeverity.CRITICAL,
                category="empty_request",
                message="请求不能为空",
                suggestion="请描述需要生成什么约束"
            ))
            return ValidationResult(is_valid=False, issues=issues)

        # 2. 验证长度
        request_len = len(request)
        if request_len < self.MIN_REQUEST_LENGTH:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                category="request_too_short",
                message=f"请求太短（{request_len}字符），需要至少{self.MIN_REQUEST_LENGTH}字符"
            ))

        # 3. 验证是否与约束相关
        constraint_keywords = [
            '约束', 'constraint', '限制', 'limit', '要求', 'requirement',
            '性能', 'performance', '安全', 'security', '可用性', 'availability',
            '规则', 'rule', '规范', 'standard', '标准'
        ]
        if not any(keyword in request.lower() for keyword in constraint_keywords):
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                category="not_constraint_related",
                message="请求可能不涉及约束生成",
                suggestion="明确说明需要什么类型的约束（性能、安全、功能等）"
            ))

        # 4. 验证是否有上下文
        if context:
            context_str = str(context)
            if len(context_str) > 50000:  # 50K字符
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    category="context_too_large",
                    message="上下文信息过多，可能影响约束生成准确性",
                    suggestion="精简上下文，只保留关键信息"
                ))

        is_valid = not any(
            issue.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL]
            for issue in issues
        )

        return ValidationResult(is_valid=is_valid, issues=issues)


if __name__ == "__main__":
    # 测试
    validator = ConstraintValidator()

    test_cases = [
        "生成性能约束",
        "",
        "请帮我设计API的性能约束",
        "API响应时间需要小于100毫秒"
    ]

    for request in test_cases:
        result = validator.validate(request)
        print(f"请求: '{request}'")
        print(f"有效: {result.is_valid}")
        if result.issues:
            for issue in result.issues:
                print(f"  [{issue.severity.value}] {issue.message}")
        print()
