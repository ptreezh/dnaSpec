"""
上下文分析技能 - 独立执行版本
支持跨CLI工具部署的独立执行函数
"""
from typing import Dict, Any, List
import re


def execute_context_analysis(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    独立执行的上下文分析技能函数
    支持跨CLI工具调用
    
    Args:
        args: 包含以下字段的字典
            - input: 待分析的上下文内容
            - detail_level: 详细程度 ("basic", "standard", "detailed")
            - options: 可选配置参数
            - context: 上下文信息
            
    Returns:
        标准化输出响应
    """
    try:
        # 解析输入参数
        input_text = args.get("input", "")
        detail_level_str = args.get("detail_level", "standard")
        options = args.get("options", {})
        context = args.get("context", {})
        
        # 验证输入
        if not input_text or not isinstance(input_text, str):
            return {
                "status": "error",
                "error": {
                    "type": "VALIDATION_ERROR",
                    "message": "Input must be a non-empty string",
                    "code": "INVALID_INPUT"
                }
            }
        
        # 处理详细程度参数
        detail_level = "standard"
        if detail_level_str in ["basic", "standard", "detailed"]:
            detail_level = detail_level_str
        
        # 执行上下文分析逻辑
        result_data = _execute_context_analysis(input_text, options, context)
        
        # 根据详细程度格式化输出
        formatted_result = _format_output(result_data, detail_level)
        
        return {
            "status": "success",
            "data": formatted_result,
            "metadata": {
                "skill_name": "context-analysis",
                "detail_level": detail_level
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": {
                "type": type(e).__name__,
                "message": str(e),
                "code": "EXECUTION_ERROR"
            }
        }


def _execute_context_analysis(input_text: str, options: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """执行上下文分析逻辑"""
    
    def _analyze_clarity(context: str) -> float:
        """分析清晰度"""
        clear_indicators = ['请', '需要', '要求', '目标', '任务', '实现', '设计', '分析', '如何', '怎样', '明确']
        unclear_indicators = ['也许', '可能', '大概', '似乎', '某些', '一些', '部分', '等等']
        
        clear_count = sum(1 for indicator in clear_indicators if indicator in context)
        unclear_count = sum(1 for indicator in unclear_indicators if indicator in context)
        
        # 基于句子和明确指令词计算清晰度
        sentences = re.split(r'[。！？.!?;；]', context)
        sentence_count = len([s for s in sentences if s.strip() and len(s.strip()) > 3])
        
        clarity_score = min(1.0, (clear_count * 0.3 + sentence_count * 0.05) if sentence_count > 0 else 0)
        unclear_penalty = min(0.5, unclear_count * 0.2)
        
        return max(0.0, clarity_score - unclear_penalty)
    
    def _analyze_relevance(context: str) -> float:
        """分析相关性"""
        task_indicators = ['系统', '功能', '任务', '目标', '需求', '实现', '开发', '设计', '分析', '管理', '处理', '支持']
        
        task_count = sum(1 for indicator in task_indicators if indicator in context)
        relevance_score = min(1.0, task_count * 0.15)
        
        return max(0.0, relevance_score)
    
    def _analyze_completeness(context: str) -> float:
        """分析完整性"""
        completeness_indicators = ['约束', '条件', '要求', '标准', '规范', '限制', '假设', '前提', '约束', '目标', '验收']
        
        completeness_count = sum(1 for indicator in completeness_indicators if indicator in context)
        completeness_score = min(1.0, completeness_count * 0.15)
        
        return max(0.0, completeness_score)
    
    def _analyze_consistency(context: str) -> float:
        """分析一致性"""
        # 检查逻辑矛盾
        contradiction_pairs = [
            ('必须', '可选'),
            ('应该', '不必'),
            ('总是', '从不'),
            ('全部', '部分'),
            ('强制', '随意'),
            ('要求', '可选'),
            ('必须', '可以')
        ]
        
        contradiction_count = 0
        for positive, negative in contradiction_pairs:
            if positive in context and negative in context:
                contradiction_count += 1
        
        # 一致性越高分数越高，矛盾越多分数越低
        consistency_score = max(0.0, 1.0 - (contradiction_count * 0.2))
        
        return consistency_score
    
    def _analyze_efficiency(context: str) -> float:
        """分析效率（信息密度）"""
        if len(context) == 0:
            return 0.0
        
        # 计算信息密度：有效词汇数 / 总字符数
        words = [w for w in re.findall(r'[\w\u4e00-\u9fff]+', context) if len(w) > 1]
        efficiency = len(words) / len(context) * 100
        
        # 归一化到0-1范围（假设每100字符理想有25个有效词为满分）
        normalized_efficiency = min(1.0, efficiency / 25)
        
        return max(0.0, normalized_efficiency)
    
    # 执行上下文分析
    clarity = _analyze_clarity(input_text)
    relevance = _analyze_relevance(input_text)
    completeness = _analyze_completeness(input_text)
    consistency = _analyze_consistency(input_text)
    efficiency = _analyze_efficiency(input_text)
    
    overall_score = (clarity + relevance + completeness + consistency + efficiency) / 5
    
    # 生成建议
    suggestions = []
    if clarity < 0.7:
        suggestions.append("增加更明确的术语和目标表述")
    if completeness < 0.6:
        suggestions.append("补充约束条件和具体要求")
    if relevance < 0.7:
        suggestions.append("明确目标和任务关联性")
    
    # 识别问题
    issues = []
    if "也许" in input_text or "可能" in input_text or "大概" in input_text:
        issues.append("包含不确定词汇：'也许'、'可能'、'大概'")
    if len(input_text) < 20:
        issues.append("上下文过短，信息不足")
    if "但是" in input_text and "因此" not in input_text:
        issues.append("包含转折但缺少结论逻辑")
    
    return {
        "context_length": len(input_text),
        "overall_score": round(overall_score, 2),
        "metrics": {
            "clarity": round(clarity, 2),
            "relevance": round(relevance, 2),
            "completeness": round(completeness, 2),
            "consistency": round(consistency, 2),
            "efficiency": round(efficiency, 2)
        },
        "issues": issues,
        "suggestions": suggestions
    }


def _format_output(result_data: Dict[str, Any], detail_level: str) -> Dict[str, Any]:
    """根据详细程度格式化输出结果"""
    if detail_level == "basic":
        # 基础级别只返回核心信息
        return {
            "overall_score": result_data["overall_score"],
            "main_issues": result_data["issues"][:3]  # 只返回前3个主要问题
        }
    elif detail_level == "standard":
        # 标准级别返回标准信息
        return {
            "overall_score": result_data["overall_score"],
            "metrics": result_data["metrics"],
            "issues": result_data["issues"],
            "suggestions": result_data["suggestions"][:5]  # 只返回前5个建议
        }
    else:  # detailed
        # 详细级别返回完整信息
        detailed_analysis = {
            "context_length": result_data["context_length"],
            "metrics_breakdown": {
                "clarity": {
                    "score": result_data["metrics"]["clarity"],
                    "analysis": "清晰度基于明确指令词和句子结构计算"
                },
                "relevance": {
                    "score": result_data["metrics"]["relevance"],
                    "analysis": "相关性基于任务相关词汇计算"
                },
                "completeness": {
                    "score": result_data["metrics"]["completeness"],
                    "analysis": "完整性基于约束条件和要求词汇计算"
                },
                "consistency": {
                    "score": result_data["metrics"]["consistency"],
                    "analysis": "一致性基于逻辑矛盾检测计算"
                },
                "efficiency": {
                    "score": result_data["metrics"]["efficiency"],
                    "analysis": "效率基于信息密度计算"
                }
            }
        }
        
        return {
            "overall_score": result_data["overall_score"],
            "metrics": result_data["metrics"],
            "issues": result_data["issues"],
            "suggestions": result_data["suggestions"],
            "detailed_analysis": detailed_analysis
        }


# 为CLI工具提供命令行接口
def main():
    """命令行接口"""
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python context_analysis_independent.py '<context>' [detail_level]")
        sys.exit(1)
    
    context = sys.argv[1]
    detail_level = sys.argv[2] if len(sys.argv) > 2 else "standard"
    
    args = {
        "input": context,
        "detail_level": detail_level,
        "options": {},
        "context": {}
    }
    
    result = execute_context_analysis(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()