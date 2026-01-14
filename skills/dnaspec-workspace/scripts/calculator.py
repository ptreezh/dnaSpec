from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class WorkspaceMetrics:
    token_count: int
    complexity_score: float
    has_create_request: bool
    has_cleanup_request: bool
    has_status_request: bool
    has_isolation_request: bool
    operation_types: List[str]
    recommended_level: str
    recommendations: List[str]

class WorkspaceCalculator:
    def calculate(self, request: str, context: Optional[Dict] = None) -> WorkspaceMetrics:
        token_count = int(len(request) / 2.5)
        complexity = min(len(request) / 1000, 1.0)

        # 检测操作类型
        keywords = {
            'create': ['创建', 'create', '新建', 'initialize', '初始化'],
            'cleanup': ['清理', 'cleanup', 'clean', '删除', 'delete', '归档', 'archive'],
            'status': ['状态', 'status', '查询', 'query', '查看', 'list'],
            'isolation': ['隔离', 'isolation', '上下文隔离', 'context isolation', '防止污染'],
        }

        operation_types = []
        for op_type, kw_list in keywords.items():
            if any(kw in request.lower() for kw in kw_list):
                operation_types.append(op_type)

        has_create = 'create' in operation_types
        has_cleanup = 'cleanup' in operation_types
        has_status = 'status' in operation_types
        has_isolation = 'isolation' in operation_types

        # 推荐级别
        level = '00'
        recommendations = []

        if complexity < 0.3:
            level = '00'
        elif complexity < 0.6:
            level = '01'
        elif len(operation_types) <= 1:
            level = '01'
        elif len(operation_types) == 2:
            level = '02'
        else:
            level = '03'

        # 智能体相关请求提升级别
        if 'agent' in request.lower() or '智能体' in request:
            if level in ['00', '01']:
                level = '02'

        if len(operation_types) == 0:
            recommendations.append("请明确需要的工作区操作类型（创建/清理/状态查询）")

        return WorkspaceMetrics(
            token_count=token_count,
            complexity_score=complexity,
            has_create_request=has_create,
            has_cleanup_request=has_cleanup,
            has_status_request=has_status,
            has_isolation_request=has_isolation,
            operation_types=operation_types,
            recommended_level=level,
            recommendations=recommendations
        )
