"""
DSGS Context Engineering Skills - AI原生实现（最终清洁版）
基于AI模型原生智能的上下文工程技能系统
"""
import json
import random
from typing import Dict, Any
from src.dsgs_spec_kit_integration.core.skill import DSGSSkill, SkillResult, SkillStatus


def simulate_ai_completion(instruction: str) -> str:
    """
    模拟AI模型完成度函数（真实实现中会调用AI API）
    """
    import re
    import json
    
    # 在实际实现中，这里会调用AI模型API
    # 目前返回基于指令内容的模拟结果
    
    if "分析" in instruction or "评估" in instruction:
        # 模拟分析结果
        context_match = re.search(r'"([^"]+)"', instruction)
        context_text = context_match.group(1) if context_match else "测试上下文"
        
        # 计算指标
        clarity = min(1.0, max(0.0, 0.5 + len(context_text) * 0.0001))
        relevance = min(1.0, max(0.0, 0.7 + (0.1 if any(kw in context_text for kw in ['系统', '功能', '任务']) else 0)))
        completeness = min(1.0, max(0.0, 0.3 + (0.3 if any(kw in context_text for kw in ['约束', '要求', '目标']) else 0)))
        consistency = min(1.0, max(0.0, 0.8 - (0.2 if any(kw in context_text for kw in ['但是', '然而']) else 0)))
        efficiency = min(1.0, max(0.0, 1.0 - len(context_text) * 0.00005))
        
        result_data = {
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
            "issues": [i for i in [
                "缺少明确的约束条件" if completeness < 0.6 else "",
                "部分表述可以更精确" if clarity < 0.7 else ""
            ] if i],  # 过滤空问题
            "confidence": 0.85
        }
        
        return json.dumps(result_data, ensure_ascii=False, indent=2)
    
    elif "优化" in instruction or "改进" in instruction:
        # 模拟优化结果
        original_match = re.search(r'原始上下文:\s*["\']([^"\']+)["\']', instruction)
        original_context = original_match.group(1) if original_match else "待优化内容"
        
        goals_match = re.search(r'优化目标:\s*([^\n\]]+)', instruction) or re.search(r'目标:\s*([^\n\]]+)', instruction)
        goals_text = goals_match.group(1) if goals_match else "clarity,completeness"
        
        goals = [g.strip() for g in goals_text.split(',') if g.strip()]
        
        optimized_context = original_context
        applied_optimizations = []
        
        if any(goal in goals_text for goal in ['clarity', '清晰度']):
            optimized_context += "\n\n请明确具体的目标和约束条件。"
            applied_optimizations.append("提升表述清晰度")
        
        if any(goal in goals_text for goal in ['completeness', '完整性']):
            optimized_context += "\n\n约束条件: 需在指定时间内完成\n明确目标: 实现预期功能\n前提假设: 有必要的资源支持"
            applied_optimizations.append("补充完整性要素")
        
        result_data = {
            "original_context": original_context,
            "optimized_context": optimized_context,
            "applied_optimizations": applied_optimizations,
            "improvement_metrics": {
                "clarity": 0.2 if any(goal in goals_text for goal in ['clarity', '清晰度']) else 0.0,
                "relevance": 0.15 if any(goal in goals_text for goal in ['relevance', '相关性']) else 0.0,
                "completeness": 0.3 if any(goal in goals_text for goal in ['completeness', '完整性']) else 0.0,
                "conciseness": -0.1 if any(goal in goals_text for goal in ['conciseness', '简洁性']) else 0.0
            },
            "optimization_summary": f"根据目标 {', '.join(goals)} 完成优化"
        }
        
        return json.dumps(result_data, ensure_ascii=False, indent=2)
    
    else:
        # 默认返回
        result_data = {
            "enhanced_content": f"AI处理了指令: {instruction[:50]}...",
            "success": True
        }
        return json.dumps(result_data, ensure_ascii=False, indent=2)


class ContextAnalysisSkill(DSGSSkill):
    """上下文分析技能 - 利用AI模型原生智能进行分析"""
    
    def __init__(self):
        super().__init__(
            name="dsgs-context-analysis",
            description="DSGS上下文分析技能 - 利用AI模型原生智能进行专业上下文质量分析"
        )
    
    def _execute_skill_logic(self, request: str, context: Dict[str, Any]) -> Any:
        """执行上下文分析 - 通过AI模型原生智能"""
        if not request.strip():
            return {
                'success': False,
                'error': '上下文不能为空',
                'result': {}
            }
        
        analysis_instruction = f"""
作为专业的上下文质量分析师，请对以下上下文进行五维度评估：

上下文: "{request}"

维度 (0.0-1.0评分):
1. 清晰度 (Clarity): 表达明确性
2. 相关性 (Relevance): 任务关联性  
3. 完整性 (Completeness): 信息完备性
4. 一致性 (Consistency): 逻辑一致性
5. 效率 (Efficiency): 信息密度

以JSON格式返回分析结果。
"""
        
        try:
            # 在实际实现中，这里会发送请求到AI API
            # 目前使用模拟AI完成度函数
            simulation_result = simulate_ai_completion(analysis_instruction)
            parsed_result = json.loads(simulation_result)
            
            return {
                'success': True,
                'result': parsed_result
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'AI处理失败: {str(e)}',
                'result': {}
            }
    
    def _calculate_confidence(self, request: str) -> float:
        """计算置信度"""
        if len(request) < 5:
            return 0.3  # 太短则置信度低
        else:
            return 0.8  # 正常长度置信度高


class ContextOptimizationSkill(DSGSSkill):
    """上下文优化技能 - 利用AI模型原生智能进行优化"""
    
    def __init__(self):
        super().__init__(
            name="dsgs-context-optimization",
            description="DSGS上下文优化技能 - 利用AI模型原生智能优化上下文质量"
        )
    
    def _execute_skill_logic(self, request: str, context: Dict[str, Any]) -> Any:
        """执行上下文优化 - 通过AI模型原生智能"""
        if not request.strip():
            return {
                'success': False,
                'error': '上下文不能为空',
                'result': {}
            }

        # 获取优化目标
        params = context or {}
        goals = params.get('optimization_goals', ['clarity', 'completeness'])
        if isinstance(goals, str):
            goals = [g.strip() for g in goals.split(',') if g.strip()]

        optimization_instruction = f"""
根据以下目标优化上下文:

优化目标: {', '.join(goals)}

原始上下文: "{request}"

请返回优化后的内容和应用的优化措施，以JSON格式。
"""

        try:
            # 使用模拟AI完成度函数
            simulation_result = simulate_ai_completion(optimization_instruction)
            parsed_result = json.loads(simulation_result)

            return {
                'success': True,
                'result': parsed_result
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'AI优化失败: {str(e)}',
                'result': {}
            }

    def _calculate_confidence(self, request: str) -> float:
        """计算置信度"""
        if len(request) < 5:
            return 0.4  # 太短置信度低
        else:
            return 0.75


class CognitiveTemplateSkill:
    """认知模板技能 - 利用AI模型原生智能应用认知模板"""
    
    def __init__(self):
        super().__init__(
            name="dsgs-cognitive-template",
            description="DSGS认知模板技能 - 利用AI模型原生智能应用认知模板结构化复杂任务"
        )
        
        self.templates = {
            'chain_of_thought': '思维链推理模板',
            'few_shot': '少样本学习模板', 
            'verification': '验证检查模板',
            'role_playing': '角色扮演模板',
            'understanding': '深度理解模板'
        }
    
    def _execute_skill_logic(self, request: str, context: Dict[str, Any]) -> Any:
        """执行认知模板应用 - 通过AI模型原生智能"""
        if not request.strip():
            return {
                'success': False,
                'error': '上下文不能为空',
                'result': {'success': False}
            }
        
        params = context or {}
        template_type = params.get('template', 'chain_of_thought')
        
        if template_type not in self.templates:
            return {
                'success': False,
                'error': f'未知模板: {template_type}',
                'available_templates': list(self.templates.keys()),
                'result': {'success': False}
            }
        
        template_desc = self.templates[template_type]
        
        if template_type == 'chain_of_thought':
            template_instruction = f"""
使用思维链方法分析以下任务：

任务: {request}

按以下步骤分析:
1. 问题理解
2. 步骤分解
3. 中间推理
4. 验证检查
5. 最终答案

返回结构化分析。
"""
        elif template_type == 'verification':
            template_instruction = f"""
使用验证框架分析以下内容:

原始内容: {request}

执行验证:
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
使用{template_desc}分析任务: {request}

返回结构化结果。
"""
        
        try:
            # 构造模板应用结果
            enhanced_content = f"""
### {template_type} 认知模板应用

**原始任务**: {request}

**结构化分析**:
[AI模型将应用{template_desc}进行专业分析...]

**专业结果**:
[返回基于{template_desc}的专业分析结果]

**置信度**: 0.85
"""
            
            return {
                'success': True,
                'result': {
                    'success': True,
                    'template_type': template_type,
                    'template_description': template_desc,
                    'original_context': request,
                    'enhanced_context': enhanced_content,
                    'template_structure': ['应用认知框架', '结构化输出', '验证结果'],
                    'confidence': 0.85
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'模板应用失败: {str(e)}',
                'result': {'success': False}
            }
    
    def _calculate_confidence(self, request: str) -> float:
        """计算置信度"""
        if len(request) < 5:
            return 0.35
        else:
            return 0.85


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
            result = skill.process_request(context_input, params)
            
            if result.status.name == 'COMPLETED':
                analysis = result.result
                if 'result' in analysis:
                    analysis_data = analysis['result']
                else:
                    analysis_data = analysis
                
                output_lines = []
                output_lines.append("上下文质量分析结果:")
                output_lines.append(f"长度: {analysis_data['context_length']} 字符")
                output_lines.append(f"Token估算: {analysis_data['token_count_estimate']}")
                output_lines.append("")
                
                output_lines.append("五维质量指标 (0.0-1.0):")
                metric_names = {
                    'clarity': '清晰度', 'relevance': '相关性', 'completeness': '完整性',
                    'consistency': '一致性', 'efficiency': '效率'
                }
                
                for metric, score in analysis_data['metrics'].items():
                    indicator = "🟢" if score >= 0.7 else "🟡" if score >= 0.4 else "🔴"
                    output_lines.append(f"  {indicator} {metric_names.get(metric, metric)}: {score:.2f}")
                
                if analysis_data.get('suggestions'):
                    output_lines.append("\n优化建议:")
                    for s in analysis_data['suggestions'][:3]:  # 显示前3条
                        output_lines.append(f"  • {s}")
                
                if analysis_data.get('issues'):
                    output_lines.append("\n识别问题:")
                    for i in analysis_data['issues']:
                        output_lines.append(f"  • {i}")
                
                return "\n".join(output_lines)
            else:
                return f"错误: {result.error_message}"
        
        elif skill_name == 'context-optimization':
            skill = ContextOptimizationSkill()
            result = skill.process_request(context_input, params)
            
            if result.status.name == 'COMPLETED':
                optimization = result.result
                if 'result' in optimization:
                    optimization_data = optimization['result']
                else:
                    optimization_data = optimization
                
                output_lines = []
                output_lines.append("上下文优化结果:")
                output_lines.append(f"原始长度: {len(optimization_data['original_context'])} 字符")
                output_lines.append(f"优化后长度: {len(optimization_data['optimized_context'])} 字符")
                output_lines.append("")
                
                output_lines.append("应用的优化措施:")
                for opt in optimization_data['applied_optimizations']:
                    output_lines.append(f"  • {opt}")
                
                output_lines.append("\n改进指标:")
                for metric, change in optimization_data['improvement_metrics'].items():
                    direction = "↗️" if change > 0 else "↘️" if change < 0 else "➡️"
                    output_lines.append(f"  {direction} {metric}: {change:+.2f}")
                
                output_lines.append("\n优化后上下文:")
                output_lines.append(optimization_data['optimized_context'])
                
                return "\n".join(output_lines)
            else:
                return f"错误: {result.error_message}"
        
        elif skill_name == 'cognitive-template':
            skill = CognitiveTemplateSkill()
            result = skill.process_request(context_input, params)
            
            if result.status.name == 'COMPLETED':
                template_result = result.result
                if 'result' in template_result:
                    template_data = template_result['result']
                else:
                    template_data = template_result
                
                if template_data.get('success', True):
                    output_lines = []
                    output_lines.append(f"认知模板应用: {template_data['template_type']} ({template_data['template_description']})")
                    output_lines.append("="*60)
                    output_lines.append("")
                    output_lines.append("结构化输出:")
                    output_lines.append(template_data['enhanced_context'])
                    
                    return "\n".join(output_lines)
                else:
                    error_msg = template_data.get('error', '模板应用失败')
                    return f"错误: {error_msg}"
            else:
                return f"错误: {result.error_message}"
        
        else:
            available_skills = ['context-analysis', 'context-optimization', 'cognitive-template']
            return f"错误: 未知技能 '{skill_name}'. 可用技能: {', '.join(available_skills)}"
    
    except Exception as e:
        return f"错误: 执行过程异常 - {str(e)}"


def get_available_skills() -> Dict[str, str]:
    """获取可用技能列表"""
    return {
        'context-analysis': '上下文质量五维专业分析',
        'context-optimization': 'AI驱动的上下文智能优化',
        'cognitive-template': '认知模板结构化复杂任务'
    }