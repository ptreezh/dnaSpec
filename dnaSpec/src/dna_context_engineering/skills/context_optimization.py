"""
Context Optimization Skill
基于AI模型的上下文优化技能
"""
from typing import Dict, Any
from ..core_skill import ContextEngineeringSkill, SkillResult
from ..ai_client import AIModelClient
from ..instruction_template import TemplateRegistry


class ContextOptimizationSkill(ContextEngineeringSkill):
    """上下文优化技能 - 基于分析结果优化上下文质量"""
    
    def __init__(self, ai_client: AIModelClient, template_registry: TemplateRegistry):
        super().__init__(
            name="dnaspec-context-optimization", 
            description="上下文优化技能 - 优化上下文质量以提升AI交互效果",
            ai_client=ai_client,
            template_registry=template_registry
        )
    
    def execute(self, context: str, params: Dict[str, Any] = None) -> SkillResult:
        """执行上下文优化"""
        # 验证输入
        validation_error = self.validate_input(context, params)
        if validation_error:
            return SkillResult(
                success=False,
                data={},
                error=validation_error
            )
        
        # 设置默认参数
        if params is None:
            params = {}
        
        optimization_goals = params.get('optimization_goals', ['clarity', 'completeness'])
        if isinstance(optimization_goals, str):
            optimization_goals = [goal.strip() for goal in optimization_goals.split(',')]
        
        language = params.get('language', 'Chinese')
        
        # 构造优化指令
        instruction = self.template_registry.create_prompt(
            'context-optimization',
            context,
            {
                'optimization_goals': optimization_goals,
                'language': language
            }
        )
        
        # 发送到AI模型
        response = self.ai_client.send_instruction(instruction)
        
        # 解析AI响应
        try:
            parsed_result = self.template_registry.parse_response('context-optimization', response)
            
            # 计算优化改进指标
            improvement_metrics = self._calculate_improvements(context, parsed_result.get('optimized_context', ''))
            
            return SkillResult(
                success=True,
                data={
                    'original_context': context,
                    'optimized_context': parsed_result.get('optimized_context', ''),
                    'applied_optimizations': parsed_result.get('applied_optimizations', []),
                    'improvement_metrics': improvement_metrics,
                    'raw_response': response
                },
                confidence=0.85  # 基于优化复杂度设定置信度
            )
            
        except Exception as e:
            return SkillResult(
                success=False,
                data={'raw_response': response},
                error=f"Failed to parse optimization response: {str(e)}"
            )
    
    def _calculate_improvements(self, original: str, optimized: str) -> Dict[str, float]:
        """计算优化改进指标"""
        improvements = {}
        
        # 简单的改进计算示例
        original_length = len(original)
        optimized_length = len(optimized)
        
        # 长度效率改进
        improvements['conciseness'] = (original_length - optimized_length) / original_length if original_length > 0 else 0
        
        # 这里可以添加更复杂的改进度量
        # 例如：通过再次分析优化前后的内容来计算质量改进
        
        return improvements
    
    def validate_input(self, context: str, params: Dict[str, Any] = None) -> str:
        """验证输入参数"""
        if not context or not context.strip():
            return "Context cannot be empty"
        
        if len(context) > 50000:  # 限制最大长度
            return "Context too long (max 50000 characters)"
        
        params = params or {}
        goals = params.get('optimization_goals', ['clarity', 'completeness'])
        
        if isinstance(goals, str):
            goals = [g.strip() for g in goals.split(',')]
        
        valid_goals = {'clarity', 'relevance', 'completeness', 'conciseness', 'consistency'}
        invalid_goals = [goal for goal in goals if goal not in valid_goals]
        
        if invalid_goals:
            return f"Invalid optimization goals: {invalid_goals}. Valid: {list(valid_goals)}"
        
        language = params.get('language', 'Chinese')
        if language not in ['Chinese', 'English']:
            return f"Unsupported language: {language}. Supported: Chinese, English"
        
        return None  # 无错误


def execute(args: Dict[str, Any]) -> str:
    """
    执行上下文优化技能（兼容函数）
    """
    context = args.get('context', '') or args.get('request', '')
    goals = args.get('optimization_goals', 'clarity,completeness')
    
    if not context:
        return "Error: No context provided for optimization"
    
    # 验证优化目标
    goal_list = [g.strip() for g in goals.split(',')]
    valid_goals = {'clarity', 'relevance', 'completeness', 'conciseness', 'consistency'}
    invalid_goals = [g for g in goal_list if g not in valid_goals]
    
    if invalid_goals:
        return f"Error: Invalid optimization goals: {invalid_goals}"
    
    # 模拟优化结果（在实际实现中，这将调用真实的AI模型）
    mock_result = {
        'original_context': context,
        'optimized_context': f"[优化后] {context} - 已根据目标 {goals} 进行优化",
        'applied_optimizations': [f"应用{goal}优化" for goal in goal_list],
        'improvement_metrics': {goal: 0.1 for goal in goal_list},  # 模拟改进指标
        'raw_response': "SIMULATED AI RESPONSE FOR OPTIMIZATION"
    }
    
    # 格式化输出
    output_lines = []
    output_lines.append("上下文优化结果:")
    output_lines.append(f"原始长度: {len(mock_result['original_context'])} 字符")
    output_lines.append(f"优化后长度: {len(mock_result['optimized_context'])} 字符")
    output_lines.append("")
    
    output_lines.append("应用的优化:")
    for opt in mock_result['applied_optimizations']:
        output_lines.append(f"  • {opt}")
    
    output_lines.append("\n改进指标:")
    for metric, improvement in mock_result['improvement_metrics'].items():
        direction = "↗️" if improvement > 0 else "↘️" if improvement < 0 else "➡️"
        output_lines.append(f"  {direction} {metric}: {improvement:+.2f}")
    
    output_lines.append("\n优化后上下文:")
    output_lines.append(mock_result['optimized_context'])
    
    return "\n".join(output_lines)