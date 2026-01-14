"""
Integration Tests for All Skills
Verifying that all three skills work together properly
"""
import unittest
import tempfile
import shutil
from pathlib import Path
from src.agent_creator_skill import AgentCreatorSkill
from src.task_decomposer_skill import TaskDecomposerSkill
from src.constraint_generator_skill import ConstraintGeneratorSkill


class TestAllSkillsIntegration(unittest.TestCase):
    """Integration tests for all three implemented skills"""
    
    def setUp(self):
        """Set up temporary directory for workspace tests"""
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_all_skills_basic_functionality(self):
        """Verify all three skills can be instantiated and execute basic operations"""
        # Test Agent Creator
        agent_skill = AgentCreatorSkill()
        agent_result = agent_skill._execute_skill_logic("Python code reviewer", {})
        self.assertTrue(agent_result["success"])
        self.assertIn("agent_config", agent_result)
        
        # Test Task Decomposer
        task_skill = TaskDecomposerSkill()
        task_result = task_skill._execute_skill_logic(
            "Build user authentication and payment system", 
            {"workspace_base": self.temp_dir}
        )
        self.assertTrue(task_result["success"])
        self.assertIn("decomposition", task_result)
        
        # Test Constraint Generator
        constraint_skill = ConstraintGeneratorSkill()
        constraint_result = constraint_skill._execute_skill_logic(
            "Financial system with high security", 
            {"change_request": "Add cryptocurrency support"}
        )
        self.assertTrue(constraint_result["success"])
        self.assertIn("constraints", constraint_result)

    def test_skills_with_common_context_pattern(self):
        """Test that all skills follow the same execution pattern with context"""
        # All skills should accept a request string and context dict
        agent_skill = AgentCreatorSkill()
        task_skill = TaskDecomposerSkill()
        constraint_skill = ConstraintGeneratorSkill()
        
        # Common pattern: request string + context dict
        agent_result = agent_skill._execute_skill_logic("Test Agent", {"domain": "software"})
        task_result = task_skill._execute_skill_logic("Decompose Task", {"max_depth": 2})
        constraint_result = constraint_skill._execute_skill_logic("System Req", {"track_version": True})
        
        # All should succeed
        self.assertTrue(agent_result["success"])
        self.assertTrue(task_result["success"])
        self.assertTrue(constraint_result["success"])
        
        # All should have timestamp
        self.assertIn("timestamp", agent_result)
        self.assertIn("timestamp", task_result)
        self.assertIn("timestamp", constraint_result)

    def test_skills_interoperability(self):
        """Test that skills can potentially work together in a workflow"""
        # Example workflow: Create an agent to handle task decomposition with constraints
        agent_skill = AgentCreatorSkill()
        task_skill = TaskDecomposerSkill()
        constraint_skill = ConstraintGeneratorSkill()
        
        # Step 1: Create an agent for project management
        agent_result = agent_skill._execute_skill_logic(
            "Project Management Agent", 
            {"capabilities": ["decomposition", "constraint_checking"]}
        )
        self.assertTrue(agent_result["success"])
        
        # Step 2: Decompose a complex task
        task_result = task_skill._execute_skill_logic(
            "Build e-commerce platform and deploy to cloud", 
            {"max_depth": 2, "workspace_base": self.temp_dir}
        )
        self.assertTrue(task_result["success"])
        
        # Step 3: Generate constraints for the project
        constraint_result = constraint_skill._execute_skill_logic(
            "E-commerce platform with security and performance", 
            {"change_request": "Add cryptocurrency payment"}
        )
        self.assertTrue(constraint_result["success"])
        
        # Verify that outputs are structured appropriately for potential chaining
        self.assertIn("agent_config", agent_result)
        self.assertIn("decomposition", task_result)
        self.assertIn("alignment_check", constraint_result)


if __name__ == '__main__':
    unittest.main()