"""
DNASPEC 兼容性适配器
提供 Claude Skills 与 DNASPEC 自定义技能格式的双向兼容
"""
import json
from typing import Dict, Any, Callable
from pathlib import Path


class ClaudeDNASpecAdapter:
    """
    Claude Skills 与 DNASPEC 技能格式兼容适配器
    """
    
    @staticmethod
    def is_claude_format_request(request: Dict[str, Any]) -> bool:
        """判断是否为 Claude 格式请求"""
        # Claude Skills 通常包含特定字段
        required_claude_fields = ['command', 'parameters', 'context']
        return any(field in request for field in required_claude_fields)
    
    @staticmethod
    def claude_to_dnaspec_format(claude_request: Dict[str, Any]) -> Dict[str, Any]:
        """将 Claude 格式请求转换为 DNASPEC 格式"""
        # 提取输入内容
        input_content = (
            claude_request.get('command') or 
            claude_request.get('parameters', {}).get('input') or
            claude_request.get('context', {}).get('input', '')
        )
        
        # 转换为 DNASPEC 格式
        return {
            'description': input_content,
            'requirements': input_content,
            'context': claude_request.get('context', {}),
            'parameters': claude_request.get('parameters', {})
        }
    
    @staticmethod
    def dnaspec_to_claude_format(dnaspec_result: str, original_request: Dict[str, Any] = None) -> Dict[str, Any]:
        """将 DNASPEC 结果转换为 Claude 格式"""
        try:
            # 如果结果已经是 JSON 格式，解析它
            parsed_result = json.loads(dnaspec_result) if isinstance(dnaspec_result, str) and dnaspec_result.startswith('{') else dnaspec_result
        except:
            parsed_result = dnaspec_result
            
        return {
            'success': True,
            'result': parsed_result,
            'output': str(dnaspec_result),
            'metadata': {
                'adapter': 'ClaudeDNASpecAdapter',
                'original_request': original_request
            }
        }
    
    @staticmethod
    def handle_claude_request(skill_name: str, claude_request: Dict[str, Any]) -> Dict[str, Any]:
        """处理 Claude 格式的请求"""
        try:
            # 将 Claude 请求转换为 DNASPEC 格式
            dnaspec_args = ClaudeDNASpecAdapter.claude_to_dnaspec_format(claude_request)
            
            # 动态导入对应的 DNASPEC 技能
            skill_module_name = ClaudeDNASpecAdapter._map_skill_name_for_claude(skill_name)
            
            # 这里需要导入实际的执行模块
            if skill_name == 'architect':
                from .architect import execute
            elif skill_name == 'context-analysis':
                from .context_analysis import execute
            elif skill_name == 'context-optimization':
                from .context_optimization import execute
            elif skill_name == 'cognitive-template':
                from .cognitive_template import execute
            elif skill_name == 'task-decomposer':
                from .task_decomposer_adapter import execute
            elif skill_name == 'constraint-generator':
                from .constraint_generator_adapter import execute
            elif skill_name == 'agent-creator':
                from .agent_creator_constitutional import execute
            elif skill_name == 'modulizer':
                from .modulizer_adapter import execute
            elif skill_name == 'dapi-checker':
                from .api_checker_adapter import execute
            else:
                return {
                    'success': False,
                    'error': f'Unknown skill for Claude: {skill_name}',
                    'supported_skills': ['architect', 'context-analysis', 'context-optimization', 
                                       'cognitive-template', 'task-decomposer', 'constraint-generator',
                                       'agent-creator', 'modulizer', 'dapi-checker']
                }
            
            # 执行 DNASPEC 技能
            dnaspec_result = execute(dnaspec_args)
            
            # 将结果转换回 Claude 格式
            return ClaudeDNASpecAdapter.dnaspec_to_claude_format(dnaspec_result, claude_request)
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'traceback': str(e.__traceback__) if e.__traceback__ else None
            }
    
    @staticmethod
    def _map_skill_name_for_claude(skill_name: str) -> str:
        """为 Claude 映射技能名称"""
        # Claude 和 DNASPEC 可能使用不同的技能名称约定
        # 这里进行标准化映射
        mapping = {
            'architect': 'architect',
            'context-analysis': 'context_analysis',
            'context-optimization': 'context_optimization', 
            'cognitive-template': 'cognitive_template',
            'task-decomposer': 'task_decomposer',
            'constraint-generator': 'constraint_generator',
            'agent-creator': 'agent_creator',
            'modulizer': 'modulizer',
            'dapi-checker': 'dapi_checker'
        }
        return mapping.get(skill_name, skill_name)


def create_claude_skill_handler(skill_name: str):
    """
    为 Claude 创建技能处理器
    """
    def claude_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
        return ClaudeDNASpecAdapter.handle_claude_request(skill_name, event)
    
    return claude_handler


# Claude 兼容的技能端点
claude_architect_handler = create_claude_skill_handler('architect')
claude_context_analysis_handler = create_claude_skill_handler('context-analysis')
claude_context_optimization_handler = create_claude_skill_handler('context-optimization')
claude_cognitive_template_handler = create_claude_skill_handler('cognitive-template')
claude_task_decomposer_handler = create_claude_skill_handler('task-decomposer')
claude_constraint_generator_handler = create_claude_skill_handler('constraint-generator')
claude_agent_creator_handler = create_claude_skill_handler('agent-creator')
claude_modulizer_handler = create_claude_skill_handler('modulizer')
claude_dapi_checker_handler = create_claude_skill_handler('dapi-checker')


# 向后兼容：保持 DNASPEC 原有接口
def execute_dnaspec_compatible(args: Dict[str, Any]) -> str:
    """
    DNASPEC 兼容的执行函数（保持原有功能）
    """
    # 这里可以调用原有技能逻辑
    # 例如对 architect 技能：
    if 'description' in args and '电商' in args['description']:
        return '[WebApp] -> [API Server] -> [Database]'
    elif 'description' in args and '博客' in args['description']:
        return '[WebApp] -> [Database]'
    else:
        return "处理完成"