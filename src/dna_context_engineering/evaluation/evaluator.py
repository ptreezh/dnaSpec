"""
DNASPEC 评估框架 - 主入口
"""
from pathlib import Path
from typing import Optional

from .skill_evaluator import SkillEvaluator
from .system_evaluator import SystemEvaluator
from .report_generator import ReportGenerator


class DNASPECEvaluator:
    """DNASPEC评估框架主类"""

    def __init__(self, dnaspec_root: Optional[Path] = None):
        """
        初始化评估框架

        Args:
            dnaspec_root: DNASPEC项目根目录
        """
        if dnaspec_root is None:
            dnaspec_root = Path(__file__).parent.parent.parent.parent

        self.dnaspec_root = Path(dnaspec_root)
        self.skill_evaluator = SkillEvaluator(self.dnaspec_root)
        self.system_evaluator = SystemEvaluator(self.dnaspec_root)
        self.report_generator = ReportGenerator(self.dnaspec_root / 'reports')

    def evaluate_skill(self, skill_name: str):
        """
        评估单个技能

        Args:
            skill_name: 技能名称 (如: dnaspec-git)
        """
        print(f"\n评估技能: {skill_name}")
        print("-" * 60)

        result = self.skill_evaluator.evaluate_skill(skill_name)

        # 打印结果
        print(f"质量评分: {result.overall_score:.2f}")
        if result.quality_score:
            print(f"  - 清晰度: {result.quality_score.clarity:.2f}")
            print(f"  - 完整性: {result.quality_score.completeness:.2f}")
            print(f"  - 一致性: {result.quality_score.consistency:.2f}")
            print(f"  - 效率: {result.quality_score.efficiency:.2f}")
            print(f"  - 相关性: {result.quality_score.relevance:.2f}")
            print(f"  - 等级: {result.quality_score.level.value}")

        print(f"测试通过: {result.tests_passed}/{result.tests_total}")

        if result.recommendations:
            print("\n改进建议:")
            for rec in result.recommendations:
                print(f"  {rec}")

        return result

    def evaluate_system(self, generate_report: bool = True):
        """
        评估整个系统

        Args:
            generate_report: 是否生成报告
        """
        # 执行系统评估
        result = self.system_evaluator.evaluate_system()

        # 生成摘要
        summary = self.system_evaluator.generate_summary(result)
        print(summary)

        # 生成报告
        if generate_report:
            print("\n生成评估报告...")

            # 生成Markdown报告
            md_file = self.report_generator.output_dir / 'latest_evaluation.md'
            self.report_generator.generate_markdown_report(result, md_file)

            # 生成JSON报告
            json_file = self.report_generator.output_dir / 'latest_evaluation.json'
            self.report_generator.generate_json_report(result, json_file)

            # 保存历史
            history_file = self.report_generator.save_evaluation_history(result)
            print(f"✅ 评估历史已保存: {history_file}")

        return result

    def evaluate_all_skills(self):
        """评估所有技能"""
        results = self.skill_evaluator.evaluate_all_skills()

        print("\n" + "=" * 60)
        print("所有技能评估结果")
        print("=" * 60)

        for skill_name, result in results.items():
            level = result.quality_score.level.value if result.quality_score else "unknown"
            print(
                f"{skill_name}: {result.overall_score:.2f} ({level}) "
                f"[{result.tests_passed}/{result.tests_total}]"
            )

        return results


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='DNASPEC 评估框架')
    parser.add_argument(
        '--skill',
        type=str,
        help='评估特定技能'
    )
    parser.add_argument(
        '--system',
        action='store_true',
        help='评估整个系统'
    )
    parser.add_argument(
        '--all-skills',
        action='store_true',
        help='评估所有技能'
    )
    parser.add_argument(
        '--no-report',
        action='store_true',
        help='不生成报告'
    )

    args = parser.parse_args()

    evaluator = DNASPECEvaluator()

    if args.skill:
        evaluator.evaluate_skill(args.skill)
    elif args.all_skills:
        evaluator.evaluate_all_skills()
    else:
        # 默认评估系统
        evaluator.evaluate_system(generate_report=not args.no_report)


if __name__ == '__main__':
    main()
