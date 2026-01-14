"""
DNASPEC Task Decomposer Skill - 符合AgentSkills.io标准
基于TDD实现，遵循KISS、SOLID、YAGNI原则
"""
import json
import uuid
from typing import Dict, Any, List, Optional, Tuple
from skills.dnaspec_skill_framework import (
    DNASpecSkillBase, 
    track_execution,
    validate_text_input,
    generate_task_id,
    SkillValidationError
)


@track_execution
class TaskDecomposerSkill(DNASpecSkillBase):
    """
    任务分解技能 - 复杂任务分解为可管理的子任务
    
    符合AgentSkills.io规范：
    - name: task-decomposer
    - description: Decomposes complex tasks into manageable, focused subtasks with appropriate isolation
    - 支持4种分解方法：层次、顺序、并行、混合
    """
    
    def __init__(self):
        super().__init__(
            name="task-decomposer",
            description="Decomposes complex tasks into manageable, focused subtasks with appropriate isolation. Use when you need to break down complex projects, create structured work breakdowns, or organize multi-step processes.",
            version="2.0.0"
        )
        
        # 支持的分解方法
        self.decomposition_methods = [
            "hierarchical",
            "sequential", 
            "parallel",
            "hybrid"
        ]
        
        # 复杂度级别
        self.complexity_levels = ["simple", "medium", "complex", "very_complex"]
        
        # 任务优先级
        self.priority_levels = ["low", "medium", "high", "critical"]
        
        # 任务类型映射
        self.task_patterns = {
            "软件开发": ["需求分析", "设计", "开发", "测试", "部署"],
            "系统集成": ["接口设计", "数据迁移", "联调测试", "上线准备"],
            "数据处理": ["数据收集", "清洗", "分析", "可视化", "报告"],
            "项目管理": ["规划", "执行", "监控", "评估", "总结"],
            "业务分析": ["现状分析", "问题识别", "方案设计", "实施计划", "效果评估"]
        }
    
    def validate_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证输入数据
        
        Args:
            input_data: 包含要分解的任务和分解方法的输入数据
            
        Returns:
            验证结果字典
        """
        # 验证必需字段
        if 'input' not in input_data:
            return {
                'valid': False, 
                'error': 'Missing required field: input'
            }
        
        # 验证任务描述
        task_validation = validate_text_input(input_data['input'], 'task')
        if not task_validation['valid']:
            return task_validation
        
        # 验证分解方法
        if 'decomposition_method' in input_data:
            method = input_data['decomposition_method']
            if method not in self.decomposition_methods:
                return {
                    'valid': False,
                    'error': f'Invalid decomposition_method. Must be one of: {", ".join(self.decomposition_methods)}'
                }
        
        # 验证最大深度
        if 'max_depth' in input_data:
            max_depth = input_data['max_depth']
            if not isinstance(max_depth, int) or max_depth < 1 or max_depth > 10:
                return {
                    'valid': False,
                    'error': 'max_depth must be an integer between 1 and 10'
                }
        
        # 验证复杂度目标
        if 'complexity_target' in input_data:
            complexity = input_data['complexity_target']
            if complexity not in self.complexity_levels:
                return {
                    'valid': False,
                    'error': f'Invalid complexity_target. Must be one of: {", ".join(self.complexity_levels)}'
                }
        
        return {'valid': True}
    
    def execute_skill(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行任务分解核心逻辑
        
        Args:
            input_data: 验证过的输入数据
            
        Returns:
            任务分解结果
        """
        task_description = input_data['input']
        decomposition_method = input_data.get('decomposition_method', 'hierarchical')
        max_depth = input_data.get('max_depth', 3)
        complexity_target = input_data.get('complexity_target', 'medium')
        
        # 分析任务特征
        task_analysis = self._analyze_task_complexity(task_description)
        
        # 根据分解方法执行不同的处理
        if decomposition_method == "hierarchical":
            result = self._hierarchical_decomposition(task_description, max_depth, complexity_target)
        elif decomposition_method == "sequential":
            result = self._sequential_decomposition(task_description, max_depth, complexity_target)
        elif decomposition_method == "parallel":
            result = self._parallel_decomposition(task_description, max_depth, complexity_target)
        elif decomposition_method == "hybrid":
            result = self._hybrid_decomposition(task_description, max_depth, complexity_target)
        else:
            raise ValueError(f"Unsupported decomposition method: {decomposition_method}")
        
        # 计算分解元数据
        metadata = self._calculate_decomposition_metadata(
            result['tasks'], decomposition_method, task_analysis
        )
        
        # 生成执行建议
        execution_recommendations = self._generate_execution_recommendations(
            result['tasks'], decomposition_method, task_analysis
        )
        
        return {
            'tasks': result['tasks'],
            'decomposition_metadata': {
                'method_used': decomposition_method,
                'total_tasks': len(result['tasks']),
                'max_depth': metadata['max_depth'],
                'estimated_total_effort': metadata['estimated_total_effort'],
                'critical_path_tasks': metadata['critical_path_tasks'],
                'task_types': metadata['task_types'],
                'isolation_strategy': metadata['isolation_strategy']
            },
            'task_analysis': task_analysis,
            'execution_recommendations': execution_recommendations
        }
    
    def _analyze_task_complexity(self, task_description: str) -> Dict[str, Any]:
        """
        分析任务复杂度
        
        Args:
            task_description: 任务描述
            
        Returns:
            任务分析结果
        """
        text_lower = task_description.lower()
        
        # 识别任务类型
        task_type = self._identify_task_type(task_description)
        
        # 计算复杂度指标
        complexity_indicators = {
            'technical_terms': len([term for term in ['系统', '集成', '架构', '算法', '技术'] if term in text_lower]),
            'management_terms': len([term for term in ['管理', '协调', '规划', '监控', '评估'] if term in text_lower]),
            'integration_terms': len([term for term in ['集成', '接口', '联调', '部署', '上线'] if term in text_lower]),
            'workflow_terms': len([term for term in ['流程', '工作流', '协作', '审批', '验收'] if term in text_lower])
        }
        
        # 计算综合复杂度评分
        total_indicators = sum(complexity_indicators.values())
        if total_indicators >= 8:
            detected_complexity = "very_complex"
        elif total_indicators >= 5:
            detected_complexity = "complex"
        elif total_indicators >= 2:
            detected_complexity = "medium"
        else:
            detected_complexity = "simple"
        
        return {
            'task_type': task_type,
            'complexity_indicators': complexity_indicators,
            'detected_complexity': detected_complexity,
            'estimated_duration': self._estimate_duration(detected_complexity),
            'resource_requirements': self._estimate_resource_requirements(detected_complexity)
        }
    
    def _identify_task_type(self, task_description: str) -> str:
        """
        识别任务类型
        
        Args:
            task_description: 任务描述
            
        Returns:
            任务类型
        """
        text_lower = task_description.lower()
        
        for task_type, keywords in self.task_patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                return task_type
        
        return "general"
    
    def _hierarchical_decomposition(
        self, 
        task_description: str, 
        max_depth: int, 
        complexity_target: str
    ) -> Dict[str, Any]:
        """
        层次分解方法
        
        Args:
            task_description: 任务描述
            max_depth: 最大深度
            complexity_target: 复杂度目标
            
        Returns:
            层次分解结果
        """
        tasks = []
        
        # 生成根任务
        root_task = {
            'id': generate_task_id(),
            'description': task_description,
            'parent_id': None,
            'level': 0,
            'dependencies': [],
            'estimated_effort': self._estimate_effort(task_description, complexity_target),
            'complexity': complexity_target,
            'priority': 'high',
            'isolation_context': 'main_task_coordination'
        }
        tasks.append(root_task)
        
        # 生成第一层子任务
        level_1_tasks = self._generate_level_tasks(task_description, 1, complexity_target)
        root_task['subtasks'] = [task['id'] for task in level_1_tasks]
        tasks.extend(level_1_tasks)
        
        # 根据深度生成更多层级
        if max_depth > 1:
            for parent_task in level_1_tasks:
                if max_depth > 2:
                    level_2_tasks = self._generate_level_tasks(
                        parent_task['description'], 2, complexity_target, parent_task['id']
                    )
                    parent_task['subtasks'] = [task['id'] for task in level_2_tasks]
                    tasks.extend(level_2_tasks)
        
        return {'tasks': tasks}
    
    def _sequential_decomposition(
        self, 
        task_description: str, 
        max_depth: int, 
        complexity_target: str
    ) -> Dict[str, Any]:
        """
        顺序分解方法
        
        Args:
            task_description: 任务描述
            max_depth: 最大深度
            complexity_target: 复杂度目标
            
        Returns:
            顺序分解结果
        """
        tasks = []
        
        # 生成顺序任务序列
        sequential_steps = self._generate_sequential_steps(task_description, complexity_target)
        
        for i, step_description in enumerate(sequential_steps[:max_depth * 2]):  # 限制任务数量
            task = {
                'id': generate_task_id(),
                'description': step_description,
                'parent_id': None,
                'level': 0,
                'dependencies': [tasks[-1]['id']] if tasks else [],  # 前一个任务作为依赖
                'estimated_effort': self._estimate_effort(step_description, complexity_target),
                'complexity': complexity_target,
                'priority': 'medium' if i > 0 else 'high',
                'isolation_context': f'sequential_step_{i+1}'
            }
            tasks.append(task)
        
        return {'tasks': tasks}
    
    def _parallel_decomposition(
        self, 
        task_description: str, 
        max_depth: int, 
        complexity_target: str
    ) -> Dict[str, Any]:
        """
        并行分解方法
        
        Args:
            task_description: 任务描述
            max_depth: 最大深度
            complexity_target: 复杂度目标
            
        Returns:
            并行分解结果
        """
        tasks = []
        
        # 生成并行任务流
        parallel_streams = self._generate_parallel_streams(task_description, complexity_target)
        
        for stream_id, stream_tasks in enumerate(parallel_streams[:3]):  # 限制并行流数量
            for i, task_desc in enumerate(stream_tasks[:max_depth]):
                task = {
                    'id': generate_task_id(),
                    'description': task_desc,
                    'parent_id': None,
                    'level': i + 1,
                    'dependencies': [],  # 并行任务通常无依赖
                    'estimated_effort': self._estimate_effort(task_desc, complexity_target),
                    'complexity': complexity_target,
                    'priority': 'medium',
                    'isolation_context': f'parallel_stream_{stream_id+1}'
                }
                tasks.append(task)
        
        return {'tasks': tasks}
    
    def _hybrid_decomposition(
        self, 
        task_description: str, 
        max_depth: int, 
        complexity_target: str
    ) -> Dict[str, Any]:
        """
        混合分解方法
        
        Args:
            task_description: 任务描述
            max_depth: 最大深度
            complexity_target: 复杂度目标
            
        Returns:
            混合分解结果
        """
        tasks = []
        
        # 阶段1：准备阶段（顺序）
        phase1_tasks = self._generate_sequential_steps(f"准备{task_description}", complexity_target)[:2]
        for i, task_desc in enumerate(phase1_tasks):
            task = {
                'id': generate_task_id(),
                'description': task_desc,
                'parent_id': None,
                'level': 1,
                'dependencies': [tasks[-1]['id']] if tasks else [],
                'estimated_effort': self._estimate_effort(task_desc, complexity_target),
                'complexity': complexity_target,
                'priority': 'high',
                'isolation_context': f'phase1_step_{i+1}'
            }
            tasks.append(task)
        
        # 阶段2：执行阶段（并行）
        phase2_tasks = self._generate_parallel_streams(f"执行{task_description}", complexity_target)
        for stream_id, stream_tasks in enumerate(phase2_tasks[:2]):
            for i, task_desc in enumerate(stream_tasks[:max_depth-1]):
                task = {
                    'id': generate_task_id(),
                    'description': task_desc,
                    'parent_id': None,
                    'level': 2,
                    'dependencies': [phase1_tasks[-1]['id']],  # 依赖准备阶段最后一个任务
                    'estimated_effort': self._estimate_effort(task_desc, complexity_target),
                    'complexity': complexity_target,
                    'priority': 'medium',
                    'isolation_context': f'phase2_stream_{stream_id+1}_step_{i+1}'
                }
                tasks.append(task)
        
        return {'tasks': tasks}
    
    def _generate_level_tasks(
        self, 
        task_description: str, 
        level: int, 
        complexity_target: str,
        parent_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        生成层级任务
        
        Args:
            task_description: 上级任务描述
            level: 当前层级
            complexity_target: 复杂度目标
            parent_id: 父任务ID
            
        Returns:
            层级任务列表
        """
        task_templates = {
            1: ["需求分析", "方案设计", "技术选型"],
            2: ["详细设计", "模块开发", "接口定义"],
            3: ["单元测试", "集成测试", "文档编写"]
        }
        
        templates = task_templates.get(level, ["详细开发", "质量检查", "成果验收"])
        tasks = []
        
        for template in templates[:3]:  # 每层最多3个任务
            task = {
                'id': generate_task_id(),
                'description': f"{template} - {task_description[:50]}",
                'parent_id': parent_id,
                'level': level,
                'dependencies': [],
                'estimated_effort': self._estimate_effort(template, complexity_target),
                'complexity': complexity_target,
                'priority': self._determine_priority(level),
                'isolation_context': f'level_{level}_task'
            }
            tasks.append(task)
        
        return tasks
    
    def _generate_sequential_steps(self, task_description: str, complexity_target: str) -> List[str]:
        """
        生成顺序步骤
        
        Args:
            task_description: 任务描述
            complexity_target: 复杂度目标
            
        Returns:
            顺序步骤列表
        """
        step_templates = {
            "simple": ["需求确认", "任务执行", "结果验证"],
            "medium": ["需求分析", "方案设计", "实施开发", "测试验证", "部署上线"],
            "complex": ["详细需求分析", "系统架构设计", "模块开发", "集成测试", "用户验收", "部署上线", "监控优化"],
            "very_complex": ["业务分析", "技术调研", "详细设计", "原型开发", "正式开发", "全面测试", "用户培训", "部署上线", "运维监控"]
        }
        
        return step_templates.get(complexity_target, step_templates["medium"])
    
    def _generate_parallel_streams(self, task_description: str, complexity_target: str) -> List[List[str]]:
        """
        生成并行任务流
        
        Args:
            task_description: 任务描述
            complexity_target: 复杂度目标
            
        Returns:
            并行任务流列表
        """
        stream_templates = {
            "simple": [
                ["需求分析"],
                ["技术实现"]
            ],
            "medium": [
                ["前端开发", "后端开发"],
                ["数据库设计", "接口开发"]
            ],
            "complex": [
                ["前端开发", "后端开发", "数据库设计"],
                ["接口开发", "系统测试", "文档编写"]
            ],
            "very_complex": [
                ["前端开发", "后端开发", "数据库设计", "API开发"],
                ["系统测试", "性能优化", "文档编写", "安全检查"]
            ]
        }
        
        return stream_templates.get(complexity_target, stream_templates["medium"])
    
    def _estimate_effort(self, task_description: str, complexity_target: str) -> str:
        """
        估算工作量
        
        Args:
            task_description: 任务描述
            complexity_target: 复杂度目标
            
        Returns:
            工作量估算字符串
        """
        effort_ranges = {
            "simple": {"前端": "1-2天", "后端": "2-3天", "测试": "1天", "文档": "0.5天"},
            "medium": {"前端": "3-5天", "后端": "5-7天", "测试": "2-3天", "文档": "1-2天"},
            "complex": {"前端": "1-2周", "后端": "2-3周", "测试": "3-5天", "文档": "2-3天"},
            "very_complex": {"前端": "2-4周", "后端": "4-6周", "测试": "1-2周", "文档": "1-2周"}
        }
        
        # 根据任务描述选择合适的工作量
        desc_lower = task_description.lower()
        
        if any(keyword in desc_lower for keyword in ["前端", "界面", "UI", "前端", "frontend"]):
            return effort_ranges[complexity_target]["前端"]
        elif any(keyword in desc_lower for keyword in ["后端", "服务", "API", "backend"]):
            return effort_ranges[complexity_target]["后端"]
        elif any(keyword in desc_lower for keyword in ["测试", "质量", "test", "quality"]):
            return effort_ranges[complexity_target]["测试"]
        elif any(keyword in desc_lower for keyword in ["文档", "说明", "doc", "documentation"]):
            return effort_ranges[complexity_target]["文档"]
        else:
            return effort_ranges[complexity_target]["后端"]  # 默认使用后端估算
    
    def _determine_priority(self, level: int) -> str:
        """
        根据层级确定优先级
        
        Args:
            level: 任务层级
            
        Returns:
            优先级
        """
        if level == 1:
            return "high"
        elif level == 2:
            return "medium"
        else:
            return "low"
    
    def _estimate_duration(self, complexity: str) -> str:
        """
        估算任务持续时间
        
        Args:
            complexity: 复杂度级别
            
        Returns:
            持续时间估算
        """
        duration_map = {
            "simple": "1-2天",
            "medium": "3-7天",
            "complex": "1-3周",
            "very_complex": "2-6周"
        }
        
        return duration_map.get(complexity, "3-7天")
    
    def _estimate_resource_requirements(self, complexity: str) -> List[str]:
        """
        估算资源需求
        
        Args:
            complexity: 复杂度级别
            
        Returns:
            资源需求列表
        """
        resource_map = {
            "simple": ["1名开发人员", "基础开发环境"],
            "medium": ["2-3名开发人员", "测试环境", "项目管理"],
            "complex": ["3-5名开发人员", "专门测试团队", "项目管理", "技术架构师"],
            "very_complex": ["5-10名开发人员", "多专业团队", "项目管理", "技术架构师", "产品经理"]
        }
        
        return resource_map.get(complexity, ["2-3名开发人员", "测试环境", "项目管理"])
    
    def _calculate_decomposition_metadata(
        self, 
        tasks: List[Dict[str, Any]], 
        method: str, 
        task_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        计算分解元数据
        
        Args:
            tasks: 任务列表
            method: 分解方法
            task_analysis: 任务分析结果
            
        Returns:
            分解元数据
        """
        # 计算最大深度
        max_depth = max([task.get('level', 0) for task in tasks]) if tasks else 0
        
        # 计算总工作量估算
        total_effort_days = 0
        for task in tasks:
            effort_str = task.get('estimated_effort', '1天')
            # 提取数字进行汇总
            import re
            numbers = re.findall(r'\d+', effort_str)
            if numbers:
                total_effort_days += int(numbers[0])
        
        # 识别关键路径任务
        critical_path_tasks = self._identify_critical_path(tasks, method)
        
        # 识别任务类型
        task_types = list(set([task.get('complexity', 'medium') for task in tasks]))
        
        # 确定隔离策略
        isolation_strategy = self._determine_isolation_strategy(method, task_analysis['detected_complexity'])
        
        return {
            'max_depth': max_depth,
            'estimated_total_effort': f"{total_effort_days}天",
            'critical_path_tasks': critical_path_tasks,
            'task_types': task_types,
            'isolation_strategy': isolation_strategy
        }
    
    def _identify_critical_path(self, tasks: List[Dict[str, Any]], method: str) -> List[str]:
        """
        识别关键路径任务
        
        Args:
            tasks: 任务列表
            method: 分解方法
            
        Returns:
            关键路径任务ID列表
        """
        if method == "sequential":
            # 顺序方法：所有任务都在关键路径上
            return [task['id'] for task in tasks]
        elif method == "parallel":
            # 并行方法：最高优先级任务在关键路径上
            high_priority_tasks = [task['id'] for task in tasks if task.get('priority') == 'high']
            return high_priority_tasks if high_priority_tasks else [tasks[0]['id']] if tasks else []
        elif method == "hierarchical":
            # 层次方法：根路径和关键分支
            root_task = [task['id'] for task in tasks if task.get('parent_id') is None]
            level_1_tasks = [task['id'] for task in tasks if task.get('level') == 1]
            return root_task + level_1_tasks
        else:  # hybrid
            # 混合方法：第一阶段 + 并行阶段的优先任务
            phase1_tasks = [task['id'] for task in tasks if task.get('level') == 1]
            phase2_high_tasks = [task['id'] for task in tasks if task.get('level') == 2 and task.get('priority') == 'high']
            return phase1_tasks + phase2_high_tasks
    
    def _determine_isolation_strategy(self, method: str, complexity: str) -> str:
        """
        确定隔离策略
        
        Args:
            method: 分解方法
            complexity: 复杂度级别
            
        Returns:
            隔离策略
        """
        if method == "parallel":
            return "process_isolation"  # 进程隔离
        elif complexity in ["complex", "very_complex"]:
            return "workspace_isolation"  # 工作空间隔离
        elif method == "hierarchical":
            return "responsibility_isolation"  # 职责隔离
        else:
            return "interface_isolation"  # 接口隔离
    
    def _generate_execution_recommendations(
        self, 
        tasks: List[Dict[str, Any]], 
        method: str, 
        task_analysis: Dict[str, Any]
    ) -> List[str]:
        """
        生成执行建议
        
        Args:
            tasks: 任务列表
            method: 分解方法
            task_analysis: 任务分析结果
            
        Returns:
            执行建议列表
        """
        recommendations = [
            f"使用{method}方法进行任务执行",
            f"总任务数量：{len(tasks)}个",
            f"预计总工作量：{self._calculate_total_effort(tasks)}",
            f"建议资源分配：{task_analysis['resource_requirements'][0]}"
        ]
        
        # 根据复杂度添加特定建议
        if task_analysis['detected_complexity'] in ["complex", "very_complex"]:
            recommendations.extend([
                "建议分阶段执行，每阶段完成后进行评审",
                "配置专门的项目管理工具进行跟踪",
                "建立定期的团队协调会议机制"
            ])
        
        # 根据方法添加特定建议
        if method == "parallel":
            recommendations.extend([
                "建立并行任务的协调机制",
                "配置统一的开发环境和规范",
                "设置定期的集成和同步检查点"
            ])
        elif method == "hierarchical":
            recommendations.extend([
                "明确各级任务的负责人和职责范围",
                "建立层级间的沟通和报告机制",
                "配置任务依赖跟踪系统"
            ])
        
        return recommendations[:8]  # 限制建议数量
    
    def _calculate_total_effort(self, tasks: List[Dict[str, Any]]) -> str:
        """
        计算总工作量
        
        Args:
            tasks: 任务列表
            
        Returns:
            总工作量字符串
        """
        total_days = 0
        for task in tasks:
            effort_str = task.get('estimated_effort', '1天')
            import re
            numbers = re.findall(r'\d+', effort_str)
            if numbers:
                total_days += int(numbers[0])
        
        return f"{total_days}天"


# 创建技能实例
task_decomposer_skill = TaskDecomposerSkill()

# 导出Lambda处理器（符合AgentSkills.io标准）
def lambda_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """Lambda处理器入口点"""
    return task_decomposer_skill.lambda_handler(event, context)

# 导出技能实例（用于注册）
def get_skill():
    """获取技能实例"""
    return task_decomposer_skill