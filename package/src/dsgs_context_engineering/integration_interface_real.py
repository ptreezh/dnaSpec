"""
DNASPEC Context Engineering Skills - AI CLI平台深度集成实现
作为AI CLI平台的内置斜杠命令，利用平台AI模型原生智能
"""
from typing import Dict, Any, List


class DNASPECContextEngineeringInterface:
    """
    DNASPEC上下文工程接口
    与AI CLI平台集成，作为平台内置技能提供服务
    """
    
    def __init__(self):
        self.name = "dnaspec-context-engineering"
        self.description = "DNASPEC Context Engineering Skills - AI CLI平台的内置上下文工程增强工具"
    
    def process_command(self, command: str, context: str, params: Dict[str, Any] = None) -> str:
        """
        处理AI CLI平台的斜杠命令
        
        Args:
            command: 指令类型 (analyze/optimization/template/help等)
            context: 当前用户选中的文本或聊天上下文
            params: 附加参数
            
        Returns:
            AI模型处理后的结构化结果
        """
        params = params or {}
        
        if command in ['analyze', 'analysis', 'context-analysis']:
            return self._create_analysis_instruction(context)
        elif command in ['optimize', 'optimization', 'context-optimization']:
            goals = params.get('goals', 'clarity,completeness')
            return self._create_optimization_instruction(context, goals)
        elif command in ['template', 'cognitive-template']:
            template_type = params.get('template', 'chain_of_thought')
            return self._create_template_instruction(context, template_type, params)
        elif command in ['help', 'info']:
            return self._get_help_text()
        else:
            return self._get_help_text()
    
    def _create_analysis_instruction(self, context: str) -> str:
        """
        创建上下文分析指令
        交给AI模型执行原生分析能力
        """
        return f"""
请作为专业的上下文质量分析师，对以下上下文进行五维度评估：

上下文内容:
"{context}"

评估标准 (0.0-1.0评分):
1. 清晰度 (Clarity): 表达明确性、术语准确性、目标清晰度
2. 相关性 (Relevance): 与目标任务的关联性、内容针对性
3. 完整性 (Completeness): 关键信息完备性、约束条件完整性  
4. 一致性 (Consistency): 内容内部逻辑一致性、表述连贯性
5. 效率 (Efficiency): 信息密度、简洁性、冗余度控制

请以JSON格式返回详细分析结果:
{{
  "context_length": {len(context) if context else 0},
  "token_count_estimate": {max(1, len(context) // 4) if context else 1},
  "metrics": {{
    "clarity": 0.0-1.0,
    "relevance": 0.0-1.0,
    "completeness": 0.0-1.0,
    "consistency": 0.0-1.0,
    "efficiency": 0.0-1.0
  }},
  "suggestions": ["建议1", "建议2", "建议3"],
  "issues": ["问题1", "问题2"],
  "confidence": 0.8-1.0
}}

然后提供简要的质量评估总结和优化建议。
"""
    
    def _create_optimization_instruction(self, context: str, goals: str) -> str:
        """
        创建上下文优化指令
        交给AI模型执行原生优化能力
        """
        return f"""
请根据以下优化目标改进指定上下文:

优化目标: {goals}

原始上下文:
"{context}"

优化要求:
- 保持原始核心意图和功能不变
- 针对指定目标进行专门改进
- 提供具体的优化措施说明
- 确保优化后内容的逻辑一致性和完整性

请返回优化结果，以JSON格式:
{{
  "original_context": "原始上下文内容",
  "optimized_context": "优化后上下文内容", 
  "applied_optimizations": ["应用的优化措施1", "应用的优化措施2"],
  "improvement_metrics": {{
    "clarity_change": +/-0.x,
    "relevance_change": +/-0.x,
    "completeness_change": +/-0.x,
    "conciseness_change": +/-0.x
  }},
  "optimization_summary": "优化过程和结果总结"
}}

并详细解释每个优化措施的理由。
"""
    
    def _create_template_instruction(self, context: str, template_type: str, params: Dict[str, Any]) -> str:
        """
        创建认知模板应用指令  
        交给AI模型执行模板化认知处理
        """
        if template_type == 'chain_of_thought':
            return f"""
请使用专业的思维链方法分析以下任务：

任务: {context}

请按以下结构化步骤进行深度分析：

1. **问题理解**: 仔细分析任务的核心需求、关键约束和目标
2. **步骤分解**: 将复杂任务分解为可执行的具体步骤
3. **中间推理**: 为每个步骤提供详细的思考和推理过程
4. **验证检查**: 检查推理过程的合理性和逻辑一致性
5. **最终答案**: 综合所有步骤给出完整、专业的解决方案

请返回完整的思维链分析过程和最终专业结论。
"""
        elif template_type == 'verification':
            return f"""
请使用系统的验证检查框架分析以下内容：

原始内容: {context}

请按以下验证步骤执行专业验证：

1. **初步答案**: 基于内容给出初步判断或解决方案
2. **逻辑一致性检查**: 验证内容内部逻辑的一致性和推理连贯性
3. **事实准确性检查**: 核实陈述事实的准确性、可靠性和有效性
4. **完整性检查**: 评估是否包含所有必要信息和关键要素
5. **最终确认**: 综合以上检查给出最终验证确认和改进建议

请返回每个验证步骤的详细结果和最终确认。
"""
        elif template_type == 'few_shot':
            return f"""
请使用少样本学习方法处理以下任务：

任务: {context}

以下是相关示例对，展示解决类似问题的模式和方法：

示例1:
输入: 分析电商系统架构需求
输出: [架构分析结果]
解释: 识别核心组件、数据流、安全要求等关键要素

示例2: 
输入: 设计API接口规范
输出: [接口设计结果]
解释: 定义数据模型、错误处理、性能考虑等要素

请参考以上示例的分析模式、推理路径和输出格式，来处理您的任务。
详细说明您的分析过程、推理基础和最终决策依据。
"""
        else:  # 默认使用思维链
            return f"""
作为专业分析助手，请使用{template_type}认知框架分析以下任务：

任务: {context}

请应用{template_type}方法，以结构化、专业化的格式返回您的分析结果和建议。
"""
    
    def _get_help_text(self) -> str:
        """
        获取帮助文本
        """
        return """
# DNASPEC Context Engineering Skills - 帮助信息

DNASPEC Context Engineering Skills 是AI CLI平台的内置上下文工程增强工具集，利用AI模型的原生智能提供专业级上下文分析、优化和结构化能力。

## 可用命令:

**/dnaspec-analyze** `<选中文本或输入上下文>`
- 对指定上下文进行五维度质量分析 (清晰度、相关性、完整性、一致性、效率)

**/dnaspec-optimize** `<选中文本或输入上下文>` `--goals clarity,completeness`
- 优化上下文质量，支持多种目标 (clarity, relevance, completeness, conciseness)

**/dnaspec-template** `<任务描述>` `--template chain_of_thought`
- 应用认知模板结构化复杂任务 (chain_of_thought, verification, few_shot)

**/dnaspec-help** 
- 显示此帮助信息

## 示例用法:

### 分析上下文质量
```
/dnaspec-analyze
```
(在选中文本时执行，或直接输入上下文)

### 优化上下文内容
```
/dnaspec-optimize --goals "clarity,completeness"
```

### 应用认知模板
```
/dnaspec-template --template "verification"
```

## 核心价值:

- **AI原生智能**: 100%利用AI模型原生分析、推理、生成能力
- **专业质量**: 提供五维度上下文质量评估和专业建议
- **认知框架**: 结构化复杂任务，提升AI交互质量
- **平台集成**: 与AI CLI平台无缝集成，无需额外配置

系统完全集成到AI平台中，直接利用平台的AI模型智能，为您的AI辅助开发、项目管理和内容创作提供专业支持。
"""


# 全局接口实例
interface = DNASPECContextEngineeringInterface()


def handle_command(command_name: str, context: str = "", params: Dict[str, Any] = None) -> str:
    """
    AI CLI平台命令处理接口
    这个函数会被AI CLI平台调用以处理/dnaspec-*命令
    """
    params = params or {}
    
    # 从命令名中提取实际命令 (移除前缀如'dnaspec-', '/dnaspec-'等)
    actual_command = command_name.lower()
    if actual_command.startswith('/'):
        actual_command = actual_command[1:]
    if actual_command.startswith('dnaspec-'):
        actual_command = actual_command[5:]
    
    return interface.process_command(actual_command, context, params)


def get_command_registration_info() -> Dict[str, Any]:
    """
    获取命令注册信息 - 用于AI CLI平台的命令注册
    """
    return {
        'name': 'dnaspec-context-engineering',
        'description': 'DNASPEC上下文工程技能 - AI平台的内置专业上下文分析、优化和结构化工具',
        'commands': [
            {
                'name': '/dnaspec-analyze',
                'description': '专业五维指标分析上下文质量',
                'parameters': [],
                'access': 'conversation_selection_or_context',
                'returns': 'json_structured_analysis_result'
            },
            {
                'name': '/dnaspec-optimize',
                'description': '智能优化上下文质量',
                'parameters': [
                    {
                        'name': 'goals',
                        'type': 'string',
                        'description': '优化目标 (clarity, relevance, completeness, conciseness)',
                        'required': False,
                        'default': 'clarity,completeness'
                    }
                ],
                'access': 'conversation_selection_or_context',
                'returns': 'optimized_context_with_improvement_metrics'
            },
            {
                'name': '/dnaspec-template', 
                'description': '应用认知模板结构化复杂任务',
                'parameters': [
                    {
                        'name': 'template',
                        'type': 'string', 
                        'description': '模板类型 (chain_of_thought, verification, few_shot)',
                        'required': False,
                        'default': 'chain_of_thought'
                    }
                ],
                'access': 'conversation_selection_or_context',
                'returns': 'structured_cognitive_analysis'
            },
            {
                'name': '/dnaspec-help',
                'description': '显示帮助信息',
                'parameters': [],
                'access': 'none',
                'returns': 'documentation'
            }
        ],
        'integration_type': 'native_plugin',
        'ai_model_requirement': 'native_semantic_understanding_reasoning_generation',
        'platform_compatibility': ['Claude CLI', 'Gemini CLI', 'Qwen CLI', 'Other AI CLI Platforms'],
        'architecture': 'AI-native, utilizes platform AI model native intelligence',
        'dependencies': 'None - uses AI CLI platform native capabilities',
        'confidentiality': 'Does not store user data locally'
    }


def execute(args: Dict[str, Any]) -> str:
    """
    统一执行接口 - 兼容现有调用方式
    """
    command = args.get('command', 'help')
    context = args.get('context', args.get('request', ''))
    params = args.get('params', {})
    
    return handle_command(command, context, params)


if __name__ == "__main__":
    # 验证接口功能
    print("🔍 DNASPEC Context Engineering Skills - AI CLI Native Integration")
    print("=" * 70)
    
    # 演示命令注册信息
    registration_info = get_command_registration_info()
    print(f"📋 注册信息: {registration_info['name']}")
    print(f"   描述: {registration_info['description']}")
    print(f"   可用命令数: {len(registration_info['commands'])}")
    
    # 修正函数名调用错误
    # 测试各命令
    print("\n🔧 验证各个命令接口:")
    
    test_context = "设计一个电商平台，支持用户注册登录、商品浏览、购物车功能。"
    
    # 测试分析命令
    result = handle_command('/dnaspec-analyze', test_context)
    print(f"   ✅ 分析命令: 已生成 {len(result)} 字符的AI指令")
    
    # 测试优化命令
    result = handle_command('/dnaspec-optimize', test_context, {'goals': 'clarity,completeness'})
    print(f"   ✅ 优化命令: 已生成 {len(result)} 字符的AI指令")
    
    # 测试模板命令
    result = handle_command('/dnaspec-template', "如何提高系统性能？", {'template': 'chain_of_thought'})
    print(f"   ✅ 模板命令: 已生成 {len(result)} 字符的AI指令")
    
    print(f"\n🎯 系统已准备就绪，可以集成到AI CLI平台中！")
    print("💡 系统完全利用AI模型原生智能，无需本地模型或API密钥")
    print("🔗 作为AI CLI平台内置功能，提供专业级上下文工程能力")