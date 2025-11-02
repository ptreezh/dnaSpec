# DAPIcheck技能使用演示

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, 'src')

def demo_dapi_checker():
    """演示DAPIcheck技能的使用方法"""
    print("=== DAPIcheck技能使用演示 ===\n")
    
    # 导入DAPIcheck技能
    from dsgs_dapi_checker import DSGS_DAPI_Checker
    
    # 创建技能实例
    dapi_checker = DSGS_DAPI_Checker()
    
    print("✓ DAPIcheck技能加载成功")
    print(f"技能名称: {dapi_checker.name}")
    print(f"技能描述: {dapi_checker.description}")
    print(f"技能能力: {dapi_checker.capabilities}")
    print("\n" + "="*60 + "\n")
    
    # 演示不同类型的接口检查请求
    demo_requests = [
        {
            "request": "Check interface consistency for the user management system",
            "description": "用户管理系统接口一致性检查"
        },
        {
            "request": "Verify API documentation and implementation consistency",
            "description": "API文档与实现一致性验证"
        },
        {
            "request": "Analyze system level component interfaces",
            "description": "系统级组件接口分析"
        }
    ]
    
    for i, demo in enumerate(demo_requests, 1):
        print(f"演示 {i}: {demo['description']}")
        print(f"请求: {demo['request']}")
        
        # 处理请求
        result = dapi_checker.process_request(demo['request'])
        
        # 显示结果
        print(f"处理状态: {result['status']}")
        
        # 显示检查结果摘要
        check_result = result['check_result']
        print(f"检查时间: {check_result['scan_time']}")
        print(f"总接口数: {check_result['total_interfaces']}")
        print(f"发现问题数: {len(check_result['issues_found'])}")
        
        # 显示摘要统计
        summary = check_result['summary']
        print(f"合规率: {summary['compliance_rate']:.1f}%")
        print(f"严重问题: {summary['critical_issues']}")
        print(f"高优先级问题: {summary['high_issues']}")
        
        # 显示前几个建议
        if check_result['recommendations']:
            print("改进建议:")
            for rec in check_result['recommendations'][:3]:
                print(f"  - {rec}")
        
        print("-" * 50 + "\n")
    
    # 演示关键点提取功能
    print("=== 关键点提取功能演示 ===")
    test_requests = [
        "Check API interface consistency",
        "Verify system level module interfaces", 
        "Review component documentation"
    ]
    
    for request in test_requests:
        key_points = dapi_checker._extract_key_points(request)
        print(f"请求: {request}")
        print(f"提取的关键点: {key_points}")
        print()
    
    print("=== DAPIcheck技能工作原理解释 ===")
    print("1. 接口扫描: 自动扫描系统中的所有接口定义")
    print("2. 一致性检查: 验证接口实现与文档的一致性")
    print("3. 问题识别: 识别缺失、不匹配、不完整等问题")
    print("4. 报告生成: 生成详细的接口一致性报告")
    print("5. 改进建议: 提供针对性的修复建议")
    print("\nDAPIcheck技能可以帮助:")
    print("- 确保接口实现与文档一致")
    print("- 及早发现接口不一致问题")
    print("- 提高系统组件间的兼容性")
    print("- 维护接口文档的准确性")

if __name__ == "__main__":
    demo_dapi_checker()