"""
DNASPEC 技能适配器 - 将原有技能集成到新架构中
"""

from typing import Dict, Any, Callable
from src.agents.agent_manager import BaseAgent
from src.hooks.hook_system import hook_manager, HookContext, HookType
from src.tools.tool_manager import ToolManager


class DnaSpecSkillAdapter:
    """
    将原有dnaspec技能适配到新架构的适配器
    """
    
    def __init__(self):
        self.skill_adapters = {}
        self._register_existing_skills()
    
    def _register_existing_skills(self):
        """
        注册现有的dnaspec技能
        """
        # 1. 将现有技能作为Agents注册
        self._register_skills_as_agents()
        
        # 2. 将现有技能作为Tools注册
        self._register_skills_as_tools()
        
        # 3. 将现有技能作为Hooks注册
        self._register_skills_as_hooks()
    
    def _register_skills_as_agents(self):
        """
        将现有技能作为Agents注册
        """
        # 示例：将context-analyzer技能作为Agent注册
        class ContextAnalyzerAgent(BaseAgent):
            async def process(self, params: Dict[str, Any]) -> Any:
                # 这里调用原有的context-analyzer技能逻辑
                context = params.get('context', '')
                # 模拟原有技能的处理逻辑
                result = {
                    'analysis': f'Context analysis for: {context[:50]}...',
                    'quality_score': 0.85,
                    'suggestions': ['Improve clarity', 'Add more details']
                }
                return result
        
        # 示例：将constraint-generator技能作为Agent注册
        class ConstraintGeneratorAgent(BaseAgent):
            async def process(self, params: Dict[str, Any]) -> Any:
                # 这里调用原有的constraint-generator技能逻辑
                requirement = params.get('requirement', '')
                # 模拟原有技能的处理逻辑
                result = {
                    'constraints': [
                        f'Constraint for {requirement}: Performance must be optimized',
                        f'Constraint for {requirement}: Security compliance required'
                    ]
                }
                return result
        
        # 示例：将modulizer技能作为Agent注册
        class ModulizerAgent(BaseAgent):
            async def process(self, params: Dict[str, Any]) -> Any:
                # 这里调用原有的modulizer技能逻辑
                system_desc = params.get('system_description', '')
                # 模拟原有技能的处理逻辑
                result = {
                    'modules': [
                        {'name': 'core_module', 'description': 'Core functionality'},
                        {'name': 'utils_module', 'description': 'Utility functions'}
                    ]
                }
                return result
        
        # 注册这些Agent到AgentManager
        from src.agents.agent_manager import AgentManager
        agent_manager = AgentManager()
        agent_manager.register_agent('context-analyzer', ContextAnalyzerAgent('context-analyzer-agent'))
        agent_manager.register_agent('constraint-generator', ConstraintGeneratorAgent('constraint-generator-agent'))
        agent_manager.register_agent('modulizer', ModulizerAgent('modulizer-agent'))
    
    def _register_skills_as_tools(self):
        """
        将现有技能作为Tools注册
        """
        tool_manager = ToolManager()
        
        # 示例：将context-analyzer作为工具注册
        def context_analyzer_tool(params: Dict[str, Any]) -> Any:
            context = params.get('context', '')
            # 模拟原有技能的处理逻辑
            return {
                'tool': 'context-analyzer',
                'analysis': f'Context analysis for: {context[:50]}...',
                'quality_score': 0.85,
                'suggestions': ['Improve clarity', 'Add more details']
            }
        
        # 示例：将constraint-generator作为工具注册
        def constraint_generator_tool(params: Dict[str, Any]) -> Any:
            requirement = params.get('requirement', '')
            # 模拟原有技能的处理逻辑
            return {
                'tool': 'constraint-generator',
                'constraints': [
                    f'Constraint for {requirement}: Performance must be optimized',
                    f'Constraint for {requirement}: Security compliance required'
                ]
            }
        
        # 注册工具
        tool_manager.register_tool('context-analyzer', context_analyzer_tool)
        tool_manager.register_tool('constraint-generator', constraint_generator_tool)
    
    def _register_skills_as_hooks(self):
        """
        将现有技能作为Hooks注册
        """
        # 示例：注册一个在代码生成后执行的技能
        def post_code_generation_skill(context: HookContext):
            if context.hook_name == 'skill_after_invoke' and context.data.get('skill_name') == 'code-generation':
                # 在代码生成后执行额外的分析
                code = context.data.get('generated_code', '')
                analysis_result = f"Post-processing analysis of {len(code)} chars of code"
                print(f"Post-generation skill executed: {analysis_result}")
        
        # 注册Hook
        hook_manager.register_hook('skill_after_invoke', post_code_generation_skill)


# 初始化适配器
skill_adapter = DnaSpecSkillAdapter()


def get_original_skill_as_agent(skill_name: str) -> BaseAgent:
    """
    获取原有技能作为Agent的适配器
    """
    from src.agents.agent_manager import AgentManager
    agent_manager = AgentManager()
    return agent_manager.get_agent(skill_name)


def execute_original_skill_as_tool(skill_name: str, params: Dict[str, Any]) -> Any:
    """
    作为工具执行原有技能
    """
    tool_manager = ToolManager()
    return tool_manager.execute_tool(skill_name, params)


def register_skill_hook(skill_name: str, callback: Callable):
    """
    将技能注册为Hook回调
    """
    hook_manager.register_hook(skill_name, callback)