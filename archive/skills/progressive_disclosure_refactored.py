"""
渐进披露技能 - 重构版本
符合DNASPEC标准化技能接口规范
"""
import os
from typing import Dict, Any, List
from src.dna_spec_kit_integration.core.skill_base import BaseSkill, DetailLevel


class ProgressiveDisclosureSkill(BaseSkill):
    """渐进披露技能 - 用于根据用户需求创建符合渐进披露原则的项目文档目录结构"""
    
    def __init__(self):
        super().__init__(
            name="progressive-disclosure",
            description="用于根据用户需求创建符合渐进披露原则的项目文档目录结构"
        )
    
    def _execute_skill_logic(self, input_text: str, detail_level: DetailLevel, 
                          options: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """执行渐进披露技能逻辑"""
        project_path = options.get("project_path", ".")
        project_name = options.get("project_name", "my_project")
        disclosure_level = options.get("disclosure_level", "basic")
        
        try:
            # 创建项目根目录
            root_dir = os.path.join(project_path, project_name)
            os.makedirs(root_dir, exist_ok=True)
            
            created_dirs = []
            created_files = []
            
            # 根据披露级别创建目录结构
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
                "result": f"成功创建项目 '{project_name}' 的渐进披露目录结构，级别: {disclosure_level}",
                "created_directories": created_dirs,
                "created_files": created_files
            }
            
        except Exception as e:
            return {
                "operation": "create-project-structure",
                "project_path": project_path,
                "project_name": project_name,
                "disclosure_level": disclosure_level,
                "result": f"创建项目目录结构失败: {str(e)}",
                "error": str(e)
            }
    
    def _format_output(self, result_data: Dict[str, Any], detail_level: DetailLevel) -> Dict[str, Any]:
        """根据详细程度格式化输出结果"""
        if detail_level == DetailLevel.BASIC:
            # 基础级别只返回核心信息
            return {
                "operation": result_data["operation"],
                "result": result_data["result"],
                "project_path": result_data["project_path"]
            }
        elif detail_level == DetailLevel.STANDARD:
            # 标准级别返回标准信息
            return {
                "operation": result_data["operation"],
                "project_path": result_data["project_path"],
                "project_name": result_data["project_name"],
                "disclosure_level": result_data["disclosure_level"],
                "result": result_data["result"]
            }
        else:  # DETAILED
            # 详细级别返回完整信息
            return result_data
    
    def _create_basic_structure(self, root_dir: str) -> tuple:
        """创建基础级别的目录结构"""
        # 基础目录
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
        
        # 基础文档文件
        readme_path = os.path.join(root_dir, "README.md")
        self._create_file(readme_path, "# Project README\n\nBasic project documentation.")
        created_files.append(readme_path)
        
        getting_started_path = os.path.join(root_dir, "docs", "getting_started.md")
        self._create_file(getting_started_path, "# Getting Started\n\nBasic setup instructions.")
        created_files.append(getting_started_path)
        
        return created_dirs, created_files
    
    def _create_intermediate_structure(self, root_dir: str) -> tuple:
        """创建中级级别的目录结构"""
        # 中级目录
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
        
        # 中级文档文件
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
        """创建高级级别的目录结构"""
        # 高级目录
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
        
        # 高级文档文件
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
        """创建文件并写入内容"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)