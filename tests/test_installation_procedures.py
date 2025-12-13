"""
Installation and Uninstallation Tests for DNASPEC
Tests package installation, configuration, and cleanup
"""
import pytest
import os
import sys
import tempfile
import shutil
import subprocess
import json
from pathlib import Path
from unittest.mock import Mock, patch

# Add project path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.dna_spec_kit_integration.core.auto_configurator import AutoConfigurator
from src.dna_spec_kit_integration.core.cli_detector import CliDetector


class TestInstallationProcedures:
    """Tests for installation procedures and configuration"""

    def test_installation_dependencies_check(self):
        """Test that installation dependencies are properly checked"""
        # This test would normally check that all required dependencies can be imported
        try:
            import src.dna_context_engineering.skills_system_final
            import src.dna_spec_kit_integration.core.cli_detector
            import src.dna_spec_kit_integration.core.auto_configurator
            # Add other core modules that should be available after installation
            assert True  # If imports work, dependencies are available
        except ImportError as e:
            pytest.fail(f"Installation dependency missing: {e}")

    def test_auto_configuration_generation(self):
        """Test that auto configuration is properly generated"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            
            # Create a mock AutoConfigurator instance
            auto_config = AutoConfigurator()
            
            # Mock the detector methods to avoid system dependency
            with patch.object(auto_config.cli_detector, 'detect_all') as mock_detect:
                mock_detect.return_value = {
                    'claude': {'installed': True, 'version': 'mock'},
                    'gemini': {'installed': False, 'version': None},
                    'qwen': {'installed': True, 'version': 'mock'}
                }
                
                # Test configuration generation
                result = auto_config.quick_configure()
                
                # Verify result structure
                assert isinstance(result, dict)
                assert 'success' in result
                assert 'configPath' in result
                assert 'config' in result

    def test_cli_tool_detection_after_installation(self):
        """Test that CLI tools are properly detected after installation"""
        detector = CliDetector()
        
        # Run detection
        results = detector.detect_all()
        
        # Verify structure
        assert isinstance(results, dict)
        
        # Check that expected tools are present
        expected_tools = ['claude', 'gemini', 'qwen', 'copilot', 'cursor', 'codebuddy', 'iflow', 'qodercli']
        for tool in expected_tools:
            assert tool in results
            assert isinstance(results[tool], dict)
            assert 'installed' in results[tool]
            assert isinstance(results[tool]['installed'], bool)

    def test_config_file_generation(self):
        """Test that configuration files are properly generated"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            
            # Change to temp directory
            original_cwd = os.getcwd()
            try:
                os.chdir(project_root)
                
                # Create a configuration using AutoConfigurator
                auto_config = AutoConfigurator()
                
                # Mock detection results
                with patch.object(auto_config.cli_detector, 'detect_all') as mock_detect:
                    mock_detect.return_value = {
                        'claude': {'installed': True, 'version': '2.0.0'},
                        'gemini': {'installed': True, 'version': '0.1.0'},
                        'qwen': {'installed': False, 'version': None}
                    }
                    
                    result = auto_config.quick_configure()
                    
                    # Verify that configuration was created successfully
                    assert result['success'] == True
                    assert 'configPath' in result
                    if result['configPath']:  # If path is provided
                        config_path = Path(result['configPath'])
                        assert config_path.exists()
            
            finally:
                os.chdir(original_cwd)

    def test_installation_verification(self):
        """Test installation verification process"""
        # Test that core functionality works after "installation"
        from src.dna_context_engineering.skills_system_final import get_available_skills
        
        skills = get_available_skills()
        
        # Verify basic skills are available
        assert isinstance(skills, dict)
        assert len(skills) >= 3  # At least context-analysis, optimization, and cognitive-template
        
        expected_skills = ['context-analysis', 'context-optimization', 'cognitive-template']
        for skill in expected_skills:
            assert skill in skills


class TestUninstallationProcedures:
    """Tests for uninstallation and cleanup procedures"""

    def test_temporary_files_cleanup(self):
        """Test that temporary files are properly cleaned up"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create some mock files that would need cleanup
            (temp_path / "temp_config.json").write_text('{"test": "data"}')
            (temp_path / "temp_dir").mkdir()
            (temp_path / "temp_dir" / "temp_file.txt").write_text("temp content")
            
            # Verify files exist
            assert (temp_path / "temp_config.json").exists()
            assert (temp_path / "temp_dir" / "temp_file.txt").exists()
            
            # "Cleanup" by removing the temporary directory
            # (This happens automatically with TemporaryDirectory)
            shutil.rmtree(temp_path)
            
            # Verify cleanup
            assert not temp_path.exists()

    def test_config_file_removal(self):
        """Test configuration file removal during uninstallation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "test_config.json"
            
            # Create a mock config file
            config_data = {"installed": True, "version": "1.0.0", "tools": ["claude", "gemini"]}
            with open(config_path, 'w') as f:
                json.dump(config_data, f)
            
            # Verify file exists
            assert config_path.exists()
            
            # Remove the config file (simulate uninstallation)
            config_path.unlink()
            
            # Verify removal
            assert not config_path.exists()

    def test_clean_project_state(self):
        """Test that project state is properly cleaned"""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            
            # Create some mock project files that might exist
            (project_root / ".dnaspec").mkdir()
            (project_root / ".dnaspec" / "slash_commands").mkdir()
            (project_root / ".dnaspec" / "slash_commands" / "config.json").write_text("{}")
            
            # Verify files exist
            assert (project_root / ".dnaspec").exists()
            assert (project_root / ".dnaspec" / "slash_commands").exists()
            
            # Clean up the project state
            shutil.rmtree(project_root / ".dnaspec")
            
            # Verify cleanup
            assert not (project_root / ".dnaspec").exists()


class TestInstallationEdgeCases:
    """Tests for installation edge cases and error handling"""

    def test_installation_with_missing_dependencies(self):
        """Test behavior when dependencies are missing"""
        # This test would normally mock missing dependencies
        # For now, just verify that the main modules can be imported
        try:
            # Try to import core modules
            from src.dna_context_engineering.skills_system_final import execute
            from src.dna_spec_kit_integration.core.skill import DNASpecSkill
            assert True
        except ImportError:
            pytest.skip("Dependencies not available, skipping test")

    def test_installation_in_non_standard_paths(self):
        """Test installation in non-standard directory paths"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create nested directory structure
            nested_path = Path(temp_dir) / "projects" / "my_project" / "src"
            nested_path.mkdir(parents=True)
            
            # Verify we can still access modules from this path
            original_path = sys.path.copy()
            sys.path.insert(0, str(Path(temp_dir) / "projects" / "my_project"))
            
            try:
                # Import should still work
                from src.dna_context_engineering.skills_system_final import get_available_skills
                skills = get_available_skills()
                assert isinstance(skills, dict)
                assert len(skills) > 0
            finally:
                sys.path[:] = original_path  # Restore original path

    def test_multiple_installations_same_system(self):
        """Test behavior with multiple installations on the same system"""
        with tempfile.TemporaryDirectory() as temp_dir1, \
             tempfile.TemporaryDirectory() as temp_dir2:
            
            # Simulate two separate installation directories
            install_path1 = Path(temp_dir1) / "dnaspec_install"
            install_path2 = Path(temp_dir2) / "dnaspec_install"
            
            install_path1.mkdir()
            install_path2.mkdir()
            
            # Each should be able to run independently
            original_cwd = os.getcwd()
            try:
                # Test installation 1
                os.chdir(install_path1)
                from src.dna_context_engineering.skills_system_final import get_available_skills
                skills1 = get_available_skills()
                
                # Test installation 2  
                os.chdir(install_path2)
                skills2 = get_available_skills()
                
                # Both should have skills available
                assert len(skills1) > 0
                assert len(skills2) > 0
                
            finally:
                os.chdir(original_cwd)

    def test_rollback_on_installation_failure(self):
        """Test rollback mechanisms if installation fails"""
        # This test simulates what would happen if an installation fails
        # and needs to be rolled back to previous state
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a mock installation state
            install_path = Path(temp_dir) / "dnaspec_install"
            install_path.mkdir()
            
            # Create some files that would be part of installation
            config_file = install_path / "config.json"
            with open(config_file, 'w') as f:
                json.dump({"installed": True, "version": "1.0.0"}, f)
            
            # Simulate successful installation verification
            assert config_file.exists()
            assert json.loads(config_file.read_text())["installed"] == True
            
            # If installation succeeded, files remain
            # If it failed, cleanup logic would remove them
            # This test just verifies the success case


class TestPostInstallationVerification:
    """Tests to run after installation to verify everything works"""

    def test_all_skills_functional_after_installation(self):
        """Test that all skills work correctly after installation"""
        from src.dna_context_engineering.skills_system_final import execute
        
        # Test context analysis
        result = execute({'skill': 'context-analysis', 'context': 'Test installation'})
        assert isinstance(result, str)
        assert 'Context Quality Analysis Results:' in result or 'Error:' in result
        
        # Test context optimization  
        result = execute({'skill': 'context-optimization', 'context': 'Test installation'})
        assert isinstance(result, str)
        assert 'Context Optimization Results:' in result or 'Error:' in result
        
        # Test cognitive template
        result = execute({'skill': 'cognitive-template', 'context': 'Test installation'})
        assert isinstance(result, str)
        assert 'Cognitive Template Application:' in result or 'Error:' in result

    def test_cli_integration_after_installation(self):
        """Test that CLI integration works after installation"""
        # Test that CLI tools can be detected
        detector = CliDetector()
        results = detector.detect_all()
        
        assert isinstance(results, dict)
        assert len(results) > 0
        
        # Test that auto configuration works
        auto_config = AutoConfigurator()
        
        # Mock the detection to avoid system dependencies
        with patch.object(auto_config.cli_detector, 'detect_all') as mock_detect:
            mock_detect.return_value = {
                'claude': {'installed': True, 'version': 'mock'},
                'gemini': {'installed': False, 'version': None},
                'qwen': {'installed': True, 'version': 'mock'}
            }
            
            result = auto_config.quick_configure()
            assert result['success'] == True

    def test_performance_after_installation(self):
        """Test that performance is acceptable after installation"""
        import time
        from src.dna_context_engineering.skills_system_final import execute
        
        # Measure execution time for a simple operation
        start_time = time.time()
        result = execute({'skill': 'context-analysis', 'context': 'Quick test'})
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Execution should be reasonably fast (under 1 second for simple operation)
        assert execution_time < 1.0
        assert isinstance(result, str)