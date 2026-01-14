#!/usr/bin/env python3
"""
spec.kit management script

This script provides utilities for managing spec.kit projects,
including initializing new projects, managing templates, and
validating specifications.
"""

import os
import sys
import argparse
from pathlib import Path


def initialize_project(project_name):
    """Initialize a new spec.kit project with basic structure."""
    print(f"Initializing new spec.kit project: {project_name}")
    
    # Create project directory
    project_path = Path(project_name)
    project_path.mkdir(exist_ok=True)
    
    # Create subdirectories
    (project_path / ".speckit").mkdir(exist_ok=True)
    (project_path / ".speckit" / "specs").mkdir(exist_ok=True)
    (project_path / ".speckit" / "plans").mkdir(exist_ok=True)
    (project_path / ".speckit" / "tasks").mkdir(exist_ok=True)
    
    # Create initial files
    readme_content = f"# {project_name}\n\nProject initialized with spec.kit\n"
    (project_path / "README.md").write_text(readme_content)
    
    print(f"Project {project_name} initialized successfully!")
    print("You can now use spec.kit commands in your AI agent.")


def validate_specification(spec_path):
    """Validate a specification file."""
    spec_file = Path(spec_path)
    if not spec_file.exists():
        print(f"Specification file does not exist: {spec_path}")
        return False
    
    content = spec_file.read_text()
    
    # Basic validation checks
    required_sections = ["Problem Statement", "Requirements", "Success Metrics"]
    missing_sections = []
    
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)
    
    if missing_sections:
        print(f"Specification validation failed. Missing sections: {', '.join(missing_sections)}")
        return False
    else:
        print("Specification validation passed!")
        return True


def main():
    parser = argparse.ArgumentParser(description="spec.kit management utilities")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize a new spec.kit project")
    init_parser.add_argument("project_name", help="Name of the project to initialize")
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate a specification file")
    validate_parser.add_argument("spec_path", help="Path to the specification file")
    
    args = parser.parse_args()
    
    if args.command == "init":
        initialize_project(args.project_name)
    elif args.command == "validate":
        validate_specification(args.spec_path)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()