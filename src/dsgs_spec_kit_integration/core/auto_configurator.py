"""
自动配置器模块
自动检测、配置和验证DSGS与AI CLI工具的集成
"""
import os
from typing import Dict, Any, Optional
from .cli_detector import CliDetector
from .config_generator import ConfigGenerator
from .integration_validator import IntegrationValidator
from .skill_executor import SkillExecutor


class AutoConfigurator:
    """
    DSGS自动配置器
    自动检测、配置和验证DSGS与AI CLI工具的集成
    """
    
    def __init__(
        self, 
        cli_detector: CliDetector = None, 
        config_generator: ConfigGenerator = None, 
        validator: IntegrationValidator = None
    ):
        """
        初始化自动配置器
        
        Args:
            cli_detector: CLI检测器实例
            config_generator: 配置生成器实例
            validator: 集成验证器实例
        """
        self.cli_detector = cli_detector or CliDetector()
        self.config_generator = config_generator or ConfigGenerator()
        self.validator = validator or IntegrationValidator()
    
    def auto_configure(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        执行自动配置
        
        Args:
            options: 配置选项字典
            
        Returns:
            配置结果字典
        """
        if options is None:
            options = {}
        
        print('🚀 Starting automatic configuration...')
        
        # 1. 检测已安装的CLI工具
        print('🔍 Detecting installed AI CLI tools...')
        detected_tools = self.cli_detector.detect_all()
        self._print_detection_results(detected_tools)
        
        # 2. 生成配置文件
        print('⚙️  Generating configuration...')
        config = self.config_generator.generate(detected_tools)
        
        # 3. 保存配置文件
        config_path = options.get('configPath', './.dsgs/config.yaml')
        print(f'💾 Saving configuration to {config_path}...')
        save_result = self.config_generator.save(config, config_path)
        
        if not save_result:
            raise Exception('Failed to save configuration')
        
        print('✅ Configuration saved successfully!')
        
        # 4. 验证集成（如果未禁用）
        if options.get('validate', True):
            print('🧪 Validating integrations...')
            validation_results = self.validator.validate_all_integrations(config)
            
            # 生成验证报告
            report = self.validator.generate_report(validation_results)
            report_path = options.get('reportPath', './dsgs-validation-report.md')
            self.validator.save_report(report, report_path)
            
            self._print_validation_results(validation_results)
            
            return {
                'success': True,
                'config': config,
                'configPath': config_path,
                'validation': validation_results,
                'reportPath': report_path
            }
        
        return {
            'success': True,
            'config': config,
            'configPath': config_path
        }
    
    def _print_detection_results(self, detected_tools: Dict[str, Any]):
        """
        打印检测结果
        
        Args:
            detected_tools: 检测结果字典
        """
        print('\nDetection Results:')
        for name, info in detected_tools.items():
            if info.get('installed', False):
                version = info.get('version', 'unknown')
                print(f'  ✅ {name}: {version}')
            else:
                print(f'  ❌ {name}: Not installed')
        print()
    
    def _print_validation_results(self, validation_results: Dict[str, Any]):
        """
        打印验证结果
        
        Args:
            validation_results: 验证结果字典
        """
        print('\nValidation Results:')
        for platform, result in validation_results.items():
            if result.get('valid', False):
                print(f'  ✅ {platform}: Valid')
            else:
                error = result.get('error', 'Unknown error')
                print(f'  ❌ {platform}: {error}')
        print()
    
    def interactive_configure(self) -> Dict[str, Any]:
        """
        执行交互式配置
        
        Returns:
            配置结果字典
        """
        print('🧙 Welcome to DSGS Interactive Configuration Wizard\n')
        
        # 检测工具
        print('🔍 Detecting AI CLI tools...')
        detected_tools = self.cli_detector.detect_all()
        self._print_detection_results(detected_tools)
        
        # 获取用户输入
        try:
            config_path = input(f'Configuration file path (default: ./.dsgs/config.yaml): ').strip()
            if not config_path:
                config_path = './.dsgs/config.yaml'
            
            validate_input = input('Run integration validation after configuration? (Y/n): ').strip().lower()
            validate = validate_input != 'n'
            
            # 执行配置
            return self.auto_configure({
                'configPath': config_path,
                'validate': validate
            })
        except KeyboardInterrupt:
            print('\nConfiguration cancelled by user.')
            return {'success': False, 'cancelled': True}
    
    def quick_configure(self) -> Dict[str, Any]:
        """
        执行快速配置（使用默认选项）
        
        Returns:
            配置结果字典
        """
        return self.auto_configure({
            'configPath': './.dsgs/config.yaml',
            'validate': True
        })
    
    def update_configuration(self, existing_config_path: str, new_options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        更新现有配置
        
        Args:
            existing_config_path: 现有配置文件路径
            new_options: 新的配置选项
            
        Returns:
            更新结果字典
        """
        if new_options is None:
            new_options = {}
        
        # 加载现有配置
        existing_config = self.config_generator.load(existing_config_path)
        if not existing_config:
            print(f'Existing config not found at {existing_config_path}, creating new config...')
            return self.auto_configure(new_options)
        
        # 检测新安装的工具
        print('🔍 Detecting newly installed AI CLI tools...')
        detected_tools = self.cli_detector.detect_all()
        self._print_detection_results(detected_tools)
        
        # 生成更新后的配置
        updated_config = self.config_generator.generate(detected_tools)
        
        # 保存更新后的配置
        config_path = new_options.get('configPath', existing_config_path)
        print(f'💾 Updating configuration at {config_path}...')
        save_result = self.config_generator.save(updated_config, config_path)
        
        if not save_result:
            raise Exception('Failed to save updated configuration')
        
        print('✅ Configuration updated successfully!')
        
        # 验证集成
        if new_options.get('validate', True):
            print('🧪 Validating integrations...')
            validation_results = self.validator.validate_all_integrations(updated_config)
            
            # 生成验证报告
            report = self.validator.generate_report(validation_results)
            report_path = new_options.get('reportPath', './dsgs-validation-report.md')
            self.validator.save_report(report, report_path)
            
            self._print_validation_results(validation_results)
            
            return {
                'success': True,
                'config': updated_config,
                'configPath': config_path,
                'validation': validation_results,
                'reportPath': report_path
            }
        
        return {
            'success': True,
            'config': updated_config,
            'configPath': config_path
        }
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取当前配置状态
        
        Returns:
            配置状态字典
        """
        # 检测当前安装的工具
        detected_tools = self.cli_detector.detect_all()
        
        # 统计安装的工具
        installed_count = sum(1 for info in detected_tools.values() if info.get('installed', False))
        total_count = len(detected_tools)
        
        return {
            'detectedTools': detected_tools,
            'installedCount': installed_count,
            'totalCount': total_count,
            'installedTools': [name for name, info in detected_tools.items() if info.get('installed', False)],
            'timestamp': self._get_timestamp()
        }
    
    def _get_timestamp(self) -> str:
        """
        获取当前时间戳
        
        Returns:
            ISO格式时间戳字符串
        """
        import datetime
        return datetime.datetime.now().isoformat()