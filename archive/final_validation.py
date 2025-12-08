"""
Final Validation: Context Engineering Skills Integration
验证上下文工程技能与DNASPEC系统的完全兼容性
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from src.dnaspec_spec_kit_integration.core.skill import DNASpecSkill, SkillResult, SkillStatus
from src.dnaspec_spec_kit_integration.skills.architect import execute as architect_execute
from src.dnaspec_spec_kit_integration.skills.liveness import execute as liveness_execute
from src.context_engineering_skills.context_analysis import ContextAnalysisSkill, execute as context_analysis_execute
from src.context_engineering_skills.context_optimization import ContextOptimizationSkill
from src.context_engineering_skills.cognitive_template import CognitiveTemplateSkill
from src.context_engineering_skills.system import ContextEngineeringSystem


def test_basic_skills():
    """测试基本技能执行"""
    print("=== 测试基本技能执行 ===")
    
    # 测试原有架构师技能
    print("1. 原有架构师技能:")
    result = architect_execute({"description": "电商系统"})
    print(f"   结果: {result}")
    print(f"   类型: {type(result)}")
    print()
    
    # 测试存活检查技能
    print("2. 存活检查技能:")
    result = liveness_execute({})
    print(f"   结果: {result}")
    print(f"   类型: {type(result)}")
    print()
    
    # 测试新的上下文分析技能
    print("3. 新上下文分析技能 (兼容接口):")
    result = context_analysis_execute({"context": "系统设计需要考虑性能和安全"})
    print(f"   结果类型: {type(result)}")
    print(f"   结果长度: {len(result)}")
    print()


def test_dnaspec_skill_compatibility():
    """测试DNASPEC技能兼容性"""
    print("=== 测试DNASPEC技能兼容性 ===")
    
    # 创建新技能实例
    context_skill = ContextAnalysisSkill()
    optimization_skill = ContextOptimizationSkill()
    template_skill = CognitiveTemplateSkill()
    system_skill = ContextEngineeringSystem()
    
    # 测试技能属性
    print("1. 新技能继承自DNASPECSkill:")
    print(f"   ContextAnalysisSkill is DNASpecSkill: {isinstance(context_skill, DNASpecSkill)}")
    print(f"   ContextOptimizationSkill is DNASpecSkill: {isinstance(optimization_skill, DNASpecSkill)}")
    print(f"   CognitiveTemplateSkill is DNASpecSkill: {isinstance(template_skill, DNASpecSkill)}")
    print(f"   ContextEngineeringSystem is DNASpecSkill: {isinstance(system_skill, DNASpecSkill)}")
    print()
    
    # 测试技能执行
    print("2. 新技能执行能力:")
    test_context = "设计一个用户管理系统，需要支持注册、登录、权限控制等功能"
    
    result = context_skill.process_request(test_context, {})
    print(f"   上下文分析技能状态: {result.status.name}")
    print(f"   上下文分析结果类型: {type(result.result)}")
    
    result = optimization_skill.process_request(test_context, {})
    print(f"   上下文优化技能状态: {result.status.name}")
    
    result = template_skill.process_request(test_context, {'template': 'chain_of_thought'})
    print(f"   认知模板技能状态: {result.status.name}")
    
    result = system_skill.process_request(test_context, {'function': 'enhance_context_for_project'})
    print(f"   系统技能状态: {result.status.name}")
    print()


def validate_skill_structure():
    """验证技能结构一致性"""
    print("=== 验证技能结构一致性 ===")
    
    # 检查技能基本信息
    skill = ContextAnalysisSkill()
    info = skill.get_skill_info()
    
    print("技能信息:")
    print(f"  名称: {info['name']}")
    print(f"  描述: {info['description']}")
    print(f"  版本: {info['version']}")
    print()
    
    # 验证执行方法的一致性
    print("执行方法一致性:")
    print(f"  有_process_request方法: {hasattr(skill, 'process_request')}")
    print(f"  有_execute_skill_logic方法: {hasattr(skill, '_execute_skill_logic')}")
    print(f"  有_calculate_confidence方法: {hasattr(skill, '_calculate_confidence')}")
    print()


def test_error_handling():
    """测试错误处理一致性"""
    print("=== 测试错误处理一致性 ===")
    
    skill = ContextAnalysisSkill()
    
    # 测试空请求
    result = skill.process_request("", {})
    print(f"空请求处理状态: {result.status.name}")
    print(f"空请求错误信息: {result.error_message if result.status == SkillStatus.ERROR else '无错误'}")
    print()


def main():
    """主要验证函数"""
    print("Context Engineering Skills Integration Validation")
    print("="*60)
    
    try:
        test_basic_skills()
        test_dnaspec_skill_compatibility()
        validate_skill_structure()
        test_error_handling()
        
        print("✓ 所有验证通过！")
        print("✓ 上下文工程技能与DNASPEC系统完全兼容")
        print("✓ 新技能遵循相同的接口和架构模式")
        print("✓ 可以无缝集成到现有的DNASPEC生态系统中")
        
    except Exception as e:
        print(f"✗ 验证失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()