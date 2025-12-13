"""
Context Engineering System Skill
用于协调分析、优化和模板技能的综合系统
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from typing import Dict, Any, List
from src.dna_spec_kit_integration.core.skill import DNASpecSkill, SkillResult, SkillStatus
from .skills_system_final import ContextAnalysisSkill, ContextOptimizationSkill, CognitiveTemplateSkill


class ContextEngineeringSystemSkill(DNASpecSkill):
    """
    上下文工程系统技能
    协调分析、优化和模板技能的综合系统
    """
    
    def __init__(self):
        super().__init__(
            name="dnaspec-context-engineering-system",
            description="DNASPEC上下文工程系统 - 综合性的上下文工程解决方案，协调多个技能执行复杂任务"
        )
        
        # 创建子技能实例
        self.analysis_skill = ContextAnalysisSkill()
        self.optimization_skill = ContextOptimizationSkill()
        self.template_skill = CognitiveTemplateSkill()
    
    def _execute_skill_logic(self, request: str, context: Dict[str, Any]) -> Any:
        """
        执行上下文工程系统逻辑
        支持三种主要功能模式
        """
        function = context.get('function', 'enhance_context_for_project')
        
        if function == 'enhance_context_for_project':
            return self.enhance_context_for_project(request, context)
        elif function == 'enhance_agentic_context':
            template_type = context.get('template', 'verification')
            return self.enhance_agentic_context(request, template_type)
        elif function == 'run_context_audit':
            return self.run_context_audit(request)
        else:
            return {
                'success': False,
                'error': f'Unknown function: {function}',
                'available_functions': ['enhance_context_for_project', 'enhance_agentic_context', 'run_context_audit']
            }
    
    def enhance_context_for_project(self, project_description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """为项目描述增强上下文"""
        optimization_goals = context.get('optimization_goals', ['clarity', 'completeness', 'relevance'])
        
        try:
            # 1. 分析原始描述
            analysis_context = {'request': project_description}
            analysis_result = self.analysis_skill.process_request(project_description, analysis_context)
            
            if not analysis_result.success:
                return {
                    'success': False,
                    'error': f"Context analysis failed: {analysis_result.error_message}"
                }
            
            # 2. 优化上下文
            optimization_context = {
                'optimization_goals': optimization_goals
            }
            optimization_result = self.optimization_skill.process_request(
                project_description, 
                optimization_context
            )
            
            if not optimization_result.success:
                return {
                    'success': False, 
                    'error': f"Context optimization failed: {optimization_result.error_message}"
                }
            
            # 3. 应用认知模板（如思维链）以结构化项目分解
            optimized_context = optimization_result.result['optimized_context']
            template_context = {'template': 'chain_of_thought'}
            template_result = self.template_skill.process_request(
                optimized_context,
                template_context
            )
            
            if not template_result.success or not template_result.result['success']:
                return {
                    'success': False,
                    'error': f"Cognitive template application failed: {template_result.result.get('error', 'Unknown template error') if template_result.success else template_result.error_message}"
                }
            
            return {
                'success': True,
                'original_description': project_description,
                'analysis_result': analysis_result.result,
                'optimized_context': optimized_context,
                'structured_context': template_result.result['enhanced_context'],
                'suggested_decomposition': self._extract_project_tasks(template_result.result['enhanced_context'])
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"System execution failed: {str(e)}"
            }
    
    def enhance_agentic_context(self, agent_task: str, template_type: str = 'verification') -> Dict[str, Any]:
        """为AI代理增强上下文"""
        try:
            # 1. 应用验证模板以确保代理任务清晰明确
            template_context = {'template': template_type}
            template_result = self.template_skill.process_request(
                agent_task,
                template_context
            )
            
            if not template_result.success or not template_result.result['success']:
                return {
                    'success': False,
                    'error': f"Template application failed: {template_result.result.get('error', 'Unknown template error') if template_result.success else template_result.error_message}"
                }
            
            # 2. 优化结构化后的上下文
            optimized_context = template_result.result['enhanced_context']
            optimization_context = {'optimization_goals': ['clarity', 'completeness']}
            optimization_result = self.optimization_skill.process_request(
                optimized_context, 
                optimization_context
            )
            
            if not optimization_result.success:
                return {
                    'success': False,
                    'error': f"Context optimization failed: {optimization_result.error_message}"
                }
            
            return {
                'success': True,
                'original_task': agent_task,
                'structured_context': template_result.result['enhanced_context'],
                'optimized_context': optimization_result.result['optimized_context'],
                'recommended_agent_context': optimization_result.result['optimized_context']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Agentic context enhancement failed: {str(e)}"
            }
    
    def run_context_audit(self, context_to_audit: str) -> Dict[str, Any]:
        """运行上下文审计"""
        try:
            # 执行完整的分析-优化-模板应用流水线
            analysis_context = {'request': context_to_audit}
            analysis_result = self.analysis_skill.process_request(context_to_audit, analysis_context)
            
            optimization_context = {'optimization_goals': ['clarity', 'relevance', 'completeness']}
            optimization_result = self.optimization_skill.process_request(
                context_to_audit,
                optimization_context
            )
            
            template_context = {'template': 'understanding'}
            template_result = self.template_skill.process_request(
                context_to_audit,
                template_context
            )
            
            # 检查所有操作是否成功
            all_successful = all([
                analysis_result.success,
                optimization_result.success,
                template_result.success and template_result.result['success']
            ])
            
            if not all_successful:
                errors = []
                if analysis_result.success:
                    errors.append(f"Analysis: succeeded")
                else:
                    errors.append(f"Analysis: {analysis_result.error_message}")
                
                if optimization_result.success:
                    errors.append(f"Optimization: succeeded")
                else:
                    errors.append(f"Optimization: {optimization_result.error_message}")
                
                if template_result.success and template_result.result['success']:
                    errors.append(f"Template: succeeded")
                else:
                    template_error = template_result.result.get('error', 'Unknown template error') if template_result.success else template_result.error_message
                    errors.append(f"Template: {template_error}")
                
                return {
                    'success': False,
                    'error': "One or more audit components failed: " + "; ".join(errors)
                }
            
            return {
                'success': True,
                'context_length': len(context_to_audit),
                'analysis': analysis_result.result,
                'optimization': optimization_result.result,
                'understanding_context': template_result.result['enhanced_context'],
                'audit_score': self._calculate_audit_score(analysis_result.result, optimization_result.result)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Audit failed: {str(e)}"
            }
    
    def _extract_project_tasks(self, structured_context: str) -> List[str]:
        """从结构化上下文中提取项目任务"""
        lines = structured_context.split('\n')
        tasks = []
        
        import re
        for line in lines:
            line = line.strip()
            if re.match(r'^\d+\.', line) or re.match(r'^[一二三四五六七八九十]+、', line):
                task_text = re.sub(r'^\d+[.\.\s]+|[一二三四五六七八九十]+、', '', line).strip()
                if len(task_text) > 0 and len(task_text) < 500:  # 过滤过长或过短的行
                    tasks.append(task_text)
        
        return tasks[:10]  # 返回最多10个任务
    
    def _calculate_audit_score(self, analysis_data: Dict[str, Any], optimization_data: Dict[str, Any]) -> float:
        """计算审计分数"""
        metrics = analysis_data.get('metrics', {})
        improvements = optimization_data.get('improvement_metrics', {})
        
        if not metrics:
            return 0.0
        
        # 计算分析质量平均分
        analysis_avg = sum(metrics.values()) / len(metrics) if metrics else 0.0
        
        # 计算优化改进平均值
        improvement_values = [v for v in improvements.values() if isinstance(v, (int, float))]
        improvement_avg = sum(improvement_values) / len(improvement_values) if improvement_values else 0.0
        
        # 综合得分（分析质量 + 优化改进）
        total_score = min(1.0, analysis_avg + improvement_avg * 0.5)  # 优化改进权重小一些
        return max(0.0, total_score)
    
    def _calculate_confidence(self, request: str) -> float:
        """计算系统执行置信度"""
        # 系统依赖子技能的置信度
        return 0.9  # 基于协调多个技能的高置信度


def execute(args: Dict[str, Any]) -> str:
    """
    执行上下文工程系统功能（兼容函数）
    """
    context = args.get('context', '') or args.get('request', '')
    function = args.get('function', 'enhance_context_for_project')
    
    if not context:
        return "错误: 未提供上下文"
    
    # 为演示目的使用系统技能
    system = ContextEngineeringSystemSkill()
    context_args = {
        'function': function
    }
    
    if 'optimization_goals' in args:
        context_args['optimization_goals'] = args['optimization_goals']
    if 'template' in args:
        context_args['template'] = args['template']
    
    result = system.process_request(context, context_args)
    
    if not result.success:
        return f"错误: {result.error_message}"
    
    data = result.result
    
    if not data['success']:
        return f"系统执行错误: {data['error']}"
    
    # 格式化输出
    output_lines = []
    
    if function == 'enhance_context_for_project':
        output_lines.append("项目上下文增强结果:")
        output_lines.append(f"原始描述长度: {len(data['original_description'])} 字符")
        output_lines.append("")
        output_lines.append("优化后上下文:")
        output_lines.append(data['optimized_context'][:300] + ("..." if len(data['optimized_context']) > 300 else ""))
        output_lines.append("")
        if data['suggested_decomposition']:
            output_lines.append("建议的项目分解:")
            for i, task in enumerate(data['suggested_decomposition'][:5], 1):  # 显示前5个任务
                output_lines.append(f"  {i}. {task}")
    
    elif function == 'enhance_agentic_context':
        output_lines.append("AI代理上下文增强结果:")
        output_lines.append(f"原始任务: {data['original_task'][:100]}...")
        output_lines.append("")
        output_lines.append("推荐的代理上下文:")
        output_lines.append(data['recommended_agent_context'][:300] + ("..." if len(data['recommended_agent_context']) > 300 else ""))
    
    elif function == 'run_context_audit':
        output_lines.append("上下文审计结果:")
        output_lines.append(f"上下文长度: {data['context_length']} 字符")
        output_lines.append(f"审计分数: {data['audit_score']:.2f}/1.0")
        output_lines.append("")
        
        analysis = data['analysis']
        output_lines.append("质量指标:")
        for metric, score in analysis['metrics'].items():
            metric_names = {
                'clarity': '清晰度',
                'relevance': '相关性',
                'completeness': '完整性', 
                'consistency': '一致性',
                'efficiency': '效率'
            }
            output_lines.append(f"  {metric_names.get(metric, metric)}: {score:.2f}")
    
    return "\n".join(output_lines)


def get_available_functions() -> List[str]:
    """获取可用功能列表"""
    return [
        'enhance_context_for_project',
        'enhance_agentic_context', 
        'run_context_audit'
    ]