"""
Cognitive Template Skill
应用认知模板到AI交互中的技能
"""
from typing import Dict, Any
from ..core_skill import ContextEngineeringSkill, SkillResult
from ..ai_client import AIModelClient
from ..instruction_template import TemplateRegistry


class CognitiveTemplateSkill(ContextEngineeringSkill):
    """认知模板技能 - 将认知模板应用于AI交互以提升推理质量"""
    
    def __init__(self, ai_client: AIModelClient, template_registry: TemplateRegistry):
        super().__init__(
            name="dsgs-cognitive-template",
            description="认知模板技能 - 应用认知模板提升AI推理质量",
            ai_client=ai_client,
            template_registry=template_registry
        )
    
    def execute(self, context: str, params: Dict[str, Any] = None) -> SkillResult:
        """执行认知模板应用"""
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
        
        template_type = params.get('template', 'chain_of_thought')
        language = params.get('language', 'Chinese')
        role = params.get('role', 'expert')
        
        # 构造模板应用指令
        instruction = self.template_registry.create_prompt(
            'cognitive-template',
            context,
            {
                'template_type': template_type,
                'language': language,
                'role': role
            }
        )
        
        # 发送到AI模型
        response = self.ai_client.send_instruction(instruction)
        
        # 解析AI响应
        try:
            parsed_result = self.template_registry.parse_response('cognitive-template', response)
            
            return SkillResult(
                success=True,
                data={
                    'template_type': template_type,
                    'enhanced_context': parsed_result.get('enhanced_context', response),
                    'applied_structure': parsed_result.get('structure', []),
                    'success': parsed_result.get('success', True),
                    'raw_response': response
                },
                confidence=0.9  # 模板应用通常有较高置信度
            )
            
        except Exception as e:
            return SkillResult(
                success=False,
                data={'raw_response': response},
                error=f"Failed to parse template response: {str(e)}"
            )
    
    def validate_input(self, context: str, params: Dict[str, Any] = None) -> str:
        """验证输入参数"""
        if not context or not context.strip():
            return "Context cannot be empty"
        
        if len(context) > 30000:  # 限制最大长度
            return "Context too long (max 30000 characters)"
        
        params = params or {}
        template_type = params.get('template', 'chain_of_thought')
        
        valid_templates = {
            'chain_of_thought', 'few_shot', 'verification', 
            'role_playing', 'understanding', 'problem_solving'
        }
        
        if template_type not in valid_templates:
            return f"Invalid template type: {template_type}. Valid: {list(valid_templates)}"
        
        language = params.get('language', 'Chinese')
        if language not in ['Chinese', 'English']:
            return f"Unsupported language: {language}. Supported: Chinese, English"
        
        return None  # 无错误


def execute(args: Dict[str, Any]) -> str:
    """
    执行认知模板应用技能（兼容函数）
    """
    context = args.get('context', '') or args.get('request', '')
    template_type = args.get('template', 'chain_of_thought')
    role = args.get('role', 'expert')
    
    if not context:
        return "Error: No context provided for template application"
    
    valid_templates = {
        'chain_of_thought': '思维链',
        'few_shot': '少示例学习', 
        'verification': '验证检查',
        'role_playing': '角色扮演',
        'understanding': '理解框架',
        'problem_solving': '问题解决'
    }
    
    if template_type not in valid_templates:
        return f"Error: Invalid template type '{template_type}'. Valid types: {list(valid_templates.keys())}"
    
    # 模拟模板应用结果（实际实现中会调用AI模型）
    template_names = {
        'chain_of_thought': '思维链',
        'few_shot': '少示例学习',
        'verification': '验证检查', 
        'role_playing': '角色扮演',
        'understanding': '理解框架',
        'problem_solving': '问题解决'
    }
    
    mock_enhanced_context = f"""
### {template_names[template_type]} 框架应用

**原始请求**: {context}

**{role}视角分析**:
[在此处应用{template_names[template_type]}认知框架进行分析]

**结构化输出**:
1. [步骤1]
2. [步骤2] 
3. [步骤3]

**结论**:
[基于{template_names[template_type]}框架得出的结论]
""".strip()
    
    result = {
        'template_type': template_type,
        'template_chinese_name': template_names[template_type],
        'enhanced_context': mock_enhanced_context,
        'success': True,
        'raw_response': f"SIMULATED_RESPONSE_APPLYING_{template_type.upper()}_TEMPLATE"
    }
    
    # 格式化输出
    output_lines = []
    output_lines.append(f"应用认知模板: {result['template_type']} ({result['template_chinese_name']})")
    output_lines.append("=" * 60)
    output_lines.append("")
    output_lines.append("结构化后的上下文:")
    output_lines.append(result['enhanced_context'])
    
    return "\n".join(output_lines)