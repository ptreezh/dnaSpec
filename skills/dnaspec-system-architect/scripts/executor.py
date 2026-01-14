"""
System Architect Executor
智能协调器
"""

from typing import Dict, Any, Optional
from pathlib import Path

from .validator import SystemArchitectValidator
from .calculator import ArchitectureCalculator
from .analyzer import ArchitectureAnalyzer


class SystemArchitectExecutor:
    """系统架构执行器"""

    def __init__(self, skill_dir: Optional[Path] = None):
        if skill_dir is None:
            skill_dir = Path(__file__).parent.parent

        self.skill_dir = Path(skill_dir)
        self.prompts_dir = self.skill_dir / "prompts"

        self.validator = SystemArchitectValidator()
        self.calculator = ArchitectureCalculator()
        self.analyzer = ArchitectureAnalyzer()

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
            prompt_file = self.prompts_dir / "00_context.md"

        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()

    def _generate_recommendations(self, metrics, analysis) -> list:
        """生成综合建议"""
        recommendations = []

        # 来自calculator的建议
        if metrics.recommendations:
            recommendations.extend(metrics.recommendations)

        # 来自analyzer的建议
        if analysis.recommendations:
            recommendations.extend(analysis.recommendations)

        # 架构类型建议
        if metrics.has_microservice_arch:
            recommendations.append("微服务架构需要完善DevOps能力")

        if metrics.has_serverless_arch:
            recommendations.append("无服务器架构适合低频、突发流量场景")

        return recommendations
