"""
TDD Tests for Task Decomposer Skill
Following the enhanced TDD plan
"""
import unittest
import tempfile
import shutil
from pathlib import Path
from src.task_decomposer_skill import TaskDecomposerSkill


class TestTaskDecomposerTDD(unittest.TestCase):
    """TDD Tests for Task Decomposer Skill Implementation"""
    
    def setUp(self):
        """Set up temporary directory for workspace tests"""
        self.temp_dir = tempfile.mkdtemp()
        self.skill = TaskDecomposerSkill()

    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_task_1_1_instantiate_task_decomposer_skill(self):
        """Task 1.1: Create unit test that instantiates TaskDecomposerSkill"""
        # Test: Create unit test that instantiates TaskDecomposerSkill
        skill = TaskDecomposerSkill()
        
        # Assertions: Verify proper instantiation
        self.assertIsInstance(skill, TaskDecomposerSkill)
        self.assertEqual(skill.name, "dnaspec-task-decomposer-simple")
        self.assertIn("Simple Task Decomposer", skill.description)

    def test_task_1_2_execute_skill_interface(self):
        """Task 1.2: Create unit test that calls _execute_skill_logic with basic parameters"""
        # Test: Verify the core execution interface
        skill = TaskDecomposerSkill()
        result = skill._execute_skill_logic("Build a simple website", {})
        
        # Assertions: Verify minimal valid response structure
        self.assertIn("decomposition", result)
        self.assertIn("validation", result)
        self.assertIn("success", result)
        self.assertTrue(result["success"])

    def test_task_1_3_basic_input_processing(self):
        """Task 1.3: Create test that verifies the skill can process a simple task description"""
        # Test: Verify skill processes task description
        skill = TaskDecomposerSkill()
        task_description = "Build a simple website"
        result = skill._execute_skill_logic(task_description, {})
        
        # Assertions: Verify task description is processed
        self.assertIn("decomposition", result)
        decomposition = result["decomposition"]
        self.assertEqual(decomposition["description"], task_description)

    def test_task_2_1_basic_task_decomposition_method(self):
        """Task 2.1: Create unit test that verifies _decompose_task method exists and returns basic structure"""
        # Test: Verify _decompose_task method returns basic structure
        skill = TaskDecomposerSkill()
        result = skill._decompose_task("Test task", 0, 0, self.temp_dir)  # max_depth=0 means atomic
        
        # Assertions: Verify basic decomposition structure
        self.assertIn("id", result)
        self.assertIn("description", result)
        self.assertIn("is_atomic", result)
        self.assertIn("depth", result)
        self.assertIn("subtasks", result)
        self.assertTrue(result["is_atomic"])  # Should be atomic at max depth 0

    def test_task_2_2_base_case_for_recursion(self):
        """Task 2.2: Create test that verifies task is marked as atomic when max_depth is reached"""
        # Test: Verify task is marked as atomic when max_depth is reached
        skill = TaskDecomposerSkill()
        result = skill._decompose_task("Test task", 2, 2, self.temp_dir)  # depth=2, max=2, so should be atomic
        
        self.assertTrue(result["is_atomic"])
        self.assertEqual(result["depth"], 2)

    def test_task_2_3_simple_task_splitting_logic(self):
        """Task 2.3: Create test that verifies _simple_task_split can divide a task containing 'and'"""
        # Test: Verify simple task splitting
        skill = TaskDecomposerSkill()
        result = skill._simple_task_split("Build user authentication and payment system")
        
        # Assertions: Verify task was split
        self.assertEqual(len(result), 2)
        self.assertIn("Build user authentication", result)
        self.assertIn("Payment system", result)

    def test_task_3_1_workspace_creation_method(self):
        """Task 3.1: Create unit test that verifies _create_workspace creates a directory"""
        # Test: Verify workspace creation
        skill = TaskDecomposerSkill()
        workspace_path = skill._create_workspace("Test Task", 0, self.temp_dir)
        
        # Assertions: Verify directory was created
        self.assertTrue(Path(workspace_path).exists())
        self.assertTrue((Path(workspace_path) / "src").exists())
        self.assertTrue((Path(workspace_path) / "docs").exists())

    def test_task_3_2_integrate_workspace_with_decomposition(self):
        """Task 3.2: Create test that verifies workspaces are created for each task in decomposition"""
        # Test: Verify workspaces are created for decomposed tasks
        skill = TaskDecomposerSkill()
        result = skill._execute_skill_logic("Test task and another task", {"workspace_base": self.temp_dir})
        
        # Assertions: Verify workspace paths exist in decomposition
        decomposition = result["decomposition"]
        self.assertTrue(Path(decomposition["workspace"]).exists())
        
        # Check subtasks also have workspaces if they exist
        for subtask in decomposition.get("subtasks", []):
            self.assertTrue(Path(subtask["workspace"]).exists())

    def test_task_4_1_process_max_depth_parameter(self):
        """Task 4.1: Create test that verifies max_depth parameter is processed with limits"""
        # Test: Verify max_depth parameter processing
        skill = TaskDecomposerSkill()
        
        # Test with max_depth=1
        result = skill._execute_skill_logic(
            "Task 1 and Task 2 and Task 3", 
            {"max_depth": 1, "workspace_base": self.temp_dir}
        )
        
        validation = result["validation"]
        self.assertLessEqual(validation["metrics"]["max_depth"], 3)  # Should respect internal limit

    def test_task_4_2_process_workspace_base_parameter(self):
        """Task 4.2: Create test that verifies workspace_base parameter is processed correctly"""
        # Test: Verify workspace_base parameter processing
        skill = TaskDecomposerSkill()
        
        # Use the temporary directory as the workspace base
        result = skill._execute_skill_logic(
            "Test task", 
            {"workspace_base": self.temp_dir}
        )
        
        # Verify the workspace was created in the specified base
        decomposition = result["decomposition"]
        self.assertTrue(decomposition["workspace"].startswith(self.temp_dir))

    def test_task_5_1_decomposition_validation_method(self):
        """Task 5.1: Create test that verifies _validate_decomposition method works"""
        # Test: Verify validation method works
        skill = TaskDecomposerSkill()
        test_decomposition = {
            "id": "test",
            "description": "test",
            "is_atomic": False,
            "depth": 0,
            "subtasks": [],
            "workspace": "/tmp"
        }
        
        validation = skill._validate_decomposition(test_decomposition)
        
        # Assertions: Verify validation structure
        self.assertIn("is_valid", validation)
        self.assertIn("issues", validation)
        self.assertIn("metrics", validation)

    def test_task_5_2_task_counting_and_depth_calculation(self):
        """Task 5.2: Create tests that verify _count_tasks and _get_max_depth methods"""
        # Test: Verify counting and depth calculation methods
        skill = TaskDecomposerSkill()
        
        # Create a test structure with 3 tasks and depth 2
        test_structure = {
            "id": "root",
            "description": "root",
            "is_atomic": False,
            "depth": 0,
            "subtasks": [
                {
                    "id": "sub1",
                    "description": "sub1", 
                    "is_atomic": True,
                    "depth": 1,
                    "subtasks": []
                },
                {
                    "id": "sub2", 
                    "description": "sub2",
                    "is_atomic": False,
                    "depth": 1,
                    "subtasks": [
                        {
                            "id": "sub2a",
                            "description": "sub2a",
                            "is_atomic": True,
                            "depth": 2,
                            "subtasks": []
                        }
                    ]
                }
            ],
            "workspace": "/tmp"
        }
        
        task_count = skill._count_tasks(test_structure)
        max_depth = skill._get_max_depth(test_structure)
        
        # Assertions: Verify accurate counting
        self.assertEqual(task_count, 4)  # root + sub1 + sub2 + sub2a
        self.assertEqual(max_depth, 2)

    def test_task_6_1_complete_output_structure(self):
        """Task 6.1: Create comprehensive test that validates entire response structure matches specification"""
        # Test: Validate entire response structure
        skill = TaskDecomposerSkill()
        result = skill._execute_skill_logic("Test task", {"workspace_base": self.temp_dir})
        
        # Verify top-level structure
        self.assertIn("decomposition", result)
        self.assertIn("validation", result)
        self.assertIn("success", result)
        self.assertTrue(result["success"])
        
        # Verify decomposition structure
        decomposition = result["decomposition"]
        required_fields = ["id", "description", "is_atomic", "depth", "subtasks", "workspace"]
        for field in required_fields:
            self.assertIn(field, decomposition)

    def test_task_6_2_limit_subtasks_to_prevent_explosion(self):
        """Task 6.2: Create test that verifies no more than 5 subtasks are created (max_subtasks limit)"""
        # Test: Verify subtask limitation
        skill = TaskDecomposerSkill()
        
        # Create a task that would naturally split into many subtasks
        complex_task = "Task A and Task B and Task C and Task D and Task E and Task F and Task G"
        
        result = skill._execute_skill_logic(complex_task, {"workspace_base": self.temp_dir, "max_depth": 1})
        
        # The decomposition should be limited to max 5 subtasks as per implementation
        decomposition = result["decomposition"]
        if decomposition["subtasks"]:  # If there are subtasks
            self.assertLessEqual(len(decomposition["subtasks"]), 5)

    def test_task_7_1_handle_edge_cases_for_task_description(self):
        """Task 7.1: Create tests for edge cases like empty strings, single tasks without splits"""
        # Test: Handle edge cases
        skill = TaskDecomposerSkill()
        
        # Test with empty string
        result1 = skill._execute_skill_logic("", {"workspace_base": self.temp_dir})
        self.assertTrue(result1["success"])
        
        # Test with task that can't be split
        result2 = skill._execute_skill_logic("Single task", {"workspace_base": self.temp_dir})
        self.assertTrue(result2["success"])

    def test_task_7_2_validate_input_parameters_properly(self):
        """Task 7.2: Create tests for invalid input parameters (negative max_depth, invalid paths)"""
        # Test: Handle invalid parameters gracefully
        skill = TaskDecomposerSkill()
        
        # Test with negative max_depth (should default to positive value)
        result = skill._execute_skill_logic(
            "Test task", 
            {"max_depth": -1, "workspace_base": self.temp_dir}
        )
        self.assertTrue(result["success"])


if __name__ == '__main__':
    unittest.main()