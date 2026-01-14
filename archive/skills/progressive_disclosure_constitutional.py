"""
Progressive Disclosure Skill - 宪法级渐进披露原则技能
用于根据用户需求创建符合渐进披露原则和宪法原则的项目文档目录结构
"""
import os
from typing import Dict, Any, List

def execute(args: Dict[str, Any]) -> str:
    """
    执行宪法级渐进披露原则技能，创建符合宪法原则的项目文档目录结构
    """
    # 导入宪法验证功能
    try:
        from .constitutional_validator import validate_constitutional_compliance
    except ImportError:
        return "错误: 无法导入宪法验证功能"

    # 验证输入参数是否符合宪法原则
    validation = validate_constitutional_compliance(str(args), "cognitive_convenience")
    if not validation["compliant"]:
        return f"参数宪法验证失败: {validation['feedback']}"

    project_path = args.get("project_path", ".")
    project_name = args.get("project_name", "my_project")
    disclosure_level = args.get("disclosure_level", "basic")

    try:
        # 创建项目根目录
        root_dir = os.path.join(project_path, project_name)
        os.makedirs(root_dir, exist_ok=True)

        # 根据披露级别创建目录结构
        if disclosure_level == "basic":
            result = _create_basic_structure_with_constitutional_validation(root_dir)
        elif disclosure_level == "intermediate":
            result = _create_intermediate_structure_with_constitutional_validation(root_dir)
        elif disclosure_level == "advanced":
            result = _create_advanced_structure_with_constitutional_validation(root_dir)
        else:
            result = _create_basic_structure_with_constitutional_validation(root_dir)

        # 验证创建结果是否符合宪法原则
        validation = validate_constitutional_compliance(result, "all")
        if not validation["compliant"]:
            return f"创建结果宪法验证失败: {validation['feedback']}"

        return result

    except Exception as e:
        error_result = f"创建项目目录结构失败: {str(e)}"
        # 验证错误消息是否符合宪法原则
        try:
            validation = validate_constitutional_compliance(error_result, "cognitive_convenience")
            if not validation["compliant"]:
                error_result += f" (宪法验证: {validation['feedback']})"
        except ImportError:
            pass
        return error_result


def _create_basic_structure_with_constitutional_validation(root_dir: str) -> str:
    """创建基础级别的目录结构并验证宪法原则"""
    from .constitutional_validator import validate_constitutional_compliance
    
    # 基础目录
    dirs = [
        "docs",
        "src", 
        "tests",
        "config"
    ]

    for dir_name in dirs:
        dir_path = os.path.join(root_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)

    # 基础文档文件 - 验证内容是否符合宪法原则
    readme_content = "# Project README\n\nBasic project documentation with progressive disclosure."
    validation = validate_constitutional_compliance(readme_content, "progressive_disclosure")
    if not validation["compliant"]:
        readme_content += f"\n\n# Constitutional Note: {validation['feedback']}"
    
    _create_file(os.path.join(root_dir, "README.md"), readme_content)
    
    getting_started_content = "# Getting Started\n\nBasic setup instructions."
    validation = validate_constitutional_compliance(getting_started_content, "cognitive_convenience")
    if not validation["compliant"]:
        getting_started_content += f"\n\n# Constitutional Note: {validation['feedback']}"
    
    _create_file(os.path.join(root_dir, "docs", "getting_started.md"), getting_started_content)

    result = f"成功创建项目 '{os.path.basename(root_dir)}' 的基础渐进披露目录结构"
    
    # 验证结果是否符合宪法原则
    validation = validate_constitutional_compliance(result, "information_encapsulation")
    if not validation["compliant"]:
        result += f" (宪法验证: {validation['feedback']})"
        
    return result


def _create_intermediate_structure_with_constitutional_validation(root_dir: str) -> str:
    """创建中级级别的目录结构并验证宪法原则"""
    from .constitutional_validator import validate_constitutional_compliance
    
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
        dir_path = os.path.join(root_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)

    # 中级文档文件
    readme_content = "# Project README\n\nComprehensive project documentation with progressive disclosure."
    validation = validate_constitutional_compliance(readme_content, "progressive_disclosure")
    if not validation["compliant"]:
        readme_content += f"\n\n# Constitutional Note: {validation['feedback']}"
    
    _create_file(os.path.join(root_dir, "README.md"), readme_content)
    
    overview_content = "# Project Overview\n\nHigh-level project description with layered information."
    validation = validate_constitutional_compliance(overview_content, "cognitive_convenience")
    if not validation["compliant"]:
        overview_content += f"\n\n# Constitutional Note: {validation['feedback']}"
    
    _create_file(os.path.join(root_dir, "docs", "overview.md"), overview_content)
    
    design_content = "# Architecture Design\n\nSystem architecture overview with progressive detail levels."
    validation = validate_constitutional_compliance(design_content, "progressive_disclosure")
    if not validation["compliant"]:
        design_content += f"\n\n# Constitutional Note: {validation['feedback']}"
    
    _create_file(os.path.join(root_dir, "docs", "architecture", "design.md"), design_content)
    
    dev_guide_content = "# Development Guide\n\nDevelopment workflow instructions with layered access."
    validation = validate_constitutional_compliance(dev_guide_content, "cognitive_convenience")
    if not validation["compliant"]:
        dev_guide_content += f"\n\n# Constitutional Note: {validation['feedback']}"
    
    _create_file(os.path.join(root_dir, "docs", "guides", "development.md"), dev_guide_content)

    result = f"成功创建项目 '{os.path.basename(root_dir)}' 的中级渐进披露目录结构"
    
    # 验证结果是否符合宪法原则
    validation = validate_constitutional_compliance(result, "information_encapsulation")
    if not validation["compliant"]:
        result += f" (宪法验证: {validation['feedback']})"
        
    return result


def _create_advanced_structure_with_constitutional_validation(root_dir: str) -> str:
    """创建高级级别的目录结构并验证宪法原则"""
    from .constitutional_validator import validate_constitutional_compliance
    
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
        dir_path = os.path.join(root_dir, dir_name)
        os.makedirs(dir_path, exist_ok=True)

    # 高级文档文件
    readme_content = """# Project README

Complete project documentation with full progressive disclosure implementation.

## Basic Overview
Simple high-level description for initial understanding.

## Detailed Information  
Comprehensive details for in-depth exploration.

## Advanced Topics
Expert-level information for advanced users.
"""
    validation = validate_constitutional_compliance(readme_content, "progressive_disclosure")
    if not validation["compliant"]:
        readme_content += f"\n\n# Constitutional Note: {validation['feedback']}"
    
    _create_file(os.path.join(root_dir, "README.md"), readme_content)
    
    overview_content = "# Project Overview\n\nDetailed project description with multi-level information hierarchy."
    validation = validate_constitutional_compliance(overview_content, "progressive_disclosure")
    if not validation["compliant"]:
        overview_content += f"\n\n# Constitutional Note: {validation['feedback']}"
    
    _create_file(os.path.join(root_dir, "docs", "overview.md"), overview_content)
    
    design_content = """# Architecture Design

## High-Level Overview
Basic architecture concepts.

### Detailed Architecture
In-depth architectural components and relationships.

#### Implementation Details
Specific implementation information for developers.
"""
    validation = validate_constitutional_compliance(design_content, "progressive_disclosure")
    if not validation["compliant"]:
        design_content += f"\n\n# Constitutional Note: {validation['feedback']}"
    
    _create_file(os.path.join(root_dir, "docs", "architecture", "design.md"), design_content)
    
    diagram_content = "<!-- System Architecture Diagram with progressive detail levels -->"
    validation = validate_constitutional_compliance(diagram_content, "cognitive_gestalt")
    if not validation["compliant"]:
        diagram_content += f"<!-- Constitutional Note: {validation['feedback']} -->"
    
    _create_file(os.path.join(root_dir, "docs", "architecture", "diagrams", "system.svg"), diagram_content)
    
    # 其他文件也应用宪法原则...
    development_guide_content = """# Development Guide

## Getting Started
Basic setup and initial configuration.

### Advanced Configuration
Detailed configuration options.

#### Expert Customization
Advanced customization for power users.
"""
    validation = validate_constitutional_compliance(development_guide_content, "progressive_disclosure")
    if not validation["compliant"]:
        development_guide_content += f"\n\n# Constitutional Note: {validation['feedback']}"
    
    _create_file(os.path.join(root_dir, "docs", "guides", "development.md"), development_guide_content)

    result = f"成功创建项目 '{os.path.basename(root_dir)}' 的高级渐进披露目录结构，包含完整的宪法原则实现"
    
    # 验证结果是否符合宪法原则
    validation = validate_constitutional_compliance(result, "cognitive_gestalt")
    if not validation["compliant"]:
        result += f" (宪法验证: {validation['feedback']})"
        
    return result


def _create_file(file_path: str, content: str):
    """创建文件并写入内容"""
    # 创建目录（如果不存在）
    dir_path = os.path.dirname(file_path)
    os.makedirs(dir_path, exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)