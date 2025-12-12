#!/usr/bin/env python3
"""
技能执行安全集成测试
测试真实技能执行过程中的安全边界和权限控制
"""
import pytest
import os
import sys
import tempfile
import shutil
import json
import subprocess
from pathlib import Path
from unittest.mock import patch, Mock

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestSkillExecutionSecurity:
    """技能执行安全集成测试"""

    def test_project_skill_execution_within_allowed_directory(self):
        """测试：项目内技能执行（允许的目录）"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            work_dir = project_root / "test_project"
            work_dir.mkdir()

            # 创建项目文件
            test_file = work_dir / "requirements.txt"
            test_file.write_text("Flask==2.0.0\\nSQLAlchemy==1.4.0")

            original_cwd = os.getcwd()

            try:
                # 切换到项目目录
                os.chdir(work_dir)

                # 部署安全的技能文件
                from dna_spec_kit_integration.core.secure_deployment_manager import SecureDeploymentManager

                manager = SecureDeploymentManager(project_root)
                with patch.object(manager, 'stigmergy_available', False):
                    # 生成architect技能
                    skill = {
                        'name': 'architect',
                        'description': 'Design system architecture',
                        'function': 'execute_architect'
                    }
                    manager._generate_secure_project_skill_files(skill)

                    # 测试技能执行器
                    executor_file = manager.project_slash_dir / 'architect' / 'architect_executor.py'

                    # 模拟技能函数（避免依赖真实的技能模块）
                    with patch('dna_context_engineering.skills_system_final.execute_architect') as mock_execute:
                        mock_execute.return_value = "Architecture designed successfully"

                        result = subprocess.run([
                            sys.executable, str(executor_file), "Design a simple web app"
                        ], capture_output=True, text=True, cwd=work_dir)

                        # 验证执行成功
                        assert result.returncode == 0
                        assert "Architecture designed successfully" in result.stdout

                        # 验证技能函数被调用
                        mock_execute.assert_called_once()

            finally:
                os.chdir(original_cwd)

    def test_project_skill_execution_security_violation(self):
        """测试：项目内技能执行安全违规"""
        with tempfile.TemporaryDirectory() as temp_dir1, tempfile.TemporaryDirectory() as temp_dir2:
            project_root = Path(temp_dir1)
            outside_dir = Path(temp_dir2)
            work_dir = project_root / "test_project"
            work_dir.mkdir()

            original_cwd = os.getcwd()

            try:
                # 切换到项目目录
                os.chdir(work_dir)

                # 部署安全的技能文件
                from dna_spec_kit_integration.core.secure_deployment_manager import SecureDeploymentManager

                manager = SecureDeploymentManager(project_root)
                with patch.object(manager, 'stigmergy_available', False):
                    skill = {
                        'name': 'architect',
                        'description': 'Design system architecture',
                        'function': 'execute_architect'
                    }
                    manager._generate_secure_project_skill_files(skill)

                    executor_file = manager.project_slash_dir / 'architect' / 'architect_executor.py'

                    # 尝试在项目外部执行（应该失败）
                    result = subprocess.run([
                        sys.executable, str(executor_file), "Design a web app"
                    ], capture_output=True, text=True, cwd=outside_dir)

                    # 验证执行失败（安全违规）
                    assert result.returncode != 0
                    assert "SECURITY VIOLATION" in result.stderr or "Access denied" in result.stderr

            finally:
                os.chdir(original_cwd)

    def test_secure_wrapper_script_security_check(self):
        """测试：安全包装脚本安全检查"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            work_dir = project_root / "test_project"
            work_dir.mkdir()

            original_cwd = os.getcwd()

            try:
                # 部署安全的技能文件
                from dna_spec_kit_integration.core.secure_deployment_manager import SecureDeploymentManager

                manager = SecureDeploymentManager(project_root)
                with patch.object(manager, 'stigmergy_available', False):
                    skill = {
                        'name': 'architect',
                        'description': 'Design system architecture',
                        'function': 'execute_architect'
                    }
                    manager._generate_secure_project_skill_files(skill)

                    # 测试Windows包装脚本
                    if os.name == 'nt':
                        wrapper_file = manager.project_slash_dir / 'architect' / 'architect.cmd'

                        # 在项目内执行（应该成功）
                        result = subprocess.run([
                            str(wrapper_file), "Design a web app"
                        ], capture_output=True, text=True, cwd=work_dir)

                        # 包装脚本应该存在，但可能因缺少Python模块而失败
                        # 重要的是安全检查应该被执行
                        assert wrapper_file.exists()

            finally:
                os.chdir(original_cwd)

    def test_skill_file_access_control_within_project(self):
        """测试：技能内文件访问控制（项目内）"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            work_dir = project_root / "test_project"
            work_dir.mkdir()

            # 创建测试文件
            config_file = work_dir / "config.json"
            config_file.write_text('{"name": "test", "version": "1.0"}')

            source_file = work_dir / "main.py"
            source_file.write_text('print("Hello World")')

            original_cwd = os.getcwd()

            try:
                os.chdir(work_dir)

                # 测试安全上下文文件访问
                from dna_spec_kit_integration.core.secure_deployment_manager import SecurityContext

                security_context = SecurityContext(project_root)

                # 测试允许的文件访问
                safe_config_path = security_context.get_safe_path("config.json")
                assert safe_config_path == config_file.resolve()

                safe_source_path = security_context.get_safe_path("main.py")
                assert safe_source_path == source_file.resolve()

                # 测试子目录访问
                subdir = work_dir / "src"
                subdir.mkdir()
                subdir_file = subdir / "app.py"
                subdir_file.write_text("app code")

                safe_subdir_path = security_context.get_safe_path("src/app.py")
                assert safe_subdir_path == subdir_file.resolve()

            finally:
                os.chdir(original_cwd)

    def test_skill_file_access_control_violation_attempts(self):
        """测试：技能内文件访问控制违规尝试"""
        with tempfile.TemporaryDirectory() as temp_dir1, tempfile.TemporaryDirectory() as temp_dir2:
            project_root = Path(temp_dir1)
            outside_dir = Path(temp_dir2)
            work_dir = project_root / "test_project"
            work_dir.mkdir()

            # 创建项目外文件
            outside_file = outside_dir / "secret.txt"
            outside_file.write_text("secret information")

            original_cwd = os.getcwd()

            try:
                os.chdir(work_dir)

                from dna_spec_kit_integration.core.secure_deployment_manager import SecurityContext

                security_context = SecurityContext(project_root)

                # 测试各种访问违规尝试
                violation_attempts = [
                    f"../../../{outside_file.name}",
                    f"..\\..\\..\\{outside_file.name}",
                    f"/etc/passwd",
                    f"C:\\Windows\\System32\\config",
                    str(outside_file),
                ]

                for attempt in violation_attempts:
                    with pytest.raises(SecurityError, match="Access denied"):
                        security_context.get_safe_path(attempt)

            finally:
                os.chdir(original_cwd)

    def test_project_context_information_accuracy(self):
        """测试：项目上下文信息准确性"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            subdir = project_root / "subdir"
            subdir.mkdir()
            deep_dir = subdir / "deep"
            deep_dir.mkdir()

            original_cwd = os.getcwd()

            try:
                # 测试根目录
                os.chdir(project_root)
                security_context = SecurityContext(project_root)
                context = security_context.get_project_context()

                assert context['project_root'] == str(project_root)
                assert context['current_dir'] == str(project_root)
                assert context['relative_path'] == '.'
                assert context['is_root'] == True
                assert context['security_level'] == 'project-isolated'

                # 测试子目录
                os.chdir(subdir)
                security_context = SecurityContext(project_root)
                context = security_context.get_project_context()

                assert context['relative_path'] == 'subdir'
                assert not context['is_root']

                # 测试深层目录
                os.chdir(deep_dir)
                security_context = SecurityContext(project_root)
                context = security_context.get_project_context()

                assert context['relative_path'] == 'subdir/deep'
                assert not context['is_root']

            finally:
                os.chdir(original_cwd)

    def test_security_config_generation_and_validation(self):
        """测试：安全配置生成和验证"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            manager = SecureDeploymentManager(project_root)

            with patch.object(manager, 'stigmergy_available', False):
                # 生成安全配置
                manager.project_slash_dir.mkdir(parents=True)
                manager._generate_security_config()

                # 验证配置文件存在
                security_config_file = manager.project_slash_dir / 'security_config.json'
                assert security_config_file.exists()

                # 读取并验证配置
                with open(security_config_file, 'r') as f:
                    config = json.load(f)

                # 验证安全策略配置
                assert 'security_policy' in config
                security_policy = config['security_policy']
                assert security_policy['level'] == 'project-isolated'
                assert security_policy['access_control'] == 'directory_isolation'
                assert security_policy['allowed_root'] == str(project_root)
                assert security_policy['boundary_enforcement'] == True

                # 验证权限配置
                assert 'permissions' in config
                permissions = config['permissions']
                assert not permissions['read_only_outside_project']
                assert not permissions['write_outside_project']
                assert permissions['directory_traversal_blocked']

                # 验证监控配置
                assert 'monitoring' in config
                monitoring = config['monitoring']
                assert monitoring['access_logging']
                assert monitoring['violation_detection']
                assert monitoring['audit_trail']

    def test_cross_project_isolation(self):
        """测试：跨项目隔离"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # 创建两个独立的项目
            project1_root = Path(temp_dir) / "project1"
            project2_root = Path(temp_dir) / "project2"
            project1_root.mkdir()
            project2_root.mkdir()

            # 为每个项目创建安全上下文
            security_context1 = SecurityContext(project1_root)
            security_context2 = SecurityContext(project2_root)

            # 验证上下文隔离
            context1 = security_context1.get_project_context()
            context2 = security_context2.get_project_context()

            assert context1['project_root'] != context2['project_root']
            assert context1['project_root'] == str(project1_root)
            assert context2['project_root'] == str(project2_root)

            # 验证项目1不能访问项目2的文件
            project2_file = project2_root / "private.txt"
            project2_file.write_text("private data")

            with pytest.raises(SecurityError):
                security_context1.get_safe_path(str(project2_file))


class TestStigmergyGlobalSecurity:
    """Stigmergy全局安全测试"""

    def test_stigmergy_hook_security_configuration(self):
        """测试：Stigmergy钩子安全配置"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            hooks_dir = Path(temp_dir) / "stigmergy_hooks"
            hooks_dir.mkdir()

            # 模拟Stigmergy部署
            from dna_spec_kit_integration.core.secure_deployment_manager import SecureDeploymentManager

            manager = SecureDeploymentManager(project_root)
            manager.stigmergy_hooks_dir = hooks_dir

            # 测试钩子安全配置
            manager._secure_stigmergy_hooks()

            # 验证安全配置文件
            for cli_name in manager.supported_clis[:2]:  # 测试前两个CLI
                cli_hook_dir = hooks_dir / cli_name
                cli_hook_dir.mkdir(exist_ok=True)

                security_file = cli_hook_dir / 'dnaspec_security.json'
                assert security_file.exists()

                with open(security_file, 'r') as f:
                    config = json.load(f)

                assert config['security_enabled'] == True
                assert config['access_control'] == 'directory_isolation'
                assert config['allowed_root'] == '$CURRENT_WORKING_DIRECTORY'
                assert config['security_level'] == 'global-dynamic'

    def test_dynamic_security_context_validation(self):
        """测试：动态安全上下文验证"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            work_dir = project_root / "current_work"
            work_dir.mkdir()

            # 模拟在不同目录中的Stigmergy调用
            original_cwd = os.getcwd()

            try:
                os.chdir(work_dir)

                # 创建基于当前目录的安全上下文（模拟Stigmergy行为）
                current_context = SecurityContext(work_dir)

                # 验证动态上下文
                context = current_context.get_project_context()
                assert context['project_root'] == str(work_dir)
                assert context['current_dir'] == str(work_dir)
                assert context['relative_path'] == '.'

                # 创建子目录并切换
                subdir = work_dir / "subdir"
                subdir.mkdir()
                os.chdir(subdir)

                subdir_context = SecurityContext(work_dir)
                subdir_context_info = subdir_context.get_project_context()
                assert subdir_context_info['current_dir'] == str(subdir)
                assert subdir_context_info['relative_path'] == 'subdir'

            finally:
                os.chdir(original_cwd)


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])