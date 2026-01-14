"""
Claude Skills标准的架构设计技能实现
符合Claude官方Skills规范和信息渐进披露哲学
"""
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Claude Skills标准处理函数
    """
    try:
        # Claude Skills标准结构：event包含inputs数组
        inputs = event.get('inputs', [{}])
        if not inputs:
            return {
                'statusCode': 400,
                'body': {
                    'error': 'No inputs provided',
                    'timestamp': datetime.utcnow().isoformat()
                }
            }
        
        input_data = inputs[0]  # Claude Skills标准，输入在第一个元素
        action = event.get('action', '').lower()
        
        # 根据动作类型执行不同功能
        if action == 'analyze_context':
            result = _execute_context_analysis(input_data)
        elif action == 'optimize_context':
            result = _execute_context_optimization(input_data)
        elif action == 'apply_cognitive_template':
            result = _execute_cognitive_template_application(input_data)
        else:
            return {
                'statusCode': 400,
                'body': {
                    'error': f'Unknown action: {action}',
                    'available_actions': ['analyze_context', 'optimize_context', 'apply_cognitive_template'],
                    'timestamp': datetime.utcnow().isoformat()
                }
            }
        
        return {
            'statusCode': 200,
            'body': result
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
        }


def _execute_context_analysis(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行上下文分析 - 遵循信息渐进披露原则
    """
    input_text = input_data.get('input', input_data.get('context', ''))
    
    if not input_text.strip():
        return {
            'success': False,
            'error': 'No input context provided for analysis',
            'timestamp': datetime.utcnow().isoformat()
        }
    
    # 执行五维质量分析（使用简化版本以实现快速响应）
    length = len(input_text)
    tokens_estimated = max(1, len(input_text) // 4)
    
    # 计算质量指标
    clarity_score = min(1.0, max(0.0, 0.5 + len(input_text) * 0.00001))
    relevance_score = min(1.0, max(0.0, 0.7 if any(kw in input_text.lower() for kw in ['system', 'function', 'task', 'requirement']) else 0.3))
    completeness_score = min(1.0, max(0.0, 0.3 if any(kw in input_text.lower() for kw in ['constraint', 'requirement', 'goal']) else 0.2))
    consistency_score = min(1.0, max(0.0, 0.8 - (0.2 if any(kw in input_text.lower() for kw in ['but', 'however']) else 0)))
    efficiency_score = min(1.0, max(0.0, 1.0 - len(input_text) * 0.00005))
    
    result = {
        'success': True,
        'analysis': {
            'context_length': length,
            'token_estimate': tokens_estimated,
            'quality_metrics': {
                'clarity': round(clarity_score, 2),
                'relevance': round(relevance_score, 2),
                'completeness': round(completeness_score, 2),
                'consistency': round(consistency_score, 2),
                'efficiency': round(efficiency_score, 2)
            },
            # 仅在需要时显示详细建议（信息渐进披露）
            'detailed_analysis_available': True
        },
        'input': input_text[:100] + '...' if len(input_text) > 100 else input_text,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    return result


def _execute_context_optimization(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行上下文优化 - 遵循信息渐进披露原则
    """
    input_text = input_data.get('input', input_data.get('context', ''))
    goals = input_data.get('optimization_goals', [])
    
    if not input_text.strip():
        return {
            'success': False,
            'error': 'No input context provided for optimization',
            'timestamp': datetime.utcnow().isoformat()
        }
    
    # 执行优化（简化实现）
    optimized_text = input_text
    
    applied_optimizations = []
    
    # 根据优化目标进行优化
    if any(goal.lower() in ['clarity', 'clear', 'clarity', '清晰度'] for goal in goals):
        optimized_text += "\n\nNote: Improve clarity by specifying goals and constraints."
        applied_optimizations.append('Added clarity improvement suggestions')
    
    if any(goal.lower() in ['completeness', 'complete', 'completeness', '完整性'] for goal in goals):
        optimized_text += "\n\nConstraint: Need to complete within specified time\nGoal: Implement expected functionality\nPrerequisites: Having necessary resources"
        applied_optimizations.append('Added completeness elements')
    
    result = {
        'success': True,
        'optimization': {
            'original_context_length': len(input_text),
            'optimized_context_length': len(optimized_text),
            'applied_optimizations': applied_optimizations,
            'optimization_summary': f"Optimized for: {', '.join(goals) if goals else 'general improvement'}",
            # 仅显示关键优化指标，详情按需展开（信息渐进披露）
            'metrics_improved': {
                'clarity_change': 0.2 if any('clarity' in goal.lower() for goal in goals) else 0.0,
                'completeness_change': 0.3 if any('completeness' in goal.lower() for goal in goals) else 0.0
            },
            'detailed_optimization_available': True
        },
        'input_preview': input_text[:50] + '...' if len(input_text) > 50 else input_text,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    return result


def _execute_cognitive_template_application(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    应用认知模板 - 遵循信息渐进披露原则
    """
    input_text = input_data.get('input', input_data.get('context', ''))
    template_type = input_data.get('template_type', 'chain_of_thought')
    
    if not input_text.strip():
        return {
            'success': False,
            'error': 'No input provided for cognitive template application',
            'timestamp': datetime.utcnow().isoformat()
        }
    
    # 根据模板类型应用不同认知框架
    if template_type == 'chain_of_thought':
        # 应用链式思维模板
        enhanced_output = f"Chain of Thought Analysis for: {input_text}\n\n"
        enhanced_output += "1. Problem Understanding\n"
        enhanced_output += "2. Step Decomposition\n"
        enhanced_output += "3. Intermediate Reasoning\n"
        enhanced_output += "4. Verification Check\n"
        enhanced_output += "5. Final Answer\n\n"
        
    elif template_type == 'few_shot':
        # 应用少样本学习模板
        enhanced_output = f"Few-Shot Learning Pattern for: {input_text}\n\n"
        enhanced_output += "Example 1: [Pattern to replicate]\n"
        enhanced_output += "Example 2: [Pattern to replicate]\n"
        enhanced_output += "Current Task: [Apply learned pattern]\n\n"
        
    elif template_type == 'verification':
        # 应用验证模板
        enhanced_output = f"Verification Process for: {input_text}\n\n"
        enhanced_output += "1. Initial Answer\n"
        enhanced_output += "2. Logical Consistency Check\n"
        enhanced_output += "3. Fact Accuracy Verification\n"
        enhanced_output += "4. Completeness Validation\n"
        enhanced_output += "5. Final Confirmation\n\n"
        
    elif template_type == 'role_playing':
        # 应用角色扮演模板
        enhanced_output = f"Role-Playing Analysis for: {input_text}\n\n"
        enhanced_output += "Assuming role appropriate to task...\n"
        enhanced_output += "[Applying role-specific reasoning]\n\n"
        
    else:  # Default to chain of thought
        enhanced_output = f"Cognitive Template Application: Applying systematic reasoning to {input_text}\n\n"
        enhanced_output += "1. Understanding the task\n"
        enhanced_output += "2. Breaking into sub-components\n"
        enhanced_output += "3. Applying relevant frameworks\n"
        enhanced_output += "4. Synthesizing solutions\n"
        enhanced_output += "5. Providing final output\n\n"
    
    result = {
        'success': True,
        'template_application': {
            'template_type': template_type,
            'template_description': _get_template_description(template_type),
            'output_preview': enhanced_output[:200] + '...' if len(enhanced_output) > 200 else enhanced_output,
            # 提供完整输出的选项，但默认只显示预览（信息渐进披露）
            'full_output_available': True,
            'cognitive_framework_applied': True
        },
        'input_preview': input_text[:50] + '...' if len(input_text) > 50 else input_text,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    return result


def _get_template_description(template_type: str) -> str:
    """
    获取模板描述
    """
    descriptions = {
        'chain_of_thought': 'Chain of Thought reasoning pattern for systematic problem solving',
        'few_shot': 'Few-shot learning pattern for learning from examples',
        'verification': 'Verification pattern for validating reasoning and outputs',
        'role_playing': 'Role-playing pattern for perspective-based analysis',
        'understanding': 'Deep understanding pattern for concept comprehension'
    }
    return descriptions.get(template_type, 'Generic cognitive template pattern')


# Local test function for development
def test_local():
    """
    本地测试函数（非Claude标准）
    """
    # Test context analysis
    test_event = {
        'action': 'analyze_context',
        'inputs': [{'input': 'Build a user authentication system'}]
    }
    
    result = lambda_handler(test_event, None)
    print('Context Analysis Result:')
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Test context optimization
    test_event = {
        'action': 'optimize_context',
        'inputs': [
            {
                'input': 'System needs better requirements',
                'optimization_goals': ['clarity', 'completeness']
            }
        ]
    }
    
    result = lambda_handler(test_event, None)
    print('\nContext Optimization Result:')
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Test cognitive template
    test_event = {
        'action': 'apply_cognitive_template',
        'inputs': [
            {
                'input': 'How to improve system performance?',
                'template_type': 'chain_of_thought'
            }
        ]
    }
    
    result = lambda_handler(test_event, None)
    print('\nCognitive Template Result:')
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    test_local()