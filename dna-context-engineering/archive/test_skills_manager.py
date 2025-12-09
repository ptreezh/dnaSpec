"""
Context Engineering Skills Manager Test
测试技能管理器功能
"""
import sys
import os

# 添加项目路径到sys.path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from src.context_engineering_skills.skills_manager import ContextEngineeringSkillsManager, execute
from src.context_engineering_skills.context_analysis import ContextAnalysisSkill
from src.context_engineering_skills.context_optimization import ContextOptimizationSkill
from src.context_engineering_skills.cognitive_template import CognitiveTemplateSkill


def test_skills_manager():
    """测试技能管理器"""
    print("=== 测试技能管理器 ===")
    
    # 测试各个DNASPEC技能
    print("1. 测试上下文分析技能 (DNASPEC模式):")
    analysis_skill = ContextAnalysisSkill()
    result = analysis_skill.process_request(
        "设计一个电商平台的用户认证系统，需要支持多种登录方式，并确保安全性和用户体验。",
        {}
    )
    if result.status.name == 'COMPLETED':
        analysis = result.result
        print(f"   长度: {analysis['context_length']} 字符")
        print(f"   清晰度: {analysis['metrics']['clarity']:.2f}")
        print(f"   完整性: {analysis['metrics']['completeness']:.2f}")
    else:
        print(f"   错误: {result.error_message}")
    print()
    
    print("2. 测试上下文优化技能 (DNASPEC模式):")
    optimization_skill = ContextOptimizationSkill()
    result = optimization_skill.process_request(
        "开发一个任务管理系统，包含任务创建、分配、跟踪和报告功能。",
        {'optimization_goals': 'clarity,relevance,completeness'}
    )
    if result.status.name == 'COMPLETED':
        optimization = result.result
        print(f"   优化改进: 完整性 +{optimization['improvement_metrics']['completeness']:.2f}")
    else:
        print(f"   错误: {result.error_message}")
    print()
    
    print("3. 测试认知模板技能 (DNASPEC模式):")
    template_skill = CognitiveTemplateSkill()
    result = template_skill.process_request(
        "如何提高系统的安全性？",
        {'template': 'chain_of_thought'}
    )
    if result.status.name == 'COMPLETED':
        print("   模板应用成功")
    else:
        print(f"   错误: {result.error_message}")
    print()


def test_direct_execute():
    """测试直接执行函数"""
    print("=== 测试直接执行函数 ===")
    
    context = "开发一个任务管理系统，包含任务创建、分配、跟踪和报告功能。"
    
    # 测试上下文分析
    print("1. 直接执行上下文分析:")
    args = {'context': context}
    result = execute(args)
    print(f"   结果长度: {len(result)} 字符")
    print()
    
    print("所有测试完成！")


def main():
    """主要测试函数"""
    print("Context Engineering Skills Manager 测试")
    print("=" * 60)
    
    try:
        test_skills_manager()
        test_direct_execute()
        
        print("所有测试完成！")
    except Exception as e:
        print(f"测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()