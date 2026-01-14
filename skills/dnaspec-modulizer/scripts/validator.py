"""
Modulizer Validator
负责验证模块化设计请求
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


class ModulizerValidator:
    """模块化验证器"""

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
                message="请求不能为空"
            ))
            return ValidationResult(is_valid=False, issues=issues)

        # 2. 验证长度
        request_len = len(request)
        if request_len < self.MIN_REQUEST_LENGTH:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                category="request_too_short",
                message=f"请求太短（{request_len}字符）"
            ))

        # 3. 验证是否与模块化相关
        keywords = ['模块', 'module', '重构', 'refactor', '耦合', 'coupling', '接口', 'interface']
        if not any(keyword in request.lower() for keyword in keywords):
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                category="not_modularization_related",
                message="请求可能不涉及模块化设计"
            ))

        is_valid = not any(
            issue.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL]
            for issue in issues
        )

        return ValidationResult(is_valid=is_valid, issues=issues)
