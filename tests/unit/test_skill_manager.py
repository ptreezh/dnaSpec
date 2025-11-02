"""
DSGS技能系统扩展单元测试
"""
import sys
import os
import pytest
from unittest.mock import Mock, patch

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.dsgs_spec_kit_integration.core.skill import DSGSSkill, SkillResult, SkillStatus
from src.dsgs_spec_kit_integration.core.manager import SkillManager
from src.dsgs_spec_kit_integration.skills.examples import ArchitectSkill, AgentCreatorSkill, TaskDecomposerSkill
from src.dsgs_spec_kit_integration.adapters.concrete_spec_kit_adapter import ConcreteSpecKitAdapter


class TestSkillManager:
    """SkillManager单元测试"""
    
    def test_skill_manager_initialization(self):
        """测试技能管理器初始化"""
        manager = SkillManager()
        assert manager is not None
        assert len(manager.skills) == 0
        assert len(manager.skill_registry) == 0
        assert len(manager._spec_kit_adapters) == 0
    
    def test_skill_registration(self):
        """测试技能注册功能"""
        manager = SkillManager()
        
        # 创建测试技能
        skill = ArchitectSkill()
        
        # 注册技能
        result = manager.register_skill(skill)
        assert result is True
        assert skill.name in manager.skills
        assert skill.name in manager.skill_registry
        
        # 验证技能信息
        skill_info = manager.get_skill_info(skill.name)
        assert skill_info is not None
        assert skill_info.name == skill.name
        assert skill_info.description == skill.description
    
    def test_skill_execution(self):
        """测试技能执行功能"""
        manager = SkillManager()
        
        # 注册技能
        skill = ArchitectSkill()
        manager.register_skill(skill)
        
        # 执行技能
        result = manager.execute_skill(skill.name, "电商系统")
        assert isinstance(result, SkillResult)
        assert result.status == SkillStatus.COMPLETED
        assert result.skill_name == skill.name
        assert result.result is not None
        assert "电商系统" in result.result["architecture"]
    
    def test_manager_info(self):
        """测试获取管理器信息"""
        manager = SkillManager()
        
        # 注册多个技能
        skills = [ArchitectSkill(), AgentCreatorSkill(), TaskDecomposerSkill()]
        for skill in skills:
            manager.register_skill(skill)
        
        info = manager.get_manager_info()
        assert info['registered_skills_count'] == 3
        assert len(info['registered_skills']) == 3
        assert 'dsgs-architect' in info['registered_skills']
        assert 'dsgs-agent-creator' in info['registered_skills']
        assert 'dsgs-task-decomposer' in info['registered_skills']
    
    def test_spec_kit_adapter_integration(self):
        """测试spec.kit适配器集成"""
        manager = SkillManager()
        
        # 注册多个技能
        skills = [ArchitectSkill(), AgentCreatorSkill(), TaskDecomposerSkill()]
        for skill in skills:
            manager.register_skill(skill)
        
        # 创建并注册spec.kit适配器
        adapter = ConcreteSpecKitAdapter()
        manager.register_spec_kit_adapter(adapter)
        
        # 验证适配器信息
        info = manager.get_manager_info()
        assert info['registered_adapters_count'] == 1
        
        # 验证技能已注册到适配器
        registered_skills = adapter.get_registered_skills()
        assert 'dsgs-architect' in registered_skills
        assert 'dsgs-agent-creator' in registered_skills
        assert 'dsgs-task-decomposer' in registered_skills
    
    def test_spec_kit_command_execution(self):
        """测试spec.kit命令执行"""
        manager = SkillManager()
        
        # 注册技能
        skills = [ArchitectSkill(), AgentCreatorSkill(), TaskDecomposerSkill()]
        for skill in skills:
            manager.register_skill(skill)
        
        # 创建并注册适配器
        adapter = ConcreteSpecKitAdapter()
        manager.register_spec_kit_adapter(adapter)
        
        # 执行spec.kit命令
        result = manager.execute_spec_kit_command("/speckit.dsgs.architect 电商系统架构", adapter)
        assert result['success'] is True
        assert result['skill_name'] == 'dsgs-architect'
        assert 'result' in result
        assert '电商系统架构' in result['result']['result']['architecture']
    
    def test_direct_command_execution(self):
        """测试直接命令执行"""
        manager = SkillManager()
        
        # 注册技能
        skills = [ArchitectSkill(), AgentCreatorSkill(), TaskDecomposerSkill()]
        for skill in skills:
            manager.register_skill(skill)
        
        # 执行命令（没有适配器）
        result = manager.execute_spec_kit_command("/speckit.dsgs.architect 电商系统架构")
        assert result['success'] is True
        assert result['skill_name'] == 'dsgs-architect'
        
        # 测试无效命令
        result = manager.execute_spec_kit_command("/invalid.command")
        assert result['success'] is False
        assert result['error'] == 'Invalid command format'


class TestDSGSSkills:
    """DSGS技能单元测试"""
    
    def test_architect_skill(self):
        """测试架构师技能"""
        skill = ArchitectSkill()
        result = skill.process_request("电商系统")
        assert result.status == SkillStatus.COMPLETED
        assert "电商系统" in result.result["architecture"]
        assert "API网关" in result.result["components"]
    
    def test_agent_creator_skill(self):
        """测试智能体创建技能"""
        skill = AgentCreatorSkill()
        result = skill.process_request("订单处理智能体")
        assert result.status == SkillStatus.COMPLETED
        assert "订单处理智能体" in result.result["agent"]
        assert "任务执行" in result.result["capabilities"]
    
    def test_task_decomposer_skill(self):
        """测试任务分解技能"""
        skill = TaskDecomposerSkill()
        result = skill.process_request("用户管理模块")
        assert result.status == SkillStatus.COMPLETED
        assert "用户管理模块" in result.result["task"]
        assert len(result.result["subtasks"]) == 4