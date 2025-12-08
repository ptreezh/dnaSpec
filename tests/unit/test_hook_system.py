"""
Hook系统单元测试
"""
import sys
import os
import pytest
from unittest.mock import Mock, patch

# 添加项目根目录到Python路径
# 从 tests/unit/test_hook_system.py 到项目根目录需要向上两级
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.dnaspec_spec_kit_integration.core.hook import HookSystem, HookConfig, HookResult
from src.dnaspec_spec_kit_integration.core.skill import DNASpecSkill, SkillResult, SkillStatus


class TestHookConfig:
    """HookConfig单元测试"""
    
    def test_hook_config_initialization(self):
        """测试Hook配置初始化"""
        config = HookConfig()
        assert config.enabled is True
        assert config.intercept_spec_kit_commands is True
        assert config.intercept_text_commands is True
        assert config.auto_invoke_threshold == 0.6
        assert config.enabled_skills == []
        assert config.disabled_patterns == []
    
    def test_skill_enable_disable(self):
        """测试技能启用/禁用功能"""
        config = HookConfig()
        
        # 启用技能
        config.enable_skill("dnaspec-architect")
        assert "dnaspec-architect" in config.enabled_skills
        assert config.is_skill_enabled("dnaspec-architect") is True
        
        # 禁用技能
        config.disable_skill("dnaspec-architect")
        assert "dnaspec-architect" not in config.enabled_skills
        assert config.is_skill_enabled("dnaspec-architect") is True  # 当启用列表为空时，默认启用所有技能
    
    def test_pattern_disable(self):
        """测试模式禁用功能"""
        config = HookConfig()
        
        # 添加禁用模式
        config.add_disabled_pattern(r"test.*pattern")
        assert len(config.disabled_patterns) == 1
        assert r"test.*pattern" in config.disabled_patterns
        
        # 检查模式是否被禁用
        assert config.is_pattern_disabled("test some pattern") is True
        assert config.is_pattern_disabled("normal request") is False


class TestHookSystem:
    """HookSystem单元测试"""
    
    def test_hook_system_initialization(self):
        """测试Hook系统初始化"""
        hook_system = HookSystem()
        assert hook_system is not None
        assert hook_system.config is not None
        assert len(hook_system._interceptors) == 0
        assert len(hook_system._processors) == 0
        assert len(hook_system._hooks) == 0
    
    def test_spec_kit_command_detection(self):
        """测试spec.kit命令检测"""
        hook_system = HookSystem()
        
        # 测试有效的spec.kit命令
        assert hook_system._is_spec_kit_command("/speckit.dnaspec.architect 设计系统") is True
        assert hook_system._is_spec_kit_command("/speckit.dnaspec.agent-creator 创建智能体") is True
        assert hook_system._is_spec_kit_command("/speckit.dnaspec.task-decomposer 分解任务") is True
        
        # 测试无效命令
        assert hook_system._is_spec_kit_command("普通文本请求") is False
        assert hook_system._is_spec_kit_command("/other.command") is False
        assert hook_system._is_spec_kit_command("") is False
    
    def test_natural_language_detection(self):
        """测试自然语言请求检测"""
        hook_system = HookSystem()
        
        # 测试自然语言请求
        assert hook_system._is_natural_language_request("设计一个系统架构") is True
        assert hook_system._is_natural_language_request("创建订单处理智能体") is True
        assert hook_system._is_natural_language_request("分解用户管理任务") is True
        assert hook_system._is_natural_language_request("Check API interface consistency") is True
        
        # 测试无效请求
        assert hook_system._is_natural_language_request("") is False
        assert hook_system._is_natural_language_request("a") is False
        assert hook_system._is_natural_language_request("  ") is False
    
    def test_hook_registration(self):
        """测试钩子注册功能"""
        hook_system = HookSystem()
        
        # 定义测试钩子函数
        def test_hook(request):
            return HookResult(intercepted=True, handled=True)
        
        # 注册钩子
        hook_system.register_hook("test_hook", test_hook)
        assert len(hook_system._hooks) == 1
        assert "test_hook" in hook_system._hooks
    
    def test_interceptor_processor_registration(self):
        """测试拦截器和处理器注册"""
        hook_system = HookSystem()
        
        def test_interceptor(request):
            return True
        
        def test_processor(request):
            return {"result": "processed"}
        
        # 注册拦截器和处理器
        hook_system.register_interceptor(test_interceptor)
        hook_system.register_processor(test_processor)
        
        assert len(hook_system._interceptors) == 1
        assert len(hook_system._processors) == 1
    
    def test_hook_system_disabled(self):
        """测试Hook系统禁用情况"""
        hook_system = HookSystem()
        hook_system.config.enabled = False
        
        result = hook_system.intercept_request("任何请求")
        assert result.intercepted is False
        assert result.handled is False
    
    def test_pattern_disabled(self):
        """测试模式禁用情况"""
        hook_system = HookSystem()
        hook_system.config.add_disabled_pattern(r"禁用.*请求")
        
        result = hook_system.intercept_request("禁用的请求内容")
        assert result.intercepted is False
        assert result.handled is False
        assert result.processing_time >= 0  # 处理时间应该被计算
    
    def test_hook_info(self):
        """测试获取Hook系统信息"""
        hook_system = HookSystem()
        
        # 注册一些组件
        def test_interceptor(request):
            return True
        
        def test_processor(request):
            return {"result": "processed"}
        
        def test_hook(request):
            return HookResult(intercepted=True, handled=True)
        
        hook_system.register_interceptor(test_interceptor)
        hook_system.register_processor(test_processor)
        hook_system.register_hook("test_hook", test_hook)
        hook_system.config.enable_skill("dnaspec-architect")
        
        info = hook_system.get_hook_info()
        assert isinstance(info, dict)
        assert info['enabled'] is True
        assert info['interceptor_count'] == 1
        assert info['processor_count'] == 1
        assert info['hook_count'] == 1
        assert "dnaspec-architect" in info['enabled_skills']


class TestHookSystemWithSkillManager:
    """Hook系统与技能管理器集成测试"""
    
    def test_spec_kit_command_handling_with_skill_manager(self):
        """测试spec.kit命令处理（带技能管理器）"""
        # 创建模拟技能管理器
        mock_skill_manager = Mock()
        
        # 设置模拟的执行结果
        mock_result = Mock()
        mock_result.skill_name = "dnaspec-architect"
        mock_result.status = SkillStatus.COMPLETED
        mock_result.result = {"architecture": "test"}
        
        mock_skill_manager.execute_spec_kit_command.return_value = {
            'success': True,
            'result': mock_result,
            'skill_name': 'dnaspec-architect'
        }
        
        hook_system = HookSystem(mock_skill_manager)
        
        # 测试spec.kit命令处理
        result = hook_system.intercept_request("/speckit.dnaspec.architect 设计系统")
        
        assert result.intercepted is True
        assert result.handled is True
        assert result.skill_name == "dnaspec-architect"
        assert result.skill_result is not None
        assert result.error_message == ""
        
        # 验证技能管理器被调用
        mock_skill_manager.execute_spec_kit_command.assert_called_once_with("/speckit.dnaspec.architect 设计系统")
    
    def test_spec_kit_command_handling_skill_disabled(self):
        """测试技能禁用时的spec.kit命令处理"""
        mock_skill_manager = Mock()
        hook_system = HookSystem(mock_skill_manager)
        
        # 禁用技能
        hook_system.config.disable_skill("dnaspec-architect")
        
        # 尝试处理命令，应该失败
        result = hook_system.intercept_request("/speckit.dnaspec.architect 设计系统")
        
        assert result.intercepted is True
        assert result.handled is False
        assert "disabled" in result.error_message
    
    def test_spec_kit_command_handling_skill_manager_missing(self):
        """测试技能管理器缺失时的spec.kit命令处理"""
        hook_system = HookSystem(None)
        
        result = hook_system.intercept_request("/speckit.dnaspec.architect 设计系统")
        
        assert result.intercepted is True
        assert result.handled is False
        assert "Skill manager not available" in result.error_message
    
    def test_natural_language_handling_with_skill_manager(self):
        """测试自然语言请求处理（带技能管理器）"""
        mock_skill_manager = Mock()
        
        # 设置智能匹配结果
        mock_match_result = {
            'skill_name': 'dnaspec-architect',
            'confidence': 0.8,
            'match_type': 'keyword',
            'matched_keywords': ['架构', '设计']
        }
        
        mock_skill_manager.match_skill_intelligently.return_value = mock_match_result
        
        # 设置技能执行结果
        mock_skill_result = SkillResult(
            skill_name='dnaspec-architect',
            status=SkillStatus.COMPLETED,
            result={"architecture": "test_result"},
            confidence=0.8,
            execution_time=0.1
        )
        
        mock_skill_manager.execute_skill.return_value = mock_skill_result
        
        hook_system = HookSystem(mock_skill_manager)
        
        # 测试自然语言请求处理
        result = hook_system.intercept_request("设计一个系统架构")
        
        assert result.intercepted is True
        assert result.handled is True
        assert result.skill_name == "dnaspec-architect"
        assert result.skill_result is not None
        assert result.error_message == ""
        
        # 验证相关方法被调用
        mock_skill_manager.match_skill_intelligently.assert_called_once_with("设计一个系统架构")
        mock_skill_manager.execute_skill.assert_called_once_with("dnaspec-architect", "设计一个系统架构")
    
    def test_natural_language_handling_low_confidence(self):
        """测试低置信度时的自然语言请求处理"""
        mock_skill_manager = Mock()
        
        # 设置低置信度的匹配结果
        mock_match_result = {
            'skill_name': 'dnaspec-architect',
            'confidence': 0.3,  # 低于阈值0.6
            'match_type': 'keyword'
        }
        
        mock_skill_manager.match_skill_intelligently.return_value = mock_match_result
        
        hook_system = HookSystem(mock_skill_manager)
        
        # 测试低置信度请求处理
        result = hook_system.intercept_request("设计一个系统架构")
        
        assert result.intercepted is True
        assert result.handled is False
        assert "Confidence too low" in result.error_message
        assert "0.30" in result.error_message
    
    def test_natural_language_handling_skill_disabled(self):
        """测试技能禁用时的自然语言请求处理"""
        mock_skill_manager = Mock()
        
        # 设置匹配结果
        mock_match_result = {
            'skill_name': 'dnaspec-architect',
            'confidence': 0.8,
            'match_type': 'keyword'
        }
        
        mock_skill_manager.match_skill_intelligently.return_value = mock_match_result
        
        hook_system = HookSystem(mock_skill_manager)
        
        # 禁用技能
        hook_system.config.disable_skill("dnaspec-architect")
        
        # 测试请求处理
        result = hook_system.intercept_request("设计一个系统架构")
        
        assert result.intercepted is True
        assert result.handled is False
        assert "disabled" in result.error_message
    
    def test_natural_language_handling_skill_manager_missing(self):
        """测试技能管理器缺失时的自然语言请求处理"""
        hook_system = HookSystem(None)
        
        result = hook_system.intercept_request("设计一个系统架构")
        
        assert result.intercepted is True
        assert result.handled is False
        assert "Skill manager not available" in result.error_message
    
    def test_natural_language_handling_no_match_found(self):
        """测试无匹配技能时的自然语言请求处理"""
        mock_skill_manager = Mock()
        
        # 没有匹配结果
        mock_skill_manager.match_skill_intelligently.return_value = None
        
        hook_system = HookSystem(mock_skill_manager)
        
        result = hook_system.intercept_request("不相关的请求")
        
        assert result.intercepted is True
        assert result.handled is False
        assert "No matching skill found" in result.error_message
    
    def test_interceptor_processor_handling(self):
        """测试拦截器和处理器处理"""
        hook_system = HookSystem()
        
        # 注册拦截器和处理器
        def test_interceptor(request):
            return "设计" in request
        
        def test_processor(request):
            return {
                'result': 'intercepted_result',
                'skill_name': 'intercepted_skill'
            }
        
        hook_system.register_interceptor(test_interceptor)
        hook_system.register_processor(test_processor)
        
        # 测试拦截器和处理器
        result = hook_system.intercept_request("设计一个新的系统")
        
        assert result.intercepted is True
        assert result.handled is True
        assert result.skill_name == 'intercepted_skill'
        assert result.skill_result is not None
    
    def test_error_handling_in_spec_kit_command(self):
        """测试spec.kit命令处理中的错误"""
        mock_skill_manager = Mock()
        mock_skill_manager.execute_spec_kit_command.side_effect = Exception("Test error")
        
        hook_system = HookSystem(mock_skill_manager)
        
        result = hook_system.intercept_request("/speckit.dnaspec.architect 设计系统")
        
        assert result.intercepted is True
        assert result.handled is False
        assert "Test error" in result.error_message
        assert result.processing_time >= 0
    
    def test_error_handling_in_natural_language_request(self):
        """测试自然语言请求处理中的错误"""
        mock_skill_manager = Mock()
        mock_skill_manager.execute_skill.side_effect = Exception("Execution error")
        
        # 设置匹配结果
        mock_match_result = {
            'skill_name': 'dnaspec-architect',
            'confidence': 0.8,
            'match_type': 'keyword'
        }
        
        mock_skill_manager.match_skill_intelligently.return_value = mock_match_result
        
        hook_system = HookSystem(mock_skill_manager)
        
        result = hook_system.intercept_request("设计一个系统架构")
        
        assert result.intercepted is True
        assert result.handled is False
        assert "Execution error" in result.error_message
        assert result.processing_time >= 0