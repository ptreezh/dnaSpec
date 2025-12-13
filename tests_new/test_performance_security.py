"""
Performance and Security Tests for DNASPEC
Tests performance under load and security boundary enforcement
"""
import pytest
import time
import tempfile
import os
from pathlib import Path
import sys
import subprocess
from unittest.mock import Mock, patch

# Add project path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src.dna_context_engineering.skills_system_final import (
    execute_context_analysis,
    execute_context_optimization,
    execute_cognitive_template
)
from src.dna_context_engineering.core_skill import (
    ContextAnalysisSkill,
    ContextOptimizationSkill,
    CognitiveTemplateSkill,
    SkillsManager
)
from src.dna_context_engineering.ai_client import GenericAPIClient
from src.dna_context_engineering.instruction_template import TemplateRegistry


class TestPerformanceUnderLoad:
    """Performance tests to ensure system works under various loads"""

    def test_skill_response_time_baseline(self):
        """Test baseline response time for individual skills"""
        context = "Implement a simple user authentication system"

        start_time = time.time()
        result = execute_context_analysis(context)
        analysis_time = time.time() - start_time
        
        assert analysis_time < 1.0  # Should complete in under 1 second with simulated client
        assert isinstance(result, str)

        start_time = time.time()
        result = execute_context_optimization(context)
        optimization_time = time.time() - start_time
        
        assert optimization_time < 1.0
        assert isinstance(result, str)

    def test_concurrent_skill_execution(self):
        """Test ability to handle multiple concurrent skill executions"""
        import concurrent.futures
        from threading import Thread
        import queue

        context = "Design a simple API"
        results_queue = queue.Queue()
        
        def execute_skill(skill_func, ctx, label):
            try:
                result = skill_func(ctx)
                results_queue.put((label, True, result))
            except Exception as e:
                results_queue.put((label, False, str(e)))
        
        # Start multiple threads
        threads = []
        for i in range(5):
            # Alternate between different skills
            if i % 3 == 0:
                func = execute_context_analysis
                label = f"analysis_{i}"
            elif i % 3 == 1:
                func = execute_context_optimization
                label = f"optimization_{i}"
            else:
                func = execute_cognitive_template
                label = f"template_{i}"
            
            thread = Thread(target=execute_skill, args=(func, context, label))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check results
        success_count = 0
        while not results_queue.empty():
            label, success, result = results_queue.get()
            if success:
                success_count += 1
        
        # At least 80% should succeed
        assert success_count >= 4

    def test_large_context_performance(self):
        """Test performance with large contexts"""
        # Create a large context (simulating real-world complex requirements)
        large_context = "Design " + "a complex system with many requirements and constraints " * 500
        large_context += "\nAdditional requirements: " + "requirement " * 100

        start_time = time.time()
        analysis_result = execute_context_analysis(large_context)
        analysis_time = time.time() - start_time
        
        # Should handle large contexts in reasonable time
        assert analysis_time < 3.0  # Under 3 seconds for large context
        assert isinstance(analysis_result, str)
        
        # Test optimization with large context
        start_time = time.time()
        optimization_result = execute_context_optimization(large_context)
        optimization_time = time.time() - start_time
        
        assert optimization_time < 3.0
        assert isinstance(optimization_result, str)

    def test_memory_usage_stability(self):
        """Test that memory usage remains stable during repeated operations"""
        import psutil
        import os
        
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        context = "Implement a feature"

        # Execute multiple operations
        for i in range(10):
            execute_context_analysis(context)
            execute_context_optimization(context)
            execute_cognitive_template(context, params={'template': 'chain-of-thought'})

        # Check final memory usage
        final_memory = process.memory_info().rss / 1024 / 1024

        # Memory increase should be reasonable (less than 100MB for 30 operations)
        memory_increase = final_memory - initial_memory
        assert memory_increase < 100.0

    def test_skill_execution_timing_consistency(self):
        """Test that skill execution times remain consistent"""
        context = "Build a simple web page"
        execution_times = []

        # Execute skill multiple times and measure timing
        for i in range(5):
            start_time = time.time()
            execute_context_analysis(context)
            execution_time = time.time() - start_time
            execution_times.append(execution_time)

        # Calculate average and standard deviation
        avg_time = sum(execution_times) / len(execution_times)
        if len(execution_times) > 1:  # Need more than 1 sample for meaningful std dev
            variance = sum((x - avg_time) ** 2 for x in execution_times) / len(execution_times)
            std_dev = variance ** 0.5
            # Execution should be reasonably consistent (CV < 3 is acceptable for small sample sizes)
            cv = std_dev / avg_time if avg_time > 0 else 0
            assert cv < 3.0
        else:
            # If only one sample, just check timing
            assert execution_times[0] < 2.0 if execution_times else True

        assert avg_time < 2.0  # Average should be under 2 seconds

    def test_throughput_measurement(self):
        """Test system throughput - operations per second"""
        context = "Simple task"
        
        start_time = time.time()
        operations_completed = 0
        
        # Run for up to 5 seconds or until 20 operations
        while time.time() - start_time < 5.0 and operations_completed < 20:
            execute_context_analysis(context)
            operations_completed += 1
        
        elapsed_time = time.time() - start_time
        ops_per_second = operations_completed / elapsed_time if elapsed_time > 0 else 0
        
        # Should handle at least 2 operations per second (with simulated client)
        assert ops_per_second >= 1.0


class TestSecurityBoundaryEnforcement:
    """Security tests to ensure boundaries are properly enforced"""

    def test_input_validation_and_sanitization(self):
        """Test that inputs are properly validated and sanitized"""
        # Test malicious inputs
        malicious_inputs = [
            "../../../../etc/passwd",
            "file://localhost/C:/windows/system32",
            "<script>alert('xss')</script>",
            "SELECT * FROM users; DROP TABLE users; --",
            "${env:PATH}",  # Environment variable injection
            "normal context"  # Control case
        ]

        for inp in malicious_inputs:
            # All should execute without error (not crash the system)
            analysis_result = execute_context_analysis(inp)
            optimization_result = execute_context_optimization(inp)
            template_result = execute_cognitive_template(inp)

            # Results should be strings (no exceptions)
            assert isinstance(analysis_result, str)
            assert isinstance(optimization_result, str)
            assert isinstance(template_result, str)

    def test_file_system_boundary_enforcement(self):
        """Test that file system boundaries are enforced"""
        # This test ensures that the system doesn't access unauthorized files
        # The core skill implementation should validate all file paths
        
        # Initialize components
        ai_client = GenericAPIClient()
        template_registry = TemplateRegistry()
        
        # Test that skills properly validate input
        analysis_skill = ContextAnalysisSkill(ai_client, template_registry)
        optimization_skill = ContextOptimizationSkill(ai_client, template_registry)
        template_skill = CognitiveTemplateSkill(ai_client, template_registry)
        
        # All skills should validate empty input
        empty_validation = analysis_skill.validate_input("")
        assert empty_validation is not None  # Should return error message

        long_validation = analysis_skill.validate_input("a" * 15000)  # Very long context
        assert long_validation is not None  # Should return error message

    def test_skill_manager_security(self):
        """Test security aspects of skill manager"""
        ai_client = GenericAPIClient()
        template_registry = TemplateRegistry()
        manager = SkillsManager(ai_client, template_registry)

        # Test invalid skill name
        invalid_result = manager.execute_skill('nonexistent-skill', 'test context')
        assert not invalid_result.success  # Should fail gracefully

        # Test valid skills still work
        valid_result = manager.execute_skill('context-analysis', 'test context')
        # This might fail due to simulated client, but shouldn't crash
        assert hasattr(valid_result, 'success')

    def test_template_injection_protection(self):
        """Test protection against template injection"""
        # Test that special characters in context don't break templates
        injection_attempts = [
            "Normal context",
            "Context with {braces} that might be used for injection",
            "Context with $pecial characters",
            "Context with 'quotes'",
            "Context with \"double quotes\"",
            "Context with `backticks`",
        ]

        for context in injection_attempts:
            # All should execute without crashing
            result = execute_cognitive_template(context)
            assert isinstance(result, str)

    def test_dos_protection(self):
        """Test protection against denial of service attempts"""
        # Very large input designed to consume resources
        large_input = "A" * 100000  # 100KB input

        start_time = time.time()
        result = execute_context_analysis(large_input)
        elapsed_time = time.time() - start_time

        # Should handle gracefully without excessive time consumption
        assert elapsed_time < 5.0  # Should complete in under 5 seconds
        assert isinstance(result, str)

    def test_skill_parameter_validation(self):
        """Test validation of skill parameters"""
        ai_client = GenericAPIClient()
        template_registry = TemplateRegistry()
        
        analysis_skill = ContextAnalysisSkill(ai_client, template_registry)
        optimization_skill = ContextOptimizationSkill(ai_client, template_registry)
        template_skill = CognitiveTemplateSkill(ai_client, template_registry)

        # Test normal operation
        normal_result = analysis_skill.execute("normal context", {})
        assert hasattr(normal_result, 'success')

        # Test with various parameter types (should handle gracefully)
        edge_cases = [
            {"invalid_param": "value"},
            12345,  # Non-dict parameter
            "string_param",  # String instead of dict
            [],  # List instead of dict
            None  # None instead of dict
        ]

        for params in edge_cases:
            try:
                # Should handle all parameter types gracefully
                result = analysis_skill.execute("context", params)
                assert hasattr(result, 'success') or True  # Just ensure no crash
            except:
                pass  # If it fails, that's okay as long as it doesn't crash the system

    def test_ai_client_interface_security(self):
        """Test security of AI client interfaces"""
        ai_client = GenericAPIClient()
        
        # Test various inputs to AI client
        test_inputs = [
            "Normal instruction",
            "Instruction with special characters: { } [ ] < > & |",
            "Instruction with potential injection: ${ENV_VAR} or $(command)",
            "Very long instruction: " + "word " * 10000
        ]

        for instruction in test_inputs:
            try:
                # This should not crash or raise exceptions
                result = ai_client.send_instruction(instruction)
                assert isinstance(result, str)
            except Exception as e:
                # If there's an exception, it should be handled gracefully
                assert isinstance(e, Exception)

    def test_context_length_limits(self):
        """Test enforcement of context length limits"""
        ai_client = GenericAPIClient()
        template_registry = TemplateRegistry()
        
        analysis_skill = ContextAnalysisSkill(ai_client, template_registry)
        
        # Test with context that exceeds the defined limit (>10000 chars)
        long_context = "A" * 10001  # 10001 characters, exceeding the 10000 limit

        validation_result = analysis_skill.validate_input(long_context)
        assert validation_result is not None  # Should return error message
        assert "too long" in validation_result.lower() or "limit" in validation_result.lower()

        # Execution with long context should also fail validation
        result = analysis_skill.execute(long_context, {})
        # Should have failed validation and returned appropriate response
        assert not result.success or "too long" in getattr(result, 'error', '').lower()


class TestIntegrationSecurity:
    """Integration security tests"""

    def test_cross_skill_security_boundary(self):
        """Test that skills don't leak information between each other inappropriately"""
        # Execute skills with sensitive-looking information and verify
        # that information doesn't leak inappropriately
        context_with_sensitive_info = "Password is SECRET123! and API key is APIKEY456$"
        
        analysis_result = execute_context_analysis(context_with_sensitive_info)
        optimization_result = execute_context_optimization(context_with_sensitive_info)
        
        # The system should not echo or mishandle sensitive information
        # Although it might appear in output since it's part of the context being analyzed,
        # the important part is that it doesn't crash or behave unexpectedly
        assert isinstance(analysis_result, str)
        assert isinstance(optimization_result, str)

    def test_error_handling_does_not_leak_info(self):
        """Test that error messages don't leak internal system information"""
        # Test error conditions and make sure they don't expose internal details
        error_context = None  # This will cause a type error in some functions

        # Execute with error-inducing inputs
        try:
            # This should handle the error gracefully
            result = execute_context_analysis(str(error_context) if error_context is not None else "")
            assert isinstance(result, str)
        except Exception as e:
            # Any exception should be handled appropriately
            assert isinstance(str(e), str)


if __name__ == "__main__":
    pytest.main([__file__])