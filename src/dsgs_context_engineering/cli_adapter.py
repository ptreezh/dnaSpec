"""
DNASPEC Context Engineering Skills - AI原生接口适配器
与Claude/Gemini等AI CLI平台集成的上下文工程增强系统
"""
import json
from typing import Dict, Any, List
import sys
import os


class ContextEngineeringAdapter:
    """
    上下文工程适配器
    将AI CLI平台的指令格式转换为上下文工程操作
    """
    
    def __init__(self):
        self.name = "dnaspec-context-engineering-adapter"
        self.description = "DNASPEC Context Engineering Skills - 为AI CLI平台提供专业上下文工程能力的适配器"
    
    def handle_cli_command(self, command_parts: List[str], context: str) -> str:
        """
        处理AI CLI平台命令
        实际系统中会将命令转换为AI指令并由AI模型执行
        """
        if len(command_parts) < 1:
            return self._show_help()
        
        action = command_parts[0].lower()
        
        if action in ['analyze', 'analysis', '上下文分析']:
            return self._execute_analysis(context, command_parts[1:])
        elif action in ['optimize', 'optimization', '上下文优化']:
            return self._execute_optimization(context, command_parts[1:])
        elif action in ['template', 'apply-template', '应用模板']:
            return self._execute_template(context, command_parts[1:])
        elif action in ['help', 'info']:
            return self._show_help()
        else:
            return f"错误: 未知操作 '{action}'. 请使用 analyze, optimize, template, 或 help"
    
    def _execute_analysis(self, context: str, params: List[str]) -> str:
        """
        执行上下文分析
        构造AI指令并返回给AI模型处理
        """
        if not context.strip():
            return "错误: 请提供需要分析的上下文内容"
        
        # 构造用于AI模型的分析指令
        analysis_instruction = f"""
作为专业的上下文质量分析师，请对以下上下文进行五维度评估：

上下文内容: "{context}"

评估维度 (0.0-1.0评分):
1. 清晰度 (Clarity): 表达明确性，术语准确性
2. 相关性 (Relevance): 与目标关联性，内容针对性
3. 完整性 (Completeness): 信息完备性，约束完整性  
4. 一致性 (Consistency): 逻辑一致性，表述连贯性
5. 效率 (Efficiency): 信息密度，简洁性

请返回JSON格式分析结果:
{{
  "context_length": {len(context)},
  "token_count_estimate": {max(1, len(context) // 4)},
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

并提供简要分析总结。
"""
        
        # 在实际AI CLI平台中，这会直接发送给AI模型
        # 返回AI模型将要执行的指令
        return analysis_instruction
    
    def _execute_optimization(self, context: str, params: List[str]) -> str:
        """
        执行上下文优化
        构造AI指令让AI模型进行智能优化
        """
        if not context.strip():
            return "错误: 请提供需要优化的上下文内容"
        
        # 解析优化目标
        goals = ['clarity', 'completeness']  # 默认目标
        for param in params:
            if '=' in param:
                key, value = param.split('=', 1)
                if key == 'goals' or key == '目标':
                    goals = [g.strip() for g in value.split(',') if g.strip()]
        
        # 构造优化指令
        optimization_instruction = f"""
根据以下目标优化上下文内容:

优化目标: {', '.join(goals)}

原始上下文: "{context}"

优化要求:
- 保持原始意图不变
- 针对指定目标进行改进
- 返回优化后的内容和应用的改进措施
- 以JSON格式返回结果

优化后的上下文应该:
"""
        
        # 添加具体优化需求
        if 'clarity' in goals or '清晰' in goals:
            optimization_instruction += "- 表述更加明确和精确\n"
        
        if 'completeness' in goals or '完整' in goals:
            optimization_instruction += "- 包含更完整的约束和要求\n"
        
        if 'relevance' in goals or '相关' in goals:
            optimization_instruction += "- 与目标更相关和针对性\n"
        
        optimization_instruction += """

请返回JSON格式结果:
{
  "original_context": "原始上下文",
  "optimized_context": "优化后上下文", 
  "applied_optimizations": ["应用的优化措施"],
  "optimization_summary": "优化过程和结果总结"
}
"""
        
        return optimization_instruction
    
    def _execute_template(self, context: str, params: List[str]) -> str:
        """
        应用认知模板
        构造AI指令让AI模型应用认知框架
        """
        if not context.strip():
            return "错误: 请提供需要应用模板的上下文或任务"
        
        # 解析模板类型，默认为思维链
        template_type = 'chain_of_thought'
        for param in params:
            if '=' in param:
                key, value = param.split('=', 1)
                if key in ['template', '模板', 'type', '类型']:
                    template_type = value.strip()
        
        # 根据模板类型构造不同指令
        template_instructions = {
            'chain_of_thought': f"""
使用思维链方法分析以下任务：

任务: {context}

请按以下步骤进行结构化分析：

1. **问题理解**: 明确任务核心需求、约束和目标
2. **步骤分解**: 将任务分解为可执行的子步骤
3. **中间推理**: 在每个步骤中提供详细思考过程
4. **验证检查**: 检查推理过程的合理性和逻辑一致性
5. **最终答案**: 综合所有步骤给出完整解决方案

请返回完整的思维链分析过程和最终结论。
""",
            'verification': f"""
使用验证框架分析以下内容：

原始内容: {context}

执行验证步骤：
1. **初步答案**: 基于内容给出初步判断
2. **逻辑一致性检查**: 验证内容内部逻辑一致性
3. **事实准确性检查**: 核实事实陈述的准确性
4. **完整性检查**: 评估信息完整性
5. **最终确认**: 综合以上检查给出确认

请返回每个验证步骤结果和最终确认。
""",
            'few_shot': f"""
使用少样本学习方法处理以下任务:

任务: {context}

以下是相关示例对，展示处理类似问题的模式：

示例1:
输入: [类似任务输入]
输出: [示例处理结果]
解释: [处理模式说明]

示例2: 
输入: [另一个类似任务输入]
输出: [另一个示例处理结果]
解释: [处理模式说明]

请参考以上示例模式处理您的任务。
详细解释您的分析过程和决策依据。
""",
            'role_playing': f"""
请以专家角色视角分析以下任务：

任务: {context}

从专家专业角度出发:
1. **角色理解**: 作为专家，我具备的专业能力...
2. **专业分析**: 从专家角度分析任务要素
3. **专业建议**: 基于专业知识给出建议
4. **专业决策**: 从专家视角推荐决策

请返回专家视角的专业分析和建议。
"""
        }
        
        return template_instructions.get(template_type, f"""
使用{template_type}认知框架分析任务: {context}

请返回结构化分析结果。
""")
    
    def _show_help(self) -> str:
        """返回帮助信息"""
        return """
# DNASPEC Context Engineering Skills 帮助

DNASPEC Context Engineering Skills 是为AI CLI平台设计的上下文工程增强工具集，利用AI模型原生智能提供专业级上下文分析、优化和结构化能力。

## 可用命令:

**analyze** [上下文内容]
- 分析上下文质量的五维指标 (清晰度、相关性、完整性、一致性、效率)

**optimize** [上下文内容] [--goals "clarity,completeness"]
- 优化上下文内容，支持多种优化目标

**template** [任务内容] [--template "chain_of_thought"]
- 应用认知模板结构化复杂任务
- 支持: chain_of_thought, verification, few_shot, role_playing

## 示例用法:

```
/dnaspec-context analyze "设计电商系统，支持用户登录商品浏览功能。"
/dnaspec-context optimize "系统要处理订单" --goals "clarity,completeness"  
/dnaspec-context template "如何提高性能？" --template "chain_of_thought"
```

## 核心价值观:

- **AI原生**: 100%利用AI模型原生智能，无本地模型依赖
- **指令工程**: 精确指令引导AI模型执行专业任务
- **专业增强**: 为AI交互提供专业级上下文工程能力
- **平台集成**: 与Claude/Gemini等AI CLI平台无缝集成
"""
    
    def get_skill_info(self) -> Dict[str, Any]:
        """返回技能信息"""
        return {
            'name': self.name,
            'description': self.description,
            'version': '1.0.0',
            'skills': [
                {
                    'name': 'context-analysis',
                    'description': '五维指标上下文质量分析',
                    'command': 'analyze [context]'
                },
                {
                    'name': 'context-optimization',
                    'description': '多目标上下文智能优化',
                    'command': 'optimize [context] --goals [targets]'
                },
                {
                    'name': 'cognitive-template',
                    'description': '认知模板结构化复杂任务',
                    'command': 'template [context] --template [type]'
                }
            ]
        }


def execute_dsgs_command(skill_args: Dict[str, Any]) -> str:
    """
    执行DSGS Context Engineering Skill命令
    这是与AI CLI平台集成的入口函数
    """
    adapter = ContextEngineeringAdapter()
    
    # 从参数中提取技能名称和上下文
    skill_name = skill_args.get('skill', 'analyze')
    context = skill_args.get('context', '') or skill_args.get('request', '') or skill_args.get('input', '')
    params = skill_args.get('params', {})
    command = skill_args.get('command', skill_name)
    
    # 根据命令解析参数
    if isinstance(params, dict):
        command_parts = [command]
        if 'goals' in params:
            command_parts.append(f"goals={params['goals']}")
        if 'template' in params:
            command_parts.append(f"template={params['template']}")
    else:
        command_parts = [command] if command else [skill_name]
    
    # 执行相应的上下文工程操作
    result = adapter.handle_cli_command(command_parts, context)
    return result


def get_available_skills() -> List[Dict[str, str]]:
    """
    获取可用技能列表
    """
    adapter = ContextEngineeringAdapter()
    info = adapter.get_skill_info()
    return info['skills']


# CLI兼容接口
def main():
    """
    CLI主入口点 - 模拟与AI CLI平台的交互
    """
    if len(sys.argv) < 2:
        print("Usage: python -m dnaspec_context_engineering.cli <command> [context]")
        print("Commands: analyze, optimize, template, help")
        return
    
    command = sys.argv[1]
    context = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
    
    adapter = ContextEngineeringAdapter()
    result = adapter.handle_cli_command([command], context)
    
    print(result)


if __name__ == "__main__":
    main()