"""
Context Fundamentals Validator

负责验证用户请求和上下文的有效性
提供确定性的输入验证逻辑
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class ValidationSeverity(Enum):
    """验证结果严重程度"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationIssue:
    """验证问题"""
    severity: ValidationSeverity
    category: str
    message: str
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    """验证结果"""
    is_valid: bool
    issues: List[ValidationIssue]

    def has_errors(self) -> bool:
        """是否有错误"""
        return any(issue.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL]
                   for issue in self.issues)

    def has_warnings(self) -> bool:
        """是否有警告"""
        return any(issue.severity == ValidationSeverity.WARNING
                   for issue in self.issues)

    def get_summary(self) -> Dict[str, int]:
        """获取问题汇总"""
        summary = {
            "critical": 0,
            "error": 0,
            "warning": 0,
            "info": 0
        }
        for issue in self.issues:
            summary[issue.severity.value] += 1
        return summary


class ContextFundamentalsValidator:
    """上下文基础知识验证器"""

    # 常量定义
    MIN_REQUEST_LENGTH = 10
    MAX_REQUEST_LENGTH = 10000
    MIN_CONTEXT_LENGTH = 0
    MAX_CONTEXT_LENGTH = 1000000  # 1M字符

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化验证器

        Args:
            config: 配置参数，可覆盖默认值
        """
        self.config = config or {}

    def validate(self, request: str, context: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """
        验证请求和上下文

        Args:
            request: 用户请求
            context: 附加上下文信息

        Returns:
            ValidationResult: 验证结果
        """
        issues = []

        # 1. 验证请求不为空
        request_issues = self._validate_request_not_empty(request)
        issues.extend(request_issues)

        # 2. 验证请求长度
        length_issues = self._validate_request_length(request)
        issues.extend(length_issues)

        # 3. 验证请求语言（支持中英文）
        language_issues = self._validate_request_language(request)
        issues.extend(language_issues)

        # 4. 验证请求是否有意义
        meaningful_issues = self._validate_request_meaningful(request)
        issues.extend(meaningful_issues)

        # 5. 验证上下文（如果提供）
        if context:
            context_issues = self._validate_context(context)
            issues.extend(context_issues)

        # 6. 检测常见问题
        common_issues = self._detect_common_problems(request, context)
        issues.extend(common_issues)

        # 判断是否有效
        is_valid = not any(issue.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL]
                          for issue in issues)

        return ValidationResult(is_valid=is_valid, issues=issues)

    def _validate_request_not_empty(self, request: str) -> List[ValidationIssue]:
        """验证请求不为空"""
        issues = []

        if not request or not request.strip():
            issues.append(ValidationIssue(
                severity=ValidationSeverity.CRITICAL,
                category="empty_request",
                message="请求不能为空",
                suggestion="请提供您想了解的上下文相关问题"
            ))

        return issues

    def _validate_request_length(self, request: str) -> List[ValidationIssue]:
        """验证请求长度"""
        issues = []

        request_len = len(request)

        if request_len < self.MIN_REQUEST_LENGTH:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                category="request_too_short",
                message=f"请求太短（{request_len}字符），至少需要{self.MIN_REQUEST_LENGTH}字符",
                suggestion="请提供更多细节，例如您想了解的具体概念或应用场景"
            ))

        elif request_len > self.MAX_REQUEST_LENGTH:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                category="request_too_long",
                message=f"请求很长（{request_len}字符），可能需要分解",
                suggestion="考虑将复杂问题分解为多个简单问题"
            ))

        return issues

    def _validate_request_language(self, request: str) -> List[ValidationIssue]:
        """验证请求语言"""
        issues = []

        # 检查是否包含中文字符
        has_chinese = any('\u4e00' <= char <= '\u9fff' for char in request)
        # 检查是否包含英文字符
        has_english = any(char.isalpha() and ord(char) < 128 for char in request)

        if not has_chinese and not has_english:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                category="unknown_language",
                message="无法识别请求的语言",
                suggestion="请使用中文或英文提问"
            ))

        return issues

    def _validate_request_meaningful(self, request: str) -> List[ValidationIssue]:
        """验证请求是否有意义"""
        issues = []

        # 检查是否只包含标点符号或特殊字符
        meaningful_chars = sum(1 for c in request if c.isalnum() or '\u4e00' <= c <= '\u9fff')
        if meaningful_chars < self.MIN_REQUEST_LENGTH / 2:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                category="meaningful_content_low",
                message="请求中包含的有效字符较少",
                suggestion="请用完整句子描述您的问题"
            ))

        return issues

    def _validate_context(self, context: Dict[str, Any]) -> List[ValidationIssue]:
        """验证上下文"""
        issues = []

        # 验证上下文大小
        context_str = str(context)
        context_len = len(context_str)

        if context_len > self.MAX_CONTEXT_LENGTH:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                category="context_too_large",
                message=f"上下文过大（{context_len}字符）",
                suggestion="考虑精简上下文，只保留相关信息"
            ))

        # 验证上下文结构
        if isinstance(context, dict):
            # 检查是否有已知的上下文失效模式
            if self._has_context_poisoning(context):
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    category="context_poisoning",
                    message="检测到可能的上下文毒化（矛盾信息）",
                    suggestion="检查上下文中是否有矛盾或过时的信息"
                ))

            # 检查是否有上下文分心
            if self._has_context_distraction(context):
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    category="context_distraction",
                    message="检测到可能的上下文分心（无关信息过多）",
                    suggestion="移除不相关的信息，提高上下文相关性"
                ))

        return issues

    def _detect_common_problems(self, request: str, context: Optional[Dict[str, Any]]) -> List[ValidationIssue]:
        """检测常见问题"""
        issues = []

        # 检测是否是多问题合并
        if self._is_multi_question(request):
            issues.append(ValidationIssue(
                severity=ValidationSeverity.INFO,
                category="multi_question",
                message="请求包含多个问题",
                suggestion="考虑分别提问，或使用task-decomposer技能分解"
            ))

        # 检测是否是其他技能的请求
        if self._is_other_skill_request(request):
            issues.append(ValidationIssue(
                severity=ValidationSeverity.INFO,
                category="other_skill",
                message="这可能是其他技能的请求",
                suggestion="请确认是否需要使用专门的技能（如context-analysis、task-decomposer等）"
            ))

        return issues

    def _has_context_poisoning(self, context: Dict[str, Any]) -> bool:
        """检测上下文毒化"""
        # 简化检测：检查是否有重复的键或矛盾的信息
        # 实际实现应该更复杂
        return False

    def _has_context_distraction(self, context: Dict[str, Any]) -> bool:
        """检测上下文分心"""
        # 简化检测：检查上下文是否过大且包含大量无关信息
        # 实际实现应该分析相关性
        context_str = str(context)
        return len(context_str) > 50000  # 超过50K字符可能分心

    def _is_multi_question(self, request: str) -> bool:
        """检测是否是多问题"""
        # 检查是否包含多个问句
        question_markers = ['？', '?', '如何', '怎么', 'what', 'how', 'why']
        question_count = sum(request.count(marker) for marker in question_markers)
        return question_count > 2

    def _is_other_skill_request(self, request: str) -> bool:
        """检测是否是其他技能的请求"""
        # 检查是否明确提到其他技能
        other_skills = [
            'task-decomposer', 'constraint-generator', 'dapi-checker',
            'context-optimization', 'context-analysis', 'agent-creator',
            'architect', 'modulizer', 'system-architect'
        ]
        request_lower = request.lower()
        return any(skill in request_lower for skill in other_skills)


# 便捷函数
def validate_request(request: str, context: Optional[Dict[str, Any]] = None) -> ValidationResult:
    """
    验证请求的便捷函数

    Args:
        request: 用户请求
        context: 附加上下文

    Returns:
        ValidationResult: 验证结果
    """
    validator = ContextFundamentalsValidator()
    return validator.validate(request, context)


if __name__ == "__main__":
    # 测试
    test_cases = [
        ("什么是上下文？", None),
        ("", None),
        ("a?", None),
        ("上下文是什么？如何优化？token限制是什么？", None),
    ]

    for request, context in test_cases:
        print(f"\n测试: {request}")
        result = validate_request(request, context)
        print(f"有效: {result.is_valid}")
        print(f"问题汇总: {result.get_summary()}")
        for issue in result.issues:
            print(f"  [{issue.severity.value.upper()}] {issue.category}: {issue.message}")
            if issue.suggestion:
                print(f"    建议: {issue.suggestion}")
