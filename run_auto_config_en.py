#!/usr/bin/env python3
"""
DSGS Context Engineering Skills - English Auto Configuration Script
Provides automated detection, configuration, and validation of DSGS in English
"""
from src.dsgs_spec_kit_integration.core.auto_configurator import AutoConfigurator


def main():
    print("🚀 DSGS Context Engineering Skills - Auto Configuration Wizard (English)")
    print("=" * 70)

    # Create auto configurator instance
    auto_config = AutoConfigurator()

    # Run quick configuration
    print("\\nStarting automatic configuration process...")
    result = auto_config.quick_configure()

    if result['success']:
        print("\\n✅ Automatic configuration completed successfully!")
        print(f"Configuration file saved to: {result['configPath']}")
        print(f"Validation report saved to: {result['reportPath']}")

        print("\\n📊 Configuration Status Overview:")
        for platform, validation_result in result['validation'].items():
            status = "✅" if validation_result.get('valid', False) else "❌"
            print(f"  {status} {platform}")

        print("\\nUsage Instructions:")
        print("  Now you can use the following commands in your AI CLI tools:")
        print("  /speckit.dsgs.context-analysis [context] - Analyze context quality")
        print("  /speckit.dsgs.context-optimization [context] - Optimize context")
        print("  /speckit.dsgs.cognitive-template [task] - Apply cognitive template")
        print("  /speckit.dsgs.architect [requirements] - System architecture design")
        print("  ...and other DSGS professional skills")

    else:
        print("\\n❌ Automatic configuration failed")
        if 'error' in result:
            print(f"Error message: {result['error']}")


if __name__ == "__main__":
    main()