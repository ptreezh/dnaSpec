"""
DNASPEC spec.kit集成演示脚本
演示整个系统的功能
"""
from src.dnaspec_spec_kit_integration.core.command_parser import CommandParser
from src.dnaspec_spec_kit_integration.core.skill_mapper import SkillMapper
from src.dnaspec_spec_kit_integration.core.python_bridge import PythonBridge
from src.dnaspec_spec_kit_integration.core.skill_executor import SkillExecutor
from src.dnaspec_spec_kit_integration.core.command_handler import CommandHandler
from src.dnaspec_spec_kit_integration.core.interactive_shell import InteractiveShell
from src.dnaspec_spec_kit_integration.core.cli_detector import CliDetector
from src.dnaspec_spec_kit_integration.core.config_generator import ConfigGenerator
from src.dnaspec_spec_kit_integration.core.integration_validator import IntegrationValidator
from src.dnaspec_spec_kit_integration.core.auto_configurator import AutoConfigurator
import tempfile
import os


def demo_command_parsing():
    """
    演示命令解析功能
    """
    print("=== 命令解析演示 ===")
    parser = CommandParser()
    
    # 测试有效命令
    result = parser.parse('/speckit.dnaspec.architect 设计电商系统')
    print(f"解析结果: {result}")
    
    # 测试无效命令
    result = parser.parse('/invalid.command')
    print(f"无效命令解析结果: {result}")
    print()


def demo_skill_execution():
    """
    演示技能执行功能
    """
    print("=== 技能执行演示 ===")
    skill_executor = SkillExecutor()
    
    # 执行架构师技能
    result = skill_executor.execute('architect', '电商系统')
    print(f"技能执行结果: {result}")
    
    # 执行博客技能
    result = skill_executor.execute('architect', '个人博客')
    print(f"博客技能执行结果: {result}")
    print()


def demo_command_handling():
    """
    演示完整命令处理流程
    """
    print("=== 完整命令处理演示 ===")
    command_handler = CommandHandler()
    
    # 处理完整命令
    result = command_handler.handle_command('/speckit.dnaspec.architect 电商系统')
    print(f"命令处理结果: {result}")
    
    result = command_handler.handle_command('/speckit.dnaspec.architect 博客系统')
    print(f"博客命令处理结果: {result}")
    print()


def demo_cli_detection():
    """
    演示CLI检测功能
    """
    print("=== CLI检测演示 ===")
    detector = CliDetector()
    
    # 检测所有CLI工具
    results = detector.detect_all()
    print("检测结果:")
    for name, info in results.items():
        if info.get('installed', False):
            print(f"  ✅ {name}: {info.get('version', 'unknown')}")
        else:
            print(f"  ❌ {name}: Not installed ({info.get('error', 'No error info')})")
    print()


def demo_configuration():
    """
    演示配置生成功能
    """
    print("=== 配置生成演示 ===")
    detector = CliDetector()
    config_gen = ConfigGenerator()
    
    # 检测工具并生成配置
    detected_tools = detector.detect_all()
    config = config_gen.generate(detected_tools)
    
    print(f"生成的配置包含 {len(config['platforms'])} 个平台")
    print(f"可用技能数: {len(config['skills'])}")
    
    # 临时保存配置
    temp_file = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            temp_file = f.name
            config_gen.save(config, temp_file)
            print(f"配置已保存到: {temp_file}")
            
            # 读取并验证配置
            loaded_config = config_gen.load(temp_file)
            validation_result = config_gen.validate(loaded_config)
            print(f"配置验证结果: {validation_result}")
    finally:
        # 确保临时文件被清理
        if temp_file and os.path.exists(temp_file):
            try:
                os.unlink(temp_file)
            except PermissionError:
                # 在Windows上，有时无法立即删除文件
                print(f"注意: 无法立即删除临时文件 {temp_file}")
    print()


def demo_validation():
    """
    演示集成验证功能
    """
    print("=== 集成验证演示 ===")
    detector = CliDetector()
    config_gen = ConfigGenerator()
    skill_executor = SkillExecutor()
    validator = IntegrationValidator(skill_executor)
    
    # 生成模拟配置
    detected_tools = detector.detect_all()
    config = config_gen.generate(detected_tools)
    
    # 运行性能测试
    perf_result = validator.run_performance_test(3)  # 只运行3次迭代
    print(f"性能测试结果: {perf_result['successRate']*100}% 成功率, 平均响应时间 {perf_result['averageResponseTime']}ms")
    
    # 生成验证报告
    validation_results = validator.validate_all_integrations(config)
    report = validator.generate_report(validation_results)
    print("验证报告预览 (前200字符):")
    print(report[:200] + "..." if len(report) > 200 else report)
    print()


def demo_auto_configuration():
    """
    演示自动配置功能
    """
    print("=== 自动配置演示 ===")
    auto_config = AutoConfigurator()
    
    # 获取当前状态
    status = auto_config.get_status()
    print(f"检测到 {status['installedCount']}/{status['totalCount']} 个已安装的工具")
    print(f"已安装工具: {status['installedTools']}")
    
    # 运行快速配置（不实际保存文件）
    print("运行快速配置测试...")
    try:
        # 仅测试配置逻辑，不实际保存文件
        detected_tools = auto_config.cli_detector.detect_all()
        config = auto_config.config_generator.generate(detected_tools)
        print(f"配置生成成功，包含 {len(config['platforms'])} 个平台")
    except Exception as e:
        print(f"配置过程中出现错误: {e}")
    print()


def main():
    """
    主函数 - 运行所有演示
    """
    print("DNASPEC spec.kit 集成系统演示")
    print("=" * 50)
    
    demo_command_parsing()
    demo_skill_execution()
    demo_command_handling()
    demo_cli_detection()
    demo_configuration()
    demo_validation()
    demo_auto_configuration()
    
    print("演示完成！")
    print("\n要启动交互式Shell，请运行: python -c \"from src.dnaspec_spec_kit_integration.core.interactive_shell import InteractiveShell; from src.dnaspec_spec_kit_integration.core.command_handler import CommandHandler; shell = InteractiveShell(CommandHandler()); shell.start()\"")


if __name__ == "__main__":
    main()