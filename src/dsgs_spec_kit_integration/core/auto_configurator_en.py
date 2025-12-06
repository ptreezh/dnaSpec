"""
Auto Configurator Module
Automatically detects, configures, and validates DSGS and AI CLI tool integration
"""
import os
from typing import Dict, Any, Optional
from .cli_detector import CliDetector
from .config_generator import ConfigGenerator
from .integration_validator import IntegrationValidator
from .skill_executor import SkillExecutor


class AutoConfigurator:
    """
    DSGS Auto Configurator
    Automatically detects, configures, and validates DSGS and AI CLI tool integration
    """

    def __init__(
        self,
        cli_detector: CliDetector = None,
        config_generator: ConfigGenerator = None,
        validator: IntegrationValidator = None
    ):
        """
        Initialize the auto configurator

        Args:
            cli_detector: CLI detector instance
            config_generator: Config generator instance
            validator: Integration validator instance
        """
        self.cli_detector = cli_detector or CliDetector()
        self.config_generator = config_generator or ConfigGenerator()
        self.validator = validator or IntegrationValidator()

    def auto_configure(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform auto configuration

        Args:
            options: Configuration options dictionary

        Returns:
            Configuration result dictionary
        """
        if options is None:
            options = {}

        print('Starting automatic configuration...')

        # 1. Detect installed CLI tools
        print('Detecting installed AI CLI tools...')
        detected_tools = self.cli_detector.detect_all()
        self._print_detection_results(detected_tools)

        # 2. Generate configuration file
        print('Generating configuration...')
        config = self.config_generator.generate(detected_tools)

        # 3. Save configuration file
        config_path = options.get('configPath', './.dsgs/config.yaml')
        print(f'Saving configuration to {config_path}...')
        save_result = self.config_generator.save(config, config_path)

        if not save_result:
            raise Exception('Failed to save configuration')

        print('Configuration saved successfully!')

        # 4. Validate integration (if not disabled)
        if options.get('validate', True):
            print('Validating integrations...')
            validation_results = self.validator.validate_all_integrations(config)

            # Generate validation report
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
        Print detection results

        Args:
            detected_tools: Detection results dictionary
        """
        print('\\nDetection Results:')
        for name, info in detected_tools.items():
            if info.get('installed', False):
                version = info.get('version', 'unknown')
                print(f'  OK {name}: {version}')
            else:
                print(f'  FAIL {name}: Not installed')
        print()

    def _print_validation_results(self, validation_results: Dict[str, Any]):
        """
        Print validation results

        Args:
            validation_results: Validation results dictionary
        """
        print('\\nValidation Results:')
        for platform, result in validation_results.items():
            if result.get('valid', False):
                print(f'  OK {platform}: Valid')
            else:
                error = result.get('error', 'Unknown error')
                print(f'  FAIL {platform}: {error}')
        print()

    def interactive_configure(self) -> Dict[str, Any]:
        """
        Perform interactive configuration

        Returns:
            Configuration result dictionary
        """
        print('Welcome to DSGS Interactive Configuration Wizard\\n')

        # Detect tools
        print('Detecting AI CLI tools...')
        detected_tools = self.cli_detector.detect_all()
        self._print_detection_results(detected_tools)

        # Get user input
        try:
            config_path = input(f'Configuration file path (default: ./.dsgs/config.yaml): ').strip()
            if not config_path:
                config_path = './.dsgs/config.yaml'

            validate_input = input('Run integration validation after configuration? (Y/n): ').strip().lower()
            validate = validate_input != 'n'

            # Execute configuration
            return self.auto_configure({
                'configPath': config_path,
                'validate': validate
            })
        except KeyboardInterrupt:
            print('\\nConfiguration cancelled by user.')
            return {'success': False, 'cancelled': True}

    def quick_configure(self) -> Dict[str, Any]:
        """
        Perform quick configuration (using default options)

        Returns:
            Configuration result dictionary
        """
        return self.auto_configure({
            'configPath': './.dsgs/config.yaml',
            'validate': True
        })

    def update_configuration(self, existing_config_path: str, new_options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update existing configuration

        Args:
            existing_config_path: Existing configuration file path
            new_options: New configuration options

        Returns:
            Update result dictionary
        """
        if new_options is None:
            new_options = {}

        # Load existing configuration
        existing_config = self.config_generator.load(existing_config_path)
        if not existing_config:
            print(f'Existing config not found at {existing_config_path}, creating new config...')
            return self.auto_configure(new_options)

        # Detect newly installed tools
        print('Detecting newly installed AI CLI tools...')
        detected_tools = self.cli_detector.detect_all()
        self._print_detection_results(detected_tools)

        # Generate updated configuration
        updated_config = self.config_generator.generate(detected_tools)

        # Save updated configuration
        config_path = new_options.get('configPath', existing_config_path)
        print(f'Updating configuration at {config_path}...')
        save_result = self.config_generator.save(updated_config, config_path)

        if not save_result:
            raise Exception('Failed to save updated configuration')

        print('Configuration updated successfully!')

        # Validate integration
        if new_options.get('validate', True):
            print('Validating integrations...')
            validation_results = self.validator.validate_all_integrations(updated_config)

            # Generate validation report
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
        Get current configuration status

        Returns:
            Configuration status dictionary
        """
        # Detect currently installed tools
        detected_tools = self.cli_detector.detect_all()

        # Count installed tools
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
        Get current timestamp

        Returns:
            ISO format timestamp string
        """
        import datetime
        return datetime.datetime.now().isoformat()