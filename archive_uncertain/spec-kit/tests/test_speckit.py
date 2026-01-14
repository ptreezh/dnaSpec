import pytest
import tempfile
import os
from pathlib import Path

# Import the management functions
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.manage_speckit import initialize_project, validate_specification


def test_initialize_project():
    """Test project initialization functionality."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_name = "test_project"
        project_path = Path(temp_dir) / project_name
        
        # Run initialization
        initialize_project(str(project_path))
        
        # Verify structure
        assert project_path.exists()
        assert (project_path / "README.md").exists()
        assert (project_path / ".speckit").exists()
        assert (project_path / ".speckit" / "specs").exists()
        assert (project_path / ".speckit" / "plans").exists()
        assert (project_path / ".speckit" / "tasks").exists()
        
        # Verify README content
        readme_content = (project_path / "README.md").read_text()
        assert project_name in readme_content
        assert "spec.kit" in readme_content


def test_validate_specification():
    """Test specification validation functionality."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a valid specification
        spec_path = Path(temp_dir) / "valid_spec.md"
        spec_content = """
# Project Specification

## 1. Problem Statement
This is the problem statement.

## 2. Requirements
These are the requirements.

## 3. Success Metrics
These are the success metrics.
"""
        spec_path.write_text(spec_content)
        
        # Test valid specification
        result = validate_specification(str(spec_path))
        assert result is True
        
        # Create an invalid specification
        invalid_spec_path = Path(temp_dir) / "invalid_spec.md"
        invalid_spec_content = """
# Project Specification

## 1. Introduction
This is an incomplete specification.
"""
        invalid_spec_path.write_text(invalid_spec_content)
        
        # Test invalid specification
        result = validate_specification(str(invalid_spec_path))
        assert result is False


if __name__ == "__main__":
    # Run tests
    test_initialize_project()
    test_validate_specification()
    print("All tests passed!")