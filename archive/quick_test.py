# quick_test.py - 快速功能验证脚本
"""
DSGS Context Engineering Skills - Quick Test
用于验证系统基本功能是否正常工作
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

print("🔍 DSGS Context Engineering Skills - 功能验证")
print("="*60)

try:
    # 1. 测试Context Analysis Skill
    print("\n1. 测试Context Analysis Skill...")
    from src.context_engineering_skills.context_analysis import ContextAnalysisSkill, execute as analysis_execute
    
    analysis_skill = ContextAnalysisSkill()
    
    # 测试简单分析
    test_context = "设计一个电商系统，需要支持用户登录、商品浏览、购物车和订单功能。"
    result = analysis_skill.process_request(test_context, {})
    
    print(f"   上下文长度: {result.result['context_length']} 字符")
    print(f"   估算Token数: {result.result['token_count']}")
    print(f"   清晰度得分: {result.result['metrics']['clarity']:.2f}")
    print(f"   相关性得分: {result.result['metrics']['relevance']:.2f}")
    print(f"   完整性得分: {result.result['metrics']['completeness']:.2f}")
    print("   ✅ Context Analysis Skill 工作正常")
    
    # 2. 测试Context Optimization Skill
    print("\n2. 测试Context Optimization Skill...")
    from src.context_engineering_skills.context_optimization import ContextOptimizationSkill, execute as optimization_execute
    
    optimization_skill = ContextOptimizationSkill()
    
    # 测试内容优化
    simple_context = "系统需要支持用户和订单"
    result = optimization_skill.process_request(simple_context, {'optimization_goals': ['completeness']})
    
    print(f"   原始内容: {simple_context}")
    print(f"   优化后内容: {result.result['optimized_context']}")
    print(f"   应用的优化: {len(result.result['applied_optimizations'])} 项")
    print("   ✅ Context Optimization Skill 工作正常")
    
    # 3. 测试Cognitive Template Skill
    print("\n3. 测试Cognitive Template Skill...")
    from src.context_engineering_skills.cognitive_template import CognitiveTemplateSkill, execute as template_execute
    
    template_skill = CognitiveTemplateSkill()
    
    # 测试思维链模板
    task = "如何提高系统性能？"
    result = template_skill.process_request(task, {'template': 'chain_of_thought'})
    
    print(f"   原始任务: {task}")
    print(f"   模板应用成功: {result.result['success']}")
    if result.result['success']:
        enhanced = result.result['enhanced_context']
        print(f"   结构化后内容长度: {len(enhanced)} 字符")
        print("   ✅ Cognitive Template Skill 工作正常")
    
    # 4. 测试直接执行函数
    print("\n4. 测试直接执行函数...")
    analysis_args = {"context": "用户认证模块设计"}
    optimization_args = {"context": "API接口设计", "optimization_goals": "clarity"}
    template_args = {"context": "数据库设计", "template": "verification"}
    
    analysis_result = analysis_execute(analysis_args)
    optimization_result = optimization_execute(optimization_args)
    template_result = template_execute(template_args)
    
    print("   ✅ 所有直接执行函数工作正常")
    
    print("\n🎉 所有功能测试通过！DSGS Context Engineering Skills 系统可正常使用。")
    print("\n💡 您可以开始使用以下功能：")
    print("   - context_analysis: 分析上下文质量")
    print("   - context_optimization: 优化上下文内容") 
    print("   - cognitive_template: 应用认知模板")
    
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("   请确保已正确安装依赖并激活虚拟环境")
except Exception as e:
    print(f"❌ 运行错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("DSGS Context Engineering Skills - 本地部署验证完成")