"""
Context Engineering Skills Test Suite
测试上下文工程技能的功能
"""
import sys
import os

# 添加项目路径到sys.path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from src.context_engineering_skills.context_analysis import execute as analyze_execute
from src.context_engineering_skills.context_optimization import execute as optimize_execute
from src.context_engineering_skills.cognitive_template import execute as template_execute


def test_context_analysis_skill():
    """测试上下文分析技能"""
    print("=== 测试上下文分析技能 ===")
    
    test_context = "需要设计一个系统，这个系统要能够处理用户的请求，然后给出响应。可能需要考虑性能问题，也许还要考虑安全。"
    
    args = {"context": test_context}
    result = analyze_execute(args)
    
    print("输入上下文:")
    print(test_context)
    print("\n分析结果:")
    print(result)
    print()


def test_context_optimization_skill():
    """测试上下文优化技能"""
    print("=== 测试上下文优化技能 ===")
    
    test_context = "需要设计一个系统，这个系统要能够处理用户的请求，然后给出响应。可能需要考虑性能问题，也许还要考虑安全。"
    
    args = {
        "context": test_context,
        "optimization_goals": "clarity,relevance,completeness"
    }
    result = optimize_execute(args)
    
    print("输入上下文:")
    print(test_context)
    print("\n优化结果:")
    print(result)
    print()


def test_cognitive_template_skill():
    """测试认知模板应用技能"""
    print("=== 测试认知模板应用技能 ===")
    
    test_context = "如何提高系统的安全性？"
    
    # 测试思维链模板
    args = {
        "context": test_context,
        "template": "chain_of_thought"
    }
    result = template_execute(args)
    
    print("输入上下文:")
    print(test_context)
    print("\n应用思维链模板结果:")
    print(result)
    print()
    
    # 测试验证检查模板
    args = {
        "context": test_context,
        "template": "verification"
    }
    result = template_execute(args)
    
    print("应用验证检查模板结果:")
    print(result)
    print()


def main():
    """主要测试函数"""
    print("Context Engineering Skills 测试套件")
    print("=" * 60)
    
    try:
        test_context_analysis_skill()
        test_context_optimization_skill()
        test_cognitive_template_skill()
        
        print("所有测试完成！")
    except ImportError as e:
        print(f"导入错误，请检查文件路径: {e}")
        print("确保在正确的目录下运行此脚本")
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()