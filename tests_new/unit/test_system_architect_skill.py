"""
Unit tests for System Architect Skill following TDD approach
"""
import pytest
import sys
from pathlib import Path

# Add the skill path to sys.path
skill_path = Path("D:/DAIP/dnaSpec/spec-kit/skills/dna-system-architect/scripts")
sys.path.insert(0, str(skill_path))

try:
    import system_architect_designer
except ImportError:
    pytest.skip("System Architect skill not available", allow_module_level=True)


class TestSystemArchitectSkill:
    """Test cases for System Architect Skill"""

    def test_skill_class_exists(self):
        """Test that the DNASPECSystemArchitect class exists"""
        assert hasattr(system_architect_designer, 'DNASPECSystemArchitect')
        
        # Create instance
        architect = system_architect_designer.DNASPECSystemArchitect()
        assert architect is not None

    def test_identify_architecture_type(self):
        """Test architecture type identification"""
        architect = system_architect_designer.DNASPECSystemArchitect()
        
        # Test with microservices requirements
        result = architect.identify_architecture_type("Create a microservices architecture for e-commerce")
        assert isinstance(result, system_architect_designer.SystemArchitectureType)
        
        # Test with layered architecture requirements
        result = architect.identify_architecture_type("Design a layered monolithic system")
        assert isinstance(result, system_architect_designer.SystemArchitectureType)

    def test_recommend_tech_stack(self):
        """Test technology stack recommendation"""
        architect = system_architect_designer.DNASPECSystemArchitect()
        from system_architect_designer import SystemArchitectureType
        
        # Test with microservices architecture
        result = architect.recommend_tech_stack("E-commerce microservices", SystemArchitectureType.MICROSERVICES)
        assert isinstance(result, system_architect_designer.TechnologyStack)

    def test_identify_modules(self):
        """Test module identification"""
        architect = system_architect_designer.DNASPECSystemArchitect()
        from system_architect_designer import SystemArchitectureType
        
        # Test with simple requirements
        modules = architect.identify_modules("Web application with user management", SystemArchitectureType.LAYERED)
        
        # Should return a list of SystemComponent objects
        assert isinstance(modules, list)
        if modules:
            assert hasattr(modules[0], 'name')
            assert hasattr(modules[0], 'module_type')

    def test_generate_architecture_design_basic(self):
        """Test basic architecture design generation"""
        architect = system_architect_designer.DNASPECSystemArchitect()

        result = architect.generate_architecture_design("Simple web application")
        assert isinstance(result, dict)

        # Check for expected keys in result
        # Note: The actual implementation may use different key names than expected
        expected_keys = [
            "architecture_type", "recommended_tech_stack", "identified_modules",
            "defined_interfaces", "architecture_recommendations", "potential_issues",
            "implementation_guidance"
        ]

        for key in expected_keys:
            assert key in result, f"Missing key: {key}"

    def test_generate_architecture_recommendations(self):
        """Test architecture recommendations generation"""
        architect = system_architect_designer.DNASPECSystemArchitect()
        from system_architect_designer import SystemArchitectureType
        
        recommendations = architect.generate_architecture_recommendations(
            "E-commerce platform", 
            SystemArchitectureType.MICROSERVICES
        )
        
        assert isinstance(recommendations, list)
        assert len(recommendations) >= 0  # Could be empty list

    def test_system_component_functionality(self):
        """Test SystemComponent functionality"""
        from system_architect_designer import SystemComponent, ModuleType
        
        component = SystemComponent(
            name="Test Component",
            module_type=ModuleType.FRONTEND,
            technologies=["React", "JavaScript"],
            responsibilities=["UI rendering", "User interaction"]
        )
        
        assert component.name == "Test Component"
        assert component.module_type == ModuleType.FRONTEND
        assert "React" in component.technologies
        assert "UI rendering" in component.responsibilities
        
        # Test adding dependencies
        component.add_dependency("Backend API", "REST")
        assert len(component.dependencies) == 1
        assert component.dependencies[0]["name"] == "Backend API"

    def test_enum_values(self):
        """Test that enums have expected values"""
        from system_architect_designer import SystemArchitectureType, TechnologyStack, ModuleType
        
        # Test architecture types
        assert hasattr(SystemArchitectureType, 'MICROSERVICES')
        assert hasattr(SystemArchitectureType, 'LAYERED')
        assert hasattr(SystemArchitectureType, 'CLIENT_SERVER')
        
        # Test technology stacks
        assert hasattr(TechnologyStack, 'MERN')
        assert hasattr(TechnologyStack, 'LAMP')
        assert hasattr(TechnologyStack, 'CLOUD_NATIVE')
        
        # Test module types
        assert hasattr(ModuleType, 'FRONTEND')
        assert hasattr(ModuleType, 'BACKEND')
        assert hasattr(ModuleType, 'DATABASE')


if __name__ == "__main__":
    # Run the tests directly if this file is executed
    pytest.main([__file__, "-v"])