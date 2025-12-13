"""
Test utilities for DNASPEC testing framework
"""
import json
from typing import Dict, Any, List
from pathlib import Path
import tempfile
import shutil


def create_temp_project_structure() -> Path:
    """
    Create a temporary project structure for testing
    """
    temp_dir = Path(tempfile.mkdtemp(prefix="dnaspec_test_"))
    
    # Create basic project structure
    (temp_dir / "src").mkdir(exist_ok=True)
    (temp_dir / "docs").mkdir(exist_ok=True)
    (temp_dir / "tests").mkdir(exist_ok=True)
    
    # Create a sample project file
    project_spec = {
        "name": "TestProject",
        "version": "1.0.0",
        "description": "Test project for DNASPEC verification",
        "skills_used": [],
        "tasks": []
    }
    
    with open(temp_dir / "PROJECT_SPEC.json", "w", encoding="utf-8") as f:
        json.dump(project_spec, f, ensure_ascii=False, indent=2)
    
    return temp_dir


def cleanup_temp_project(temp_dir: Path):
    """
    Clean up temporary project structure
    """
    shutil.rmtree(temp_dir, ignore_errors=True)


def get_expected_skill_outputs(skill_name: str) -> Dict[str, Any]:
    """
    Get expected outputs for different skills to verify correctness
    """
    expected_outputs = {
        "context-analysis": {
            "required_fields": [
                "context_length", "token_count_estimate", "metrics",
                "suggestions", "issues", "confidence"
            ],
            "metric_keys": ["clarity", "relevance", "completeness", "consistency", "efficiency"]
        },
        "context-optimization": {
            "required_fields": [
                "original_context", "optimized_context", "applied_optimizations",
                "improvement_metrics", "optimization_summary"
            ]
        },
        "cognitive-template": {
            "required_fields": [
                "success", "template_type", "template_description",
                "original_context", "enhanced_context", "template_structure", "confidence"
            ]
        },
        "agent-creator": {
            "required_fields": [
                "name", "type", "description", "system_prompt",
                "capabilities", "tools", "personality", "specialization"
            ]
        }
    }
    
    return expected_outputs.get(skill_name, {})


def validate_skill_output(skill_name: str, output: Any) -> List[str]:
    """
    Validate skill output against expected structure
    """
    errors = []
    expected = get_expected_skill_outputs(skill_name)
    
    if not isinstance(output, dict):
        errors.append(f"Output is not a dictionary for {skill_name}")
        return errors
    
    if "required_fields" in expected:
        for field in expected["required_fields"]:
            if field not in output:
                errors.append(f"Missing required field '{field}' in {skill_name} output")
    
    return errors


def sample_test_data() -> Dict[str, str]:
    """
    Provide sample test data for different skill types
    """
    return {
        "context_analysis_context": "Design a user authentication system with OAuth integration",
        "context_optimization_context": "User login",
        "cognitive_template_context": "How to improve system performance?",
        "agent_creator_context": "Create a data analysis agent for sales reports"
    }