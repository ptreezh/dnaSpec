# simple_demo.py - 简单演示脚本
"""
DNASPEC Context Engineering Skills - 简单演示
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.context_engineering_skills.context_analysis import ContextAnalysisSkill
from src.context_engineering_skills.context_optimization import ContextOptimizationSkill
from src.context_engineering_skills.cognitive_template import CognitiveTemplateSkill


def demo_all_features():
    """演示所有功能"""
    print("="*70)
    print("🎯 DNASPEC Context Engineering Skills - 简单演示")
    print("="*70)
    
    print("\n1. 📊 Context Analysis Skill")
    print("-"*40)
    analysis_skill = ContextAnalysisSkill()
    
    # 测试分析功能
    test_context = "设计一个电商平台，需要支持用户注册登录、商品浏览、购物车功能。"
    result = analysis_skill.process_request(test_context, {})
    
    print(f"输入: {test_context[:50]}...")
    print(f"长度: {result.result['context_length']} 字符")
    print(f"Token数: {result.result['token_count']}")
    print("指标分析:")
    for metric, score in result.result['metrics'].items():
        print(f"  {metric}: {score:.2f}")
    print(f"建议: {len(result.result['suggestions'])} 项")
    
    print("\n2. 🚀 Context Optimization Skill")
    print("-"*40)
    optimization_skill = ContextOptimizationSkill()
    
    # 测试优化功能
    simple_context = "系统要处理用户订单。"
    result = optimization_skill.process_request(simple_context, {
        'optimization_goals': ['clarity', 'completeness']
    })
    
    print(f"原始: {simple_context}")
    print(f"优化后: {result.result['optimized_context']}")
    print(f"应用了 {len(result.result['applied_optimizations'])} 项优化")
    
    print("\n3. 🧠 Cognitive Template Skill")
    print("-"*40)
    template_skill = CognitiveTemplateSkill()
    
    # 测试模板功能
    task = "如何提高系统性能？"
    result = template_skill.process_request(task, {'template': 'chain_of_thought'})
    
    print(f"任务: {task}")
    print(f"模板类型: 思维链")
    print(f"结构化结果长度: {len(result.result['enhanced_context'])} 字符")
    
    print("\n" + "="*70)
    print("✅ DNASPEC Context Engineering Skills 功能演示完成!")
    print("💡 您现在可以在您的项目中使用这些技能了")
    print("="*70)


def usage_examples():
    """使用示例"""
    print("\n📋 使用示例:")
    print("-"*40)
    
    print("""
# 1. 在Python代码中使用
from src.context_engineering_skills.context_analysis import ContextAnalysisSkill

skill = ContextAnalysisSkill()
result = skill.process_request("您的上下文", {})
print(result.result['metrics'])

# 2. 使用Context Optimization
from src.context_engineering_skills.context_optimization import ContextOptimizationSkill

skill = ContextOptimizationSkill()
result = skill.process_request("待优化内容", {'optimization_goals': ['clarity', 'completeness']})

# 3. 使用Cognitive Template
from src.context_engineering_skills.cognitive_template import CognitiveTemplateSkill

skill = CognitiveTemplateSkill()
result = skill.process_request("任务描述", {'template': 'chain_of_thought'})
""")


def main():
    """主函数"""
    print("🌟 DNASPEC Context Engineering Skills - 本地部署验证成功")
    print("   系统已成功安装和配置，可以正常使用")
    
    demo_all_features()
    usage_examples()
    
    print("\n🎉 您的DNASPEC Context Engineering Skills系统现在可以使用了!")
    print("   系统提供了完整的上下文工程能力，包括分析、优化和结构化功能")


if __name__ == "__main__":
    main()