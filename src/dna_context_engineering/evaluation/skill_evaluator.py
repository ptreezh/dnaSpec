"""
技能评估器 - 评估单个DNASPEC技能的质量
"""
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from .metrics import SkillEvaluationResult, QualityScore, PerformanceMetrics


class SkillEvaluator:
    """技能评估器"""

    def __init__(self, dnaspec_root: Optional[Path] = None):
        if dnaspec_root is None:
            dnaspec_root = Path(__file__).parent.parent.parent.parent
        self.dnaspec_root = Path(dnaspec_root)
        self.skills_dir = self.dnaspec_root / 'skills'

    def evaluate_skill(self, skill_name: str) -> SkillEvaluationResult:
        """评估单个技能"""
        print(f"评估技能: {skill_name}")

        skill_dir = self.skills_dir / skill_name
        if not skill_dir.exists():
            return SkillEvaluationResult(
                skill_name=skill_name,
                version="unknown",
                issues=[f"技能目录不存在: {skill_dir}"]
            )

        # 1. 检查技能结构
        structure_score = self._evaluate_structure(skill_dir)

        # 2. 运行测试
        test_results = self._run_tests(skill_name)

        # 3. 评估提示质量
        prompt_quality = self._evaluate_prompts(skill_dir)

        # 4. 评估代码质量
        code_quality = self._evaluate_code(skill_dir)

        # 5. 组合质量评分
        quality_score = QualityScore(
            clarity=(structure_score + prompt_quality['clarity']) / 2,
            completeness=prompt_quality['completeness'],
            consistency=code_quality['consistency'],
            efficiency=code_quality['efficiency'],
            relevance=0.8  # 默认良好
        )

        # 6. 生成建议
        recommendations = self._generate_recommendations(
            skill_name, quality_score, test_results
        )

        return SkillEvaluationResult(
            skill_name=skill_name,
            version=self._get_version(skill_dir),
            evaluated_at=datetime.now(),
            quality_score=quality_score,
            tests_passed=test_results['passed'],
            tests_total=test_results['total'],
            test_success_rate=test_results['success_rate'],
            issues=test_results['issues'],
            recommendations=recommendations
        )

    def _evaluate_structure(self, skill_dir: Path) -> float:
        """评估技能目录结构"""
        required_files = [
            'SKILL.md',
            'prompts/00_context.md',
            'prompts/01_basic.md',
            'prompts/02_intermediate.md',
            'scripts/validator.py',
            'scripts/calculator.py',
            'scripts/analyzer.py',
            'scripts/executor.py',
        ]

        score = 0.0
        for file in required_files:
            if (skill_dir / file).exists():
                score += 1.0 / len(required_files)

        return score

    def _run_tests(self, skill_name: str) -> Dict:
        """运行技能测试"""
        test_file = self.dnaspec_root / f'test_{skill_name.replace("dnaspec-", "")}.py'

        if not test_file.exists():
            return {
                'passed': 0,
                'total': 0,
                'success_rate': 0.0,
                'issues': [f"测试文件不存在: {test_file}"]
            }

        try:
            result = subprocess.run(
                [sys.executable, str(test_file)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.dnaspec_root
            )

            if result.returncode == 0:
                # 简单解析测试输出
                output = result.stdout
                if '✅ 所有测试通过' in output:
                    return {
                        'passed': 5,  # 估计值
                        'total': 5,
                        'success_rate': 1.0,
                        'issues': []
                    }

            return {
                'passed': 0,
                'total': 1,
                'success_rate': 0.0,
                'issues': [f"测试失败: {result.stderr[:200]}"]
            }
        except Exception as e:
            return {
                'passed': 0,
                'total': 0,
                'success_rate': 0.0,
                'issues': [f"测试执行异常: {str(e)}"]
            }

    def _evaluate_prompts(self, skill_dir: Path) -> Dict:
        """评估提示文件质量"""
        prompts_dir = skill_dir / 'prompts'

        clarity_scores = []
        completeness_scores = []

        for prompt_file in ['00_context.md', '01_basic.md', '02_intermediate.md']:
            file_path = prompts_dir / prompt_file
            if not file_path.exists():
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 清晰度评估：检查是否使用了markdown格式
            clarity = 0.5
            if '##' in content:  # 有标题
                clarity += 0.2
            if '```' in content:  # 有代码块
                clarity += 0.15
            if '-' in content:  # 有列表
                clarity += 0.15

            # 完整性评估：检查内容长度
            min_length = 300
            completeness = min(len(content) / min_length, 1.0)

            clarity_scores.append(clarity)
            completeness_scores.append(completeness)

        return {
            'clarity': sum(clarity_scores) / len(clarity_scores) if clarity_scores else 0.5,
            'completeness': sum(completeness_scores) / len(completeness_scores) if completeness_scores else 0.5
        }

    def _evaluate_code(self, skill_dir: Path) -> Dict:
        """评估代码质量"""
        scripts_dir = skill_dir / 'scripts'

        consistency = 0.8  # 默认良好
        efficiency = 0.8

        # 检查是否有必要的脚本
        required_scripts = ['validator.py', 'calculator.py', 'analyzer.py', 'executor.py']
        existing_scripts = sum(1 for s in required_scripts if (scripts_dir / s).exists())
        consistency = existing_scripts / len(required_scripts)

        return {
            'consistency': consistency,
            'efficiency': efficiency
        }

    def _get_version(self, skill_dir: Path) -> str:
        """获取技能版本"""
        package_json = self.dnaspec_root / 'package.json'
        if package_json.exists():
            import json
            with open(package_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('version', 'unknown')
        return 'unknown'

    def _generate_recommendations(
        self,
        skill_name: str,
        quality_score: QualityScore,
        test_results: Dict
    ) -> List[str]:
        """生成改进建议"""
        recommendations = []

        # 基于质量评分生成建议
        if quality_score.clarity < 0.7:
            recommendations.append("📝 提示清晰度较低，建议改进提示文件的组织结构和表述")
        if quality_score.completeness < 0.7:
            recommendations.append("📋 提示完整性不足，建议补充更多示例和说明")
        if quality_score.consistency < 0.7:
            recommendations.append("🔧 代码一致性需要改进，确保所有脚本都存在")
        if quality_score.overall < 0.6:
            recommendations.append(f"⚠️ 技能 {skill_name} 整体质量较低，建议全面优化")

        # 基于测试结果生成建议
        if test_results['success_rate'] < 1.0:
            recommendations.append(f"🧪 测试通过率仅 {test_results['success_rate']*100:.0f}%，需要修复失败的测试")

        if not recommendations:
            recommendations.append("✅ 技能质量良好，继续保持")

        return recommendations

    def evaluate_all_skills(self) -> Dict[str, SkillEvaluationResult]:
        """评估所有技能"""
        results = {}

        if not self.skills_dir.exists():
            return results

        for skill_dir in sorted(self.skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue

            skill_name = skill_dir.name
            if not skill_name.startswith('dnaspec-'):
                continue

            results[skill_name] = self.evaluate_skill(skill_name)

        return results
