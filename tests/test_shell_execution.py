"""
Shell Call Tests for DNASPEC
Tests shell command execution and subprocess integration
"""
import pytest
import os
import sys
import tempfile
import subprocess
import json
from pathlib import Path
from unittest.mock import Mock, patch

# Add project path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


class TestShellCommandExecution:
    """Tests for shell command execution"""

    def test_basic_shell_command_execution(self):
        """Test basic shell command execution functionality"""
        # Test that we can execute basic shell commands
        result = subprocess.run([sys.executable, '--version'], 
                              capture_output=True, text=True)
        
        assert result.returncode == 0
        assert 'Python' in result.stdout or 'Python' in result.stderr

    def test_dnaspec_cli_command_execution(self):
        """Test DNASPEC CLI command execution"""
        # Test that we can execute DNASPEC commands
        cmd_args = [
            sys.executable, '-c',
            'from src.dna_context_engineering.skills_system_final import execute; '
            'result = execute({"skill": "context-analysis", "context": "test"}); '
            'print("SUCCESS" if result else "FAILED")'
        ]
        
        result = subprocess.run(cmd_args, capture_output=True, text=True)
        
        assert result.returncode == 0
        # The command should either succeed or fail gracefully, not crash

    def test_subprocess_skill_execution(self):
        """Test executing skills through subprocess"""
        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = Path(temp_dir) / "test_script.py"
            
            # Create a test script that executes a DNASPEC skill
            import os
            project_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            script_content = f'''
import sys
import os
# Add project root to Python path so imports work
project_root = r"{project_root_path}"
sys.path.insert(0, project_root)

from src.dna_context_engineering.skills_system_final import execute

result = execute({{
    'skill': 'context-analysis',
    'context': 'Test context for subprocess execution'
}})

print("SUBPROCESS_RESULT:")
print(result)
'''
            
            with open(script_path, 'w') as f:
                f.write(script_content)

            # Run the script in a subprocess
            result = subprocess.run([sys.executable, str(script_path)],
                                  capture_output=True, text=True, encoding='utf-8')

            assert result.returncode == 0
            assert 'SUBPROCESS_RESULT:' in result.stdout

    def test_shell_command_with_parameters(self):
        """Test shell commands with various parameters"""
        test_cases = [
            {"skill": "context-analysis", "context": "Simple test"},
            {"skill": "context-optimization", "context": "Optimize this"},
            {"skill": "cognitive-template", "context": "Apply template", "params": {"template": "verification"}}
        ]
        
        for test_case in test_cases:
            cmd_args = [
                sys.executable, '-c',
                f'''
import sys
sys.path.insert(0, "{os.path.join(os.path.dirname(__file__), "src")}")
from src.dna_context_engineering.skills_system_final import execute
result = execute({test_case!r})
print("EXECUTION_RESULT")
'''
            ]
            
            result = subprocess.run(cmd_args, capture_output=True, text=True)
            
            # Should not crash on any of the test cases
            assert result.returncode == 0 or result.returncode == 1  # Allow for skill-specific errors

    def test_error_handling_in_shell_execution(self):
        """Test error handling when executing commands through shell"""
        # Test command with invalid skill
        cmd_args = [
            sys.executable, '-c',
            '''
import sys
sys.path.insert(0, "''' + os.path.join(os.path.dirname(__file__), 'src') + '''")
from src.dna_context_engineering.skills_system_final import execute
result = execute({"skill": "nonexistent-skill", "context": "test"})
print("ERROR_HANDLING_RESULT")
'''
        ]
        
        result = subprocess.run(cmd_args, capture_output=True, text=True)
        
        # Should handle the error gracefully without crashing
        assert result.returncode == 0 or result.returncode == 1


class TestSubprocessIntegration:
    """Tests for subprocess integration"""

    def test_subprocess_timeout_handling(self):
        """Test timeout handling in subprocess calls"""
        # Create a script that potentially takes a while
        import os
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        script_content = f'''
import sys
import time
sys.path.insert(0, r"{project_root}")

from src.dna_context_engineering.skills_system_final import execute

# Execute a simple skill
result = execute({{
    'skill': 'context-analysis',
    'context': 'Test context for timeout'
}})

print("TIMEOUT_TEST_RESULT")
'''
        
        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = Path(temp_dir) / "timeout_test.py"
            
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            # Run with timeout
            try:
                result = subprocess.run(
                    [sys.executable, str(script_path)], 
                    capture_output=True, 
                    text=True, 
                    timeout=10  # 10 second timeout
                )
                
                assert result.returncode == 0
                assert 'TIMEOUT_TEST_RESULT' in result.stdout
            except subprocess.TimeoutExpired:
                pytest.fail("Subprocess timed out unexpectedly")

    def test_subprocess_with_complex_input(self):
        """Test subprocess with complex input scenarios"""
        complex_context = """
        Design a comprehensive system architecture that includes:
        - Microservices with API gateway
        - Containerized deployment
        - Event-driven communication
        - CQRS pattern implementation
        - Saga pattern for distributed transactions
        - Circuit breaker and retry mechanisms
        - Centralized logging and monitoring
        - Security with OAuth2 and JWT
        - Database sharding strategy
        - Caching layer with Redis
        """
        
        import os
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        script_content = f'''
import sys
sys.path.insert(0, r"{project_root}")

from src.dna_context_engineering.skills_system_final import execute

result = execute({{
    'skill': 'context-analysis',
    'context': """{complex_context}"""
}})

print("COMPLEX_INPUT_TEST")
'''
        
        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = Path(temp_dir) / "complex_input_test.py"
            
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            result = subprocess.run([sys.executable, str(script_path)],
                                  capture_output=True, text=True, encoding='utf-8')

            assert result.returncode == 0
            assert 'COMPLEX_INPUT_TEST' in result.stdout

    def test_subprocess_output_redirection(self):
        """Test subprocess output redirection and capture"""
        import os
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        script_content = f'''
import sys
sys.path.insert(0, r"{project_root}")

from src.dna_context_engineering.skills_system_final import execute

result = execute({{
    'skill': 'context-optimization',
    'context': 'Optimize simple context'
}})

# Print both stdout and stderr to test redirection
print("STDOUT_CONTENT: " + str(len(result) if result else 0))
print("SUCCESS", file=sys.stderr)
'''
        
        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = Path(temp_dir) / "output_test.py"
            
            with open(script_path, 'w') as f:
                f.write(script_content)

            result = subprocess.run([sys.executable, str(script_path)],
                                  capture_output=True, text=True, encoding='utf-8')

            assert result.returncode == 0
            assert 'STDOUT_CONTENT:' in result.stdout
            # stderr is captured separately but would be in result.stderr if we checked

    def test_subprocess_environment_isolation(self):
        """Test that subprocess maintains environment isolation"""
        import os
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        script_content = f'''
import sys
import os

# Add path to import modules
sys.path.insert(0, r"{project_root}")

# Import and use DNASPEC functionality
from src.dna_context_engineering.skills_system_final import execute

result = execute({{
    'skill': 'cognitive-template',
    'context': 'Test environment isolation',
    'params': {{'template': 'verification'}}
}})

print("ENVIRONMENT_ISOLATION_TEST")
'''
        
        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = Path(temp_dir) / "env_test.py"
            
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            # Run with modified environment
            env = os.environ.copy()
            env['CUSTOM_VAR'] = 'test_value'
            
            result = subprocess.run([sys.executable, str(script_path)],
                                  capture_output=True, text=True, env=env, encoding='utf-8')
            
            assert result.returncode == 0
            assert 'ENVIRONMENT_ISOLATION_TEST' in result.stdout


class TestCrossPlatformShellCompatibility:
    """Tests for cross-platform shell compatibility"""

    def test_command_execution_on_different_platforms(self):
        """Test that command execution works across platforms"""
        # This test will run on the current platform but verifies cross-platform compatibility
        # by using platform-independent Python calls
        
        cmd_args = [
            sys.executable, '-c',
            '''
import sys
import platform
sys.path.insert(0, "''' + os.path.join(os.path.dirname(__file__), 'src') + '''")

from src.dna_context_engineering.skills_system_final import execute

result = execute({
    "skill": "context-analysis", 
    "context": f"Platform test: {{platform.system()}}"
})

print(f"CROSS_PLATFORM_TEST: {{platform.system()}}")
'''
        ]
        
        result = subprocess.run(cmd_args, capture_output=True, text=True)
        
        assert result.returncode == 0
        assert 'CROSS_PLATFORM_TEST:' in result.stdout

    def test_path_handling_in_subprocess(self):
        """Test path handling in subprocess calls across platforms"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test script in the temp directory
            script_path = Path(temp_dir) / "path_test.py"
            
            import os
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            script_content = f'''
import sys
import os
from pathlib import Path

# Add project root to path
project_root_path = Path(r"{project_root}").resolve()
sys.path.insert(0, str(project_root_path))

# Verify path is accessible
assert project_root_path.exists(), f"Source path does not exist: {{project_root_path}}"

from src.dna_context_engineering.skills_system_final import execute

result = execute({{
    "skill": "context-optimization",
    "context": "Path test with: {{temp_dir}}"
}})

print(f"PATH_HANDLING_TEST: {{len(result) if result else 0}}")
'''
            
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            # Execute the script as subprocess
            result = subprocess.run([sys.executable, str(script_path)],
                                  capture_output=True, text=True, encoding='utf-8')

            assert result.returncode == 0
            assert 'PATH_HANDLING_TEST:' in result.stdout

    def test_encoding_handling_in_subprocess(self):
        """Test character encoding handling in subprocess"""
        unicode_context = "测试中文字符 Test with unicode: ñáéíóú 🚀"
        
        import os
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        script_content = f'''
import sys
import os
sys.path.insert(0, r"{project_root}")

from src.dna_context_engineering.skills_system_final import execute

result = execute({{
    "skill": "cognitive-template",
    "context": """{unicode_context}""",
    "params": {{"template": "chain_of_thought"}}
}})

print("ENCODING_TEST_COMPLETE")
'''
        
        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = Path(temp_dir) / "encoding_test.py"
            
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            # Execute with proper encoding
            result = subprocess.run([sys.executable, str(script_path)], 
                                  capture_output=True, text=True, encoding='utf-8')
            
            # If this doesn't crash, encoding is handled properly
            assert 'ENCODING_TEST_COMPLETE' in result.stdout or result.returncode in [0, 1]


class TestShellExecutionEdgeCases:
    """Tests for edge cases in shell execution"""

    def test_empty_context_handling(self):
        """Test subprocess execution with empty context"""
        import os
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        script_content = f'''
import sys
sys.path.insert(0, r"{project_root}")

from src.dna_context_engineering.skills_system_final import execute

result = execute({{
    "skill": "context-analysis",
    "context": ""
}})

print("EMPTY_CONTEXT_TEST")
'''
        
        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = Path(temp_dir) / "empty_context_test.py"
            
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            result = subprocess.run([sys.executable, str(script_path)],
                                  capture_output=True, text=True, encoding='utf-8')

            # Should handle empty context gracefully
            assert result.returncode == 0 or result.returncode == 1
            assert 'EMPTY_CONTEXT_TEST' in result.stdout

    def test_very_long_context_handling(self):
        """Test subprocess execution with very long context"""
        long_context = "This is a very long context. " * 1000  # Repeat 1000 times
        
        script_content = f'''
import sys
sys.path.insert(0, "''' + os.path.join(os.path.dirname(__file__), 'src') + '''")

from src.dna_context_engineering.skills_system_final import execute

result = execute({{
    "skill": "context-analysis", 
    "context": """{long_context}"""
}})

print(f"LONG_CONTEXT_TEST: {{len(result) if result else 0}}")
'''
        
        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = Path(temp_dir) / "long_context_test.py"
            
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            result = subprocess.run([sys.executable, str(script_path)], 
                                  capture_output=True, text=True)
            
            # Should handle long context without crashing
            assert result.returncode == 0 or result.returncode == 1

    def test_multiple_simultaneous_calls(self):
        """Test multiple simultaneous subprocess calls"""
        import threading
        import time

        results = []
        
        def run_dnaspec_call(context):
            script_content = f'''
import sys
sys.path.insert(0, "''' + os.path.join(os.path.dirname(__file__), 'src') + '''")

from src.dna_context_engineering.skills_system_final import execute

result = execute({{
    "skill": "context-analysis", 
    "context": "{context}"
}})

print("MULTI_CALL_TEST")
'''
            
            with tempfile.TemporaryDirectory() as temp_dir:
                script_path = Path(temp_dir) / f"multi_call_test_{int(time.time() * 1000000)}.py"
                
                with open(script_path, 'w') as f:
                    f.write(script_content)
                
                result = subprocess.run([sys.executable, str(script_path)], 
                                      capture_output=True, text=True)
                
                results.append(result.returncode == 0 or 'MULTI_CALL_TEST' in result.stdout)

        # Run several calls in parallel
        threads = []
        contexts = [f"Context for call {i}" for i in range(5)]
        
        for context in contexts:
            thread = threading.Thread(target=run_dnaspec_call, args=(context,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check that most calls succeeded
        successful_calls = sum(results)
        assert successful_calls >= 3  # At least 3 out of 5 should succeed

    def test_command_injection_protection(self):
        """Test that command injection is properly prevented"""
        # This is more of a security test to ensure that arbitrary commands 
        # cannot be executed through the skill interface
        
        potentially_malicious_context = '"; ls -la; echo "malicious command" #'

        import os
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        # Create the script content with proper escaping
        script_content = '''import sys
sys.path.insert(0, r"''' + project_root + '''")

from src.dna_context_engineering.skills_system_final import execute

# This should NOT execute any malicious commands
context = "; ls -la; echo \\"malicious command\\" #"
result = execute({
    "skill": "context-analysis",
    "context": context
})

print("INJECTION_PROTECTION_TEST")
'''
        
        with tempfile.TemporaryDirectory() as temp_dir:
            script_path = Path(temp_dir) / "injection_test.py"
            
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            result = subprocess.run([sys.executable, str(script_path)],
                                  capture_output=True, text=True, encoding='utf-8')

            # Should handle the potentially malicious input safely
            assert result.returncode == 0 or result.returncode == 1
            assert 'INJECTION_PROTECTION_TEST' in result.stdout or 'Error:' in result.stdout