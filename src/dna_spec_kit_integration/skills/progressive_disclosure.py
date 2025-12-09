"""
Progressive Disclosure Skill - 渐进披露原则技能
用于根据用户需求创建符合渐进披露原则的项目文档目录结构
"""
import os
from typing import Dict, Any, List


def execute(args: Dict[str, Any]) -> str:
    """
    执行渐进披露原则技能，创建符合渐进披露原则的项目文档目录结构
    """
    project_path = args.get("project_path", ".")
    project_name = args.get("project_name", "my_project")
    disclosure_level = args.get("disclosure_level", "basic")
    
    try:
        # 创建项目根目录
        root_dir = os.path.join(project_path, project_name)
        os.makedirs(root_dir, exist_ok=True)
        
        # 根据披露级别创建目录结构
        if disclosure_level == "basic":
            _create_basic_structure(root_dir)
        elif disclosure_level == "intermediate":
            _create_intermediate_structure(root_dir)
        elif disclosure_level == "advanced":
            _create_advanced_structure(root_dir)
        else:
            _create_basic_structure(root_dir)
        
        return f"成功创建项目 '{project_name}' 的渐进披露目录结构，级别: {disclosure_level}"
        
    except Exception as e:
        return f"创建项目目录结构失败: {str(e)}"


def _create_basic_structure(root_dir: str):
    """创建基础级别的目录结构"""
    # 基础目录
    dirs = [
        "docs",
        "src",
        "tests",
        "config"
    ]
    
    for dir_name in dirs:
        os.makedirs(os.path.join(root_dir, dir_name), exist_ok=True)
    
    # 基础文档文件
    _create_file(os.path.join(root_dir, "README.md"), "# Project README\n\nBasic project documentation.")
    _create_file(os.path.join(root_dir, "docs", "getting_started.md"), "# Getting Started\n\nBasic setup instructions.")


def _create_intermediate_structure(root_dir: str):
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
    
    for dir_name in dirs:
        os.makedirs(os.path.join(root_dir, dir_name), exist_ok=True)
    
    # 中级文档文件
    _create_file(os.path.join(root_dir, "README.md"), "# Project README\n\nComprehensive project documentation.")
    _create_file(os.path.join(root_dir, "docs", "overview.md"), "# Project Overview\n\nHigh-level project description.")
    _create_file(os.path.join(root_dir, "docs", "architecture", "design.md"), "# Architecture Design\n\nSystem architecture overview.")
    _create_file(os.path.join(root_dir, "docs", "guides", "development.md"), "# Development Guide\n\nDevelopment workflow instructions.")


def _create_advanced_structure(root_dir: str):
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
    
    for dir_name in dirs:
        os.makedirs(os.path.join(root_dir, dir_name), exist_ok=True)
    
    # 高级文档文件
    _create_file(os.path.join(root_dir, "README.md"), "# Project README\n\nComplete project documentation.")
    _create_file(os.path.join(root_dir, "docs", "overview.md"), "# Project Overview\n\nDetailed project description.")
    _create_file(os.path.join(root_dir, "docs", "architecture", "design.md"), "# Architecture Design\n\nDetailed system architecture.")
    _create_file(os.path.join(root_dir, "docs", "architecture", "diagrams", "system.svg"), "<!-- System Architecture Diagram -->")
    _create_file(os.path.join(root_dir, "docs", "guides", "development.md"), "# Development Guide\n\nComplete development workflow.")
    _create_file(os.path.join(root_dir, "docs", "guides", "contributing", "style_guide.md"), "# Style Guide\n\nCoding standards and conventions.")
    _create_file(os.path.join(root_dir, "docs", "api", "reference.md"), "# API Reference\n\nAPI documentation.")
    _create_file(os.path.join(root_dir, "docs", "deployment", "instructions.md"), "# Deployment Instructions\n\nDeployment procedures.")


def _create_file(file_path: str, content: str):
    """创建文件并写入内容"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)