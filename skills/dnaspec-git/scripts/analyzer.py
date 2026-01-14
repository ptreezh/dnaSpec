from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class GitAnalysis:
    primary_operation: str
    operation_details: List[str]
    suggested_workflow: str
    recommendations: List[str]

class GitAnalyzer:
    def analyze(self, request: str, context: Optional[Dict] = None) -> GitAnalysis:
        request_lower = request.lower()

        # 检测主要操作
        operations = {
            'commit': ['提交', 'commit', '提交信息', 'commit message'],
            'branch': ['分支', 'branch', '分支管理'],
            'conflict': ['冲突', 'conflict', '合并冲突', 'merge conflict'],
            'workflow': ['工作流', 'workflow', 'git flow', '分支策略'],
            'tag': ['标签', 'tag', '版本', 'version', 'release', '发布']
        }

        detected_ops = []
        for op, keywords in operations.items():
            if any(kw in request_lower for kw in keywords):
                detected_ops.append(op)

        primary = detected_ops[0] if detected_ops else 'general'

        # 操作详情
        details = []
        if 'commit' in detected_ops:
            details.append('提交信息生成')
            details.append('Conventional Commits规范')
        if 'branch' in detected_ops:
            details.append('分支命名规范')
            details.append('分支策略选择')
        if 'conflict' in detected_ops:
            details.append('冲突类型识别')
            details.append('解决策略建议')
        if 'workflow' in detected_ops:
            details.append('工作流选择')
            details.append('团队规模评估')
        if 'tag' in detected_ops:
            details.append('语义化版本')
            details.append('标签创建')

        # 建议工作流
        workflow_suggestions = {
            'solo': 'Centralized Workflow（集中式工作流）',
            'small_team': 'Feature Branch Workflow（功能分支工作流）',
            'medium_team': 'Git Flow（Git工作流）',
            'large_team': 'Git Flow with modifications（改进的Git工作流）',
            'continuous_deployment': 'GitHub Flow（GitHub工作流）'
        }

        # 简单分析建议工作流
        if '单人' in request or 'solo' in request_lower:
            suggested = workflow_suggestions['solo']
        elif '小团队' in request or 'small' in request_lower:
            suggested = workflow_suggestions['small_team']
        elif '持续部署' in request or 'continuous' in request_lower or 'ci/cd' in request_lower:
            suggested = workflow_suggestions['continuous_deployment']
        else:
            suggested = '根据项目特点推荐（需评估团队规模、发布频率、CI/CD成熟度）'

        recommendations = []
        if not detected_ops:
            recommendations.append("请明确需要的Git操作类型")

        return GitAnalysis(
            primary_operation=primary,
            operation_details=details,
            suggested_workflow=suggested,
            recommendations=recommendations
        )
