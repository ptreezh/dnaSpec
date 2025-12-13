"""
临时工作区技能重构测试
"""
import pytest
from src.dna_spec_kit_integration.skills.temp_workspace_refactored import WorkspaceSkill


def test_temp_workspace_skill_basic_create():
    """测试临时工作区技能 - 基础级别创建工作区"""
    skill = WorkspaceSkill()
    args = {
        "input": "创建临时工作区",
        "options": {
            "operation": "create-workspace"
        },
        "detail_level": "basic"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert "operation" in result["data"]
    assert "result" in result["data"]
    assert "workspace_path" in result["data"]
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "basic"


def test_temp_workspace_skill_standard_add_file():
    """测试临时工作区技能 - 标准级别添加文件"""
    skill = WorkspaceSkill()
    args = {
        "input": "添加文件到临时工作区",
        "options": {
            "operation": "add-file",
            "file_path": "test.txt",
            "file_content": "This is a test file"
        },
        "detail_level": "standard"
    }

    # 先创建工作区
    create_args = {
        "input": "创建临时工作区",
        "options": {
            "operation": "create-workspace"
        },
        "detail_level": "standard"
    }
    skill.execute(create_args)

    # 再添加文件
    result = skill.execute(args)

    assert result["status"] == "success"
    assert "data" in result
    assert "operation" in result["data"]
    assert "result" in result["data"]
    assert "file_path" in result["data"]
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "standard"


def test_temp_workspace_skill_detailed_list_files():
    """测试临时工作区技能 - 详细级别列出文件"""
    skill = WorkspaceSkill()
    args = {
        "input": "列出临时工作区中的文件",
        "options": {
            "operation": "list-files"
        },
        "detail_level": "detailed"
    }

    # 先创建工作区
    create_args = {
        "input": "创建临时工作区",
        "options": {
            "operation": "create-workspace"
        },
        "detail_level": "detailed"
    }
    skill.execute(create_args)

    # 再列出文件
    result = skill.execute(args)

    assert result["status"] == "success"
    assert "data" in result
    assert "operation" in result["data"]
    assert "result" in result["data"]
    assert "files" in result["data"]
    assert "workspace_path" in result["data"]
    assert "file_count" in result["data"]
    assert "metadata" in result
    assert result["metadata"]["detail_level"] == "detailed"


def test_temp_workspace_skill_missing_operation():
    """测试临时工作区技能处理缺失操作"""
    skill = WorkspaceSkill()
    args = {
        "input": "执行临时工作区操作",
        "detail_level": "standard"
        # 没有指定operation
    }

    result = skill.execute(args)

    assert result["status"] == "success"
    assert "data" in result
    assert "result" in result["data"]
    assert "未知操作" in result["data"]["result"]


def test_temp_workspace_skill_invalid_operation():
    """测试临时工作区技能处理无效操作"""
    skill = WorkspaceSkill()
    args = {
        "input": "执行无效的临时工作区操作",
        "options": {
            "operation": "invalid-operation"
        },
        "detail_level": "standard"
    }

    result = skill.execute(args)

    assert result["status"] == "success"
    assert "data" in result
    assert "未知操作" in result["data"]["result"]


def test_temp_workspace_skill_default_detail_level():
    """测试临时工作区技能使用默认详细级别"""
    skill = WorkspaceSkill()
    args = {
        "input": "创建临时工作区",
        "options": {
            "operation": "create-workspace"
        }
        # 没有指定detail_level，应该使用默认值"standard"
    }

    result = skill.execute(args)

    assert result["status"] == "success"
    assert result["metadata"]["detail_level"] == "standard"


def test_temp_workspace_skill_missing_input():
    """测试临时工作区技能处理缺失输入"""
    skill = WorkspaceSkill()
    args = {
        "options": {
            "operation": "create-workspace"
        }
        # 没有input参数
    }

    result = skill.execute(args)

    assert result["status"] == "error"
    assert result["error"]["type"] == "VALIDATION_ERROR"
    assert "Input cannot be empty" in result["error"]["message"]


def test_temp_workspace_skill_empty_input():
    """测试临时工作区技能处理空输入"""
    skill = WorkspaceSkill()
    args = {
        "input": "",  # 空字符串
        "options": {
            "operation": "create-workspace"
        }
    }

    result = skill.execute(args)

    assert result["status"] == "error"
    assert result["error"]["type"] == "VALIDATION_ERROR"
    assert "Input cannot be empty" in result["error"]["message"]