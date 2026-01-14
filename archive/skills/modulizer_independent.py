"""
独立模块化技能 - 简化版本
基于DNASPEC标准化技能接口规范
"""
from typing import Dict, Any, List
import re


def execute_modulizer(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行模块化技能

    Args:
        args: 包含输入参数的字典
            - context: 系统架构描述

    Returns:
        执行结果字典
    """
    context = args.get('context', '')

    # 如果没有提供上下文，返回帮助信息
    if not context.strip():
        return {
            'success': False,
            'error': '请提供系统架构描述',
            'usage': '/dnaspec.modulizer "系统架构"'
        }

    # 生成模块化方案
    modularization_plan = generate_simple_modularization_plan(context)

    return {
        'success': True,
        'result': modularization_plan,
        'context': context
    }


def generate_simple_modularization_plan(context: str) -> Dict[str, Any]:
    """
    生成简化的模块化方案
    """
    # 识别系统组件
    components = identify_simple_components(context)

    # 设计模块结构
    modules = design_simple_modules(components)

    # 生成接口定义
    interfaces = define_simple_interfaces(modules)

    # 确定依赖关系
    dependencies = identify_simple_dependencies(modules)

    return {
        'system_overview': context.strip(),
        'components': components,
        'modules': modules,
        'interfaces': interfaces,
        'dependencies': dependencies,
        'modularization_principles': [
            '高内聚，低耦合',
            '单一职责原则',
            '模块化设计',
            '可重用性'
        ]
    }


def identify_simple_components(context: str) -> List[Dict[str, Any]]:
    """识别系统组件"""
    components = []
    context_lower = context.lower()

    # 简单的组件识别模式
    component_patterns = {
        '用户管理': ['用户', 'user', '认证', 'authentication'],
        '数据处理': ['数据', 'data', '处理', 'processing'],
        '存储': ['存储', 'storage', '数据库', 'database'],
        '接口': ['接口', 'interface', 'api', 'service'],
        '业务逻辑': ['业务', 'business', '逻辑', 'logic'],
        '前端': ['前端', 'frontend', 'ui', '界面'],
        '后端': ['后端', 'backend', '服务端', 'server'],
        '安全': ['安全', 'security', '验证', 'validation']
    }

    for component_name, keywords in component_patterns.items():
        if any(keyword in context_lower for keyword in keywords):
            components.append({
                'name': component_name,
                'description': f'负责{component_name}相关功能',
                'type': infer_component_type(component_name)
            })

    # 如果没有识别到组件，添加通用组件
    if not components:
        components = [
            {
                'name': '核心模块',
                'description': '处理核心业务功能',
                'type': 'core'
            },
            {
                'name': '接口模块',
                'description': '处理外部通信',
                'type': 'interface'
            }
        ]

    return components


def infer_component_type(component_name: str) -> str:
    """推断组件类型"""
    type_mapping = {
        '用户管理': 'business',
        '数据处理': 'processing',
        '存储': 'infrastructure',
        '接口': 'interface',
        '业务逻辑': 'business',
        '前端': 'presentation',
        '后端': 'application',
        '安全': 'crosscutting'
    }
    return type_mapping.get(component_name, 'generic')


def design_simple_modules(components: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """设计简化的模块结构"""
    modules = []

    # 按类型分组组件创建模块
    type_groups = {}
    for component in components:
        comp_type = component['type']
        if comp_type not in type_groups:
            type_groups[comp_type] = []
        type_groups[comp_type].append(component)

    for module_type, comp_list in type_groups.items():
        if comp_list:  # 只包含非空类型
            modules.append({
                'name': f"{module_type.title()}模块",
                'type': module_type,
                'components': [c['name'] for c in comp_list],
                'description': f"处理{module_type}相关的所有功能",
                'responsibility': f"协调和管理{module_type}组件"
            })

    return modules


def define_simple_interfaces(modules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """定义简化的模块接口"""
    interfaces = []

    for module in modules:
        interfaces.append({
            'module_name': module['name'],
            'interface_type': 'rest_api',
            'methods': [
                {'name': 'process', 'description': '处理主要功能'},
                {'name': 'get_status', 'description': '获取状态信息'}
            ],
            'data_format': 'json'
        })

    return interfaces


def identify_simple_dependencies(modules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """识别简化的依赖关系"""
    dependencies = []

    # 简单的依赖规则
    for i, module in enumerate(modules):
        for j, other_module in enumerate(modules):
            if i != j and has_simple_dependency(module, other_module):
                dependencies.append({
                    'source': module['name'],
                    'target': other_module['name'],
                    'type': 'functional_dependency',
                    'description': f"{module['name']}依赖于{other_module['name']}"
                })

    return dependencies


def has_simple_dependency(module1: Dict[str, Any], module2: Dict[str, Any]) -> bool:
    """判断是否存在简单依赖关系"""
    type1 = module1['type']
    type2 = module2['type']

    # 基本依赖规则
    dependency_rules = {
        ('presentation', 'interface'): True,
        ('interface', 'business'): True,
        ('business', 'processing'): True,
        ('business', 'infrastructure'): True,
        ('processing', 'infrastructure'): True,
    }

    return (type1, type2) in dependency_rules