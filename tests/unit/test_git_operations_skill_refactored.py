"""
Git操作技能重构测试
"""
import pytest
from src.dna_spec_kit_integration.skills.git_operations_refactored import GitOperationsSkill


def test_git_operations_skill_basic_status():
    """测试Git操作技能 - 基础级别状态查询"""
    skill = GitOperationsSkill()
    args = {
        "input": "查询当前仓库状态",
        "options": {
            "operation": "status"
        },
        "detail_level": "basic"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert "operation" in result["data"]
    assert "result" in result["data"]
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "basic"


def test_git_operations_skill_standard_commit():
    """测试Git操作技能 - 标准级别提交操作"""
    skill = GitOperationsSkill()
    args = {
        "input": "提交所有更改",
        "options": {
            "operation": "commit",
            "message": "Test commit message"
        },
        "detail_level": "standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert "operation" in result["data"]
    assert "result" in result["data"]
    assert "repository_path" in result["data"]
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "standard"


def test_git_operations_skill_detailed_push():
    """测试Git操作技能 - 详细级别推送操作"""
    skill = GitOperationsSkill()
    args = {
        "input": "推送到远程仓库",
        "options": {
            "operation": "push",
            "remote": "origin",
            "branch": "main"
        },
        "detail_level": "detailed"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert "operation" in result["data"]
    assert "result" in result["data"]
    assert "repository_path" in result["data"]
    assert "command_executed" in result["data"]
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "detailed"


def test_git_operations_skill_missing_operation():
    """测试Git操作技能处理缺失操作"""
    skill = GitOperationsSkill()
    args = {
        "input": "执行Git操作",
        "detail_level": "standard"
        # 没有指定operation
    }
    
    result = skill.execute(args)
    
    # 由于缺少必需的操作参数，技能执行逻辑会处理这个情况
    assert result["status"] == "success"
    assert "data" in result
    assert "result" in result["data"]
    assert "未指定Git操作" in result["data"]["result"]


def test_git_operations_skill_invalid_operation():
    """测试Git操作技能处理无效操作"""
    skill = GitOperationsSkill()
    args = {
        "input": "执行无效的Git操作",
        "options": {
            "operation": "invalid-operation"
        },
        "detail_level": "standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert "未知的Git操作" in result["data"]["result"]


def test_git_operations_skill_default_detail_level():
    """测试Git操作技能使用默认详细级别"""
    skill = GitOperationsSkill()
    args = {
        "input": "查询当前仓库状态",
        "options": {
            "operation": "status"
        }
        # 没有指定detail_level，应该使用默认值"standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert result["metadata"]["detail_level"] == "standard"


def test_git_operations_skill_missing_input():
    """测试Git操作技能处理缺失输入"""
    skill = GitOperationsSkill()
    args = {
        "options": {
            "operation": "status"
        }
        # 没有input参数
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "error"
    assert result["error"]["type"] == "VALIDATION_ERROR"
    assert "Input cannot be empty" in result["error"]["message"]


def test_git_operations_skill_empty_input():
    """测试Git操作技能处理空输入"""
    skill = GitOperationsSkill()
    args = {
        "input": "",  # 空字符串
        "options": {
            "operation": "status"
        }
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "error"
    assert result["error"]["type"] == "VALIDATION_ERROR"
    assert "Input cannot be empty" in result["error"]["message"]