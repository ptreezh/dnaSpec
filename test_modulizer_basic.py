"""
Modulizer End-to-End Test
"""

import sys
from pathlib import Path

skills_dir = Path(__file__).parent / "skills" / "dnaspec-modulizer"
sys.path.insert(0, str(skills_dir))

from scripts.executor import ModulizerExecutor

def test_modulizer():
    """测试modulizer"""
    executor = ModulizerExecutor(skills_dir)

    # 测试1: 基本执行
    result = executor.execute("如何将代码组织为模块？")
    print("✅ Test 1 passed: 基本执行")

    # 测试2: 验证
    validation = executor.validator.validate("请帮助设计模块结构")
    print(f"✅ Test 2 passed: 验证通过={validation.is_valid}")

    # 测试3: 计算
    metrics = executor.calculator.calculate("分析模块耦合度")
    print(f"✅ Test 3 passed: 复杂度={metrics.complexity_score}")

    print("\n🎉 Modulizer基础功能测试通过!")

if __name__ == "__main__":
    test_modulizer()
