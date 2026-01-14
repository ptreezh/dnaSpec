"""
Constraint Generator Executor
智能协调器 - 组合所有组件并选择合适的提示词层次
"""

from typing import Dict, Any, Optional
from pathlib import Path
import json

from .validator import ConstraintValidator, ValidationResult
from .calculator import ConstraintCalculator, ConstraintMetrics
from .analyzer import ConstraintAnalyzer, ConstraintAnalysis


class ConstraintExecutor:
    """约束生成执行器"""

    def __init__(self, skill_dir: Optional[Path] = None):
        if skill_dir is None:
            skill_dir = Path(__file__).parent.parent

        self.skill_dir = Path(skill_dir)
        self.prompts_dir = self.skill_dir / "prompts"

        # 初始化组件
        self.validator = ConstraintValidator()
        self.calculator = ConstraintCalculator()
        self.analyzer = ConstraintAnalyzer()

    def execute(
        self,
        request: str,
        context: Optional[Dict] = None,
        force_level: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        执行约束生成

        Args:
            request: 约束生成请求
            context: 可选的上下文信息
            force_level: 强制使用特定层次的提示词 (00/01/02/03)

        Returns:
            包含以下键的字典:
            - success: bool - 是否成功
            - validation: ValidationResult - 验证结果
            - metrics: ConstraintMetrics - 计算的指标
            - analysis: ConstraintAnalysis - 分析结果
            - prompt_level: str - 使用的提示词层次
            - prompt_content: str - 提示词内容
            - recommendations: List[str] - 综合建议
        """
        # 1. 验证请求
        validation = self.validator.validate(request, context)

        if not validation.is_valid:
            return {
                "success": False,
                "validation": validation,
                "error": "请求验证失败"
            }

        # 2. 计算指标
        metrics = self.calculator.calculate(request, context)

        # 3. 分析约束
        analysis = self.analyzer.analyze(request, context)

        # 4. 选择提示词层次
        if force_level:
            prompt_level = force_level
        else:
            prompt_level = self._select_level(metrics, analysis)

        # 5. 加载提示词
        prompt_content = self._load_prompt(prompt_level)

        # 6. 生成综合建议
        recommendations = self._generate_recommendations(metrics, analysis)

        return {
            "success": True,
            "validation": validation,
            "metrics": metrics,
            "analysis": analysis,
            "prompt_level": prompt_level,
            "prompt_content": prompt_content,
            "recommendations": recommendations
        }

    def _select_level(
        self,
        metrics: ConstraintMetrics,
        analysis: ConstraintAnalysis
    ) -> str:
        """
        智能选择提示词层次

        规则:
        - 00: 基础概念 (复杂度 < 0.3, tokens < 1000)
        - 01: 基本应用 (复杂度 < 0.5, tokens < 3000)
        - 02: 中级场景 (复杂度 < 0.7, tokens < 5000)
        - 03: 高级应用 (其他情况)
        """
        complexity = metrics.complexity_score
        tokens = metrics.token_count

        # 检测约束冲突 → 高级层次
        if analysis.potential_conflicts:
            return "03"

        # 检测多种约束类型 → 中级或高级
        type_count = sum([
            metrics.has_performance_constraint,
            metrics.has_security_constraint,
            metrics.has_functional_constraint,
            metrics.has_technical_constraint
        ])

        if type_count >= 3:
            return "03"
        elif type_count >= 2:
            return "02"

        # 基于复杂度和token数量
        if complexity < 0.3 and tokens < 1000:
            return "00"
        elif complexity < 0.5 and tokens < 3000:
            return "01"
        elif complexity < 0.7 or tokens < 5000:
            return "02"
        else:
            return "03"

    def _load_prompt(self, level: str) -> str:
        """加载提示词文件"""
        prompt_file = self.prompts_dir / f"{level}_context.md"

        if not prompt_file.exists():
            return f"# 约束生成 - 层次 {level}\n\n提示词文件未找到"

        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()

    def _generate_recommendations(
        self,
        metrics: ConstraintMetrics,
        analysis: ConstraintAnalysis
    ) -> list:
        """生成综合建议"""
        recommendations = []

        # 来自calculator的建议
        recommendations.extend(metrics.recommendations)

        # 来自analyzer的建议
        recommendations.extend(analysis.recommendations)

        # 额外的执行建议
        if metrics.complexity_score > 0.7:
            recommendations.append(
                "请求复杂度较高，建议分阶段处理约束"
            )

        if metrics.specificity_score < 0.5:
            recommendations.append(
                "建议使用SMART原则使约束更具体、可测量"
            )

        if analysis.potential_conflicts:
            recommendations.append(
                f"检测到{len(analysis.potential_conflicts)}个潜在冲突，需要优先处理"
            )

        return recommendations


if __name__ == "__main__":
    # 测试
    executor = ConstraintExecutor()

    test_cases = [
        ("生成API性能约束", None),
        ("系统需要高安全性和快速响应，可能存在冲突", None),
        ("响应时间小于100ms，支持1000 QPS，需要加密", None),
    ]

    for request, context in test_cases:
        print(f"\n{'='*60}")
        print(f"请求: {request}")
        print(f"{'='*60}")

        result = executor.execute(request, context)

        if result["success"]:
            print(f"✅ 验证通过")
            print(f"📊 复杂度: {result['metrics'].complexity_score:.2f}")
            print(f"📈 推荐层次: {result['prompt_level']}")
            print(f"🔍 检测到的约束类型: {[t.value for t in result['analysis'].detected_types]}")
            print(f"⚠️  潜在冲突: {len(result['analysis'].potential_conflicts)}")
            print(f"💡 建议: {len(result['recommendations'])}")

            if result['analysis'].potential_conflicts:
                for conflict in result['analysis'].potential_conflicts:
                    print(f"   - {conflict}")
        else:
            print(f"❌ 验证失败")
            for issue in result["validation"].issues:
                print(f"   [{issue.severity.value}] {issue.message}")
