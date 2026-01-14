"""
System Architect Validator
负责验证系统架构设计请求
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


class SystemArchitectValidator:
    """系统架构验证器"""

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
                suggestion="请描述需要设计的系统架构"
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

        # 3. 验证是否与架构设计相关
        arch_keywords = [
            '架构', 'architecture', '设计', 'design',
            '技术栈', 'tech stack', '模块', 'module',
            '接口', 'interface', '系统', 'system',
            '微服务', 'microservice', '数据库', 'database'
        ]
        if not any(keyword in request.lower() for keyword in arch_keywords):
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                category="not_architecture_related",
                message="请求可能不涉及系统架构设计",
                suggestion="明确说明需要什么类型的架构设计（技术选型、模块划分等）"
            ))

        # 4. 验证是否有上下文
        if context:
            context_str = str(context)
            if len(context_str) > 50000:  # 50K字符
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    category="context_too_large",
                    message="上下文信息过多，可能影响架构设计准确性",
                    suggestion="精简上下文，只保留关键信息"
                ))

        is_valid = not any(
            issue.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL]
            for issue in issues
        )

        return ValidationResult(is_valid=is_valid, issues=issues)
