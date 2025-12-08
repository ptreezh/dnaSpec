#!/usr/bin/env python3
"""
DNASPEC Context Engineering Skills - 集成式自动配置系统
使用改进的CLI检测器进行自动配置
"""
import os
import json
from typing import Dict, Any
from improved_cli_detector import ImprovedCliDetector
from src.dnaspec_spec_kit_integration.core.config_generator import ConfigGenerator
from src.dnaspec_spec_kit_integration.core.integration_validator import IntegrationValidator


class IntegratedAutoConfig:
    """
    集成式自动配置系统
    使用改进的CLI检测器进行更准确的检测和配置
    """
    
    def __init__(self):
        self.detector = ImprovedCliDetector()
        self.config_generator = ConfigGenerator()
        self.validator = IntegrationValidator()
    
    def generate_config(self) -> Dict[str, Any]:
        """
        根据检测结果生成配置
        
        Returns:
            生成的配置字典
        """
        print("🔍 获取CLI工具安装状态...")
        detection_results = self.detector.get_detailed_report()
        
        # 根据检测结果生成配置
        detected_tools = detection_results['detectedTools']
        config = self.config_generator.default_config.copy()
        
        # 根据检测到的工具配置平台
        for platform_name, tool_info in detected_tools.items():
            if tool_info.get('installed', False):
                platform_config = {
                    'name': platform_name,
                    'enabled': True,
                    'version': tool_info.get('version', 'unknown'),
                    'installPath': tool_info.get('installPath', 'unknown'),
                    'configPath': self._get_config_path(platform_name),
                    'skills': self.config_generator._get_platform_skills(platform_name)
                }
                config['platforms'].append(platform_config)
        
        print(f"✅ 为 {len(config['platforms'])} 个平台生成配置")
        return config
    
    def _get_config_path(self, platform_name: str) -> str:
        """
        获取平台特定的配置路径
        
        Args:
            platform_name: 平台名称
            
        Returns:
            配置路径字符串
        """
        import platform
        home = os.path.expanduser("~")
        
        paths = {
            'claude': os.path.join(home, ".config", "claude", "skills"),
            'gemini': os.path.join(home, ".local", "share", "gemini", "extensions"),
            'qwen': os.path.join(home, ".qwen", "plugins"),
            'copilot': os.path.join(home, ".config", "gh-copilot"),
            'cursor': os.path.join(home, ".cursor")
        }
        
        return paths.get(platform_name, os.path.join(home, f".{platform_name}"))
    
    def run_integrated_config(self) -> Dict[str, Any]:
        """
        运行集成的自动配置流程
        
        Returns:
            配置结果字典
        """
        print("🚀 开始集成式自动配置...")
        print("="*60)
        
        # 1. 检测已安装的CLI工具
        print("\n🔍 步骤 1: 检测已安装的AI CLI工具")
        detection_report = self.detector.get_detailed_report()
        
        print("\n检测结果概览:")
        detected_count = detection_report['summary']['installedTools']
        total_count = detection_report['summary']['totalTools']
        
        for name, info in detection_report['detectedTools'].items():
            status = "✅" if info.get('installed', False) else "❌"
            version = info.get('version', 'unknown')
            print(f"  {status} {name}: {version}")
        
        print(f"\n📊 总计: {detected_count}/{total_count} 个工具已安装")
        
        # 2. 生成配置
        print(f"\n⚙️  步骤 2: 为 {detected_count} 个检测到的工具生成配置")
        config = self.generate_config()
        
        # 3. 保存配置
        config_path = './.dnaspec/integrated-config.yaml'
        print(f"💾 步骤 3: 保存配置到 {config_path}")
        
        save_success = self.config_generator.save(config, config_path)
        if not save_success:
            print("❌ 配置保存失败")
            return {
                'success': False,
                'error': 'Failed to save configuration',
                'detection': detection_report
            }
        
        print("✅ 配置保存成功")
        
        # 4. 验证集成
        print(f"\n🧪 步骤 4: 验证 {detected_count} 个平台的集成")
        validation_results = self.validator.validate_all_integrations(config)
        
        # 生成验证报告
        report = self.validator.generate_report(validation_results)
        report_path = './dnaspec-integrated-validation-report.md'
        self.validator.save_report(report, report_path)
        
        print("✅ 集成验证完成")
        
        # 显示验证结果
        print("\n验证结果:")
        for platform, result in validation_results.items():
            status = "✅" if result.get('valid', False) else "❌"
            print(f"  {status} {platform}")
        
        # 5. 显示使用说明
        print(f"\n🎯 步骤 5: 配置完成!")
        print("="*60)
        print("现在您可以在AI CLI工具中使用以下命令:")
        print("  /speckit.dnaspec.context-analysis [上下文] - 分析上下文质量")
        print("  /speckit.dnaspec.context-optimization [上下文] - 优化上下文")
        print("  /speckit.dnaspec.cognitive-template [任务] - 应用认知模板")
        print("  /speckit.dnaspec.architect [需求] - 系统架构设计")
        print("  ...以及其他DSGS专业技能")
        print("="*60)
        
        return {
            'success': True,
            'detection': detection_report,
            'config': config,
            'configPath': config_path,
            'validation': validation_results,
            'reportPath': report_path
        }


def main():
    """主函数"""
    print("DNASPEC Context Engineering Skills - 集成式自动配置系统")
    print("使用npm包管理器进行精准CLI工具检测")
    
    config_system = IntegratedAutoConfig()
    result = config_system.run_integrated_config()
    
    if result['success']:
        print("\n🎉 集成配置成功完成！")
        print(f"配置文件: {result['configPath']}")
        print(f"验证报告: {result['reportPath']}")
    else:
        print(f"\n❌ 配置失败: {result.get('error', 'Unknown error')}")
    
    return result['success']


if __name__ == "__main__":
    main()