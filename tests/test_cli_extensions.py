#!/usr/bin/env/python3
"""
CLI扩展部署器单元测试
测试项目级CLI扩展和全局Stigmergy部署
"""
import pytest
import os
import sys
import tempfile
import shutil
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dna_spec_kit_integration.core.cli_extension_deployer import CLIExtensionDeployer
from dna_spec_kit_integration.cli_extension_handler import (
    handle_dnaspec_command, get_available_skills, validate_skill_parameters,
    get_skill_examples
)


class TestCLIExtensionDeployer:
    """CLI扩展部署器测试"""

    def test_initialization_with_stigmergy(self):
        """测试：有Stigmergy时的初始化"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            with patch('dna_spec_kit_integration.core.cli_extension_deployer.CLIExtensionDeployer._check_stigmergy_availability', return_value=True):
                deployer = CLIExtensionDeployer(project_root)

                assert deployer.deployment_mode == 'stigmergy'
                assert deployer.stigmergy_available == True
                assert deployer.project_root == project_root
                assert len(deployer.supported_clis) == 6

    def test_initialization_without_stigmergy(self):
        """测试：无Stigmergy时的初始化"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            with patch('dna_spec_kit_integration.core.cli_extension_deployer.CLIExtensionDeployer._check_stigmergy_availability', return_value=False):
                deployer = CLIExtensionDeployer(project_root)

                assert deployer.deployment_mode == 'cli-extensions'
                assert not deployer.stigmergy_available
                assert deployer.project_root == project_root

    def test_supported_clis_configuration(self):
        """测试：支持的CLI工具配置"""
        deployer = CLIExtensionDeployer()

        expected_clis = ['claude', 'cursor', 'vscode', 'windsurf', 'continue', 'cursor_rules',
                       'gemini', 'qwen', 'iflow', 'qodercli', 'codebuddy', 'copilot']
        assert list(deployer.supported_clis.keys()) == expected_clis
        assert len(deployer.supported_clis) == 12

        # 验证每个CLI工具的配置
        for cli_name, config in deployer.supported_clis.items():
            assert 'format' in config
            assert 'extension' in config
            assert 'command_prefix' in config
            assert 'description' in config

    def test_get_dnaspec_skills(self):
        """测试：获取DNASPEC技能列表"""
        deployer = CLIExtensionDeployer()
        skills = deployer._get_dnaspec_skills()

        assert len(skills) == 6
        skill_names = [skill['name'] for skill in skills]
        expected_names = [
            'context-analysis', 'context-optimization', 'cognitive-template',
            'architect', 'task-decomposer', 'constraint-generator'
        ]
        assert skill_names == expected_names

        # 验证技能结构
        for skill in skills:
            assert 'name' in skill
            assert 'display_name' in skill
            assert 'description' in skill
            assert 'command' in skill
            assert 'function' in skill
            assert 'category' in skill

    def test_deploy_cli_extensions(self):
        """测试：部署CLI扩展"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # 模拟无Stigmergy环境
            with patch('dna_spec_kit_integration.core.cli_extension_deployer.CLIExtensionDeployer._check_stigmergy_availability', return_value=False):
                deployer = CLIExtensionDeployer(project_root)
                result = deployer._deploy_cli_extensions()

                # 验证部署结果
                assert result['success'] == True
                assert result['mode'] == 'cli-extensions'
                assert len(result['deployed_extensions']) > 0
                assert len(result['supported_clis']) == 6
                assert result['deployment_errors'] == []

                # 验证扩展目录已创建
                assert deployer.cli_extensions_dir.exists()

                # 验证每个CLI工具都有扩展文件
                for cli_name in deployer.supported_clis.keys():
                    cli_dir = deployer.cli_extensions_dir / cli_name
                    assert cli_dir.exists()

    def test_generate_claude_skills(self):
        """测试：生成Claude技能扩展"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            deployer = CLIExtensionDeployer(project_root)
            cli_dir = deployer.cli_extensions_dir / 'claude'
            cli_dir.mkdir(parents=True, exist_ok=True)

            skills = deployer._get_dnaspec_skills()
            generated_files = deployer._generate_claude_skills(cli_dir, skills)

            assert len(generated_files) == 1  # Claude只生成一个配置文件

            # 验证生成的Claude技能配置文件
            config_file = cli_dir / 'dnaspec_skills.json'
            assert config_file.exists()

            with open(config_file, 'r') as f:
                config = json.load(f)

            assert 'version' in config
            assert 'skills' in config
            assert len(config['skills']) == 6
            assert config['project_root'] == str(project_root)

            # 验证技能配置结构
            for skill_config in config['skills']:
                assert 'name' in skill_config
                assert 'description' in skill_config
                assert 'command' in skill_config
                assert 'category' in skill_config
                assert 'handler' in skill_config
                assert skill_config['handler']['type'] == 'python'
                assert skill_config['handler']['module'] == 'dna_spec_kit_integration.cli_extension_handler'

    def test_generate_cursor_extensions(self):
        """测试：生成Cursor扩展"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            deployer = CLIExtensionDeployer(project_root)
            cli_dir = deployer.cli_extensions_dir / 'cursor'
            cli_dir.mkdir(parents=True, exist_ok=True)

            skills = deployer._get_dnaspec_skills()
            generated_files = deployer._generate_cursor_extensions(cli_dir, skills)

            assert len(generated_files) == 6  # Cursor为每个技能生成一个文件

            # 验证生成的扩展文件
            for skill in skills:
                extension_file = cli_dir / f"dnaspec_{skill['name']}.md"
                assert extension_file.exists()

                with open(extension_file, 'r') as f:
                    content = f.read()

                # 验证文件内容
                assert f"# DNASPEC {skill['display_name']}" in content
                assert skill['description'] in content
                assert "## Usage" in content
                assert "Generated for project:" in content

    def test_generate_vscode_tasks(self):
        """测试：生成VS Code任务"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            deployer = CLIExtensionDeployer(project_root)
            cli_dir = deployer.cli_extensions_dir / 'vscode'
            cli_dir.mkdir(parents=True, exist_ok=True)

            skills = deployer._get_dnaspec_skills()
            generated_files = deployer._generate_vscode_tasks(cli_dir, skills)

            assert len(generated_files) == 1  # VS Code只生成一个tasks.json文件

            # 验证生成的tasks文件
            tasks_file = cli_dir / 'tasks.json'
            assert tasks_file.exists()

            with open(tasks_file, 'r') as f:
                tasks_config = json.load(f)

            assert 'version' in tasks_config
            assert 'tasks' in tasks_config
            assert len(tasks_config['tasks']) == 6

            # 验证任务配置结构
            for task in tasks_config['tasks']:
                assert 'label' in task
                assert 'type' in task
                assert task['type'] == 'shell'
                assert task['command'] == 'dnaspec-spec-kit'
                assert 'args' in task
                assert len(task['args']) == 3
                assert task['args'][0] == 'exec'
                assert task['args'][1].startswith('/')  # 技能命令

    def test_generate_windsurf_skills(self):
        """测试：生成Windsurf技能"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            deployer = CLIExtensionDeployer(project_root)
            cli_dir = deployer.cli_extensions_dir / 'windsurf'
            cli_dir.mkdir(parents=True, exist_ok=True)

            skills = deployer._get_dnaspec_skills()
            generated_files = deployer._generate_windsurf_skills(cli_dir, skills)

            assert len(generated_files) == 6  # Windsurf为每个技能生成一个JS文件

            # 验证生成的技能文件
            for skill in skills:
                skill_file = cli_dir / f"dnaspec_{skill['name']}.js"
                assert skill_file.exists()

                with open(skill_file, 'r', encoding='utf-8') as f:
                    js_content = f.read()

                # 验证JavaScript代码结构
                assert f"// DNASPEC {skill['display_name']} Extension" in js_content
                assert "handler" in js_content
                assert "module.exports" in js_content
                assert project_root.name in js_content

    def test_generate_continue_tools(self):
        """测试：生成Continue.dev工具"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            deployer = CLIExtensionDeployer(project_root)
            cli_dir = deployer.cli_extensions_dir / 'continue'
            cli_dir.mkdir(parents=True, exist_ok=True)

            skills = deployer._get_dnaspec_skills()
            generated_files = deployer._generate_continue_tools(cli_dir, skills)

            assert len(generated_files) == 6  # Continue为每个技能生成一个Python文件

            # 验证生成的工具文件
            for skill in skills:
                tool_file = cli_dir / f"dnaspec_{skill['name']}.py"
                assert tool_file.exists()

                with open(tool_file, 'r', encoding='utf-8') as f:
                    py_content = f.read()

                # 验证Python代码结构
                assert f'"""' in py_content  # 文档字符串开始
                assert f"DNASPEC {skill['display_name']} Tool" in py_content
                assert "class Dnaspec" in py_content
                assert "execute" in py_content
                assert project_root.name in py_content

    def test_generate_usage_guide(self):
        """测试：生成使用指南"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            deployer = CLIExtensionDeployer(project_root)

            # 创建CLI扩展目录
            deployer.cli_extensions_dir.mkdir(parents=True, exist_ok=True)

            # 生成使用指南
            deployer._generate_usage_guide()

            guide_file = deployer.cli_extensions_dir / 'USAGE_GUIDE.md'
            assert guide_file.exists()

            with open(guide_file, 'r') as f:
                content = f.read()

            # 验证指南内容
            assert "DNASPEC CLI Extensions Usage Guide" in content
            assert "Supported AI Tools" in content
            assert "Usage Instructions" in content
            assert project_root.name in content

    def test_get_deployment_status(self):
        """测试：获取部署状态"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            with patch('dna_spec_kit_integration.core.cli_extension_deployer.CLIExtensionDeployer._check_stigmergy_availability', return_value=False):
                deployer = CLIExtensionDeployer(project_root)
                status = deployer.get_deployment_status()

                assert status['stigmergy_available'] == False
                assert status['deployment_mode'] == 'cli-extensions'
                assert status['project_root'] == str(project_root)
                assert 'cli_extensions_dir' in status
                assert 'supported_clis' in status
                assert 'cli_count' in status
                assert status['cli_count'] == 12


  def test_generate_commands_dir_extensions(self):
        """测试：生成基于commands目录的扩展"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            deployer = CLIExtensionDeployer(project_root)

            # 测试Gemini CLI
            cli_config = deployer.supported_clis['gemini']
            skills = deployer._get_dnaspec_skills()

            commands_dir = project_root / '.gemini' / 'commands'
            commands_dir.mkdir(parents=True, exist_ok=True)

            generated_files = deployer._generate_commands_dir_extensions('gemini', cli_config, skills)

            assert len(generated_files) == 6  # 为每个技能生成一个命令文件

            # 验证生成的命令文件
            for skill in skills:
                command_file = commands_dir / f"dnaspec-{skill['name']}.md"
                assert command_file.exists()

                with open(command_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 验证Markdown内容结构
                assert f"# DNASPEC {skill['display_name']}" in content
                assert f"dnaspec-{skill['name']}" in content
                assert skill['description'] in content
                assert "## Description" in content
                assert "## Command" in content
                assert "## Usage" in content
                assert "Generated for gemini CLI" in content
                assert project_root.name in content

  def test_generate_slash_command_content(self):
        """测试：生成斜杠命令内容"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            deployer = CLIExtensionDeployer(project_root)

            skill = {
                'name': 'context-analysis',
                'display_name': 'Context Analysis',
                'description': 'Analyze context quality across 5 dimensions'
            }

            content = deployer._generate_slash_command_content('qwen', skill)

            # 验证内容结构
            assert "# DNASPEC Context Analysis" in content
            assert "/dnaspec-context-analysis" in content
            assert "Analyze context quality across 5 dimensions" in content
            assert "Generated for qwen CLI" in content
            assert project_root.name in content

    def test_new_cli_tools_integration(self):
        """测试：新CLI工具的完整集成"""
        new_clis = ['gemini', 'qwen', 'iflow', 'qodercli', 'codebuddy', 'copilot']

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            deployer = CLIExtensionDeployer(project_root)

            skills = deployer._get_dnaspec_skills()
            total_expected_files = 0

            for cli_name in new_clis:
                cli_config = deployer.supported_clis[cli_name]
                assert cli_config['format'] == 'commands_dir'
                assert 'commands_dir' in cli_config

                # 测试生成扩展
                generated_files = deployer._generate_cli_extensions(cli_name, cli_config, skills)
                total_expected_files += len(generated_files)

                # 验证commands目录被创建
                commands_dir = project_root / cli_config['commands_dir']
                assert commands_dir.exists()

                # 验证每个技能都有对应的命令文件
                for skill in skills:
                    command_file = commands_dir / f"dnaspec-{skill['name']}.md"
                    assert command_file.exists()

            # 验证总共生成的文件数量
            assert total_expected_files == 36  # 6 CLI tools × 6 skills each

import subprocess

class TestCLIExtensionHandler:
    """CLI扩展处理器测试"""

    def test_handle_dnaspec_command_success(self):
        """测试：成功处理DNASPEC命令"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            work_dir = project_root / "test_project"
            work_dir.mkdir()

            # 创建测试文件
            test_file = work_dir / "requirements.txt"
            test_file.write_text("Flask==2.0.0")

            original_cwd = os.getcwd()
            try:
                os.chdir(work_dir)

                # 模拟技能执行
                with patch('dna_spec_kit_integration.cli_extension_handler.subprocess.run') as mock_run:
                    mock_run.return_value = Mock(
                        returncode=0,
                        stdout="Context analysis completed successfully"
                    )

                    result = handle_dnaspec_command(
                        skill_name='context-analysis',
                        input_text='Analyze this context',
                        context={'project_root': str(project_root)}
                    )

                    assert result['success'] == True
                    assert result['output'] == 'Context analysis completed successfully'
                    assert result['skill_name'] == 'context-analysis'
                    assert result['project_root'] == str(project_root)

                    # 验证subprocess调用
                    mock_run.assert_called_once()
                    call_args = mock_run.call_args[0][0]
                    assert call_args[0] == sys.executable
                    assert call_args[1] == '-m'
                    assert 'dna_spec_kit_integration.cli' in call_args[2:]
                    assert 'exec' in call_args
                    assert '/context-analysis' in call_args
                    assert 'Analyze this context' in call_args

            finally:
                os.chdir(original_cwd)

    def test_handle_dnaspec_command_failure(self):
        """测试：DNASPEC命令执行失败"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # 模拟技能执行失败
            with patch('dna_spec_kit_integration.cli_extension_handler.subprocess.run') as mock_run:
                mock_run.return_value = Mock(
                    returncode=1,
                    stderr='Error: Skill execution failed'
                )

                result = handle_dnaspec_command(
                    skill_name='invalid-skill',
                    input_text='Test input',
                    context={'project_root': str(project_root)}
                )

                assert result['success'] == False
                assert result['error'] == 'Error: Skill execution failed'
                assert result['error_code'] == 'EXECUTION_FAILED'

    def test_handle_dnaspec_command_timeout(self):
        """测试：DNASPEC命令超时"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # 模拟技能执行超时
            with patch('dna_spec_kit_integration.cli_extension_handler.subprocess.run') as mock_run:
                mock_run.side_effect = subprocess.TimeoutExpired(['command'], 120)

                result = handle_dnaspec_command(
                    skill_name='context-analysis',
                    input_text='Test input',
                    context={'project_root': str(project_root)}
                )

                assert result['success'] == False
                assert result['error'] == 'DNASPEC execution timed out'
                assert result['error_code'] == 'TIMEOUT'

    def test_get_available_skills(self):
        """测试：获取可用技能列表"""
        skills = get_available_skills()

        assert 'skills' in skills
        assert 'total_count' in skills
        assert 'categories' in skills
        assert 'updated_at' in skills

        assert skills['total_count'] == 6
        assert len(skills['skills']) == 6
        assert len(skills['categories']) == 6

        # 验证技能列表结构
        for skill in skills['skills']:
            assert 'name' in skill
            assert 'display_name' in skill
            assert 'description' in skill
            assert 'command' in skill
            assert 'category' in skill
            assert 'examples' in skill
            assert len(skill['examples']) > 0

    def test_validate_skill_parameters(self):
        """测试：验证技能参数"""
        # 测试有效技能
        result = validate_skill_parameters('context-analysis', {})
        assert result['valid'] == True
        assert result['skill_name'] == 'context-analysis'

        # 测试无效技能
        result = validate_skill_parameters('invalid-skill', {})
        assert result['valid'] == False
        assert 'error' in result
        assert 'available_skills' in result

        # 验证可用技能列表
        available_skills = [skill['name'] for skill in get_available_skills()['skills']]
        assert result['available_skills'] == available_skills

    def test_get_skill_examples(self):
        """测试：获取技能示例"""
        # 测试有效技能
        result = get_skill_examples('architect')
        assert 'architect' == result['skill_name']
        assert 'display_name' in result
        assert 'examples' in result
        assert len(result['examples']) > 0

        # 测试无效技能
        result = get_skill_examples('invalid-skill')
        assert 'error' in result
        assert 'available_skills' in result

    def test_detect_project_root(self):
        """测试：检测项目根目录"""
        # 测试在项目目录内
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            work_dir = project_root / "subdir"
            work_dir.mkdir()

            # 创建项目标记文件
            (project_root / '.dnaspec').touch()

            original_cwd = os.getcwd()
            try:
                os.chdir(work_dir)

                # 测试目录检测逻辑 - 测试私有函数
                from dna_spec_kit_integration.cli_extension_handler import _detect_project_root
                detected_root = _detect_project_root()

                # 应该能检测到项目根目录
                assert detected_root == project_root

            finally:
                os.chdir(original_cwd)


class TestIntegrationScenarios:
    """集成测试场景"""

    def test_full_cli_extensions_deployment_flow(self):
        """测试：完整的CLI扩展部署流程"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            original_cwd = os.getcwd()

            try:
                os.chdir(project_root)

                # 模拟无Stigmergy环境
                with patch('dna_spec_kit_integration.core.cli_extension_deployer.CLIExtensionDeployer._check_stigmergy_availability', return_value=False):
                    deployer = CLIExtensionDeployer()
                    result = deployer.deploy_all()

                    # 验证部署结果
                    assert result['success'] == True
                    assert result['mode'] == 'cli-extensions'
                    assert len(result['deployed_extensions']) == 21  # 6个AI工具 x 各种文件数

                    # 验证生成的文件结构
                    for cli_name in deployer.supported_clis.keys():
                        cli_dir = deployer.cli_extensions_dir / cli_name
                        assert cli_dir.exists()

                    # 验证使用指南已生成
                    guide_file = deployer.cli_extensions_dir / 'USAGE_GUIDE.md'
                    assert guide_file.exists()

                    # 验证集成配置已生成
                    config_file = deployer.cli_extensions_dir / 'integration_config.json'
                    assert config_file.exists()

            finally:
                os.chdir(original_cwd)

    def test_stigmergy_deployment_fallback(self):
        """测试：Stigmergy部署失败时的降级"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # 模拟有Stigmergy但StigmergyAdapter导入失败
            with patch('dna_spec_kit_integration.core.cli_extension_deployer.CLIExtensionDeployer._check_stigmergy_availability', return_value=True):
                # Mock the StigmergyAdapter import to fail
                with patch('builtins.__import__') as mock_import:
                    def import_side_effect(name, *args, **kwargs):
                        if 'stigmergy_adapter' in name:
                            raise ModuleNotFoundError("StigmergyAdapter not found")
                        return __import__(name, *args, **kwargs)

                    mock_import.side_effect = import_side_effect

                    deployer = CLIExtensionDeployer(project_root)
                    result = deployer.deploy_all()

                    # 验证降级到CLI扩展模式成功
                    assert result['success'] == True
                    assert result['mode'] == 'stigmergy'  # 仍然标记为stigmergy模式，但有fallback
                    assert 'fallback_result' in result
                    assert result['fallback_result']['success'] == True

    def test_cross_platform_compatibility(self):
        """测试：跨平台兼容性"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            deployer = CLIExtensionDeployer(project_root)

            # 验证所有支持的平台都有正确的扩展格式
            for cli_name, config in deployer.supported_clis.items():
                assert 'extension' in config
                assert config['extension'] in ['.json', '.md', '.js', '.py']

                # 验证命令前缀
                assert 'command_prefix' in config
                assert config['command_prefix'] in ['/', '']

                # 验证描述
                assert 'description' in config
                assert len(config['description']) > 0

    def test_skill_extension_integration(self):
        """测试：技能扩展集成"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # 部署CLI扩展
            with patch('dna_spec_kit_integration.core.cli_extension_deployer.CLIExtensionDeployer._check_stigmergy_availability', return_value=False):
                deployer = CLIExtensionDeployer(project_root)
                deploy_result = deployer.deploy_all()

                # 测试每个技能在每个CLI工具中的表现
                skills = deployer._get_dnaspec_skills()

                for skill in skills:
                    # 测试处理器
                    with patch('dna_spec_kit_integration.cli_extension_handler.handle_dnaspec_command') as mock_handler:
                        mock_handler.return_value = {
                            'success': True,
                            'output': f'{skill["display_name"]} executed successfully'
                        }

                        # 模拟在每个CLI工具中调用技能
                        result = handle_dnaspec_command(
                            skill_name=skill['name'],
                            input_text='Test input',
                            context={'project_root': str(project_root)}
                        )

                        assert result['success'] == True
                        assert result['skill_name'] == skill['name']

    def test_security_isolation(self):
        """测试：安全隔离"""
        with tempfile.TemporaryDirectory() as temp_dir1, tempfile.TemporaryDirectory() as temp_dir2:
            project_root = Path(temp_dir1)
            outside_dir = Path(temp_dir2)

            # 测试项目内正常访问
            with patch('dna_spec_kit_integration.cli_extension_handler.handle_dnaspec_command') as mock_handler:
                mock_handler.return_value = {
                    'success': True,
                    'output': 'Success'
                }

                result = handle_dnaspec_command(
                    skill_name='context-analysis',
                    input_text='Test',
                    context={'project_root': str(project_root)}
                )
                assert result['success'] == True

            # 测试项目外访问（应该被安全处理器阻止）
            # 这部分依赖于安全处理器中的项目检测逻辑


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])