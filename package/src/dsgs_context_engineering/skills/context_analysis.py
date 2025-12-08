"""
Context Analysis Skill
基于AI模型的上下文分析技能
"""
from typing import Dict, Any
from ..core_skill import ContextEngineeringSkill, SkillResult
from ..ai_client import AIModelClient
from ..instruction_template import TemplateRegistry


class ContextAnalysisSkill(ContextEngineeringSkill):
    """上下文分析技能 - 分析上下文质量的五维指标"""
    
    def __init__(self, ai_client: AIModelClient, template_registry: TemplateRegistry):
        super().__init__(
            name="dnaspec-context-analysis",
            description="上下文分析技能 - 专业分析上下文质量的五维指标",
            ai_client=ai_client,
            template_registry=template_registry
        )
    
    def execute(self, context: str, params: Dict[str, Any] = None) -> SkillResult:
        """执行上下文分析"""
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
        
        # 构造分析指令
        language = params.get('language', 'Chinese')
        instruction = self.template_registry.create_prompt(
            'context-analysis',
            context,
            {'language': language}
        )
        
        # 发送到AI模型并获取结果
        response = self.ai_client.send_instruction(instruction)
        
        # 解析AI响应
        try:
            parsed_result = self.template_registry.parse_response('context-analysis', response)
            
            # 计算总体置信度（基于各指标的一致性）
            metrics = parsed_result.get('metrics', {})
            if metrics:
                avg_score = sum(metrics.values()) / len(metrics) if metrics else 0.5
                confidence = min(1.0, avg_score + 0.2)  # 基础置信度
            else:
                confidence = 0.5  # 默认置信度
            
            return SkillResult(
                success=True,
                data={
                    'context_length': len(context),
                    'token_count': self._estimate_tokens(context),
                    'metrics': parsed_result.get('metrics', {}),
                    'suggestions': parsed_result.get('suggestions', []),
                    'issues': parsed_result.get('issues', []),
                    'raw_response': response
                },
                confidence=confidence
            )
            
        except Exception as e:
            return SkillResult(
                success=False,
                data={'raw_response': response},
                error=f"Failed to parse AI response: {str(e)}"
            )
    
    def _estimate_tokens(self, text: str) -> int:
        """估算token数量（简单估算）"""
        # 简单估算：中文按每4字符约1token，英文按每4字符约1token
        if len(text) == 0:
            return 0
        
        # 更准确的估算方法，考虑中英文混合
        chinese_chars = len([c for c in text if '\u4e00' <= c <= '\u9fff'])
        english_words = len([w for w in text.split() if w.isascii()])
        other_chars = len(text) - chinese_chars - len(' '.join(text.split()))
        
        # 估算：中文4字≈1token，英文单词≈1token，其他10字符≈1token
        estimated_tokens = (chinese_chars // 4) + english_words + (other_chars // 10)
        return max(1, estimated_tokens)
    
    def validate_input(self, context: str, params: Dict[str, Any] = None) -> str:
        """验证输入参数"""
        if not context or not context.strip():
            return "Context cannot be empty"
        
        if len(context) > 50000:  # 限制最大长度
            return "Context too long (max 50000 characters)"
        
        params = params or {}
        language = params.get('language', 'Chinese')
        if language not in ['Chinese', 'English']:
            return f"Unsupported language: {language}. Supported: Chinese, English"
        
        return None  # 无错误


# 便捷的执行函数，兼容现有接口
def execute(args: Dict[str, Any]) -> str:
    """
    执行上下文分析技能（兼容函数）
    """
    context = args.get('context', '') or args.get('request', '')
    if not context:
        return "Error: No context provided for analysis"
    
    # 注意：在实际使用中，这里需要真实的AI客户端和模板注册表
    # 现在我们提供一个模拟版本用于演示
    try:
        # 模拟分析结果
        mock_result = {
            'context_length': len(context),
            'token_count': max(1, len(context) // 4),
            'metrics': {
                'clarity': 0.7,
                'relevance': 0.85, 
                'completeness': 0.6,
                'consistency': 0.9,
                'efficiency': 0.8
            },
            'suggestions': [
                "增加更明确的目标描述",
                "添加约束条件说明", 
                "提高表达清晰度"
            ],
            'issues': [
                "缺少关键约束条件"
            ]
        }
        
        # 格式化输出
        output_lines = []
        output_lines.append("上下文分析结果:")
        output_lines.append(f"长度: {mock_result['context_length']} 字符")
        output_lines.append(f"Token估算: {mock_result['token_count']}")
        output_lines.append("")
        output_lines.append("五维指标分析:")
        
        for metric, score in mock_result['metrics'].items():
            metric_names = {
                'clarity': '清晰度',
                'relevance': '相关性', 
                'completeness': '完整性',
                'consistency': '一致性', 
                'efficiency': '效率'
            }
            indicator = "🟢" if score >= 0.7 else "🟡" if score >= 0.4 else "🔴"
            output_lines.append(f"  {indicator} {metric_names.get(metric, metric)}: {score:.2f}")
        
        if mock_result['suggestions']:
            output_lines.append("\n优化建议:")
            for suggestion in mock_result['suggestions']:
                output_lines.append(f"  • {suggestion}")
        
        if mock_result['issues']:
            output_lines.append("\n识别问题:")
            for issue in mock_result['issues']:
                output_lines.append(f"  • {issue}")
        
        return "\n".join(output_lines)
        
    except Exception as e:
        return f"Analysis failed: {str(e)}"