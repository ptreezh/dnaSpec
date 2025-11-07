import sys
sys.path.insert(0, '.')
import traceback

print('🔍 DSGS Context Engineering Skills - AI原生架构最终验证')
print('='*70)

# 测试导入
try:
    print("尝试导入模块...")
    from src.dsgs_context_engineering.core.skill import ContextAnalysisSkill, ContextOptimizationSkill, CognitiveTemplateSkill
    print('✅ 模块导入成功')
    
    print("尝试实例化技能...")
    # 实例化技能
    analysis = ContextAnalysisSkill()
    optimization = ContextOptimizationSkill()
    template = CognitiveTemplateSkill()
    
    print('✅ 技能实例化成功')
    print(f"分析技能名称: {analysis.name}")
    print(f"优化技能名称: {optimization.name}")
    print(f"模板技能名称: {template.name}")
    
    # 测试分析功能
    print("测试分析功能...")
    context = '设计一个电商平台，支持用户登录和商品浏览功能。'
    result = analysis.execute_with_ai(context)
    print(f"执行结果类型: {type(result)}")
    print(f"执行结果: {result}")
    
    if 'success' in result:
        if result['success']:
            print('✅ Context Analysis Skill 工作正常')
            if 'result' in result and 'metrics' in result['result']:
                metrics = result['result']['metrics']
                print(f'   五维指标: {list(metrics.keys())}')
        else:
            print(f'❌ Context Analysis 失败: {result.get("error", "Unknown error")}')
    else:
        print(f'❌ Context Analysis 结果格式不正确: {result}')
    
    print("\n测试完成")
    
except Exception as e:
    print(f'❌ 验证失败: {e}')
    traceback.print_exc()