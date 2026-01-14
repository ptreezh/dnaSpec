"""
任务分解技能实现 - 实现从简单到复杂系统的渐进式任务分解
遵循KISS、YAGNI、SOLID原则，确保任务分解的简洁性和有效性
"""
import json
import re
from typing import Dict, List, Any
from pathlib import Path
import uuid
from datetime import datetime

class TaskDecomposer:
    """任务分解核心类"""
    
    def __init__(self):
        self.max_subtasks = 10  # 防止任务爆炸
        self.workspace_base = "./task_workspaces"
    
    def decompose_task(self, requirements: str, depth: int = 1, max_depth: int = 3) -> Dict[str, Any]:
        """
        分解任务为主子任务结构
        遵循KISS原则（Keep It Simple, Stupid）
        遵循YAGNI原则（You Aren't Gonna Need It）
        遵循SOLID原则（Single Responsibility等）
        """
        if depth > max_depth:
            return {
                "id": f"TASK-{uuid.uuid4().hex[:8]}",
                "description": requirements,
                "is_atomic": True,
                "depth": depth,
                "principles_applied": ["KISS", "YAGNI", "SOLID-SRP"],
                "workspace": self._create_isolated_workspace(requirements[:30])
            }
        
        # 使用AI模型分析需求，拆解为子任务
        # 这里简化为模拟AI分析
        subtasks = self._analyze_and_split_requirements(requirements)
        
        if len(subtasks) <= 1 or depth >= max_depth:
            # 如果无法拆分或者到达最大深度，创建原子任务
            return {
                "id": f"TASK-{uuid.uuid4().hex[:8]}",
                "description": requirements,
                "is_atomic": True,
                "depth": depth,
                "principles_applied": ["KISS", "YAGNI", "SOLID-SRP"],
                "workspace": self._create_isolated_workspace(requirements[:30])
            }
        
        # 限制子任务数量，防止爆炸
        limited_subtasks = subtasks[:self.max_subtasks]
        
        result = {
            "id": f"TASK-{uuid.uuid4().hex[:8]}",
            "description": requirements,
            "is_atomic": False,
            "depth": depth,
            "subtasks": [],
            "principles_applied": ["KISS", "YAGNI", "SOLID"],
            "context_isolation_level": depth,
            "workspace": self._create_isolated_workspace(f"level_{depth}_{requirements[:20]}")
        }
        
        for i, subtask in enumerate(limited_subtasks):
            subtask_result = self.decompose_task(subtask, depth + 1, max_depth)
            result["subtasks"].append(subtask_result)
        
        return result
    
    def _analyze_and_split_requirements(self, requirements: str) -> List[str]:
        """分析需求并拆分为子任务"""
        # 简化的任务拆分逻辑，实际应用中应调用AI模型
        sentences = re.split(r'[.!?;]+', requirements)
        subtasks = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:  # 忽略太短的句子
                # 检查是否是任务性描述
                task_indicators = ['需要', '实现', '创建', '开发', '设计', '构建', '添加', '修改', '优化', '分析']
                if any(indicator in sentence for indicator in task_indicators):
                    subtasks.append(sentence)
        
        # 如果没有识别到任务性描述，尝试按功能模块拆分
        if not subtasks:
            # 按功能领域拆分
            functional_areas = [
                '认证', '授权', '数据管理', '用户界面', 'API接口', '数据库', 
                '安全性', '性能', '测试', '部署', '监控', '日志'
            ]
            
            for area in functional_areas:
                if area in requirements:
                    subtasks.append(f"实现{area}功能")
        
        return subtasks[:self.max_subtasks]  # 限制数量防止爆炸
    
    def _create_isolated_workspace(self, task_prefix: str) -> str:
        """为任务创建隔离的工作区"""
        workspace_id = f"{task_prefix.replace(' ', '_')}_{uuid.uuid4().hex[:8]}"
        workspace_path = Path(self.workspace_base) / workspace_id
        
        # 创建工作区目录结构
        workspace_path.mkdir(parents=True, exist_ok=True)
        (workspace_path / "src").mkdir(exist_ok=True)
        (workspace_path / "test").mkdir(exist_ok=True)
        (workspace_path / "docs").mkdir(exist_ok=True)
        
        return str(workspace_path)
    
    def validate_decomposition(self, task_structure: Dict[str, Any]) -> Dict[str, Any]:
        """验证任务分解是否符合原则"""
        validation_result = {
            "is_valid": True,
            "issues": [],
            "metrics": {
                "total_tasks": self._count_tasks(task_structure),
                "max_depth": self._get_max_depth(task_structure),
                "average_branching_factor": self._get_average_branching(task_structure)
            }
        }
        
        # 检查任务数量是否过多（防止爆炸）
        if validation_result["metrics"]["total_tasks"] > 50:
            validation_result["is_valid"] = False
            validation_result["issues"].append("Task count exceeds recommended limit (50)")
        
        # 检查深度是否过深
        if validation_result["metrics"]["max_depth"] > 5:
            validation_result["is_valid"] = False
            validation_result["issues"].append("Task decomposition depth exceeds recommended limit (5)")
        
        # 检查分支因子是否过大
        if validation_result["metrics"]["average_branching_factor"] > 5:
            validation_result["is_valid"] = False
            validation_result["issues"].append("Average branching factor exceeds recommended limit (5)")
        
        return validation_result
    
    def _count_tasks(self, task_structure: Dict[str, Any]) -> int:
        """计算总任务数"""
        count = 1  # 当前任务
        if "subtasks" in task_structure:
            for subtask in task_structure["subtasks"]:
                count += self._count_tasks(subtask)
        return count
    
    def _get_max_depth(self, task_structure: Dict[str, Any], current_depth: int = 0) -> int:
        """获取最大深度"""
        max_depth = current_depth
        if "subtasks" in task_structure:
            for subtask in task_structure["subtasks"]:
                sub_depth = self._get_max_depth(subtask, current_depth + 1)
                max_depth = max(max_depth, sub_depth)
        return max_depth
    
    def _get_average_branching(self, task_structure: Dict[str, Any]) -> float:
        """获取平均分支因子"""
        total_branches = 0
        total_nodes = 0
        
        def traverse(node):
            nonlocal total_branches, total_nodes
            if "subtasks" in node:
                branches = len(node["subtasks"])
                total_branches += branches
                total_nodes += 1
                for subtask in node["subtasks"]:
                    traverse(subtask)
        
        traverse(task_structure)
        return total_branches / total_nodes if total_nodes > 0 else 0

def execute_task_decomposer(args: Dict[str, Any]) -> str:
    """
    任务分解技能执行函数
    Args:
        args: 包含'requirements'键的参数字典
    Returns:
        JSON格式的分解结果
    """
    requirements = args.get('requirements', args.get('input', ''))
    max_depth = args.get('max_depth', 3)
    
    if not requirements:
        return json.dumps({
            "success": False,
            "error": "No requirements provided for task decomposition"
        }, ensure_ascii=False, indent=2)
    
    decomposer = TaskDecomposer()
    task_structure = decomposer.decompose_task(requirements, max_depth=max_depth)
    validation = decomposer.validate_decomposition(task_structure)
    
    result = {
        "success": True,
        "task_structure": task_structure,
        "validation": validation,
        "execution_info": {
            "skill": "task-decomposer",
            "timestamp": datetime.now().isoformat(),
            "principles_applied": ["KISS", "YAGNI", "SOLID"]
        }
    }
    
    return json.dumps(result, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # 测试任务分解
    test_reqs = "开发一个用户管理系统，需要支持用户注册、登录、个人资料管理、密码修改功能，需要考虑安全性，需要有管理后台"
    args = {"requirements": test_reqs, "max_depth": 2}
    result = execute_task_decomposer(args)
    print(result)