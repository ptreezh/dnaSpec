"""
DSGS Context Engineering Skills - AI原生实现（清洁版）
基于AI模型原生智能的上下文工程技能系统
"""
import json
import random
from typing import Dict, Any
from src.dsgs_spec_kit_integration.core.skill import DSGSSkill, SkillResult, SkillStatus


from src.dsgs_spec_kit_integration.core.skill import DSGSSkill, SkillResult, SkillStatus

class DSGSSkillBase(DSGSSkill):
    """DSGS技能基类"""
    
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self.name = name
        self.description = description


def simulate_ai_completion(instruction: str) -> str:
    """
    模拟AI模型完成度函数（真实实现中会调用AI API）
    """
    # 在实际实现中，这里会调用AI模型API
    # 目前返回基于指令内容的模拟结果
    
    if "分析" in instruction or "评估" in instruction:
        # 模拟分析结果
        import re
        # 提取上下文长度信息（从指令中提取原上下文）
        context_match = re.search(r'"([^"]+)"', instruction)
        context_text = context_match.group(1) if context_match else "unknown context"
        
        # 计算指标
        clarity = min(1.0, max(0.0, 0.5 + len(context_text) * 0.0001))
        relevance = min(1.0, max(0.0, 0.7 + (0.1 if any(kw in context_text for kw in ['系统', '功能', '任务']) else 0)))
        completeness = min(1.0, max(0.0, 0.3 + (0.3 if any(kw in context_text for kw in ['约束', '要求', '目标']) else 0)))
        consistency = min(1.0, max(0.0, 0.8 - (0.2 if any(kw in context_text for kw in ['但是', '然而']) else 0)))
        efficiency = min(1.0, max(0.0, 1.0 - len(context_text) * 0.00005))
        
        return json.dumps({
            "context_length": len(context_text),
            "token_count_estimate": max(1, len(context_text) // 4),
            "metrics": {
                "clarity": round(clarity, 2),
                "relevance": round(relevance, 2),
                "completeness": round(completeness, 2),
                "consistency": round(consistency, 2),
                "efficiency": round(efficiency, 2)
            },
            "suggestions": [
                "增加更明确的目标描述",
                "补充约束条件和具体要求",
                "提高表述清晰度"
            ],
            "issues": [
                "缺少明确的约束条件" if completeness < 0.6 else "",
                "部分表述可以更精确" if clarity < 0.7 else ""
            ],
            "confidence": 0.85
        }, ensure_ascii=False, indent=2)
    
    elif "优化" in instruction or "改进" in instruction:
        # 模拟优化结果
        goals_match = re.search(r'优化目标:\s*([^\n]+)', instruction)
        goals_text = goals_match.group(1) if goals_match else "clarity,completeness"
        
        goals = [g.strip() for g in goals_text.split(',') if g.strip()]
        
        original_match = re.search(r'原始上下文:\s*["\']([^"\']+)["\']', instruction)
        original_context = original_match.group(1) if original_match else "待优化内容"
        
        optimized_context = original_context
        applied_optimizations = []
        
        if any(goal in goals_text for goal in ['clarity', '清晰度']):
            optimized_context += "\n\n请明确具体的目标和约束条件。"
            applied_optimizations.append("提升表述清晰度")
        
        if any(goal in goals_text for goal in ['completeness', '完整性']):
            optimized_context += "\n\n约束条件: 需在指定时间内完成\n明确目标: 实现预期功能\n前提假设: 有必要的资源支持"
            applied_optimizations.append("补充完整性要素")
            
        return json.dumps({
            "original_context": original_context,
            "optimized_context": optimized_context,
            "applied_optimizations": applied_optimizations,
            "improvement_metrics": {
                "clarity": 0.2 if any(goal in goals_text for goal in ['clarity', '清晰度']) else 0.0,
                "relevance": 0.1 if any(goal in goals_text for goal in ['relevance', '相关性']) else 0.0,
                "completeness": 0.3 if any(goal in goals_text for goal in ['completeness', '完整性']) else 0.0,
                "conciseness": -0.05 if any(goal in goals_text for goal in ['conciseness', '简洁性']) else 0.0
            },
            "optimization_summary": f"根据目标 {', '.join(goals)} 完成优化"
        }, ensure_ascii=False, indent=2)
    
    else:
        # 默认返回
        return json.dumps({
            "enhanced_content": f"AI处理了指令: {instruction[:50]}...",
            "success": True
        }, ensure_ascii=False, indent=2)


class ContextAnalysisSkill(DSGSSkillBase):
    """上下文分析技能 - 利用AI模型原生智能进行分析"""
    
    def __init__(self):
        super().__init__(
            name="dsgs-context-analysis",
            description="DSGS上下文分析技能 - 利用AI模型原生智能进行专业上下文质量分析"
        )
    
    def execute_with_ai(self, context: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """执行上下文分析"""
        if not context.strip():
            return {
                'success': False,
                'error': '上下文不能为空'
            }
        
        analysis_instruction = f"""
作为专业的上下文质量分析师，请对以下上下文进行五维度评估：

上下文: "{context}"

维度 (0.0-1.0评分):
1. 清晰度 (Clarity): 表达明确性
2. 相关性 (Relevance): 任务关联性  
3. 完整性 (Completeness): 信息完备性
4. 一致性 (Consistency): 逻辑一致性
5. 效率 (Efficiency): 信息密度

以JSON格式返回结果，包含metrics、suggestions、issues。
"""
        
        try:
            # 在实际实现中，这里会调用真实的AI API
            simulation_result = simulate_ai_completion(analysis_instruction)
            result = json.loads(simulation_result)
            
            return {
                'success': True,
                'result': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'分析执行失败: {str(e)}'
            }


class ContextOptimizationSkill(DSGSSkillBase):
    """上下文优化技能 - 利用AI模型原生智能进行优化"""
    
    def __init__(self):
        super().__init__(
            name="dsgs-context-optimization",
            description="DSGS上下文优化技能 - 利用AI模型原生智能优化上下文质量"
        )
    
    def execute_with_ai(self, context: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """执行上下文优化"""
        if not context.strip():
            return {
                'success': False,
                'error': '上下文不能为空'
            }
        
        params = params or {}
        goals = params.get('optimization_goals', ['clarity', 'completeness'])
        
        if isinstance(goals, str):
            goals = [g.strip() for g in goals.split(',') if g.strip()]
        
        optimization_instruction = f"""
根据以下目标优化上下文:

优化目标: {', '.join(goals)}

原始上下文: "{context}"

请返回优化后的内容和应用的优化措施，以JSON格式。
"""
        
        try:
            # 在实际实现中，这里会调用真实的AI API
            simulation_result = simulate_ai_completion(optimization_instruction)
            result = json.loads(simulation_result)
            
            return {
                'success': True,
                'result': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'优化执行失败: {str(e)}'
            }


class CognitiveTemplateSkill(DSGSSkillBase):
    """认知模板技能 - 利用AI模型原生智能应用认知模板"""
    
    def __init__(self):
        super().__init__(
            name="dsgs-cognitive-template",
            description="DSGS认知模板技能 - 利用AI模型原生智能应用认知模板结构化任务"
        )
    
    def execute_with_ai(self, context: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """执行认知模板应用"""
        if not context.strip():
            return {
                'success': False,
                'error': '上下文不能为空'
            }
        
        params = params or {}
        template_type = params.get('template', 'chain_of_thought')
        
        template_descriptions = {
            'chain_of_thought': '思维链推理',
            'few_shot': '少样本学习',
            'verification': '验证检查',
            'role_playing': '角色扮演',
            'understanding': '深度理解'
        }
        
        template_desc = template_descriptions.get(template_type, '未知模板')
        
        if template_type == 'chain_of_thought':
            template_instruction = f"""
使用思维链方法分析以下任务：

任务: {context}

按以下步骤分析:
1. 问题理解
2. 步骤分解
3. 中间推理
4. 验证检查
5. 最终答案

返回结构化分析结果。
"""
        elif template_type == 'verification':
            template_instruction = f"""
使用验证框架分析以下内容：

原始内容: {context}

执行验证步骤:
1. 初步答案
2. 逻辑一致性检查
3. 事实准确性检查
4. 完整性检查
5. 最终确认

返回验证结果。
"""
        else:
            # 默认使用思维链
            template_instruction = f"""
使用{template_desc}方法分析任务: {context}

请返回结构化分析结果。
"""
        
        try:
            # 在实际实现中，这里会调用真实的AI API
            enhanced_content = f"""
### 认知模板应用: {template_type} ({template_desc})

**原始任务**: {context}

**结构化分析**:
[AI模型将应用{template_desc}认知框架进行专业分析...]

**专业结果**:
[返回基于{template_desc}框架的专业分析结果]
"""
            
            return {
                'success': True,
                'result': {
                    'success': True,
                    'template_type': template_type,
                    'template_description': template_desc,
                    'original_context': context,
                    'enhanced_context': enhanced_content,
                    'confidence': 0.85
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'模板应用失败: {str(e)}',
                'result': {'success': False}
            }


def execute(args: Dict[str, Any]) -> str:
    """
    执行函数 - 与AI CLI平台集成的接口
    """
    skill_name = args.get('skill', 'context-analysis')
    context_input = args.get('context', '') or args.get('request', '')
    params = args.get('params', {})
    
    if not context_input:
        return "错误: 未提供需要处理的上下文"
    
    try:
        if skill_name == 'context-analysis':
            skill = ContextAnalysisSkill()
            result = skill.execute_with_ai(context_input, params)
            
            if result['success']:
                analysis = result['result']
                output_lines = []
                output_lines.append("上下文分析结果:")
                output_lines.append(f"长度: {analysis['context_length']} 字符")
                output_lines.append(f"Token估算: {analysis['token_count_estimate']}")
                output_lines.append("")
                
                output_lines.append("五维质量指标 (0.0-1.0):")
                for metric, score in analysis['metrics'].items():
                    names = {'clarity': '清晰度', 'relevance': '相关性', 'completeness': '完整性', 'consistency': '一致性', 'efficiency': '效率'}
                    indicator = "🟢" if score >= 0.7 else "🟡" if score >= 0.4 else "🔴"
                    output_lines.append(f"  {indicator} {names.get(metric, metric)}: {score:.2f}")
                
                if analysis.get('suggestions'):
                    output_lines.append("\n优化建议:")
                    for s in analysis['suggestions'][:3]:  # 显示前3条
                        if s.strip():  # 过滤空建议
                            output_lines.append(f"  • {s}")
                
                if analysis.get('issues'):
                    output_lines.append("\n识别问题:")
                    for i in analysis['issues']:
                        if i.strip():  # 过滤空问题
                            output_lines.append(f"  • {i}")
                
                return "\n".join(output_lines)
            else:
                return f"错误: {result.get('error', '分析失败')}"
        
        elif skill_name == 'context-optimization':
            skill = ContextOptimizationSkill()
            result = skill.execute_with_ai(context_input, params)
            
            if result['success']:
                optimization = result['result']
                output_lines = []
                output_lines.append("上下文优化结果:")
                output_lines.append(f"原始长度: {len(optimization['original_context'])} 字符")
                output_lines.append(f"优化后长度: {len(optimization['optimized_context'])} 字符")
                output_lines.append("")
                
                if 'applied_optimizations' in optimization:
                    output_lines.append("应用的优化措施:")
                    for opt in optimization['applied_optimizations']:
                        output_lines.append(f"  • {opt}")
                
                if 'improvement_metrics' in optimization:
                    output_lines.append("\n改进指标:")
                    for metric, change in optimization['improvement_metrics'].items():
                        if change != 0:  # 只显示有变化的指标
                            direction = "↗️" if change > 0 else "↘️" if change < 0 else "➡️"
                            output_lines.append(f"  {direction} {metric}: {change:+.2f}")
                
                output_lines.append("\n优化后上下文:")
                output_lines.append(optimization['optimized_context'])
                
                return "\n".join(output_lines)
            else:
                return f"错误: {result.get('error', '优化失败')}"
        
        elif skill_name == 'cognitive-template':
            skill = CognitiveTemplateSkill()
            result = skill.execute_with_ai(context_input, params)
            
            if result['success'] and result['result']['success']:
                template_result = result['result']
                output_lines = []
                output_lines.append(f"认知模板应用: {template_result['template_type']} ({template_result['template_description']})")
                output_lines.append("="*60)
                output_lines.append("")
                output_lines.append("结构化输出:")
                output_lines.append(template_result['enhanced_context'])
                
                return "\n".join(output_lines)
            else:
                return f"错误: {result.get('error', '模板应用失败')}"
        else:
            available_skills = ['context-analysis', 'context-optimization', 'cognitive-template']
            return f"错误: 未知技能 '{skill_name}'. 可用技能: {', '.join(available_skills)}"
    
    except Exception as e:
        return f"错误: 执行过程异常 - {str(e)}"


def get_available_skills() -> list:
    """获取可用技能列表"""
    return ['context-analysis', 'context-optimization', 'cognitive-template']


def get_skill_descriptions() -> dict:
    """获取技能描述"""
    return {
        'context-analysis': '上下文质量五维专业分析',
        'context-optimization': '基于AI智能的上下文优化',
        'cognitive-template': '认知模板结构化任务分析'
    }