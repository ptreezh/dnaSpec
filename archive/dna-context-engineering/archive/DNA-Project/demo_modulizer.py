# 模块化技能使用演示

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, 'src')

def demo_modulizer():
    """演示模块化技能的使用方法"""
    print("=== 模块化技能使用演示 ===\n")
    
    # 导入模块化技能
    from dnaspec_modulizer import DNASPEC_Modulizer
    
    # 创建技能实例
    modulizer = DNASPEC_Modulizer()
    
    print("✓ 模块化技能加载成功")
    print(f"技能名称: {modulizer.name}")
    print(f"技能描述: {modulizer.description}")
    print(f"技能能力: {modulizer.capabilities}")
    print("\n" + "="*60 + "\n")
    
    # 演示不同类型的模块化请求
    demo_requests = [
        {
            "request": "Analyze system components maturity and identify sealable modules",
            "description": "系统组件成熟度分析"
        },
        {
            "request": "Perform bottom-up modularization for the e-commerce platform",
            "description": "电商系统自底向上模块化"
        },
        {
            "request": "Check module maturity and generate modularization recommendations",
            "description": "模块成熟度检查和建议"
        }
    ]
    
    for i, demo in enumerate(demo_requests, 1):
        print(f"演示 {i}: {demo['description']}")
        print(f"请求: {demo['request']}")
        
        # 处理请求
        result = modulizer.process_request(demo['request'])
        
        # 显示结果
        print(f"处理状态: {result['status']}")
        
        # 显示模块化结果摘要
        modularization_result = result['modularization_result']
        print(f"分析时间: {modularization_result['assessment_time']}")
        print(f"分析组件数: {len(modularization_result['components_analyzed'])}")
        print(f"可封装组件数: {len(modularization_result['sealable_components'])}")
        
        # 显示成熟度评估
        if modularization_result['maturity_assessments']:
            print("成熟度评估:")
            for assessment in modularization_result['maturity_assessments'][:2]:  # 显示前2个
                print(f"  - {assessment['component_name']}: {assessment['current_level'].value}")
                print(f"    评估分数: {assessment['assessment_score']:.2f}")
                if assessment['can_be_sealed']:
                    print(f"    ✓ 可以封装")
        
        # 显示风险分析
        risk_analysis = modularization_result['risk_analysis']
        print(f"成熟度比率: {risk_analysis['maturity_rate']:.2f}")
        print(f"封装比率: {risk_analysis['sealing_rate']:.2f}")
        
        # 显示前几个建议
        if modularization_result['recommendations']:
            print("改进建议:")
            for rec in modularization_result['recommendations'][:3]:
                print(f"  - {rec}")
        
        print("-" * 50 + "\n")
    
    # 演示关键点提取功能
    print("=== 关键点提取功能演示 ===")
    test_requests = [
        "Check module maturity and sealing",
        "Analyze component level systems",
        "Perform bottom-up modularization"
    ]
    
    for request in test_requests:
        key_points = modulizer._extract_key_points(request)
        print(f"请求: {request}")
        print(f"提取的关键点: {key_points}")
        print()
    
    print("=== 模块化技能工作原理解释 ===")
    print("1. 自底向上分析: 从最底层组件开始，逐层向上进行模块化")
    print("2. 成熟度评估: 基于测试覆盖率、性能、安全等标准评估组件成熟度")
    print("3. 组件封装: 对成熟的组件进行封装，确保后续不被修改")
    print("4. 风险分析: 识别模块化过程中的潜在风险")
    print("5. 建议生成: 提供针对性的模块化改进建议")
    print("\n模块化技能可以帮助:")
    print("- 降低系统复杂性")
    print("- 提高组件复用性")
    print("- 确保系统稳定性")
    print("- 优化开发流程")

if __name__ == "__main__":
    demo_modulizer()
