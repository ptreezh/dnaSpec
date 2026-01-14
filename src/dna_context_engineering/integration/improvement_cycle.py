"""
上下文改进循环 - 集成context-analysis和context-optimization
"""
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

# 添加src到路径
src_dir = Path(__file__).parent.parent.parent.parent / 'src'
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))


class ImprovementPhase(Enum):
    """改进阶段"""
    ANALYSIS = "analysis"  # 分析阶段
    OPTIMIZATION = "optimization"  # 优化阶段
    VERIFICATION = "verification"  # 验证阶段


@dataclass
class ImprovementCycleResult:
    """改进循环结果"""
    context_id: str
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    cycles_completed: int = 0
    max_cycles: int = 3

    # 初始状态
    initial_quality_score: float = 0.0

    # 最终状态
    final_quality_score: float = 0.0
    quality_improvement: float = 0.0

    # 各阶段结果
    analysis_results: List[Dict] = field(default_factory=list)
    optimization_results: List[Dict] = field(default_factory=list)
    verification_results: List[Dict] = field(default_factory=list)

    # 状态
    success: bool = False
    stopped_reason: Optional[str] = None

    @property
    def improvement_percentage(self) -> float:
        """改进百分比"""
        if self.initial_quality_score == 0:
            return 0.0
        return ((self.final_quality_score - self.initial_quality_score) /
                self.initial_quality_score) * 100


class ContextImprovementCycle:
    """上下文改进循环"""

    def __init__(self, dnaspec_root: Optional[Path] = None):
        if dnaspec_root is None:
            dnaspec_root = Path(__file__).parent.parent.parent.parent

        self.dnaspec_root = Path(dnaspec_root)
        self.max_cycles = 3  # 默认最多3个循环
        self.quality_threshold = 0.8  # 质量阈值0.8即可停止

    def improve_context(
        self,
        context_id: str,
        context_content: str,
        max_cycles: int = 3,
        quality_threshold: float = 0.8
    ) -> ImprovementCycleResult:
        """
        执行上下文改进循环

        流程: Analysis → Optimization → Verification → (重复或结束)

        Args:
            context_id: 上下文标识符
            context_content: 上下文内容
            max_cycles: 最大循环次数
            quality_threshold: 质量阈值（达到则停止）

        Returns:
            ImprovementCycleResult: 改进结果
        """
        print(f"\n{'='*60}")
        print(f"上下文改进循环: {context_id}")
        print(f"{'='*60}")

        result = ImprovementCycleResult(
            context_id=context_id,
            max_cycles=max_cycles
        )

        current_content = context_content

        for cycle in range(1, max_cycles + 1):
            print(f"\n📊 循环 {cycle}/{max_cycles}")
            print("-" * 60)

            # 阶段1: 分析（Analysis）
            print("[1/3] 分析阶段...")
            analysis_result = self._run_analysis(context_id, current_content)
            result.analysis_results.append(analysis_result)

            current_quality = self._extract_quality_score(analysis_result)
            if cycle == 1:
                result.initial_quality_score = current_quality

            print(f"  当前质量评分: {current_quality:.2f}")

            # 检查是否已达到阈值
            if current_quality >= quality_threshold:
                print(f"  ✅ 质量已达标 ({current_quality:.2f} >= {quality_threshold})")
                result.final_quality_score = current_quality
                result.cycles_completed = cycle
                result.success = True
                result.stopped_reason = "质量阈值达标"
                break

            # 阶段2: 优化（Optimization）
            print("[2/3] 优化阶段...")
            optimization_result = self._run_optimization(
                context_id, current_content, analysis_result
            )
            result.optimization_results.append(optimization_result)

            # 更新内容（这里模拟优化后的内容）
            # 实际应用中，optimization技能会返回优化后的内容
            current_content = self._simulate_optimization(current_content, optimization_result)

            # 阶段3: 验证（Verification）
            print("[3/3] 验证阶段...")
            verification_result = self._run_verification(context_id, current_content)
            result.verification_results.append(verification_result)

            new_quality = self._extract_quality_score(verification_result)
            print(f"  改进后质量评分: {new_quality:.2f}")

            result.cycles_completed = cycle
            result.final_quality_score = new_quality

            # 检查是否有改进
            if new_quality <= current_quality:
                print(f"  ⚠️ 质量未提升，停止循环")
                result.stopped_reason = "质量未提升"
                break

        else:
            # 完成所有循环
            result.success = result.final_quality_score > result.initial_quality_score
            result.stopped_reason = "达到最大循环次数"

        result.completed_at = datetime.now()
        result.quality_improvement = result.final_quality_score - result.initial_quality_score

        # 生成总结
        self._print_summary(result)

        return result

    def _run_analysis(self, context_id: str, content: str) -> Dict:
        """运行context-analysis技能"""
        try:
            from dna_context_engineering.skills_system_final import SkillExecutor

            executor = SkillExecutor()
            result = executor.execute_skill(
                skill_name='context-analysis',
                request='全面分析上下文质量，检测清晰度、完整性、一致性问题',
                context={'content': content[:2000]}  # 限制长度
            )

            return {
                'success': result.get('success', False),
                'metrics': result.get('metrics', {}),
                'analysis': result.get('analysis', {}),
                'recommendations': result.get('recommendations', []),
                'prompt_level': result.get('prompt_level', '00')
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'fallback_analysis': self._fallback_analysis(content)
            }

    def _run_optimization(
        self,
        context_id: str,
        content: str,
        analysis_result: Dict
    ) -> Dict:
        """运行context-optimization技能"""
        try:
            from dna_context_engineering.skills_system_final import SkillExecutor

            # 根据分析结果生成优化请求
            issues = analysis_result.get('recommendations', [])
            request = '优化上下文质量'
            if issues:
                request += f"，重点解决：{', '.join(issues[:3])}"

            executor = SkillExecutor()
            result = executor.execute_skill(
                skill_name='context-optimization',
                request=request,
                context={'content': content[:2000]}
            )

            return {
                'success': result.get('success', False),
                'metrics': result.get('metrics', {}),
                'analysis': result.get('analysis', {}),
                'recommendations': result.get('recommendations', []),
                'prompt_level': result.get('prompt_level', '00')
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'fallback_optimization': self._fallback_optimization(content)
            }

    def _run_verification(self, context_id: str, content: str) -> Dict:
        """验证优化效果"""
        # 重新分析来验证
        return self._run_analysis(context_id, content)

    def _extract_quality_score(self, result: Dict) -> float:
        """从分析结果提取质量评分"""
        # 尝试从不同位置提取评分
        if 'metrics' in result:
            metrics = result['metrics']
            if hasattr(metrics, 'analysis_dimensions'):
                # QualityScore对象
                return 0.7  # 默认值
            if isinstance(metrics, dict):
                # 简单评分模拟
                return 0.6 + (len(metrics.get('analysis_dimensions', [])) * 0.05)

        # fallback: 基于成功状态
        if result.get('success'):
            return 0.75
        return 0.5

    def _simulate_optimization(self, content: str, optimization_result: Dict) -> str:
        """模拟优化效果（实际应用中应返回真实优化后的内容）"""
        # 这里只是模拟，实际应用中应该使用optimization技能返回的内容
        return content  # 暂时返回原内容

    def _fallback_analysis(self, content: str) -> Dict:
        """降级分析（当技能不可用时）"""
        # 简单的内容分析
        quality = 0.6

        if len(content) > 10000:
            quality -= 0.1  # 太长扣分
        if 'TODO' in content or 'FIXME' in content:
            quality -= 0.05  # 有待办项扣分
        if '#' in content and '##' in content:
            quality += 0.1  # 有结构加分

        return {
            'quality_score': max(0.0, min(1.0, quality)),
            'clarity': quality,
            'completeness': quality * 0.9,
            'consistency': quality * 0.95
        }

    def _fallback_optimization(self, content: str) -> Dict:
        """降级优化（当技能不可用时）"""
        # 简单优化建议
        return {
            'optimizations': [
                '删除重复内容',
                '统一术语使用',
                '添加结构化标题'
            ]
        }

    def _print_summary(self, result: ImprovementCycleResult):
        """打印改进总结"""
        print(f"\n{'='*60}")
        print("改进循环总结")
        print(f"{'='*60}")
        print(f"上下文: {result.context_id}")
        print(f"循环次数: {result.cycles_completed}/{result.max_cycles}")
        print(f"初始质量: {result.initial_quality_score:.2f}")
        print(f"最终质量: {result.final_quality_score:.2f}")
        print(f"质量提升: +{result.quality_improvement:.2f} ({result.improvement_percentage:.1f}%)")
        print(f"状态: {'✅ 成功' if result.success else '⚠️ 未达标'}")
        print(f"停止原因: {result.stopped_reason}")

        if result.improvement_percentage > 20:
            print(f"\n🎉 优秀！质量显著提升！")
        elif result.improvement_percentage > 10:
            print(f"\n✅ 良好！质量有所提升！")
        elif result.improvement_percentage > 0:
            print(f"\n📈 质量轻微提升，继续努力！")
        else:
            print(f"\n⚠️ 质量未提升，需要人工干预！")

        print(f"{'='*60}\n")


def demo_improvement_cycle():
    """演示改进循环"""
    print("="*60)
    print("上下文改进循环演示")
    print("="*60)

    cycle = ContextImprovementCycle()

    # 模拟一个质量不高的上下文
    poor_context = """
    用户认证系统

    这个系统可以做登录。账号可以做登录。使用者可以登入。
    系统支持多种认证方式：用户名密码、账号密码、使用者名密码。

    待更新功能：
    TODO: 添加OAuth
    FIXME: 修复bug

    这个系统可以注册。这个系统可以注册。这个系统可以注册。

    登录后可以访问系统。登入后可以访问系统。signin后可以访问系统。
    """ * 5

    result = cycle.improve_context(
        context_id='demo-context',
        context_content=poor_context,
        max_cycles=2,
        quality_threshold=0.85
    )

    return result


if __name__ == '__main__':
    demo_improvement_cycle()
