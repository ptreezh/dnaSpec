"""
DNASPEC Cognitive Templater Skill - 符合AgentSkills.io标准
基于TDD实现，遵循KISS、SOLID、YAGNI原则
"""
import json
import uuid
from typing import Dict, Any, List, Optional
from skills.dnaspec_skill_framework import (
    DNASpecSkillBase, 
    track_execution,
    validate_text_input,
    SkillValidationError
)


@track_execution
class CognitiveTemplaterSkill(DNASpecSkillBase):
    """
    认知模板技能 - 应用结构化认知框架
    
    符合AgentSkills.io规范：
    - name: cognitive-templater
    - description: Applies cognitive templates to enhance reasoning
    - 支持5种认知模板：思维链、验证、少样本、角色扮演、理解框架
    """
    
    def __init__(self):
        super().__init__(
            name="cognitive-templater",
            description="Applies cognitive templates (chain-of-thought, verification, few-shot, role-playing, understanding) to enhance reasoning and problem-solving. Use when you need structured thinking approaches, systematic problem analysis, verification frameworks, or role-based perspective taking.",
            version="2.0.0"
        )
        
        # 支持的模板类型
        self.supported_templates = [
            "chain_of_thought",
            "verification", 
            "few_shot",
            "role_playing",
            "understanding"
        ]
        
        # 模板配置
        self.template_configs = {
            "chain_of_thought": {
                "name": "Chain of Thought",
                "description": "Systematic step-by-step reasoning process",
                "max_steps": 10,
                "default_steps": 3
            },
            "verification": {
                "name": "Verification Template", 
                "description": "Critical thinking and validation framework",
                "max_questions": 8,
                "default_questions": 4
            },
            "few_shot": {
                "name": "Few-Shot Learning",
                "description": "Learning from examples and patterns",
                "max_examples": 5,
                "default_examples": 2
            },
            "role_playing": {
                "name": "Role-Playing",
                "description": "Adopting different perspectives and roles",
                "max_roles": 3,
                "default_roles": 2
            },
            "understanding": {
                "name": "Understanding Framework",
                "description": "Deep comprehension and conceptual mapping",
                "max_concepts": 10,
                "default_concepts": 5
            }
        }
    
    def validate_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证输入数据
        
        Args:
            input_data: 包含要处理的内容和模板类型的输入数据
            
        Returns:
            验证结果字典
        """
        # 验证必需字段
        if 'input' not in input_data:
            return {
                'valid': False, 
                'error': 'Missing required field: input'
            }
        
        if 'template_type' not in input_data:
            return {
                'valid': False, 
                'error': 'Missing required field: template_type'
            }
        
        # 验证输入内容
        input_validation = validate_text_input(input_data['input'], 'input')
        if not input_validation['valid']:
            return input_validation
        
        # 验证模板类型
        template_type = input_data['template_type']
        if template_type not in self.supported_templates:
            return {
                'valid': False,
                'error': f'Invalid template_type. Must be one of: {", ".join(self.supported_templates)}'
            }
        
        # 验证可选参数
        if 'max_depth' in input_data:
            max_depth = input_data['max_depth']
            if not isinstance(max_depth, int) or max_depth < 1 or max_depth > 20:
                return {
                    'valid': False,
                    'error': 'max_depth must be an integer between 1 and 20'
                }
        
        return {'valid': True}
    
    def execute_skill(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行认知模板应用核心逻辑
        
        Args:
            input_data: 验证过的输入数据
            
        Returns:
            认知模板应用结果
        """
        content = input_data['input']
        template_type = input_data['template_type']
        max_depth = input_data.get('max_depth', None)
        
        # 根据模板类型执行不同的处理
        if template_type == "chain_of_thought":
            result = self._apply_chain_of_thought(content, max_depth)
        elif template_type == "verification":
            result = self._apply_verification_template(content, max_depth)
        elif template_type == "few_shot":
            result = self._apply_few_shot_template(content, max_depth)
        elif template_type == "role_playing":
            result = self._apply_role_playing_template(content, max_depth)
        elif template_type == "understanding":
            result = self._apply_understanding_template(content, max_depth)
        else:
            raise ValueError(f"Unsupported template type: {template_type}")
        
        return {
            'template_type': template_type,
            'template_description': self.template_configs[template_type]['description'],
            'enhanced_output': result['enhanced_output'],
            'cognitive_framework_applied': result['framework_applied'],
            'thinking_steps': result.get('thinking_steps', []),
            'input_processed': content,
            'template_metadata': result.get('metadata', {})
        }
    
    def _apply_chain_of_thought(self, content: str, max_depth: Optional[int]) -> Dict[str, Any]:
        """
        应用思维链模板
        
        Args:
            content: 要处理的内容
            max_depth: 最大深度
            
        Returns:
            思维链应用结果
        """
        config = self.template_configs["chain_of_thought"]
        max_steps = min(config['max_steps'], max_depth or config['default_steps'])
        
        # 生成思维步骤
        thinking_steps = [
            {
                'step': 1,
                'description': '问题理解',
                'analysis': f"清晰理解问题: {content[:50]}...",
                'output': '问题理解完成'
            },
            {
                'step': 2,
                'description': '步骤分解',
                'analysis': f"将问题分解为{max_steps}个逻辑步骤",
                'output': '分解步骤规划完成'
            },
            {
                'step': 3,
                'description': '中间推理',
                'analysis': '逐步分析每个步骤的逻辑关系',
                'output': '中间推理完成'
            }
        ]
        
        # 如果需要更多步骤，添加通用步骤
        if max_steps > 3:
            for i in range(4, max_steps + 1):
                thinking_steps.append({
                    'step': i,
                    'description': f'步骤{i-3}',
                    'analysis': f'继续深入分析问题的第{i-3}个层面',
                    'output': f'步骤{i}完成'
                })
        
        # 生成增强输出
        enhanced_output = f"链式思维分析: {content}\n\n"
        for step in thinking_steps:
            enhanced_output += f"{step['step']}. {step['description']}\n"
            enhanced_output += f"   分析: {step['analysis']}\n"
            enhanced_output += f"   结果: {step['output']}\n\n"
        
        enhanced_output += "最终答案: 基于以上分析，得出系统性解决方案。"
        
        return {
            'enhanced_output': enhanced_output,
            'framework_applied': True,
            'thinking_steps': thinking_steps,
            'metadata': {
                'total_steps': len(thinking_steps),
                'depth': max_steps,
                'complexity': 'systematic'
            }
        }
    
    def _apply_verification_template(self, content: str, max_depth: Optional[int]) -> Dict[str, Any]:
        """
        应用验证模板
        
        Args:
            content: 要处理的内容
            max_depth: 最大深度
            
        Returns:
            验证模板应用结果
        """
        config = self.template_configs["verification"]
        max_questions = min(config['max_questions'], max_depth or config['default_questions'])
        
        # 生成验证问题
        verification_questions = [
            {
                'category': '假设分析',
                'question': '这个分析基于哪些关键假设？',
                'analysis': '识别问题背后的基本假设'
            },
            {
                'category': '逻辑验证',
                'question': '推理过程是否逻辑一致？',
                'analysis': '检查逻辑链条的有效性'
            },
            {
                'category': '证据评估',
                'question': '支持结论的证据是否充分？',
                'analysis': '评估证据的可靠性和相关性'
            },
            {
                'category': '替代方案',
                'question': '是否考虑了其他可能的解决方案？',
                'analysis': '探索替代的可能性和路径'
            }
        ]
        
        # 根据深度调整问题数量
        if max_questions > 4:
            additional_questions = [
                {
                    'category': '偏见检查',
                    'question': '是否存在认知偏见影响判断？',
                    'analysis': '识别潜在的认知偏见'
                },
                {
                    'category': '边界条件',
                    'question': '解决方案的边界和限制是什么？',
                    'analysis': '定义解决方案的适用范围'
                }
            ]
            verification_questions.extend(additional_questions[:max_questions-4])
        
        # 生成增强输出
        enhanced_output = f"验证框架分析: {content}\n\n"
        enhanced_output += "验证检查:\n"
        for i, q in enumerate(verification_questions[:max_questions], 1):
            enhanced_output += f"{i}. {q['category']}: {q['question']}\n"
            enhanced_output += f"   分析方法: {q['analysis']}\n\n"
        
        enhanced_output += "结论: 经过多维度验证，提高结论的可靠性。"
        
        return {
            'enhanced_output': enhanced_output,
            'framework_applied': True,
            'thinking_steps': verification_questions[:max_questions],
            'metadata': {
                'verification_categories': [q['category'] for q in verification_questions[:max_questions]],
                'depth': max_questions,
                'rigor': 'critical'
            }
        }
    
    def _apply_few_shot_template(self, content: str, max_depth: Optional[int]) -> Dict[str, Any]:
        """
        应用少样本学习模板
        
        Args:
            content: 要处理的内容
            max_depth: 最大深度
            
        Returns:
            少样本学习模板应用结果
        """
        config = self.template_configs["few_shot"]
        max_examples = min(config['max_examples'], max_depth or config['default_examples'])
        
        # 生成示例
        examples = [
            {
                'example': 1,
                'scenario': '类似的简单问题',
                'pattern': '模式A：直接应用已知解决方案',
                'application': '直接套用已有模式'
            },
            {
                'example': 2,
                'scenario': '复杂相关情况',
                'pattern': '模式B：结合多个已知模式',
                'application': '组合模式处理复杂情况'
            }
        ]
        
        if max_examples > 2:
            additional_example = {
                'example': 3,
                'scenario': '更复杂的多层次问题',
                'pattern': '模式C：层次化模式应用',
                'application': '分层应用模式处理复杂问题'
            }
            examples.append(additional_example)
        
        # 生成增强输出
        enhanced_output = f"少样本学习分析: {content}\n\n"
        enhanced_output += "从以下示例中学习模式:\n"
        for ex in examples[:max_examples]:
            enhanced_output += f"示例{ex['example']}: {ex['scenario']}\n"
            enhanced_output += f"模式: {ex['pattern']}\n"
            enhanced_output += f"应用: {ex['application']}\n\n"
        
        enhanced_output += f"当前问题应用: 基于以上{max_examples}个示例的模式，应用到当前问题。"
        
        return {
            'enhanced_output': enhanced_output,
            'framework_applied': True,
            'thinking_steps': examples[:max_examples],
            'metadata': {
                'examples_used': max_examples,
                'patterns_identified': [ex['pattern'] for ex in examples[:max_examples]],
                'learning_approach': 'inductive'
            }
        }
    
    def _apply_role_playing_template(self, content: str, max_depth: Optional[int]) -> Dict[str, Any]:
        """
        应用角色扮演模板
        
        Args:
            content: 要处理的内容
            max_depth: 最大深度
            
        Returns:
            角色扮演模板应用结果
        """
        config = self.template_configs["role_playing"]
        max_roles = min(config['max_roles'], max_depth or config['default_roles'])
        
        # 生成角色
        roles = [
            {
                'role': '专家视角',
                'characteristics': '专业知识、深度分析、技术导向',
                'focus': '技术可行性、实现细节、最佳实践'
            },
            {
                'role': '用户视角',
                'characteristics': '实用性、易用性、用户体验',
                'focus': '使用场景、实际需求、用户满意度'
            }
        ]
        
        if max_roles > 2:
            additional_role = {
                'role': '管理者视角',
                'characteristics': '战略思维、资源考虑、风险评估',
                'focus': '商业价值、成本效益、长期影响'
            }
            roles.append(additional_role)
        
        # 生成增强输出
        enhanced_output = f"多角色分析: {content}\n\n"
        for i, role in enumerate(roles[:max_roles], 1):
            enhanced_output += f"角色{i}: {role['role']}\n"
            enhanced_output += f"特征: {role['characteristics']}\n"
            enhanced_output += f"关注点: {role['focus']}\n"
            enhanced_output += f"分析: 从{role['role']}角度分析问题\n\n"
        
        enhanced_output += "综合观点: 整合多个角色视角，形成全面解决方案。"
        
        return {
            'enhanced_output': enhanced_output,
            'framework_applied': True,
            'thinking_steps': roles[:max_roles],
            'metadata': {
                'roles_analyzed': max_roles,
                'perspectives': [role['role'] for role in roles[:max_roles]],
                'synthesis_approach': 'multi_perspective'
            }
        }
    
    def _apply_understanding_template(self, content: str, max_depth: Optional[int]) -> Dict[str, Any]:
        """
        应用理解框架模板
        
        Args:
            content: 要处理的内容
            max_depth: 最大深度
            
        Returns:
            理解框架模板应用结果
        """
        config = self.template_configs["understanding"]
        max_concepts = min(config['max_concepts'], max_depth or config['default_concepts'])
        
        # 生成概念分析
        concepts = [
            {
                'concept': '核心概念识别',
                'analysis': '提取问题和语境中的关键概念',
                'examples': ['主要术语', '技术概念', '业务概念']
            },
            {
                'concept': '关系映射',
                'analysis': '分析概念之间的逻辑关系',
                'examples': ['因果关系', '层次关系', '依赖关系']
            },
            {
                'concept': '情境分析',
                'analysis': '理解问题所处的具体情境',
                'examples': ['环境因素', '约束条件', '资源限制']
            }
        ]
        
        if max_concepts > 3:
            additional_concepts = [
                {
                    'concept': '综合理解',
                    'analysis': '将所有概念整合成完整理解',
                    'examples': ['整体图景', '系统视图', '全面认知']
                },
                {
                    'concept': '深度洞察',
                    'analysis': '识别深层次的隐含信息和模式',
                    'examples': ['潜在问题', '隐藏机会', '深层联系']
                }
            ]
            concepts.extend(additional_concepts[:max_concepts-3])
        
        # 生成增强输出
        enhanced_output = f"深度理解框架: {content}\n\n"
        enhanced_output += "概念层次分析:\n"
        for i, concept in enumerate(concepts[:max_concepts], 1):
            enhanced_output += f"{i}. {concept['concept']}\n"
            enhanced_output += f"   分析: {concept['analysis']}\n"
            enhanced_output += f"   示例: {', '.join(concept['examples'])}\n\n"
        
        enhanced_output += "整合理解: 基于概念分析，形成系统性理解。"
        
        return {
            'enhanced_output': enhanced_output,
            'framework_applied': True,
            'thinking_steps': concepts[:max_concepts],
            'metadata': {
                'concepts_analyzed': max_concepts,
                'understanding_depth': 'comprehensive',
                'analysis_method': 'hierarchical'
            }
        }


# 创建技能实例
cognitive_templater_skill = CognitiveTemplaterSkill()

# 导出Lambda处理器（符合AgentSkills.io标准）
def lambda_handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    """Lambda处理器入口点"""
    return cognitive_templater_skill.lambda_handler(event, context)

# 导出技能实例（用于注册）
def get_skill():
    """获取技能实例"""
    return cognitive_templater_skill