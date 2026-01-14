"""
系统评估器 - 评估DNASPEC整体系统性能
"""
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
import json

from .metrics import SystemEvaluationResult, SkillEvaluationResult
from .skill_evaluator import SkillEvaluator


class SystemEvaluator:
    """系统评估器"""

    def __init__(self, dnaspec_root: Optional[Path] = None):
        self.dnaspec_root = Path(dnaspec_root) if dnaspec_root else Path(__file__).parent.parent.parent.parent
        self.skill_evaluator = SkillEvaluator(self.dnaspec_root)

    def evaluate_system(self) -> SystemEvaluationResult:
        """评估整个系统"""
        print("=" * 60)
        print("DNASPEC 系统评估")
        print("=" * 60)

        # 1. 评估所有技能
        skill_evaluations = self.skill_evaluator.evaluate_all_skills()

        # 2. 计算系统整体指标
        total_skills = len(skill_evaluations)
        skills_passing = sum(
            1 for result in skill_evaluations.values()
            if result.overall_score >= 0.6
        )
        avg_quality = sum(
            result.overall_score for result in skill_evaluations.values()
        ) / total_skills if total_skills > 0 else 0.0

        # 3. 评估技能协作
        collaboration_score = self._evaluate_collaboration(skill_evaluations)

        # 4. 评估可用性
        usability_score = self._evaluate_usability(skill_evaluations)

        # 5. 确定健康状态
        health_status = self._determine_health_status(
            avg_quality, skills_passing, total_skills
        )

        result = SystemEvaluationResult(
            evaluated_at=datetime.now(),
            skill_evaluations=skill_evaluations,
            total_skills=total_skills,
            skills_passing_threshold=skills_passing,
            average_quality_score=avg_quality,
            collaboration_score=collaboration_score,
            usability_score=usability_score,
            health_status=health_status
        )

        return result

    def _evaluate_collaboration(
        self,
        skill_evaluations: Dict[str, SkillEvaluationResult]
    ) -> float:
        """评估技能协作效果"""
        # 检查已知协作技能对的质量
        collaboration_pairs = [
            ('dnaspec-context-analysis', 'dnaspec-context-optimization'),
            ('dnaspec-task-decomposer', 'dnaspec-workspace'),
            ('dnaspec-agent-creator', 'dnaspec-workspace'),
        ]

        pair_scores = []
        for skill1, skill2 in collaboration_pairs:
            if skill1 in skill_evaluations and skill2 in skill_evaluations:
                score1 = skill_evaluations[skill1].overall_score
                score2 = skill_evaluations[skill2].overall_score
                # 协作评分：两个技能质量的平均
                pair_scores.append((score1 + score2) / 2)

        return sum(pair_scores) / len(pair_scores) if pair_scores else 0.7

    def _evaluate_usability(
        self,
        skill_evaluations: Dict[str, SkillEvaluationResult]
    ) -> float:
        """评估系统可用性"""
        # 基于以下因素评估：
        # 1. 技能测试通过率
        test_rates = [
            result.test_success_rate
            for result in skill_evaluations.values()
        ]
        avg_test_rate = sum(test_rates) / len(test_rates) if test_rates else 0.0

        # 2. 技能平均质量
        avg_quality = sum(
            result.overall_score for result in skill_evaluations.values()
        ) / len(skill_evaluations) if skill_evaluations else 0.0

        # 综合评分
        return (avg_test_rate * 0.4 + avg_quality * 0.6)

    def _determine_health_status(
        self,
        avg_quality: float,
        passing_count: int,
        total_count: int
    ) -> str:
        """确定系统健康状态"""
        if avg_quality >= 0.8 and passing_count == total_count:
            return "healthy"
        elif avg_quality >= 0.6 and passing_count >= total_count * 0.8:
            return "warning"
        else:
            return "critical"

    def generate_summary(self, result: SystemEvaluationResult) -> str:
        """生成评估摘要"""
        lines = [
            "",
            "=" * 60,
            "DNASPEC 系统评估摘要",
            "=" * 60,
            "",
            f"评估时间: {result.evaluated_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"总技能数: {result.total_skills}",
            f"通过门槛技能: {result.skills_passing_threshold}",
            f"平均质量评分: {result.average_quality_score:.2f}",
            f"技能协作评分: {result.collaboration_score:.2f}",
            f"可用性评分: {result.usability_score:.2f}",
            f"健康状态: {result.health_status.upper()}",
            "",
            "-" * 60,
            "技能详情",
            "-" * 60,
        ]

        for skill_name, skill_result in result.skill_evaluations.items():
            level = skill_result.quality_score.level.value if skill_result.quality_score else "unknown"
            lines.append(
                f"{skill_name}: {skill_result.overall_score:.2f} ({level}) "
                f"[{skill_result.tests_passed}/{skill_result.tests_total} 测试通过]"
            )

        lines.append("")
        lines.append("-" * 60)

        # 汇总建议
        all_recommendations = []
        for skill_result in result.skill_evaluations.values():
            all_recommendations.extend(skill_result.recommendations)

        if all_recommendations:
            lines.append("改进建议:")
            for rec in all_recommendations[:10]:  # 最多显示10条
                lines.append(f"  {rec}")
        else:
            lines.append("✅ 系统整体质量良好，无重大问题")

        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)
