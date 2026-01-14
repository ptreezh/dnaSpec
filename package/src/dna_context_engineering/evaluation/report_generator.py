"""
报告生成器 - 生成评估报告
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import asdict

from .metrics import SystemEvaluationResult, SkillEvaluationResult, TrendData


class ReportGenerator:
    """报告生成器"""

    def __init__(self, output_dir: Optional[Path] = None):
        if output_dir is None:
            output_dir = Path(__file__).parent.parent.parent.parent / 'reports'
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_markdown_report(
        self,
        result: SystemEvaluationResult,
        output_file: Optional[Path] = None
    ) -> str:
        """生成Markdown格式报告"""
        lines = [
            "# DNASPEC 系统评估报告",
            "",
            f"**生成时间**: {result.evaluated_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"**系统健康状态**: {result.health_status.upper()}",
            "",
            "## 📊 整体指标",
            "",
            f"- **总技能数**: {result.total_skills}",
            f"- **通过门槛技能**: {result.skills_passing_threshold}/{result.total_skills}",
            f"- **平均质量评分**: {result.average_quality_score:.2f} / 1.00",
            f"- **技能协作评分**: {result.collaboration_score:.2f} / 1.00",
            f"- **可用性评分**: {result.usability_score:.2f} / 1.00",
            "",
            "## 📈 质量分布",
            "",
        ]

        # 质量分布统计
        quality_ranges = {
            'excellent (0.9-1.0)': 0,
            'good (0.75-0.9)': 0,
            'satisfactory (0.6-0.75)': 0,
            'needs improvement (0.4-0.6)': 0,
            'poor (0.0-0.4)': 0
        }

        for skill_result in result.skill_evaluations.values():
            score = skill_result.overall_score
            if score >= 0.9:
                quality_ranges['excellent (0.9-1.0)'] += 1
            elif score >= 0.75:
                quality_ranges['good (0.75-0.9)'] += 1
            elif score >= 0.6:
                quality_ranges['satisfactory (0.6-0.75)'] += 1
            elif score >= 0.4:
                quality_ranges['needs improvement (0.4-0.6)'] += 1
            else:
                quality_ranges['poor (0.0-0.4)'] += 1

        for range_name, count in quality_ranges.items():
            if count > 0:
                lines.append(f"- **{range_name}**: {count}")

        lines.append("")
        lines.append("## 🔧 技能详情")
        lines.append("")

        # 技能详情表
        lines.append("| 技能 | 质量评分 | 清晰度 | 完整性 | 一致性 | 效率 | 测试通过 |")
        lines.append("|------|---------|--------|--------|--------|------|----------|")

        for skill_name, skill_result in result.skill_evaluations.items():
            if skill_result.quality_score:
                lines.append(
                    f"| {skill_name} | "
                    f"{skill_result.overall_score:.2f} | "
                    f"{skill_result.quality_score.clarity:.2f} | "
                    f"{skill_result.quality_score.completeness:.2f} | "
                    f"{skill_result.quality_score.consistency:.2f} | "
                    f"{skill_result.quality_score.efficiency:.2f} | "
                    f"{skill_result.tests_passed}/{skill_result.tests_total} |"
                )

        lines.append("")
        lines.append("## 💡 改进建议")
        lines.append("")

        # 汇总所有建议
        all_recommendations = []
        for skill_result in result.skill_evaluations.values():
            all_recommendations.extend(skill_result.recommendations)

        if all_recommendations:
            for i, rec in enumerate(all_recommendations, 1):
                lines.append(f"{i}. {rec}")
        else:
            lines.append("✅ 系统整体质量良好，无重大问题需要改进。")

        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("*本报告由 DNASPEC 评估框架自动生成*")

        report = "\n".join(lines)

        if output_file:
            output_file = Path(output_file)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"✅ Markdown报告已保存: {output_file}")

        return report

    def generate_json_report(
        self,
        result: SystemEvaluationResult,
        output_file: Optional[Path] = None
    ) -> Dict[str, Any]:
        """生成JSON格式报告"""
        # 转换为可序列化的字典
        report_dict = {
            'evaluated_at': result.evaluated_at.isoformat(),
            'overall_metrics': {
                'total_skills': result.total_skills,
                'skills_passing_threshold': result.skills_passing_threshold,
                'average_quality_score': result.average_quality_score,
                'collaboration_score': result.collaboration_score,
                'usability_score': result.usability_score,
                'health_status': result.health_status
            },
            'skill_evaluations': {}
        }

        for skill_name, skill_result in result.skill_evaluations.items():
            skill_dict = {
                'overall_score': skill_result.overall_score,
                'test_success_rate': skill_result.test_success_rate,
                'tests_passed': skill_result.tests_passed,
                'tests_total': skill_result.tests_total,
                'issues': skill_result.issues,
                'recommendations': skill_result.recommendations
            }

            if skill_result.quality_score:
                skill_dict['quality_score'] = {
                    'clarity': skill_result.quality_score.clarity,
                    'completeness': skill_result.quality_score.completeness,
                    'consistency': skill_result.quality_score.consistency,
                    'efficiency': skill_result.quality_score.efficiency,
                    'relevance': skill_result.quality_score.relevance,
                    'overall': skill_result.quality_score.overall,
                    'level': skill_result.quality_score.level.value
                }

            report_dict['skill_evaluations'][skill_name] = skill_dict

        if output_file:
            output_file = Path(output_file)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report_dict, f, indent=2, ensure_ascii=False)
            print(f"✅ JSON报告已保存: {output_file}")

        return report_dict

    def save_evaluation_history(
        self,
        result: SystemEvaluationResult
    ) -> Path:
        """保存评估历史"""
        timestamp = result.evaluated_at.strftime('%Y%m%d_%H%M%S')
        history_dir = self.output_dir / 'history'
        history_dir.mkdir(exist_ok=True)

        # 保存JSON格式
        json_file = history_dir / f'evaluation_{timestamp}.json'
        self.generate_json_report(result, json_file)

        # 保存Markdown格式
        md_file = history_dir / f'evaluation_{timestamp}.md'
        self.generate_markdown_report(result, md_file)

        # 更新索引
        self._update_history_index(result, json_file, md_file)

        return json_file

    def _update_history_index(
        self,
        result: SystemEvaluationResult,
        json_file: Path,
        md_file: Path
    ):
        """更新历史索引"""
        index_file = self.output_dir / 'history_index.json'

        # 加载现有索引
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                index = json.load(f)
        else:
            index = {'evaluations': []}

        # 添加新记录
        index['evaluations'].append({
            'timestamp': result.evaluated_at.isoformat(),
            'json_file': str(json_file),
            'md_file': str(md_file),
            'average_quality_score': result.average_quality_score,
            'health_status': result.health_status
        })

        # 按时间排序
        index['evaluations'].sort(key=lambda x: x['timestamp'], reverse=True)

        # 保存索引
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
