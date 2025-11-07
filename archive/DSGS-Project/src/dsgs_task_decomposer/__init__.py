# dsgs-task-decomposer子技能实现

import os
import sys
from typing import Dict, Any, List, Tuple
from collections import defaultdict

class DSGSTaskDecomposer:
    """DSGS任务分解器子技能类"""
    
    def __init__(self):
        """初始化任务分解器技能"""
        self.name = "dsgs-task-decomposer"
        self.description = "DSGS任务分解器子技能，用于将复杂项目需求分解为原子化任务，生成任务依赖关系图，确保任务上下文文档的闭包性"
        self.capabilities = [
            "task_decomposition",
            "dependency_analysis",
            "context_closure",
            "execution_planning"
        ]
    
    def process_request(self, request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """处理任务分解请求"""
        if not request or not request.strip():
            return {"error": "请求不能为空"}
        
        # 分析请求并生成任务分解
        task_decomposition = self._generate_task_decomposition(request, context or {})
        
        result = {
            "status": "completed",
            "skill": self.name,
            "request": request,
            "task_decomposition": task_decomposition,
            "timestamp": self._get_timestamp()
        }
        
        return result
    
    def _generate_task_decomposition(self, request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """生成任务分解"""
        # 这里是任务分解的核心逻辑
        # 在实际实现中，这将是一个复杂的分析和分解过程
        
        # 提取关键信息
        key_points = self._extract_key_points(request)
        
        # 生成原子化任务
        atomic_tasks = self._create_atomic_tasks(request, key_points)
        
        # 分析任务依赖关系
        dependencies = self._analyze_dependencies(atomic_tasks)
        
        # 生成执行计划
        execution_plan = self._generate_execution_plan(atomic_tasks, dependencies)
        
        # 生成任务分解结果
        decomposition = {
            "atomic_tasks": atomic_tasks,
            "dependencies": dependencies,
            "execution_plan": execution_plan,
            "context_documents": self._generate_context_documents(atomic_tasks),
            "resource_allocation": self._suggest_resource_allocation(atomic_tasks)
        }
        
        return decomposition
    
    def _extract_key_points(self, request: str) -> List[str]:
        """从请求中提取关键点"""
        # 简单的关键词提取（实际实现中会更复杂）
        keywords = []
        request_lower = request.lower()
        
        if "web" in request_lower or "website" in request_lower:
            keywords.append("web_development")
        if "mobile" in request_lower or "app" in request_lower:
            keywords.append("mobile_app")
        if "api" in request_lower:
            keywords.append("api_development")
        if "database" in request_lower or "data" in request_lower:
            keywords.append("data_management")
        if "ui" in request_lower or "interface" in request_lower:
            keywords.append("user_interface")
        if "security" in request_lower or "secure" in request_lower:
            keywords.append("security_implementation")
        if "testing" in request_lower:
            keywords.append("testing")
        if "deployment" in request_lower or "deploy" in request_lower:
            keywords.append("deployment")
            
        return keywords
    
    def _create_atomic_tasks(self, request: str, key_points: List[str]) -> List[Dict[str, Any]]:
        """创建原子化任务"""
        tasks = []
        task_id = 1
        
        # 基于关键点创建任务
        for point in key_points:
            if point == "web_development":
                tasks.extend([
                    {
                        "id": f"T{task_id:03d}",
                        "name": "前端框架选择",
                        "description": "选择合适的前端框架和技术栈",
                        "type": "planning",
                        "estimated_hours": 4
                    },
                    {
                        "id": f"T{task_id+1:03d}",
                        "name": "UI组件设计",
                        "description": "设计用户界面组件和交互流程",
                        "type": "design",
                        "estimated_hours": 8
                    },
                    {
                        "id": f"T{task_id+2:03d}",
                        "name": "前端页面开发",
                        "description": "实现前端页面和用户交互功能",
                        "type": "development",
                        "estimated_hours": 16
                    }
                ])
                task_id += 3
            elif point == "api_development":
                tasks.extend([
                    {
                        "id": f"T{task_id:03d}",
                        "name": "API设计",
                        "description": "设计RESTful API接口规范",
                        "type": "design",
                        "estimated_hours": 6
                    },
                    {
                        "id": f"T{task_id+1:03d}",
                        "name": "API实现",
                        "description": "实现后端API服务功能",
                        "type": "development",
                        "estimated_hours": 12
                    },
                    {
                        "id": f"T{task_id+2:03d}",
                        "name": "API文档编写",
                        "description": "编写详细的API文档和使用说明",
                        "type": "documentation",
                        "estimated_hours": 4
                    }
                ])
                task_id += 3
            elif point == "data_management":
                tasks.extend([
                    {
                        "id": f"T{task_id:03d}",
                        "name": "数据库设计",
                        "description": "设计数据库模式和表结构",
                        "type": "design",
                        "estimated_hours": 8
                    },
                    {
                        "id": f"T{task_id+1:03d}",
                        "name": "数据模型实现",
                        "description": "实现数据模型和数据访问层",
                        "type": "development",
                        "estimated_hours": 10
                    }
                ])
                task_id += 2
            elif point == "security_implementation":
                tasks.append({
                    "id": f"T{task_id:03d}",
                    "name": "安全机制实现",
                    "description": "实现认证、授权和数据安全机制",
                    "type": "development",
                    "estimated_hours": 8
                })
                task_id += 1
            elif point == "testing":
                tasks.append({
                    "id": f"T{task_id:03d}",
                    "name": "测试用例编写",
                    "description": "编写单元测试和集成测试用例",
                    "type": "testing",
                    "estimated_hours": 6
                })
                task_id += 1
            elif point == "deployment":
                tasks.append({
                    "id": f"T{task_id:03d}",
                    "name": "部署配置",
                    "description": "配置部署环境和持续集成流程",
                    "type": "deployment",
                    "estimated_hours": 6
                })
                task_id += 1
        
        # 如果没有特定任务，创建通用任务
        if not tasks:
            tasks = [
                {
                    "id": "T001",
                    "name": "需求分析",
                    "description": "详细分析项目需求和约束条件",
                    "type": "analysis",
                    "estimated_hours": 4
                },
                {
                    "id": "T002",
                    "name": "技术选型",
                    "description": "选择合适的技术栈和工具",
                    "type": "planning",
                    "estimated_hours": 4
                },
                {
                    "id": "T003",
                    "name": "架构设计",
                    "description": "设计系统架构和组件关系",
                    "type": "design",
                    "estimated_hours": 8
                },
                {
                    "id": "T004",
                    "name": "核心功能开发",
                    "description": "实现系统核心业务功能",
                    "type": "development",
                    "estimated_hours": 16
                },
                {
                    "id": "T005",
                    "name": "测试验证",
                    "description": "进行全面的测试验证",
                    "type": "testing",
                    "estimated_hours": 8
                },
                {
                    "id": "T006",
                    "name": "部署上线",
                    "description": "部署系统到生产环境",
                    "type": "deployment",
                    "estimated_hours": 4
                }
            ]
        
        return tasks
    
    def _analyze_dependencies(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """分析任务依赖关系"""
        dependencies = []
        
        # 简单的依赖关系分析（实际实现中会更复杂）
        task_dict = {task["id"]: task for task in tasks}
        
        for task in tasks:
            task_id = task["id"]
            
            # 根据任务类型确定依赖关系
            if task["type"] == "design":
                # 设计任务通常依赖于需求分析
                for potential_dep in tasks:
                    if potential_dep["type"] == "analysis" and potential_dep["id"] != task_id:
                        dependencies.append({
                            "from": potential_dep["id"],
                            "to": task_id,
                            "type": "finish_to_start"
                        })
            elif task["type"] == "development":
                # 开发任务通常依赖于设计任务
                for potential_dep in tasks:
                    if potential_dep["type"] == "design" and potential_dep["id"] != task_id:
                        dependencies.append({
                            "from": potential_dep["id"],
                            "to": task_id,
                            "type": "finish_to_start"
                        })
            elif task["type"] == "testing":
                # 测试任务依赖于开发任务
                for potential_dep in tasks:
                    if potential_dep["type"] == "development" and potential_dep["id"] != task_id:
                        dependencies.append({
                            "from": potential_dep["id"],
                            "to": task_id,
                            "type": "finish_to_start"
                        })
            elif task["type"] == "deployment":
                # 部署任务依赖于测试任务
                for potential_dep in tasks:
                    if potential_dep["type"] == "testing" and potential_dep["id"] != task_id:
                        dependencies.append({
                            "from": potential_dep["id"],
                            "to": task_id,
                            "type": "finish_to_start"
                        })
        
        return dependencies
    
    def _generate_execution_plan(self, tasks: List[Dict[str, Any]], dependencies: List[Dict[str, Any]]) -> List[str]:
        """生成执行计划"""
        # 简单的执行顺序生成（实际实现中会使用拓扑排序等算法）
        execution_order = []
        
        # 按类型排序：分析 -> 设计 -> 开发 -> 测试 -> 部署
        type_order = ["analysis", "planning", "design", "development", "testing", "deployment"]
        
        for task_type in type_order:
            for task in tasks:
                if task["type"] == task_type and task["id"] not in execution_order:
                    execution_order.append(task["id"])
        
        return execution_order
    
    def _generate_context_documents(self, tasks: List[Dict[str, Any]]) -> Dict[str, str]:
        """生成任务上下文文档"""
        context_docs = {}
        
        for task in tasks:
            context_docs[task["id"]] = f"""
# {task["name"]} 上下文文档

## 任务描述
{task["description"]}

## 输入要求
- 相关需求文档
- 技术规范说明
- 设计约束条件

## 输出要求
- 完整的功能实现
- 相关文档说明
- 测试验证结果

## 验收标准
- 功能完整性和正确性
- 代码质量和可维护性
- 符合设计规范要求
            """.strip()
        
        return context_docs
    
    def _suggest_resource_allocation(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """建议资源分配"""
        resource_allocation = {
            "team_roles": ["项目经理", "架构师", "开发工程师", "测试工程师", "运维工程师"],
            "task_assignment": {},
            "tools_required": ["开发工具", "测试工具", "部署工具", "协作平台"]
        }
        
        # 简单的任务分配建议
        for task in tasks:
            if task["type"] == "analysis":
                resource_allocation["task_assignment"][task["id"]] = "架构师"
            elif task["type"] == "design":
                resource_allocation["task_assignment"][task["id"]] = "架构师"
            elif task["type"] == "development":
                resource_allocation["task_assignment"][task["id"]] = "开发工程师"
            elif task["type"] == "testing":
                resource_allocation["task_assignment"][task["id"]] = "测试工程师"
            elif task["type"] == "deployment":
                resource_allocation["task_assignment"][task["id"]] = "运维工程师"
            else:
                resource_allocation["task_assignment"][task["id"]] = "开发工程师"
        
        return resource_allocation
    
    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_skill_info(self) -> Dict[str, Any]:
        """获取技能信息"""
        return {
            "name": self.name,
            "description": self.description,
            "capabilities": self.capabilities
        }

# 全局实例
task_decomposer = DSGSTaskDecomposer()

if __name__ == "__main__":
    # 简单测试
    print("DSGS Task Decomposer Skill Loaded")
    print(f"Skill Name: {task_decomposer.name}")
    print(f"Description: {task_decomposer.description}")