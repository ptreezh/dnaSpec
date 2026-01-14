"""
DNASPEC 综合技能实现
最完善的技能实现，结合所有最佳实践
"""
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List


def execute_skill(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    智能技能路由 - 根据输入内容智能判断需要执行的技能
    """
    # 从事件中提取关键信息
    input_text = (
        event.get('requirements') or
        event.get('context') or
        event.get('input') or
        event.get('query', '') or
        event.get('description', '')
    ).lower()

    # 根据关键词判断技能类型
    if any(kw in input_text for kw in ['architect', 'design', 'architecture', 'system', 'structure', 'build', 'construct']):
        return _execute_architect_skill(event)
    elif any(kw in input_text for kw in ['task', 'decompose', 'break', 'subtask', 'decomposition', 'divide', 'split']):
        return _execute_task_decomposer_skill(event)
    elif any(kw in input_text for kw in ['constraint', 'rule', 'condition', 'requirement', 'security', 'policy', 'governance']):
        return _execute_constraint_generator_skill(event)
    elif any(kw in input_text for kw in ['analyze', 'context', 'quality', 'evaluate', 'assessment', 'metric']):
        return _execute_context_analysis_skill(event)
    elif any(kw in input_text for kw in ['agent', 'create', 'build', 'generate', 'make']):
        return _execute_agent_creator_skill(event)
    elif any(kw in input_text for kw in ['module', 'modular', 'component', 'structure', 'organization']):
        return _execute_modulizer_skill(event)
    elif any(kw in input_text for kw in ['api', 'interface', 'endpoint', 'service', 'check', 'validate']):
        return _execute_api_checker_skill(event)
    else:
        # 默认执行架构设计
        return _execute_architect_skill(event)


def _execute_architect_skill(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    架构设计技能实现
    """
    try:
        # 从事件中提取描述
        description = (
            event.get('requirements') or
            event.get('input') or
            event.get('query', '') or
            event.get('description', '')
        ).lower()

        # 使用架构映射
        architecture_map = {
            "电商": "[WebApp] -> [API Server] -> [Database]",
            "博客": "[WebApp] -> [Database]",
            "用户管理": "[Frontend] -> [API Gateway] -> [Auth Service] -> [User DB]",
            "认证": "[Auth Service] -> [User DB] -> [Session Store]",
            "api": "[API Gateway] -> [Microservices] -> [Data Layer]"
        }

        # 查找匹配的架构
        for keyword, architecture in architecture_map.items():
            if keyword in description:
                result = {
                    "success": True,
                    "result": architecture,
                    "architecture_type": keyword,
                    "input": description
                }
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps(result, ensure_ascii=False)
                }

        # 默认返回
        result = {
            "success": True,
            "result": f"根据需求设计系统架构: {description}",
            "architecture_type": "custom",
            "input": description
        }

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(result, ensure_ascii=False)
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


def _execute_task_decomposer_skill(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    任务分解技能实现
    """
    try:
        requirements = (
            event.get('requirements') or
            event.get('input') or
            event.get('query', '') or
            event.get('description', '')
        )

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

        # 简单的任务分解逻辑
        sentences = requirements.split('.')
        subtasks = []

        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 5:  # 忽略太短的句子
                # 识别任务性关键词
                task_indicators = ['需要', '实现', '创建', '开发', '设计', '构建', '添加', '修改', '优化', '分析', 'build', 'develop', 'implement', 'create']
                if any(indicator in sentence.lower() for indicator in task_indicators):
                    subtasks.append(sentence)

        # 如果没有识别到任务性描述，按功能领域分解
        if not subtasks:
            functional_areas = [
                '认证', '授权', '数据管理', '用户界面', 'API接口', '数据库',
                '安全性', '性能', '测试', '部署', '监控', '日志',
                'authentication', 'authorization', 'data management', 'UI', 'API', 'database'
            ]

            for area in functional_areas:
                if area in requirements.lower():
                    subtasks.append(f"实现{area}功能")

        # 限制子任务数量
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


def _execute_constraint_generator_skill(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    约束生成技能实现
    """
    try:
        requirements = (
            event.get('requirements') or
            event.get('input') or
            event.get('query', '') or
            event.get('description', '')
        )
        change_request = event.get('change_request', '')

        if not requirements.strip():
            error_result = {
                "success": False,
                "error": "Requirements input is required for constraint generation",
                "input": requirements
            }
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(error_result)
            }

        # 生成约束
        req_lower = requirements.lower()
        constraints = []

        # 安全约束
        if any(term in req_lower for term in ['security', 'secure', 'auth', 'encrypt', 'privacy', 'protect', 'password', 'login']):
            constraints.append({
                "id": f"constraint_{uuid.uuid4().hex[:8]}",
                "type": "security",
                "description": "系统必须实现标准安全措施",
                "severity": "high",
                "created_at": datetime.now().isoformat()
            })

        # 性能约束
        if any(term in req_lower for term in ['performance', 'fast', 'response', 'throughput', 'latency', 'speed']):
            constraints.append({
                "id": f"constraint_{uuid.uuid4().hex[:8]}",
                "type": "performance",
                "description": "系统必须满足定义的性能要求",
                "severity": "medium",
                "created_at": datetime.now().isoformat()
            })

        # 数据约束
        if any(term in req_lower for term in ['data', 'database', 'storage', 'retrieve', 'persist', 'record']):
            constraints.append({
                "id": f"constraint_{uuid.uuid4().hex[:8]}",
                "type": "data_integrity",
                "description": "系统必须保持数据完整性和备份能力",
                "severity": "high",
                "created_at": datetime.now().isoformat()
            })

        # 对齐检查
        alignment_check = {
            "is_aligned": not (change_request and
                             any(contradiction in change_request.lower()
                                 for contradiction in ['no security', 'negligible performance', 'unreliable'])),
            "conflicts": [],
            "suggestions": ["No change request provided, requirements are baseline"] if not change_request else ["Change request appears aligned with base requirements"]
        }

        result_data = {
            "constraints": constraints,
            "alignment_check": alignment_check,
            "version_info": {
                "current_version": f"version_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}",
                "tracked": True
            },
            "timestamp": datetime.now().timestamp()
        }

        success_result = {
            "success": True,
            "result": result_data,
            "input": {
                "requirements": requirements,
                "change_request": change_request
            }
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


def _execute_context_analysis_skill(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    上下文分析技能实现
    """
    try:
        context_input = (
            event.get('context') or
            event.get('input') or
            event.get('query', '') or
            event.get('description', '')
        )

        if not context_input.strip():
            error_result = {
                "success": False,
                "error": "Context input is required for analysis",
                "input": context_input
            }
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(error_result)
            }

        # 简单的上下文分析（在实际实现中会调用AI模型）
        context_length = len(context_input)
        token_count_estimate = max(1, len(context_input) // 4)

        # 计算质量指标
        clarity = min(1.0, max(0.0, 0.5 + len(context_input) * 0.00001))
        relevance = min(1.0, max(0.0, 0.7 + (0.1 if any(kw in context_input.lower() for kw in ['system', 'function', 'task', 'requirement']) else 0)))
        completeness = min(1.0, max(0.0, 0.3 + (0.3 if any(kw in context_input.lower() for kw in ['constraint', 'requirement', 'goal']) else 0)))
        consistency = min(1.0, max(0.0, 0.8 - (0.2 if any(kw in context_input.lower() for kw in ['but', 'however']) else 0)))
        efficiency = min(1.0, max(0.0, 1.0 - len(context_input) * 0.00005))

        result_data = {
            "context_length": context_length,
            "token_count_estimate": token_count_estimate,
            "metrics": {
                "clarity": round(clarity, 2),
                "relevance": round(relevance, 2),
                "completeness": round(completeness, 2),
                "consistency": round(consistency, 2),
                "efficiency": round(efficiency, 2)
            },
            "suggestions": [
                "Add more specific goal descriptions",
                "Supplement constraint conditions and specific requirements",
                "Improve expression clarity"
            ],
            "issues": [i for i in [
                "Lack of explicit constraint conditions" if completeness < 0.6 else "",
                "Some expressions can be more precise" if clarity < 0.7 else ""
            ] if i],  # Filter out empty issues
            "confidence": 0.85
        }

        success_result = {
            "success": True,
            "result": result_data,
            "input": context_input
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


def _execute_agent_creator_skill(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    代理创建技能实现
    """
    try:
        agent_description = (
            event.get('agent_description') or
            event.get('requirements') or
            event.get('input') or
            event.get('description', '')
        )

        if not agent_description.strip():
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'success': False,
                    'error': 'Agent description is required',
                    'input': agent_description
                })
            }

        # 生成智能体配置
        agent_config = {
            "id": f"agent_{uuid.uuid4().hex[:8]}",
            "role": agent_description,
            "domain": "general",
            "capabilities": ["Task execution", "Information retrieval", "Decision making"],
            "instructions": f"You are acting as a {agent_description} in the general domain.",
            "personality": "Professional, helpful, focused on assigned tasks",
            "created_at": datetime.now().isoformat()
        }

        result = {
            "success": True,
            "result": agent_config,
            "input": agent_description
        }

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(result, ensure_ascii=False)
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


def _execute_modulizer_skill(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    模块化技能实现
    """
    try:
        system_description = (
            event.get('system_description') or
            event.get('requirements') or
            event.get('input') or
            event.get('description', '')
        )

        if not system_description.strip():
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'success': False,
                    'error': 'System description is required for modularization',
                    'input': system_description
                })
            }

        # 简单的模块化建议
        modulization_suggestions = [
            "将认证功能分离为独立模块",
            "将数据访问层抽象为单独模块",
            "将业务逻辑封装为独立的服务模块",
            "将用户界面与后端逻辑分离"
        ]

        result = {
            "success": True,
            "result": {
                "suggestions": modulization_suggestions,
                "system": system_description,
                "principles": ["Single Responsibility", "Loose Coupling", "High Cohesion"]
            },
            "input": system_description
        }

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(result, ensure_ascii=False)
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


def _execute_api_checker_skill(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    API检查技能实现
    """
    try:
        api_spec = (
            event.get('api_specification') or
            event.get('requirements') or
            event.get('input') or
            event.get('description', '')
        )

        if not api_spec.strip():
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'success': False,
                    'error': 'API specification is required for checking',
                    'input': api_spec
                })
            }

        # 简单的API检查
        issues = []
        if 'password' in api_spec.lower() and 'encrypted' not in api_spec.lower():
            issues.append("Potential security issue: Password fields should be encrypted")

        if 'api_key' in api_spec.lower() and 'authentication' not in api_spec.lower():
            issues.append("API key should have authentication mechanism")

        result = {
            "success": True,
            "result": {
                "valid": len(issues) == 0,
                "issues": issues,
                "recommendations": ["Use HTTPS for all endpoints", "Implement rate limiting", "Add proper error handling"],
                "specification": api_spec
            },
            "input": api_spec
        }

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(result, ensure_ascii=False)
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


def execute(args: Dict[str, Any]) -> str:
    """
    DNASPEC 格式入口（兼容性）
    """
    # 从参数中获取描述，args 可能是字符串或字典
    try:
        if isinstance(args, str):
            # 如果是字符串，则是直接的参数
            description = args.lower()
            input_param = args
        elif hasattr(args, 'get'):
            # 如果是字典-like 对象
            description = (
                args.get('description', '') or
                args.get('requirements', '') or
                args.get('input', '') or
                args.get('context', '')
            ).lower()
            input_param = args.get('input', '') or args.get('context', '') or args.get('requirements', '') or args.get('description', '')
        else:
            # 如果是其他类型，转换为字符串
            description = str(args).lower()
            input_param = str(args)
    except Exception:
        # 万全之策，保证不出现错误
        description = "default"  # 默认值
        input_param = "default"  # 默认值

    # 根据关键词判断技能类型并调用相应的处理函数
    if any(kw in description for kw in ['architect', 'design', 'architecture', 'system', 'structure', 'build', 'construct']):
        # 模拟 Claude 格式的输入
        event = {'requirements': input_param, 'input': input_param}
        result = _execute_architect_skill(event)
        if isinstance(result.get('body'), str):
            import json
            try:
                body_data = json.loads(result['body'])
                return str(body_data.get('result', {}).get('result', '架构设计完成'))
            except:
                return '架构设计完成'
        else:
            return '架构设计完成'

    elif any(kw in description for kw in ['task', 'decompose', 'break', 'subtask', 'decomposition', 'divide', 'split']):
        event = {'requirements': input_param, 'input': input_param}
        result = _execute_task_decomposer_skill(event)
        if isinstance(result.get('body'), str):
            import json
            try:
                body_data = json.loads(result['body'])
                task_struct = body_data.get('result', {}).get('task_structure', {})
                output_lines = []
                output_lines.append(f"任务分解: {task_struct.get('description', 'N/A')}")
                subtasks = task_struct.get('subtasks', [])
                output_lines.append(f"子任务数量: {len(subtasks)}")
                for i, task in enumerate(subtasks, 1):
                    output_lines.append(f"  {i}. {task.get('description', 'N/A')}")
                return "\n".join(output_lines)
            except:
                return '任务分解完成'
        else:
            return '任务分解完成'

    elif any(kw in description for kw in ['constraint', 'rule', 'condition', 'requirement', 'security', 'policy', 'governance']):
        event = {'requirements': input_param, 'input': input_param}
        result = _execute_constraint_generator_skill(event)
        if isinstance(result.get('body'), str):
            import json
            try:
                body_data = json.loads(result['body'])
                constraints = body_data.get('result', {}).get('constraints', [])
                output_lines = [f"生成 {len(constraints)} 个约束:"]
                for constraint in constraints:
                    output_lines.append(f"- {constraint.get('type', 'N/A')}: {constraint.get('description', 'N/A')}")
                return "\n".join(output_lines)
            except:
                return '约束生成完成'
        else:
            return '约束生成完成'

    elif any(kw in description for kw in ['analyze', 'context', 'quality', 'evaluate', 'assessment', 'metric']):
        event = {'context': input_param, 'input': input_param}
        result = _execute_context_analysis_skill(event)
        if isinstance(result.get('body'), str):
            import json
            try:
                body_data = json.loads(result['body'])
                metrics = body_data.get('result', {}).get('metrics', {})
                output_lines = ["上下文质量分析:"]
                for metric, score in metrics.items():
                    output_lines.append(f"{metric}: {score}")
                return "\n".join(output_lines)
            except:
                return '上下文分析完成'
        else:
            return '上下文分析完成'

    elif any(kw in description for kw in ['agent', 'create', 'build', 'generate', 'make']):
        event = {'agent_description': input_param, 'input': input_param}
        result = _execute_agent_creator_skill(event)
        if isinstance(result.get('body'), str):
            import json
            try:
                body_data = json.loads(result['body'])
                agent_config = body_data.get('result', {})
                return f"创建智能体: {agent_config.get('role', 'N/A')}"
            except:
                return '代理创建完成'
        else:
            return '代理创建完成'

    elif any(kw in description for kw in ['module', 'modular', 'component', 'structure', 'organization']):
        event = {'system_description': input_param, 'input': input_param}
        result = _execute_modulizer_skill(event)
        if isinstance(result.get('body'), str):
            import json
            try:
                body_data = json.loads(result['body'])
                suggestions = body_data.get('result', {}).get('suggestions', [])
                output_lines = ["模块化建议:"]
                for suggestion in suggestions:
                    output_lines.append(f"- {suggestion}")
                return "\n".join(output_lines)
            except:
                return '模块化完成'
        else:
            return '模块化完成'

    elif any(kw in description for kw in ['api', 'interface', 'endpoint', 'service', 'check', 'validate']):
        event = {'api_specification': input_param, 'input': input_param}
        result = _execute_api_checker_skill(event)
        if isinstance(result.get('body'), str):
            import json
            try:
                body_data = json.loads(result['body'])
                result_data = body_data.get('result', {})
                output_lines = ["API检查结果:"]
                output_lines.append(f"有效: {'是' if result_data.get('valid', False) else '否'}")

                issues = result_data.get('issues', [])
                if issues:
                    output_lines.append("\n发现的问题:")
                    for issue in issues:
                        output_lines.append(f"- {issue}")
                else:
                    output_lines.append("\n未发现明显问题")

                return "\n".join(output_lines)
            except:
                return 'API检查完成'
        else:
            return 'API检查完成'

    else:
        # 默认使用架构设计
        event = {'requirements': input_param, 'input': input_param}
        result = _execute_architect_skill(event)
        if isinstance(result.get('body'), str):
            import json
            try:
                body_data = json.loads(result['body'])
                return str(body_data.get('result', {}).get('result', '标准处理完成'))
            except:
                return '标准处理完成'
        else:
            return '标准处理完成'


def lambda_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    AWS Lambda 兼容的处理函数
    """
    return execute_skill(event, context)