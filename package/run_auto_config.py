#!/usr/bin/env python3
"""
DSGS Context Engineering Skills - 自动配置脚本
运行一次安装后的自动检测、配置和验证流程
"""
from src.dsgs_spec_kit_integration.core.auto_configurator import AutoConfigurator


def main():
    print("🚀 DSGS Context Engineering Skills - 自动配置向导")
    print("=" * 60)
    
    # 创建自动配置器实例
    auto_config = AutoConfigurator()
    
    # 运行快速配置
    print("\n开始自动配置流程...")
    result = auto_config.quick_configure()
    
    if result['success']:
        print("\n✅ 自动配置成功完成！")
        print(f"配置文件保存至: {result['configPath']}")
        print(f"验证报告保存至: {result['reportPath']}")
        
        print("\n📊 配置状态概览:")
        for platform, validation_result in result['validation'].items():
            status = "✅" if validation_result.get('valid', False) else "❌"
            print(f"  {status} {platform}")
        
        print("\n使用方法:")
        print("  现在您可以直接在支持的CLI工具中使用以下命令:")
        print("  /speckit.dsgs.context-analysis [上下文] - 分析上下文质量")
        print("  /speckit.dsgs.context-optimization [上下文] - 优化上下文")
        print("  /speckit.dsgs.cognitive-template [任务] - 应用认知模板")
        print("  ...以及其他DSGS技能")
        
    else:
        print("\n❌ 自动配置失败")
        if 'error' in result:
            print(f"错误信息: {result['error']}")


if __name__ == "__main__":
    main()