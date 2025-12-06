"""
Context Engineering Skills Manager
统一管理所有上下文工程技能
"""
from typing import Dict, Any, List
from src.dsgs_spec_kit_integration.core.skill import DSGSSkill, SkillResult, SkillStatus
from .context_analysis import ContextAnalysisSkill
from .context_optimization import ContextOptimizationSkill
from .cognitive_template import CognitiveTemplateSkill


class ContextEngineeringSkillsManager(DSGSSkill):
    """
    上下文工程技能管理器
    统一管理并协调各种上下文工程技能
    """
    
    def __init__(self):
        super().__init__(
            name="dsgs-context-engineering-manager",
            description="DSGS上下文工程技能管理器 - 统一管理上下文工程技能的专家"
        )
        self.context_analysis_skill = ContextAnalysisSkill()
        self.context_optimization_skill = ContextOptimizationSkill()
        self.cognitive_template_skill = CognitiveTemplateSkill()
        
        self.skills = {
            'context_analysis': self.context_analysis_skill,
            'context_optimization': self.context_optimization_skill,
            'cognitive_template': self.cognitive_template_skill,
            'full_context_pipeline': self._run_full_pipeline
        }
    
    def _execute_skill_logic(self, request: str, context: Dict[str, Any]) -> Any:
        """
        执行技能管理逻辑
        """
        skill_name = context.get('skill', 'context_analysis')
        context_to_process = request  # 原始请求作为要处理的上下文
        
        if skill_name not in self.skills:
            available_skills = list(self.skills.keys())
            return {
                'success': False,
                'error': f'技能不存在: {skill_name}',
                'available_skills': available_skills
            }
        
        # 如果是预定义的技能，直接调用
        if skill_name in ['context_analysis', 'context_optimization', 'cognitive_template']:
            skill_instance = self.skills[skill_name]
            skill_request = context_to_process
            skill_context = {k: v for k, v in context.items() if k != 'skill'}  # 除去skill参数
            return skill_instance.process_request(skill_request, skill_context).result
        else:
            # 运行完整流水线
            return self._run_full_pipeline(context_to_process, context)
    
    def _run_full_pipeline(self, context_to_process: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        运行完整上下文工程流水线
        """
        # 步骤1: 分析上下文
        analysis_context = {
            'request': context_to_process
        }
        analysis_result = self.context_analysis_skill.process_request(context_to_process, analysis_context)
        
        # 步骤2: 优化上下文
        optimization_goals = context.get('optimization_goals', 'clarity,relevance,completeness')
        goals_list = [goal.strip() for goal in optimization_goals.split(',')]
        optimization_context = {
            'optimization_goals': goals_list
        }
        optimization_result = self.context_optimization_skill.process_request(context_to_process, optimization_context)
        
        # 步骤3: 应用认知模板
        template_name = context.get('template', 'chain_of_thought')
        template_context = {
            'template': template_name,
            'role': context.get('role', '专家')
        }
        template_result = self.cognitive_template_skill.process_request(context_to_process, template_context)
        
        return {
            'original_context': context_to_process,
            'analysis': analysis_result.result if analysis_result.status == SkillStatus.COMPLETED else None,
            'optimization': optimization_result.result if optimization_result.status == SkillStatus.COMPLETED else None,
            'template_application': template_result.result if template_result.status == SkillStatus.COMPLETED else None,
            'final_enhanced_context': optimization_result.result['optimized_context'] if optimization_result.status == SkillStatus.COMPLETED else context_to_process
        }
    
    def _calculate_confidence(self, request: str) -> float:
        """
        计算管理器置信度
        """
        return 0.95  # 管理器调用已验证技能，置信度高


def execute(args: Dict[str, Any]) -> str:
    """
    执行上下文工程技能管理器 - 兼容现有接口
    """
    context_to_process = args.get('context', '') or args.get('request', '')
    skill_name = args.get('skill', 'context_analysis')
    
    if not context_to_process:
        return "错误: 未提供上下文"
    
    # 准备上下文参数
    context_params = {k: v for k, v in args.items() if k not in ['context', 'request']}
    context_params['skill'] = skill_name
    
    skill = ContextEngineeringSkillsManager()
    result = skill.process_request(context_to_process, context_params)
    
    if result.status == SkillStatus.ERROR:
        return f"错误: {result.error_message}"
    
    # 对于流水线技能，需要特殊处理输出
    if skill_name == 'full_context_pipeline':
        pipeline_result = result.result
        output = []
        output.append("完整上下文工程流水线执行结果:")
        output.append("\n1. 上下文分析:")
        analysis = pipeline_result['analysis']
        output.append(f"   长度: {analysis['context_length']} 字符, 估算Tokens: {analysis['token_count']}")
        
        output.append("\n2. 上下文优化:")
        optimization = pipeline_result['optimization']
        output.append(f"   原始长度: {optimization['original_analysis']['context_length']}, 优化后: {optimization['optimized_analysis']['context_length']}")
        
        output.append("\n3. 认知模板应用:")
        template_result = pipeline_result['template_application']
        output.append(f"   模板: {template_result['template_name']}")
        
        output.append("\n4. 最终增强上下文:")
        output.append(pipeline_result['final_enhanced_context'])
        
        return "\n".join(output)
    else:
        # 其他技能直接返回对应技能的输出格式
        return execute_skill_direct(skill_name, context_to_process, args)


def execute_skill_direct(skill_name: str, context: str, args: Dict[str, Any]) -> str:
    """
    直接执行特定技能
    """
    if skill_name == 'context_analysis':
        from .context_analysis import execute as analysis_execute
        temp_args = {'context': context, **args}
        return analysis_execute(temp_args)
    elif skill_name == 'context_optimization':
        from .context_optimization import execute as optimization_execute
        temp_args = {'context': context, **args}
        return optimization_execute(temp_args)
    elif skill_name == 'cognitive_template':
        from .cognitive_template import execute as template_execute
        temp_args = {'context': context, **args}
        return template_execute(temp_args)
    else:
        return f"错误: 未知技能 '{skill_name}'"