#!/usr/bin/env python3
"""
TDD驱动的安全部署测试
实现单元测试、集成测试和回归测试
"""
import pytest
import os
import sys
import tempfile
import shutil
import json
import subprocess
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from dna_spec_kit_integration.core.secure_deployment_manager import (
    SecurityContext, SecurityError, SecureDeploymentManager
)


class TestSecurityContext:
    """安全上下文单元测试"""

    def test_valid_security_context_in_allowed_root(self):
        """测试：在允许根目录内的有效安全上下文"""
        with tempfile.TemporaryDirectory() as temp_dir:
            allowed_root = Path(temp_dir)
            work_dir = allowed_root / "project"
            work_dir.mkdir()

            # 切换到工作目录
            original_cwd = os.getcwd()
            os.chdir(work_dir)

            try:
                security_context = SecurityContext(allowed_root)
                context = security_context.get_project_context()

                assert context['project_root'] == str(allowed_root)
                assert context['current_dir'] == str(work_dir)
                assert context['relative_path'] == 'project'
                assert context['security_level'] == 'project-isolated'
                assert not context['is_root']
            finally:
                os.chdir(original_cwd)

    def test_security_context_at_root(self):
        """测试：在根目录的安全上下文"""
        with tempfile.TemporaryDirectory() as temp_dir:
            allowed_root = Path(temp_dir)

            original_cwd = os.getcwd()
            os.chdir(allowed_root)

            try:
                security_context = SecurityContext(allowed_root)
                context = security_context.get_project_context()

                assert context['is_root'] == True
            finally:
                os.chdir(original_cwd)

    def test_security_context_violation_outside_allowed_root(self):
        """测试：在允许根目录外的安全违规"""
        with tempfile.TemporaryDirectory() as temp_dir1, tempfile.TemporaryDirectory() as temp_dir2:
            allowed_root = Path(temp_dir1)
            violation_dir = Path(temp_dir2)

            original_cwd = os.getcwd()
            os.chdir(violation_dir)

            try:
                with pytest.raises(SecurityError, match="Access denied"):
                    SecurityContext(allowed_root)
            finally:
                os.chdir(original_cwd)

    def test_get_safe_path_relative(self):
        """测试：获取安全的相对路径"""
        with tempfile.TemporaryDirectory() as temp_dir:
            allowed_root = Path(temp_dir)
            work_dir = allowed_root / "project"
            work_dir.mkdir()

            original_cwd = os.getcwd()
            os.chdir(work_dir)

            try:
                security_context = SecurityContext(allowed_root)

                # 测试相对路径
                safe_path = security_context.get_safe_path("file.txt")
                assert safe_path == work_dir / "file.txt"

                # 测试子目录路径
                safe_path = security_context.get_safe_path("subdir/file.txt")
                assert safe_path == work_dir / "subdir" / "file.txt"
            finally:
                os.chdir(original_cwd)

    def test_get_safe_path_absolute_within_allowed(self):
        """测试：获取允许范围内的绝对路径"""
        with tempfile.TemporaryDirectory() as temp_dir:
            allowed_root = Path(temp_dir)
            target_file = allowed_root / "project" / "file.txt"

            security_context = SecurityContext(allowed_root)
            safe_path = security_context.get_safe_path(str(target_file))

            assert safe_path == target_file.resolve()

    def test_get_safe_path_absolute_violation(self):
        """测试：获取范围外的绝对路径（安全违规）"""
        with tempfile.TemporaryDirectory() as temp_dir1, tempfile.TemporaryDirectory() as temp_dir2:
            allowed_root = Path(temp_dir1)
            violation_file = Path(temp_dir2) / "file.txt"

            security_context = SecurityContext(allowed_root)

            with pytest.raises(SecurityError, match="Access denied"):
                security_context.get_safe_path(str(violation_file))

    def test_get_safe_path_directory_traversal_attempt(self):
        """测试：目录遍历攻击尝试"""
        with tempfile.TemporaryDirectory() as temp_dir:
            allowed_root = Path(temp_dir)
            work_dir = allowed_root / "project"
            work_dir.mkdir()

            original_cwd = os.getcwd()
            os.chdir(work_dir)

            try:
                security_context = SecurityContext(allowed_root)

                # 尝试目录遍历
                with pytest.raises(SecurityError, match="Access denied"):
                    security_context.get_safe_path("../../../etc/passwd")

                with pytest.raises(SecurityError, match="Access denied"):
                    security_context.get_safe_path("..\\..\\..\\windows\\system32")
            finally:
                os.chdir(original_cwd)


class TestSecureDeploymentManager:
    """安全部署管理器单元测试"""

    def test_project_level_initialization(self):
        """测试：项目级模式初始化"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # 模拟无Stigmergy环境
            with patch('dna_spec_kit_integration.core.secure_deployment_manager.SecureDeploymentManager._check_stigmergy_availability', return_value=False):
                manager = SecureDeploymentManager(project_root)

                assert manager.deployment_mode == 'project-level'
                assert not manager.stigmergy_available
                assert manager.project_root == project_root
                assert isinstance(manager.security_context, SecurityContext)

    def test_stigmergy_mode_initialization(self):
        """测试：Stigmergy模式初始化"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # 模拟有Stigmergy环境
            with patch('dna_spec_kit_integration.core.secure_deployment_manager.SecureDeploymentManager._check_stigmergy_availability', return_value=True):
                manager = SecureDeploymentManager(project_root)

                assert manager.deployment_mode == 'stigmergy'
                assert manager.stigmergy_available
                assert manager.project_root == project_root

    def test_get_dnaspec_skills(self):
        """测试：获取DNASPEC技能列表"""
        manager = SecureDeploymentManager()
        skills = manager._get_dnaspec_skills()

        assert len(skills) == 6
        skill_names = [skill['name'] for skill in skills]
        expected_names = [
            'context-analysis', 'context-optimization', 'cognitive-template',
            'architect', 'task-decomposer', 'constraint-generator'
        ]
        assert skill_names == expected_names

    def test_generate_secure_project_skill_files(self):
        """测试：生成安全项目级技能文件"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            manager = SecureDeploymentManager(project_root)

            skill = {
                'name': 'test-skill',
                'description': 'Test skill for unit testing',
                'function': 'execute_test_skill'
            }

            # 模拟无Stigmergy环境
            with patch.object(manager, 'stigmergy_available', False):
                generated_files = manager._generate_secure_project_skill_files(skill)

                # 验证生成的文件
                assert len(generated_files) == 4  # executor.py, .cmd, .sh, config.json

                # 检查文件是否存在
                skill_dir = manager.project_slash_dir / 'test-skill'
                assert skill_dir.exists()

                executor_file = skill_dir / 'test-skill_executor.py'
                assert executor_file.exists()

                wrapper_file = skill_dir / 'test-skill.cmd'
                assert wrapper_file.exists()

                bash_file = skill_dir / 'test-skill.sh'
                assert bash_file.exists()

                config_file = skill_dir / 'config.json'
                assert config_file.exists()

    def test_secure_skill_executor_code_generation(self):
        """测试：安全技能执行器代码生成"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            manager = SecureDeploymentManager(project_root)

            skill = {
                'name': 'architect',
                'description': 'Design system architecture',
                'function': 'execute_architect'
            }

            code = manager._generate_secure_skill_executor_code(skill)

            # 验证安全相关代码
            assert 'ALLOWED_ROOT' in code
            assert 'validate_security' in code
            assert 'get_safe_context' in code
            assert 'project-isolated' in code
            assert 'SECURITY VIOLATION' in code

            # 验证项目根路径正确嵌入
            assert str(project_root) in code

    def test_secure_wrapper_code_generation(self):
        """测试：安全包装脚本代码生成"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            manager = SecureDeploymentManager(project_root)

            skill = {
                'name': 'architect',
                'description': 'Design system architecture',
                'function': 'execute_architect'
            }

            # 测试Windows包装脚本
            cmd_code = manager._generate_secure_wrapper_code(skill)
            assert 'SECURITY ERROR' in cmd_code
            assert 'Not in project directory' in cmd_code
            assert str(project_root) in cmd_code

            # 测试Bash包装脚本
            bash_code = manager._generate_secure_bash_wrapper_code(skill)
            assert 'SECURITY ERROR' in bash_code
            assert 'Not in project directory' in bash_code
            assert str(project_root) in bash_code

    def test_generate_security_config(self):
        """测试：生成安全配置文件"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            manager = SecureDeploymentManager(project_root)

            # 创建slash_commands目录
            manager.project_slash_dir.mkdir(parents=True)

            manager._generate_security_config()

            security_config_file = manager.project_slash_dir / 'security_config.json'
            assert security_config_file.exists()

            with open(security_config_file, 'r') as f:
                config = json.load(f)

            # 验证安全配置结构
            assert 'security_policy' in config
            assert 'deployment' in config
            assert 'permissions' in config
            assert 'monitoring' in config

            # 验证安全策略
            assert config['security_policy']['level'] == 'project-isolated'
            assert config['security_policy']['access_control'] == 'directory_isolation'
            assert config['security_policy']['allowed_root'] == str(project_root)
            assert config['security_policy']['boundary_enforcement'] == True

    def test_generate_secure_integration_guide(self):
        """测试：生成安全集成指南"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            manager = SecureDeploymentManager(project_root)

            # 创建slash_commands目录
            manager.project_slash_dir.mkdir(parents=True)

            manager._generate_secure_integration_guide()

            guide_file = manager.project_slash_dir / 'SECURITY_INTEGRATION_GUIDE.md'
            assert guide_file.exists()

            with open(guide_file, 'r') as f:
                content = f.read()

            # 验证安全相关内容
            assert 'Security Overview' in content
            assert 'project-isolated' in content
            assert 'Directory Isolation' in content
            assert 'Security Guarantees' in content
            assert str(project_root) in content

    def test_generate_secure_ai_tool_configs(self):
        """测试：生成安全AI工具配置"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            manager = SecureDeploymentManager(project_root)

            # 创建slash_commands目录
            manager.project_slash_dir.mkdir(parents=True)

            manager._generate_secure_ai_tool_configs()

            configs_dir = manager.project_slash_dir / 'ai_configs'
            assert configs_dir.exists()

            # 验证Claude配置
            claude_config_file = configs_dir / 'claude_secure_config.json'
            assert claude_config_file.exists()

            with open(claude_config_file, 'r') as f:
                config = json.load(f)

            assert 'security_policy' in config
            assert config['security_policy']['level'] == 'project-isolated'
            assert config['security_policy']['project_root'] == str(project_root)

    def test_verify_project_deployment_secure(self):
        """测试：验证项目级部署安全配置"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            manager = SecureDeploymentManager(project_root)

            # 模拟无Stigmergy环境
            with patch.object(manager, 'stigmergy_available', False):
                # 创建部署文件
                manager.project_slash_dir.mkdir(parents=True)
                manager._generate_security_config()

                # 创建一些技能文件
                skill_dir = manager.project_slash_dir / 'architect'
                skill_dir.mkdir()
                (skill_dir / 'architect_executor.py').touch()
                (skill_dir / 'architect.cmd').touch()

                # 创建技能配置
                skill_config = {
                    'security_context': manager.security_context.get_project_context()
                }
                with open(skill_dir / 'config.json', 'w') as f:
                    json.dump(skill_config, f)

                verification = manager._verify_project_deployment_secure()

                assert verification['success'] == True
                assert verification['deployment_mode'] == 'project-level'
                assert verification['security_level'] == 'project-isolated'
                assert verification['security_config_exists'] == True
                assert 'architect' in verification['deployed_skills']


class TestIntegrationScenarios:
    """集成测试场景"""

    def test_full_project_level_deployment_flow(self):
        """测试：完整的项目级部署流程"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            original_cwd = os.getcwd()

            try:
                os.chdir(project_root)

                # 模拟无Stigmergy环境
                with patch('dna_spec_kit_integration.core.secure_deployment_manager.SecureDeploymentManager._check_stigmergy_availability', return_value=False):
                    manager = SecureDeploymentManager()
                    result = manager.deploy_all()

                    # 验证部署结果
                    assert result['success'] == True
                    assert result['mode'] == 'project-level'
                    assert len(result['deployed_skills']) > 0
                    assert 'security_context' in result

                    # 验证文件生成
                    assert manager.project_slash_dir.exists()
                    security_config_file = manager.project_slash_dir / 'security_config.json'
                    assert security_config_file.exists()

                    # 验证技能文件生成
                    skills = manager._get_dnaspec_skills()
                    for skill in skills[:1]:  # 测试第一个技能
                        skill_dir = manager.project_slash_dir / skill['name']
                        assert skill_dir.exists()

                        executor_file = skill_dir / f'{skill["name"]}_executor.py'
                        assert executor_file.exists()

                        with open(executor_file, 'r') as f:
                            code = f.read()
                        assert 'validate_security' in code

            finally:
                os.chdir(original_cwd)

    def test_security_boundary_enforcement(self):
        """测试：安全边界强制执行"""
        with tempfile.TemporaryDirectory() as temp_dir1, tempfile.TemporaryDirectory() as temp_dir2:
            project_root = Path(temp_dir1)
            outside_dir = Path(temp_dir2)

            # 在项目内创建安全上下文
            security_context = SecurityContext(project_root)

            # 测试允许范围内的路径
            allowed_file = project_root / "project" / "file.txt"
            safe_path = security_context.get_safe_path(str(allowed_file))
            assert safe_path == allowed_file.resolve()

            # 测试范围外的路径（应该抛出异常）
            violation_file = outside_dir / "file.txt"
            with pytest.raises(SecurityError):
                security_context.get_safe_path(str(violation_file))

    def test_stigmergy_global_deployment_simulation(self):
        """测试：Stigmergy全局部署模拟"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # 模拟有Stigmergy环境
            with patch('dna_spec_kit_integration.core.secure_deployment_manager.SecureDeploymentManager._check_stigmergy_availability', return_value=True):
                with patch('dna_spec_kit_integration.core.secure_deployment_manager.StigmergyAdapter') as mock_adapter_class:
                    # 模拟Stigmergy适配器
                    mock_adapter = Mock()
                    mock_adapter.deploy_to_all_clis.return_value = {
                        'success': True,
                        'successful_deployments': 8,
                        'total_platforms': 8,
                        'deployment_results': {}
                    }
                    mock_adapter.verify_deployment.return_value = {
                        'success': True,
                        'deployed_clis': ['claude', 'gemini'],
                        'missing_clis': []
                    }
                    mock_adapter_class.return_value = mock_adapter

                    manager = SecureDeploymentManager(project_root)
                    result = manager.deploy_all()

                    # 验证全局部署结果
                    assert result['mode'] == 'stigmergy'
                    assert result['success'] == True
                    assert 'security_context' in result
                    assert result['security_context']['security_level'] == 'global-dynamic'

    def test_command_line_interface(self):
        """测试：命令行接口"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            original_cwd = os.getcwd()

            try:
                os.chdir(project_root)

                # 测试状态命令
                result = subprocess.run([
                    sys.executable, '-c',
                    f'''
import sys
sys.path.insert(0, "{os.path.join(os.path.dirname(__file__), "..", "src")}")
from dna_spec_kit_integration.core.secure_deployment_manager import SecureDeploymentManager

manager = SecureDeploymentManager()
status = manager.get_deployment_status()
import json
print(json.dumps(status))
                    '''
                ], capture_output=True, text=True)

                assert result.returncode == 0
                status = json.loads(result.stdout)
                assert 'security_context' in status

            finally:
                os.chdir(original_cwd)


class TestRegressionTests:
    """回归测试"""

    def test_backwards_compatibility_with_existing_deployments(self):
        """测试：与现有部署的向后兼容性"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            # 创建旧风格的部署结构
            old_slash_dir = project_root / '.dnaspec' / 'slash_commands'
            old_slash_dir.mkdir(parents=True)

            # 创建旧技能文件（没有安全配置）
            old_skill_dir = old_slash_dir / 'architect'
            old_skill_dir.mkdir()
            (old_skill_dir / 'architect.cmd').write_text('@echo off\necho Old architect skill')

            # 创建新的安全部署管理器
            manager = SecureDeploymentManager(project_root)

            # 验证能检测到缺少安全配置
            verification = manager._verify_project_deployment_secure()
            assert verification['security_level'] in ['unprotected', 'none']

    def test_security_policy_enforcement_regression(self):
        """测试：安全策略执行回归"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)

            manager = SecureDeploymentManager(project_root)

            # 生成技能文件
            skill = {
                'name': 'architect',
                'description': 'Design system architecture',
                'function': 'execute_architect'
            }

            executor_code = manager._generate_secure_skill_executor_code(skill)

            # 验证所有必需的安全检查都存在
            required_security_checks = [
                'validate_security',
                'get_safe_context',
                'ALLOWED_ROOT',
                'relative_to',
                'SECURITY VIOLATION',
                'project-isolated'
            ]

            for check in required_security_checks:
                assert check in executor_code, f"Missing security check: {check}"

    def test_performance_regression_deployment_speed(self):
        """测试：部署速度性能回归"""
        import time

        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            original_cwd = os.getcwd()

            try:
                os.chdir(project_root)

                # 模拟无Stigmergy环境
                with patch('dna_spec_kit_integration.core.secure_deployment_manager.SecureDeploymentManager._check_stigmergy_availability', return_value=False):
                    manager = SecureDeploymentManager()

                    start_time = time.time()
                    result = manager.deploy_all()
                    end_time = time.time()

                    deployment_time = end_time - start_time

                    # 验证部署在合理时间内完成（应该少于5秒）
                    assert deployment_time < 5.0, f"Deployment too slow: {deployment_time:.2f}s"
                    assert result['success'] == True

            finally:
                os.chdir(original_cwd)


if __name__ == '__main__':
    # 运行测试
    pytest.main([__file__, '-v', '--tb=short'])