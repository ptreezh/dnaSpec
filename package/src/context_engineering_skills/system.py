"""
Context Engineering Enhancement System
综合的上下文工程技能增强系统
"""
from typing import Dict, Any, List
from src.dnaspec_spec_kit_integration.core.skill import DNASpecSkill, SkillResult, SkillStatus
from .skills_manager import ContextEngineeringSkillsManager


class ContextEngineeringSystem(DNASpecSkill):
    """
    上下文工程系统
    提供完整的上下文工程解决方案，支持项目分解和AI Agentic架构的上下文管理
    """
    
    def __init__(self):
        super().__init__(
            name="dnaspec-context-engineering-system",
            description="DSGS上下文工程系统 - 提供完整上下文工程解决方案的专家"
        )
        self.skills_manager = ContextEngineeringSkillsManager()
    
    def _execute_skill_logic(self, request: str, context: Dict[str, Any]) -> Any:
        """
        执行上下文工程系统逻辑
        """
        function = context.get('function', 'enhance_context_for_project')
        context_to_process = request
        
        if function == 'enhance_context_for_project':
            return self._enhance_context_for_project(context_to_process, context)
        elif function == 'enhance_agentic_context':
            return self._enhance_agentic_context(context_to_process, context)
        elif function == 'run_context_audit':
            return self._run_context_audit(context_to_process, context)
        else:
            return {
                'success': False,
                'error': f'未知功能: {function}'
            }
    
    def _enhance_context_for_project(self, project_description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        为项目描述增强上下文
        专门用于优化项目分解
        """
        # 分析项目描述的上下文
        analysis_context = {'skill': 'context_analysis', 'context': project_description}
        analysis_result = self.skills_manager.process_request(project_description, analysis_context)
        
        if analysis_result.status != SkillStatus.COMPLETED or not analysis_result.result.get('success', True):
            return {
                'success': False,
                'error': '上下文分析失败'
            }
        
        # 优化项目描述的上下文
        optimization_context = {
            'skill': 'context_optimization',
            'context': project_description,
            'optimization_goals': 'clarity,relevance,completeness'
        }
        optimization_result = self.skills_manager.process_request(project_description, optimization_context)
        
        if optimization_result.status != SkillStatus.COMPLETED or not optimization_result.result.get('success', True):
            return {
                'success': False,
                'error': '上下文优化失败'
            }
        
        # 应用认知模板进行项目分解
        template_context = {
            'skill': 'cognitive_template',
            'context': optimization_result.result['optimized_context'],
            'template': 'chain_of_thought'
        }
        decomposition_result = self.skills_manager.process_request(optimization_result.result['optimized_context'], template_context)
        
        if decomposition_result.status != SkillStatus.COMPLETED or not decomposition_result.result.get('success', True):
            return {
                'success': False,
                'error': '认知模板应用失败'
            }
        
        return {
            'success': True,
            'original_description': project_description,
            'analysis': analysis_result.result,
            'optimized_context': optimization_result.result['optimized_context'],
            'decomposition_context': decomposition_result.result['enhanced_context'],
            'suggested_decomposition': self._extract_decomposition(decomposition_result.result['enhanced_context'])
        }
    
    def _enhance_agentic_context(self, agent_task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        为AI Agentic架构增强上下文
        优化AI代理的上下文管理
        """
        # 执行完整的上下文工程流水线
        pipeline_context = {
            'skill': 'full_context_pipeline',
            'context': agent_task,
            'optimization_goals': 'clarity,completeness,relevance',
            'template': 'verification'
        }
        pipeline_result = self.skills_manager.process_request(agent_task, pipeline_context)
        
        if pipeline_result.status != SkillStatus.COMPLETED or not pipeline_result.result.get('success', True):
            return {
                'success': False,
                'error': '完整流水线执行失败'
            }
        
        result_data = pipeline_result.result
        
        return {
            'success': True,
            'original_task': agent_task,
            'enhanced_context': result_data['final_enhanced_context'],
            'analysis': result_data['analysis'],
            'optimization': result_data['optimization'],
            'verification_context': result_data['template_application']['enhanced_context'],
            'recommended_agent_context': self._format_agent_context(
                result_data['final_enhanced_context'],
                result_data['template_application']['enhanced_context']
            )
        }
    
    def _run_context_audit(self, context_to_audit: str, context_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        运行上下文审计
        """
        # 使用分析、优化和模板应用进行综合审计
        analysis_context = {'skill': 'context_analysis', 'context': context_to_audit}
        analysis_result = self.skills_manager.process_request(context_to_audit, analysis_context)
        
        optimization_context = {
            'skill': 'context_optimization',
            'context': context_to_audit,
            'optimization_goals': 'efficiency,clarity,consistency'
        }
        optimization_result = self.skills_manager.process_request(context_to_audit, optimization_context)
        
        template_context = {
            'skill': 'cognitive_template',
            'context': context_to_audit,
            'template': 'understanding'
        }
        template_result = self.skills_manager.process_request(context_to_audit, template_context)
        
        audit_result = {
            'context_length': len(context_to_audit),
            'original_analysis': analysis_result.result if analysis_result.status == SkillStatus.COMPLETED else None,
            'optimization_suggestions': optimization_result.result if optimization_result.status == SkillStatus.COMPLETED else None,
            'understanding_framework': template_result.result if template_result.status == SkillStatus.COMPLETED else None,
            'overall_quality_score': self._calculate_quality_score(analysis_result, optimization_result)
        }
        
        return {
            'success': True,
            'audit_result': audit_result
        }
    
    def _extract_decomposition(self, enhanced_context: str) -> List[str]:
        """
        从增强的上下文中提取项目分解
        """
        # 这里可以实现具体的分解提取逻辑
        # 简单实现：提取以数字开头的行
        lines = enhanced_context.split('\n')
        decomposition_parts = []
        
        for line in lines:
            # 检查是否为分解的步骤
            if any(keyword in line for keyword in ['1.', '2.', '3.', '4.', '5.', '步骤', '阶段']):
                clean_line = line.strip()
                if clean_line:
                    # 去除markdown格式等
                    clean_line = clean_line.replace('**', '').replace('##', '').replace('#', '')
                    # 确保不是标题而是实际内容
                    if any(digit in clean_line for digit in ['1', '2', '3', '4', '5']):
                        decomposition_parts.append(clean_line)
        
        return decomposition_parts
    
    def _format_agent_context(self, optimized_context: str, verification_context: str) -> str:
        """
        格式化适用于AI代理的上下文
        """
        formatted = []
        formatted.append("### AI代理任务上下文")
        formatted.append("")
        formatted.append("#### 任务描述")
        formatted.append(optimized_context)
        formatted.append("")
        formatted.append("#### 验证框架")
        formatted.append(verification_context)
        formatted.append("")
        formatted.append("#### 执行指南")
        formatted.append("- 遵循以上验证框架执行任务")
        formatted.append("- 保持上下文一致性")
        formatted.append("- 定期检查执行结果的准确性")
        
        return "\n".join(formatted)
    
    def _calculate_quality_score(self, analysis_result: SkillResult, optimization_result: SkillResult) -> float:
        """
        计算上下文质量得分
        """
        if analysis_result.status != SkillStatus.COMPLETED or optimization_result.status != SkillStatus.COMPLETED:
            return 0.0
        
        analysis = analysis_result.result
        optimization = optimization_result.result
        
        # 基于分析指标计算基础分数
        base_score = sum(analysis['metrics'].values()) / len(analysis['metrics'])
        
        # 基于优化改进调整分数
        improvement_score = sum(max(0, v) for v in optimization['improvement_metrics'].values() 
                               if isinstance(v, (int, float))) / len(optimization['improvement_metrics'])
        
        # 综合得分
        final_score = (base_score + improvement_score) / 2
        return min(1.0, max(0.0, final_score))
    
    def _calculate_confidence(self, request: str) -> float:
        """
        计算系统置信度
        """
        if len(request) < 10:
            return 0.5  # 上下文太短，置信度中等
        else:
            return 0.85  # 有足够上下文，高置信度


def execute(args: Dict[str, Any]) -> str:
    """
    执行上下文工程系统的主要功能 - 兼容现有接口
    """
    context_to_process = args.get('context', '') or args.get('request', '')
    function = args.get('function', 'enhance_context_for_project')
    
    if not context_to_process:
        return "错误: 未提供上下文"
    
    # 准备上下文参数
    context_params = {k: v for k, v in args.items() if k not in ['context', 'request']}
    context_params['function'] = function
    
    skill = ContextEngineeringSystem()
    result = skill.process_request(context_to_process, context_params)
    
    if result.status == SkillStatus.ERROR:
        return f"错误: {result.error_message}"
    
    # 格式化输出结果
    output = []
    output.append(f"上下文工程系统执行结果 - 功能: {function}")
    output.append("=" * 70)
    
    if function == 'enhance_context_for_project':
        project_result = result.result
        if project_result['success']:
            output.append(f"原始项目描述: {project_result['original_description'][:100]}...")
            output.append(f"优化后上下文: {project_result['optimized_context'][:100]}...")
            output.append("\n建议的项目分解:")
            for i, part in enumerate(project_result['suggested_decomposition'][:5]):  # 只显示前5项
                output.append(f"  {i+1}. {part}")
        else:
            output.append(f"执行失败: {project_result.get('error', '未知错误')}")
        
    elif function == 'enhance_agentic_context':
        agent_result = result.result
        if agent_result['success']:
            output.append(f"原始任务: {agent_result['original_task'][:100]}...")
            output.append(f"推荐的代理上下文: {agent_result['recommended_agent_context'][:200]}...")
        else:
            output.append(f"执行失败: {agent_result.get('error', '未知错误')}")
        
    elif function == 'run_context_audit':
        audit_result = result.result
        if audit_result['success']:
            audit = audit_result['audit_result']
            output.append(f"上下文长度: {audit['context_length']} 字符")
            output.append(f"整体质量得分: {audit['overall_quality_score']:.2f}/1.0")
            
            if audit['original_analysis']:
                output.append(f"清晰度: {audit['original_analysis']['metrics']['clarity']:.2f}")
                output.append(f"完整性: {audit['original_analysis']['metrics']['completeness']:.2f}")
        else:
            output.append(f"执行失败: {audit_result.get('error', '未知错误')}")
    
    return "\n".join(output)


def get_system_info() -> Dict[str, Any]:
    """
    获取系统信息
    """
    return {
        'system_name': 'Context Engineering Enhancement System',
        'version': '1.0.0',
        'description': '用于优化项目分解和AI Agentic架构系统上下文工程的增强系统',
        'features': [
            '上下文分析与评估',
            '上下文优化与改进',
            '认知模板应用',
            '项目分解支持',
            'AI代理上下文管理',
            '上下文审计功能'
        ],
        'available_functions': [
            'enhance_context_for_project',
            'enhance_agentic_context',
            'run_context_audit'
        ]
    }