"""
测试评估框架
"""
import sys
from pathlib import Path

# 添加src到路径
src_dir = Path(__file__).parent / 'src'
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from dna_context_engineering.evaluation import DNASPECEvaluator


def test_evaluator():
    """测试评估器"""
    print("=" * 60)
    print("DNASPEC 评估框架测试")
    print("=" * 60)

    evaluator = DNASPECEvaluator()

    # 测试1: 评估单个技能
    print("\n### 测试1: 评估单个技能 ###")
    result = evaluator.evaluate_skill('dnaspec-git')
    assert result is not None
    assert result.skill_name == 'dnaspec-git'
    print("✅ 单个技能评估测试通过")

    # 测试2: 评估所有技能
    print("\n### 测试2: 评估所有技能 ###")
    results = evaluator.evaluate_all_skills()
    assert len(results) > 0
    print(f"✅ 评估了 {len(results)} 个技能")

    # 测试3: 系统评估
    print("\n### 测试3: 系统评估 ###")
    system_result = evaluator.evaluate_system(generate_report=True)
    assert system_result is not None
    assert system_result.total_skills > 0
    print("✅ 系统评估测试通过")

    print("\n" + "=" * 60)
    print("✅ 所有测试通过！")
    print("=" * 60)


if __name__ == '__main__':
    try:
        test_evaluator()
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
