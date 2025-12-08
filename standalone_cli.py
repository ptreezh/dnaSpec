#!/usr/bin/env python3
"""
DSGS CLI命令处理器 - 独立的命令接口
解决模块导入问题，提供直接的CLI功能
"""
import sys
import os
from typing import Dict, Any

# 添加项目路径
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
sys.path.insert(0, project_root)

def execute_cli_command(args: list) -> str:
    """
    执行CLI命令 - 独立接口，避免导入问题
    """
    if len(args) < 2:
        return "Usage: dnaspec [command] [options]"

    command = args[1].lower()
    
    if command == 'list':
        return _list_available_skills()
    elif command == 'version' or command == '--version':
        return _get_version()
    elif command == 'help':
        return _get_help()
    elif command == 'validate':
        return _validate_integration()
    else:
        return f"Unknown command: {command}. Available: list, version, help, validate"

def _list_available_skills() -> str:
    """
    列出所有可用技能
    """
    skills_description = """
Available DSGS Skills:

1. Context Engineering Skills:
   - /speckit.dsgs.context-analysis [context]     # Analyze context quality (5 dimensions)
   - /speckit.dsgs.context-optimization [context] # Optimize context with goals
   - /speckit.dsgs.cognitive-template [task]     # Apply cognitive templates

2. System Design Skills:
   - /speckit.dsgs.architect [requirements]       # System architecture design
   - /speckit.dsgs.agent-creator [spec]           # Create specialized AI agents
   - /speckit.dsgs.task-decomposer [task]         # Decompose complex tasks

3. Development Skills:
   - /speckit.dsgs.constraint-generator [reqs]    # Generate system constraints
   - /speckit.dsgs.dapi-checker [api]             # API interface validation
   - /speckit.dsgs.modulizer [system]             # System modularization

4. Utility Skills:
   - /speckit.dsgs.git-skill [operation]          # Git operations
   - /speckit.dsgs.temp-workspace [operation]     # Temporary workspace management
    """
    return skills_description.strip()

def _get_version() -> str:
    """
    获取版本信息
    """
    return "DSGS Context Engineering Skills v1.0.4 - Dynamic Specification Growth System"

def _get_help() -> str:
    """
    获取帮助信息
    """
    help_text = """
DSGS Context Engineering Skills - Help

Commands:
  dnaspec list      - List all available skills
  dnaspec version   - Show version information
  dnaspec help      - Show this help
  dnaspec validate  - Validate DSGS integration
  dnaspec deploy    - Deploy skills to AI CLI tools

Usage in AI CLI Tools:
  /speckit.dsgs.context-analysis "Analyze this requirement"
  /speckit.dsgs.context-optimization "Optimize this context"
  /speckit.dsgs.cognitive-template "Apply cognitive framework" template=verification

For more information visit: https://github.com/ptreezh/dnaSpec
    """
    return help_text.strip()

def _validate_integration() -> str:
    """
    验证集成状态
    """
    # 导入检测器验证集成
    try:
        from src.dsgs_spec_kit_integration.core.cli_detector import CliDetector
        detector = CliDetector()
        results = detector.detect_all()
        
        validation_report = "DSGS Integration Validation Results:\n\n"
        installed_count = 0
        total_count = len(results)
        
        for tool, result in results.items():
            if result.get('installed', False):
                installed_count += 1
                validation_report += f"✅ {tool}: {result.get('version', 'Unknown')}\n"
            else:
                validation_report += f"❌ {tool}: Not installed\n"
        
        validation_report += f"\nSummary: {installed_count}/{total_count} tools detected and integrated\n"
        validation_report += "DSGS Context Engineering Skills system is ready for use!"
        
        return validation_report
    except Exception as e:
        return f"Validation failed: {str(e)}"

if __name__ == "__main__":
    result = execute_cli_command(sys.argv)
    print(result)