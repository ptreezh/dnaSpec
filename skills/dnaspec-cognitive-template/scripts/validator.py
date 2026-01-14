from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

class ValidationSeverity(Enum):
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    CRITICAL = 'critical'

@dataclass
class ValidationIssue:
    severity: ValidationSeverity
    category: str
    message: str

@dataclass
class ValidationResult:
    is_valid: bool
    issues: List[ValidationIssue]

class CognitiveTemplateValidator:
    MIN_REQUEST_LENGTH = 10

    def validate(self, request: str, context: Optional[Dict] = None) -> ValidationResult:
        issues = []
        if not request or not request.strip():
            issues.append(ValidationIssue(ValidationSeverity.CRITICAL, 'empty', '请求不能为空'))
            return ValidationResult(False, issues)
        if len(request) < self.MIN_REQUEST_LENGTH:
            issues.append(ValidationIssue(ValidationSeverity.ERROR, 'too_short', f'请求太短'))
        is_valid = not any(i.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL] for i in issues)
        return ValidationResult(is_valid, issues)
