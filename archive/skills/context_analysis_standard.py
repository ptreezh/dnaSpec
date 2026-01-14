"""
DNASPEC 上下文分析技能 - 符合Claude Skills标准规范
"""
from typing import Dict, Any, Union
import re
from datetime import datetime

class ClaudeContextAnalysisSkill:
    """
    Claude Skills标准上下文分析技能
    遵循渐进披露、最小认知负荷、工具化思维、定性定量结合原则
    """
    
    def __init__(self):
        self.name = "dnaspec-context-analysis"
        self.description = "使用宪法原则分析上下文质量的技能，提供五维质量评估"
        self.version = "1.0.0"
        self.created_at = datetime.now().isoformat()
    
    def execute(self, args: Dict[str, Any]) -> str:
        """Claude Skills标准执行入口"""
        context = args.get("context", "") or args.get("request", "") or args.get("input", "")
        
        if not context.strip():
            return "❌ 未提供要分析的上下文，请提供context参数"
        
        # 执行定量分析（程序化）
        analysis_data = self._perform_quantitative_analysis(context)
        
        # 应用AI定性解释和决策（AI原生能力）
        qualitative_insights = self._get_qualitative_insights(analysis_data, context)
        
        # 格式化输出（渐进披露）
        return self._format_progressive_output(analysis_data, qualitative_insights, args)
    
    def _perform_quantitative_analysis(self, context: str) -> Dict[str, Any]:
        """执行定量分析 - 程序化逻辑"""
        # 定量指标计算
        context_length = len(context)
        token_estimate = max(1, len(context) // 4)
        
        # 清晰度评估
        has_goals = bool(re.search(r'(目标|目的|goal|objective|需要|requirement|需求)', context, re.IGNORECASE))
        has_requirements = bool(re.search(r'(要求|条件|constraint|requirement|constraint|限制|约束)', context, re.IGNORECASE))
        has_structure = bool(re.search(r'(#|\d+\.|[•\-•○▪])', context, re.MULTILINE))
        
        clarity_score = min(1.0, 0.3 + (0.3 if has_goals else 0) + (0.2 if has_requirements else 0) + (0.2 if has_structure else 0))
        
        # 相关性评估
        task_indicators = ['系统', '功能', '任务', '目标', '实现', '开发', '设计', '分析', '管理', '处理', '支持']
        relevant_indicators = sum(1 for indicator in task_indicators if indicator in context)
        relevance_score = min(1.0, (relevant_indicators * 0.15) if relevant_indicators > 0 else 0.1)
        
        # 完整性评估
        completeness_indicators = ['约束', '条件', '要求', '标准', '规范', '限制', '假设', '前提', '目标', '验收']
        completeness_count = sum(1 for indicator in completeness_indicators if indicator in context)
        completeness_score = min(1.0, (completeness_count * 0.15) if completeness_count > 0 else 0.2)
        
        # 一致性评估（检查矛盾词汇）
        contradiction_pairs = [
            ('必须', '可选'), ('应该', '不必'), ('总是', '从不'), ('全部', '部分'),
            ('强制', '随意'), ('要求', '可选'), ('必须', '可以')
        ]
        contradiction_count = sum(1 for pos, neg in contradiction_pairs if pos in context and neg in context)
        consistency_score = max(0.0, min(1.0, 0.9 - (contradiction_count * 0.2)))
        
        # 效率评估（信息密度）
        words = [w for w in re.findall(r'[\w\u4e00-\u9fff]+', context) if len(w) > 1]
        word_count = len(words)
        efficiency_score = min(1.0, word_count / (len(context) / 5 + 1) if context else 0)
        
        # 生成建议（定量）
        suggestions = []
        if not has_goals:
            suggestions.append("增加更明确的目标描述")
        if not has_requirements:
            suggestions.append("补充具体的约束条件和要求")
        if contradiction_count > 0:
            suggestions.append(f"解决检测到的{contradiction_count}个逻辑矛盾")
        
        # 识别问题（定量）
        issues = []
        if contradiction_count > 0:
            issues.append(f"发现{contradiction_count}个逻辑矛盾")
        if len(context) < 20:
            issues.append("上下文过短，信息不足")
        if not has_structure:
            issues.append("缺乏清晰的结构")
        
        return {
            'context_length': context_length,
            'token_count_estimate': token_count,
            'metrics': {
                'clarity': round(clarity_score, 2),
                'relevance': round(relevance_score, 2),
                'completeness': round(completeness_score, 2),
                'consistency': round(consistency_score, 2),
                'efficiency': round(efficiency_score, 2)
            },
            'suggestions': suggestions,
            'issues': issues,
            'indicators': {
                'has_goals': has_goals,
                'has_requirements': has_requirements,
                'has_structure': has_structure,
                'contradiction_count': contradiction_count
            }
        }
    
    def _get_qualitative_insights(self, analysis_data: Dict[str, Any], original_context: str) -> Dict[str, Any]:
        """获取定性见解 - 利用AI模型原生智能"""
        # 这里是示意，实际在Claude CLI环境中，AI模型会直接处理提示词
        # 但在当前实现中，我们会基于定量分析提供智能解释
        
        insights = {
            'interpretation': self._interpret_metrics(analysis_data['metrics']),
            'recommendations': self._generate_recommendations(analysis_data),
            'confidence_levels': self._assess_confidence(analysis_data),
            'critical_issues': self._identify_critical_issues(analysis_data)
        }
        
        return insights
    
    def _interpret_metrics(self, metrics: Dict[str, float]) -> str:
        """解释质量指标"""
        interpretation = []
        
        for metric, score in metrics.items():
            metric_names = {
                'clarity': '清晰度',
                'relevance': '相关性', 
                'completeness': '完整性',
                'consistency': '一致性',
                'efficiency': '效率'
            }
            name = metric_names.get(metric, metric)
            
            if score >= 0.8:
                interpretation.append(f"{name}优秀(≥0.8)")
            elif score >= 0.6:
                interpretation.append(f"{name}良好(0.6-0.79)")
            elif score >= 0.4:
                interpretation.append(f"{name}一般(0.4-0.59)")
            else:
                interpretation.append(f"{name}较差(<0.4)")
        
        return "; ".join(interpretation)
    
    def _generate_recommendations(self, analysis_data: Dict[str, Any]) -> list:
        """生成改进建议"""
        recommendations = []
        metrics = analysis_data['metrics']
        
        if metrics['clarity'] < 0.6:
            recommendations.append("使用更明确的目标和术语")
        if metrics['relevance'] < 0.7:
            recommendations.append("明确任务相关性")
        if metrics['completeness'] < 0.6:
            recommendations.append("补充约束条件和具体要求")
        if metrics['consistency'] < 0.8:
            recommendations.append("检查并解决逻辑矛盾")
        
        return recommendations
    
    def _assess_confidence(self, analysis_data: Dict[str, Any]) -> Dict[str, str]:
        """评估分析置信度"""
        confidences = {}
        metrics = analysis_data['metrics']
        
        for metric, score in metrics.items():
            if score >= 0.8:
                confidences[metric] = "高置信度"
            elif score >= 0.6:
                confidences[metric] = "中等置信度"
            else:
                confidences[metric] = "低置信度"
        
        return confidences
    
    def _identify_critical_issues(self, analysis_data: Dict[str, Any]) -> list:
        """识别关键问题"""
        critical_issues = []
        
        if analysis_data['metrics']['consistency'] < 0.5:
            critical_issues.append("严重一致性问题")
        if analysis_data['context_length'] < 15:
            critical_issues.append("内容过短")
        if analysis_data['indicators']['contradiction_count'] > 2:
            critical_issues.append("多重逻辑矛盾")
        
        return critical_issues if critical_issues else ["无关键问题"]
    
    def _format_progressive_output(self, analysis_data: Dict[str, Any], insights: Dict[str, Any], args: Dict[str, Any]) -> str:
        """格式化渐进披露输出 - 符合Claude Skills规范"""
        detailed = args.get("detailed", False)
        
        output_lines = []
        
        # 基本信息（最低认知负荷）
        output_lines.append("📋 上下文质量分析结果")
        output_lines.append(f"长度: {analysis_data['context_length']} 字符")
        output_lines.append(f"Token估算: {analysis_data['token_count_estimate']}")
        output_lines.append("")
        
        # 核心指标（关键信息优先）
        output_lines.append("五维质量指标 (0.0-1.0):")
        metric_names = {
            'clarity': '清晰度',
            'relevance': '相关性',
            'completeness': '完整性', 
            'consistency': '一致性',
            'efficiency': '效率'
        }
        
        for metric, score in analysis_data['metrics'].items():
            indicator = "🟢" if score >= 0.7 else "🟡" if score >= 0.4 else "🔴"
            output_lines.append(f"  {indicator} {metric_names.get(metric, metric)}: {score:.2f}")
        
        output_lines.append("")
        
        # 按需提供详细信息
        if detailed:
            # 解释和建议（AI定性分析）
            output_lines.append("🔍 质量解读:")
            output_lines.append(f"  {insights['interpretation']}")
            
            if analysis_data['suggestions']:
                output_lines.append("\n💡 优化建议:")
                for suggestion in analysis_data['suggestions']:
                    output_lines.append(f"  • {suggestion}")
            
            if insights['recommendations']:
                output_lines.append("\n🎯 AI推荐改进:")
                for rec in insights['recommendations']:
                    output_lines.append(f"  • {rec}")
            
            if analysis_data['issues']:
                output_lines.append("\n⚠️  识别问题:")
                for issue in analysis_data['issues']:
                    output_lines.append(f"  • {issue}")
            
            critical_issues = [issue for issue in insights['critical_issues'] if issue != "无关键问题"]
            if critical_issues:
                output_lines.append("\n🚨 关键问题:")
                for issue in critical_issues:
                    output_lines.append(f"  • {issue}")
        else:
            # 简化版本 - 只显示最关键信息
            suggestions = analysis_data['suggestions'][:2]  # 只显示前2个建议
            issues = analysis_data['issues'][:2]            # 只显示前2个问题
            
            if suggestions:
                output_lines.append("\n💡 优化建议:")
                for suggestion in suggestions:
                    output_lines.append(f"  • {suggestion}")
            
            if issues:
                output_lines.append("\n⚠️  主要问题:")
                for issue in issues:
                    output_lines.append(f"  • {issue}")
            
            # 提供详细模式提示
            output_lines.append("\n💡 使用 detailed=true 参数获取完整分析")
        
        return "\n".join(output_lines)


# 实例化技能
CONTEXT_ANALYSIS_SKILL = ClaudeContextAnalysisSkill()

def execute(args: Dict[str, Any]) -> str:
    """
    Claude Skills标准执行接口
    """
    return CONTEXT_ANALYSIS_SKILL.execute(args)

def get_manifest() -> Dict[str, Any]:
    """
    获取技能清单 - Claude Skills标准
    """
    return {
        "name": CONTEXT_ANALYSIS_SKILL.name,
        "description": CONTEXT_ANALYSIS_SKILL.description,
        "version": CONTEXT_ANALYSIS_SKILL.version,
        "created_at": CONTEXT_ANALYSIS_SKILL.created_at,
        "parameters": {
            "type": "object",
            "properties": {
                "context": {
                    "type": "string",
                    "description": "要分析的上下文内容"
                },
                "request": {
                    "type": "string", 
                    "description": "分析请求（context的别名）"
                },
                "input": {
                    "type": "string",
                    "description": "输入内容（context的别名）"
                },
                "detailed": {
                    "type": "boolean",
                    "description": "是否返回详细分析",
                    "default": False
                }
            },
            "required": ["context"]
        }
    }