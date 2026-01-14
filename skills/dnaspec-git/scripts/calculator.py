from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class GitMetrics:
    token_count: int
    complexity_score: float
    has_commit_request: bool
    has_branch_request: bool
    has_conflict_request: bool
    has_workflow_request: bool
    operation_types: List[str]
    recommended_level: str
    recommendations: List[str]

class GitCalculator:
    def calculate(self, request: str, context: Optional[Dict] = None) -> GitMetrics:
        token_count = int(len(request) / 2.5)
        complexity = min(len(request) / 1000, 1.0)

        # 检测操作类型
        keywords = {
            'commit': ['提交', 'commit', '提交信息', 'commit message'],
            'branch': ['分支', 'branch', '分支管理', 'branch management'],
            'conflict': ['冲突', 'conflict', '合并冲突', 'merge conflict'],
            'workflow': ['工作流', 'workflow', 'git flow', '分支策略'],
            'tag': ['标签', 'tag', '版本', 'version', 'release'],
        }

        operation_types = []
        for op_type, kw_list in keywords.items():
            if any(kw in request.lower() for kw in kw_list):
                operation_types.append(op_type)

        has_commit = 'commit' in operation_types
        has_branch = 'branch' in operation_types
        has_conflict = 'conflict' in operation_types
        has_workflow = 'workflow' in operation_types

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

        if len(operation_types) == 0:
            recommendations.append("请明确需要的Git操作类型（提交/分支/冲突/工作流）")

        return GitMetrics(
            token_count=token_count,
            complexity_score=complexity,
            has_commit_request=has_commit,
            has_branch_request=has_branch,
            has_conflict_request=has_conflict,
            has_workflow_request=has_workflow,
            operation_types=operation_types,
            recommended_level=level,
            recommendations=recommendations
        )
