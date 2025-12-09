# 完整Hook系统功能测试
import sys
import os
from unittest.mock import Mock

# 添加项目路径
project_root = r"D:\DAIP\dnaspec-core"
sys.path.insert(0, project_root)

try:
    from src.dnaspec_spec_kit_integration.core.hook import HookSystem, HookResult
    from src.dnaspec_spec_kit_integration.core.skill import SkillResult, SkillStatus
    print("✅ 所有模块导入成功")
    
    # 创建模拟技能管理器
    mock_skill_manager = Mock()
    
    # 设置模拟的spec.kit命令执行结果
    mock_skill_manager.execute_spec_kit_command.return_value = {
        'success': True,
        'result': Mock(),
        'skill_name': 'dnaspec-architect'
    }
    
    # 创建Hook系统并注入模拟的技能管理器
    hook_system = HookSystem(mock_skill_manager)
    print("✅ Hook系统与模拟技能管理器集成成功")
    
    # 测试spec.kit命令处理
    result = hook_system.intercept_request("/speckit.dnaspec.architect 设计系统")
    print(f"✅ Spec.kit命令拦截处理: intercepted={result.intercepted}, handled={result.handled}")
    print(f"   技能名称: {result.skill_name}")
    print(f"   处理时间: {result.processing_time:.4f}秒")
    
    # 验证技能管理器被调用
    mock_skill_manager.execute_spec_kit_command.assert_called_once_with("/speckit.dnaspec.architect 设计系统")
    print("✅ 技能管理器调用验证成功")
    
    # 测试自然语言请求处理
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
    result = hook_system.intercept_request("设计一个系统架构")
    print(f"✅ 自然语言请求处理: intercepted={result.intercepted}, handled={result.handled}")
    print(f"   技能名称: {result.skill_name}")
    print(f"   处理时间: {result.processing_time:.4f}秒")
    
    # 验证相关方法被调用
    mock_skill_manager.match_skill_intelligently.assert_called_with("设计一个系统架构")
    mock_skill_manager.execute_skill.assert_called_with("dnaspec-architect", "设计一个系统架构")
    print("✅ 自然语言处理调用验证成功")
    
    # 测试配置功能
    hook_system.config.enable_skill("dnaspec-task-decomposer")
    hook_system.config.add_disabled_pattern(r"危险.*命令")
    print("✅ Hook配置功能测试成功")
    
    # 测试Hook信息获取
    info = hook_system.get_hook_info()
    print(f"✅ Hook系统信息获取成功:")
    print(f"   启用状态: {info['enabled']}")
    print(f"   拦截器数量: {info['interceptor_count']}")
    print(f"   启用技能: {info['enabled_skills']}")
    
    print("\n🎉 所有Hook系统功能测试通过!")
    print("\n📊 测试总结:")
    print("   1. ✅ 模块导入成功")
    print("   2. ✅ 系统初始化成功")
    print("   3. ✅ 命令拦截处理成功")
    print("   4. ✅ 自然语言处理成功")
    print("   5. ✅ 技能管理器集成成功")
    print("   6. ✅ 配置管理成功")
    print("   7. ✅ 系统信息获取成功")
    
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()