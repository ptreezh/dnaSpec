"""
集成测试模块
测试所有核心模块的协同工作
"""
import unittest
import tempfile
import os
from pathlib import Path

from src.dsgs_spec_kit_integration.core.command_parser import CommandParser
from src.dsgs_spec_kit_integration.core.skill_mapper import SkillMapper
from src.dsgs_spec_kit_integration.core.python_bridge import PythonBridge
from src.dsgs_spec_kit_integration.core.skill_executor import SkillExecutor
from src.dsgs_spec_kit_integration.core.command_handler import CommandHandler
from src.dsgs_spec_kit_integration.core.interactive_shell import InteractiveShell
from src.dsgs_spec_kit_integration.core.cli_detector import CliDetector
from src.dsgs_spec_kit_integration.core.config_generator import ConfigGenerator
from src.dsgs_spec_kit_integration.core.integration_validator import IntegrationValidator
from src.dsgs_spec_kit_integration.core.auto_configurator import AutoConfigurator
from src.dsgs_spec_kit_integration.core.platform_utils import PlatformUtils


class TestDSGSIntegration(unittest.TestCase):
    """
    DSGS集成测试类
    """
    
    def setUp(self):
        """
        测试前准备
        """
        self.parser = CommandParser()
        self.skill_mapper = SkillMapper()
        self.python_bridge = PythonBridge()
        self.skill_executor = SkillExecutor(self.python_bridge, self.skill_mapper)
        self.command_handler = CommandHandler(self.parser, self.skill_executor)
        self.shell = InteractiveShell(self.command_handler)
        self.cli_detector = CliDetector()
        self.config_generator = ConfigGenerator()
        self.validator = IntegrationValidator(self.skill_executor)
        self.auto_configurator = AutoConfigurator(
            self.cli_detector, 
            self.config_generator, 
            self.validator
        )
    
    def test_command_parser(self):
        """
        测试命令解析器
        """
        # 测试有效命令
        result = self.parser.parse('/speckit.dsgs.architect 设计电商系统')
        self.assertTrue(result['isValid'])
        self.assertEqual(result['skill'], 'architect')
        self.assertEqual(result['params'], '设计电商系统')
        
        # 测试无参数命令
        result = self.parser.parse('/speckit.dsgs.agent-creator')
        self.assertTrue(result['isValid'])
        self.assertEqual(result['skill'], 'agent-creator')
        self.assertEqual(result['params'], '')
        
        # 测试无效命令
        result = self.parser.parse('/invalid.command')
        self.assertFalse(result['isValid'])
    
    def test_skill_mapper(self):
        """
        测试技能映射器
        """
        # 测试标准映射
        mapped = self.skill_mapper.map('architect')
        self.assertEqual(mapped, 'dsgs-architect')
        
        # 测试自定义映射
        self.skill_mapper.register('custom-skill', 'dsgs-custom')
        mapped = self.skill_mapper.map('custom-skill')
        self.assertEqual(mapped, 'dsgs-custom')
        
        # 测试不存在的技能
        mapped = self.skill_mapper.map('nonexistent')
        self.assertIsNone(mapped)
    
    def test_python_bridge(self):
        """
        测试Python桥接器
        """
        # 测试architect技能
        result = self.python_bridge.execute_skill('dsgs-architect', '电商系统')
        self.assertTrue(result['success'])
        self.assertIn('WebApp', result['result'])
    
    def test_skill_executor(self):
        """
        测试技能执行器
        """
        # 测试architect技能执行
        result = self.skill_executor.execute('architect', '电商系统')
        self.assertTrue(result['success'])
        self.assertIn('WebApp', result['result'])
        
        # 测试不存在的技能
        result = self.skill_executor.execute('nonexistent', 'test')
        self.assertFalse(result['success'])
    
    def test_command_handler(self):
        """
        测试命令处理器
        """
        # 测试完整命令处理流程
        result = self.command_handler.handle_command('/speckit.dsgs.architect 电商系统')
        self.assertTrue(result['success'])
        self.assertIn('WebApp', result['result'])
        
        # 测试无效命令
        result = self.command_handler.handle_command('/invalid.command test')
        self.assertFalse(result['success'])
    
    def test_cli_detector(self):
        """
        测试CLI检测器
        """
        # 检测所有CLI工具
        results = self.cli_detector.detect_all()
        
        # 验证结果结构
        self.assertIsInstance(results, dict)
        self.assertIn('claude', results)
        self.assertIn('gemini', results)
        self.assertIn('qwen', results)
        
        # 检查检测结果格式
        for name, info in results.items():
            self.assertIn('installed', info)
    
    def test_config_generator(self):
        """
        测试配置生成器
        """
        # 使用模拟检测结果
        mock_detected_tools = {
            'claude': {
                'installed': True,
                'version': '1.0.0',
                'installPath': '/usr/bin/claude',
                'configPath': '/home/user/.config/claude'
            }
        }
        
        config = self.config_generator.generate(mock_detected_tools)
        
        # 验证配置结构
        self.assertIn('version', config)
        self.assertIn('platforms', config)
        self.assertIn('skills', config)
        
        # 验证平台信息
        self.assertEqual(len(config['platforms']), 1)
        self.assertEqual(config['platforms'][0]['name'], 'claude')
        
        # 测试配置验证
        self.assertTrue(self.config_generator.validate(config))
    
    def test_integration_validator(self):
        """
        测试集成验证器
        """
        # 创建模拟配置
        mock_config = {
            'platforms': [
                {
                    'name': 'test-platform',
                    'enabled': True,
                    'skills': {}
                }
            ]
        }
        
        # 验证单个平台集成
        result = self.validator.validate_platform_integration('test-platform', mock_config)
        # 结果可能因实际环境而异，但结构应该正确
        
        # 验证所有集成
        all_results = self.validator.validate_all_integrations(mock_config)
        self.assertIsInstance(all_results, dict)
    
    def test_platform_utils(self):
        """
        测试平台工具
        """
        # 测试平台检测
        platform_name = PlatformUtils.get_platform()
        self.assertIn(platform_name, ['windows', 'darwin', 'linux'])
        
        # 测试路径操作
        home = PlatformUtils.get_user_home()
        self.assertIsInstance(home, str)
        self.assertTrue(len(home) > 0)
        
        # 测试标准路径
        paths = PlatformUtils.get_standard_paths()
        self.assertIn('config', paths)
        self.assertIn('temp', paths)
        self.assertIn('data', paths)
    
    def test_auto_configurator_status(self):
        """
        测试自动配置器状态功能
        """
        status = self.auto_configurator.get_status()
        self.assertIn('detectedTools', status)
        self.assertIn('installedCount', status)
        self.assertIn('totalCount', status)
        self.assertIn('installedTools', status)
        self.assertIn('timestamp', status)
    
    def test_end_to_end_integration(self):
        """
        测试端到端集成
        """
        # 测试命令解析 -> 执行 -> 返回结果的完整流程
        result = self.command_handler.handle_command('/speckit.dsgs.architect 博客系统')
        
        # 验证结果结构
        self.assertIn('success', result)
        self.assertIn('result', result)
        
        if result['success']:
            self.assertIsInstance(result['result'], str)
            self.assertTrue(len(result['result']) > 0)


if __name__ == '__main__':
    unittest.main()