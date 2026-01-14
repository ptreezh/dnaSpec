"""
Claude Skills 规范的任务分解技能实现
符合 Claude 官方 Skills 规范
"""
import json
from typing import Dict, Any, List
import uuid
from datetime import datetime


def execute_skill(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    Claude Skills 标准执行函数
    """
    try:
        # 从事件中提取参数
        requirements = event.get('requirements') or event.get('input') or event.get('query', '')
        max_depth = event.get('max_depth', 3)
        
        if not requirements.strip():
            error_result = {
                "success": False,
                "error": "Requirements input is required for task decomposition",
                "input": requirements
            }
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(error_result)
            }

        # 简单的任务分解逻辑（实际应用中会调用AI模型）
        # 这里简化为关键词识别
        sentences = requirements.split('.')
        subtasks = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 5:  # 忽略太短的句子
                # 识别任务性关键词
                task_indicators = ['需要', '实现', '创建', '开发', '设计', '构建', '添加', '修改', '优化', '分析']
                if any(indicator in sentence for indicator in task_indicators):
                    subtasks.append(sentence)
        
        # 如果没有识别到任务性描述，按功能领域分解
        if not subtasks:
            functional_areas = [
                '认证', '授权', '数据管理', '用户界面', 'API接口', '数据库',
                '安全性', '性能', '测试', '部署', '监控', '日志'
            ]

            for area in functional_areas:
                if area in requirements:
                    subtasks.append(f"实现{area}功能")
        
        # 只制子任务数量
        subtasks = subtasks[:10]  # 防止任务爆炸

        result_data = {
            "task_structure": {
                "id": f"TASK-{uuid.uuid4().hex[:8]}",
                "description": requirements,
                "is_atomic": len(subtasks) == 0,
                "depth": 1,
                "subtasks": [{"id": f"SUB-{uuid.uuid4().hex[:8]}", "description": task, "completed": False} for task in subtasks],
                "created_at": datetime.now().isoformat()
            },
            "validation": {
                "is_valid": True,
                "issues": [],
                "metrics": {
                    "total_tasks": len(subtasks) + 1,
                    "max_depth": 1,
                    "average_branching_factor": len(subtasks)
                }
            },
            "execution_info": {
                "skill": "task-decomposer",
                "timestamp": datetime.now().isoformat(),
                "principles_applied": ["KISS", "YAGNI", "SOLID"]
            }
        }

        success_result = {
            "success": True,
            "result": result_data,
            "input": requirements
        }
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(success_result, ensure_ascii=False)
        }
        
    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'input': event
        }
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(error_result, ensure_ascii=False)
        }


def lambda_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    AWS Lambda 兼容的处理函数
    """
    return execute_skill(event, context)


# 同时保留 DNASPEC 格式的 execute 函数以保持兼容性
def execute(args: Dict[str, Any]) -> str:
    """
    DNASPEC 格式的执行函数
    """
    requirements = args.get("requirements", args.get("input", args.get("description", "")))
    max_depth = args.get("max_depth", 3)

    if not requirements.strip():
        return "错误: 需要提供任务分解的需求描述"

    # 简单的任务分解逻辑
    sentences = requirements.split('.')
    subtasks = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 5:  # 忽略太短的句子
            # 识别任务性关键词
            task_indicators = ['需要', '实现', '创建', '开发', '设计', '构建', '添加', '修改', '优化', '分析']
            if any(indicator in sentence for indicator in task_indicators):
                subtasks.append(sentence)
    
    # 如果没有识别到任务性描述，按功能领域分解
    if not subtasks:
        functional_areas = [
            '认证', '授权', '数据管理', '用户界面', 'API接口', '数据库',
            '安全性', '性能', '测试', '部署', '监控', '日志'
        ]

        for area in functional_areas:
            if area in requirements:
                subtasks.append(f"实现{area}功能")
    
    # 只制子任务数量
    subtasks = subtasks[:10]  # 防止任务爆炸

    # 格式化为 DNASPEC 输出
    output_lines = []
    output_lines.append("任务分解结果:")
    output_lines.append(f"主任务: {requirements}")
    output_lines.append(f"子任务数量: {len(subtasks)}")
    output_lines.append("")

    if subtasks:
        output_lines.append("分解的子任务:")
        for i, task in enumerate(subtasks, 1):
            output_lines.append(f"  {i}. {task}")
    else:
        output_lines.append("未识别到具体的子任务，可能需要更详细的需求描述")

    output_lines.append("")
    output_lines.append("应用的原则: KISS, YAGNI, SOLID")

    return "\n".join(output_lines)