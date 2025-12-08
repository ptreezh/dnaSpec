#!/usr/bin/env python3
"""
DNASPEC Context Engineering Skills - Auto Configuration Script
Performs automated detection, configuration, and validation after installation
"""
import sys
import os

# 确保当前目录在Python路径中，以便正确导入模块
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from src.dnaspec_spec_kit_integration.core.auto_configurator import AutoConfigurator


def main():
    print("🚀 DNASPEC Context Engineering Skills - Auto Configuration Wizard")
    print("=" * 60)

    # Create auto configurator instance
    auto_config = AutoConfigurator()

    # Run quick configuration
    print("\nStarting automatic configuration process...")
    result = auto_config.quick_configure()

    if result['success']:
        print("\n✅ Automatic configuration completed successfully!")
        print(f"Configuration file saved to: {result['configPath']}")
        print(f"Validation report saved to: {result['reportPath']}")

        print("\n📊 Configuration Status Overview:")
        for platform, validation_result in result['validation'].items():
            status = "✅" if validation_result.get('valid', False) else "❌"
            print(f"  {status} {platform}")

        print("\nUsage Instructions:")
        print("  Now you can use the following commands in your supported CLI tools:")
        print("  /speckit.dnaspec.context-analysis [context] - Analyze context quality")
        print("  /speckit.dnaspec.context-optimization [context] - Optimize context")
        print("  /speckit.dnaspec.cognitive-template [task] - Apply cognitive template")
        print("  ...and other DNASPEC skills")

    else:
        print("\n❌ Automatic configuration failed")
        if 'error' in result:
            print(f"Error message: {result['error']}")


if __name__ == "__main__":
    main()