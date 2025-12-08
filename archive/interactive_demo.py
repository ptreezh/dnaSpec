# interactive_demo.py - 交互式演示脚本
"""
DNASPEC Context Engineering Skills - 交互式演示
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.context_engineering_skills.context_analysis import ContextAnalysisSkill
from src.context_engineering_skills.context_optimization import ContextOptimizationSkill
from src.context_engineering_skills.cognitive_template import CognitiveTemplateSkill


def demo_context_analysis():
    """演示上下文分析功能"""
    print("\n" + "="*60)
    print("🎯 DNASPEC Context Analysis Demo")
    print("="*60)
    
    skill = ContextAnalysisSkill()
    
    # 示例1：电商系统设计
    sample_context = "设计一个电商平台，支持用户注册登录、商品浏览、购物车、下单支付、订单追踪功能。要求系统高可用，支持10万用户并发。"
    
    print("📝 输入上下文:")
    print(f"   {sample_context[:100]}...")  # 显示前100字符
    
    result = skill.process_request(sample_context, {})
    
    print(f"\n📊 分析结果:")
    print(f"   长度: {result.result['context_length']} 字符")
    print(f"   约 {result.result['token_count']} 个Token")
    print("")
    print("📈 五维指标分析:")
    for metric, score in result.result['metrics'].items():
        metrics_names = {
            'clarity': '清晰度', 
            'relevance': '相关性', 
            'completeness': '完整性', 
            'consistency': '一致性', 
            'efficiency': '效率'
        }
        indicator = "🟢" if score >= 0.7 else "🟡" if score >= 0.4 else "🔴"
        print(f"   {indicator} {metrics_names[metric]}: {score:.2f}")
    
    print("\n💡 优化建议:")
    for suggestion in result.result['suggestions']:
        print(f"   • {suggestion}")
    
    print("\n⚠️  识别问题:")
    if result.result['issues']:
        for issue in result.result['issues']:
            print(f"   • {issue}")
    else:
        print("   • 未发现问题")


def demo_context_optimization():
    """演示上下文优化功能"""
    print("\n" + "="*60)
    print("🚀 DNASPEC Context Optimization Demo")
    print("="*60)
    
    skill = ContextOptimizationSkill()
    
    # 示例：简单任务描述
    simple_context = "系统要能处理用户订单。"
    
    print("📝 原始上下文:")
    print(f"   '{simple_context}'")
    
    # 优化目标：清晰度和完整性
    result = skill.process_request(simple_context, {
        'optimization_goals': ['clarity', 'completeness']
    })
    
    print("\n✨ 优化后上下文:")
    print(f"   '{result.result['optimized_context']}'")
    
    print("\n🔧 应用的优化:")
    for opt in result.result['applied_optimizations']:
        print(f"   • {opt}")
    
    print("\n📈 改进指标:")
    for metric, improvement in result.result['improvement_metrics'].items():
        if improvement != 0:
            direction = "⬆️" if improvement > 0 else "⬇️"
            print(f"   {direction} {metric}: {improvement:+.2f}")


def demo_cognitive_templates():
    """演示认知模板功能"""
    print("\n" + "="*60)
    print("🧠 DNASPEC Cognitive Template Demo")
    print("="*60)
    
    skill = CognitiveTemplateSkill()
    
    # 示例任务
    task = "如何设计一个高并发的用户认证系统？"
    
    print("📝 原始任务:")
    print(f"   {task}")
    
    # 使用思维链模板
    result = skill.process_request(task, {'template': 'chain_of_thought'})
    
    print("\n📋 思维链结构化结果:")
    print(result.result['enhanced_context'][:500] + "..." if len(result.result['enhanced_context']) > 500 else result.result['enhanced_context'])


def interactive_mode():
    """交互模式"""
    print("\n" + "="*60)
    print("🎮 DNASPEC Context Engineering - 交互模式")
    print("="*60)
    print("\n选择功能:")
    print("1. 上下文分析")
    print("2. 上下文优化") 
    print("3. 认知模板应用")
    print("4. 全部功能演示")
    print("q. 退出")
    
    analysis_skill = ContextAnalysisSkill()
    optimization_skill = ContextOptimizationSkill() 
    template_skill = CognitiveTemplateSkill()
    
    while True:
        choice = input("\n请选择 (1-4, q退出): ").strip().lower()
        
        if choice == 'q':
            print("👋 感谢使用DNASPEC Context Engineering Skills!")
            break
        elif choice == '1':
            user_input = input("请输入要分析的上下文: ").strip()
            if user_input:
                result = analysis_skill.process_request(user_input, {})
                print(f"\n📊 分析结果:")
                print(f"长度: {result.result['context_length']} 字符")
                print("指标:", result.result['metrics'])
                print("建议:", result.result['suggestions'][:3])  # 显示前3个建议
        elif choice == '2':
            user_input = input("请输入要优化的上下文: ").strip()
            if user_input:
                goals_input = input("输入优化目标 (clarity,completeness,relevance,conciseness, 默认: clarity,completeness): ").strip()
                goals = [g.strip() for g in goals_input.split(',') if g.strip()] if goals_input else ['clarity', 'completeness']
                result = optimization_skill.process_request(user_input, {'optimization_goals': goals})
                print(f"\n✨ 优化结果:")
                print(f"优化后: {result.result['optimized_context']}")
        elif choice == '3':
            user_input = input("请输入任务描述: ").strip()
            if user_input:
                template = input("选择模板 (chain_of_thought, verification, few_shot, 默认: chain_of_thought): ").strip()
                if not template:
                    template = 'chain_of_thought'
                result = template_skill.process_request(user_input, {'template': template})
                print(f"\n📋 模板应用结果:")
                print(result.result['enhanced_context'][:500] + "..." if len(result.result['enhanced_context']) > 500 else result.result['enhanced_context'])
        elif choice == '4':
            demo_context_analysis()
            demo_context_optimization() 
            demo_cognitive_templates()
        else:
            print("无效选择，请重试。")


def main():
    """主函数"""
    print("🌟 DNASPEC Context Engineering Skills - 本地试用版")
    print("   这个系统可以帮助您分析、优化和结构化AI上下文")
    
    demo_context_analysis()
    demo_context_optimization()
    demo_cognitive_templates()
    
    # 可否进入交互模式
    enter_interactive = input("\n是否进入交互模式体验更多功能？(y/N): ").strip().lower()
    if enter_interactive == 'y':
        interactive_mode()


if __name__ == "__main__":
    main()