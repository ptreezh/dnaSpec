"""
DNASPEC Context Engineering Skills - 基于AI CLI原生命令系统的实现
重新设计为可在AI CLI平台中直接注册使用的命令集
"""
from typing import Dict, Any, List, Union
import json
import re
from abc import ABC, abstractmethod


class DNASPECCommandContext:
    """
    DNASPEC命令上下文
    在AI CLI环境中运行时可访问的上下文信息
    """
    
    def __init__(self, 
                 current_conversation: List[Dict[str, str]] = None,
                 selected_text: str = "",
                 current_cursor_position: int = 0,
                 user_preferences: Dict[str, Any] = None):
        self.current_conversation = current_conversation or []
        self.selected_text = selected_text
        self.current_cursor_position = current_cursor_position
        self.user_preferences = user_preferences or {}
    
    def get_full_conversation_context(self) -> str:
        """获取完整对话上下文作为字符串"""
        context_parts = []
        for message in self.current_conversation:
            role = message.get('role', 'user')
            content = message.get('content', '')
            context_parts.append(f"[{role}]: {content}")
        return "\n".join(context_parts)
    
    def get_recent_messages(self, num_messages: int = 5) -> List[Dict[str, str]]:
        """获取最近的几条消息"""
        return self.current_conversation[-num_messages:]
    
    def get_message_at_cursor(self) -> str:
        """获取光标位置的消息（如果有）"""
        if self.selected_text:
            return self.selected_text
        elif self.current_conversation:
            # 返回最近一条消息作为默认处理对象
            return self.current_conversation[-1].get('content', '')
        return ""


class DNASPECCommand(ABC):
    """
    DNASPEC命令抽象基类
    所有DNASPEC命令都需要继承此类
    """
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, context: DNASPECCommandContext, args: List[str]) -> str:
        """
        执行命令
        Args:
            context: 命令执行上下文（包含AI会话信息）
            args: 命令参数列表
        Returns:
            命令执行结果（将显示在AI聊天中）
        """
        pass


class ContextAnalysisCommand(DNASPECCommand):
    """
    上下文分析命令
    对当前对话上下文进行质量分析
    """
    
    def __init__(self):
        super().__init__(
            name="/dnaspec-analyze",
            description="分析当前对话或所选内容的上下文质量"
        )
    
    def execute(self, context: DNASPECCommandContext, args: List[str]) -> str:
        """执行上下文分析"""
        # 确定要分析的内容
        content_to_analyze = context.get_message_at_cursor()
        if not content_to_analyze:
            content_to_analyze = context.get_full_conversation_context()
        
        if not content_to_analyze.strip():
            return "❌ 错误：没有可分析的上下文内容。请在对话中输入内容后再使用此命令。"
        
        # 检查是否指定了特定分析目标
        analysis_target = " ".join(args) if args else content_to_analyze
        
        # 构造AI指令来分析上下文
        analysis_instruction = f"""
请对以下上下文进行专业分析，评估其质量：

上下文：
"{analysis_target}"

请按照以下五个维度进行评估：
1. 清晰度 (Clarity): 内容表述的明确程度 (0-1分)
2. 相关性 (Relevance): 与目标任务的相关程度 (0-1分)  
3. 完整性 (Completeness): 关键信息的完备程度 (0-1分)
4. 一致性 (Consistency): 内容之间的逻辑一致性 (0-1分)
5. 效率 (Efficiency): 信息密度和简洁性 (0-1分)

请以JSON格式返回分析结果：
{{  
  "metrics": {{
    "clarity": 数值,
    "relevance": 数值,
    "completeness": 数值, 
    "consistency": 数值,
    "efficiency": 数值
  }},
  "suggestions": ["建议1", "建议2", "建议3"],
  "issues": ["问题1", "问题2"]
}}

然后提供一段总结性的文字分析。
"""
        
        # 返回分析指令，由AI模型执行
        return analysis_instruction


class ContextOptimizationCommand(DNASPECCommand):
    """
    上下文优化命令
    优化当前对话或所选内容的上下文质量
    """
    
    def __init__(self):
        super().__init__(
            name="/dnaspec-optimize",
            description="优化当前对话或所选内容的上下文质量"
        )
    
    def execute(self, context: DNASPECCommandContext, args: List[str]) -> str:
        """执行上下文优化"""
        content_to_optimize = context.get_message_at_cursor()
        if not content_to_optimize:
            content_to_optimize = context.get_full_conversation_context()
        
        if not content_to_optimize.strip():
            return "❌ 错误：没有可优化的上下文内容。请在对话中输入内容后再使用此命令。"
        
        # 解析优化目标参数
        goals = args if args else ['clarity', 'completeness']
        valid_goals = ['clarity', 'relevance', 'completeness', 'conciseness', 'consistency']
        
        invalid_goals = [g for g in goals if g not in valid_goals]
        if invalid_goals:
            return f"❌ 错误：无效的优化目标：{invalid_goals}。有效目标：{valid_goals}"
        
        # 构造优化指令
        optimization_instruction = f"""
请优化以下内容的{', '.join(goals)}：

原始内容：
"{content_to_optimize}"

请返回：
1. 优化后的上下文内容
2. 应用了哪些优化改进
3. 与原内容相比的改进说明

请保持原意不变，仅在{', '.join(goals)}方面进行改进。
"""
        
        return optimization_instruction


class CognitiveTemplateCommand(DNASPECCommand):
    """
    认知模板命令
    应用认知模板到当前对话内容
    """
    
    def __init__(self):
        super().__init__(
            name="/dnaspec-template",
            description="应用认知模板到当前对话内容（思维链、验证等）"
        )
    
    def execute(self, context: DNASPECCommandContext, args: List[str]) -> str:
        """执行认知模板应用"""
        content = context.get_message_at_cursor()
        if not content:
            content = context.get_full_conversation_context()
        
        if not content.strip():
            return "❌ 错误：没有可应用模板的内容。请在对话中输入内容后再使用此命令。"
        
        # 解析模板类型参数
        template_type = args[0] if args else 'chain_of_thought'
        valid_templates = [
            'chain_of_thought',    # 思维链
            'few_shot',           # 少样本学习  
            'verification',       # 验证检查
            'role_playing',       # 角色扮演
            'understanding'       # 理解框架
        ]
        
        if template_type not in valid_templates:
            return f"❌ 错误：无效的模板类型：{template_type}。有效类型：{valid_templates}"
        
        # 构造模板应用指令
        template_instructions = {
            'chain_of_thought': f"""
请使用思维链方法分析以下任务：

任务：{content}

请按以下步骤进行分析：
1. 问题理解：明确任务的核心需求
2. 步骤分解：将任务分解为可执行的步骤
3. 中间推理：在每个步骤中提供详细思考
4. 验证检查：检查每步推理的合理性
5. 最终答案：综合所有步骤给出最终结果

请以结构化格式返回分析过程和结果。
""",
            'few_shot': f"""
请使用少样本学习方法处理以下任务：

任务：{content}

以下是相关示例：
示例1: 输入X，输出Y（因为...）
示例2: 输入A，输出B（因为...）

请参考以上示例模式，处理您的任务，并解释您的推理过程。
""",
            'verification': f"""
请使用验证框架分析以下内容：

原始内容：{content}

请执行以下验证步骤：
1. 初步答案：基于内容给出初始判断
2. 逻辑一致性检查：验证内容的内在逻辑
3. 事实准确性检查：核对事实性陈述的准确性 
4. 完整性检查：评估信息的完备性
5. 最终确认：综合以上检查给出最终确认

请返回验证过程和最终结论。
""",
            'role_playing': f"""
请以特定角色的视角分析以下内容：

内容：{content}
角色：[根据内容类型自动确定，如：系统架构师、产品经理、技术专家等]

请从指定角色的专业角度分析该内容，提供专业的见解和建议。
""",
            'understanding': f"""
请深度理解以下内容：

内容：{content}

请从以下角度进行理解：
1. 核心目标：内容的主要目的是什么？
2. 关键要素：包含哪些重要组成部分？
3. 约束条件：有哪些限制和要求？
4. 成功标准：如何判断任务完成得好？
5. 潜在风险：可能存在哪些挑战？

请返回深度理解结果。
"""
        }
        
        return template_instructions[template_type]


class DNASPECCommandRegistry:
    """
    DNASPEC命令注册表
    管理所有可用的DNASPEC命令
    """
    
    def __init__(self):
        self.commands: Dict[str, DNASPECCommand] = {}
        self._register_default_commands()
    
    def _register_default_commands(self):
        """注册默认命令"""
        commands = [
            ContextAnalysisCommand(),
            ContextOptimizationCommand(), 
            CognitiveTemplateCommand()
        ]
        
        for cmd in commands:
            self.register_command(cmd)
    
    def register_command(self, command: DNASPECCommand):
        """注册命令"""
        self.commands[command.name] = command
    
    def execute_command(self, command_name: str, context: DNASPECCommandContext, args: List[str] = None) -> str:
        """执行命令"""
        if command_name not in self.commands:
            available_commands = list(self.commands.keys())
            return f"❌ 错误：未知命令 '{command_name}'。可用命令：{', '.join(available_commands)}"
        
        if args is None:
            args = []
        
        command = self.commands[command_name]
        try:
            result = command.execute(context, args)
            return result
        except Exception as e:
            return f"❌ 命令执行错误：{str(e)}"
    
    def get_command_help(self, command_name: str = None) -> str:
        """获取命令帮助信息"""
        if command_name and command_name in self.commands:
            cmd = self.commands[command_name]
            return f"{cmd.name} - {cmd.description}"
        elif command_name:
            return f"❌ 未知命令：{command_name}"
        else:
            help_text = "DNASPEC Context Engineering Skills 可用命令：\n"
            for name, cmd in self.commands.items():
                help_text += f"  {name} - {cmd.description}\n"
            help_text += "\n用法示例：\n"
            help_text += "  /dnaspec-analyze - 分析当前对话的上下文质量\n"
            help_text += "  /dnaspec-optimize clarity completeness - 优化清晰度和完整性\n" 
            help_text += "  /dnaspec-template chain_of_thought - 应用思维链模板\n"
            return help_text


# Claude Commands兼容接口
def handle_command(command_name: str, args: List[str], context_data: Dict[str, Any]) -> str:
    """
    Claude Commands处理接口
    这是Claude Commands SDK调用的入口函数
    """
    # 从context_data构建DNASPEC命令上下文
    command_context = DNASPECCommandContext(
        current_conversation=context_data.get('conversation_history', []),
        selected_text=context_data.get('selected_text', ''),
        current_cursor_position=context_data.get('cursor_position', 0),
        user_preferences=context_data.get('user_preferences', {})
    )
    
    # 创建命令注册表并执行
    registry = DNASPECCommandRegistry()
    return registry.execute_command(command_name, command_context, args)


# 通用命令行接口（用于开发测试）
def cli_main():
    """
    命令行接口 - 用于开发和测试
    """
    import sys
    
    if len(sys.argv) < 2:
        print("DNASPEC Context Engineering Skills CLI")
        print("Usage: python -m dnaspec_context_engineering.cli <command> [args...]")
        print("Commands: analyze, optimize, template, help")
        return
    
    command = sys.argv[1]
    
    # 模拟上下文环境
    simulated_context = DNASPECCommandContext(
        current_conversation=[
            {"role": "user", "content": " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Hello, please analyze this context."}
        ]
    )
    
    registry = DNASPECCommandRegistry()
    
    if command == "analyze":
        result = registry.execute_command('/dnaspec-analyze', simulated_context, sys.argv[2:])
        print("Context Analysis Instruction for AI:")
        print("="*50)
        print(result)
    elif command == "optimize":
        args = sys.argv[2:] if len(sys.argv) > 2 else []
        result = registry.execute_command('/dnaspec-optimize', simulated_context, args)
        print("Context Optimization Instruction for AI:")
        print("="*50) 
        print(result)
    elif command == "template":
        args = sys.argv[2:] if len(sys.argv) > 2 else ['chain_of_thought']
        result = registry.execute_command('/dnaspec-template', simulated_context, args)
        print("Cognitive Template Application Instruction for AI:")
        print("="*50)
        print(result)
    elif command == "help":
        print(registry.get_command_help())
    else:
        print(f"Unknown command: {command}")
        print("Available commands: analyze, optimize, template, help")


if __name__ == "__main__":
    cli_main()