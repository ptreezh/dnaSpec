"""
端到端功能验证脚本
"""
from src.dsgs_spec_kit_integration import (
    CommandParser,
    SkillMapper,
    PythonBridge,
    SkillExecutor,
    CommandHandler
)


def test_end_to_end():
    """
    测试端到端功能
    """
    print("开始端到端功能测试...")
    
    # 创建所有必要的组件
    parser = CommandParser()
    skill_mapper = SkillMapper()
    python_bridge = PythonBridge()
    skill_executor = SkillExecutor(python_bridge, skill_mapper)
    command_handler = CommandHandler(parser, skill_executor)
    
    # 测试命令解析
    print("\n1. 测试命令解析...")
    parsed = parser.parse('/speckit.dsgs.architect 电商系统设计')
    print(f"   解析结果: {parsed}")
    assert parsed['isValid'] == True
    assert parsed['skill'] == 'architect'
    assert parsed['params'] == '电商系统设计'
    print("   ✓ 命令解析测试通过")
    
    # 测试技能映射
    print("\n2. 测试技能映射...")
    mapped_skill = skill_mapper.map('architect')
    print(f"   映射结果: {mapped_skill}")
    assert mapped_skill == 'dsgs-architect'
    print("   ✓ 技能映射测试通过")
    
    # 测试技能执行
    print("\n3. 测试技能执行...")
    execution_result = skill_executor.execute('architect', '电商系统')
    print(f"   执行结果: {execution_result}")
    assert execution_result['success'] == True
    assert '[WebApp]' in execution_result['result']
    print("   ✓ 技能执行测试通过")
    
    # 测试完整命令处理
    print("\n4. 测试完整命令处理...")
    command_result = command_handler.handle_command('/speckit.dsgs.architect 博客系统')
    print(f"   完整处理结果: {command_result}")
    assert command_result['success'] == True
    assert '[WebApp]' in command_result['result']
    print("   ✓ 完整命令处理测试通过")
    
    print("\n✓ 所有端到端测试通过！")
    return True


def test_error_handling():
    """
    测试错误处理
    """
    print("\n开始错误处理测试...")
    
    command_handler = CommandHandler()
    
    # 测试无效命令
    print("\n1. 测试无效命令处理...")
    result = command_handler.handle_command('/invalid.command test')
    print(f"   无效命令处理结果: {result}")
    assert result['success'] == False
    print("   ✓ 无效命令处理测试通过")
    
    # 测试不存在的技能
    print("\n2. 测试不存在的技能...")
    result = command_handler.handle_command('/speckit.dsgs.nonexistent test')
    print(f"   不存在技能处理结果: {result}")
    assert result['success'] == False
    print("   ✓ 不存在技能处理测试通过")
    
    print("\n✓ 所有错误处理测试通过！")
    return True


def main():
    """
    主函数
    """
    print("DSGS端到端功能验证")
    print("="*50)
    
    try:
        test_end_to_end()
        test_error_handling()
        
        print("\n" + "="*50)
        print("🎉 所有测试通过！DSGS系统功能正常。")
        
        # 展示一些示例命令
        print("\n示例命令:")
        examples = [
            "/speckit.dsgs.architect 设计一个电商系统",
            "/speckit.dsgs.agent-creator 创建一个订单处理智能体",
            "/speckit.dsgs.task-decomposer 分解电商系统开发任务"
        ]
        for example in examples:
            print(f"  {example}")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    main()