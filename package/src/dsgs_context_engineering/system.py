"""
System Components for DNASPEC Context Engineering Skills
完整的系统组件实现
"""
from typing import Dict, Any, List
from .core_skill import ContextEngineeringSkill, SkillResult, SkillsManager
from .skills.context_analysis import ContextAnalysisSkill
from .skills.context_optimization import ContextOptimizationSkill  
from .skills.cognitive_template import CognitiveTemplateSkill
from .ai_client import AIModelClient, create_ai_client
from .instruction_template import TemplateRegistry


class ContextEngineeringSystem:
    """上下文工程系统 - 综合的上下文工程解决方案"""
    
    def __init__(self, ai_provider: str = "generic", api_key: str = ""):
        # 创建AI客户端
        self.ai_client = create_ai_client(ai_provider, api_key)
        
        # 创建模板注册表
        self.template_registry = TemplateRegistry()
        
        # 创建技能管理器
        self.skills_manager = SkillsManager(
            ai_client=self.ai_client,
            template_registry=self.template_registry
        )
        
        # SkillsManager已在初始化时预注册了核心技能，无需重复注册
        # 核心技能: context-analysis, context-optimization, cognitive-template 已预加载
    
    def enhance_context_for_project(self, project_description: str, optimization_goals: List[str] = None) -> Dict[str, Any]:
        """为项目描述增强上下文"""
        if optimization_goals is None:
            optimization_goals = ['clarity', 'completeness', 'relevance']
        
        try:
            # 1. 分析原始描述
            analysis_result = self.skills_manager.execute_skill('context-analysis', project_description, {})
            if not analysis_result.success:
                return {
                    'success': False,
                    'error': f"Context analysis failed: {analysis_result.error}"
                }
            
            # 2. 优化上下文
            optimization_params = {'optimization_goals': optimization_goals}
            optimization_result = self.skills_manager.execute_skill(
                'context-optimization', 
                project_description, 
                optimization_params
            )
            if not optimization_result.success:
                return {
                    'success': False, 
                    'error': f"Context optimization failed: {optimization_result.error}"
                }
            
            # 3. 应用认知模板（如思维链）以结构化项目分解
            template_params = {'template': 'chain_of_thought', 'language': 'Chinese'}
            template_result = self.skills_manager.execute_skill(
                'cognitive-template',
                optimization_result.data['optimized_context'],
                template_params
            )
            if not template_result.success:
                return {
                    'success': False,
                    'error': f"Cognitive template application failed: {template_result.error}"
                }
            
            return {
                'success': True,
                'original_description': project_description,
                'analysis_result': analysis_result.data,
                'optimized_context': optimization_result.data['optimized_context'],
                'structured_context': template_result.data['enhanced_context'],
                'suggested_decomposition': self._extract_project_tasks(template_result.data['enhanced_context'])
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
            template_params = {'template': template_type, 'language': 'Chinese'}
            template_result = self.skills_manager.execute_skill(
                'cognitive-template',
                agent_task,
                template_params
            )
            
            if not template_result.success:
                return {
                    'success': False,
                    'error': f"Template application failed: {template_result.error}"
                }
            
            # 2. 优化结构化后的上下文
            optimization_params = {'optimization_goals': ['clarity', 'completeness']}
            optimization_result = self.skills_manager.execute_skill(
                'context-optimization',
                template_result.data['enhanced_context'], 
                optimization_params
            )
            
            if not optimization_result.success:
                return {
                    'success': False,
                    'error': f"Context optimization failed: {optimization_result.error}"
                }
            
            return {
                'success': True,
                'original_task': agent_task,
                'structured_context': template_result.data['enhanced_context'],
                'optimized_context': optimization_result.data['optimized_context'],
                'recommended_agent_context': optimization_result.data['optimized_context']
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
            analysis_result = self.skills_manager.execute_skill('context-analysis', context_to_audit, {})
            optimization_result = self.skills_manager.execute_skill(
                'context-optimization',
                context_to_audit,
                {'optimization_goals': ['clarity', 'relevance', 'completeness']}
            )
            template_result = self.skills_manager.execute_skill(
                'cognitive-template',
                context_to_audit,
                {'template': 'understanding'}
            )
            
            # 验证所有操作都成功
            all_successful = all([
                analysis_result.success,
                optimization_result.success,
                template_result.success
            ])
            
            if not all_successful:
                errors = []
                if not analysis_result.success:
                    errors.append(f"Analysis: {analysis_result.error}")
                if not optimization_result.success:
                    errors.append(f"Optimization: {optimization_result.error}")
                if not template_result.success:
                    errors.append(f"Template: {template_result.error}")
                
                return {
                    'success': False,
                    'error': "One or more audit components failed: " + "; ".join(errors)
                }
            
            return {
                'success': True,
                'context_length': len(context_to_audit),
                'analysis': analysis_result.data,
                'optimization': optimization_result.data,
                'understanding_context': template_result.data['enhanced_context'],
                'audit_score': self._calculate_audit_score(analysis_result.data, optimization_result.data)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Audit failed: {str(e)}"
            }
    
    def _extract_project_tasks(self, structured_context: str) -> List[str]:
        """从结构化上下文中提取项目任务"""
        # 这里可以实现更复杂的任务提取逻辑
        # 简单实现：提取带数字编号的行
        lines = structured_context.split('\n')
        tasks = []
        
        import re
        for line in lines:
            line = line.strip()
            if re.match(r'^\d+\.', line) or re.match(r'^[一二三四五六七八九十]+、', line):
                task_text = re.sub(r'^\d+[.\.\s]+|[一二三四五六七八九十]+、', '', line).strip()
                if len(task_text) > 0 and len(task_text) < 200:  # 过滤过长或过短的行
                    tasks.append(task_text)
        
        return tasks[:10]  # 返回最多10个任务
    
    def _calculate_audit_score(self, analysis_data: Dict[str, Any], optimization_data: Dict[str, Any]) -> float:
        """计算审计分数"""
        # 基于分析指标和优化改进计算综合分数
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
        total_score = min(1.0, analysis_avg + improvement_avg)
        return max(0.0, total_score)


def execute(args: Dict[str, Any]) -> str:
    """
    执行上下文工程系统功能
    """
    function = args.get('function', 'enhance_context_for_project')
    context = args.get('context', '') or args.get('request', '')
    
    if not context:
        return "错误: 未提供上下文"
    
    # 为演示目的使用通用客户端
    system = ContextEngineeringSystem(ai_provider="generic")
    
    if function == 'enhance_context_for_project':
        result = system.enhance_context_for_project(context)
    elif function == 'enhance_agentic_context':
        template_type = args.get('template', 'verification')
        result = system.enhance_agentic_context(context, template_type)
    elif function == 'run_context_audit':
        result = system.run_context_audit(context)
    else:
        return f"错误: 未知功能 '{function}'"
    
    if not result['success']:
        return f"错误: {result['error']}"
    
    # 格式化输出
    output_lines = []
    
    if function == 'enhance_context_for_project':
        output_lines.append("项目上下文增强结果:")
        output_lines.append(f"原始描述: {result['original_description'][:100]}...")
        output_lines.append("")
        output_lines.append("优化后上下文:")
        output_lines.append(result['optimized_context'])
        output_lines.append("")
        if result['suggested_decomposition']:
            output_lines.append("建议的项目分解:")
            for i, task in enumerate(result['suggested_decomposition'][:5], 1):  # 显示前5个任务
                output_lines.append(f"  {i}. {task}")
    
    elif function == 'enhance_agentic_context':
        output_lines.append("AI代理上下文增强结果:")
        output_lines.append(f"原始任务: {result['original_task'][:100]}...")
        output_lines.append("")
        output_lines.append("推荐的代理上下文:")
        output_lines.append(result['recommended_agent_context'])
    
    elif function == 'run_context_audit':
        output_lines.append("上下文审计结果:")
        output_lines.append(f"上下文长度: {result['context_length']} 字符")
        output_lines.append(f"审计分数: {result['audit_score']:.2f}/1.0")
        output_lines.append("")
        
        analysis = result['analysis']
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