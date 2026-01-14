"""
独立智能体创建技能 - 简化版本
基于DNASPEC标准化技能接口规范
"""
from typing import Dict, Any, List


def execute_agent_creator(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行智能体创建技能

    Args:
        args: 包含输入参数的字典
            - context: 智能体需求描述

    Returns:
        执行结果字典
    """
    context = args.get('context', '')

    # 如果没有提供上下文，返回帮助信息
    if not context.strip():
        return {
            'success': False,
            'error': '请提供智能体需求描述',
            'usage': '/dnaspec.agent-creator "智能体需求描述"'
        }

    # 生成智能体配置
    agent_config = generate_simple_agent_config(context)

    return {
        'success': True,
        'result': agent_config,
        'context': context
    }


def generate_simple_agent_config(context: str) -> Dict[str, Any]:
    """
    生成简化的智能体配置
    """
    # 从上下文推断智能体类型和特性
    agent_type = infer_agent_type(context)
    capabilities = infer_capabilities(context)
    tools = infer_tools(context)
    personality = infer_personality(context)
    specialization = infer_specialization(context)

    # 基础配置
    config = {
        'name': generate_simple_agent_name(context),
        'type': agent_type,
        'description': context.strip(),
        'system_prompt': f"你是一个专业的{agent_type}。你的主要职责是：{context.strip()}。请始终提供准确、有帮助且负责任的回应。",
        'capabilities': capabilities,
        'tools': tools,
        'personality': personality,
        'specialization': specialization
    }

    return config


def infer_agent_type(context: str) -> str:
    """从上下文推断智能体类型"""
    context_lower = context.lower()

    if any(word in context_lower for word in ['分析', '数据', 'data', 'analyze']):
        return 'analyst'
    elif any(word in context_lower for word in ['开发', '代码', 'programming', 'code', 'developer']):
        return 'developer'
    elif any(word in context_lower for word in ['研究', 'research', '调查', '学术']):
        return 'researcher'
    else:
        return 'assistant'


def infer_capabilities(context: str) -> List[str]:
    """从上下文推断能力"""
    capabilities = []
    context_lower = context.lower()

    if any(word in context_lower for word in ['分析', 'analyze', '数据', 'data']):
        capabilities.append('数据分析')
    if any(word in context_lower for word in ['开发', 'code', '编程']):
        capabilities.append('编程开发')
    if any(word in context_lower for word in ['设计', 'design', '架构']):
        capabilities.append('系统设计')
    if any(word in context_lower for word in ['研究', 'research']):
        capabilities.append('研究分析')
    if any(word in context_lower for word in ['协助', 'assist', '帮助']):
        capabilities.append('任务协助')

    return capabilities if capabilities else ['通用任务处理']


def infer_tools(context: str) -> List[str]:
    """从上下文推断工具"""
    tools = []
    context_lower = context.lower()

    if any(word in context_lower for word in ['代码', 'code', '编程']):
        tools.append('代码编辑器')
    if any(word in context_lower for word in ['数据', 'data', '分析']):
        tools.append('数据分析工具')
    if any(word in context_lower for word in ['研究', 'research']):
        tools.append('学术数据库')

    return tools if tools else ['文本编辑器']


def infer_personality(context: str) -> str:
    """从上下文推断性格特征"""
    context_lower = context.lower()

    if any(word in context_lower for word in ['分析', '逻辑']):
        return '分析性、严谨'
    elif any(word in context_lower for word in ['开发', '创新', '技术']):
        return '创新、务实'
    elif any(word in context_lower for word in ['研究', '细致', '深入']):
        return '细致、探究精神'
    else:
        return '友好、专业'


def infer_specialization(context: str) -> str:
    """从上下文推断专业领域"""
    context_lower = context.lower()

    if any(word in context_lower for word in ['商业', 'business', '市场']):
        return '商业分析'
    elif any(word in context_lower for word in ['技术', 'technology', '软件']):
        return '软件开发'
    elif any(word in context_lower for word in ['数据', 'data', '分析']):
        return '数据分析'
    elif any(word in context_lower for word in ['学术', 'academic', '研究']):
        return '学术研究'
    else:
        return '通用问题解决'


def generate_simple_agent_name(context: str) -> str:
    """生成简单的智能体名称"""
    context_lower = context.lower()

    if '数据' in context_lower or 'data' in context_lower:
        return '数据分析师'
    elif '开发' in context_lower or 'code' in context_lower:
        return '开发工程师'
    elif '研究' in context_lower or 'research' in context_lower:
        return '研究专家'
    else:
        return '智能助手'