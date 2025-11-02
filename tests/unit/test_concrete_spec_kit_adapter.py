"""
spec.kit适配器完整功能单元测试
"""
import sys
import os
import pytest
from unittest.mock import Mock, patch

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.dsgs_spec_kit_integration.adapters.spec_kit_adapter import SpecKitAdapter
from src.dsgs_spec_kit_integration.adapters.concrete_spec_kit_adapter import ConcreteSpecKitAdapter


class TestConcreteSpecKitAdapter:
    """ConcreteSpecKitAdapter单元测试"""
    
    def test_concrete_adapter_initialization(self):
        """测试具体适配器初始化"""
        adapter = ConcreteSpecKitAdapter()
        assert adapter is not None
        assert adapter.is_initialized == False
        assert len(adapter.get_registered_skills()) > 0
    
    def test_skill_registration(self):
        """测试技能注册功能"""
        adapter = ConcreteSpecKitAdapter()
        
        # 测试注册新技能
        def test_skill(params):
            return {"result": "test"}
        
        result = adapter.register_skill("dsgs-test-skill", test_skill)
        assert result is True
        assert adapter.is_skill_registered("dsgs-test-skill") is True
        
        # 测试重复注册
        result = adapter.register_skill("dsgs-test-skill", test_skill)
        assert result is True
        
        # 测试无效注册
        result = adapter.register_skill("", test_skill)
        assert result is False
        
        result = adapter.register_skill("dsgs-invalid", "not_a_function")
        assert result is False
    
    def test_skill_execution(self):
        """测试技能执行功能"""
        adapter = ConcreteSpecKitAdapter()
        
        # 测试执行已注册技能
        result = adapter.execute_skill("dsgs-architect", {"params": "电商系统"})
        assert result["skill"] == "architect"
        assert "电商系统" in result["result"]
        
        # 测试执行未注册技能
        with pytest.raises(ValueError):
            adapter.execute_skill("dsgs-unknown", {"params": "test"})
    
    def test_command_execution(self):
        """测试完整命令执行"""
        adapter = ConcreteSpecKitAdapter()
        
        # 测试有效命令执行
        result = adapter.execute_command("/speckit.dsgs.architect 设计电商系统架构")
        assert result["success"] is True
        assert result["skill_name"] == "dsgs-architect"
        assert "电商系统架构" in result["result"]["result"]
        
        # 测试无效命令格式
        result = adapter.execute_command("/invalid.command")
        assert result["success"] is False
        assert result["error"] == "Invalid command format"
        
        # 测试未注册技能命令
        result = adapter.execute_command("/speckit.dsgs.unknown 未知技能")
        assert result["success"] is False
        assert "Skill not registered" in result["error"]
        
        # 测试空命令
        result = adapter.execute_command("")
        assert result["success"] is False
        assert result["error"] == "Invalid command format"
    
    def test_get_registered_skills(self):
        """测试获取已注册技能列表"""
        adapter = ConcreteSpecKitAdapter()
        skills = adapter.get_registered_skills()
        assert isinstance(skills, list)
        assert len(skills) > 0
        assert "dsgs-architect" in skills
        assert "dsgs-agent-creator" in skills
        assert "dsgs-task-decomposer" in skills
    
    def test_adapter_info(self):
        """测试获取适配器信息"""
        adapter = ConcreteSpecKitAdapter()
        info = adapter.get_adapter_info()
        
        assert isinstance(info, dict)
        assert 'name' in info
        assert 'supported_agents' in info
        assert 'command_prefix' in info
        assert 'is_initialized' in info
        assert 'dependencies' in info
        assert 'registered_skills_count' in info
        assert 'registered_skills' in info
        assert info['name'] == 'ConcreteSpecKitAdapter'
        assert info['registered_skills_count'] >= 3


class TestSpecKitAdapterAbstract:
    """抽象类测试"""
    
    def test_abstract_class_cannot_be_instantiated(self):
        """测试抽象类不能被实例化"""
        with pytest.raises(TypeError):
            SpecKitAdapter()