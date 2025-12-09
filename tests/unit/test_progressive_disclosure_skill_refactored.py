"""
渐进披露技能重构测试
"""
import pytest
import os
import tempfile
import shutil
from src.dna_spec_kit_integration.skills.progressive_disclosure_refactored import ProgressiveDisclosureSkill


def test_progressive_disclosure_skill_basic():
    """测试渐进披露技能 - 基础级别"""
    skill = ProgressiveDisclosureSkill()
    
    # 创建临时目录用于测试
    with tempfile.TemporaryDirectory() as temp_dir:
        args = {
            "input": "创建项目目录结构",
            "options": {
                "project_path": temp_dir,
                "project_name": "test_project",
                "disclosure_level": "basic"
            },
            "detail_level": "basic"
        }
        
        result = skill.execute(args)
        
        assert result["status"] == "success"
        assert "data" in result
        assert "operation" in result["data"]
        assert "result" in result["data"]
        assert "project_path" in result["data"]
        assert "metadata" in result
        assert result["metadata"]["detail_level"] == "basic"
        
        # 验证目录结构是否创建成功
        project_dir = os.path.join(temp_dir, "test_project")
        assert os.path.exists(project_dir)
        assert os.path.exists(os.path.join(project_dir, "docs"))
        assert os.path.exists(os.path.join(project_dir, "src"))
        assert os.path.exists(os.path.join(project_dir, "tests"))
        assert os.path.exists(os.path.join(project_dir, "config"))


def test_progressive_disclosure_skill_standard():
    """测试渐进披露技能 - 标准级别"""
    skill = ProgressiveDisclosureSkill()
    
    # 创建临时目录用于测试
    with tempfile.TemporaryDirectory() as temp_dir:
        args = {
            "input": "创建项目目录结构",
            "options": {
                "project_path": temp_dir,
                "project_name": "test_project",
                "disclosure_level": "intermediate"
            },
            "detail_level": "standard"
        }
        
        result = skill.execute(args)
        
        assert result["status"] == "success"
        assert "data" in result
        assert "operation" in result["data"]
        assert "result" in result["data"]
        assert "project_path" in result["data"]
        assert "disclosure_level" in result["data"]
        assert "metadata" in result
        assert result["metadata"]["detail_level"] == "standard"
        
        # 验证目录结构是否创建成功
        project_dir = os.path.join(temp_dir, "test_project")
        assert os.path.exists(project_dir)
        assert os.path.exists(os.path.join(project_dir, "docs"))
        assert os.path.exists(os.path.join(project_dir, "docs", "architecture"))
        assert os.path.exists(os.path.join(project_dir, "docs", "guides"))
        assert os.path.exists(os.path.join(project_dir, "src"))
        assert os.path.exists(os.path.join(project_dir, "src", "core"))
        assert os.path.exists(os.path.join(project_dir, "src", "utils"))
        assert os.path.exists(os.path.join(project_dir, "tests"))
        assert os.path.exists(os.path.join(project_dir, "tests", "unit"))
        assert os.path.exists(os.path.join(project_dir, "tests", "integration"))
        assert os.path.exists(os.path.join(project_dir, "config"))
        assert os.path.exists(os.path.join(project_dir, "scripts"))


def test_progressive_disclosure_skill_detailed():
    """测试渐进披露技能 - 详细级别"""
    skill = ProgressiveDisclosureSkill()
    
    # 创建临时目录用于测试
    with tempfile.TemporaryDirectory() as temp_dir:
        args = {
            "input": "创建项目目录结构",
            "options": {
                "project_path": temp_dir,
                "project_name": "test_project",
                "disclosure_level": "advanced"
            },
            "detail_level": "detailed"
        }
        
        result = skill.execute(args)
        
        assert result["status"] == "success"
        assert "data" in result
        assert "operation" in result["data"]
        assert "result" in result["data"]
        assert "project_path" in result["data"]
        assert "disclosure_level" in result["data"]
        assert "created_directories" in result["data"]
        assert "created_files" in result["data"]
        assert "metadata" in result
        assert result["metadata"]["detail_level"] == "detailed"
        
        # 验证目录结构是否创建成功
        project_dir = os.path.join(temp_dir, "test_project")
        assert os.path.exists(project_dir)
        # 检查一些关键目录
        assert os.path.exists(os.path.join(project_dir, "docs"))
        assert os.path.exists(os.path.join(project_dir, "docs", "architecture"))
        assert os.path.exists(os.path.join(project_dir, "docs", "architecture", "diagrams"))
        assert os.path.exists(os.path.join(project_dir, "src"))
        assert os.path.exists(os.path.join(project_dir, "src", "modules"))
        assert os.path.exists(os.path.join(project_dir, "src", "modules", "auth"))
        assert os.path.exists(os.path.join(project_dir, "tests"))
        assert os.path.exists(os.path.join(project_dir, "tests", "e2e"))
        assert os.path.exists(os.path.join(project_dir, "scripts"))
        assert os.path.exists(os.path.join(project_dir, "scripts", "build"))
        assert os.path.exists(os.path.join(project_dir, "assets"))
        assert os.path.exists(os.path.join(project_dir, "assets", "images"))


def test_progressive_disclosure_skill_invalid_level():
    """测试渐进披露技能处理无效披露级别"""
    skill = ProgressiveDisclosureSkill()
    
    # 创建临时目录用于测试
    with tempfile.TemporaryDirectory() as temp_dir:
        args = {
            "input": "创建项目目录结构",
            "options": {
                "project_path": temp_dir,
                "project_name": "test_project",
                "disclosure_level": "invalid"
            },
            "detail_level": "standard"
        }
        
        result = skill.execute(args)
        
        assert result["status"] == "success"
        assert "data" in result
        assert "result" in result["data"]
        # 无效级别应回退到基础级别
        assert "成功创建项目" in result["data"]["result"]


def test_progressive_disclosure_skill_default_detail_level():
    """测试渐进披露技能使用默认详细级别"""
    skill = ProgressiveDisclosureSkill()
    
    # 创建临时目录用于测试
    with tempfile.TemporaryDirectory() as temp_dir:
        args = {
            "input": "创建项目目录结构",
            "options": {
                "project_path": temp_dir,
                "project_name": "test_project",
                "disclosure_level": "basic"
            }
            # 没有指定detail_level，应该使用默认值"standard"
        }
        
        result = skill.execute(args)
        
        assert result["status"] == "success"
        assert result["metadata"]["detail_level"] == "standard"


def test_progressive_disclosure_skill_missing_input():
    """测试渐进披露技能处理缺失输入"""
    skill = ProgressiveDisclosureSkill()
    args = {
        "options": {
            "project_path": ".",
            "project_name": "test_project",
            "disclosure_level": "basic"
        }
        # 没有input参数
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "error"
    assert result["error"]["type"] == "VALIDATION_ERROR"
    assert "Input cannot be empty" in result["error"]["message"]


def test_progressive_disclosure_skill_empty_input():
    """测试渐进披露技能处理空输入"""
    skill = ProgressiveDisclosureSkill()
    args = {
        "input": "",  # 空字符串
        "options": {
            "project_path": ".",
            "project_name": "test_project",
            "disclosure_level": "basic"
        }
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "error"
    assert result["error"]["type"] == "VALIDATION_ERROR"
    assert "Input cannot be empty" in result["error"]["message"]