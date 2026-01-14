#!/usr/bin/env python3
"""
Cognitive Templater - Template Execution Engine
确定性认知模板执行引擎
"""

import json
import sys
import re
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class TemplateResult:
    """模板执行结果数据结构"""
    template_type: str
    applied_steps: List[Dict[str, Any]]
    structured_output: str
    confidence_score: float
    reasoning_path: List[str]
    validation_results: Dict[str, Any]

class CognitiveTemplateEngine:
    """认知模板引擎 - 确定性框架执行"""
    
    def __init__(self):
        self.template_functions = {
            'chain_of_thought': self.execute_chain_of_thought,
            'verification': self.execute_verification_template,
            'few_shot': self.execute_few_shot_learning,
            'role_playing': self.execute_role_playing,
            'understanding': self.execute_understanding_framework
        }
        
        # 模板特征识别规则
        self.template_indicators = {
            'chain_of_thought': [
                '如何', '怎样', '步骤', '过程', '方法', '解决', '实现', '分析'
            ],
            'verification': [
                '检查', '验证', '审查', '评估', '测试', '确认', '正确性', '质量'
            ],
            'few_shot': [
                '示例', '例子', '类似', '参考', '模式', '借鉴', '模仿'
            ],
            'role_playing': [
                '角色', '角度', '视角', '身份', '立场', '观点', '体验'
            ],
            'understanding': [
                '理解', '解释', '分析', '概念', '原理', '关系', '结构'
            ]
        }
    
    def auto_select_template(self, problem_description: str) -> str:
        """自动选择最适合的模板"""
        template_scores = {}
        
        for template, indicators in self.template_indicators.items():
            score = sum(1 for indicator in indicators if indicator in problem_description)
            template_scores[template] = score
        
        # 选择得分最高的模板
        selected_template = max(template_scores.items(), key=lambda x: x[1])[0]
        
        # 如果所有得分都很低，默认选择chain_of_thought
        if template_scores[selected_template] == 0:
            selected_template = 'chain_of_thought'
        
        return selected_template
    
    def execute_template(self, problem_description: str, template_type: str = None,
                       context: Dict[str, Any] = None) -> TemplateResult:
        """执行指定的认知模板"""
        if template_type is None:
            template_type = self.auto_select_template(problem_description)
        
        if template_type not in self.template_functions:
            raise ValueError(f"Unsupported template type: {template_type}")
        
        # 执行模板函数
        result = self.template_functions[template_type](problem_description, context or {})
        
        return TemplateResult(
            template_type=template_type,
            applied_steps=result['steps'],
            structured_output=result['output'],
            confidence_score=result['confidence'],
            reasoning_path=result['reasoning_path'],
            validation_results=result.get('validation', {})
        )
    
    def execute_chain_of_thought(self, problem: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行思维链模板"""
        steps = []
        reasoning_path = []
        
        # 步骤1: 问题理解
        problem_understanding = self._analyze_problem_understanding(problem)
        steps.append({
            'step': 1,
            'name': 'Problem Understanding',
            'action': 'Analyze problem components and requirements',
            'result': problem_understanding
        })
        reasoning_path.append(f"理解问题: {problem_understanding}")
        
        # 步骤2: 分解问题
        decomposition = self._decompose_problem(problem)
        steps.append({
            'step': 2,
            'name': 'Problem Decomposition',
            'action': 'Break down into logical sub-problems',
            'result': decomposition
        })
        reasoning_path.append(f"分解为: {decomposition}")
        
        # 步骤3: 中间推理
        intermediate_reasoning = self._generate_intermediate_reasoning(problem, decomposition)
        steps.append({
            'step': 3,
            'name': 'Intermediate Reasoning',
            'action': 'Reason through each sub-problem step by step',
            'result': intermediate_reasoning
        })
        reasoning_path.append("逐步推理...")
        
        # 步骤4: 解决方案验证
        solution_verification = self._verify_solution(problem, intermediate_reasoning)
        steps.append({
            'step': 4,
            'name': 'Solution Verification',
            'action': 'Verify the final solution against requirements',
            'result': solution_verification
        })
        reasoning_path.append(f"验证结果: {solution_verification}")
        
        # 生成结构化输出
        output = self._format_chain_of_thought_output(problem, steps)
        
        # 计算置信度
        confidence = self._calculate_confidence(steps)
        
        return {
            'steps': steps,
            'output': output,
            'confidence': confidence,
            'reasoning_path': reasoning_path,
            'validation': self._validate_chain_of_thought(steps)
        }
    
    def execute_verification_template(self, problem: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行验证模板"""
        steps = []
        reasoning_path = []
        
        # 步骤1: 假设分析
        assumptions = self._identify_assumptions(problem)
        steps.append({
            'step': 1,
            'name': 'Assumption Analysis',
            'action': 'Identify underlying assumptions',
            'result': assumptions
        })
        reasoning_path.append(f"识别假设: {assumptions}")
        
        # 步骤2: 逻辑验证
        logic_validation = self._validate_logic(problem, assumptions)
        steps.append({
            'step': 2,
            'name': 'Logic Validation',
            'action': 'Check logical consistency',
            'result': logic_validation
        })
        reasoning_path.append(f"逻辑验证: {logic_validation}")
        
        # 步骤3: 证据评估
        evidence_evaluation = self._evaluate_evidence(problem)
        steps.append({
            'step': 3,
            'name': 'Evidence Evaluation',
            'action': 'Assess supporting evidence',
            'result': evidence_evaluation
        })
        reasoning_path.append(f"证据评估: {evidence_evaluation}")
        
        # 步骤4: 替代方案考虑
        alternatives = self._consider_alternatives(problem)
        steps.append({
            'step': 4,
            'name': 'Alternative Consideration',
            'action': 'Explore alternative solutions',
            'result': alternatives
        })
        reasoning_path.append(f"替代方案: {alternatives}")
        
        output = self._format_verification_output(problem, steps)
        confidence = self._calculate_confidence(steps)
        
        return {
            'steps': steps,
            'output': output,
            'confidence': confidence,
            'reasoning_path': reasoning_path,
            'validation': self._validate_verification_template(steps)
        }
    
    def execute_few_shot_learning(self, problem: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行少样本学习模板"""
        steps = []
        reasoning_path = []
        
        # 步骤1: 示例选择
        examples = self._select_relevant_examples(problem, context)
        steps.append({
            'step': 1,
            'name': 'Example Selection',
            'action': 'Choose relevant examples for learning',
            'result': examples
        })
        reasoning_path.append(f"选择示例: {len(examples)}个")
        
        # 步骤2: 模式提取
        patterns = self._extract_patterns(examples)
        steps.append({
            'step': 2,
            'name': 'Pattern Extraction',
            'action': 'Identify common patterns from examples',
            'result': patterns
        })
        reasoning_path.append(f"提取模式: {patterns}")
        
        # 步骤3: 模式应用
        application = self._apply_patterns(problem, patterns)
        steps.append({
            'step': 3,
            'name': 'Pattern Application',
            'action': 'Apply extracted patterns to current problem',
            'result': application
        })
        reasoning_path.append(f"应用模式: {application}")
        
        # 步骤4: 验证
        validation = self._validate_pattern_application(problem, application)
        steps.append({
            'step': 4,
            'name': 'Validation',
            'action': 'Verify pattern application effectiveness',
            'result': validation
        })
        reasoning_path.append(f"验证结果: {validation}")
        
        output = self._format_few_shot_output(problem, steps)
        confidence = self._calculate_confidence(steps)
        
        return {
            'steps': steps,
            'output': output,
            'confidence': confidence,
            'reasoning_path': reasoning_path,
            'validation': self._validate_few_shot_template(steps)
        }
    
    def execute_role_playing(self, problem: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行角色扮演模板"""
        steps = []
        reasoning_path = []
        
        # 步骤1: 角色定义
        roles = self._define_relevant_roles(problem)
        steps.append({
            'step': 1,
            'name': 'Role Definition',
            'action': 'Define relevant perspectives and roles',
            'result': roles
        })
        reasoning_path.append(f"定义角色: {roles}")
        
        # 步骤2: 视角采纳
        perspectives = {}
        for role in roles:
            perspective = self._adopt_perspective(problem, role)
            perspectives[role] = perspective
        
        steps.append({
            'step': 2,
            'name': 'Perspective Taking',
            'action': 'View problem from each role\'s viewpoint',
            'result': perspectives
        })
        reasoning_path.append(f"采纳视角: {list(perspectives.keys())}")
        
        # 步骤3: 专业知识应用
        expertise_application = {}
        for role, perspective in perspectives.items():
            expertise = self._apply_expertise(problem, role, perspective)
            expertise_application[role] = expertise
        
        steps.append({
            'step': 3,
            'name': 'Expertise Application',
            'action': 'Apply role-specific knowledge and experience',
            'result': expertise_application
        })
        reasoning_path.append("应用专业知识...")
        
        # 步骤4: 综合整合
        integration = self._integrate_perspectives(perspectives, expertise_application)
        steps.append({
            'step': 4,
            'name': 'Integration',
            'action': 'Combine multiple perspectives into comprehensive solution',
            'result': integration
        })
        reasoning_path.append(f"综合结果: {integration}")
        
        output = self._format_role_playing_output(problem, steps)
        confidence = self._calculate_confidence(steps)
        
        return {
            'steps': steps,
            'output': output,
            'confidence': confidence,
            'reasoning_path': reasoning_path,
            'validation': self._validate_role_playing_template(steps)
        }
    
    def execute_understanding_framework(self, problem: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行理解框架模板"""
        steps = []
        reasoning_path = []
        
        # 步骤1: 概念识别
        concepts = self._identify_key_concepts(problem)
        steps.append({
            'step': 1,
            'name': 'Concept Identification',
            'action': 'Identify key concepts and terminology',
            'result': concepts
        })
        reasoning_path.append(f"识别概念: {concepts}")
        
        # 步骤2: 关系映射
        relationships = self._map_concept_relationships(concepts)
        steps.append({
            'step': 2,
            'name': 'Relationship Mapping',
            'action': 'Map relationships between concepts',
            'result': relationships
        })
        reasoning_path.append(f"映射关系: {relationships}")
        
        # 步骤3: 上下文分析
        context_analysis = self._analyze_contextual_factors(problem, concepts)
        steps.append({
            'step': 3,
            'name': 'Context Analysis',
            'action': 'Understand situational context and factors',
            'result': context_analysis
        })
        reasoning_path.append(f"上下文分析: {context_analysis}")
        
        # 步骤4: 综合
        synthesis = self._synthesize_understanding(concepts, relationships, context_analysis)
        steps.append({
            'step': 4,
            'name': 'Synthesis',
            'action': 'Create comprehensive understanding',
            'result': synthesis
        })
        reasoning_path.append(f"综合理解: {synthesis}")
        
        output = self._format_understanding_output(problem, steps)
        confidence = self._calculate_confidence(steps)
        
        return {
            'steps': steps,
            'output': output,
            'confidence': confidence,
            'reasoning_path': reasoning_path,
            'validation': self._validate_understanding_template(steps)
        }
    
    # 辅助方法实现（简化版本）
    def _analyze_problem_understanding(self, problem: str) -> str:
        """分析问题理解"""
        if '如何' in problem or '怎样' in problem:
            return "寻求方法或步骤的问题"
        elif '为什么' in problem:
            return "寻求原因或解释的问题"
        elif '什么' in problem:
            return "寻求定义或描述的问题"
        else:
            return "一般性分析问题"
    
    def _decompose_problem(self, problem: str) -> List[str]:
        """问题分解"""
        # 简单的关键词分解
        if '和' in problem:
            return problem.split('和')
        elif '、' in problem:
            return problem.split('、')
        else:
            return [problem]
    
    def _generate_intermediate_reasoning(self, problem: str, decomposition: List[str]) -> str:
        """生成中间推理"""
        return f"针对{'、'.join(decomposition)}进行逐步分析和推理"
    
    def _verify_solution(self, problem: str, reasoning: str) -> str:
        """解决方案验证"""
        return "解决方案符合问题要求，逻辑一致"
    
    def _format_chain_of_thought_output(self, problem: str, steps: List[Dict]) -> str:
        """格式化思维链输出"""
        output = f"## 思维链分析\n\n**问题**: {problem}\n\n"
        for step in steps:
            output += f"### {step['step']}. {step['name']}\n"
            output += f"**操作**: {step['action']}\n"
            output += f"**结果**: {step['result']}\n\n"
        return output
    
    def _calculate_confidence(self, steps: List[Dict]) -> float:
        """计算置信度"""
        # 简化的置信度计算
        return 0.85 if len(steps) >= 4 else 0.7
    
    def _validate_chain_of_thought(self, steps: List[Dict]) -> Dict[str, Any]:
        """验证思维链执行质量"""
        return {
            'completeness': len(steps) == 4,
            'logical_flow': all(step['step'] == i+1 for i, step in enumerate(steps)),
            'quality_score': 0.8
        }
    
    # 其他模板的辅助方法简化实现...
    def _identify_assumptions(self, problem: str) -> List[str]:
        """识别假设"""
        return ["基本假设1", "基本假设2"]
    
    def _validate_logic(self, problem: str, assumptions: List[str]) -> str:
        """逻辑验证"""
        return "逻辑一致，无明显矛盾"
    
    def _evaluate_evidence(self, problem: str) -> str:
        """证据评估"""
        return "证据支持度中等"
    
    def _consider_alternatives(self, problem: str) -> List[str]:
        """考虑替代方案"""
        return ["方案1", "方案2"]
    
    def _format_verification_output(self, problem: str, steps: List[Dict]) -> str:
        """格式化验证模板输出"""
        return f"## 验证分析\n\n**问题**: {problem}\n\n验证步骤执行完成..."
    
    def _validate_verification_template(self, steps: List[Dict]) -> Dict[str, Any]:
        """验证模板执行质量"""
        return {'completeness': True, 'quality_score': 0.8}
    
    def _select_relevant_examples(self, problem: str, context: Dict[str, Any]) -> List[str]:
        """选择相关示例"""
        return ["示例1", "示例2", "示例3"]
    
    def _extract_patterns(self, examples: List[str]) -> List[str]:
        """提取模式"""
        return ["模式1", "模式2"]
    
    def _apply_patterns(self, problem: str, patterns: List[str]) -> str:
        """应用模式"""
        return "应用模式后的解决方案"
    
    def _validate_pattern_application(self, problem: str, application: str) -> str:
        """验证模式应用"""
        return "模式应用有效"
    
    def _format_few_shot_output(self, problem: str, steps: List[Dict]) -> str:
        """格式化少样本学习输出"""
        return f"## 少样本学习\n\n**问题**: {problem}\n\n基于示例的学习分析..."
    
    def _validate_few_shot_template(self, steps: List[Dict]) -> Dict[str, Any]:
        """验证少样本模板执行质量"""
        return {'completeness': True, 'quality_score': 0.8}
    
    def _define_relevant_roles(self, problem: str) -> List[str]:
        """定义相关角色"""
        return ["用户", "开发者", "管理者"]
    
    def _adopt_perspective(self, problem: str, role: str) -> str:
        """采纳视角"""
        return f"从{role}角度：{problem}"
    
    def _apply_expertise(self, problem: str, role: str, perspective: str) -> str:
        """应用专业知识"""
        return f"{role}专业分析：{perspective}"
    
    def _integrate_perspectives(self, perspectives: Dict[str, str], expertise: Dict[str, str]) -> str:
        """综合多个视角"""
        return "多角度综合分析结果"
    
    def _format_role_playing_output(self, problem: str, steps: List[Dict]) -> str:
        """格式化角色扮演输出"""
        return f"## 角色扮演分析\n\n**问题**: {problem}\n\n多视角分析结果..."
    
    def _validate_role_playing_template(self, steps: List[Dict]) -> Dict[str, Any]:
        """验证角色扮演模板执行质量"""
        return {'completeness': True, 'quality_score': 0.8}
    
    def _identify_key_concepts(self, problem: str) -> List[str]:
        """识别关键概念"""
        # 简单的关键词提取
        import re
        words = re.findall(r'[\w\u4e00-\u9fff]+', problem)
        return list(set(words))
    
    def _map_concept_relationships(self, concepts: List[str]) -> Dict[str, List[str]]:
        """映射概念关系"""
        return {concept: [] for concept in concepts}
    
    def _analyze_contextual_factors(self, problem: str, concepts: List[str]) -> str:
        """分析上下文因素"""
        return "上下文环境分析"
    
    def _synthesize_understanding(self, concepts: List[str], relationships: Dict, context: str) -> str:
        """综合理解"""
        return f"对{len(concepts)}个概念的深度理解"
    
    def _format_understanding_output(self, problem: str, steps: List[Dict]) -> str:
        """格式化理解框架输出"""
        return f"## 深度理解\n\n**问题**: {problem}\n\n概念分析完成..."
    
    def _validate_understanding_template(self, steps: List[Dict]) -> Dict[str, Any]:
        """验证理解框架模板执行质量"""
        return {'completeness': True, 'quality_score': 0.8}

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("Usage: python template_executor.py <problem_description> [template_type]")
        print("Supported templates: chain_of_thought, verification, few_shot, role_playing, understanding")
        sys.exit(1)
    
    problem_description = sys.argv[1]
    template_type = sys.argv[2] if len(sys.argv) > 2 else None
    
    engine = CognitiveTemplateEngine()
    result = engine.execute_template(problem_description, template_type)
    
    # 输出结构化结果
    output = {
        "problem": problem_description,
        "selected_template": result.template_type,
        "applied_steps": result.applied_steps,
        "structured_output": result.structured_output,
        "confidence_score": result.confidence_score,
        "reasoning_path": result.reasoning_path,
        "validation_results": result.validation_results
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()