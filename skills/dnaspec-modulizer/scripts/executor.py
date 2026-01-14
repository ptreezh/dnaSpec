"""
Modulizer Executor
智能协调器
"""

from typing import Dict, Any, Optional
from pathlib import Path

from .validator import ModulizerValidator
from .calculator import ModulizerCalculator, ModularityMetrics
from .analyzer import ModulizerAnalyzer, ModularityAnalysis


class ModulizerExecutor:
    """执行器"""

    def __init__(self, skill_dir: Optional[Path] = None):
        if skill_dir is None:
            skill_dir = Path(__file__).parent.parent

        self.skill_dir = Path(skill_dir)
        self.prompts_dir = self.skill_dir / "prompts"

        self.validator = ModulizerValidator()
        self.calculator = ModulizerCalculator()
        self.analyzer = ModulizerAnalyzer()

    def execute(
        self,
        request: str,
        context: Optional[Dict] = None,
        force_level: Optional[str] = None
    ) -> Dict[str, Any]:
        """执行"""
        # 1. 验证
        validation = self.validator.validate(request, context)

        if not validation.is_valid:
            return {
                "success": False,
                "validation": validation,
                "error": "请求验证失败"
            }

        # 2. 计算
        metrics = self.calculator.calculate(request, context)

        # 3. 分析
        analysis = self.analyzer.analyze(request, context)

        # 4. 选择层次
        level = force_level or metrics.recommended_level

        # 5. 加载提示词
        prompt = self._load_prompt(level)

        # 6. 生成建议
        recommendations = self._generate_recommendations(metrics, analysis)

        return {
            "success": True,
            "validation": validation,
            "metrics": metrics,
            "analysis": analysis,
            "prompt_level": level,
            "prompt_content": prompt,
            "recommendations": recommendations
        }

    def _load_prompt(self, level: str) -> str:
        """加载提示词"""
        filename_map = {
            "00": "00_context.md",
            "01": "01_basic.md",
            "02": "02_intermediate.md",
            "03": "03_advanced.md"
        }

        if level not in filename_map:
            raise ValueError(f"Invalid level: {level}")

        prompt_file = self.prompts_dir / filename_map[level]

        if not prompt_file.exists():
            # 其他层次还没创建，返回00层
            prompt_file = self.prompts_dir / "00_context.md"

        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()

    def _generate_recommendations(self, metrics, analysis) -> list:
        """生成综合建议"""
        recommendations = []

        # 来自calculator的建议
        if metrics.suggestions:
            recommendations.extend(metrics.suggestions)

        # 额外的执行建议
        if metrics.coupling_score > 0.5:
            recommendations.append("模块间耦合度较高，建议引入依赖注入或事件驱动架构")

        if metrics.cohesion_score < 0.5:
            recommendations.append("模块内聚性较低，建议重新审视模块职责划分")

        if metrics.complexity_score > 0.7:
            recommendations.append("系统复杂度较高，建议采用DDD领域驱动设计")

        return recommendations
