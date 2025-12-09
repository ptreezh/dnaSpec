"""
Cognitive Template Application Skill
用于应用认知模板到上下文工程任务
"""
from typing import Dict, Any, List
import json
import re


class CognitiveTemplateApplier:
    """
    认知模板应用器
    应用预定义的认知模板来改进上下文工程
    """
    
    def __init__(self):
        # 预定义的认知模板
        self.templates = {
            'chain_of_thought': {
                'name': '思维链',
                'description': '将复杂问题分解为步骤序列',
                'structure': [
                    '问题理解',
                    '步骤分解', 
                    '中间推理',
                    '验证检查',
                    '最终答案'
                ]
            },
            'few_shot': {
                'name': '少示例学习',
                'description': '提供示例对以指导模型行为',
                'structure': [
                    '指令说明',
                    '示例输入1 -> 示例输出1',
                    '示例输入2 -> 示例输出2', 
                    '新输入 -> 预期输出'
                ]
            },
            'verification': {
                'name': '验证检查',
                'description': '对输出进行多角度验证',
                'structure': [
                    '初步答案',
                    '逻辑一致性检查',
                    '事实准确性检查', 
                    '完整性检查',
                    '最终确认'
                ]
            },
            'role_playing': {
                'name': '角色扮演',
                'description': '以特定角色视角进行分析',
                'structure': [
                    '角色定义',
                    '角色知识背景',
                    '角色视角分析',
                    '角色决策建议'
                ]
            },
            'understanding': {
                'name': '理解框架',
                'description': '深入理解任务和需求',
                'structure': [
                    '核心目标',
                    '关键要素',
                    '约束条件',
                    '成功标准',
                    '潜在风险'
                ]
            }
        }
    
    def apply_template(self, template_name: str, context: str, **kwargs) -> Dict[str, Any]:
        """
        应用认知模板到上下文
        
        Args:
            template_name: 模板名称
            context: 原始上下文
            **kwargs: 其他参数
            
        Returns:
            应用模板后的结果
        """
        if template_name not in self.templates:
            return {
                'success': False,
                'error': f'模板不存在: {template_name}',
                'available_templates': list(self.templates.keys())
            }
        
        template = self.templates[template_name]
        
        # 根据模板结构重新组织上下文
        enhanced_context = self._structure_context_with_template(template, context, kwargs)
        
        return {
            'success': True,
            'template_name': template_name,
            'template_description': template['description'],
            'original_context': context,
            'enhanced_context': enhanced_context,
            'structure': template['structure']
        }
    
    def _structure_context_with_template(self, template: Dict, context: str, kwargs: Dict) -> str:
        """
        使用模板结构化上下文
        """
        structure = template['structure']
        enhanced_parts = []
        
        if template['name'] == '思维链':
            enhanced_parts.append("### 思维链分析")
            enhanced_parts.append("请使用以下思维链步骤分析问题：")
            enhanced_parts.append("")
            
            for i, step in enumerate(structure):
                if i == 0:  # 问题理解
                    enhanced_parts.append(f"1. **{step}**: {context}")
                elif i == len(structure) - 1:  # 最终答案
                    enhanced_parts.append(f"{i+1}. **{step}**: [在此提供最终答案]")
                else:
                    enhanced_parts.append(f"{i+1}. **{step}**: [请详细执行此步骤]")
            
        elif template['name'] == '少示例学习':
            enhanced_parts.append("### 少示例学习框架")
            enhanced_parts.append("以下是示例对，用于指导任务执行：")
            enhanced_parts.append("")
            
            # 添加指令说明
            enhanced_parts.append(f"- **{structure[0]}**: {context}")
            enhanced_parts.append("")
            
            # 添加示例（这里使用通用示例，实际应用中应该根据具体任务定制）
            enhanced_parts.append(f"- **{structure[1]}**")
            enhanced_parts.append("  输入: [示例输入1]")
            enhanced_parts.append("  输出: [示例输出1]")
            enhanced_parts.append("")
            
            enhanced_parts.append(f"- **{structure[2]}**")
            enhanced_parts.append("  输入: [示例输入2]")
            enhanced_parts.append("  输出: [示例输出2]")
            enhanced_parts.append("")
            
            enhanced_parts.append(f"- **{structure[3]}**")
            enhanced_parts.append(f"  输入: {context}")
            enhanced_parts.append("  输出: [请根据以上示例生成输出]")
            
        elif template['name'] == '验证检查':
            enhanced_parts.append("### 验证检查框架")
            enhanced_parts.append(f"任务: {context}")
            enhanced_parts.append("")
            
            for i, check in enumerate(structure):
                if i == 0:  # 初步答案
                    enhanced_parts.append(f"1. **{check}**: [针对任务{context}的初步答案]")
                elif i == len(structure) - 1:  # 最终确认
                    enhanced_parts.append(f"{i+1}. **{check}**: [基于以上检查的最终确认]")
                else:
                    enhanced_parts.append(f"{i+1}. **{check}**: [在此执行{check}]")
                    
        elif template['name'] == '角色扮演':
            role = kwargs.get('role', '专家')
            enhanced_parts.append(f"### {role}角色扮演分析")
            enhanced_parts.append(f"请以{role}的身份分析以下任务：")
            enhanced_parts.append(f"任务: {context}")
            enhanced_parts.append("")
            
            for i, aspect in enumerate(structure):
                if i == 0:  # 角色定义
                    enhanced_parts.append(f"1. **{aspect}**: 作为{role}，我具有以下专业能力...")
                elif i == len(structure) - 1:  # 角色决策建议
                    enhanced_parts.append(f"{i+1}. **{aspect}**: [基于以上分析给出{role}的专业建议]")
                else:
                    enhanced_parts.append(f"{i+1}. **{aspect}**: [从{role}视角分析{aspect}]")
        
        elif template['name'] == '理解框架':
            enhanced_parts.append("### 任务理解框架")
            enhanced_parts.append(f"详细分析任务: {context}")
            enhanced_parts.append("")
            
            for i, element in enumerate(structure):
                enhanced_parts.append(f"{i+1}. **{element}**: [详细描述{element}]")
        
        return "\n".join(enhanced_parts)
    
    def list_templates(self) -> List[Dict[str, str]]:
        """
        列出所有可用模板
        """
        return [
            {
                'name': name,
                'description': template['description'],
                'structure': template['structure']
            }
            for name, template in self.templates.items()
        ]


def execute(args: Dict[str, Any]) -> str:
    """
    执行认知模板应用技能
    """
    template_name = args.get("template", "chain_of_thought")
    context = args.get("context", "")
    role = args.get("role", "专家")
    
    if not context:
        return "错误: 未提供需要应用模板的上下文"
    
    applier = CognitiveTemplateApplier()
    
    if template_name not in applier.templates:
        available = ", ".join(applier.templates.keys())
        return f"错误: 模板 '{template_name}' 不存在。可用模板: {available}"
    
    result = applier.apply_template(template_name, context, role=role)
    
    if not result['success']:
        return result['error']
    
    # 格式化输出结果
    output = []
    output.append(f"应用认知模板: {result['template_name']} ({result['template_description']})")
    output.append("=" * 60)
    output.append("")
    output.append("结构化后的上下文:")
    output.append(result['enhanced_context'])
    output.append("")
    output.append("模板结构:")
    for i, step in enumerate(result['structure'], 1):
        output.append(f"  {i}. {step}")
    
    return "\n".join(output)