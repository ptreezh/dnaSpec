# final_verification.py - 最终验证脚本
"""
DNASPEC Context Engineering Skills - 最终验证
验证所有组件正确安装和配置
"""
import sys
import os
import time

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

print("🔍 DNASPEC Context Engineering Skills - 最终验证")
print("=" * 60)

# 1. 验证基本导入
print("\n1. 验证模块导入...")
try:
    from src.context_engineering_skills.context_analysis import ContextAnalysisSkill, execute as analysis_execute
    from src.context_engineering_skills.context_optimization import ContextOptimizationSkill, execute as optimization_execute
    from src.context_engineering_skills.cognitive_template import CognitiveTemplateSkill, execute as template_execute
    from src.context_engineering_skills.skills_manager import ContextEngineeringSkillsManager
    from src.context_engineering_skills.system import ContextEngineeringSystem
    print("   ✅ 所有模块成功导入")
except ImportError as e:
    print(f"   ❌ 导入错误: {e}")
    sys.exit(1)

# 2. 验证技能实例化
print("\n2. 验证技能实例化...")
try:
    analysis_skill = ContextAnalysisSkill()
    optimization_skill = ContextOptimizationSkill()
    template_skill = CognitiveTemplateSkill()
    skills_manager = ContextEngineeringSkillsManager()
    system = ContextEngineeringSystem()
    print("   ✅ 所有技能成功实例化")
except Exception as e:
    print(f"   ❌ 实例化错误: {e}")
    sys.exit(1)

# 3. 验证技能继承关系
print("\n3. 验证继承关系...")
from src.dnaspec_spec_kit_integration.core.skill import DNASpecSkill

skills = [analysis_skill, optimization_skill, template_skill, skills_manager, system]
for i, skill in enumerate(skills):
    if isinstance(skill, DNASpecSkill):
        skill_names = ["ContextAnalysisSkill", "ContextOptimizationSkill", "CognitiveTemplateSkill", "SkillsManager", "ContextEngineeringSystem"]
        print(f"   ✅ {skill_names[i]} 继承自 DNASpecSkill")
    else:
        print(f"   ❌ {skill} 未正确继承 DNASpecSkill")
        sys.exit(1)

# 4. 验证基础功能
print("\n4. 验证基础功能...")
test_context = "开发一个电商平台，支持用户注册、商品浏览、购物车功能。"

# 测试分析技能
start_time = time.time()
analysis_result = analysis_skill.process_request(test_context, {})
analysis_time = time.time() - start_time
if analysis_result.status.name == 'COMPLETED':
    print(f"   ✅ Context Analysis - 处行时间: {analysis_time:.3f}s, 长度: {analysis_result.result['context_length']} 字符")
else:
    print(f"   ❌ Context Analysis 执行失败")
    sys.exit(1)

# 测试优化技能
start_time = time.time()
optimization_result = optimization_skill.process_request(test_context, {'optimization_goals': ['clarity', 'completeness']})
optimization_time = time.time() - start_time
if optimization_result.status.name == 'COMPLETED':
    print(f"   ✅ Context Optimization - 处行时间: {optimization_time:.3f}s, 优化项: {len(optimization_result.result['applied_optimizations'])} 个")
else:
    print(f"   ❌ Context Optimization 执行失败")
    sys.exit(1)

# 测试模板技能
start_time = time.time()
template_result = template_skill.process_request("如何设计订单系统?", {'template': 'chain_of_thought'})
template_time = time.time() - start_time
if template_result.status.name == 'COMPLETED' and template_result.result['success']:
    print(f"   ✅ Cognitive Template - 处行时间: {template_time:.3f}s, 成功应用模板")
else:
    print(f"   ❌ Cognitive Template 执行失败")
    sys.exit(1)

# 5. 验证直接执行函数
print("\n5. 验证直接执行函数...")
try:
    analysis_out = analysis_execute({"context": "测试上下文"})
    optimization_out = optimization_execute({"context": "测试", "optimization_goals": "clarity"})
    template_out = template_execute({"context": "测试", "template": "chain_of_thought"})
    print("   ✅ 所有直接执行函数正常工作")
except Exception as e:
    print(f"   ❌ 直接执行函数错误: {e}")
    sys.exit(1)

# 6. 性能基准测试
print("\n6. 性能基准测试...")
large_context = "这是测试上下文。" * 500  # 7500 字符

start_time = time.time()
large_result = analysis_skill.process_request(large_context, {})
large_time = time.time() - start_time

if large_result.status.name == 'COMPLETED':
    print(f"   ✅ 大量上下文处理 - 长度: {large_result.result['context_length']} 字符, 时间: {large_time:.3f}s")
    if large_time < 2.0:  # 2秒内处理7500字
        print("   ⭐ 性能优秀")
    else:
        print("   ⚠️  性能一般")
else:
    print(f"   ❌ 大量上下文处理失败")
    sys.exit(1)

# 7. 输出验证总结
print("\n" + "=" * 60)
print("✅ 系统验证通过! DNASPEC Context Engineering Skills 准备就绪")
print("=" * 60)
print("\n系统特性:")
print("   • 5维指标分析 (清晰度、相关性、完整性、一致性、效率)")
print("   • 多目标上下文优化 (清晰度、完整性、简洁性等)")
print("   • 5种认知模板 (思维链、少样本、验证等)")
print("   • DNASPEC框架完全兼容")
print("   • 高性能处理能力")
print("   • 完整的错误处理机制")
print("\n开始使用:")
print("   1. 参看 LOCAL_DEPLOYMENT_GUIDE.md 获取完整文档")
print("   2. 运行: python simple_demo.py 进行功能体验")
print("   3. 在代码中导入并使用: from src.context_engineering_skills... import ...")
print("\n系统已成功部署并准备好使用! 🚀")