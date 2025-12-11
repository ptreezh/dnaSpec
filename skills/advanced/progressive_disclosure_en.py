"""
Progressive Disclosure Skill - Refactored Version
Compliant with DNASPEC Standardized Skill Interface Specification
"""
import os
from typing import Dict, Any, List
from ..skill_base_en import BaseSkill, DetailLevel


class ProgressiveDisclosureSkill(BaseSkill):
    """Progressive Disclosure Skill - Used to create project documentation directory structures that comply with progressive disclosure principles based on user requirements"""
    
    def __init__(self):
        super().__init__(
            name="progressive-disclosure",
            description="Used to create project documentation directory structures that comply with progressive disclosure principles based on user requirements"
        )
    
    def _execute_skill_logic(self, input_text: str, detail_level: DetailLevel, 
                          options: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute progressive disclosure skill logic"""
        project_path = options.get("project_path", ".")
        project_name = options.get("project_name", "my_project")
        disclosure_level = options.get("disclosure_level", "basic")
        
        try:
            # Create project root directory
            root_dir = os.path.join(project_path, project_name)
            os.makedirs(root_dir, exist_ok=True)
            
            created_dirs = []
            created_files = []
            
            # Create directory structure based on disclosure level
            if disclosure_level == "basic":
                created_dirs, created_files = self._create_basic_structure(root_dir)
            elif disclosure_level == "intermediate":
                created_dirs, created_files = self._create_intermediate_structure(root_dir)
            elif disclosure_level == "advanced":
                created_dirs, created_files = self._create_advanced_structure(root_dir)
            else:
                created_dirs, created_files = self._create_basic_structure(root_dir)
            
            return {
                "operation": "create-project-structure",
                "project_path": project_path,
                "project_name": project_name,
                "disclosure_level": disclosure_level,
                "result": f"Successfully created progressive disclosure directory structure for project '{project_name}', level: {disclosure_level}",
                "created_directories": created_dirs,
                "created_files": created_files
            }
            
        except Exception as e:
            return {
                "operation": "create-project-structure",
                "project_path": project_path,
                "project_name": project_name,
                "disclosure_level": disclosure_level,
                "result": f"Failed to create project directory structure: {str(e)}",
                "error": str(e)
            }
    
    def _format_output(self, result_data: Dict[str, Any], detail_level: DetailLevel) -> Dict[str, Any]:
        """Format output result based on detail level"""
        if detail_level == DetailLevel.BASIC:
            # Basic level returns core information only
            return {
                "operation": result_data["operation"],
                "result": result_data["result"],
                "project_path": result_data["project_path"]
            }
        elif detail_level == DetailLevel.STANDARD:
            # Standard level returns standard information
            return {
                "operation": result_data["operation"],
                "project_path": result_data["project_path"],
                "project_name": result_data["project_name"],
                "disclosure_level": result_data["disclosure_level"],
                "result": result_data["result"]
            }
        else:  # DETAILED
            # Detailed level returns complete information
            return result_data
    
    def _create_basic_structure(self, root_dir: str) -> tuple:
        """Create basic level directory structure"""
        # Basic directories
        dirs = [
            "docs",
            "src",
            "tests",
            "config"
        ]
        
        created_dirs = []
        created_files = []
        
        for dir_name in dirs:
            dir_path = os.path.join(root_dir, dir_name)
            os.makedirs(dir_path, exist_ok=True)
            created_dirs.append(dir_path)
        
        # Basic documentation files
        readme_path = os.path.join(root_dir, "README.md")
        self._create_file(readme_path, "# Project README\n\nBasic project documentation.")
        created_files.append(readme_path)
        
        getting_started_path = os.path.join(root_dir, "docs", "getting_started.md")
        self._create_file(getting_started_path, "# Getting Started\n\nBasic setup instructions.")
        created_files.append(getting_started_path)
        
        return created_dirs, created_files
    
    def _create_intermediate_structure(self, root_dir: str) -> tuple:
        """Create intermediate level directory structure"""
        # Intermediate directories
        dirs = [
            "docs",
            "docs/architecture",
            "docs/guides",
            "src",
            "src/core",
            "src/utils",
            "tests",
            "tests/unit",
            "tests/integration",
            "config",
            "scripts"
        ]
        
        created_dirs = []
        created_files = []
        
        for dir_name in dirs:
            dir_path = os.path.join(root_dir, dir_name)
            os.makedirs(dir_path, exist_ok=True)
            created_dirs.append(dir_path)
        
        # Intermediate documentation files
        readme_path = os.path.join(root_dir, "README.md")
        self._create_file(readme_path, "# Project README\n\nComprehensive project documentation.")
        created_files.append(readme_path)
        
        overview_path = os.path.join(root_dir, "docs", "overview.md")
        self._create_file(overview_path, "# Project Overview\n\nHigh-level project description.")
        created_files.append(overview_path)
        
        design_path = os.path.join(root_dir, "docs", "architecture", "design.md")
        self._create_file(design_path, "# Architecture Design\n\nSystem architecture overview.")
        created_files.append(design_path)
        
        development_path = os.path.join(root_dir, "docs", "guides", "development.md")
        self._create_file(development_path, "# Development Guide\n\nDevelopment workflow instructions.")
        created_files.append(development_path)
        
        return created_dirs, created_files
    
    def _create_advanced_structure(self, root_dir: str) -> tuple:
        """Create advanced level directory structure"""
        # Advanced directories
        dirs = [
            "docs",
            "docs/architecture",
            "docs/architecture/diagrams",
            "docs/guides",
            "docs/guides/contributing",
            "docs/api",
            "docs/deployment",
            "src",
            "src/core",
            "src/modules",
            "src/modules/auth",
            "src/modules/user",
            "src/shared",
            "src/utils",
            "tests",
            "tests/unit",
            "tests/integration",
            "tests/e2e",
            "config",
            "scripts",
            "scripts/build",
            "scripts/deploy",
            "scripts/test",
            "assets",
            "assets/images",
            "assets/styles"
        ]
        
        created_dirs = []
        created_files = []
        
        for dir_name in dirs:
            dir_path = os.path.join(root_dir, dir_name)
            os.makedirs(dir_path, exist_ok=True)
            created_dirs.append(dir_path)
        
        # Advanced documentation files
        readme_path = os.path.join(root_dir, "README.md")
        self._create_file(readme_path, "# Project README\n\nComplete project documentation.")
        created_files.append(readme_path)
        
        overview_path = os.path.join(root_dir, "docs", "overview.md")
        self._create_file(overview_path, "# Project Overview\n\nDetailed project description.")
        created_files.append(overview_path)
        
        design_path = os.path.join(root_dir, "docs", "architecture", "design.md")
        self._create_file(design_path, "# Architecture Design\n\nDetailed system architecture.")
        created_files.append(design_path)
        
        diagrams_path = os.path.join(root_dir, "docs", "architecture", "diagrams", "system.svg")
        self._create_file(diagrams_path, "<!-- System Architecture Diagram -->")
        created_files.append(diagrams_path)
        
        development_path = os.path.join(root_dir, "docs", "guides", "development.md")
        self._create_file(development_path, "# Development Guide\n\nComplete development workflow.")
        created_files.append(development_path)
        
        style_guide_path = os.path.join(root_dir, "docs", "guides", "contributing", "style_guide.md")
        self._create_file(style_guide_path, "# Style Guide\n\nCoding standards and conventions.")
        created_files.append(style_guide_path)
        
        api_path = os.path.join(root_dir, "docs", "api", "reference.md")
        self._create_file(api_path, "# API Reference\n\nAPI documentation.")
        created_files.append(api_path)
        
        deployment_path = os.path.join(root_dir, "docs", "deployment", "instructions.md")
        self._create_file(deployment_path, "# Deployment Instructions\n\nDeployment procedures.")
        created_files.append(deployment_path)
        
        return created_dirs, created_files
    
    def _create_file(self, file_path: str, content: str):
        """Create file and write content"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)