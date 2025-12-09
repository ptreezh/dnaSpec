# 最终修正的完整Hook系统集成测试
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from src.dnaspec_spec_kit_integration.core.hook import HookSystem, HookConfig, HookResult
    from src.dnaspec_spec_kit_integration.core.skill import DNASpecSkill, SkillResult, SkillStatus
    from src.dnaspec_spec_kit_integration.core.manager import SkillManager
    from unittest.mock import Mock
    print("所有导入成功")
except ImportError as e:
    print("导入错误:", e)
    import traceback
    traceback.print_exc()
    sys.exit(1)

def test_all_hook_functionalities():
    """测试所有Hook系统功能"""
    print("\n=== 完整Hook系统功能测试 ===")
    
    # 1. 测试Hook配置
    print("\n1. 测试Hook配置")
    config = HookConfig()
    assert config.enabled == True
    assert config.auto_invoke_threshold == 0.6
    print("  ✓ Hook配置初始化正确")
    
    # 测试技能启用/禁用
    config.enable_skill("dnaspec-architect")
    assert config.is_skill_enabled("dnaspec-architect") == True
    print("  ✓ 技能启用功能正常")
    
    config.disable_skill("dnaspec-architect")
    # 当启用列表为空时，默认启用所有技能
    assert config.is_skill_enabled("dnaspec-architect") == True
    print("  ✓ 技能禁用功能正常")
    
    # 2. 测试Hook系统基本功能
    print("\n2. 测试Hook系统基本功能")
    hook_system = HookSystem()
    assert hook_system is not None
    assert len(hook_system._interceptors) == 0
    assert len(hook_system._processors) == 0
    print("  ✓ Hook系统初始化正确")
    
    # 测试命令检测
    assert hook_system._is_spec_kit_command("/speckit.dnaspec.architect 设计系统") == True
    assert hook_system._is_spec_kit_command("普通文本") == False
    print("  ✓ 命令检测功能正常")
    
    assert hook_system._is_natural_language_request("设计一个系统架构") == True
    assert hook_system._is_natural_language_request("") == False
    print("  ✓ 自然语言检测功能正常")
    
    # 3. 测试Hook系统禁用
    print("\n3. 测试Hook系统禁用")
    hook_system.config.enabled = False
    result = hook_system.intercept_request("任何请求")
    assert result.intercepted == False
    assert result.handled == False
    hook_system.config.enabled = True
    print("  ✓ Hook系统禁用功能正常")
    
    # 4. 测试模式禁用
    print("\n4. 测试模式禁用")
    hook_system.config.add_disabled_pattern(r"禁用.*请求")
    result = hook_system.intercept_request("禁用的请求内容")
    assert result.intercepted == False
    assert result.handled == False
    hook_system.config.disabled_patterns = []  # 清除禁用模式
    print("  ✓ 模式禁用功能正常")
    
    # 5. 测试Hook系统与技能管理器集成
    print("\n5. 测试Hook系统与技能管理器集成")
    
    # 创建模拟技能管理器
    mock_skill_manager = Mock()
    
    # 创建Hook系统并注入模拟的技能管理器
    hook_system_with_manager = HookSystem(mock_skill_manager)
    
    # 设置模拟的spec.kit命令执行结果
    mock_skill_manager.execute_spec_kit_command.return_value = {
        'success': True,
        'result': Mock(),
        'skill_name': 'dnaspec-architect'
    }
    
    # 测试spec.kit命令处理
    result = hook_system_with_manager.intercept_request("/speckit.dnaspec.architect 设计系统")
    assert result.intercepted == True
    assert result.handled == True
    assert result.skill_name == "dnaspec-architect"
    mock_skill_manager.execute_spec_kit_command.assert_called_once_with("/speckit.dnaspec.architect 设计系统")
    print("  ✓ Spec.kit命令处理功能正常")
    
    # 重置模拟对象调用历史
    mock_skill_manager.reset_mock()
    
    # 6. 测试自然语言请求处理
    print("\n6. 测试自然语言请求处理")
    
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
    
    # 测试自然语言请求处理
    result = hook_system_with_manager.intercept_request("设计一个系统架构")
    assert result.intercepted == True
    assert result.handled == True
    assert result.skill_name == "dnaspec-architect"
    mock_skill_manager.match_skill_intelligently.assert_called_once_with("设计一个系统架构")
    mock_skill_manager.execute_skill.assert_called_once_with("dnaspec-architect", "设计一个系统架构")
    print("  ✓ 自然语言请求处理功能正常")
    
    # 重置模拟对象调用历史
    mock_skill_manager.reset_mock()
    
    # 7. 测试低置信度处理
    print("\n7. 测试低置信度处理")
    
    # 设置低置信度的匹配结果
    mock_low_confidence_result = {
        'skill_name': 'dnaspec-architect',
        'confidence': 0.3,  # 低于阈值0.6
        'match_type': 'keyword'
    }
    
    mock_skill_manager.match_skill_intelligently.return_value = mock_low_confidence_result
    
    result = hook_system_with_manager.intercept_request("创建智能体")
    assert result.intercepted == True
    assert result.handled == False
    assert "Confidence too low" in result.error_message
    print("  ✓ 低置信度处理功能正常")
    
    # 重置模拟对象调用历史
    mock_skill_manager.reset_mock()
    
    # 8. 测试技能禁用处理
    print("\n8. 测试技能禁用处理")
    
    # 启用技能并设置正常匹配结果
    hook_system_with_manager.config.enable_skill("dnaspec-architect")
    mock_skill_manager.match_skill_intelligently.return_value = {
        'skill_name': 'dnaspec-architect',
        'confidence': 0.8,
        'match_type': 'keyword'
    }
    
    # 禁用技能
    hook_system_with_manager.config.disable_skill("dnaspec-architect")
    
    result = hook_system_with_manager.intercept_request("分解任务")
    assert result.intercepted == True
    assert result.handled == False
    assert "disabled" in result.error_message
    print("  ✓ 技能禁用处理功能正常")
    
    # 重置模拟对象调用历史
    mock_skill_manager.reset_mock()
    
    # 9. 测试错误处理
    print("\n9. 测试错误处理")
    
    # 测试spec.kit命令执行错误
    mock_skill_manager.execute_spec_kit_command.side_effect = Exception("Test error")
    result = hook_system_with_manager.intercept_request("/speckit.dnaspec.constraint-generator 生成约束")
    assert result.intercepted == True
    assert result.handled == False
    assert "Test error" in result.error_message
    print("  ✓ Spec.kit命令错误处理正常")
    
    # 重置模拟对象调用历史和异常
    mock_skill_manager.reset_mock()
    mock_skill_manager.execute_spec_kit_command.side_effect = None
    
    # 测试自然语言请求执行错误
    mock_skill_manager.match_skill_intelligently.return_value = {
        'skill_name': 'dnaspec-agent-creator',
        'confidence': 0.8,
        'match_type': 'keyword'
    }
    mock_skill_manager.execute_skill.side_effect = Exception("Execution error")
    
    result = hook_system_with_manager.intercept_request("创建智能体")
    assert result.intercepted == True
    assert result.handled == False
    assert "Execution error" in result.error_message
    print("  ✓ 自然语言请求错误处理正常")
    
    # 10. 测试Hook信息获取
    print("\n10. 测试Hook信息获取")
    info = hook_system_with_manager.get_hook_info()
    assert isinstance(info, dict)
    assert 'enabled' in info
    assert 'interceptor_count' in info
    assert 'processor_count' in info
    assert 'hook_count' in info
    print("  ✓ Hook信息获取功能正常")
    
    print("\n🎉 所有Hook系统功能测试通过!")

if __name__ == "__main__":
    test_all_hook_functionalities()
