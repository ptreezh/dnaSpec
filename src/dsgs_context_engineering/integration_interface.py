"""
DSGS Context Engineering Skills - AI CLI平台集成实现
正确实现为AI CLI平台的内置斜杠命令，利用AI模型的原生智能
"""
import json
import re
from typing import Dict, Any, List
from abc import ABC, abstractmethod


class DSGSSkillInterface:
    """
    DSGS斜杠命令接口
    与AI CLI平台集成，作为平台内置命令
    """
    
    def __init__(self, platform_context: Dict[str, Any] = None):
        """
        初始化接口，使用AI CLI平台的上下文和配置
        """
        self.platform_context = platform_context or {}
        self.name = "dsgs-context-engineering"
        self.description = "DSGS Context Engineering Skills - AI CLI平台的内置上下文工程增强工具"
    
    def execute_skill(self, command: str, args: List[str], message_context: str) -> str:
        """
        执行技能 - 与AI CLI平台集成的入口点
        
        Args:
            command: 命令类型 (如: analyze, optimize, template)
            args: 命令参数列表
            message_context: 当前会话上下文（用户可以选择的文本或整个对话历史）
            
        Returns:
            命令执行结果字符串
        """
        # 如果用户没有提供具体上下文，使用当前会话上下文
        target_context = " ".join(args) if args else message_context
        
        if not target_context.strip():
            return "错误: 请提供要处理的上下文或在对话框中选择文本"
        
        # 根据命令类型执行相应功能
        if command in ['analyze', 'analysis', 'context-analysis']:
            return self._handle_analysis_command(target_context)
        elif command in ['optimize', 'optimization', 'context-optimization']:
            return self._handle_optimization_command(target_context, args)
        elif command in ['template', 'cognitive-template']:
            return self._handle_template_command(target_context, args)
        elif command in ['help', 'info']:
            return handle_help_command()
        else:
            return handle_help_command()


    def _handle_analysis_command(self, target_context: str) -> str:
        """
        处理分析命令
        直接向AI模型发送分析指令，利用AI的原生分析能力
        """
        analysis_instruction = f"""
请作为专业的上下文质量分析师，对以下上下文进行五维度评估：

上下文内容:
"{target_context}"

请从以下五个维度进行专业评估（0.0-1.0评分）：

1. 清晰度 (Clarity): 表达明确性，术语准确性，目标清晰度
2. 相关性 (Relevance): 与目标任务的关联性，内容针对性
3. 完整性 (Completeness): 关键信息完备性，约束条件完整性  
4. 一致性 (Consistency): 内容内部的逻辑一致性，表述连贯性
5. 效率 (Efficiency): 信息密度，简洁性，冗余度控制

请返回JSON格式的专业分析结果：
{{
  "context_length": {len(target_context)},
  "token_count_estimate": {max(1, len(target_context) // 4)},
  "metrics": {{
    "clarity": 0.0-1.0,
    "relevance": 0.0-1.0,
    "completeness": 0.0-1.0,
    "consistency": 0.0-1.0,
    "efficiency": 0.0-1.0
  }},
  "suggestions": ["建议1", "建议2", "建议3"],
  "issues": ["问题1", "问题2"]
}}

然后提供简要的质量评估总结。
"""
        
        # 将分析指令交给AI模型处理（通过平台内置机制）
        # 在AI CLI平台中，这会触发AI模型进行分析
        return analysis_instruction


    def _handle_optimization_command(self, target_context: str, args: List[str]) -> str:
        """
        处理优化命令
        利用AI模型的原生推理和生成能力进行上下文优化
        """
        # 检查是否有优化目标参数
        optimization_goals = ['clarity', 'completeness']  # 默认目标
        if len(args) > 1:  # 如果用户提供了上下文后还有其他参数
            # 这里需要更复杂的参数解析，假设最后一个非上下文参数是优化目标
            possible_goals = ' '.join(args[1:]) if len(args) > 1 else ''
            if possible_goals and any(g in possible_goals for g in ['clarity', 'relevance', 'completeness', 'conciseness']):
                optimization_goals = [g.strip() for g in possible_goals.split(',') if g.strip()]
        
        optimization_instruction = f"""
请根据以下目标优化指定的上下文内容：

优化目标: {', '.join(optimization_goals)}

原始上下文:
"{target_context}"

请返回优化后的上下文内容和详细的改进措施说明，以JSON格式：
{{
  "original_context": "原始上下文内容",
  "optimized_context": "优化后的上下文内容", 
  "applied_optimizations": ["应用的优化措施1", "应用的优化措施2"],
  "improvement_metrics": {{
    "clarity_change": +/-0.x,
    "relevance_change": +/-0.x,
    "completeness_change": +/-0.x,
    "conciseness_change": +/-0.x
  }}
}}

请保持原始的核心意图不变，仅针对指定目标进行优化改进。
"""
        
        # 将优化指令交给AI模型处理
        return optimization_instruction


    def _handle_template_command(self, target_context: str, args: List[str]) -> str:
        """
        处理认知模板命令  
        利用AI模型的原生推理能力应用认知模板
        """
        import sys
        
        # 解析模板参数
        template = 'chain_of_thought'  # 默认模板
        if len(args) > 1:  # 如果有额外参数
            possible_template = args[1].lower() if args else ''
            valid_templates = ['chain_of_thought', 'few_shot', 'verification', 'role_playing', 'understanding']
            if possible_template in valid_templates:
                template = possible_template
        
        # 定义不同认知模板的指令
        template_instructions = {
            'chain_of_thought': f"""
请使用思维链方法深度分析以下任务：

原始任务: {target_context}

请按以下思维链步骤进行专业分析：
1. **问题理解**: 明确任务的核心需求、约束和目标
2. **步骤分解**: 将任务分解为可执行的具体步骤
3. **中间推理**: 在每个步骤中提供详细思考和推理过程
4. **验证检查**: 检查推理过程的合理性和逻辑一致性
5. **最终答案**: 综合所有分析步骤给出完整的最终解决方案

请以结构化格式返回完整的思维链分析过程和专业结果。
""",
            'few_shot': f"""
请使用少样本学习方法处理以下任务：

任务: {target_context}

以下是相关的示例对，展示了解决类似任务的模式：

示例1:
输入: 分析电商平台架构需求
输出: [架构分析示例]
解释: 识别核心组件、数据流、安全要求等

示例2:
输入: 设计API接口规范  
输出: [接口设计示例]
解释: 定义数据模型、错误处理、性能考虑等

请参考以上示例的思维模式、推理路径和输出格式，来处理您的任务。
详细说明您的分析过程和决策依据。
""",
            'verification': f"""
请使用验证检查框架分析以下内容：

原始内容: {target_context}

请执行以下验证检查步骤：
1. **初步答案**: 基于原始内容给出初步判断或解决方案
2. **逻辑一致性检查**: 验证内容内部的逻辑一致性和推理连贯性
3. **事实准确性检查**: 核实陈述事实的准确性、可靠性和有效性
4. **完整性检查**: 评估是否包含所有必要信息和关键要素
5. **最终确认**: 综合以上检查给出最终验证结论和改进建议

请返回每个验证步骤的详细结果和最终确认。
""",
            'role_playing': f"""
请以{args[2] if len(args) > 2 else '专家'}的专业身份和视角分析以下任务：

任务: {target_context}

请基于{args[2] if len(args) > 2 else '专家'}的专业知识、经验和技能进行分析：
1. **角色理解**: 作为{args[2] if len(args) > 2 else '专家'}，我具备以下专业能力...
2. **专业分析**: 从专业视角分析任务的关键要素和考虑点
3. **专业建议**: 基于专业知识提供具体、可行的建议和方案
4. **专业决策**: 从专业视角给出最优决策推荐和风险评估

请返回{args[2] if len(args) > 2 else '专家'}视角的专业分析、建议和决策。
""",
            'understanding': f"""
请使用深度理解框架分析以下内容：

分析内容: {target_context}

请从以下维度进行专业的深度理解：
1. **核心目标**: 此任务的主要目的和预期成果是什么？
2. **关键要素**: 包含哪些重要的组成部分和核心要求？
3. **约束条件**: 有哪些限制条件和前置假设？
4. **成功标准**: 如何判断任务完成得优秀？
5. **潜在风险**: 可能存在哪些挑战和风险因素？

请返回深度理解结果和相关专业建议。
"""
        }
        
        return template_instructions.get(template, template_instructions['chain_of_thought'])


        return help_text


def handle_help_command() -> str:
    """
    处理帮助命令
    """
    help_text = """
## DSGS Context Engineering Skills - 帮助信息

DSGS Context Engineering Skills 是AI CLI平台的内置上下文工程增强工具集，利用AI模型的原生智能提供专业级上下文分析、优化和认知模板应用。

### 可用命令:

**/dsgs-analyze** `上下文内容`
- 对指定上下文进行五维度质量分析 (清晰度、相关性、完整性、一致性、效率)

**/dsgs-optimize** `上下文内容` `[优化目标]`
- 优化上下文质量，支持多种优化目标 (clarity, completeness, relevance, conciseness)

**/dsgs-template** `任务描述` `[模板类型]`
- 应用认知模板结构化复杂任务，支持多种模板 (chain_of_thought, few_shot, verification, role_playing, understanding)

**/dsgs-help** 
- 显示此帮助信息

### 示例用法:
```
/dsgs-analyze 设计一个电商平台，支持用户登录、商品浏览、购物车功能
/dsgs-optimize 系统需要处理订单 clarity,completeness
/dsgs-template 如何提高系统安全性？ verification
```

系统完全集成到AI CLI平台中，无需额外配置，直接利用平台的AI模型原生智能。
    """
    
    return help_text


# 全局命令处理器实例（模拟AI CLI平台集成）
slash_command_handler = DSGSSlashCommandInterface()


def handle_command(command_name: str, arguments: List[str], platform_context: str) -> str:
    """
    AI CLI平台命令处理入口函数
    这个函数会被AI CLI平台调用以处理斜杠命令
    """
    # 从命令名称中提取具体操作（如 analyze, optimize, template）
    if command_name.startswith('/dsgs-'):
        actual_command = command_name[6:]  # 去掉 '/dsgs-' 前缀
    else:
        actual_command = command_name
    
    return slash_command_handler.execute_slash_command(actual_command, arguments, platform_context)


def get_command_info() -> Dict[str, Any]:
    """
    获取命令信息 - 用于AI CLI平台的命令注册
    """
    return {
        'name': 'dsgs-context-engineering',
        'commands': [
            {
                'name': '/dsgs-analyze',
                'description': '分析上下文质量的五维指标',
                'usage': '/dsgs-analyze <上下文内容>',
                'access': 'conversation_context',  # 可以访问当前对话上下文
                'permissions': ['read_conversation']
            },
            {
                'name': '/dsgs-optimize', 
                'description': '优化上下文质量，支持多目标',
                'usage': '/dsgs-optimize <上下文内容> [优化目标]',
                'access': 'conversation_context',
                'permissions': ['read_conversation']
            },
            {
                'name': '/dsgs-template',
                'description': '应用认知模板结构化复杂任务',
                'usage': '/dsgs-template <任务描述> [模板类型]',
                'access': 'conversation_context', 
                'permissions': ['read_conversation']
            },
            {
                'name': '/dsgs-help',
                'description': '显示DSGS Context Engineering Skills帮助信息',
                'usage': '/dsgs-help',
                'access': 'none',
                'permissions': []
            }
        ],
        'integration': 'Built into AI CLI platform',
        'architecture': 'AI-native, utilizes platform AI model native intelligence',
        'dependencies': 'None - uses AI CLI platform capabilities'
    }


# Claude CLI、Gemini CLI等平台的命令注册接口（示例）
def register_with_cli_platform():
    """
    向AI CLI平台注册命令
    这个函数会被平台调用以注册DSGS命令
    """
    command_info = get_command_info()
    print(f"Registering DSGS Context Engineering Commands with AI CLI Platform:")
    for cmd in command_info['commands']:
        print(f"  - {cmd['name']}: {cmd['description']}")
    
    return command_info


if __name__ == "__main__":
    # 演示集成模式
    print("DSGS Context Engineering Skills - AI CLI Platform Integration Demo")
    print("="*70)
    
    info = register_with_cli_platform()
    print(f"\\n✅ {len(info['commands'])} 个斜杠命令已注册到AI CLI平台")
    print("💡 系统现在作为AI CLI平台的内置工具可用")
    print("🎯 无需额外AI API密钥，直接利用平台AI智能")
    print("🚀 用户可通过 /dsgs-<command> 直接调用专业上下文工程功能")