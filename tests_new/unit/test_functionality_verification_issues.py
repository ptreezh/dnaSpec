"""
TDD Tests for DNASPEC complete functionality verification issues
"""
import pytest
import sys
from unittest.mock import patch, MagicMock


class TestModuleImportIssues:
    """Test for module import errors in complete_functionality_verification"""

    def test_nonexistent_skill_modules_import(self):
        """Test that non-existent skill modules cause ImportError"""
        # These modules don't exist - they should raise ImportError
        with pytest.raises(ImportError):
            import src.dna_context_engineering.skills.context_analysis
        
        with pytest.raises(ImportError):
            import src.dna_context_engineering.skills.context_optimization
            
        with pytest.raises(ImportError):
            import src.dna_context_engineering.skills.cognitive_template

    def test_existing_modules_import(self):
        """Test that existing modules can be imported successfully"""
        # These modules should exist and import without issues
        import src.dna_context_engineering.skills_system_final
        import src.dna_spec_kit_integration.core.skill
        
        assert hasattr(src.dna_context_engineering.skills_system_final, 'execute')
        assert hasattr(src.dna_context_engineering.skills_system_final, 'ContextAnalysisSkill')


class TestExecuteFunctionScopeIssue:
    """Test for the execute function scope issue"""

    def test_execute_function_scope_in_test_function(self):
        """Test that execute function is accessible in the test context"""
        # This mimics the issue in the test_available_skills function
        # where execute is called but not in scope
        from src.dna_context_engineering.skills_system_final import execute
        
        # Test that execute function works when properly imported
        result = execute({'skill': 'context-analysis', 'context': 'Test'})
        assert result is not None
        assert isinstance(result, str)  # The execute function returns a string

    def test_execute_function_exists(self):
        """Test that execute function exists and is callable"""
        from src.dna_context_engineering.skills_system_final import execute
        assert callable(execute)


class TestSpecKitAdapterIssue:
    """Test for abstract class instantiation issue"""

    def test_abstract_spec_kit_adapter_cannot_be_instantiated(self):
        """Test that abstract SpecKitAdapter cannot be instantiated directly"""
        from src.dna_spec_kit_integration.adapters.spec_kit_adapter import SpecKitAdapter
        
        # This should raise TypeError because it has abstract methods
        with pytest.raises(TypeError) as exc_info:
            SpecKitAdapter()
        
        # Verify the error message mentions the abstract method
        assert "execute_skill" in str(exc_info.value)

    def test_concrete_spec_kit_adapter_can_be_instantiated(self):
        """Test that ConcreteSpecKitAdapter can be instantiated (it implements abstract methods)"""
        from src.dna_spec_kit_integration.adapters.concrete_spec_kit_adapter import ConcreteSpecKitAdapter
        
        # This should work because it implements execute_skill
        adapter = ConcreteSpecKitAdapter()
        assert adapter is not None
        assert hasattr(adapter, 'execute_skill')
        assert callable(adapter.execute_skill)


class TestAdapterIntegrationIssues:
    """Test for adapter integration problems"""

    def test_concrete_adapter_register_and_execute_skills(self):
        """Test that ConcreteSpecKitAdapter can register and execute skills properly"""
        from src.dna_spec_kit_integration.adapters.concrete_spec_kit_adapter import ConcreteSpecKitAdapter
        
        adapter = ConcreteSpecKitAdapter()
        
        # Verify skills were registered during initialization
        registered_skills = adapter.get_registered_skills()
        assert len(registered_skills) > 0
        assert 'dnaspec-context-analysis' in registered_skills
        assert 'dnaspec-context-optimization' in registered_skills
        assert 'dnaspec-cognitive-template' in registered_skills
        
        # Test skill execution
        result = adapter.execute_skill('dnaspec-context-analysis', {'params': 'test context'})
        assert isinstance(result, dict)
        assert 'success' in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])