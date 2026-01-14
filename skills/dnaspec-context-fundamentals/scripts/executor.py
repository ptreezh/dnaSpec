"""
Context Fundamentals Executor

智能协调器：整合定性分析和定量计算
根据请求复杂度和上下文特征自动选择合适的提示词层次
"""

from typing import Dict, Any, Optional, List
from pathlib import Path
import json

from .validator import ContextFundamentalsValidator, ValidationResult
from .calculator import ContextFundamentalsCalculator, ContextMetrics
from .analyzer import ContextFundamentalsAnalyzer, ContextAnalysis, FailureModeDetection


class ContextFundamentalsExecutor:
    """
    上下文基础知识执行器

    职责：
    1. 验证输入
    2. 计算指标
    3. 分析上下文
    4. 选择合适的提示词层次
    5. 加载提示词内容
    6. 返回完整结果
    """

    def __init__(self, skill_dir: Optional[Path] = None):
        """
        初始化执行器

        Args:
            skill_dir: 技能目录路径
        """
        if skill_dir is None:
            # 默认为当前技能目录
            skill_dir = Path(__file__).parent.parent

        self.skill_dir = Path(skill_dir)
        self.prompts_dir = self.skill_dir / "prompts"

        # 初始化组件
        self.validator = ContextFundamentalsValidator()
        self.calculator = ContextFundamentalsCalculator()
        self.analyzer = ContextFundamentalsAnalyzer()

    def execute(
        self,
        request: str,
        context: Optional[Dict[str, Any]] = None,
        force_level: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        执行上下文基础知识分析

        Args:
            request: 用户请求
            context: 附加上下文
            force_level: 强制使用特定提示词层次（"00", "01", "02", "03"）

        Returns:
            Dict: 完整的执行结果
        """
        # 1. 验证输入
        validation = self.validator.validate(request, context)

        # 2. 计算指标
        metrics = self.calculator.calculate(request, context)

        # 3. 分析上下文
        analysis = self.analyzer.analyze(request, context)

        # 4. 选择提示词层次
        if force_level:
            prompt_level = force_level
        else:
            prompt_level = self._select_prompt_level(metrics, analysis, validation)

        # 5. 加载提示词
        prompt_content = self._load_prompt(prompt_level)

        # 6. 构建最终结果
        result = {
            "validation": self._format_validation(validation),
            "metrics": self._format_metrics(metrics),
            "analysis": self._format_analysis(analysis),
            "prompt_level": prompt_level,
            "prompt_content": prompt_content,
            "summary": self._generate_summary(validation, metrics, analysis, prompt_level),
            "recommendations": self._generate_recommendations(metrics, analysis)
        }

        return result

    def _select_prompt_level(
        self,
        metrics: ContextMetrics,
        analysis: ContextAnalysis,
        validation: ValidationResult
    ) -> str:
        """
        智能选择提示词层次

        选择逻辑：
        1. 如果有严重验证错误，使用最简单的Level 00
        2. 基于复杂度分数、token数量、失效模式综合判断
        3. 倾向于使用较低层次（渐进式披露）
        """
        # 检查验证结果
        if validation.has_errors():
            # 有验证错误，使用基础层
            return "00"

        # 检查是否有严重失效模式
        critical_failures = [f for f in analysis.detected_failures if f.severity == "high"]
        if critical_failures:
            # 有严重问题，先解决基础
            return "00"

        # 基于指标综合判断
        complexity = metrics.complexity_score
        tokens = metrics.token_count

        # 决策树
        if complexity < 0.3 and tokens < 5000:
            # 简单请求，核心概念层
            return "00"

        elif complexity < 0.5 and tokens < 10000:
            # 中等复杂度，基础应用层
            return "01"

        elif complexity < 0.7 or tokens < 20000:
            # 较复杂，中级场景层
            return "02"

        else:
            # 高度复杂，高级应用层
            return "03"

    def _load_prompt(self, level: str) -> str:
        """
        加载指定层次的提示词

        Args:
            level: 提示词层次（"00", "01", "02", "03"）

        Returns:
            str: 提示词内容
        """
        # 文件名映射
        filename_map = {
            "00": "00_context.md",
            "01": "01_basic.md",
            "02": "02_intermediate.md",
            "03": "03_advanced.md"
        }

        if level not in filename_map:
            raise ValueError(f"无效的提示词层次: {level}")

        prompt_file = self.prompts_dir / filename_map[level]

        if not prompt_file.exists():
            raise FileNotFoundError(f"提示词文件不存在: {prompt_file}")

        with open(prompt_file, 'r', encoding='utf-8') as f:
            content = f.read()

        return content

    def _format_validation(self, validation: ValidationResult) -> Dict[str, Any]:
        """格式化验证结果"""
        return {
            "is_valid": validation.is_valid,
            "has_errors": validation.has_errors(),
            "has_warnings": validation.has_warnings(),
            "summary": validation.get_summary(),
            "issues": [
                {
                    "severity": issue.severity.value,
                    "category": issue.category,
                    "message": issue.message,
                    "suggestion": issue.suggestion
                }
                for issue in validation.issues
            ]
        }

    def _format_metrics(self, metrics: ContextMetrics) -> Dict[str, Any]:
        """格式化指标"""
        return {
            "token_count": metrics.token_count,
            "character_count": metrics.character_count,
            "word_count": metrics.word_count,
            "line_count": metrics.line_count,
            "complexity_score": metrics.complexity_score,
            "information_density": metrics.information_density,
            "structure_quality": metrics.structure_quality,
            "relevance_score": metrics.relevance_score,
            "keyword_overlap": metrics.keyword_overlap,
            "completeness_score": metrics.completeness_score,
            "consistency_score": metrics.consistency_score,
            "freshness_score": metrics.freshness_score,
            "recommended_level": metrics.recommended_prompt_level,
            "actions": metrics.recommended_actions,
            "warnings": metrics.warnings
        }

    def _format_analysis(self, analysis: ContextAnalysis) -> Dict[str, Any]:
        """格式化分析结果"""
        return {
            "detected_failures": [
                {
                    "mode": failure.mode.value,
                    "severity": failure.severity,
                    "evidence": failure.evidence,
                    "suggestions": failure.suggestions
                }
                for failure in analysis.detected_failures
            ],
            "recognized_patterns": [
                {
                    "type": pattern.pattern_type,
                    "confidence": pattern.confidence,
                    "description": pattern.description
                }
                for pattern in analysis.recognized_patterns
            ],
            "quality_scores": analysis.quality_scores,
            "optimization_suggestions": analysis.optimization_suggestions,
            "recommended_strategy": analysis.recommended_strategy
        }

    def _generate_summary(
        self,
        validation: ValidationResult,
        metrics: ContextMetrics,
        analysis: ContextAnalysis,
        prompt_level: str
    ) -> str:
        """生成执行摘要"""
        lines = []

        # 验证状态
        if validation.is_valid:
            lines.append("✅ 请求验证通过")
        else:
            lines.append("❌ 请求验证失败")

        # Token数量
        lines.append(f"📊 Token数量: {metrics.token_count:,}")

        # 复杂度
        complexity_desc = self._describe_complexity(metrics.complexity_score)
        lines.append(f"🎯 复杂度: {complexity_desc}")

        # 选择的层次
        level_desc = {
            "00": "核心概念层（快速理解）",
            "01": "基础应用层（常见场景）",
            "02": "中级场景层（复杂任务）",
            "03": "高级应用层（大规模系统）"
        }.get(prompt_level, "未知")
        lines.append(f"📚 提示词层次: Level {prompt_level} - {level_desc}")

        # 失效模式
        if analysis.detected_failures:
            lines.append(f"⚠️ 检测到{len(analysis.detected_failures)}个潜在失效模式")
        else:
            lines.append("✅ 未检测到失效模式")

        # 质量分数
        avg_quality = sum(analysis.quality_scores.values()) / len(analysis.quality_scores) if analysis.quality_scores else 0
        quality_desc = self._describe_quality(avg_quality)
        lines.append(f"📈 上下文质量: {quality_desc}")

        return "\n".join(lines)

    def _describe_complexity(self, score: float) -> str:
        """描述复杂度"""
        if score < 0.3:
            return "简单"
        elif score < 0.5:
            return "中等"
        elif score < 0.7:
            return "较复杂"
        else:
            return "高度复杂"

    def _describe_quality(self, score: float) -> str:
        """描述质量"""
        if score > 0.8:
            return "优秀"
        elif score > 0.6:
            return "良好"
        elif score > 0.4:
            return "中等"
        else:
            return "需要改进"

    def _generate_recommendations(
        self,
        metrics: ContextMetrics,
        analysis: ContextAnalysis
    ) -> List[str]:
        """生成综合推荐"""
        recommendations = []

        # 来自指标的建议
        recommendations.extend(metrics.recommended_actions)

        # 来自分析的建议
        recommendations.extend(analysis.optimization_suggestions)

        # 来自推荐策略的建议
        recommendations.append(f"策略建议: {analysis.recommended_strategy}")

        # 去重并排序
        unique_recommendations = list(set(recommendations))

        return unique_recommendations


# 便捷函数
def execute_context_fundamentals(
    request: str,
    context: Optional[Dict[str, Any]] = None,
    skill_dir: Optional[Path] = None,
    force_level: Optional[str] = None
) -> Dict[str, Any]:
    """
    执行上下文基础知识分析的便捷函数

    Args:
        request: 用户请求
        context: 附加上下文
        skill_dir: 技能目录
        force_level: 强制使用特定提示词层次

    Returns:
        Dict: 完整的执行结果
    """
    executor = ContextFundamentalsExecutor(skill_dir)
    return executor.execute(request, context, force_level)


if __name__ == "__main__":
    import sys

    # 测试
    test_cases = [
        {
            "name": "简单问题",
            "request": "什么是上下文？",
            "context": None
        },
        {
            "name": "中等复杂度",
            "request": "如何在AI系统中优化上下文管理？请说明最佳实践和常见陷阱",
            "context": {"domain": "AI", "scale": "medium"}
        },
        {
            "name": "高度复杂",
            "request": "设计一个包含50个微服务的大型电商系统的上下文管理架构，需要考虑分布式协作、版本控制、性能优化等多个方面",
            "context": {"scale": "large", "services": 50, "architecture": "microservices"}
        }
    ]

    for test_case in test_cases:
        print(f"\n{'='*80}")
        print(f"测试用例: {test_case['name']}")
        print(f"{'='*80}\n")

        result = execute_context_fundamentals(
            request=test_case["request"],
            context=test_case["context"]
        )

        # 打印摘要
        print("📋 执行摘要:")
        print(result["summary"])
        print()

        # 打印验证结果
        if result["validation"]["issues"]:
            print("🔍 验证问题:")
            for issue in result["validation"]["issues"]:
                print(f"  [{issue['severity'].upper()}] {issue['message']}")
                if issue.get("suggestion"):
                    print(f"    💡 {issue['suggestion']}")
            print()

        # 打印检测到的失效模式
        if result["analysis"]["detected_failures"]:
            print("⚠️ 失效模式:")
            for failure in result["analysis"]["detected_failures"]:
                print(f"\n  {failure['mode']} ({failure['severity']}):")
                for evidence in failure["evidence"]:
                    print(f"    - {evidence}")
            print()

        # 打印识别的模式
        if result["analysis"]["recognized_patterns"]:
            print("🔍 识别的模式:")
            for pattern in result["analysis"]["recognized_patterns"]:
                print(f"  - {pattern['type']}: {pattern['description']}")
            print()

        # 打印推荐
        if result["recommendations"]:
            print("💡 推荐:")
            for rec in result["recommendations"][:5]:  # 只显示前5个
                print(f"  - {rec}")
            print()

        # 打印提示词层次
        print(f"📚 选择的提示词: Level {result['prompt_level']}")
        print(f"   提示词长度: {len(result['prompt_content'])} 字符")
        print()

        # 询问是否继续
        input("\n按Enter键继续下一个测试用例...")
