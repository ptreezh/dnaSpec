#!/usr/bin/env python3
"""
验证 dnaspec init 和 deploy 命令的功能区别
"""
from src.dsgs_spec_kit_integration.core.auto_configurator import AutoConfigurator
from src.dsgs_spec_kit_integration.core.cli_detector import CliDetector
from src.dsgs_context_engineering.skills_system_final import execute as skill_execute

def simulate_init_behavior():
    """
    模拟 init 命令的行为 - 完整初始化
    """
    print("🔄 模拟 dnaspec init 命令行为:")
    print("1. 检查环境依赖...")
    print("2. 安装DSGS Python包...")
    print("3. 检测AI CLI工具...")
    print("4. 生成全面配置...")
    print("5. 验证所有集成...")
    
    # 实际执行完整配置过程
    auto_config = AutoConfigurator()
    result = auto_config.quick_configure()
    
    print(f"6. 完成状态: {'✅' if result.get('success', False) else '❌'}")
    print()

def simulate_deploy_behavior():
    """
    模拟 deploy 命令行为 - 仅部署技能
    """
    print("🔄 模拟 dnaspec deploy 命令行为:")
    print("1. 重用已安装的DSGS包...")
    print("2. 检测AI CLI工具...")
    print("3. 部署技能到AI工具...")
    print("4. 创建AI CLI扩展...")
    
    # 检测已安装的工具
    detector = CliDetector()
    detected_tools = detector.detect_all()
    
    print(f"5. 已检测到的工具数量: {sum(1 for info in detected_tools.values() if info.get('installed', False))}")
    print("6. 部署状态: 根据已检测工具进行部署")
    print()

def compare_commands():
    """
    比较两个命令的主要区别
    """
    print("="*70)
    print("📋 dnaspec init vs dnaspec deploy 功能对比")
    print("="*70)
    
    comparison = {
        "Command": ["dnaspec init", "dnaspec deploy"],
        "Purpose": ["Complete installation and initialization", "Deploy skills to AI CLI tools"],
        "Includes Python Package Install": ["✅ Yes", "❌ No (assumes already installed)"],
        "Includes Dependency Check": ["✅ Yes", "⚠️ Only if needed"],
        "AI Tool Detection": ["✅ Full detection", "✅ Full detection"], 
        "Configuration Generation": ["✅ Complete config", "✅ Updates existing config"],
        "Skill Deployment": ["✅ Yes (as part of init)", "✅ Focus on skill deployment"],
        "Execution Speed": ["Slower (full process)", "Faster (lightweight)"],
        "When to Use": [
            "First installation, full reset, fresh setup",
            "New AI tool installed, skill update, maintenance"
        ]
    }
    
    # 打印对比表格
    for key, values in comparison.items():
        print(f"{key:.<25} {values[0]:<35} {values[1]}")
    
    print()
    print("🎯 建议使用场景:")
    print("  dnaspec init    : 首次安装或需要完全重置系统时")
    print("  dnaspec deploy  : 日常使用，当AI工具环境变化时")
    print()
    
    print("🔗 内部关系:")
    print("  dnaspec init → 完整安装流程 (包括deploy的操作)")
    print("  dnaspec deploy → 轻量级部署操作 (不包括安装)")

if __name__ == "__main__":
    simulate_deploy_behavior()  # deploy命令更快，先验证
    simulate_init_behavior()    # init命令较慢，后验证
    compare_commands()