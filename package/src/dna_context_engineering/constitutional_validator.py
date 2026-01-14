"""
constitution_validator.py
宪法验证技能 - 符合Claude Skills规范
"""
from typing import Dict, Any, List, Optional
import json
import re
from datetime import datetime

def execute(args: Dict[str, Any]) -> str:
    """
    Claude Skills标准执行入口
    """
    content = args.get("content", "") or args.get("context", "")
    principle = args.get("principle", "all")
    detailed = args.get("detailed", False)
    
    if not content.strip():
        return "❌ 错误: 未提供要验证的内容"
    
    # 执行宪法验证
    validation_result = perform_constitutional_validation(content, principle)
    
    # 格式化输出
    return format_validation_output(validation_result, detailed)


def perform_constitutional_validation(content: str, principle: str = "all") -> Dict[str, Any]:
    """
    执行宪法验证 - 定量分析部分
    """
    validation_results = {}
    
    if principle == "all" or principle == "progressive_disclosure":
        validation_results["progressive_disclosure"] = validate_progressive_disclosure(content)
    
    if principle == "all" or principle == "cognitive_convenience":
        validation_results["cognitive_convenience"] = validate_cognitive_convenience(content)
    
    if principle == "all" or principle == "information_encapsulation":
        validation_results["information_encapsulation"] = validate_information_encapsulation(content)
    
    if principle == "all" or principle == "cognitive_gestalt":
        validation_results["cognitive_gestalt"] = validate_cognitive_gestalt(content)
    
    overall_compliant = all(result["compliant"] for result in validation_results.values())
    
    return {
        "content_length": len(content),
        "validation_results": validation_results,
        "overall_compliant": overall_compliant,
        "non_compliant_principles": [
            principle for principle, result in validation_results.items() 
            if not result["compliant"]
        ],
        "principle_count": len(validation_results)
    }


def validate_progressive_disclosure(content: str) -> Dict[str, Any]:
    """验证渐进披露原则"""
    # 定量分析：检查内容层次结构
    headers = len(re.findall(r'^#+\s+.+$', content, re.MULTILINE))
    sub_headers = len(re.findall(r'^##+\s+.+$', content, re.MULTILINE))
    has_structure = headers >= 1
    has_hierarchy = sub_headers >= 1
    
    compliant = has_structure and has_hierarchy
    confidence = min(1.0, (headers * 0.3 + sub_headers * 0.4) if headers > 0 else 0)
    
    return {
        "compliant": compliant,
        "confidence": round(confidence, 2),
        "feedback": f"渐进披露: {headers}个标题, {sub_headers}个子标题" if compliant else "缺少层次结构"
    }


def validate_cognitive_convenience(content: str) -> Dict[str, Any]:
    """验证认知便利原则"""
    # 定量分析：检查结构清晰度
    structure_elements = [
        bool(re.search(r'^(#|\d+\.)\s+', content, re.MULTILINE)),
        bool(re.search(r'^\s*[-*]\s+', content, re.MULTILINE)),
        '.' in content or '。' in content,
        '\n\n' in content
    ]
    structure_score = sum(structure_elements)
    
    min_content_ok = len(content.strip()) > 15
    has_separation = '\n' in content
    
    compliant = structure_score >= 2 and min_content_ok and has_separation
    confidence = min(1.0, (structure_score * 0.3 + (1 if min_content_ok else 0) * 0.4 + (1 if has_separation else 0) * 0.3))
    
    return {
        "compliant": compliant,
        "confidence": round(confidence, 2),
        "feedback": f"认知便利: {structure_score}个结构元素，长度{len(content)}字符" if compliant else "结构不清晰或内容过短"
    }


def validate_information_encapsulation(content: str) -> Dict[str, Any]:
    """验证信息封装原则"""
    # 定量分析：检查自包含性
    context_indicators = any(
        keyword in content.lower() for keyword in 
        ['context', 'overview', 'description', 'purpose', 'function', 'role', '目标', '功能', '概述', '说明']
    )
    has_min_content = len(content.strip()) >= 20
    has_complete_sentences = ('.' in content or '。' in content) and len(content) >= 15
    
    compliant = has_context_indicators and has_min_content and has_complete_sentences
    confidence = min(1.0, (0.4 if has_context_indicators else 0) + (0.3 if has_min_content else 0) + (0.3 if has_complete_sentences else 0))
    
    return {
        "compliant": compliant,
        "confidence": round(confidence, 2),
        "feedback": "信息封装: 内容自包含" if compliant else "内容不够自包含"
    }


def validate_cognitive_gestalt(content: str) -> Dict[str, Any]:
    """验证认知格式塔原则"""
    # 定量分析：检查整体性
    has_content = len(content.strip()) > 0
    has_structure = bool(re.search(r'^(#|\d+\.|[•\-•○▪])', content, re.MULTILINE))
    has_min_completeness = len(content) >= 15
    has_multiline = len([line for line in content.split('\n') if line.strip()]) >= 2
    has_coherence = ('.' in content or '。' in content and len(content) > 10) or has_structure
    
    compliant = all([has_content, has_structure, has_min_completeness, has_multiline, has_coherence])
    confidence = min(1.0, sum([
        0.2 if has_content else 0,
        0.2 if has_structure else 0,
        0.2 if has_min_completeness else 0,
        0.2 if has_multiline else 0,
        0.2 if has_coherence else 0
    ]))
    
    return {
        "compliant": compliant,
        "confidence": round(confidence, 2),
        "feedback": "认知格式塔: 形成完整认知单元" if compliant else "内容缺乏完整性"
    }


def format_validation_output(validation_result: Dict[str, Any], detailed: bool) -> str:
    """格式化验证输出"""
    lines = []
    lines.append(f"📋 宪法验证结果")
    lines.append(f"长度: {validation_result['content_length']} 字符")
    lines.append(f"合规: {'✅' if validation_result['overall_compliant'] else '❌'}")
    lines.append(f"原则: {validation_result['principle_count']} 项")
    
    if validation_result['non_compliant_principles']:
        lines.append(f"违规: {', '.join(validation_result['non_compliant_principles'])}")
    
    lines.append("")  # 空行
    
    if detailed:
        lines.append("🔍 验证详情:")
        for principle, result in validation_result['validation_results'].items():
            indicator = "🟢" if result['compliant'] else "🔴"
            confidence_indicator = "🟢" if result['confidence'] >= 0.7 else "🟡" if result['confidence'] >= 0.4 else "🔴"
            lines.append(f"  {indicator} {principle}: {result['feedback']}")
            lines.append(f"      置信度: {confidence_indicator} {result['confidence']:.2f}")
    else:
        lines.append("💡 使用 detailed=true 参数查看详细验证结果")
    
    return "\n".join(lines)


def get_manifest() -> Dict[str, Any]:
    """
    Claude Skills标准技能清单
    """
    return {
        "name": "dnaspec-constitutional-validator",
        "description": "使用宪法原则验证内容质量的技能，确保AI生成内容符合认知优化原则",
        "version": "1.0.0",
        "created_at": datetime.now().isoformat(),
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "要验证的内容"
                },
                "context": {
                    "type": "string",
                    "description": "要验证的内容（content的别名）"
                },
                "principle": {
                    "type": "string",
                    "description": "要验证的宪法原则",
                    "enum": ["all", "progressive_disclosure", "cognitive_convenience", 
                            "information_encapsulation", "cognitive_gestalt"],
                    "default": "all"
                },
                "detailed": {
                    "type": "boolean",
                    "description": "是否返回详细验证结果",
                    "default": False
                }
            },
            "required": ["content"]
        }
    }