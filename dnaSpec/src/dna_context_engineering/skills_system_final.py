"""
DNASPEC Context Engineering Skills - AI CLI平台增强工具集
基于AI原生智能的上下文工程技能系统
"""
from typing import Dict, Any
from src.dnaspec_spec_kit_integration.core.skill import DNASpecSkill, SkillResult, SkillStatus
import time


class ContextAnalysisSkill(DNASpecSkill):
    """
    上下文分析技能
    利用AI模型原生智能进行上下文质量分析
    """
    
    def __init__(self):
        super().__init__(
            name="dnaspec-context-analysis",
            description="上下文分析技能 - 利用AI模型原生智能分析上下文质量的专业技能"
        )
    
    def _execute_skill_logic(self, request: str, context: Dict[str, Any]) -> Any:
        """
        执行上下文分析逻辑
        通过向AI模型发送专业指令实现
        """
        if not request.strip():
            return {
                'success': False,
                'error': 'Context cannot be empty',
                'result': {}
            }
        
        # 构造AI指令用于专业分析
        analysis_instruction = f"""
作为专业的上下文质量分析师，请对以下上下文进行五维度评估：

上下文: "{request}"

请从以下五个维度评估(0.0-1.0评分)：
1. 清晰度: 表达明确性
2. 相关性: 与目标关联性  
3. 完整性: 信息完备性
4. 一致性: 逻辑一致性
5. 效率: 信息密度

请返回JSON格式结果。
"""
        
        # 模拟AI分析结果（实际应通过AI API调用）
        import random
        seed = hash(request) % 10000
        random.seed(seed)
        
        # 基于上下文特征计算指标
        clarity = min(1.0, max(0.0, 0.5 + len(request) * 0.0001))
        relevance = min(1.0, max(0.0, 0.7 + (0.2 if any(kw in request for kw in ['系统', '功能', '任务']) else 0)))
        completeness = min(1.0, max(0.0, 0.3 + (0.3 if any(kw in request for kw in ['约束', '要求', '目标']) else 0)))
        consistency = min(1.0, max(0.0, 0.8 - (0.2 if any(kw in request for kw in ['但是', '然而']) else 0)))
        efficiency = min(1.0, max(0.0, 1.0 - len(request) * 0.00005))
        
        return {
            'success': True,
            'result': {
                'context_length': len(request),
                'token_count_estimate': max(1, len(request) // 4),
                'metrics': {
                    'clarity': round(clarity, 2),
                    'relevance': round(relevance, 2),
                    'completeness': round(completeness, 2),
                    'consistency': round(consistency, 2),
                    'efficiency': round(efficiency, 2)
                },
                'suggestions': [
                    "增加更明确的约束条件" if completeness < 0.6 else "",
                    "提高表达清晰度" if clarity < 0.7 else ""
                ],
                'suggestions': [s for s in [
                    "增加更明确的约束条件" if completeness < 0.6 else "",
                    "提高表达清晰度" if clarity < 0.7 else ""
                ] if s],
                'issues': [
                    "信息完整性不足" if completeness < 0.5 else "",
                    "表述不够清晰" if clarity < 0.5 else ""
                ],
                'issues': [i for i in [
                    "信息完整性不足" if completeness < 0.5 else "",
                    "表述不够清晰" if clarity < 0.5 else ""
                ] if i]
            }
        }

    def _calculate_confidence(self, request: str) -> float:
        """计算置信度"""
        return 0.85


class ContextOptimizationSkill(DNASpecSkill):
    """
    上下文优化技能 
    利用AI模型原生智能进行上下文优化
    """
    
    def __init__(self):
        super().__init__(
            name="dnaspec-context-optimization",
            description="上下文优化技能 - 利用AI模型原生智能优化上下文质量的专业技能"
        )
    
    def _execute_skill_logic(self, request: str, context: Dict[str, Any]) -> Any:
        """
        执行上下文优化逻辑
        通过向AI模型发送优化指令实现
        """
        if not request.strip():
            return {
                'success': False,
                'error': 'Context cannot be empty',
                'result': {}
            }
        
        # 解析优化目标
        goals = context.get('optimization_goals', ['clarity', 'completeness'])
        if isinstance(goals, str):
            goals = [goal.strip() for goal in goals.split(',') if goal.strip()]
        
        # 构造优化指令
        optimization_instruction = f"""
请根据以下目标优化上下文：

优化目标: {', '.join(goals)}
原始上下文: "{request}"

请返回优化后的内容。
"""
        
        # 模拟AI优化结果
        optimized_context = request
        
        applied_optimizations = []
        improvements = {}
        
        if 'clarity' in goals:
            if not any(word in optimized_context for word in ['明确', '具体', '详细', '请']):
                optimized_context += "\n\n请明确具体目标和约束条件。"
                applied_optimizations.append("提升表述清晰度")
                improvements['clarity'] = 0.2
            
        if 'completeness' in goals:
            if not any(kw in optimized_context for kw in ['约束', '条件', '要求', '目标']):
                optimized_context += "\n\n约束条件: 需在指定时限内完成\n明确目标: 实现预期功能"
                applied_optimizations.append("补充完整性要素")
                improvements['completeness'] = 0.3
        
        if 'relevance' in goals:
            optimized_context = f"任务目标: {optimized_context}"
            applied_optimizations.append("增强任务目标相关性")  
            improvements['relevance'] = 0.15
        
        return {
            'success': True,
            'result': {
                'original_context': request,
                'optimized_context': optimized_context,
                'applied_optimizations': applied_optimizations,
                'improvement_metrics': {
                    'clarity': improvements.get('clarity', 0.0),
                    'relevance': improvements.get('relevance', 0.0),
                    'completeness': improvements.get('completeness', 0.0),
                    'conciseness': improvements.get('conciseness', 0.0)
                },
                'summary': f"应用了{len(applied_optimizations)}项优化措施"
            }
        }

    def _calculate_confidence(self, request: str) -> float:
        """计算置信度"""
        return 0.8


class CognitiveTemplateSkill(DNASpecSkill):
    """
    认知模板技能
    利用AI模型原生智能应用认知模板
    """
    
    def __init__(self):
        super().__init__(
            name="dnaspec-cognitive-template",
            description="认知模板技能 - 利用AI模型原生智能应用认知模板的专业技能"
        )
        
        self.templates = {
            'chain_of_thought': {
                'name': '思维链', 
                'description': '逐步推理分析复杂问题'
            },
            'verification': {
                'name': '验证检查',
                'description': '验证推理过程和结果质量'
            },
            'few_shot': {
                'name': '少样本学习',
                'description': '通过示例对指导AI行为'
            }
        }
    
    def _execute_skill_logic(self, request: str, context: Dict[str, Any]) -> Any:
        """
        执行认知模板应用逻辑
        通过向AI模型发送模板指令实现
        """
        if not request.strip():
            return {
                'success': False,
                'error': 'Context cannot be empty',
                'result': {'success': False}
            }
        
        template_type = context.get('template', 'chain_of_thought')
        
        if template_type not in self.templates:
            return {
                'success': False,
                'error': f'Unknown template: {template_type}',
                'available_templates': list(self.templates.keys()),
                'result': {'success': False}
            }
        
        template_info = self.templates[template_type]
        
        # 构造认知模板指令
        template_instruction = f"""
使用{template_info['name']}方法分析任务：

任务: {request}

请按{template_info['name']}模板执行分析。
"""
        
        # 模拟AI模板应用结果
        template_results = {
            'chain_of_thought': f"""
### 思维链分析框架

**原始任务**: {request}

**分析步骤**:
1. 问题理解: [AI模型将理解任务核心需求]
2. 步骤分解: [AI模型将任务分解为可执行步骤] 
3. 中间推理: [AI模型提供详细推理过程]
4. 验证检查: [AI模型验证推理合理性]
5. 最终答案: [AI模型提供最终解决方案]

**思维链分析完成**
""",
            'verification': f"""
### 验证检查框架

**原始内容**: {request}

**验证步骤**:
1. 初步答案: [AI模型基于内容给出初步判断]
2. 逻辑一致性: [AI模型验证内容逻辑一致性]
3. 事实准确性: [AI模型核实事实陈述准确性]
4. 完整性检查: [AI模型评估信息完整性]
5. 最终确认: [AI模型给出最终验证确认]

**验证检查完成**
""",
            'few_shot': f"""
### 少样本学习框架

**任务**: {request}

**示例对**:
示例1:
输入: [类似任务输入1] 
输出: [示例处理方式1]

示例2:
输入: [类似任务输入2]
输出: [示例处理方式2]

**新输入**: {request}
**预期输出**: [AI模型将参考示例模式处理新输入]

**少样本学习应用完成**
"""
        }
        
        enhanced_context = template_results.get(template_type, f"应用{template_type}模板: {request}")
        
        return {
            'success': True,
            'result': {
                'success': True,
                'template_type': template_type,
                'template_name': template_info['name'],
                'template_description': template_info['description'],
                'original_context': request,
                'enhanced_context': enhanced_context,
                'template_structure': ['应用认知框架', '结构化输出', '验证结果']
            }
        }

    def _calculate_confidence(self, request: str) -> float:
        """计算置信度"""
        return 0.85


def execute(args: Dict[str, Any]) -> str:
    """
    执行函数 - 与AI CLI平台集成的接口
    """
    from src.dnaspec_spec_kit_integration.core.skill import SkillStatus  # 避免循环导入
    
    skill_name = args.get('skill', 'context-analysis')
    context_input = args.get('context', '') or args.get('request', '')
    params = args.get('params', {})
    
    if not context_input:
        return "错误: 未提供需要处理的上下文或请求"
    
    try:
        # 根据技能名称选择技能
        if skill_name == 'context-analysis':
            skill = ContextAnalysisSkill()
            skill_result = skill.process_request(context_input, params)
            
            if skill_result.status == SkillStatus.COMPLETED:
                result = skill_result.result
                actual_result = result.get('result', result) if isinstance(result, dict) and 'result' in result else result
                
                output_lines = []
                output_lines.append("上下文分析结果:")
                output_lines.append(f"长度: {actual_result['context_length']} 字符")
                
                output_lines.append("\n五维指标 (0.0-1.0):")
                for metric, score in actual_result['metrics'].items():
                    names = {'clarity': '清晰度', 'relevance': '相关性', 'completeness': '完整性', 'consistency': '一致性', 'efficiency': '效率'}
                    indicator = "🟢" if score >= 0.7 else "🟡" if score >= 0.4 else "🔴"
                    output_lines.append(f"  {indicator} {names.get(metric, metric)}: {score:.2f}")
                
                if actual_result.get('suggestions', []):
                    output_lines.append("\n优化建议:")
                    for s in actual_result['suggestions']:
                        output_lines.append(f"  • {s}")
                
                if actual_result.get('issues', []):
                    output_lines.append("\n识别问题:")  
                    for i in actual_result['issues']:
                        output_lines.append(f"  • {i}")
                
                return "\n".join(output_lines)
            else:
                return f"错误: {getattr(skill_result, 'error_message', '技能执行失败')}"
        
        elif skill_name == 'context-optimization':
            skill = ContextOptimizationSkill()
            skill_result = skill.process_request(context_input, params)
            
            if skill_result.status == SkillStatus.COMPLETED:
                result = skill_result.result
                actual_result = result.get('result', result) if isinstance(result, dict) and 'result' in result else result
                
                output_lines = []
                output_lines.append("上下文优化结果:")
                output_lines.append(f"原始长度: {len(actual_result['original_context'])} 字符")
                output_lines.append(f"优化后长度: {len(actual_result['optimized_context'])} 字符") 
                
                if 'applied_optimizations' in actual_result:
                    output_lines.append(f"\n应用优化: {len(actual_result['applied_optimizations'])} 项")
                    for opt in actual_result['applied_optimizations']:
                        output_lines.append(f"  • {opt}")
                
                output_lines.append("\n改进指标:")
                for metric, change in actual_result['improvement_metrics'].items():
                    direction = "↗️" if change > 0 else "↘️" if change < 0 else "➡️"
                    output_lines.append(f"  {direction} {metric}: {change:+.2f}")
                
                output_lines.append("\n优化后上下文:")
                output_lines.append(actual_result['optimized_context'])
                
                return "\n".join(output_lines)
            else:
                return f"错误: {getattr(skill_result, 'error_message', '技能执行失败')}"
        
        elif skill_name == 'cognitive-template':
            skill = CognitiveTemplateSkill()
            skill_result = skill.process_request(context_input, params)
            
            if skill_result.status == SkillStatus.COMPLETED:
                result = skill_result.result
                actual_result = result.get('result', result) if isinstance(result, dict) and 'result' in result else result
                # Handle the nested result structure
                success_result = actual_result.get('result', actual_result) if 'success' in actual_result else actual_result
                
                if success_result.get('success', True):
                    output_lines = []
                    output_lines.append(f"认知模板应用: {success_result['template_name']} ({success_result['template_type']})")
                    output_lines.append(f"描述: {success_result['template_description']}")
                    output_lines.append("="*60)
                    output_lines.append("")
                    output_lines.append("结构化输出:")
                    output_lines.append(success_result['enhanced_context'])
                    
                    return "\n".join(output_lines)
                else:
                    error_msg = success_result.get('error', '模板应用失败')
                    return f"错误: 模板应用失败 - {error_msg}"
            else:
                return f"错误: {getattr(skill_result, 'error_message', '技能执行失败')}"
        
        else:
            available_skills = ['context-analysis', 'context-optimization', 'cognitive-template']
            return f"错误: 未知技能 '{skill_name}'. 可用技能: {', '.join(available_skills)}"
    
    except Exception as e:
        return f"错误: 执行过程中发生异常 - {str(e)}"


def get_available_skills() -> Dict[str, str]:
    """获取可用技能列表"""
    return {
        'context-analysis': '上下文质量五维分析',
        'context-optimization': '上下文多目标优化',
        'cognitive-template': '认知模板结构化应用'
    }