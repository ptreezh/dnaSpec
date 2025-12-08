"""
DNASPEC Context Engineering Skills - AI CLI平台集成核心
利用AI原生智能提供上下文工程能力
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'DNASPEC-Project'))

from typing import Dict, Any, List
from abc import ABC, abstractmethod


class DNASpecSkill(ABC):
    """DSGS技能基类 - 为AI CLI平台设计"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.version = "1.0.0"
    
    @abstractmethod
    def execute(self, context: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """执行技能 - 抽象方法"""
        pass


class ContextAnalysisSkill(DNASpecSkill):
    """
    上下文分析技能 - 直接在AI CLI平台内部利用AI智能
    不依赖外部API，而是构造精确指令让AI模型自身分析
    """
    
    def __init__(self):
        super().__init__(
            name="dnaspec-context-analysis",
            description="DSGS上下文分析技能 - 利用AI模型原生智能分析上下文质量"
        )
    
    def execute(self, context: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行上下文分析
        构造AI指令并利用AI模型原生分析能力
        """
        if not context.strip():
            return {
                'success': False,
                'error': '上下文不能为空',
                'result': {}
            }
        
        # 构造高质量AI指令用于上下文分析
        analysis_instruction = f"""
作为专业的上下文质量分析师，请对以下上下文进行五维度的专业评估：

上下文内容:
"{context}"

请根据专业分析框架，按以下维度进行深度评估（0.0-1.0评分）：

1. **清晰度 (Clarity)**: 表达明确性、术语准确性、目标清晰度
2. **相关性 (Relevance)**: 与目标任务的关联性、内容针对性
3. **完整性 (Completeness)**: 关键信息完备性、约束条件完整性
4. **一致性 (Consistency)**: 内容内部逻辑一致性、表述连贯性  
5. **效率 (Efficiency)**: 信息密度、简洁性、冗余度控制

请以标准JSON格式返回分析结果:
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

然后提供简要的质量评估总结。
        """
        
        # 在AI CLI平台内部，这会成为向AI模型发送的内部指令
        # AI模型将使用其原生智能进行分析并返回结果
        return {
            'success': True,
            'result': {
                'analysis_instruction': analysis_instruction,
                'instruction_type': 'context_analysis',
                'target_context': context,
                'expected_output_format': 'json_with_metrics'
            }
        }


class ContextOptimizationSkill(DNASpecSkill):
    """
    上下文优化技能 - 利用AI模型原生推理和生成能力
    """
    
    def __init__(self):
        super().__init__(
            name="dnaspec-context-optimization",
            description="DSGS上下文优化技能 - 利用AI模型原生智能优化上下文质量"
        )
    
    def execute(self, context: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行上下文优化
        让AI模型使用原生推理和生成能力优化上下文
        """
        if not context.strip():
            return {
                'success': False,
                'error': '上下文不能为空',
                'result': {}
            }
        
        params = params or {}
        goals = params.get('optimization_goals', ['clarity', 'completeness'])
        if isinstance(goals, str):
            goals = [g.strip() for g in goals.split(',') if g.strip()]
        
        # 构造AI指令用于上下文优化
        optimization_instruction = f"""
请根据以下目标优化指定上下文：

优化目标: {', '.join(goals)}

原始上下文:
"{context}"

优化要求:
- 保持原始核心意图不变
- 针对指定目标进行专门改进
- 提供具体的优化措施说明
- 确保优化后的逻辑一致性和内容准确性

请返回优化后的内容和详细的改进说明，以JSON格式:
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
        """
        
        return {
            'success': True,
            'result': {
                'optimization_instruction': optimization_instruction,
                'instruction_type': 'context_optimization',
                'target_context': context,
                'optimization_goals': goals,
                'expected_output_format': 'json_with_optimization'
            }
        }


class CognitiveTemplateSkill(DNASpecSkill):
    """
    认知模板技能 - 利用AI模型原生认知能力
    """
    
    def __init__(self):
        super().__init__(
            name="dnaspec-cognitive-template",
            description="DSGS认知模板技能 - 利用AI模型原生智能应用认知模板结构化任务"
        )
        
        # 定义可用的认知模板
        self.cognitive_templates = {
            'chain_of_thought': {
                'name': '思维链',
                'description': '通过逐步推理分析复杂问题',
                'structure': ['问题理解', '步骤分解', '中间推理', '验证检查', '最终答案']
            },
            'few_shot': {
                'name': '少样本学习',
                'description': '通过示例对引导AI行为模式',
                'structure': ['示例1-输入', '示例1-输出', '示例2-输入', '示例2-输出', '新输入-推理-输出']
            },
            'verification': {
                'name': '验证检查',
                'description': '通过多步验证确保结果质量',
                'structure': ['初步答案', '逻辑检查', '事实检查', '完整性检查', '最终确认']
            },
            'role_playing': {
                'name': '角色扮演',
                'description': '从特定角色专业视角分析问题',
                'structure': ['角色定义', '专业分析', '专业建议', '专业决策']
            },
            'understanding': {
                'name': '深度理解',
                'description': '从多维度深入理解任务',
                'structure': ['核心目标', '关键要素', '约束条件', '成功标准', '潜在风险']
            }
        }
    
    def execute(self, context: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行认知模板应用
        引导AI模型使用特定认知框架进行结构化思考
        """
        if not context.strip():
            return {
                'success': False,
                'error': '上下文不能为空',
                'result': {'success': False}
            }
        
        params = params or {}
        template_type = params.get('template', 'chain_of_thought')
        role = params.get('role', '专家')
        
        if template_type not in self.cognitive_templates:
            return {
                'success': False,
                'error': f'未知模板: {template_type}. 支持: {list(self.cognitive_templates.keys())}',
                'available_templates': list(self.cognitive_templates.keys())
            }
        
        template_info = self.cognitive_templates[template_type]
        
        # 根据选定模板构造指令
        if template_type == 'chain_of_thought':
            template_instruction = f"""
请使用专业的思维链方法深度分析以下任务：

原始任务: {context}

请按以下思维链步骤进行结构化分析：

1. **问题理解**: 仔细理解任务的核心需求、关键约束和目标
2. **步骤分解**: 将任务分解为可执行的具体步骤
3. **中间推理**: 在每个步骤中提供详细的推理和思考过程
4. **验证检查**: 检查推理过程的合理性和逻辑一致性
5. **最终答案**: 综合所有分析步骤给出完整解决方案

请以结构化格式返回完整的思维链分析过程和最终专业结论。
"""
        elif template_type == 'verification':
            template_instruction = f"""
请使用系统的验证检查框架深度分析以下内容：

原始内容: {context}

请按以下验证步骤执行专业检查：

1. **初步答案**: 基于原始内容给出初步判断或解决方案
2. **逻辑一致性检查**: 验证内容内部逻辑的一致性和推理连贯性
3. **事实准确性检查**: 核实陈述事实的准确性、可靠性和有效性
4. **完整性检查**: 评估是否包含所有必要信息和关键要素
5. **最终确认**: 综合以上检查给出最终验证结论和改进建议

请返回每个验证步骤的详细结果和最终确认。
"""
        elif template_type == 'role_playing':
            template_instruction = f"""
请以{role}的专业身份和视角深入分析以下任务：

任务: {context}

请从{role}的专业知识、经验和技能出发进行分析：
1. **角色理解**: 作为{role}，我具备的专业能力包括...
2. **专业分析**: 从{role}专业角度分析任务的关键要素
3. **专业建议**: 基于{role}专业知识提供具体可行的建议
4. **专业决策**: 从{role}专业视角做出最优决策推荐

请返回{role}视角的专业分析、建议和决策。
"""
        elif template_type == 'few_shot':
            template_instruction = f"""
请使用少样本学习方法处理以下任务：

任务: {context}

以下是一些相关的示例对，展示了解决类似问题的模式和方法：

示例1:
输入: [类似任务输入1]
输出: [示例处理结果1]
解释: [说明处理模式]

示例2:
输入: [类似任务输入2] 
输出: [示例处理结果2]
解释: [说明处理模式]

请参考以上示例的模式、推理路径和输出格式，来处理您的任务。
详细解释您的分析过程和决策依据。
"""
        elif template_type == 'understanding':
            template_instruction = f"""
请使用深度理解框架来分析以下内容：

分析内容: {context}

请从以下维度进行深入理解：
1. **核心目标**: 此任务的主要目标和目的是什么？
2. **关键要素**: 包含哪些重要组成部分和关键要求？
3. **约束条件**: 有哪些限制条件和前置假设？
4. **成功标准**: 如何判断任务完成得好？
5. **潜在风险**: 可能存在哪些挑战和风险因素？

请返回深度理解结果和相关建议。
"""
        else:  # 默认使用少样本学习或其他模板
            # 在else分支中，template_info可能没有定义，所以需要获取模板信息
            template_info = self.cognitive_templates.get('few_shot', self.cognitive_templates['chain_of_thought'])  # 提供默认模板信息
            template_instruction = f"""
请使用{template_info['name']}认知框架分析以下任务：

任务: {context}

根据{template_info['name']}框架，按照{template_info['structure']}的结构进行专业分析。

请返回结构化后的认知框架分析结果。
"""
        
        return {
            'success': True,
            'result': {
                'template_instruction': template_instruction,
                'instruction_type': 'cognitive_template',
                'template_type': template_type,
                'template_info': template_info,
                'target_context': context,
                'expected_output_format': 'structured_with_framework'
            }
        }


def execute(args: Dict[str, Any]) -> str:
    """
    统一执行接口 - 与AI CLI平台集成
    """
    skill_name = args.get('skill', 'context-analysis')
    context_input = args.get('context', '') or args.get('request', '')
    params = args.get('params', {})
    
    if not context_input:
        return "错误: 未提供需要处理的上下文或请求内容"
    
    # 根据技能名称创建相应的技能实例
    if skill_name in ['context-analysis', 'analyze']:
        skill = ContextAnalysisSkill()
    elif skill_name in ['context-optimization', 'optimize']:
        skill = ContextOptimizationSkill()
    elif skill_name in ['cognitive-template', 'template']:
        skill = CognitiveTemplateSkill()
    else:
        available_skills = ['dnaspec-context-analysis', 'dnaspec-context-optimization', 'dnaspec-cognitive-template']
        return f"错误: 未知技能 '{skill_name}'. 可用技能: {available_skills}"
    
    # 执行技能
    result = skill.execute(context_input, params)
    
    if not result['success']:
        return f"错误: {result.get('error', '技能执行失败')}"
    
    # 根据技能类型格式化输出
    skill_result = result['result']
    
    if skill_name in ['context-analysis', 'analyze']:
        output_lines = [
            "# 上下文质量分析指令",
            "## 指令内容:",
            "```",
            skill_result['analysis_instruction'],
            "```",
            "",
            "## 执行说明:",
            "这个指令将发送给AI模型进行五维度专业分析",
            f"原始上下文长度: {len(context_input)} 字符",
            f"目标输出: JSON格式的指标分析"
        ]
        return "\n".join(output_lines)
    
    elif skill_name in ['context-optimization', 'optimize']:
        output_lines = [
            "# 上下文优化指令", 
            "## 指令内容:",
            "```",
            skill_result['optimization_instruction'],
            "```",
            "",
            "## 优化信息:",
            f"目标: {', '.join(skill_result['optimization_goals'])}",
            f"原始上下文长度: {len(context_input)} 字符",
            f"目标输出: JSON格式的优化结果"
        ]
        return "\n".join(output_lines)
    
    elif skill_name in ['cognitive-template', 'template']:
        output_lines = [
            "# 认知模板应用指令",
            f"## 模板类型: {skill_result['template_type']}",
            f"## 模板描述: {skill_result['template_info']['description']}",
            "## 指令内容:",
            "```",
            skill_result['template_instruction'],
            "```",
            "",
            "## 执行说明:",
            f"模板结构: {', '.join(skill_result['template_info']['structure'])}",
            f"目标输出: 基于{skill_result['template_type']}框架的结构化结果"
        ]
        return "\n".join(output_lines)


def get_available_skills() -> List[str]:
    """获取可用技能列表"""
    return [
        'dnaspec-context-analysis',
        'dnaspec-context-optimization', 
        'dnaspec-cognitive-template'
    ]


def get_skill_descriptions() -> Dict[str, str]:
    """获取技能描述"""
    return {
        'dnaspec-context-analysis': '上下文质量五维专业分析',
        'dnaspec-context-optimization': 'AI驱动的上下文智能优化',
        'dnaspec-cognitive-template': '认知模板结构化复杂任务'
    }