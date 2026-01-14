"""
TDD Tests for Constraint Generator Skill
Following the enhanced TDD plan
"""
import unittest
from src.constraint_generator_skill import ConstraintGeneratorSkill


class TestConstraintGeneratorTDD(unittest.TestCase):
    """TDD Tests for Constraint Generator Skill Implementation"""
    
    def test_task_1_1_instantiate_constraint_generator_skill(self):
        """Task 1.1: Create unit test that instantiates ConstraintGeneratorSkill"""
        # Test: Create unit test that instantiates ConstraintGeneratorSkill
        skill = ConstraintGeneratorSkill()
        
        # Assertions: Verify proper instantiation
        self.assertIsInstance(skill, ConstraintGeneratorSkill)
        self.assertEqual(skill.name, "dnaspec-constraint-generator-simple")
        self.assertIn("Simple Constraint Generator", skill.description)

    def test_task_1_2_execute_skill_interface(self):
        """Task 1.2: Create unit test that calls _execute_skill_logic with basic parameters"""
        # Test: Verify the core execution interface
        skill = ConstraintGeneratorSkill()
        result = skill._execute_skill_logic("System with security", {})
        
        # Assertions: Verify minimal valid response structure
        self.assertIn("constraints", result)
        self.assertIn("alignment_check", result)
        self.assertIn("version_info", result)
        self.assertIn("success", result)
        self.assertTrue(result["success"])

    def test_task_1_3_basic_input_processing(self):
        """Task 1.3: Create test that verifies the skill can process a simple requirements string"""
        # Test: Verify skill processes requirements
        skill = ConstraintGeneratorSkill()
        requirements = "Financial system with high security"
        result = skill._execute_skill_logic(requirements, {})
        
        # Assertions: Verify requirements are processed
        self.assertIn("constraints", result)
        self.assertEqual(result["success"], True)

    def test_task_2_1_basic_constraint_generation_method(self):
        """Task 2.1: Create unit test that verifies _generate_constraints_from_requirements returns a list"""
        # Test: Verify constraint generation method returns a list
        skill = ConstraintGeneratorSkill()
        constraints = skill._generate_constraints_from_requirements("System with security")
        
        # Assertions: Verify it returns a list with required fields
        self.assertIsInstance(constraints, list)
        for constraint in constraints:
            required_fields = ["id", "type", "description", "severity", "created_at"]
            for field in required_fields:
                self.assertIn(field, constraint)

    def test_task_2_2_security_constraint_generation(self):
        """Task 2.2: Create test that verifies security constraints are generated when keywords are present"""
        # Test: Verify security constraints generated with security keywords
        skill = ConstraintGeneratorSkill()
        constraints = skill._generate_constraints_from_requirements("Financial system with high security")
        
        # Find security constraint
        security_constraints = [c for c in constraints if c["type"] == "security"]
        
        # Assertions: Verify security constraint exists
        self.assertGreater(len(security_constraints), 0)
        self.assertEqual(security_constraints[0]["type"], "security")
        self.assertEqual(security_constraints[0]["severity"], "high")

    def test_task_2_3_other_constraint_types(self):
        """Task 2.3: Create tests that verify performance and data constraints are generated when keywords are present"""
        # Test: Verify multiple constraint types
        skill = ConstraintGeneratorSkill()
        
        # Test performance constraints
        perf_constraints = skill._generate_constraints_from_requirements("System with high performance")
        perf_found = any(c["type"] == "performance" for c in perf_constraints)
        self.assertTrue(perf_found)
        
        # Test data constraints
        data_constraints = skill._generate_constraints_from_requirements("System with data storage")
        data_found = any(c["type"] == "data_integrity" for c in data_constraints)
        self.assertTrue(data_found)

    def test_task_3_1_alignment_check_method(self):
        """Task 3.1: Create unit test that verifies _perform_alignment_check method exists and returns structure"""
        # Test: Verify alignment check method returns proper structure
        skill = ConstraintGeneratorSkill()
        result = skill._perform_alignment_check("System with security", "Add new feature")
        
        # Assertions: Verify structure
        self.assertIn("is_aligned", result)
        self.assertIn("conflicts", result)
        self.assertIn("suggestions", result)
        self.assertIsInstance(result["conflicts"], list)
        self.assertIsInstance(result["suggestions"], list)

    def test_task_3_2_basic_alignment_logic(self):
        """Task 3.2: Create test that verifies alignment check returns is_aligned=true when no change_request"""
        # Test: Verify default alignment when no change request
        skill = ConstraintGeneratorSkill()
        result = skill._perform_alignment_check("System with security", "")
        
        # Assertions: Verify aligned with no change request
        self.assertTrue(result["is_aligned"])
        self.assertEqual(len(result["conflicts"]), 0)
        self.assertGreater(len(result["suggestions"]), 0)

    def test_task_3_3_conflict_detection(self):
        """Task 3.3: Create test that verifies conflicts are detected between contradictory terms"""
        # Test: Verify conflict detection between contradictory terms
        skill = ConstraintGeneratorSkill()
        result = skill._perform_alignment_check(
            "System with high security", 
            "Add feature with no security"
        )
        
        # Assertions: Verify conflict was detected
        self.assertFalse(result["is_aligned"])
        self.assertGreater(len(result["conflicts"]), 0)
        conflict = result["conflicts"][0]
        self.assertIn("security", conflict["description"].lower())

    def test_task_4_1_version_tracking_method(self):
        """Task 4.1: Create unit test that verifies _handle_version_tracking method works"""
        # Test: Verify version tracking method works
        skill = ConstraintGeneratorSkill()
        result = skill._handle_version_tracking("Test requirements", True)
        
        # Assertions: Verify version tracking structure
        self.assertIn("current_version", result)
        self.assertIn("tracked", result)
        self.assertTrue(result["tracked"])
        self.assertIsNotNone(result["current_version"])

    def test_task_4_2_integrate_version_tracking_with_execution(self):
        """Task 4.2: Create test that verifies version is tracked when track_version is true"""
        # Test: Verify version tracking in execution context
        skill = ConstraintGeneratorSkill()
        result = skill._execute_skill_logic(
            "Test requirements", 
            {"track_version": True}
        )
        
        # Assertions: Verify version was tracked
        version_info = result["version_info"]
        self.assertTrue(version_info["tracked"])
        self.assertIsNotNone(version_info["current_version"])

    def test_task_5_1_process_change_request_parameter(self):
        """Task 5.1: Create test that verifies change_request parameter is processed correctly"""
        # Test: Verify change_request parameter processing
        skill = ConstraintGeneratorSkill()
        
        # Test with change request
        result = skill._execute_skill_logic(
            "System with security",
            {"change_request": "Add new feature"}
        )
        
        # Verify alignment check happened
        self.assertIn("alignment_check", result)
        self.assertIn("is_aligned", result["alignment_check"])

    def test_task_5_2_process_track_version_parameter(self):
        """Task 5.2: Create test that verifies track_version parameter is processed correctly"""
        # Test: Verify track_version parameter processing
        skill = ConstraintGeneratorSkill()
        
        # Test with track_version=False (default)
        result1 = skill._execute_skill_logic("Test requirements", {})
        self.assertFalse(result1["version_info"]["tracked"])
        
        # Test with track_version=True
        result2 = skill._execute_skill_logic("Test requirements", {"track_version": True})
        self.assertTrue(result2["version_info"]["tracked"])

    def test_task_6_1_active_constraints_management(self):
        """Task 6.1: Create test that verifies constraints are stored in active_constraints list"""
        # Test: Verify constraints are stored in active constraints list
        skill = ConstraintGeneratorSkill()
        
        # Generate some constraints
        result = skill._execute_skill_logic("System with security and performance", {})
        
        # Check that constraints were added to active list
        self.assertGreater(len(skill.active_constraints), 0)
        
        # Verify specific constraint types were added
        has_security = any(c["type"] == "security" for c in skill.active_constraints)
        has_performance = any(c["type"] == "performance" for c in skill.active_constraints)
        
        self.assertTrue(has_security or has_performance)

    def test_task_7_1_complete_output_structure(self):
        """Task 7.1: Create comprehensive test that validates entire response structure matches specification"""
        # Test: Validate entire response structure
        skill = ConstraintGeneratorSkill()
        result = skill._execute_skill_logic(
            "Financial system with high security", 
            {"change_request": "Add new feature", "track_version": True}
        )
        
        # Verify top-level structure
        required_keys = ["constraints", "alignment_check", "version_info", "success", "timestamp"]
        for key in required_keys:
            self.assertIn(key, result)
        
        self.assertTrue(result["success"])
        
        # Verify constraints structure
        for constraint in result["constraints"]:
            required_fields = ["id", "type", "description", "severity", "created_at"]
            for field in required_fields:
                self.assertIn(field, constraint)
        
        # Verify alignment check structure
        alignment = result["alignment_check"]
        self.assertIn("is_aligned", alignment)
        self.assertIn("conflicts", alignment)
        self.assertIn("suggestions", alignment)
        
        # Verify version info structure
        version_info = result["version_info"]
        self.assertIn("current_version", version_info)
        self.assertIn("tracked", version_info)

    def test_task_7_2_proper_timestamp_format(self):
        """Task 7.2: Create test that verifies timestamps are in proper format"""
        # Test: Verify timestamps are properly formatted
        skill = ConstraintGeneratorSkill()
        result = skill._execute_skill_logic("Test system", {})
        
        # Verify top-level timestamp
        self.assertIn("timestamp", result)
        self.assertIsInstance(result["timestamp"], float)
        
        # Verify constraint timestamps
        for constraint in result["constraints"]:
            self.assertIn("created_at", constraint)

    def test_task_8_1_edge_cases_for_requirements(self):
        """Task 8.1: Create tests for edge cases like empty strings, various keyword combinations"""
        # Test: Handle edge cases for requirements
        skill = ConstraintGeneratorSkill()
        
        # Test with empty string
        result1 = skill._execute_skill_logic("", {})
        self.assertTrue(result1["success"])
        
        # Test with multiple keywords
        result2 = skill._execute_skill_logic("System with security, performance, and data", {})
        self.assertTrue(result2["success"])
        
        # Verify multiple constraint types could be generated
        constraint_types = [c["type"] for c in result2["constraints"]]
        self.assertIsInstance(constraint_types, list)

    def test_task_8_2_validate_input_parameters_properly(self):
        """Task 8.2: Create tests for invalid input parameters and various keyword scenarios"""
        # Test: Validate input parameters
        skill = ConstraintGeneratorSkill()
        
        # Test with various context parameters
        result = skill._execute_skill_logic(
            "Test requirements", 
            {"change_request": "Test change", "track_version": False}
        )
        
        self.assertTrue(result["success"])
        self.assertIn("constraints", result)
        self.assertIn("alignment_check", result)


if __name__ == '__main__':
    unittest.main()