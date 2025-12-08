#!/usr/bin/env python3
"""
DNASPEC Context Engineering Skills - 独立配置入口点
用于在任何环境中运行自动配置
"""
import sys
import os
import importlib.util

def run_standalone_config():
    """
    在独立环境中运行配置
    避免在项目目录中运行时的环境冲突
    """
    print("🚀 DNASPEC Context Engineering Skills - 独立配置向导")
    print("=" * 60)

    try:
        # 获取当前脚本目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 优先从当前脚本目录的src目录导入，而不是项目目录
        standalone_src_path = os.path.join(script_dir, 'src')
        
        # 临时添加到模块路径
        sys.path.insert(0, standalone_src_path)
        
        # 现在导入DNASPEC模块（使用独立的版本，而不是本地开发版本）
        from dnaspec_spec_kit_integration.core.auto_configurator import AutoConfigurator

        print("\n开始自动配置流程...")
        print("🚀 Starting automatic configuration...")
        print("🔍 Detecting installed AI CLI tools...")

        # 创建自动配置器实例
        auto_config = AutoConfigurator()

        # 运行快速配置
        result = auto_config.quick_configure()

        if result['success']:
            print("\n✅ 自动配置成功完成！")
            print(f"配置文件保存至: {result['configPath']}")
            print(f"验证报告保存至: {result['reportPath']}")

            print("\n📊 配置状态概览:")
            for platform, validation_result in result.get('validation', {}).items():
                status = "✅" if validation_result.get('valid', False) else "❌"
                print(f"  {status} {platform}")

            print("\n使用方法:")
            print("  现在您可以在支持的CLI工具中使用以下命令:")
            print("  /speckit.dnaspec.context-analysis [上下文] - 分析上下文质量")
            print("  /speckit.dnaspec.context-optimization [上下文] - 优化上下文")
            print("  /speckit.dnaspec.cognitive-template [任务] - 应用认知模板")
            print("  ...以及其他DNASPEC技能")
        else:
            print("\n❌ 自动配置失败")
            if 'error' in result:
                print(f"错误信息: {result['error']}")

    except ImportError as e:
        print(f"❌ 导入DNASPEC模块失败: {e}")
        print("这可能是因为DNASPEC包未正确安装，请尝试重新安装:")
        print("  pip install -e .")
    except Exception as e:
        print(f"❌ 配置过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_standalone_config()