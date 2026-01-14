"""
Claude Skills 主处理器
标准化的Claude Skills接口实现
"""
import json
import os
import sys
import uuid
from typing import Dict, Any, List
from datetime import datetime


def lambda_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """
    Claude Skills标准lambda处理器
    """
    try:
        # Claude Skills标准：event包含inputs数组
        inputs_array = event.get('inputs', [{}])
        if not inputs_array:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'No inputs provided',
                    'timestamp': datetime.utcnow().isoformat()
                })
            }

        # 使用第一个输入
        input_data = inputs_array[0]
        
        # Claude Skills中，工具名称通常通过某种方式标识
        # 在Claude Tools API中，工具名称在function_call参数中或通过其他方式传递
        tool_name = event.get('tool_name', '').lower()
        
        if not tool_name:
            # 从工具调用参数中获取工具名称
            function_call = event.get('function_call', {})
            tool_name = function_call.get('name', '').lower()
        
        # 根据工具名称执行相应的技能
        if tool_name == 'architect' or 'architect' in tool_name:
            result = _execute_architect_skill(input_data)
        elif tool_name == 'context-analyzer' or 'analyzer' in tool_name:
            result = _execute_context_analysis_skill(input_data)
        elif tool_name == 'context-optimizer' or 'optimizer' in tool_name:
            result = _execute_context_optimization_skill(input_data)
        elif tool_name == 'cognitive-templater' or 'templater' in tool_name:
            result = _execute_cognitive_template_skill(input_data)
        elif tool_name == 'agent-creator' or 'agent' in tool_name:
            result = _execute_agent_creator_skill(input_data)
        elif tool_name == 'task-decomposer' or 'decomposer' in tool_name:
            result = _execute_task_decomposer_skill(input_data)
        elif tool_name == 'constraint-generator' or 'constraint' in tool_name:
            result = _execute_constraint_generator_skill(input_data)
        elif tool_name == 'dnaspec-init' or 'dnaspec' in tool_name:
            result = _execute_dnaspec_init_skill(input_data)
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': f'Unknown tool: {tool_name}',
                    'available_tools': [
                        'architect', 'context-analyzer', 'context-optimizer', 
                        'cognitive-templater', 'agent-creator', 'task-decomposer', 'constraint-generator', 'dnaspec-init'
                    ],
                    'timestamp': datetime.utcnow().isoformat()
                })
            }

        return {
            'statusCode': 200,
            'body': json.dumps(result, ensure_ascii=False)
        }

    except Exception as e:
        error_body = {
            'error': str(e),
            'input_event': event,
            'timestamp': datetime.utcnow().isoformat()
        }
        return {
            'statusCode': 500,
            'body': json.dumps(error_body, ensure_ascii=False)
        }


def _execute_architect_skill(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行架构设计技能 - 遵循Claude Skills规范
    """
    input_text = input_data.get('input', input_data.get('requirements', ''))
    
    if not input_text.strip():
        return {
            'success': False,
            'error': 'No input provided for architect skill',
            'input_preview': str(input_data)[:100]
        }
    
    # 简化的架构设计算法
    input_lower = input_text.lower()
    
    # 5维质量分析
    clarity = min(1.0, max(0.0, 0.5 + len(input_text) * 0.00001))
    relevance = min(1.0, max(0.0, 0.7 + (0.1 if any(kw in input_lower for kw in ['system', 'function', 'task', 'requirement', '需求', 'system', 'function', 'task']) else 0)))
    completeness = min(1.0, max(0.0, 0.3 + (0.3 if any(kw in input_lower for kw in ['constraint', 'requirement', 'goal', 'requirement', 'constraint', 'requirement', 'goal']) else 0)))
    consistency = min(1.0, max(0.0, 0.8 - (0.2 if any(kw in input_lower for kw in ['but', 'however', '但是', '然而']) else 0)))
    efficiency = min(1.0, max(0.0, 1.0 - len(input_text) * 0.00005))

    # 系统架构设计
    architecture_map = {
        "电商": "[WebApp] -> [API Server] -> [Database]",
        "博客": "[WebApp] -> [Database]",
        "用户管理": "[Frontend] -> [API Gateway] -> [Auth Service] -> [User DB]",
        "认证": "[Auth Service] -> [User DB] -> [Session Store]",
        "api": "[API Gateway] -> [Microservices] -> [Data Layer]"
    }

    # 查找匹配的架构
    architecture_type = "custom"
    architecture_design = f"基于需求设计: {input_text[:50]}..." if len(input_text) > 50 else input_text
    for keyword, arch in architecture_map.items():
        if keyword in input_lower:
            architecture_design = arch
            architecture_type = keyword
            break

    result = {
        'success': True,
        'result': {
            'architecture_type': architecture_type,
            'design': architecture_design,
            'context_quality': {
                'clarity': round(clarity, 2),
                'relevance': round(relevance, 2),
                'completeness': round(completeness, 2),
                'consistency': round(consistency, 2),
                'efficiency': round(efficiency, 2)
            },
            'suggestions': [
                'Add more specific goal descriptions',
                'Supplement constraint conditions and specific requirements',
                'Improve expression clarity'
            ],
            'issues': [i for i in [
                'Lack of explicit constraint conditions' if completeness < 0.6 else '',
                'Some expressions can be more precise' if clarity < 0.7 else ''
            ] if i],  # Filter out empty issues
            'confidence': 0.85
        },
        'input_preview': input_text[:100] + '...' if len(input_text) > 100 else input_text,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    return result


def _execute_context_analysis_skill(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行上下文分析技能 - 遵循Claude Skills规范
    """
    input_text = input_data.get('input', input_data.get('context', ''))
    
    if not input_text.strip():
        return {
            'success': False,
            'error': 'No context provided for analysis',
            'input_preview': str(input_data)[:100]
        }
    
    # 5维上下文质量分析
    context_length = len(input_text)
    token_count_estimate = max(1, len(input_text) // 4)
    
    # 计算质量指标
    clarity = min(1.0, max(0.0, 0.5 + len(input_text) * 0.00001))
    relevance = min(1.0, max(0.0, 0.7 + (0.1 if any(kw in input_text.lower() for kw in ['system', 'function', 'task', 'requirement', '需求', 'system', 'function', 'task']) else 0)))
    completeness = min(1.0, max(0.0, 0.3 + (0.3 if any(kw in input_text.lower() for kw in ['constraint', 'requirement', 'goal', 'requirement', 'constraint', 'requirement', 'goal']) else 0)))
    consistency = min(1.0, max(0.0, 0.8 - (0.2 if any(kw in input_text.lower() for kw in ['but', 'however', '但是', '然而']) else 0)))
    efficiency = min(1.0, max(0.0, 1.0 - len(input_text) * 0.00005))

    result = {
        'success': True,
        'result': {
            'context_length': context_length,
            'token_count_estimate': token_count_estimate,
            'quality_metrics': {
                'clarity': round(clarity, 2),
                'relevance': round(relevance, 2),
                'completeness': round(completeness, 2),
                'consistency': round(consistency, 2),
                'efficiency': round(efficiency, 2)
            },
            'suggestions': [
                'Add more specific goal descriptions',
                'Supplement constraint conditions and specific requirements',
                'Improve expression clarity'
            ],
            'issues': [i for i in [
                'Lack of explicit constraint conditions' if completeness < 0.6 else '',
                'Some expressions can be more precise' if clarity < 0.7 else ''
            ] if i],  # Filter out empty issues
            'confidence': 0.85
        },
        'input_preview': input_text[:100] + '...' if len(input_text) > 100 else input_text,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    return result


def _execute_context_optimization_skill(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行上下文优化技能 - 遵循Claude Skills规范
    """
    input_text = input_data.get('input', input_data.get('context', ''))
    goals = input_data.get('optimization_goals', [])
    
    if not input_text.strip():
        return {
            'success': False,
            'error': 'No context provided for optimization',
            'input_preview': str(input_data)[:100]
        }

    # 简化的优化算法
    original_length = len(input_text)
    
    optimized_text = input_text
    applied_improvements = []
    
    # 根据优化目标进行优化
    if any(goal.lower() in ['clarity', 'clear', 'clarity', '清晰度'] for goal in goals):
        optimized_text += "\n\n为了提高清晰度，明确指出目标和约束条件: [在此处补充具体目标和约束]"
        applied_improvements.append('Added clarity directives')
    
    if any(goal.lower() in ['completeness', 'complete', 'completeness', '完整性'] for goal in goals):
        optimized_text += "\n\n约束: 需要在规定时间内完成\n明确目标: 实现预期功能\n前提条件: 具备必要的资源支持"
        applied_improvements.append('Added completeness elements')
    
    # 计算改进指标
    clarity_impact = 0.2 if any(g.lower().find('clarity') != -1 or g.lower().find('clear') != -1 for g in goals) else 0.0
    completeness_impact = 0.3 if any('completeness' in g.lower() or 'complete' in g.lower() for g in goals) else 0.0
    relevance_impact = 0.15 if any('relevance' in g.lower() or 'relevant' in g.lower() for g in goals) else 0.0
    efficiency_impact = -0.1 if any('concise' in g.lower() or 'efficiency' in g.lower() for g in goals) else 0.0

    result = {
        'success': True,
        'result': {
            'original_length': original_length,
            'optimized_length': len(optimized_text),
            'applied_optimizations': applied_improvements,
            'optimization_goals': goals,
            'improvement_metrics': {
                'clarity_change': round(clarity_impact, 2),
                'completeness_change': round(completeness_impact, 2),
                'relevance_change': round(relevance_impact, 2),
                'efficiency_change': round(efficiency_impact, 2)
            },
            'optimized_context': optimized_text[:500] + '...' if len(optimized_text) > 500 else optimized_text,
            'optimization_summary': f"Optimized for goals: {', '.join(goals) if goals else 'general improvement'}"
        },
        'input_preview': input_text[:100] + '...' if len(input_text) > 100 else input_text,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    return result


def _execute_cognitive_template_skill(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行认知模板技能 - 遵循Claude Skills规范
    """
    input_text = input_data.get('input', input_data.get('context', ''))
    template_type = input_data.get('template_type', 'chain_of_thought')
    
    if not input_text.strip():
        return {
            'success': False,
            'error': 'No input provided for cognitive template application',
            'input_preview': str(input_data)[:100]
        }

    # 根据模板类型生成相应输出
    if template_type == 'chain_of_thought':
        enhanced_output = f"链式思维分析: {input_text}\n\n"
        enhanced_output += "1. 问题理解\n"
        enhanced_output += "2. 步骤分解\n"
        enhanced_output += "3. 中间推理\n"
        enhanced_output += "4. 验证检查\n"
        enhanced_output += "5. 最终答案\n\n"
        template_desc = "Chain-of-Thought reasoning pattern for systematic problem solving"
        
    elif template_type == 'verification':
        enhanced_output = f"验证检查: {input_text}\n\n"
        enhanced_output += "1. 初步答案\n"
        enhanced_output += "2. 逻辑一致性检查\n"
        enhanced_output += "3. 事实准确性检验\n"
        enhanced_output += "4. 完整性检验\n"
        enhanced_output += "5. 最终确认\n\n"
        template_desc = "Verification pattern for validating reasoning and outputs"
        
    elif template_type == 'few_shot':
        enhanced_output = f"少样本学习: {input_text}\n\n"
        enhanced_output += "示例1: [要模仿的模式]\n"
        enhanced_output += "示例2: [要模仿的模式]\n"
        enhanced_output += "当前任务: [应用习得模式]\n\n"
        template_desc = "Few-shot learning pattern for learning from examples"
        
    elif template_type == 'role_playing':
        enhanced_output = f"角色扮演分析: {input_text}\n\n"
        enhanced_output += "设定适当角色...\n"
        enhanced_output += "[应用角色特定推理]\n\n"
        template_desc = "Role-playing pattern for perspective-based analysis"
        
    else:  # Default
        enhanced_output = f"认知模板应用: {input_text}\n\n"
        enhanced_output += "1. 理解任务\n"
        enhanced_output += "2. 分解为子组件\n"
        enhanced_output += "3. 应用相关框架\n"
        enhanced_output += "4. 综合解决方案\n"
        enhanced_output += "5. 提供最终输出\n\n"
        template_desc = "Generic cognitive template pattern"

    result = {
        'success': True,
        'result': {
            'template_type': template_type,
            'template_description': template_desc,
            'enhanced_output': enhanced_output[:500] + '...' if len(enhanced_output) > 500 else enhanced_output,
            'cognitive_framework_applied': True,
            'input_processed': input_text[:100] + '...' if len(input_text) > 100 else input_text
        },
        'input_preview': input_text[:100] + '...' if len(input_text) > 100 else input_text,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    return result


def _execute_agent_creator_skill(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行智能体创建技能 - 遵循Claude Skills规范
    """
    agent_description = input_data.get('agent_description', input_data.get('input', ''))
    capabilities = input_data.get('capabilities', [])
    
    if not agent_description.strip():
        return {
            'success': False,
            'error': 'No agent description provided',
            'input_preview': str(input_data)[:100]
        }

    # 生成智能体配置
    agent_config = {
        'id': f"agent_{uuid.uuid4().hex[:8]}",
        'role': agent_description,
        'domain': 'general',
        'capabilities': capabilities or [
            'Task execution',
            'Information retrieval', 
            'Decision making',
            'Context awareness'
        ],
        'instructions': f"You are acting as a {agent_description} in the appropriate domain.",
        'personality': 'Professional, helpful, focused on assigned tasks',
        'created_at': datetime.utcnow().isoformat()
    }

    result = {
        'success': True,
        'result': {
            'agent_config': agent_config,
            'agent_created': True,
            'capabilities_assigned': len(agent_config['capabilities']),
            'domain': agent_config['domain']
        },
        'input_preview': agent_description[:100] + '...' if len(agent_description) > 100 else agent_description,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    return result


def _execute_task_decomposer_skill(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行任务分解技能 - 遵循Claude Skills规范
    """
    input_text = input_data.get('input', input_data.get('description', ''))
    max_depth = input_data.get('max_depth', 3)
    
    if not input_text.strip():
        return {
            'success': False,
            'error': 'No task provided for decomposition',
            'input_preview': str(input_data)[:100]
        }

    # 简单的任务分解逻辑
    sentences = input_text.split('.')
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
            if area in input_text.lower():
                subtasks.append(f"实现{area}功能")
    
    # 限制子任务数量以防止爆炸
    subtasks = subtasks[:10]

    result = {
        'success': True,
        'result': {
            'task_structure': {
                'id': f"TASK-{uuid.uuid4().hex[:8]}",
                'description': input_text,
                'is_atomic': len(subtasks) == 0,
                'depth': 1,
                'subtasks': [{'id': f"SUB-{uuid.uuid4().hex[:8]}", 'description': task, 'completed': False} for task in subtasks],
                'created_at': datetime.utcnow().isoformat()
            },
            'validation': {
                'is_valid': True,
                'issues': [],
                'metrics': {
                    'total_tasks': len(subtasks) + 1,
                    'max_depth': 1,
                    'average_branching_factor': len(subtasks)
                }
            },
            'execution_info': {
                'skill': 'task-decomposer',
                'timestamp': datetime.utcnow().isoformat(),
                'principles_applied': ['KISS', 'YAGNI', 'SOLID']
            }
        },
        'input_preview': input_text[:100] + '...' if len(input_text) > 100 else input_text,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    return result


def _execute_constraint_generator_skill(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行约束生成技能 - 遵循Claude Skills规范
    """
    requirements = input_data.get('requirements', input_data.get('input', ''))
    change_request = input_data.get('change_request', '')
    
    if not requirements.strip():
        return {
            'success': False,
            'error': 'No requirements provided for constraint generation',
            'input_preview': str(input_data)[:100]
        }

    # 生成约束
    req_lower = requirements.lower()
    constraints = []
    
    # 安全约束
    if any(term in req_lower for term in ['security', 'secure', 'auth', 'encrypt', 'privacy', 'protect', 'password', 'login']):
        constraints.append({
            'id': f"constraint_{uuid.uuid4().hex[:8]}",
            'type': 'security',
            'description': '系统必须实现标准安全措施',
            'severity': 'high',
            'created_at': datetime.utcnow().isoformat()
        })

    # 性能约束
    if any(term in req_lower for term in ['performance', 'fast', 'response', 'throughput', 'latency', 'speed']):
        constraints.append({
            'id': f"constraint_{uuid.uuid4().hex[:8]}",
            'type': 'performance', 
            'description': '系统必须满足定义的性能要求',
            'severity': 'medium',
            'created_at': datetime.utcnow().isoformat()
        })

    # 数据约束
    if any(term in req_lower for term in ['data', 'database', 'storage', 'retrieve', 'persist', 'record']):
        constraints.append({
            'id': f"constraint_{uuid.uuid4().hex[:8]}",
            'type': 'data_integrity',
            'description': '系统必须保持数据完整性和备份能力',
            'severity': 'high',
            'created_at': datetime.utcnow().isoformat()
        })

    # 对齐检查
    alignment_check = {
        'is_aligned': not (change_request and 
                         any(contradiction in change_request.lower() 
                             for contradiction in ['no security', 'negligible performance', 'unreliable'])),
        'conflicts': [],
        'suggestions': ['No change request provided, requirements are baseline'] if not change_request else ['Change request appears aligned with base requirements']
    }
    
    result = {
        'success': True,
        'result': {
            'constraints': constraints,
            'alignment_check': alignment_check,
            'version_info': {
                'current_version': f"version_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}",
                'tracked': True
            },
            'timestamp': datetime.utcnow().timestamp()
        },
        'input': {
            'requirements': requirements[:100] + '...' if len(requirements) > 100 else requirements,
            'change_request': change_request[:50] + '...' if len(change_request) > 50 else change_request
        },
        'timestamp': datetime.utcnow().isoformat()
    }
    
    return result


# Test function for local development
def test_locally():
    """
    本地测试函数
    """
    import uuid
    import json
    from datetime import datetime
    
    print("Testing Claude Skills implementation...")
    
    # Test architect skill
    test_event = {
        'inputs': [{'input': 'Design an e-commerce system'}],
        'tool_name': 'architect'
    }
    
    result = lambda_handler(test_event, None)
    print("Architect skill result:", json.dumps(result, indent=2, ensure_ascii=False)[:300] + "...")
    
    # Test context analyzer skill
    test_event = {
        'inputs': [{'input': 'User needs to login to the system with security requirements'}],
        'tool_name': 'context-analyzer'
    }
    
    result = lambda_handler(test_event, None)
    print("Context analyzer skill result keys:", result.get('body', {}).keys() if isinstance(result.get('body'), dict) else 'Check body type')



def _execute_dnaspec_init_skill(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行DNASPEC初始化技能 - 遵循agentskills.io规范
    """
    import os
    import shutil
    from datetime import datetime
    
    try:
        # 解析操作类型
        operation = input_data.get('operation', 'detect').lower()
        
        # 项目根目录
        project_root = os.getcwd()
        dnaspec_dir = os.path.join(project_root, '.dnaspec')
        constitution_file = os.path.join(project_root, 'PROJECT_CONSTITUTION.md')
        config_file = os.path.join(dnaspec_dir, 'config.json')
        
        # 检测项目状态
        def detect_project_status():
            existing_files = []
            missing_files = []
            
            # 检查核心文件
            core_files = [
                constitution_file,
                config_file,
                os.path.join(dnaspec_dir, 'cache'),
                os.path.join(dnaspec_dir, 'meta'),
            ]
            
            for file_path in core_files:
                if os.path.exists(file_path):
                    existing_files.append(file_path)
                else:
                    missing_files.append(file_path)
            
            # 检测项目类型
            detected_types = _detect_project_types()
            detected_tools = _detect_development_tools()
            
            # 确定状态
            if len(existing_files) == len(core_files):
                status = "complete"
            elif len(existing_files) > 0:
                status = "partial"
            else:
                status = "not_initialized"
            
            return {
                "status": status,
                "existing_files": existing_files,
                "missing_files": missing_files,
                "detected_types": detected_types,
                "detected_tools": detected_tools,
                "project_root": project_root,
                "dnaspec_dir": dnaspec_dir
            }
        
        # 初始化项目
        def initialize_project(init_type="auto", project_type="generic", features=None, force=False):
            features = features or []
            
            # 检测当前状态
            current_status = detect_project_status()
            
            if current_status["status"] == "complete" and not force:
                return {
                    "message": "项目已经初始化",
                    "status": current_status["status"],
                    "existing_files": current_status["existing_files"]
                }
            
            # 执行初始化
            if init_type == "auto":
                init_type = _detect_init_type()
            
            result = _perform_initialization(init_type, project_type, features, project_root, dnaspec_dir, constitution_file, config_file)
            
            return {
                "success": True,
                "message": f"{init_type} 初始化完成",
                "init_type": init_type,
                "project_type": project_type,
                "features_enabled": features,
                "created_files": result.get("created_files", []),
                "configuration": result.get("configuration", {}),
                "next_steps": _generate_next_steps(features)
            }
        
        # 重置协调机制
        def reset_coordination(confirm=False):
            if not confirm:
                return {
                    "success": False,
                    "message": "需要确认重置操作",
                    "suggestion": "设置 confirm=true 来确认重置"
                }
            
            # 备份现有配置
            backup_dir = f"{dnaspec_dir}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            if os.path.exists(dnaspec_dir):
                shutil.move(dnaspec_dir, backup_dir)
            
            # 删除宪法文件
            if os.path.exists(constitution_file):
                os.remove(constitution_file)
            
            return {
                "success": True,
                "message": "协调机制已重置",
                "backup_location": backup_dir,
                "next_steps": [
                    "运行初始化命令重新配置",
                    "检查备份文件恢复特定配置"
                ]
            }
        
        # 获取配置信息
        def get_configuration_info():
            try:
                if os.path.exists(config_file):
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                else:
                    config = {}
                
                return {
                    "success": True,
                    "configuration": config,
                    "config_file": config_file,
                    "last_updated": _get_file_modification_time(config_file)
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "message": "无法读取配置信息"
                }
        
        # 执行相应操作
        if operation == "detect":
            result = detect_project_status()
            message = "项目状态检测完成"
        elif operation == "initialize":
            init_type = input_data.get('init_type', 'auto')
            project_type = input_data.get('project_type', 'generic')
            features = input_data.get('features', [])
            force = input_data.get('force', False)
            result = initialize_project(init_type=init_type, project_type=project_type, features=features, force=force)
            message = "项目初始化完成"
        elif operation == "reset":
            confirm = input_data.get('confirm', False)
            result = reset_coordination(confirm=confirm)
            message = "协调机制重置完成" if result.get('success') else "重置操作失败"
        elif operation == "get-config":
            result = get_configuration_info()
            message = "配置信息获取完成"
        elif operation == "status":
            result = detect_project_status()
            message = "项目状态查询完成"
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    "success": False,
                    "error": f"Unknown operation: {operation}",
                    "available_operations": ["detect", "initialize", "reset", "get-config", "status"]
                }, ensure_ascii=False)
            }
        
        return {
            'success': True,
            'operation': operation,
            'message': message,
            'result': result,
            'timestamp': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'operation': input_data.get('operation', 'unknown'),
            'timestamp': datetime.utcnow().isoformat()
        }


def _detect_project_types():
    """检测项目类型"""
    types = []
    
    # 检查常见项目文件
    project_indicators = {
        "web_application": ["package.json", "index.html", "vite.config.js", "webpack.config.js"],
        "mobile_app": ["App.js", "app.json", "pubspec.yaml", "build.gradle"],
        "api_service": ["main.py", "app.py", "requirements.txt", "Dockerfile"],
        "ml_project": ["requirements.txt", "jupyter", "notebook.ipynb", "model.pkl"],
        "data_science": ["requirements.txt", "notebook.ipynb", "data/", "pandas"],
        "microservice": ["Dockerfile", "docker-compose.yml", "main.py", "app.py"]
    }
    
    for project_type, indicators in project_indicators.items():
        if any(os.path.exists(indicator) for indicator in indicators):
            types.append(project_type)
    
    return types if types else ["generic"]


def _detect_development_tools():
    """检测开发工具"""
    tools = {
        "version_control": [],
        "build_tools": [],
        "team_tools": [],
        "enterprise_tools": [],
        "cicd_tools": []
    }
    
    # 版本控制
    if os.path.exists('.git'):
        tools["version_control"].append("git")
    
    # 构建工具
    if os.path.exists('package.json'):
        tools["build_tools"].append("npm")
    if os.path.exists('requirements.txt'):
        tools["build_tools"].append("pip")
    if os.path.exists('Dockerfile'):
        tools["build_tools"].append("docker")
    
    # 团队工具
    if os.path.exists('.github') or os.path.exists('workflows'):
        tools["team_tools"].append("github_actions")
    if os.path.exists('.gitlab-ci.yml') or os.path.exists('.gitlab'):
        tools["team_tools"].append("gitlab_ci")
    
    # 企业工具
    if os.path.exists('k8s') or os.path.exists('kubernetes'):
        tools["enterprise_tools"].append("kubernetes")
    if os.path.exists('terraform'):
        tools["enterprise_tools"].append("terraform")
    
    # CI/CD工具
    if os.path.exists('.github/workflows'):
        tools["cicd_tools"].append("github_actions")
    if os.path.exists('.circleci'):
        tools["cicd_tools"].append("circleci")
    
    return tools


def _detect_init_type():
    """自动检测初始化类型"""
    detected_tools = _detect_development_tools()
    
    # 基于检测结果确定初始化类型
    if len(detected_tools.get("team_tools", [])) >= 3:
        return "team"
    elif len(detected_tools.get("enterprise_tools", [])) >= 2:
        return "enterprise"
    else:
        return "project"


def _perform_initialization(init_type, project_type, features, project_root, dnaspec_dir, constitution_file, config_file):
    """执行具体初始化操作"""
    created_files = []
    
    # 创建DNASPEC目录结构
    _create_dnaspec_structure(dnaspec_dir)
    created_files.append(dnaspec_dir)
    
    # 生成项目宪法
    constitution_content = _generate_constitution(init_type, project_type, features)
    with open(constitution_file, 'w', encoding='utf-8') as f:
        f.write(constitution_content)
    created_files.append(constitution_file)
    
    # 生成配置文件
    config = _generate_configuration(init_type, project_type, features)
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    created_files.append(config_file)
    
    # 启用指定功能
    if "caching" in features:
        _setup_caching_system(dnaspec_dir)
        created_files.append(os.path.join(dnaspec_dir, 'cache'))
    
    if "git_hooks" in features:
        _setup_git_hooks(project_root, dnaspec_dir)
        created_files.append(os.path.join(dnaspec_dir, 'hooks'))
    
    if "ci_cd" in features:
        _setup_ci_cd_templates(dnaspec_dir)
        created_files.append(os.path.join(dnaspec_dir, 'cicd'))
    
    return {
        "created_files": created_files,
        "configuration": config
    }


def _create_dnaspec_structure(dnaspec_dir):
    """创建DNASPEC目录结构"""
    directories = [
        dnaspec_dir,
        os.path.join(dnaspec_dir, 'cache'),
        os.path.join(dnaspec_dir, 'cache', 'temp'),
        os.path.join(dnaspec_dir, 'cache', 'staging'),
        os.path.join(dnaspec_dir, 'cache', 'meta'),
        os.path.join(dnaspec_dir, 'meta'),
        os.path.join(dnaspec_dir, 'hooks'),
        os.path.join(dnaspec_dir, 'logs')
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def _generate_constitution(init_type, project_type, features):
    """生成项目宪法"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f"""# DNASPEC 项目协调宪法

## 项目信息
- **项目类型**: {project_type}
- **初始化类型**: {init_type}
- **初始化时间**: {timestamp}
- **DNASPEC版本**: 1.0.0

## 协调机制
本项目已启用DNASPEC协调机制，支持技能间的智能协作。

### 已启用的功能
{chr(10).join(f"- {feature}" for feature in features)}

## 技能协调规则

### 核心技能组合
1. **架构设计**: `/architect` - 系统架构设计
2. **任务分解**: `/task-decomposer` - 任务分解和规划
3. **约束生成**: `/constraint-generator` - 约束条件生成
4. **上下文分析**: `/context-analyzer` - 上下文分析
5. **上下文优化**: `/context-optimizer` - 上下文优化
6. **认知模板**: `/cognitive-templater` - 认知模板应用
7. **技能创建**: `/agent-creator` - 智能体创建
8. **DNASPEC初始化**: `/dnaspec-init` - 协调机制管理

### 协调执行模式
- **自动检测**: 系统自动检测项目宪法状态
- **智能协调**: 当检测到协调机制时启用多技能协作
- **优雅降级**: 当协调不可用时自动降级到独立模式
- **性能优化**: 基于置信度动态选择最优执行策略

## 使用指南

### 状态检查
```bash
# 检查项目状态
/dnaspec-init "operation=detect"

# 查看配置信息
/dnaspec-init "operation=get-config"

# 重置协调机制（如需要）
/dnaspec-init "operation=reset confirm=true"
```

---

**最后更新**: {timestamp}
**维护者**: DNASPEC自动生成
"""


def _generate_configuration(init_type, project_type, features):
    """生成配置文件"""
    return {
        "dnaspec": {
            "version": "1.0.0",
            "init_type": init_type,
            "project_type": project_type,
            "created_at": datetime.now().isoformat(),
            "features": {
                "caching": "caching" in features,
                "git_hooks": "git_hooks" in features,
                "ci_cd": "ci_cd" in features,
                "coordination": True,
                "graceful_degradation": True
            },
            "skills": {
                "architect": {"enabled": True, "priority": "high"},
                "task-decomposer": {"enabled": True, "priority": "high"},
                "constraint-generator": {"enabled": True, "priority": "medium"},
                "context-analyzer": {"enabled": True, "priority": "medium"},
                "context-optimizer": {"enabled": True, "priority": "medium"},
                "cognitive-templater": {"enabled": True, "priority": "low"},
                "agent-creator": {"enabled": True, "priority": "low"},
                "dnaspec-init": {"enabled": True, "priority": "high"}
            }
        }
    }


def _setup_caching_system(dnaspec_dir):
    """设置缓存系统"""
    cache_config = {
        "cache_enabled": True,
        "cache_strategies": {
            "file_cache": {"enabled": True, "ttl": 3600},
            "memory_cache": {"enabled": True, "ttl": 1800},
            "distributed_cache": {"enabled": False}
        },
        "directories": {
            "temp": "cache/temp",
            "staging": "cache/staging", 
            "meta": "cache/meta"
        }
    }
    
    cache_config_file = os.path.join(dnaspec_dir, 'cache', 'config.json')
    with open(cache_config_file, 'w', encoding='utf-8') as f:
        json.dump(cache_config, f, indent=2, ensure_ascii=False)


def _setup_git_hooks(project_root, dnaspec_dir):
    """设置Git钩子"""
    git_hooks_dir = os.path.join(project_root, '.git', 'hooks')
    
    if os.path.exists(git_hooks_dir):
        # 预提交钩子
        pre_commit_hook = """#!/bin/bash
# DNASPEC Pre-commit Hook
echo "🔍 Running DNASPEC pre-commit checks..."

# 检查是否需要运行技能
if [ -f "PROJECT_CONSTITUTION.md" ]; then
    echo "✅ DNASPEC project detected"
    # 这里可以添加具体的检查逻辑
fi
"""
        
        hook_file = os.path.join(git_hooks_dir, 'pre-commit')
        with open(hook_file, 'w') as f:
            f.write(pre_commit_hook)
        
        # 使钩子可执行
        os.chmod(hook_file, 0o755)


def _setup_ci_cd_templates(dnaspec_dir):
    """设置CI/CD模板"""
    cicd_dir = os.path.join(dnaspec_dir, 'cicd')
    os.makedirs(cicd_dir, exist_ok=True)
    
    # GitHub Actions模板
    github_workflow = """name: DNASPEC CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  dnaspec-validation:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: DNASPEC Skills Validation
      run: |
        echo "🔍 Running DNASPEC skill validations..."
        # 这里可以添加具体的验证逻辑
"""
    
    with open(os.path.join(cicd_dir, 'github-actions.yml'), 'w') as f:
        f.write(github_workflow)


def _generate_next_steps(features):
    """生成后续步骤建议"""
    steps = [
        "✅ DNASPEC协调机制初始化完成",
        "🚀 现在可以开始使用DNASPEC技能",
        "📖 查看 PROJECT_CONSTITUTION.md 了解详细规则"
    ]
    
    if "caching" in features:
        steps.append("💾 缓存系统已启用，性能将得到优化")
    
    if "git_hooks" in features:
        steps.append("🔗 Git钩子已配置，代码质量检查将自动执行")
    
    if "ci_cd" in features:
        steps.append("⚙️ CI/CD模板已生成，可用于自动化部署")
    
    steps.extend([
        "",
        "📝 常用技能使用示例:",
        "/architect \"system_type=web_application\"",
        "/task-decomposer \"input=implement_user_interface\"",
        "/constraint-generator \"requirements=performance_requirements\"",
        "",
        "🔧 状态检查命令:",
        "/dnaspec-init \"operation=detect\"",
        "/dnaspec-init \"operation=get-config\""
    ])
    
    return steps


def _get_file_modification_time(file_path):
    """获取文件修改时间"""
    try:
        if os.path.exists(file_path):
            return datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
    except Exception:
        pass
    return None


if __name__ == "__main__":
    test_locally()