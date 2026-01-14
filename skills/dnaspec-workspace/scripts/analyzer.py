from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class WorkspaceAnalysis:
    primary_operation: str
    workspace_type: str
    operation_details: List[str]
    recommendations: List[str]

class WorkspaceAnalyzer:
    def analyze(self, request: str, context: Optional[Dict] = None) -> WorkspaceAnalysis:
        request_lower = request.lower()

        # 检测主要操作
        operations = {
            'create': ['创建', 'create', '新建', 'initialize', '初始化'],
            'cleanup': ['清理', 'cleanup', 'clean', '删除', 'delete', '归档', 'archive'],
            'status': ['状态', 'status', '查询', 'query', '查看', 'list'],
            'isolation': ['隔离', 'isolation', '上下文隔离', 'context isolation']
        }

        detected_ops = []
        for op, keywords in operations.items():
            if any(kw in request_lower for kw in keywords):
                detected_ops.append(op)

        primary = detected_ops[0] if detected_ops else 'general'

        # 检测工作区类型
        if 'agent' in request_lower or '智能体' in request:
            workspace_type = 'agent_workspace'
        elif 'subtask' in request_lower or '子任务' in request:
            workspace_type = 'subtask_workspace'
        elif 'task' in request_lower or '任务' in request:
            workspace_type = 'task_workspace'
        else:
            workspace_type = 'general_workspace'

        # 操作详情
        details = []
        if 'create' in detected_ops:
            details.append('工作区创建和初始化')
            details.append('目录结构生成')
            if workspace_type == 'agent_workspace':
                details.append('智能体能力定义')
        if 'cleanup' in detected_ops:
            details.append('临时文件清理')
            details.append('归档管理')
        if 'status' in detected_ops:
            details.append('状态查询')
            details.append('工作区监控')
        if 'isolation' in detected_ops:
            details.append('上下文隔离检查')
            details.append('隔离验证')

        recommendations = []
        if not detected_ops:
            recommendations.append("请明确需要的工作区操作类型")
        if workspace_type == 'agent_workspace':
            recommendations.append("智能体工作区需要额外的 capabilities.yaml 配置")

        return WorkspaceAnalysis(
            primary_operation=primary,
            workspace_type=workspace_type,
            operation_details=details,
            recommendations=recommendations
        )
